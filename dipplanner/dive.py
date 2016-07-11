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
"""Dive class module.

Each Dive represent one dive (and only one)
For successive dives, it is possible to provide the parameters of the
previous dive in order to calculate the next one.
"""
import logging
import copy
# dependencies imports
from jinja2 import Environment, PackageLoader

# local imports
from dipplanner import settings
from dipplanner.dipp_exception import DipplannerException
from dipplanner.model.buhlmann.model_exceptions import ModelException
from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive, SegmentDeco, SegmentAscDesc
from dipplanner.model.buhlmann.model import Model as BuhlmannModel

from dipplanner.tools import calculate_pp_h2o_surf
from dipplanner.tools import depth_to_pressure
from dipplanner.tools import seconds_to_mmss
from dipplanner.tools import seconds_to_hhmmss
from dipplanner.tools import altitude_or_depth_to_absolute_pressure


class NothingToProcess(DipplannerException):
    """Raised when the is no input segments to process."""

    def __init__(self, description=""):
        """Init of the Exception.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: NothingToProcess ! (%s)", description)


class InstanciationError(DipplannerException):
    """Raised when the Dive constructor encounters a problem.

    In this case, it can not continue
    """

    def __init__(self, description=""):
        """Init of the Exception.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: InstanciationError ! (%s)", description)


class ProcessingError(DipplannerException):
    """Raised when the is no input segments to process."""

    def __init__(self, description=""):
        """Init of the Exception.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: ProcessingError ! (%s)", description)


class InfiniteDeco(DipplannerException):
    """Raised when the deco time becomes enourmous (like infinite)."""

    def __init__(self, description=""):
        """Init of the Exception.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: InfiniteDeco ! (%s)", description)


