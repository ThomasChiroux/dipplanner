#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011-2012 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/gpl.html>
#
# This module is part of dipplanner, a Dive planning Tool written in python
"""
Contains a Tank Class

.. note:: in MVPlan, this class was the 'Gas' class
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import logging
import math
import re
import json

# local imports
from dipplanner import settings
from dipplanner.dipp_exception import DipplannerException
from dipplanner.tools import pressure_to_depth, depth_to_pressure


class InvalidGas(DipplannerException):
    """Exception raised when the gas informations provided for the Tank
    are invalid
    """
    def __init__(self, description):
        """constructor : call the upper constructor and set the logger

        *Keyword Arguments:*
            :description: (str) -- text describing the error

        *Return:*
            <nothing>

        *Raise:*
            <nothing>
        """
        DipplannerException.__init__(self, description)
        self.logger = logging.getLogger(
            "dipplanner.DipplannerException.InvalidGas")
        self.logger.error(
            "Raising an exception: InvalidGas ! (%s)" % description)


class InvalidTank(DipplannerException):
    """Exception raised when the tank infos provided are invalid
    """
    def __init__(self, description):
        """constructor : call the upper constructor and set the logger

        *Keyword Arguments:*
            :description: (str) -- text describing the error

        *Return:*
            <nothing>

        *Raise:*
            <nothing>
        """
        DipplannerException.__init__(self, description)
        self.logger = logging.getLogger(
            "dipplanner.DipplannerException.InvalidTank")
        self.logger.error(
            "Raising an exception: InvalidTank ! (%s)" % description)


class InvalidMod(DipplannerException):
    """Exception raised when the given MOD is incompatible with the gas
    provided for the tank
    """
    def __init__(self, description):
        """constructor : call the upper constructor and set the logger

        *Keyword Arguments:*
            :description: (str) -- text describing the error

        *Return:*
            <nothing>

        *Raise:*
            <nothing>
        """
        DipplannerException.__init__(self, description)
        self.logger = logging.getLogger(
            "dipplanner.DipplannerException.InvalidMod")
        self.logger.error(
            "Raising an exception: InvalidMod ! (%s)" % description)


class EmptyTank(DipplannerException):
    """Exception raised when trying to consume more gas in tank than the
    remaining gas
    """
    def __init__(self, description):
        """constructor : call the upper constructor and set the logger

        *Keyword Arguments:*
            :description: (str) -- text describing the error

        *Return:*
            <nothing>

        *Raise:*
            <nothing>
        """
        DipplannerException.__init__(self, description)
        self.logger = logging.getLogger(
            "dipplanner.DipplannerException.EmptyTank")
        self.logger.error(
            "Raising an exception: EmptyTank ! (%s)" % description)


class Tank(object):
    """This class implements a representation of dive tanks wich
    contains breathing Gas
    We provide proportion of N2, O2, He, calculates MOD and volumes during the
    dives
    We can also (optionally) provide the type of tanks :

    - volume
    - pressure
    - remaining gas warning rule

    .. note:: About imperial unit conversion

        In 'imperial' countries (North America), it's common to describe
        a tank with the volume of air stored in the cylinder at its working
        pressure (if you where to release it at the surface),
        instead of (internal volume * pressure).

        This make difficult if not impossible to switch between the two units
        without any approximation or implementation choices.

        eg: 80-cubic-foot aluminium cylinder (AL80)

        TODO: continuer le texte explicatif

    *Attributes:*

        * f_o2 (float) -- fraction of oxygen in the gas in % (>= 0.0 & <= 1.0)
        * f_he (float) -- fraction of helium in the gas in % (>= 0.0 & <= 1.0)
        * f_n2 (float) -- fraction of nitrogen in the gas in %
                          (>= 0.0 & <= 1.0)
        * max_ppo2 (float) -- maximum tolerated ppo2 for this tank
        * tank_vol (float) -- volume of tank in liter
        * tank_pressure (float) -- pressure of tank in bar
        * tank_rule (str) -- tank rule for minimum gas calculation
        * mod (float) -- maximum operating depth of the tank
        * in_use (boolean) -- is the tank used for the dive of not
        * total_gas (float) -- total gas volume of the tank in liter
        * used_gas (float) -- used gas in liter
        * remaining_gas (float) -- remaining gas in liter
        * min_gas (float) -- minimum remaining gas in liter
        * given_name (str) -- name of the Tank if not provided,
                              try to set it automatically
    """

    def __init__(self,  f_o2=0.21, f_he=0.0,
                 max_ppo2=settings.DEFAULT_MAX_PPO2,
                 mod=None, tank_vol=12.0, tank_pressure=200,
                 tank_rule="30b",
                 given_name = None):
        """Constructor for Tank class

        If nothing is provided, create a default 'Air' with 12l/200b tank
        and max_ppo2 to 1.6 (used to calculate mod)
        if mod not provided, mod is calculed based on max tolerable ppo2

        *Keyword arguments:*
            :f_o2: (float) -- Fraction of O2 in the gaz in %
                              value between 0.0 and 1.0
            :f_he: (float) -- Fraction of He in the gaz in %
                              value between 0.0 and 1.0
            :max_ppo2: (float) -- sets the maximum ppo2 you want for this tank
                                  (default: settings.DEFAULT_MAX_PPO2)
            :mod: (float) -- Specify the mod you want.
                if not provided, calculates the mod based on max_ppo2

                if provided and not compatible
                  with max_ppo2: raise InvalidMod

            :tank_vol: (float) -- Volume of the tank in liter
            :tank_pressure: (float) -- Pressure of the tank, in bar
            :tank_rule: -- rule for warning in the tank consumption
                must be either : 'xxxb' or '1/x'.

                .. note:: xxxb (ex: 50b) means 50 bar minimum at
                          the end of the dive

                .. note:: 1/x (ex : 1/3 for rule of thirds:
                          1/3 for way in, 1/3 for way out,
                          1/3 remains at the end of the dive)

                          ex2: 1/6 rule: 1/6 way IN,1/6 way OUT, 2/3 remains

            :given_name: (str) -- set a specific name for the Tank.
                if not given, it will be generated automatically based
                on the gas.
        *Returns:*
            <nothing>

        *Raise:*

            * InvalidGas -- see validate()
            * InvalidMod -- if mod > max mod based on
                            max_ppo2 and see validate()
            * InvalidTank -- see validate()

        """
        #initiate class logger
        self.logger = logging.getLogger("dipplanner.tank.Tank")
        self.logger.debug("creating an instance of Tank: O2:%f, He:%f, "
                          "max_ppo2:%f, mod:%s, tank_vol:%f, "
                          "tank_pressure:%d" % (f_o2, f_he, max_ppo2,
                                                mod, tank_vol,
                                                tank_pressure))

        self.f_o2 = float(f_o2)
        self.f_he = float(f_he)
        self.f_n2 = 1.0 - (self.f_o2 + self.f_he)
        self.max_ppo2 = float(max_ppo2)
        self.tank_vol = float(tank_vol)
        self.tank_pressure = float(tank_pressure)
        self.tank_rule = tank_rule
        if mod is not None:
            if mod > self._calculate_mod(self.max_ppo2):
                raise InvalidMod(
                    "The mod exceed maximum MOD based on given max ppo2")
            self.mod = float(mod)
        else:
            self.mod = self._calculate_mod(self.max_ppo2)

        self.in_use = True
        if given_name is not None:
            self.given_name = given_name
        else:
            self.given_name = self.name()

        self._validate()

        self.used_gas = 0.0
        if self.tank_vol and self.tank_pressure:
            self.total_gas = self.calculate_real_volume()
        else:
            self.total_gas = 0.0
        self.remaining_gas = self.total_gas
        self._set_min_gas()

    def _set_min_gas(self):
        """sets the minimum gas volume for this tank based
        on the min_gas rule provided

        *Keyword Arguments:*
            <none>

        *Returns:*
            float -- minimum gas volume in liter

        *Raise:*
            <nothing>
        """
        min_re = re.search("([0-9]+)b", self.tank_rule)
        if min_re is not None:
            self.min_gas = self.calculate_real_volume(self.tank_vol,
                                                      int(min_re.group(1)))
        else:
            min_re = re.search("1/([0-9])", self.tank_rule)
            if min_re is not None:
                self.min_gas = self.total_gas * \
                    (float(1) - 2 * (1 / float(min_re.group(1))))
            else:
                self.min_gas = 0
        self.logger.debug("minimum gas authorised: %s" % self.min_gas)

    def __deepcopy__(self, memo):
        """deepcopy method will be called by copy.deepcopy

        Used for "cloning" the object into another new object.

        *Keyword Arguments:*
            :memo: -- not used here

        *Returns:*
            Tank -- Tank object copy of itself

        *Raise:*
            <nothing>
        """
        newobj = Tank()
        newobj.f_o2 = self.f_o2
        newobj.f_he = self.f_he
        newobj.f_n2 = self.f_n2
        newobj.max_ppo2 = self.max_ppo2
        newobj.tank_vol = self.tank_vol
        newobj.tank_pressure = self.tank_pressure
        newobj.mod = self.mod
        newobj.in_use = self.in_use
        newobj.used_gas = self.used_gas
        newobj.total_gas = self.total_gas
        newobj.remaining_gas = self.remaining_gas
        newobj.min_gas = self.min_gas
        return newobj

    def calculate_real_volume(self, tank_vol=None, tank_pressure=None,
                              f_o2=None, f_he=None, temp=15):
        """
        Calculate the real gas volume of the tank (in liter) based
        on Van der waals equation:
        (P+n2.a/V2).(V-n.b)=n.R.T

        *Keyword arguments:*
            :tank_vol: (float) -- Volume of the tank in liter
                    optional : if not provided, use self.tank_vol
            :tank_pressure: (float) -- Pressure of the tank in bar
                    optional : if not provided, use self.tank_pressure
            :f_o2: (float) -- fraction of O2 in the gas
                    optional : if not provided, use self.f_o2
            :f_he: (float) -- fraction of He in the gas
                    optional : if not provided, use self.f_he

        *Returns:*
            float -- total gas volume of the tank in liter

        *Raise:*
            <nothing>

        """
        # handle parameters
        if tank_vol is None:
            tank_vol = self.tank_vol
        if tank_pressure is None:
            tank_pressure = self.tank_pressure
        if f_o2 is None:
            f_o2 = self.f_o2
        if f_he is None:
            f_he = self.f_he
        f_n2 = 1.0 - (f_o2 + f_he)

        # Constants used in calculations
        a_o2 = 1.382
        b_o2 = 0.03186
        a_n2 = 1.37
        b_n2 = 0.0387
        a_he = 0.0346
        b_he = 0.0238
        #vm_o2 = 31.9988  # not used
        #vm_n2 = 28.01348  # not used
        #vm_he = 4.0020602  # not used
        R = 0.0831451
        T = 273.15 + temp  # default temp at 15°C

        # at first, calculate a and b values for this gas
        a_gas = math.sqrt(a_o2 * a_o2) * f_o2 * f_o2 +\
            math.sqrt(a_o2 * a_he) * f_o2 * f_he +\
            math.sqrt(a_o2 * a_n2) * f_o2 * f_n2 +\
            math.sqrt(a_he * a_o2) * f_he * f_o2 +\
            math.sqrt(a_he * a_he) * f_he * f_he +\
            math.sqrt(a_he * a_n2) * f_he * f_n2 +\
            math.sqrt(a_n2 * a_o2) * f_n2 * f_o2 +\
            math.sqrt(a_n2 * a_he) * f_n2 * f_he +\
            math.sqrt(a_n2 * a_n2) * f_n2 * f_n2
        #print "a: %s" % a_gas
        b_gas = math.sqrt(b_o2 * b_o2) * f_o2 * f_o2 +\
            math.sqrt(b_o2 * b_he) * f_o2 * f_he +\
            math.sqrt(b_o2 * b_n2) * f_o2 * f_n2 +\
            math.sqrt(b_he * b_o2) * f_he * f_o2 +\
            math.sqrt(b_he * b_he) * f_he * f_he +\
            math.sqrt(b_he * b_n2) * f_he * f_n2 +\
            math.sqrt(b_n2 * b_o2) * f_n2 * f_o2 +\
            math.sqrt(b_n2 * b_he) * f_n2 * f_he +\
            math.sqrt(b_n2 * b_n2) * f_n2 * f_n2
        #print "b: %s" % b_gas
        # now approximate n (quantities of molecules of gas in the tank in mol)
        # using perfect gas law : PV = nRT : n = PV/RT
        approx_n = (float(tank_pressure) * float(tank_vol)) / (R * T)

        # recalculate pressure on the tank whith approx_n
        # P=n.R.T/(V-n.b)-n2.a/V2)
        tank_pressure_mid = (approx_n * R * T) / (tank_vol - approx_n * b_gas)\
            - (approx_n * approx_n * a_gas)\
            / (tank_vol * tank_vol)

        # now try to approx tank_pressure with new_tank_pressure by
        # variating approx_n
        # start with *2 or /2 value (which is enormous !)
        if tank_pressure_mid < tank_pressure:
            n_left = approx_n
            n_right = approx_n * 2
        else:
            n_left = approx_n / 2
            n_right = approx_n

        n_mid = (n_left + n_right) / 2
        while round(tank_pressure_mid, 2) != round(tank_pressure, 2):
            n_mid = (n_left + n_right) / 2
            # new pressure calculated using:
            # P = nRT/(V - nb) - n2a/V2
            tank_pressure_mid = (n_mid * R * T) / (tank_vol - n_mid * b_gas) -\
                (n_mid * n_mid * a_gas) / (tank_vol * tank_vol)
            if tank_pressure_mid > tank_pressure:
                # keep left
                n_right = n_mid
            else:
                n_left = n_mid
        #print "n_mid:%s" % n_mid
        # recalculate volume using van der waals again
        # V = nR3T3/(PR2T2+aP2) + nb
        total_gas_volume = n_mid * pow(R, 3) * pow(T, 3) / \
            (settings.AMBIANT_PRESSURE_SURFACE * pow(R, 2) * pow(T, 2) +
             a_gas * pow(settings.AMBIANT_PRESSURE_SURFACE, 2)) + \
            n_mid * b_gas
        self.logger.debug("real total gas volume : %02fl instead of %02fl" %
                          (total_gas_volume, tank_vol * tank_pressure))
        return total_gas_volume

    def __repr__(self):
        """Returns a string representing the actual tank

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- representation of the tank in the form:
                   "Air - 12.0l-100.0% (2423.10/2423.10l)"

        *Raise:*
            <nothing>
        """
        return "%s - %s" % (self.name(), self.get_tank_info())

    def __str__(self):
        """Return a human readable name of the tank

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- name of the tank in the form:
                   "Air"
                   "Nitrox 80"
                   ...

        *Raise:*
            <nothing>
        """
        return "%s" % self.name()

    def __unicode__(self):
        """Return a human readable name of the tank in unicode

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- name of the tank in the form:
                   "Air"
                   "Nitrox 80"
                   ...

        *Raise:*
            <nothing>
        """
        return u"%s" % self.name()

    def __cmp__(self, othertank):
        """Compare a tank to another tank, based on MOD

        *Keyword arguments:*
            othertank (Tank) -- another tank object

        *Returns:*
            integer -- result of cmp()

        *Raise:*
            <nothing>
        """
        return cmp(self.mod, othertank.mod)

    def dumps_dict(self):
        """dumps the Tank object in json format

        *Keyword arguments:*
            <none>

        *Returns:*
            string -- json dumps of Tank object

        *Raise:*
            TypeError : if Tank is not serialisable
        """
        tank_dict = { 'given_name': self.given_name,
                      'name': self.name(),
                      'f_o2': self.f_o2,
                      'f_he': self.f_he,
                      'f_n2': self.f_n2,
                      'max_ppo2': self.max_ppo2,
                      'tank_vol': self.tank_vol,
                      'tank_pressure': self.tank_pressure,
                      'mod': self.mod,
                      'in_use': self.in_use,
                      'total_gas': self.total_gas,
                      'used_gas': self.used_gas,
                      'remaining_gas': self.remaining_gas,
                      'min_gas': self.min_gas,
                      'tank_rule': self.tank_rule }

        return tank_dict

    def loads_json(self, input_json):
        """loads a json structure and update the tank object with the new
        values.

        This method can be used in http PUT method to update object
        value

        *Keyword arguments:*
            :input_json: (string) -- the json structure to be loaded

        *Returns:*
            <none>

        *Raise:*
            * ValueError : if json is not loadable
            * InvalidGas -- When proportions of gas exceed
                      100% for example (or negatives values)
            * InvalidMod -- if mod > max mod based on max_ppo2
                            or ABSOLUTE_MAX_MOD.

                            ABSOLUTE_MAX_MOD is a global settings which
                            can not be exceeded.
            * InvalidTank -- when pressure or tank size exceed maximum
                      values or are incorrect (like negatives) values
        """
        if type(input_json) == str:
            tank_dict = json.loads(input_json)
        elif type(input_json) == dict:
            tank_dict = input_json
        else:
            raise TypeError("json must be either str or dict (%s given"
                            % type(input_json))

        if tank_dict.has_key('given_name'):
            self.given_name = tank_dict['given_name']
        if tank_dict.has_key('f_o2'):
            self.f_o2 = tank_dict['f_o2']
        if tank_dict.has_key('f_he'):
            self.f_he = tank_dict['f_he']
        if tank_dict.has_key('f_n2'):
            self.f_n2 = tank_dict['f_n2']
        if tank_dict.has_key('max_ppo2'):
            self.max_ppo2 = tank_dict['max_ppo2']
        if tank_dict.has_key('tank_rule'):
            self.tank_rule = tank_dict['tank_rule']
        if tank_dict.has_key('total_gas'):
            self.total_gas = tank_dict['total_gas']
        if tank_dict.has_key('used_gas'):
            self.used_gas = tank_dict['used_gas']
        if tank_dict.has_key('remaining_gas'):
            self.remaining_gas = tank_dict['remaining_gas']
        if tank_dict.has_key('min_gas'):
            self.min_gas = tank_dict['min_gas']
        if tank_dict.has_key('mod'):
            self.mod = tank_dict['mod']
        if tank_dict.has_key('in_use'):
            self.in_use = tank_dict['in_use']

        if tank_dict.has_key('tank_vol'):
            self.tank_vol = tank_dict['tank_vol']
            # tank_vol has changed, need to recalculate total_gas etc..
            self.total_gas = self.calculate_real_volume()
            self.remaining_gas = self.total_gas - self.used_gas
            self._set_min_gas()

        if tank_dict.has_key('tank_pressure'):
            self.tank_pressure = tank_dict['tank_pressure']
            # tank_pressure has changed: need to recalculate total_gas, etc..
            self.total_gas = self.calculate_real_volume()
            self.remaining_gas = self.total_gas - self.used_gas
            self._set_min_gas()

        self._validate()
        return self

    def _calculate_mod(self, max_ppo2):
        """calculate and returns mod for a given ppo2 based on this tank info
        result in meter

        *Keyword arguments:*
            :max_ppo2: -- maximum ppo2 accepted (float).
                Any value accepted, but should be > 0.0

        *Returns:*
            integer -- Maximum Operating Depth in meter

        *Raise:*
            <nothing>
        """
        return max(int(10 * (float(max_ppo2) / self.f_o2) - 10), 0)

    def _validate(self):
        """Test the validity of the tank informations inside this object
        if validity check fails raise an Exception 'InvalidTank'

        *Keyword arguments:*
            <nothing>

        *Returns:*
            <nothing>

        *Raise:*
            * InvalidGas -- When proportions of gas exceed
                      100% for example (or negatives values)
            * InvalidMod -- if mod > max mod based on max_ppo2
                            or ABSOLUTE_MAX_MOD.

                            ABSOLUTE_MAX_MOD is a global settings which
                            can not be exceeded.
            * InvalidTank -- when pressure or tank size exceed maximum
                      values or are incorrect (like negatives) values
        """
        if self.f_o2 + self.f_he > 1:
            raise InvalidGas("Proportion of O2+He is more than 100%")
        if self.f_o2 + self.f_he + self.f_n2 != 1:
            raise InvalidGas("Proportion of O2+He+N2 is not 100%")
        if self.f_o2 < 0 or self.f_he < 0 or self.f_n2 < 0:
            raise InvalidGas("Proportion of gas should not be < 0")
        if self.mod <= 0:
            raise InvalidMod("MOD should be >= 0")
        if (self.mod > self._calculate_mod(self.max_ppo2) or
                self.mod > self._calculate_mod(settings.ABSOLUTE_MAX_PPO2)):
            raise InvalidMod("MOD exceed maximum tolerable MOD")

        if self.tank_pressure > settings.ABSOLUTE_MAX_TANK_PRESSURE:
            raise InvalidTank(
                "Tank pressure exceed maximum tolerable pressure")
        if self.tank_pressure <= 0:
            raise InvalidTank("Tank pressure should be greated than zero")
        if self.tank_vol > settings.ABSOLUTE_MAX_TANK_SIZE:
            raise InvalidTank("Tank size exceed maximum tolerable tank size")
        if self.tank_vol <= 0:
            raise InvalidTank("Tank size should be greater than zero")

    def name(self):
        """returns a Human readable name for the gaz and tanks
        Differnt possibilities:
        Air, Nitrox, Oxygen, Trimix, Heliox

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- name of the tank in the form:
                   "Air"
                   "Nitrox"
                   ...

        *Raise:*
            <nothing>
        """
        name = 'Air'
        composition = ''
        if self.f_he == 0:
            composition = '%s' % int(self.f_o2 * 100)
            if self.f_o2 == 0.21:
                name = 'Air'
            elif self.f_o2 == 1:
                name = 'Oxygen'
            else:
                name = 'Nitrox ' + composition
        else:
            composition = '%s/%s' % (int(self.f_o2 * 100),
                                     int(self.f_he * 100))
            if self.f_he + self.f_o2 == 1:
                name = 'Heliox ' + composition
            else:
                name = 'Trimix ' + composition
        return name

    def get_tank_info(self):
        """returns tank infos : size, remaining vol
        example of tank info:
        15l-90% (2800/3000l)

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- infos of the tank in the form:
                   "12.0l-100.0% (2423.10/2423.10l)"
                   ...

        *Raise:*
            <nothing>
        """
        if self.total_gas > 0:
            return "%sl-%s%% (%02.02f/%02.02fl)" % (
                self.tank_vol,
                round(100 * self.remaining_gas / self.total_gas, 1),
                self.remaining_gas,
                self.total_gas)
        else:
            return "(no tank info, used:%sl)" % self.used_gas

    def get_mod(self, max_ppo2=None):
        """return mod (maximum operating depth) in meter
        if no argument provided, return the mod based on the current tank (and
        configured max_ppo2)
        if max_ppo2 is provided, returns the (new) mod based on the given ppo2

        *Keyword arguments:*
            :max_ppo2: (float) -- ppo2 for mod calculation

        *Returns:*
            float -- mod in meter

        *Raise:*
            <nothing>
        """
        if not max_ppo2:
            return self.mod
        else:
            return self._calculate_mod(max_ppo2)

    def get_min_od(self, min_ppo2=settings.ABSOLUTE_MIN_PPO2):
        """return in meter the minimum operating depth for the gas in the tank
        return 0 if diving from/to surface is ok with this gaz

        *Keyword arguments:*
            :min_ppo2: (float) -- minimum tolerated ppo2

        *Returns:*
            float -- minimum operating depthin meter

        *Raise:*
            <nothing>
        """
        return self._calculate_mod(min_ppo2)

    def get_mod_for_given_end(self, end):
        """calculate a mod based on given end and based on gaz inside the tank

        .. note::
            end calculation is based on narcotic index for all gases.

            By default, dipplanner considers that oxygen is narcotic
            (same narcotic index than nitrogen)

            All narcotic indexes can by changed in the config file,
            in the [advanced] section

        *Keyword arguments:*
            :end: (int) -- equivalent narcotic depth in meter

        *Returns:*
            int -- mod: depth in meter based on given end

        *Raise:*
            <nothing>
        """
        # calculate the reference narcotic effect of air
        # Air consists of: Nitrogen N2: 78.08%,
        #                  Oxygen O2: 20.95%,
        #                  Argon Ar: 0.934%
        #OC
        reference_narcotic = settings.AMBIANT_PRESSURE_SURFACE * \
            (settings.N2_NARCOTIC_VALUE * 0.7808 +
             settings.O2_NARCOTIC_VALUE * 0.2095 +
             settings.AR_NARCOTIC_VALUE * 0.00934)
        #OC mode
        narcotic_tank = (self.f_n2 * settings.N2_NARCOTIC_VALUE +
                         self.f_o2 * settings.O2_NARCOTIC_VALUE +
                         self.f_he * settings.HE_NARCOTIC_VALUE)

        p_absolute = (depth_to_pressure(end) +
                      settings.AMBIANT_PRESSURE_SURFACE) * \
            reference_narcotic / narcotic_tank
        mod = pressure_to_depth(p_absolute - settings.AMBIANT_PRESSURE_SURFACE)
        return mod

    def get_end_for_given_depth(self, depth):
        """calculate end (equivalent narcotic depth)
        based on given depth and based on gaz inside the tank

        .. note::
            end calculation is based on narcotic index for all gases.

            By default, dipplanner considers that oxygen is narcotic
            (same narcotic index than nitrogen)

            All narcotic indexes can by changed in the config file,
            in the [advanced] section

        *Keyword arguments:*
            depth -- int -- in meter

        *Returns:*
            end -- int -- equivalent narcotic depth in meter

        *Raise:*
            <nothing>
        """
        p_absolute = depth_to_pressure(depth) + \
            settings.AMBIANT_PRESSURE_SURFACE
        # calculate the reference narcotic effect of air
        # Air consists of: Nitrogen N2: 78.08%,
        #                  Oxygen O2: 20.95%,
        #                  Argon Ar: 0.934%
        reference_narcotic = settings.AMBIANT_PRESSURE_SURFACE * \
            (settings.N2_NARCOTIC_VALUE * 0.7808 +
             settings.O2_NARCOTIC_VALUE * 0.2095 +
             settings.AR_NARCOTIC_VALUE * 0.00934)
        #OC mode
        narcotic_index = p_absolute * (self.f_n2 * settings.N2_NARCOTIC_VALUE +
                                       self.f_o2 * settings.O2_NARCOTIC_VALUE +
                                       self.f_he * settings.HE_NARCOTIC_VALUE)

        end = pressure_to_depth(narcotic_index / reference_narcotic -
                                settings.AMBIANT_PRESSURE_SURFACE)
        if end < 0:
            end = 0
        return end

    def consume_gas(self, gas_consumed):
        """Consume gas inside this tank

        *Keyword arguments:*
            :gas_consumed: (float) -- gas consumed in liter

        *Returns:*
            float -- remaining gas in liter

        *Raise:*
            <nothing>
        """
        #if self.remaining_gas - gas_consumed < 0:
            #raise EmptyTank("There is not enought gas in this tank")
        #else:
        self.used_gas += gas_consumed
        self.remaining_gas -= gas_consumed
        return self.remaining_gas

    def refill(self):
        """Refill the tank

         *Keyword arguments:*
            <none>

        *Returns:*
            float -- remaining gas in liter

        *Raise:*
            <nothing>
        """
        self.used_gas = 0
        self.remaining_gas = self.total_gas
        return self.remaining_gas

    def check_rule(self):
        """Checks the rule agains the remaining gas in the tank

        *Keyword arguments:*
            :gas_consumed: (float) -- gas consumed in liter

        *Returns:*
            bool -- True is rule OK
                    False if rule Not OK

        *Raise:*
            <nothing>
        """
        if self.remaining_gas < self.min_gas:
            return False
        else:
            return True
