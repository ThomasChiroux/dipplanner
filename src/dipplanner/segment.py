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

"""Segment classes
A segment is a portion of a dive in the same depth (depth + duration)
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import logging
import json
# local import
from dipplanner import settings
from dipplanner.dipp_exception import DipplannerException
from dipplanner.tools import seconds_to_mmss
from dipplanner.tools import (depth_to_pressure, pressure_to_depth,
                              safe_eval_calculator)


class UnauthorizedMod(DipplannerException):
    """raised when the MOD is not possible according to the
    depth(s) of the segment"""

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
            "dipplanner.DipplannerException.UnauthorizedMod")
        self.logger.error(
            "Raising an exception: UnauthorizedMod ! (%s)" % description)


class Segment(object):
    """Base class for all types of segments

    *Attributes:*
        * dive (Dive) -- Dive object the segment belongs to
        * type (str) -- type of segment

          types of segments can be :

          * const = "Constant Depth"
          * ascent = "Ascent"
          * descent = "Descent"
          * deco = "Decompression"
          * waypoint = "Waypoint"
          * surf = "Surface"
        * in_use (boolean) -- True if segment is used
        * depth (float) -- depth of this segment, in meter
        * time (float) -- duration of this segment, in seconds
        * run_time (float) -- runtime (displayed in profile informations)
        * setpoint (float) -- setpoint for CCR
        * tank (Tank) -- refer to tank object used in this segment

    """
    types = ['const', 'ascent', 'descent', 'deco', 'waypoint', 'surf']

    def __init__(self):
        """constructor for Segment base class, just defines all the parameters

        *Keyword arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        #initiate class logger
        self.logger = logging.getLogger("dipplanner.segment.Segment")
        #self.logger.debug("creating an instance of Segment")
        self.dive = None
        self.type = None  # type of segment : base class has no type
        self.in_use = True  # is this segment in use : default: yes
        self.depth = 0.0  # depth of this segment, in meter
        self.time = 0.0  # time of this segment, in second
        self.run_time = 0.0  # runtime in profile
        self.setpoint = 0.0  # for CCR
        self.tank = None  # tank used for this segment

    def __repr__(self):
        """Returns a string representing the actual segment

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- representation of the segment in the form:
            "   CONST: at 150m for  10:00 [RT:  0:00], on Trimix 10/70,  SP:0.0, END:61m"

        *Raise:*
            <nothing>

        """
        return "%8s: at %3dm for %s [RT:%s], on %s,  SP:%s, END:%im" % (
            self.type.upper(),
            self.depth,
            self.get_time_str(),
            self.get_run_time_str(),
            str(self.tank),
            self.setpoint,
            self.get_end())

    def __str__(self):
        """Return a human readable name of the segment

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- representation of the segment in the form:
            (see __repr__)

        *Raise:*
            <nothing>
        """
        return self.__repr__()

    def __unicode__(self):
        """Return a human readable name of the segment in unicode

        *Keyword arguments:*
            <none>

        *Returns:*
            str -- representation of the segment in the form:
            (see __repr__)

        *Raise:*
            <nothing>
        """
        return u"%s" % self.__repr__()

    def dumps_dict(self):
        """dumps the Segment object in json format

        *Keyword arguments:*
            <none>

        *Returns:*
            string -- json dumps of Segment object

        *Raise:*
            TypeError : if Tank is not serialisable
        """
        current_tank_name = ""
        if self.tank is not None:
            current_tank_name = self.tank.name
        segment_dict = {'type': self.type,
                        'in_use': self.in_use,
                        'depth': self.depth,
                        'time':  self.time,
                        'run_time': self.run_time,
                        'setpoint': self.setpoint,
                        'tank': current_tank_name}

        return segment_dict

    def loads_json(self, input_json):
        """loads a json structure and update the segment object with the new
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
            segment_dict = json.loads(input_json)
        elif type(input_json) == dict:
            segment_dict = input_json
        else:
            raise TypeError("json must be either str or dict (%s given"
                            % type(input_json))

        if 'type' in segment_dict:
            #TODO: type validation
            self.type = segment_dict['type']
        if 'in_use' in segment_dict:
            self.in_use = bool(segment_dict['in_use'])
        if 'depth' in segment_dict:
            self.depth = float(segment_dict['depth'])
        if 'time' in segment_dict:
            self.time = float(safe_eval_calculator(segment_dict['time']))
        if 'run_time' in segment_dict:
            self.run_time = float(segment_dict['run_time'])
        if 'setpoint' in segment_dict:
            self.setpoint = float(segment_dict['setpoint'])
        if 'tank' in segment_dict:  # tank name, needs to find it in dive.tanks
            segment_dict['tank'] = segment_dict['tank'].strip()
            if self.dive is not None:
                if segment_dict['tank'] in \
                        [tank.name for tank in self.dive.tanks]:
                    # small hack here: we know the tank is in dive, so it's
                    # also present in the mission which has a tank dict instead
                    # of tank list which is more convenient to use
                    self.tank = self.dive.mission.tanks[segment_dict['tank']]
                else:
                    self.logger.warning("Tank not found in current dive: %s"
                                        % segment_dict['tank'])
            else:
                # self.dive is not yet known
                # (segment not yet associated to a dive)
                # in this case, we only store tank name in self.tank
                self.tank = segment_dict['tank']
            # TODO: add a new method to refind the tank when association with dive is done.

        return self

    def check(self):
        """check if it's a valid segment
        Should be executed before calculating dives

        the check does not return anything if nok, but raises Exceptions

        *Keyword arguments:*
            <none>

        *Returns:*
            True (bool) -- if check is ok

        *Raise:*
            <DiveExceptions>

        """
        if self.setpoint == 0:
            # check MOD only if OC
            self.check_mod()
            self.check_min_od()
        else:
            self.check_mod(self.setpoint)
        return True

    def check_mod(self,  max_ppo2=None):
        """checks the mod for this segment according to the used tank.

        *Keyword arguments:*
            :max_ppo2: (float) -- max tolerated ppo2

        *Returns:*
            True (bool) -- if check is ok

        *Raise:*
            UnauthorizedMod -- if segments goes below max mod or upper min mod
        """
        if self.depth > self.tank.get_mod(max_ppo2):
            raise UnauthorizedMod("depth is exceeding the maximum MOD")
        return True

    def check_min_od(self):
        """checks the minimum od for this segment according to the used tank.
        (hypoxic cases)

        *Keyword arguments:*
            <none>

        *Returns:*
            True (bool) -- if check is ok

        *Raise:*
            UnauthorizedMod -- if segments goes below max mod or upper min mod
        """
        if self.depth < self.tank.get_min_od():  # checks mini operating depth
            raise UnauthorizedMod("depth is too low for the minimum MOD")
        return True

    def get_time_str(self):
        """returns segment time in the form MMM:SS

        *Keyword Arguments:*
            <none>

        *Returns:*
            string -- segment time in the form MMM:SS

        *Raise:*
            <nothing>
        """
        return seconds_to_mmss(self.time)

    def get_run_time_str(self):
        """returns runtime in the form MMM:SS

        *Keyword Arguments:*
            <none>

        *Returns:*
            string -- segment time in the form MMM:SS

        *Raise:*
            <nothing>
        """
        return seconds_to_mmss(self.run_time)

    def get_p_absolute(self, method=settings.METHOD_FOR_DEPTH_CALCULATION):
        """returns the absolute pression in bar
        (1atm = 1ATA = 1.01325 bar = 14.70psi)

        Simple method : 10m = +1 bar
        Complex method : use real density of water, T°, etc...

        *Keyword arguments:*
            method -- 'simple' or 'complex'

        *Returns:*
            float -- indicating the absolute pressure in bar

        *Raise:*
            ValueError -- when providing a bad method
        """
        if method == 'simple':
            return float(self.depth) / 10 + settings.AMBIANT_PRESSURE_SURFACE
        elif method == 'complex':
            return depth_to_pressure(self.depth) + \
                settings.AMBIANT_PRESSURE_SURFACE
        else:
            raise ValueError("invalid method of calculation")

    def get_end(self):
        """Calculates and returns E.N.D :
        Equivalent Narcosis Depth

        Instead of Mvplan, it uses a 'calculation method' based on
        narcosis effet of all gas used, assuming there is no trace of
        other gases (like argon) in the breathing gas, but compare the narcotic
        effect with surface gas, wich is 'air' and contains
        a small amount of argon

        *Keyword arguments:*
            <none>

        *Returns:*
            integer -- Equivalent Narcosis Depth in meter

        *Raise:*
            <nothing>
        """
        #TODO: refactor with get_end_for_given_depth in Tank
        p_absolute = self.get_p_absolute()
        # calculate the reference narcotic effect of air
        # Air consists of: Nitrogen N2: 78.08%,
        #                  Oxygen O2: 20.95%,
        #                  Argon Ar: 0.934%
        reference_narcotic = settings.AMBIANT_PRESSURE_SURFACE * \
            (settings.N2_NARCOTIC_VALUE * 0.7808 +
             settings.O2_NARCOTIC_VALUE * 0.2095 +
             settings.AR_NARCOTIC_VALUE * 0.00934)

        if self.setpoint > 0:
            #CCR mode
            f_inert = self.tank.f_he + self.tank.f_n2
            if f_inert > 0:
                pp_inert = p_absolute - self.setpoint
            else:
                pp_inert = 0
            if pp_inert > 0:
                # sort of approximation here ?
                # calculate here a narcotic index based on the proportion
                # of innertgases in the dilluent tank
                # should (perhaps) calculate based on proportion
                # of innert gases inthe loop ?
                ppn2_inspired = (pp_inert * self.tank.f_n2) / f_inert
                pphe_inspired = (pp_inert * self.tank.f_he) / f_inert
                narcotic_index = (ppn2_inspired * settings.N2_NARCOTIC_VALUE +
                                  self.setpoint * settings.O2_NARCOTIC_VALUE +
                                  pphe_inspired * settings.HE_NARCOTIC_VALUE)

                self.logger.debug("pabs: %.3f, pp_inert: %.3f at %sm, "
                                  "ppn2i:%s, pphei:%s, narco idx:%s" %
                                  (p_absolute, pp_inert,
                                   self.depth, ppn2_inspired,
                                   pphe_inspired, narcotic_index))
            else:
                narcotic_index = 0
        else:
            #OC mode
            narcotic_index = p_absolute * \
                (self.tank.f_n2 * settings.N2_NARCOTIC_VALUE +
                 self.tank.f_o2 * settings.O2_NARCOTIC_VALUE +
                 self.tank.f_he * settings.HE_NARCOTIC_VALUE)
        end = pressure_to_depth(narcotic_index / reference_narcotic -
                                settings.AMBIANT_PRESSURE_SURFACE)
        if end < 0:
            end = 0
        return end

    def gas_used(self):
        """returns the quantity (in liter) of gas used for this segment

        (this method is empty)
        """
        pass


class SegmentDive(Segment):
    """Specialisation of segment class for dive segments
    """
    def __init__(self, depth=None, time=None, tank=None, setpoint=0):
        """Constructor for SegmentDive class.
        Look at base class for more explanations

        *Keyword arguments:*
            :depth: (float) -- in meter, the (constant) depth for this segment
            :time: (float) -- in second, duration of this segment
            :tank: (Tank) -- object instance of Tank class :
                             describe the tank used in this segment
            :setpoint: (float) -- for CCR, setpoint used for this segment
                                  for OC : setpoint should be zero

        *Returns:*
            <nothing>

        *Raise:*
            UnauthorizedMod -- if depth is incompatible
                               with either min or max mod

        """
        Segment.__init__(self)
        #initiate class logger
        self.logger = logging.getLogger("dipplanner.segment.SegmentDive")
        self.logger.debug("creating an instance of SegmentDive: \
    depth:%s, time:%ss, tank:%s, sp:%f" % (depth, time, tank, setpoint))

        self.type = 'const'  # type of segment
        self.in_use = True  # is this segment in use : default: yes
        if depth is not None:
            self.depth = float(depth)  # depth of this segment, in meter
        if time is not None:
            self.time = float(time)  # time of this segment, in second
        if setpoint is not None:
            self.setpoint = float(setpoint)  # for CCR
        if tank is not None:
            self.tank = tank  # tank used for this segment

    def gas_used(self):
        """calculates returns the quantity (in liter)
        of gas used for this segment

        *Keyword arguments:*
            <none>

        *Returns:*
            float -- in liter, quantity of gas used

        """
        if self.setpoint > 0:
            # CCR mode: we do not calculate gas_used
            return 0
        else:
            pressure = (depth_to_pressure(self.depth) +
                        settings.AMBIANT_PRESSURE_SURFACE)
            return (pressure * self.time *
                    float(settings.DIVE_CONSUMPTION_RATE))


class SegmentDeco(Segment):
    """Specialisation of segment class for deco segments
    """
    def __init__(self, depth, time, tank, setpoint=0):
        """Constructor for SegmentDeco class.
        Look at base class for more explanations

        In deco segment, we also have to manage some new parameters :

        * gf_used : which gradient factor is used
        * control_compartment : who is the control compartement
        * mv_max : max M-value for the compartment

        *Keyword arguments:*
            :depth: (float) -- in meter, the (constant) depth for this segment
            :time: (float) -- in second, duration of this segment
            :tank: (Tank) -- object instance of Tank class :
                             describe the tank used in this segment
            :setpoint: (float) -- for CCR, setpoint used for this segment
                                  for OC : setpoint should be zero

        *Returns:*
            <nothing>

        *Raise:*
            UnauthorizedMod -- if depth is incompatible
                               with either min or max mod

        """
        Segment.__init__(self)
        #initiate class logger
        self.logger = logging.getLogger("dipplanner.segment.SegmentDeco")
        self.logger.debug("creating an instance of SegmentDeco: \
    depth:%s, time:%ss, tank:%s, sp:%f" % (depth, time, tank, setpoint))

        self.type = 'deco'  # type of segment
        self.in_use = True  # is this segment in use : default: yes
        self.depth = float(depth)  # depth of this segment, in meter
        self.time = float(time)  # time of this segment, in second

        self.setpoint = float(setpoint)  # for CCR
        self.tank = tank  # tank used for this segment

        # other parameters used in deco mode
        self.gf_used = 0.0
        self.control_compartment = None
        self.mv_max = 0.0

    def gas_used(self):
        """calculates returns the quantity (in liter)
        of gas used for this segment

        *Keyword arguments:*
            <none>

        *Returns:*
            float -- in liter, quantity of gas used

        """
        if self.setpoint > 0:
            return 0
        else:
            pressure = (depth_to_pressure(self.depth) +
                        settings.AMBIANT_PRESSURE_SURFACE)
            return (pressure * self.time *
                    float(settings.DECO_CONSUMPTION_RATE))


class SegmentAscDesc(Segment):
    """Specialisation of segment class for Ascent or Descent segments
    """

    def __init__(self, start_depth, end_depth, rate, tank, setpoint=0):
        """Constructor for SegmentAscDesc class.
        Look at base class for more explanations
        in this segment, we do not specify time, but rate (of ascending
        or descending) and start_depth and end_depth
        The comparaison between start and end depth determine if asc or desc
        rate is given in m/min

        *Keyword arguments:*
            :start_depth: (float) -- in meter, the starting depth
                                     for this segment
            :end_depth: (float) -- in meter, the ending depth
                                     for this segment
            :rate: (float) -- in m/s, rate of ascending or descending
            :tank: (Tank) -- object instance of Tank class :
                             describe the tank used in this segment
            :setpoint: (float) -- for CCR, setpoint used for this segment
                                  for OC : setpoint should be zero

        *Returns:*
            <nothing>

        *Raise:*
            UnauthorizedMod -- if depth is incompatible
                               with either min or max mod

        """
        Segment.__init__(self)
        #initiate class logger
        self.logger = logging.getLogger("dipplanner.segment.SegmentAscDesc")
        self.logger.debug("creating an instance of SegmentAscDesc:"
                          "startdepth:%s, enddepth:%s, "
                          "rate:%ss, tank:%s, sp:%f" %
                          (start_depth,
                           end_depth,
                           rate,
                           tank,
                           setpoint))

        self.in_use = True  # is this segment in use : default: yes
        self.depth = float(end_depth)  # depth of this segment, in meter
        self.start_depth = float(start_depth)
        self.end_depth = float(end_depth)
        self.rate = float(rate)
        self.setpoint = float(setpoint)  # for CCR
        self.tank = tank  # tank used for this segment

        # calculate the time based on start-end depth and rate:
        self.time = (abs(self.end_depth - self.start_depth) / self.rate)

        if start_depth > end_depth:
            self.type = 'ascent'  # type of segment
        else:
            self.type = 'descent'

    def check_mod(self, max_ppo2=None):
        """checks the mod for this segment according to the used tank.

        *Keyword arguments:*
            :max_ppo2: (float) -- max tolerated ppo2

        *Returns:*
            <nothing>

        *Raise:*
            UnauthorizedMod -- if segments goes below max mod or upper min mod

        """
        if self.type == 'ascent':
            max_depth = self.start_depth
        else:
            max_depth = self.end_depth

        if max_depth > self.tank.get_mod():
            raise UnauthorizedMod("depth is exceeding the maximum MOD")

    def check_min_od(self):
        """checks the minimum od for this segment according to the used tank.
        (hypoxic cases)

        *Keyword arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            UnauthorizedMod -- if segments goes below max mod or upper min mod
        """
        if self.type == 'ascent':
            min_depth = self.end_depth
        else:
            min_depth = self.start_depth

        if min_depth < self.tank.get_min_od():  # checks mini operating depth
            raise UnauthorizedMod("depth is too low for the minimum MOD")

    def gas_used(self):
        """calc. and returns the quantity (in liter) of gas used
        in this segment because it's ascend or descent,
        the gas is not used at the same rate during the segment
        Because the rate is the same during all the segment, we can use the
        consumption at the average depth of the segment

        *Keyword arguments:*
            <none>

        *Returns:*
            float -- in liter, quantity of gas used

        """
        if self.setpoint > 0:
            return 0
        else:
            average_depth = (float(self.start_depth) +
                             float(self.end_depth)) / 2.0
            pressure = (depth_to_pressure(average_depth) +
                        settings.AMBIANT_PRESSURE_SURFACE)
            return (pressure * self.time *
                    float(settings.DIVE_CONSUMPTION_RATE))
