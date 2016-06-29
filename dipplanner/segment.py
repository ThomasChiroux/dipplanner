#
# Copyright 2011-2016 Thomas Chiroux
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
"""Segment classes.

A segment is a portion of a dive in the same depth (depth + duration)
"""
import logging

from dipplanner import settings
from dipplanner.dipp_exception import DipplannerException
from dipplanner.tools import seconds_to_mmss
from dipplanner.tools import depth_to_pressure


class UnauthorizedMod(DipplannerException):
    """Raised when the MOD is not possible.

    ...according to the depth(s) of the segment
    """

    def __init__(self, description):
        """Init of the Exception.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: UnauthorizedMod ! (%s)", description)


class Segment():
    """Base class for all types of segments.

    *Attributes:*

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
        """Initialisation of the Segment base class.

        just defines all the parameters
        """
        # initiate class logger
        self.logger = logging.getLogger(self.__class__.__name__)
        # self.logger.debug("creating an instance of Segment")

        self.type = None  # type of segment : base class has no type
        self.in_use = True  # is this segment in use : default: yes
        self.depth = 0.0  # depth of this segment, in meter
        self.time = 0.0  # time of this segment, in second
        self.run_time = 0.0  # runtime in profile
        self.setpoint = 0.0  # for CCR
        self.tank = None  # tank used for this segment

    def __repr__(self):
        """Return a string representing the actual segment.

        :returns: representation of the segment.
        :rtype: str
        """
        return "%8s: at %3dm for %s [RT:%s], on %s,  SP:%s, END:%im" % (
            self.type.upper(),
            self.depth,
            self.segment_time_str,
            self.run_time_str,
            str(self.tank),
            self.setpoint,
            self.end)

    def __str__(self):
        """Return a human readable name of the segment.

        :returns: representation of the segment in the form
        :rtype: str
        """
        return self.__repr__()

    def check(self):
        """Check if it's a valid segment.

        Should be executed before calculating dives

        the check does not return anything if nok, but raises Exceptions

        :returns: True if check is ok, False if not
        :rtype: bool
        """
        if self.setpoint == 0:
            # check MOD only if OC
            self.check_mod()
            self.check_min_od()
        else:
            self.check_mod(self.setpoint)
        return True

    def check_mod(self, max_ppo2=None):
        """Check the mod for this segment according to the used tank.

        :param float max_ppo2: [OPTIONAL] max tolerated ppo2

        :returns: True if check is ok
        :rtype: bool

        :raises UnauthorizedMod: if segments goes below max mod or
                                 upper min mod
        """
        if self.depth > self.tank.get_mod(max_ppo2):
            raise UnauthorizedMod("depth is exceeding the maximum MOD")
        return True

    def check_min_od(self):
        """Check the minimum od for this segment according to the used tank.

        (minimum operating depth, hypoxic cases)

        :returns: True if check is ok
        :rtype: bool

        :raises UnauthorizedMod: if segments goes below max mod or
                                 upper min mod
        """
        if self.depth < self.tank.get_min_od():  # checks mini operating depth
            raise UnauthorizedMod("depth is too low for the minimum MOD")
        return True

    @property
    def segment_time_str(self):
        """Return segment time for humans in the form MMM:SS.

        :returns: segment time in the form MMM:SS
        :rtype: str
        """
        return seconds_to_mmss(self.time)

    @property
    def run_time_str(self):
        """Return runtime for humans in the form MMM:SS.

        :returns: segment time in the form MMM:SS
        :rtype: str
        """
        return seconds_to_mmss(self.run_time)

    def get_p_absolute(self, method=settings.METHOD_FOR_DEPTH_CALCULATION):
        """Return the absolute pression in bar.

        (1atm = 1ATA = 1.01325 bar = 14.70psi)

        Simple method : 10m = +1 bar
        Complex method : use real density of water, T°, etc...

        :param str method: [OPTIONAL] 'simple' or 'complex'
                           if not given uses the defaults in settings.

        :returns: absolute pressure in bar
        :rtype: float

        :raises ValueError: when providing a bad method
        """
        if method == 'simple':
            return float(self.depth) / 10 + settings.AMBIANT_PRESSURE_SURFACE
        elif method == 'complex':
            return (depth_to_pressure(self.depth) +
                    settings.AMBIANT_PRESSURE_SURFACE)
        else:
            raise ValueError("invalid method of calculation")

    @property
    def end(self):
        """Calculate and returns E.N.D (Equivalent Narcosis Depth).

        :returns: Equivalent Narcosis Depth in meter
        :rtype: int
        """
        return self.tank.get_end_for_given_depth(self.depth, self.setpoint)

    @property
    def gas_used(self):
        """Return the quantity (in liter) of gas used for this segment.

        (this method is empty)
        """
        pass


