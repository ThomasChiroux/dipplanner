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
from dipplanner.tools import (pressure_to_depth, depth_to_pressure,
                              safe_eval_calculator)


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
        * volume (float) -- volume of tank in liter
        * pressure (float) -- pressure of tank in bar
        * rule (str) -- tank rule for minimum gas calculation
        * mod (float) -- maximum operating depth of the tank
        * in_use (boolean) -- is the tank used for the dive of not
        * total_gas (float) -- total gas volume of the tank in liter
        * used_gas (float) -- used gas in liter
        * remaining_gas (float) -- remaining gas in liter
        * min_gas (float) -- minimum remaining gas in liter
        * name (str) -- name of the Tank if not provided,
                              try to set it automatically
    """

    def __init__(self,  f_o2=0.21, f_he=0.0,
                 max_ppo2=settings.DEFAULT_MAX_PPO2,
                 mod=None, volume=12.0, pressure=200,
                 rule="30b",
                 name=None):
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

            :volume: (float) -- Volume of the tank in liter
            :pressure: (float) -- Pressure of the tank, in bar
            :rule: -- rule for warning in the tank consumption
                must be either : 'xxxb' or '1/x'.

                .. note:: xxxb (ex: 50b) means 50 bar minimum at
                          the end of the dive

                .. note:: 1/x (ex : 1/3 for rule of thirds:
                          1/3 for way in, 1/3 for way out,
                          1/3 remains at the end of the dive)

                          ex2: 1/6 rule: 1/6 way IN,1/6 way OUT, 2/3 remains

            :name: (str) -- set a specific name for the Tank.
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
                          "max_ppo2:%f, mod:%s, volume:%f, "
                          "pressure:%d" % (f_o2, f_he, max_ppo2,
                                                mod, volume,
                                                pressure))

        self.f_o2 = float(f_o2)
        self.f_he = float(f_he)
        self.f_n2 = 1.0 - (self.f_o2 + self.f_he)
        self.max_ppo2 = float(max_ppo2)
        self.volume = float(volume)
        self.pressure = float(pressure)
        self.rule = rule
        if mod is not None:
            if mod > self._calculate_mod(self.max_ppo2):
                raise InvalidMod(
                    "The mod exceed maximum MOD based on given max ppo2")
            self.mod = float(mod)
        else:
            self.mod = self._calculate_mod(self.max_ppo2)

        self.in_use = True
        if name is not None:
            self.name = name
        else:
            self.name = self.automatic_name()

        self._validate()

        self.used_gas = 0.0
        if self.volume and self.pressure:
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
        min_re = re.search("([0-9]+)b", self.rule)
        if min_re is not None:
            self.min_gas = self.calculate_real_volume(self.volume,
                                                      int(min_re.group(1)))
        else:
            min_re = re.search("1/([0-9])", self.rule)
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
        newobj.volume = self.volume
        newobj.pressure = self.pressure
        newobj.mod = self.mod
        newobj.in_use = self.in_use
        newobj.used_gas = self.used_gas
        newobj.total_gas = self.total_gas
        newobj.remaining_gas = self.remaining_gas
        newobj.min_gas = self.min_gas
        return newobj

    def calculate_real_volume(self, volume=None, pressure=None,
                              f_o2=None, f_he=None, temp=15):
        """
        Calculate the real gas volume of the tank (in liter) based
        on Van der waals equation:
        (P+n2.a/V2).(V-n.b)=n.R.T

        *Keyword arguments:*
            :volume: (float) -- Volume of the tank in liter
                    optional : if not provided, use self.volume
            :pressure: (float) -- Pressure of the tank in bar
                    optional : if not provided, use self.pressure
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
        if volume is None:
            volume = self.volume
        if pressure is None:
            pressure = self.pressure
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

        b_gas = math.sqrt(b_o2 * b_o2) * f_o2 * f_o2 +\
            math.sqrt(b_o2 * b_he) * f_o2 * f_he +\
            math.sqrt(b_o2 * b_n2) * f_o2 * f_n2 +\
            math.sqrt(b_he * b_o2) * f_he * f_o2 +\
            math.sqrt(b_he * b_he) * f_he * f_he +\
            math.sqrt(b_he * b_n2) * f_he * f_n2 +\
            math.sqrt(b_n2 * b_o2) * f_n2 * f_o2 +\
            math.sqrt(b_n2 * b_he) * f_n2 * f_he +\
            math.sqrt(b_n2 * b_n2) * f_n2 * f_n2

        # now approximate n (quantities of molecules of gas in the tank in mol)
        # using perfect gas law : PV = nRT : n = PV/RT
        approx_n = (float(pressure) * float(volume)) / (R * T)

        # recalculate pressure on the tank whith approx_n
        # P=n.R.T/(V-n.b)-n2.a/V2)
        pressure_mid = (approx_n * R * T) / (volume - approx_n * b_gas)\
            - (approx_n * approx_n * a_gas)\
            / (volume * volume)

        # now try to approx pressure with new_pressure by
        # variating approx_n
        # start with *2 or /2 value (which is enormous !)
        if pressure_mid < pressure:
            n_left = approx_n
            n_right = approx_n * 2
        else:
            n_left = approx_n / 2
            n_right = approx_n

        n_mid = (n_left + n_right) / 2
        while round(pressure_mid, 2) != round(pressure, 2):
            n_mid = (n_left + n_right) / 2
            # new pressure calculated using:
            # P = nRT/(V - nb) - n2a/V2
            pressure_mid = (n_mid * R * T) / (volume - n_mid * b_gas) -\
                (n_mid * n_mid * a_gas) / (volume * volume)
            if pressure_mid > pressure:
                # keep left
                n_right = n_mid
            else:
                n_left = n_mid

        # recalculate volume using van der waals again
        # V = nR3T3/(PR2T2+aP2) + nb
        total_gas_volume = n_mid * pow(R, 3) * pow(T, 3) / \
            (settings.AMBIANT_PRESSURE_SURFACE * pow(R, 2) * pow(T, 2) +
             a_gas * pow(settings.AMBIANT_PRESSURE_SURFACE, 2)) + \
            n_mid * b_gas
        self.logger.debug("real total gas volume : %02fl instead of %02fl" %
                          (total_gas_volume, volume * pressure))
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
        if self.name != self.automatic_name():
            return "%s (%s) - %s" % (self.name,
                                     self.automatic_name(),
                                     self.get_tank_info())
        else:
            return "%s - %s" % (self.name, self.get_tank_info())

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
        if self.name != self.automatic_name():
            return "%s (%s)" % (self.name, self.automatic_name())
        else:
            return "%s" % self.name

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
        return u"%s" % self.__str__()

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
        tank_dict = {'name': self.name,
                     'automatic_name': self.automatic_name(),
                     'f_o2': self.f_o2,
                     'f_he': self.f_he,
                     'f_n2': self.f_n2,
                     'max_ppo2': self.max_ppo2,
                     'volume': self.volume,
                     'pressure': self.pressure,
                     'mod': self.mod,
                     'in_use': self.in_use,
                     'total_gas': self.total_gas,
                     'used_gas': self.used_gas,
                     'remaining_gas': self.remaining_gas,
                     'min_gas': self.min_gas,
                     'rule': self.rule}

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

        if 'name' in tank_dict:
            self.name = tank_dict['name']
        if 'f_o2' in tank_dict:
            self.f_o2 = float(safe_eval_calculator(tank_dict['f_o2']))
        else:
            if 'f_n2' in tank_dict and 'f_he' in tank_dict:
                self.f_o2 = 1 - (self.f_n2 + self.f_he)
            else:
                raise InvalidTank("Need at least two gas to instanciate a Tank")
        if 'f_he' in tank_dict:
            self.f_he = float(safe_eval_calculator(tank_dict['f_he']))
        else:
            if 'f_o2' in tank_dict and 'f_n2' in tank_dict:
                self.f_he = 1 - (self.f_o2 + self.f_n2)
            else:
                raise InvalidTank("Need at least two gas to instanciate a Tank")
        if 'f_n2' in tank_dict:
            self.f_n2 = float(safe_eval_calculator(tank_dict['f_n2']))
        else:
            if 'f_o2' in tank_dict and 'f_he' in tank_dict:
                self.f_n2 = 1 - (self.f_o2 + self.f_he)
            else:
                raise InvalidTank("Need at least two gas to instanciate a Tank")
        if 'max_ppo2' in tank_dict:
            self.max_ppo2 = float(safe_eval_calculator(tank_dict['max_ppo2']))
        if 'rule' in tank_dict:
            self.rule = tank_dict['rule']
        if 'total_gas' in tank_dict:
            self.total_gas = float(tank_dict['total_gas'])
        if 'used_gas' in tank_dict:
            self.used_gas = float(tank_dict['used_gas'])
        if 'remaining_gas' in tank_dict:
            self.remaining_gas = float(tank_dict['remaining_gas'])
        if 'min_gas' in tank_dict:
            self.min_gas = float(tank_dict['min_gas'])
        if 'mod' in tank_dict:
            if tank_dict['mod'] == 'auto':
                self.mod = self._calculate_mod(self.max_ppo2)
            else:
                self.mod = float(tank_dict['mod'])
        else:
            self.mod = self._calculate_mod(self.max_ppo2)
        if 'in_use' in tank_dict:
            self.in_use = bool(tank_dict['in_use'])

        if 'volume' in tank_dict:
            self.volume = float(safe_eval_calculator(tank_dict['volume']))
            # volume has changed, need to recalculate total_gas etc..
            self.total_gas = self.calculate_real_volume()
            self.remaining_gas = self.total_gas - self.used_gas
            self._set_min_gas()

        if 'pressure' in tank_dict:
            self.pressure = float(safe_eval_calculator(
                tank_dict['pressure']))
            # pressure has changed: need to recalculate total_gas, etc..
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

        if self.pressure > settings.ABSOLUTE_MAX_TANK_PRESSURE:
            raise InvalidTank(
                "Tank pressure exceed maximum tolerable pressure")
        if self.pressure <= 0:
            raise InvalidTank("Tank pressure should be greated than zero")
        if self.volume > settings.ABSOLUTE_MAX_TANK_SIZE:
            raise InvalidTank("Tank size exceed maximum tolerable tank size")
        if self.volume <= 0:
            raise InvalidTank("Tank size should be greater than zero")

    def automatic_name(self):
        """returns a Human readable name for the gaz and tanks
        Different possibilities:
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
                self.volume,
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