class Dive():
    """Conducts dive based on inputSegments, knownGases, and an existing model.

    Iterates through dive segments updating the Model. When all
    dive segments are processed then calls ascend(0.0) to
    return to the surface.

    The previous_profile (Model) can be either null in which case a
    new model is created, or can be an existing model with tissue loadings.

    Gas switching is done on the final ascent if OC deco or
    bailout is specified.

    Outputs profile to a List of dive segments

    Attributes:

    * input_segments -- (list) Stores enabled input dive segment objects
    * output_segments -- (list) Stores output segments produced by this class
    * tanks -- (list) Stores enabled dive tank objects
    * current_tank -- current tank object
    * current_depth -- current dive depth
    * ambiant_pressure -- (current) ambiant pressure
    * current_f_he -- current gas fraction of He
    * current_f_n2 -- current gas fraction of N2
    * current_f_o2 -- current gas fraction of O2
    * model -- model used for this dive
    * run_time -- runTime
    * pp_o2 -- CCR ppO2, if OC : 0.0
    * is_closed_circuit -- Flag to store CC or OC
    * in_final_ascent -- flag for final ascent
    * is_repetative_dive -- Flag for repetative dives
    * surface_interval -- for surf. int. in seconds
    * no_flight_time_value -- calculated no flight time
    * metadata -- description for the dive
    """

    def __init__(self, known_segments, known_tanks, previous_profile=None):
        """Init for Dive class.

        For fist dive, instanciate the profile class with no model
        (profile will create one for you)
        For repetative dives, instanciate profile class with the previous model

        :param known_segments: -- list of input segments
        :type known_segments: list of :class:`dipplanner.segment.Segment`
        :param known_tanks: list of tanks for this dive
        :type known_tanks: list of :class:`dipplanner.tank.Tank`
        :param previous_profile: model object of the precedent dive
        :type previous_profile: :class:`dipplanner.model`

        .. note:: the initialisation should not fail. If something if wrong, it
                  MUST still instantiate itself, with errors in his own object
        """
        # initiate class logger
        self.logger = logging.getLogger("dipplanner.dive.Dive")
        self.logger.debug("creating an instance of Dive")

        # initiate dive exception list
        self.dive_exceptions = []

        if previous_profile is None:
            # new dive : new model
            self.is_repetitive_dive = False
            try:
                self.model = BuhlmannModel()  # buhlman model by default
            except DipplannerException as exc:
                self.dive_exceptions.append(
                    InstanciationError(
                        "Unable to instanciate model: %s" % exc))
            self.metadata = ""
        else:
            # repetative dive
            self.is_repetitive_dive = True
            self.model = previous_profile.model
            try:
                self.model.init_gradient()
            except DipplannerException as exc:
                self.dive_exceptions.append(
                    InstanciationError(
                        "Unable to reset model gradients: %s" % exc))

        # filter input segment for only enabled segments
        self.input_segments = []
        try:
            for segment in known_segments:
                if segment.in_use:
                    self.input_segments.append(segment)
        except DipplannerException as exc:
            self.dive_exceptions.append(
                InstanciationError("Problem while adding segments: %s" % exc))

        # filter lists of gases to make the used list of gases
        self.tanks = []
        try:
            for tank in known_tanks:
                if tank.in_use:
                    self.tanks.append(tank)
        except DipplannerException as exc:
            self.dive_exceptions.append(
                InstanciationError("Problem while adding tanks: %s" % exc))

        # initalise output_segment list
        self.output_segments = []

        # other initialisations
        self.surface_interval = 0
        self.no_flight_time_value = None
        self.full_desat_time_value = None
        self.is_closed_circuit = False  # OC by default
        self.pp_o2 = 0.0  # OC by default
        self.current_tank = None
        self.current_depth = 0.0
        self.in_final_ascent = False
        self.run_time = 0  # in second
        self.metadata = ""

    def __repr__(self):
        """Return a str representing the result of the dive.

        Using the default template

        :returns: a string with the result of the calculation of the dives
                  using the default template
        :rtype: str
        """
        return self.output("default.tpl")

    def __str__(self):
        """Return a str representing the result of the dive.

        Using the default template

        :returns: a string with the result of the calculation of the dives
                  using the default template
        :rtype: str
        """
        return self.__repr__()

    # def __cmp__(self, otherdive):
    #     """Compare a dive to another dive, based on run_time

    #     *Keyword arguments:*
    #         otherdive (Dive) -- another dive object

    #     *Returns:*
    #         Integer -- result of cmp()

    #     *Raise:*
    #         <nothing>
    #     """
    #     return cmp(self.run_time, otherdive.run_time)

    def output(self, template=None):
        """Return the dive profile calculated.

        using the template given in settings or command lines.
        (and not only the default template)

        :returns: a string with the result of the calculation of the dives
                  using the choosen template
        :rtype: str
        """
        env = Environment(loader=PackageLoader('dipplanner', 'templates'))
        if template is None:
            tpl = env.get_template(settings.TEMPLATE)
        else:
            tpl = env.get_template(template)
        # pylint: disable=no-member
        text = tpl.render(settings=settings,
                          dives=[self, ])
        # pylint: enable=no-member
        return text

    def do_surface_interval(self, time):
        """Conduct a surface interval.

        by performing a constant depth calculation on air at zero meters

        :param int time: duration of the interval, in seconds
        """
        try:
            self.model.const_depth(pressure=0.0, seg_time=time,
                                   f_he=0.0, f_n2=0.79, pp_o2=0.0)
        except DipplannerException as exc:
            self.dive_exceptions.append(
                ModelException("Unable to do surface interval: %s" % exc))

        self.surface_interval = time

        if settings.AUTOMATIC_TANK_REFILL:
            self.refill_tanks()

    def get_surface_interval(self):
        """Return surface interval in mm:ss format.

        :returns: surface interval time in mmm:ss format
        :rtype: str
        """
        return seconds_to_mmss(self.surface_interval)

    def refill_tanks(self):
        """refile all tanks defined in this dive.

        it is used for repetitive dives
        """
        for tank in self.tanks:
            tank.refill()

    def is_dive_segments(self):
        """Return true if there are loaded dive segments.

        else false means there is nothing to process

        :returns: True -- if there is at least one input
                          dive segment to process
                  False -- if there is no dive segment to process
        :rtype:  bool
        """
        return bool(len(self.input_segments) > 0)

    def do_dive_without_exceptions(self):
        """Call do_dive, and handle exceptions internally.

        do not raise any "dive related" exception : add the exception inside
        self.dive_exceptions instead.
        """
        try:
            self.do_dive()
        except DipplannerException as exc:
            self.dive_exceptions.append(exc)
        except Exception as exc:  # unknown generic exception
            self.dive_exceptions.append(
                DipplannerException("Unknown exception occured: %s" % exc))

    def do_dive(self):
        """Process the dive.

        :raises NothingToProcess: if there is no input segment to process
        :raises ModelException: <Exceptions from model>
        """
        if self.is_dive_segments() is False:
            raise NothingToProcess

        # check the segments:
        for seg in self.input_segments:
            seg.check()

        run_time_flag = settings.RUN_TIME

        # sets initial state
        #

        # else:
        first_segment = self.input_segments[0]
        self.current_tank = first_segment.tank

        # Sort self.tanks based on MOD ? why ? see below ?
        self.tanks.sort()

        self.current_depth = 0.0
        self.pp_o2 = first_segment.setpoint
        if self.pp_o2 == 0.0:
            self.is_closed_circuit = False
        else:
            self.is_closed_circuit = True
        self.in_final_ascent = False

        # check if tank for 1rst segment is suitable for descent (OC mode)
        if (not self.is_closed_circuit and
                self.input_segments[0].tank.get_min_od() > 0):
            # tank is not ok, we need to look for another better tank
            # at first, try to find a tank suitable
            # from 0m to depth of first segment
            self.logger.debug("bottom gaz not ok for descent")
            self.tanks.reverse()
            for tank in self.tanks:
                if tank.get_min_od() == 0:
                    self.logger.debug(
                        "This tank may be suitable:%s, mod:%s, end at d:%s",
                        str(tank), tank.mod, tank.get_end_for_given_depth(
                            self.input_segments[0].depth))

                    if (tank.mod >= self.input_segments[0].depth and
                            tank.get_end_for_given_depth(
                                self.input_segments[0].depth) <
                            settings.DEFAULT_MAX_END):
                        # ok we have a winner
                        self.logger.info(
                            "Changed tank for descent to:%s", str(tank))
                        self.current_tank = tank
                        break
            if self.current_tank == self.input_segments[0].tank:
                # not found : we need to stop in the descent
                # to switch from first gas
                # to bottom gas
                self.logger.debug("No directly usage tank found,"
                                  " try to stop and change tank")
                for tank in self.tanks:
                    if tank.get_min_od() == 0:
                        self.logger.debug(
                            "This tank may be suitable:%s, "
                            "mod:%s, end at d:%s",
                            str(tank),
                            tank.mod,
                            tank.get_end_for_given_depth(
                                self.input_segments[0].depth))

                        if settings.TRAVEL_SWITCH == 'late':
                            depth = min(tank.mod, tank.get_mod_for_given_end(
                                settings.DEFAULT_MAX_END))
                            self.input_segments.insert(0, SegmentDive(
                                depth=depth,
                                tank=self.input_segments[0].tank,
                                time=0))
                            self.input_segments.insert(0, SegmentDive(
                                depth=depth, tank=tank, time=0))
                            self.current_tank = tank
                            break
                        else:  # early
                            depth = self.input_segments[0].tank.get_min_od(
                                min_ppo2=settings.DEFAULT_MIN_PPO2)
                            self.input_segments.insert(0, SegmentDive(
                                depth=depth,
                                tank=self.input_segments[0].tank,
                                time=0))
                            self.input_segments.insert(0, SegmentDive(
                                depth=depth, tank=tank, time=0))
                            self.current_tank = tank
                            break
        self.tanks.sort()
        for seg in self.input_segments:
            if seg.type == 'const':  # only dive segment allowed for input
                delta_depth = float(seg.depth) - float(self.current_depth)
                # Ascend or descend to dive segment,
                # using existing gas and ppO2 settings
                if delta_depth > 0.0:  # descent
                    self.model.asc_desc(depth_to_pressure(self.current_depth),
                                        depth_to_pressure(seg.depth),
                                        settings.DESCENT_RATE,
                                        self.current_tank.f_he,
                                        self.current_tank.f_n2,
                                        self.pp_o2)
                    self.output_segments.append(
                        SegmentAscDesc(self.current_depth,
                                       seg.depth,
                                       settings.DESCENT_RATE,
                                       self.current_tank,
                                       self.pp_o2))
                    self.run_time += abs(float(delta_depth) /
                                         (float(settings.DESCENT_RATE)))
                    self.logger.debug("descent time : %ss",
                                      float(delta_depth) /
                                      settings.DESCENT_RATE)
                else:  # ascent
                    # call ascend method of this class
                    # for decompression calculation
                    self.ascend(seg.depth)

                # we are now at the desired depth : process the dive segment
                self.current_depth = seg.depth  # new depth
                self.pp_o2 = seg.setpoint
                self.current_tank = seg.tank
                if seg.time > 0:  # only do this if it's not a waypoint
                    if run_time_flag:
                        run_time_flag = False  # do this one only
                        self.model.const_depth(depth_to_pressure(seg.depth),
                                               seg.time - self.run_time,
                                               self.current_tank.f_he,
                                               self.current_tank.f_n2,
                                               self.pp_o2)
                        self.output_segments.append(
                            SegmentDive(seg.depth,
                                        seg.time - self.run_time,
                                        self.current_tank,
                                        self.pp_o2))
                        self.metadata += "Dive to %s for %ss\n" % (
                            seg.depth, seg.time - self.run_time)
                        self.logger.debug("Dive to %s for %ss",
                                          seg.depth,
                                          seg.time - self.run_time)
                        # run_time = seg_time because it's
                        # only done the first time
                        self.run_time = seg.time
                        self.logger.debug(
                            "update run time : %ss", self.run_time)
                    else:
                        self.model.const_depth(depth_to_pressure(seg.depth),
                                               seg.time,
                                               self.current_tank.f_he,
                                               self.current_tank.f_n2,
                                               self.pp_o2)
                        self.output_segments.append(
                            SegmentDive(seg.depth,
                                        seg.time,
                                        self.current_tank,
                                        self.pp_o2))
                        self.metadata += "Dive to %s for %ss\n" % (seg.depth,
                                                                   seg.time)
                        self.logger.debug("Dive to %s for %ss",
                                          seg.depth, seg.time)
                        self.run_time += seg.time
                        self.logger.debug("update run time : %ss",
                                          self.run_time)
                else:  # process waypoint
                    self.output_segments.append(
                        SegmentDive(seg.depth,
                                    seg.time,
                                    self.current_tank,
                                    self.pp_o2))

        # all input segment are now processed: process to ascend to the surface
        self.in_final_ascent = True
        # ascend to the surface
        self.ascend(0.0)
        # for each output segment, recalculate runtime and update segments
        total_time = 0
        for output_seg in self.output_segments:
            total_time += output_seg.time
            output_seg.run_time = total_time
        if total_time != self.run_time:
            self.logger.warning("dive run_time (%ss) differs from"
                                " all segments time (%ss)",
                                self.run_time, total_time)

        # write metadata into the model
        self.model.metadata = self.metadata
        # recalculate the gas consumptions
        self.do_gas_calcs()
        # save the tanks parameters : next dives may use the same tanks,
        # but we need here to duplicate tank object within this dive in
        # order to save the tank parameters for this dive only
        saved_tanks = []
        for tank in self.tanks:
            saved_tanks.append(copy.deepcopy(tank))
        self.tanks = saved_tanks

    def get_no_flight_hhmmss(self):
        """Return no flight time (if calculated) in hhmmss format.

        instead of an int in seconds

        .. note::

           This method does not calculate no_flight_time
           you need to call no_flight_time() or
           no_flight_time_wo_exception() before.

        :returns: "hh:mm:ss" no flight time
                  "" (empty string) if no flight time is not calculated
        :rtype: str
        """
        if self.no_flight_time_value is not None:
            return seconds_to_hhmmss(self.no_flight_time_value)
        else:
            return ""

    def no_flight_time_wo_exception(self,
                                    altitude=settings.FLIGHT_ALTITUDE,
                                    tank=None):
        """Call no_flight_time, and handle exceptions internally.

        do not raise any "dive related" exception: add the
        exception inside self.dive_exceptions instead.

        :param int altitude: in meter : altitude used for the calculation
        :param float flight_ascent_rate: in m/s
        :param tank: [optionnal]
                     it is possible to provide a tank while calling
                     no_flight_time to force "no flight deco" with
                     another mix than air.
                     In this case, we will 'consume' the tank
                     When the tank is empty, it automatically switch to air
        :type tank: :class:`dipplanner.tank.Tank`

        :returns: no fight time in seconds
        :rtype: int
        """
        try:
            result = self.no_flight_time(altitude, tank)
        except DipplannerException as exc:
            self.dive_exceptions.append(exc)
        except Exception as exc:  # unknown generic exception
            self.dive_exceptions.append(
                DipplannerException("Unknown exception occured: %s" % exc))
        else:
            return result

    def no_flight_time(self, altitude=settings.FLIGHT_ALTITUDE, tank=None):
        """Evaluate the no flight time.

        by 'ascending' to the choosen flight altitude.
        Ascending will generate the necessary 'stop' at the current depth
        (which is 0m) .
        The stop time represents the no flight time

        :param int altitude: in meter : altitude used for the calculation
        :param float flight_ascent_rate: in m/ms
        :param tank: (optionnal)
                    it is possible to provide a tank while calling
                    no_flight_time to force "no flight deco" with
                    another mix than air.
                    In this case, we will 'consume' the tank
                    When the tank is empty, it automatically switch to air
        :type tank: :class:`dipplanner.tank.Tank`

        :returns: no fight time in seconds
        :rtype: int

        :raises InfiniteDeco: if the no flight time can not achieve enough
                              decompression to be able to go to give altitude
        """
        no_flight_time = 0
        deco_uses_tank = False  # set to true when deco is using a tank
        # need to change gaz to air:
        # create a 'dummy' air tank
        no_flight_air_tank = Tank(
            tank_vol=settings.ABSOLUTE_MAX_TANK_SIZE,
            tank_pressure=settings.ABSOLUTE_MAX_TANK_PRESSURE,
            tank_rule="30b")

        if tank is not None:
            no_flight_tank = tank
            deco_uses_tank = True
            self.logger.info("Accelerating no flight"
                             "time using a tank:%s", tank)
        else:
            no_flight_tank = no_flight_air_tank

        next_stop_pressure = altitude_or_depth_to_absolute_pressure(altitude)
        # bigger stop time to speed up calculation
        # (precision is not necesary here)
        stop_time = 60  # in second -

        model_copy = copy.deepcopy(self.model)
        model_ceiling = model_copy.ceiling_in_pabs()
        while model_ceiling > next_stop_pressure:
            # loop for "deco" calculation based on the new ceiling
            model_copy.const_depth(0.0,
                                   stop_time,
                                   no_flight_tank.f_he,  # f_he
                                   no_flight_tank.f_n2,  # f_n2
                                   0.0)  # ppo2 (for cc)
            no_flight_time += stop_time
            model_ceiling = model_copy.ceiling_in_pabs()
            if deco_uses_tank:
                if no_flight_tank.remaining_gas <= 0:
                    no_flight_tank = no_flight_air_tank
                    deco_uses_tank = False
                    self.logger.info("Tank used for accelerating "
                                     "no flight time is empty, "
                                     "swithing to air at %s s",
                                     no_flight_time)
                else:
                    no_flight_tank.consume_gas(
                        settings.DECO_CONSUMPTION_RATE * stop_time)
            if no_flight_time > 300000:
                raise InfiniteDeco("Infinite deco error")

        self.no_flight_time_value = no_flight_time
        return no_flight_time

    def get_full_desat_hhmmss(self):
        """Return full desat time (if calculated) in hhmmss format.

        instead of an int in seconds

        :returns: "hh:mm:ss" full desat time
        :rtype: str
        """
        if self.full_desat_time_value is not None:
            return seconds_to_hhmmss(self.full_desat_time_value)
        else:
            return seconds_to_hhmmss(self.full_desat_time())

    def full_desat_time(self):
        """Evaluate the full desat time.

        By doing deco at const depth of 0m until all compartement
        are (nearly) empty.
        Because of compartments halftimes, full desat is never really achieved.
        So we need to setup an arbitrary "margin": when sur-saturation falls
        below this margin, we consider that the compartment is not satured
        anymore.

        :returns: full desat time in seconds
        :rtype: int

        :raises InfiniteDeco: if the no flight time can not achieve enough
                              decompression to be able to go to give altitude
        """
        # TODO: DONE FOR TESTS HERE:
        return 0

        full_desat_time = 0
        margin = 0.01 + calculate_pp_h2o_surf(settings.SURFACE_TEMP)

        # bigger stop time to speed up calculation
        # (precision is not necesary here)
        stop_time = 60  # in second

        model_copy = copy.deepcopy(self.model)
        full_desat = False
        while not full_desat:
            # loop for "deco" calculation based on the new ceiling
            model_copy.const_depth(pressure=0.0,
                                   seg_time=stop_time,
                                   f_he=0.0,
                                   f_n2=settings.DEFAULT_AIR_FN2,
                                   pp_o2=0.0)
            full_desat_time += stop_time

            if full_desat_time > 300000:
                raise InfiniteDeco("Infinite deco error")

            full_desat = True
            for comp in model_copy.tissues:
                if (comp.pp_n2 > settings.DEFAULT_AIR_FN2 + margin or
                        comp.pp_he > margin):
                    full_desat = False
                    break

        self.full_desat_time_value = full_desat_time
        return full_desat_time

    def ascend(self, target_depth):
        """Ascend to target depth, decompressing if necessary.

        If inFinalAscent then gradient factors start changing,
        and automatic gas selection is made.

        This method is called by do_dive()

        :param float target_depth: in meter, target depth for the ascend

        :raises ModelException: <Exceptions from model>
        """
        force_deco_stop = False
        in_deco_cycle = False
        deco_stop_time = 0

        if self.in_final_ascent and settings.USE_OC_DECO:
            self.set_deco_gas(self.current_depth)

        if self.current_depth < target_depth:
            # going backwards !
            raise ProcessingError("Not allowed to ascend while descending !")

        # Set initial stop to be the next integral stop depth
        if self.current_depth % settings.STOP_DEPTH_INCREMENT > 0:
            # we are not on a stop depth already : go to the next stop depth
            next_stop_depth = (int(self.current_depth /
                                   settings.STOP_DEPTH_INCREMENT) *
                               settings.STOP_DEPTH_INCREMENT)
        else:
            next_stop_depth = int(self.current_depth -
                                  settings.STOP_DEPTH_INCREMENT)

        self.logger.debug("next_stop_depth: %s", next_stop_depth)
        # hack in case we are overshooting or hit last stop or any of
        # the other bizzar combinations ...
        if (next_stop_depth < target_depth or
                self.current_depth < settings.LAST_STOP_DEPTH):
            next_stop_depth = target_depth
            self.logger.debug("new next_stop_depth: %s", next_stop_depth)
        elif next_stop_depth == settings.LAST_STOP_DEPTH:
            self.logger.warning("next_stop_depth==LAST_STOP_DEPTH !")
            next_stop_depth = target_depth
            self.logger.debug("new next_stop_depth: %s", next_stop_depth)
        elif next_stop_depth < settings.LAST_STOP_DEPTH:
            next_stop_depth = settings.LAST_STOP_DEPTH
            self.logger.debug("new next_stop_depth: %s", next_stop_depth)

        # Initialise ascent segment start depth
        start_depth = self.current_depth
        in_ascent_cycle = True  # Start in free ascent

        # Initialise gradient factor for next (in this case first) stop depth
        self.model.gradient.set_gf_at_depth(next_stop_depth)

        # Remember maxM-Value and controlling compartment
        max_mv = self.model.m_value(depth_to_pressure(self.current_depth))
        control = self.model.control_compartment()

        while self.current_depth > target_depth:
            self.logger.debug("ascent from: %s, to: %s",
                              self.current_depth, next_stop_depth)
            # can we move to the proposed next stop depth ?
            model_ceiling = self.model.ceiling()
            self.logger.debug("model ceiling: %s", model_ceiling)
            while force_deco_stop or next_stop_depth < model_ceiling:
                in_deco_cycle = True
                # Only used for first entry into deco stop
                force_deco_stop = False
                if in_ascent_cycle:
                    # Finalise last ascent cycle as we are now decomp
                    if start_depth > self.current_depth:
                        # add ascent segment
                        self.logger.debug("Add AscDesc(1): start_depth:%s "
                                          "current_depth:%s",
                                          start_depth, self.current_depth)
                        self.output_segments.append(
                            SegmentAscDesc(start_depth,
                                           self.current_depth,
                                           settings.ASCENT_RATE,
                                           self.current_tank,
                                           self.pp_o2))
                    in_ascent_cycle = False

                # set m-value gradient under the following conditions:
                #   - if not in multilevel mode, then set it as soon as
                #     we do a decompression cycle
                #   - otherwise wait until we are finally
                #     surfacing before setting it
                if ((not settings.MULTILEVEL_MODE or self.in_final_ascent) and
                        (not self.model.gradient.gf_set)):
                    self.model.gradient.set_gf_slope_at_depth(
                        self.current_depth)
                    self.model.gradient.set_gf_at_depth(next_stop_depth)
                    self.logger.debug("...set m-value gradient: %s",
                                      self.model.gradient.gf)

                # calculate stop_time
                # if (deco_stop_time == 0 and
                #         self.run_time % settings.STOP_TIME_INCREMENT > 0):
                #     stop_time = (
                #         int(self.run_time / settings.STOP_TIME_INCREMENT) *
                #         settings.STOP_TIME_INCREMENT +
                #         settings.STOP_TIME_INCREMENT - self.run_time)
                #     print("+++++ ", stop_time)
                #     if stop_time == 0:
                #         stop_time = settings.STOP_TIME_INCREMENT  # in second
                # else:
                stop_time = settings.STOP_TIME_INCREMENT  # in second

                # execute the stop
                self.model.const_depth(depth_to_pressure(self.current_depth),
                                       stop_time,
                                       self.current_tank.f_he,
                                       self.current_tank.f_n2,
                                       self.pp_o2)

                deco_stop_time += stop_time
                # sanity check for infinite loop
                if deco_stop_time > 300000:
                    raise InfiniteDeco("Infinite deco error")

                model_ceiling = self.model.ceiling()

            # finished decompression loop
            if in_deco_cycle:
                self.logger.debug("...in deco cycle")
                # finalise the last deco cycle
                self.run_time += deco_stop_time
                self.logger.debug(
                    "update run time with deco time: %ss at %sm (runtime:%s)",
                    deco_stop_time, self.current_depth, self.run_time)
                if settings.FORCE_ALL_STOPS:
                    force_deco_stop = True

                # write deco segment
                deco_segment = SegmentDeco(self.current_depth,
                                           deco_stop_time,
                                           self.current_tank,
                                           self.pp_o2)
                deco_segment.mv_max = max_mv
                deco_segment.gf_used = self.model.gradient.gf
                deco_segment.control_compartment = control
                self.output_segments.append(deco_segment)
                in_deco_cycle = False
                deco_stop_time = 0

            if in_ascent_cycle:
                self.logger.debug("...in ascent cycle, do asc from %s to %s",
                                  self.current_depth, next_stop_depth)
                self.model.asc_desc(depth_to_pressure(self.current_depth),
                                    depth_to_pressure(next_stop_depth),
                                    -settings.ASCENT_RATE,
                                    self.current_tank.f_he,
                                    self.current_tank.f_n2,
                                    self.pp_o2)
                self.run_time += abs((float(self.current_depth) -
                                      float(next_stop_depth)) /
                                     float(settings.ASCENT_RATE))
                self.logger.debug("update run time : %ss", self.run_time)
            else:
                self.logger.debug("...in deco cycle, do asc from %s to %s",
                                  self.current_depth, next_stop_depth)
                self.model.asc_desc(depth_to_pressure(self.current_depth),
                                    depth_to_pressure(next_stop_depth),
                                    -settings.DECO_ASCENT_RATE,
                                    self.current_tank.f_he,
                                    self.current_tank.f_n2,
                                    self.pp_o2)
                self.run_time += abs((float(self.current_depth) -
                                      float(next_stop_depth)) /
                                     float(settings.DECO_ASCENT_RATE))
                self.logger.debug("update run time : %ss", self.run_time)
                self.output_segments.append(
                    SegmentAscDesc(self.current_depth,
                                   next_stop_depth,
                                   settings.DECO_ASCENT_RATE,
                                   self.current_tank,
                                   self.pp_o2))

            # now we moved up the the next depth
            self.current_depth = next_stop_depth
            max_mv = self.model.m_value(depth_to_pressure(self.current_depth))
            control = self.model.control_compartment()

            # Check and switch deco gas
            temp_tank = self.current_tank  # remember in case we switch
            if self.set_deco_gas(self.current_depth):  # True if we changed gas
                if in_ascent_cycle:
                    self.logger.debug("Add AscDesc(2): start_depth:%s, "
                                      "current_depth:%s",
                                      start_depth, self.current_depth)
                    self.output_segments.append(
                        SegmentAscDesc(start_depth,
                                       self.current_depth,
                                       settings.ASCENT_RATE,
                                       temp_tank,
                                       self.pp_o2))
                    start_depth = self.current_depth

            # set next rounded stop depth
            next_stop_depth = int(
                self.current_depth) - settings.STOP_DEPTH_INCREMENT

            self.logger.debug("next stop depth: %s, target depth: %s",
                              next_stop_depth, target_depth)

            # check in cas we are overshooting or hit last stop
            if (next_stop_depth < target_depth or
                    self.current_depth < settings.LAST_STOP_DEPTH):
                self.logger.debug("next_stop_depth (%s) < target_depth (%s)",
                                  next_stop_depth, target_depth)
                next_stop_depth = target_depth
            elif self.current_depth < settings.LAST_STOP_DEPTH:
                self.logger.debug("current_depth (%s) < LAST_STOP_DEPTH (%s)",
                                  self.current_depth,
                                  settings.LAST_STOP_DEPTH)
                next_stop_depth = target_depth
            elif (next_stop_depth < settings.LAST_STOP_DEPTH and
                  next_stop_depth > 0):
                self.logger.debug("next_stop_depth (%s) < "
                                  "settings.LAST_STOP_DEPTH (%s)",
                                  next_stop_depth, settings.LAST_STOP_DEPTH)
                next_stop_depth = target_depth

            if self.model.gradient.gf_set:  # update gf for next stop
                self.model.gradient.set_gf_at_depth(next_stop_depth)

        # are we still in ascent segment ?
        if in_ascent_cycle:
            self.logger.debug("Add AscDesc(3): start_depth:%s, "
                              "current_depth:%s",
                              start_depth, self.current_depth)
            self.output_segments.append(
                SegmentAscDesc(start_depth,
                               self.current_depth,
                               -settings.ASCENT_RATE,
                               self.current_tank,
                               self.pp_o2))

    def do_gas_calcs(self):
        """Estimate gas consumption for all output segments.

        and set this into the respective gas objects

        :raises InvalidGas: <Exceptions from tank>
        :raises InvalidTank: <Exceptions from tank>
        :raises InvalidMod: <Exceptions from tank>
        :raises EmptyTank: <Exceptions from tank>
        """
        for seg in self.output_segments:
            seg.tank.consume_gas(seg.gas_used)

    def set_deco_gas(self, depth):
        """Select appropriate deco gas for the depth specified.

        Returns true if a gas switch occured

        :param float depth: target depth to make the choice

        :returns: True -- if gas swich occured
                  False -- if no gas switch occured
        :rtype: bool

        :raises InvalidGas: <Exceptions from tank>
        :raises InvalidTank: <Exceptions from tank>
        :raises InvalidMod: <Exceptions from tank>
        :raises EmptyTank: <Exceptions from tank>
        """
        gas_switch = False

        # check to see if we should be changing gases at all ...
        # if so just return doing nothing
        if not self.in_final_ascent:
            return False
        if not settings.USE_OC_DECO:
            return False
        if len(self.tanks) == 0:
            return False

        # check and switch deco gases
        current_tank_sav = self.current_tank
        for temp_tank in self.tanks:
            if (temp_tank.get_mod() >= depth and
                    temp_tank.get_min_od() < depth):
                # authorised tank  at this depth
                if temp_tank < current_tank_sav:
                    if self.is_closed_circuit:
                        # only change from CC to OC when a valid tank
                        # for deco is available
                        self.pp_o2 = False
                        self.is_closed_circuit = False

                    self.current_tank = temp_tank
                    gas_switch = True
                    self.logger.info("Changing gas from %s (mod:%s)"
                                     "to %s (mod:%s)",
                                     current_tank_sav,
                                     current_tank_sav.get_mod(),
                                     self.current_tank,
                                     self.current_tank.get_mod())
            # else:
            #   break
        return gas_switch