class SegmentDive(Segment):
    """Specialisation of segment class for dive segments."""

    def __init__(self, depth, time, tank, setpoint=0):
        """Init of SegmentDive class.

        Look at base class for more explanations

        :param float depth: in meter, the (constant) depth for this segment
        :param float time: in second, duration of this segment
        :param tank: object instance of Tank class :
                     describe the tank used in this segment
        :type tank: :class:`dipplanner.tank.Tank`
        :param float setpoint: for CCR, setpoint used for this segment
                               for OC : setpoint should be zero

        :raises UnauthorizedMod: if depth is incompatible
                                 with either min or max mod
        """
        super().__init__()
        self.logger.debug("creating an instance of SegmentDive: "
                          "depth:%s, time:%ss, tank:%s, sp:%f",
                          depth, time, tank, setpoint)

        self.type = 'const'  # type of segment
        self.in_use = True  # is this segment in use : default: yes
        self.depth = float(depth)  # depth of this segment, in meter
        self.time = float(time)  # time of this segment, in second

        self.setpoint = float(setpoint)  # for CCR
        self.tank = tank  # tank used for this segment

    @property
    def gas_used(self):
        """Calculate and return the quantity of gas used for this segment.

        (in liter)

        :returns: in liter, quantity of gas used
        :rtype: float
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
    """Specialisation of segment class for deco segments."""

    def __init__(self, depth, time, tank, setpoint=0):
        """Init of  SegmentDeco class.

        Look at base class for more explanations

        In deco segment, we also have to manage some new parameters :

        * gf_used : which gradient factor is used
        * control_compartment : who is the control compartement
        * mv_max : max M-value for the compartment

        :param float depth: in meter, the (constant) depth for this segment
        :param float time: in second, duration of this segment
        :param tank: object instance of Tank class :
                     describe the tank used in this segment
        :type tank: :class:`dipplanner.tank.Tank`
        :param float setpoint: for CCR, setpoint used for this segment
                               for OC : setpoint should be zero

        :raises UnauthorizedMod: if depth is incompatible
                                 with either min or max mod
        """
        super().__init__()
        self.logger.debug("creating an instance of SegmentDeco: "
                          "depth:%s, time:%ss, tank:%s, sp:%f",
                          depth, time, tank, setpoint)

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

    @property
    def gas_used(self):
        """Calculate and return the quantity of gas used for this segment.

        (in liter)

        :returns: in liter, quantity of gas used
        :rtype: float
        """
        if self.setpoint > 0:
            return 0
        else:
            pressure = (depth_to_pressure(self.depth) +
                        settings.AMBIANT_PRESSURE_SURFACE)
            return (pressure * self.time *
                    float(settings.DECO_CONSUMPTION_RATE))


class SegmentAscDesc(Segment):
    """Specialisation of segment class for Ascent or Descent segments."""

    def __init__(self, start_depth, end_depth, rate, tank, setpoint=0):
        """Init of SegmentAscDesc class.

        Look at base class for more explanations
        in this segment, we do not specify time, but rate (of ascending
        or descending) and start_depth and end_depth
        The comparaison between start and end depth determine if asc or desc
        rate is given in m/min

        :param float start_depth: in meter, the starting depth
                                  for this segment
        :param float end_depth: in meter, the ending depth
                                for this segment
        :param float rate: in m/s, rate of ascending or descending
        :param tank: object instance of Tank class :
                     describe the tank used in this segment
        :type tank: :class:`dipplanner.tank.Tank`
        :param float setpoint: for CCR, setpoint used for this segment
                               for OC : setpoint should be zero

        :raises UnauthorizedMod: if depth is incompatible
                                 with either min or max mod
        """
        super().__init__()
        self.logger.debug("creating an instance of SegmentAscDesc:"
                          "startdepth:%s, enddepth:%s, "
                          "rate:%ss, tank:%s, sp:%f",
                          start_depth,
                          end_depth,
                          rate,
                          tank,
                          setpoint)

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
        """Check the mod for this segment according to the used tank.

        :param float max_ppo2: max tolerated ppo2

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
        """Check the minimum od for this segment according to the used tank.

        (minimum operating depth, hypoxic cases)

        :returns: True if check is ok
        :rtype: bool

        :raises UnauthorizedMod: if segments goes below max mod or
                                 upper min mod
        """
        if self.type == 'ascent':
            min_depth = self.end_depth
        else:
            min_depth = self.start_depth

        if min_depth < self.tank.get_min_od():  # checks mini operating depth
            raise UnauthorizedMod("depth is too low for the minimum MOD")

    @property
    def gas_used(self):
        """Calculate and return the quantity of gas used for this segment.

        (in liter)

        in this segment because it's ascend or descent,
        the gas is not used at the same rate during the segment
        Because the rate is the same during all the segment, we can use the
        consumption at the average depth of the segment

        :returns: in liter, quantity of gas used
        :rtype: float
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
