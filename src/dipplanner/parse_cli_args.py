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

"""uses argparse to parse Command Line Arguments
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import argparse
from collections import OrderedDict

# local imports
from dipplanner.parse_config_files import DipplannerConfigFiles
from dipplanner import settings
from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive
from dipplanner.dive import Dive
from dipplanner.mission import Mission
from dipplanner.tools import altitude_to_pressure
from dipplanner.tools import safe_eval_calculator


class DipplannerCliArguments(object):
    """This class contains all methods and elements to parse the cli
    arguments and launch dipplanner

    Attributes:

    * parser: argparse object
    * args: args is the result of argpaser
    * dives: dives dict is in the following form:

        .. code-block:: python

            dives = { 'dive1': { 'tanks': {},
                                 'segments': {},
                                 'surface_interval':0 },
                      'dive2': { 'tanks': {},
                                 'segments': {},
                                 'surface_interval':60 }}
    """

    def __init__(self, cli_arguments):
        """Constructor for DipplannerCliArguments object

        *Keyword Arguments:*
            cli_arguments (list of string) -- list of arguments, like sys.argv

        """
        description = """%(prog)s calculates and output dive profile
      Thomas Chiroux, 2011-2012 - see http://dipplanner.org
      """

        epilog = ""

        self.parser = argparse.ArgumentParser(
            description=description,
            #usage=usage,
            epilog=epilog,
            formatter_class=argparse.RawTextHelpFormatter)

        self.parser.add_argument('--version',
                                 action='version',
                                 version=settings.__VERSION__)

        self.mandatory_arguments()
        self.dive_params_arguments()
        self.adv_params_arguments()
        self.output_params_arguments()

        self.args = None
        self.dives = None

        # parse the options
        args = self.parser.parse_args(cli_arguments[1:])

        self.check_arguments(args)

    def mandatory_arguments(self):
        """Mandatory options

        *Keyword Arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        group1 = self.parser.add_argument_group(
            "Mandatory Options",
            """Either presence of tank and segment inside a config file or
      this mandatory options (at leat one of each) are needed for this
       program to run""")
        group1.add_argument(
            "-c", "--config", dest="config_files",
            action="append", type=str, metavar="STRING",
            help="""path for config file.
      Default : ./config.cfg
      see manual for more infos on config file""")

        group1.add_argument(
            "-t", "--tank", dest="tanks",
            action="append", type=str, metavar="STRING",
            help="""Tank used for the dive
      Format:  "tank_name;f_o2;f_he;Volume(l);Pressure(bar);Minimum gas rule"
      Example: "airtank;0.21;0.0;12;200,50b"

      Minimum gas rule in format : xxxb of 1/x
      """)
        group1.add_argument(
            "-s", "--segment", dest="segments",
            action="append", type=str, metavar="STRING",
            help="""Input segments used for the dive

      Format:  "depth;duration;tank;setpoint"
      Example: "30;20*60;airtank;0.0"
      * depth: in meter
      * duration : in seconds (operations are allowed like: '30*60')
      * tank : name of the tank (same name as tank options)
      * setpoint : 0 if OC, setpoint if CCR

      You can specify multiple args like:
      %(prog)s [other_options] -s "30;1000;airtank;0.0" -s "20;800;airtank;0.0"
      """)

        group1.add_argument(
            "--surfaceinterval", dest="surfaceinterval",
            type=str, metavar="SECONDS",
            help="""Optional Surface Interval in seconds""")

    def dive_params_arguments(self):
        """Dive parameters

        *Keyword Arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        group2 = self.parser.add_argument_group("Dive Parameters")
        group2.add_argument(
            "--model", metavar="VAL", type=str,
            choices=['ZHL16b', 'ZHL16c'],
            help="""Decompression model: either ZHL16b or ZHL16c """)

        group2.add_argument(
            "--gflow", metavar="VAL", type=str,
            help="""GF low, in """)
        group2.add_argument(
            "--gfhigh", metavar="VAL", type=str,
            help="""GF high, in """)

        group2.add_argument(
            "--water", metavar="VAL", type=str,
            help="""type of water : sea or fresh""")

        group2.add_argument(
            "--altitude", metavar="VAL", type=int,
            help="""altitude of the dive in meter.""")
        group2.add_argument(
            "--diveconsrate", metavar="VAL", type=str,
            help="""gas consumption rate during dive (in l/minute).""")
        group2.add_argument(
            "--decoconsrate", metavar="VAL", type=str,
            help="""gas consumption rate during deco (in l/minute).""")
        group2.add_argument(
            "--descentrate", metavar="VAL", type=str,
            help="""descent rate (in m/minute).""")
        group2.add_argument(
            "--ascentrate", metavar="VAL", type=str,
            help="""ascent rate (in m/minute).""")

        group2.add_argument(
            "--maxppo2", metavar="VAL", type=float,
            help="max allowed ppo2 for this dive.")
        group2.add_argument(
            "--minppo2", metavar="VAL", type=float,
            help="minimum allowed ppo2 for this dive.")
        group2.add_argument(
            "--maxend", metavar="VAL", type=float,
            help="max END allowed for this dive.")

        group2.add_argument(
            "--forcesegmenttime", action="store_true",
            help="""if set, each input segment will be dove
      at the full time of the segment.
      By default the segment time is shortened by descent or ascent time
      """)

        group2.add_argument(
            "--samegasfordeco", action="store_true",
            help="if set, do not use deco tanks (or bailout) "
                 "for decompressions")

        group2.add_argument("--multilevel", action="store_true",
                            help="Multilevel mode")

        group2.add_argument("--automatictankrefill",
                            action="store_true",
                            help="Automatic tank refill between dives")

        group2.add_argument("--notankrefill",
                            action="store_true",
                            help="Do not refill tanks between dives")


    def adv_params_arguments(self):
        """Advanced parameters

        *Keyword Arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        group3 = self.parser.add_argument_group("Advanced Parameters")
        group3.add_argument(
            "--depthcalcmethod", metavar="simple|complex",
            type=str,
            help="""method used for pressure from depth calculation.
                Simple method uses only +10m = +1bar
                Complex methods uses real water density""")

        group3.add_argument(
            "--travelswitch", metavar="late|early",
            type=str,
            help="""Travel switch method (late or early).
                  if late, it will keep the travel as long as possible
                  if early, it will switch to bottom tank as soon as is it
                  breathable""")
        group3.add_argument(
            "--surfacetemp", metavar="VAL", type=float,
            help="""Temperature at surface in celcius""")

        group3.add_argument(
            "--ambiantpressureatsea", metavar="VAL",
            type=float,
            help="""Change ambiant pressure at sea level (in bar)""")

    def output_params_arguments(self):
        """Output parameters

        *Keyword Arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        group4 = self.parser.add_argument_group("Output Parameters")
        group4.add_argument(
            "--template", metavar="TEMPLATE",
            type=str,
            help="""Name of the template to be used
      The template file should be present in ./templates""")

    def check_arguments(self, args):
        """parse all command lines options

        could also exit from program because of wrong arguments

        *Keyword Arguments:*
            args -- parsed arguments object

        *Returns:*
            <nothing>


        *Raise:*
            Nothing, but can exit
        """
        parsed_config_files = DipplannerConfigFiles(args.config_files)
        dives = parsed_config_files.dives

        if dives is None:
            dives = {}

        if args.gflow:
            try:
                settings.GF_LOW = \
                    float(safe_eval_calculator(args.gflow.strip('%'))) / 100
            except ValueError:
                self.parser.error("Error while parsing option gflow : %s"
                                  % args.gflow)

        if args.gfhigh:
            try:
                settings.GF_HIGH = \
                    float(safe_eval_calculator(args.gfhigh.strip('%'))) / 100
            except ValueError:
                self.parser.error("Error while parsing option gfhigh: %s"
                                  % args.gfhigh)

        if args.water:
            if args.water.lower() == "sea":
                settings.WATER_DENSITY = settings.SEA_WATER_DENSITY
            if args.water.lower() == "fresh":
                settings.WATER_DENSITY = settings.FRESH_WATER_DENSITY

        if args.altitude:
            settings.AMBIANT_PRESSURE_SURFACE = \
                altitude_to_pressure(args.altitude)

        if args.diveconsrate:
            try:
                settings.DIVE_CONSUMPTION_RATE = \
                    float(safe_eval_calculator(args.diveconsrate)) / 60
            except ValueError:
                self.parser.error("Error while parsing option "
                                  "diveconsrate : %s"
                                  % args.diveconsrate)

        if args.decoconsrate:
            try:
                settings.DECO_CONSUMPTION_RATE = \
                    float(safe_eval_calculator(args.decoconsrate)) / 60
            except ValueError:
                self.parser.error("Error while parsing option "
                                  "decoconsrate : %s"
                                  % args.decoconsrate)

        if args.descentrate:
            try:
                settings.DESCENT_RATE = \
                    float(safe_eval_calculator(args.descentrate)) / 60
            except ValueError:
                self.parser.error("Error while parsing option "
                                  "descentrate : %s"
                                  % args.descentrate)

        if args.ascentrate:
            try:
                settings.ASCENT_RATE = \
                    float(safe_eval_calculator(args.ascentrate)) / 60
            except ValueError:
                self.parser.error("Error while parsing option "
                                  "ascentrate : %s"
                                  % args.ascentrate)

        if args.model:
            settings.DECO_MODEL = args.model

        if args.maxppo2:
            settings.DEFAULT_MAX_PPO2 = args.maxppo2

        if args.minppo2:
            settings.DEFAULT_MIN_PPO2 = args.minppo2

        if args.maxend:
            settings.DEFAULT_MAX_END = args.maxend

        if args.samegasfordeco:
            settings.USE_OC_DECO = False

        if args.forcesegmenttime:
            settings.RUN_TIME = False

        if args.depthcalcmethod == 'simple' or \
                args.depthcalcmethod == 'complex':
            settings.METHOD_FOR_DEPTH_CALCULATION = args.depthcalcmethod

        if args.travelswitch == 'late' or args.travelswitch == 'early':
            settings.TRAVEL_SWITCH = args.travelswitch

        if args.surfacetemp is not None:
            settings.SURFACE_TEMP = args.surfacetemp

        if args.ambiantpressureatsea:
            settings.AMBIANT_PRESSURE_SEA_LEVEL = args.ambiantpressureatsea

        if args.multilevel:
            settings.MULTILEVEL_MODE = True

        if args.automatictankrefill:
            settings.AUTOMATIC_TANK_REFILL = True

        if args.notankrefill:
            settings.AUTOMATIC_TANK_REFILL = False

        # try to find tank(s) and segment(s).
        # if found, add this dive to the (eventually) other dives defined
        # in config files.
        # this will be the last dive
        tanks = {}

        if args.tanks:
            for tank in args.tanks:
                (name, f_o2, f_he, volume, pressure, rule) = tank.split(";")

                tanks[name] = Tank(
                    float(f_o2),
                    float(f_he),
                    max_ppo2=settings.DEFAULT_MAX_PPO2,
                    tank_vol=float(safe_eval_calculator(volume)),
                    tank_pressure=float(safe_eval_calculator(pressure)),
                    tank_rule=rule,
                    given_name=name)

        if tanks == {}:
            # no tank provided, try to get the previous tanks
            try:
                tanks = dives[dives.items()[-1][0]]['tanks']
            except (KeyError, IndexError):
                self.parser.error("Error : no tank provided for this dive !")

        segments = {}
        if args.segments:
            num_seg = 1
            for seg in args.segments:
                (depth, time, tankname, setpoint) = seg.split(";")
                # looks for tank in tanks
                try:
                    #seg_name = 'segment%s' % num_seg
                    #print seg_name
                    segments['segment%s' % num_seg] = SegmentDive(
                        float(safe_eval_calculator(depth)),
                        float(safe_eval_calculator(time)),
                        tanks[tankname],
                        float(setpoint))
                except KeyError:
                    self.parser.error(
                        "Error : tank name (%s) in not found in tank list !" %
                        tankname)
                except:
                    pass
                num_seg += 1
            segments = OrderedDict(sorted(segments.items(),
                                   key=lambda t: t[0]))
            if args.surfaceinterval:
                dives['diveCLI'] = {'tanks': tanks,
                                    'segments': segments,
                                    'surface_interval':
                                    safe_eval_calculator(args.surfaceinterval)}
            else:
                dives['diveCLI'] = {'tanks': tanks,
                                    'segments': segments,
                                    'surface_interval': 0}

        if args.template:
            settings.TEMPLATE = args.template
            # returns

        self.args = args
        self.dives = dives
        self.create_mission()

    def create_mission(self):
        """Create a mission object based of listed dives in self.dives

        *Keyword Arguments:*
        <none>

        *Returns:*
        <nothing>

        *Raise:*
        <nothing>
        """
        self.mission = Mission()
        previous_dive = None

        for dive in self.dives:
            if previous_dive is None:
                current_dive = Dive(self.dives[dive]['segments'].values(),
                                    self.dives[dive]['tanks'].values())
                self.mission.add_dive(current_dive)
            else:
                current_dive = Dive(self.dives[dive]['segments'].values(),
                                    self.dives[dive]['tanks'].values(),
                                    previous_dive)
                if self.dives[dive]['surface_interval']:
                    current_dive=self.dives[dive]['surface_interval']
                self.mission.add_dive(current_dive)
            previous_dive = current_dive

