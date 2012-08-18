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

"""main dipplanner module for command line usage.

This module is used by the only "executable" of the project:
bin/dipplanner (which is an empty shell)

runs in command line and output resulting dive profile
also initiate log files
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import sys
import logging
from collections import OrderedDict

# dependencies imports
from jinja2 import Environment, PackageLoader

# local imports
from dipplanner import settings
from dipplanner.dive import Dive
from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive
from dipplanner.tools import altitude_to_pressure

LOGGER = logging.getLogger("dipplanner")


def activate_debug():
    """setup the default debug parameters

    it's mainly used for test cases who needs also logging to be set

    *Keyword Arguments:*
        <none>

    *Return:*
        <nothing>

    *Raise:*
        <nothing>

    """
    LOGGER.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    file_handler = logging.FileHandler("dipplanner.log")
    file_handler.setLevel(logging.INFO)
    # create console handler with a higher log level
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # add the handlers to the logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)


def activate_debug_for_tests():
    """setup the default debug parameters

    it's mainly used for test cases who needs also logging to be set

    *Keyword Arguments:*
        <none>

    *Return:*
        <nothing>

    *Raise:*
        <nothing>
    """
    LOGGER.setLevel(logging.CRITICAL)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)


def parse_config_file(filenames):
    """parse a config file and change default settings values

    *Keyword Arguments:*
        :filename: (str) -- name (and path) of the config file to be parsed

    *Returns:*
        <nothing>

    *Raise:*
        Nothing, but can exit
    """
    from ConfigParser import SafeConfigParser

    if filenames is not None:
        config = SafeConfigParser()
        filesread = config.read(filenames)
    else:
        LOGGER.info("No config file found: skip config from files")
        return {}

    missing = set(filenames) - set(filesread)
    if len(filesread) == 0:
        LOGGER.info("No config file found: skip config from files")
        return {}

    if len(missing) > 0:
        if len(missing) == 1:
            LOGGER.warning(
                "Config file : %s not found, skip it" % list(missing)[0])
        else:
            LOGGER.warning("Config files : %s not found, skip them" %
                           ', '.join(str(n) for n in list(missing)))

    # now try to find each parameter and set the new setting
    if config.has_section('advanced'):
        section = 'advanced'
        if config.has_option(section, 'fresh_water_density'):
            settings.FRESH_WATER_DENSITY = float(
                config.get(section, 'fresh_water_density'))
        if config.has_option(section, 'sea_water_density'):
            settings.SEA_WATER_DENSITY = float(
                config.get(section, 'sea_water_density'))
        if config.has_option(section, 'absolute_max_ppo2'):
            settings.ABSOLUTE_MAX_PPO2 = float(
                config.get(section, 'absolute_max_ppo2'))
        if config.has_option(section, 'absolute_min_ppo2'):
            settings.ABSOLUTE_MIN_PPO2 = float(
                config.get(section, 'absolute_min_ppo2'))
        if config.has_option(section, 'absolute_max_tank_pressure'):
            settings.ABSOLUTE_MAX_TANK_PRESSURE = float(
                config.get(section, 'absolute_max_tank_pressure'))
        if config.has_option(section, 'absolute_max_tank_size'):
            settings.ABSOLUTE_MAX_TANK_SIZE = float(
                config.get(section, 'absolute_max_tank_size'))

        if config.has_option(section, 'surface_temp'):
            settings.SURFACE_TEMP = float(config.get(section, 'surface_temp'))
        if config.has_option(section, 'he_narcotic_value'):
            settings.HE_NARCOTIC_VALUE = float(
                config.get(section, 'he_narcotic_value'))
        if config.has_option(section, 'n2_narcotic_value'):
            settings.N2_NARCOTIC_VALUE = float(
                config.get(section, 'n2_narcotic_value'))
        if config.has_option(section, 'o2_narcotic_value'):
            settings.O2_NARCOTIC_VALUE = float(
                config.get(section, 'o2_narcotic_value'))
        if config.has_option(section, 'ar_narcotic_value'):
            settings.AR_NARCOTIC_VALUE = float(
                config.get(section, 'ar_narcotic_value'))

        if config.has_option(section, 'stop_depth_increment'):
            settings.STOP_DEPTH_INCREMENT = float(
                config.get(section, 'stop_depth_increment'))
        if config.has_option(section, 'last_stop_depth'):
            settings.LAST_STOP_DEPTH = float(
                config.get(section, 'last_stop_depth'))
        if config.has_option(section, 'stop_time_increment'):
            settings.STOP_TIME_INCREMENT = float(
                config.get(section, 'stop_time_increment'))
        if config.has_option(section, 'force_all_stops'):
            settings.FORCE_ALL_STOPS = eval(
                ''.join(config.get(section, 'force_all_stops')).title())
        if config.has_option(section, 'ambiant_pressure_sea_level'):
            settings.AMBIANT_PRESSURE_SEA_LEVEL = float(
                config.get(section, 'ambiant_pressure_sea_level'))
        if config.has_option(section, 'method_for_depth_calculation'):
            method = config.get(section, 'method_for_depth_calculation')
            if  method == 'simple' or method == 'complex':
                settings.METHOD_FOR_DEPTH_CALCULATION = method
        if config.has_option(section, 'travel_switch'):
            travel = config.get(section, 'travel_switch')
            if travel == 'late' or travel == 'early':
                settings.TRAVEL_SWITCH = travel
        if config.has_option(section, 'flight_altitude'):
            settings.FLIGHT_ALTITUDE = float(
                config.get(section, 'flight_altitude'))

    if config.has_section('output'):
        section = 'output'
        if config.has_option(section, 'template'):
            settings.TEMPLATE = config.get(section, 'template')

    if config.has_section('general'):
        section = 'general'
        if config.has_option(section, 'deco_model'):
            model = config.get(section, 'deco_model')
            if model == "ZHL16b" or model == "ZHL16c":
                settings.DECO_MODEL = model
        if config.has_option(section, 'max_ppo2'):
            settings.DEFAULT_MAX_PPO2 = float(config.get(section, 'max_ppo2'))
        if config.has_option(section, 'min_ppo2'):
            settings.DEFAULT_MIN_PPO2 = float(config.get(section, 'min_ppo2'))
        if config.has_option(section, 'max_end'):
            settings.DEFAULT_MAX_END = float(config.get(section, 'max_end'))
        if config.has_option(section, 'descent_rate'):
            settings.DESCENT_RATE = float(
                config.get(section, 'descent_rate')) / 60
        if config.has_option(section, 'ascent_rate'):
            settings.ASCENT_RATE = float(
                config.get(section, 'ascent_rate')) / 60

        if config.has_option(section, 'dive_consumption_rate'):
            settings.DIVE_CONSUMPTION_RATE = \
                float(config.get(section, 'dive_consumption_rate')) / 60
        if config.has_option(section, 'deco_consumption_rate'):
            settings.DIVE_CONSUMPTION_RATE = \
                float(config.get(section, 'deco_consumption_rate')) / 60

        if config.has_option(section, 'gf_low'):
            settings.GF_LOW = float(
                eval(''.join(config.get(section, 'gf_low')).strip('%'))) / 100
        if config.has_option(section, 'gf_high'):
            settings.GF_HIGH = float(
                eval(''.join(config.get(section, 'gf_high')).strip('%'))) / 100

        if config.has_option(section, 'water'):
            if config.get(section, 'water') == 'sea':
                settings.WATER_DENSITY = settings.SEA_WATER_DENSITY
            elif config.get(section, 'water') == 'fresh':
                settings.WATER_DENSITY = settings.FRESH_WATER_DENSITY

        if config.has_option(section, 'altitude'):
            settings.AMBIANT_PRESSURE_SURFACE = \
                altitude_to_pressure(float(config.get(section, 'altitude')))

        if config.has_option(section, 'run_time'):
            settings.RUN_TIME = eval(
                ''.join(config.get(section, 'run_time')).title())

        if config.has_option(section, 'use_oc_deco'):
            settings.USE_OC_DECO = eval(
                ''.join(config.get(section, 'use_oc_deco')).title())

        if config.has_option(section, 'multilevel_mode'):
            settings.MULTILEVEL_MODE = eval(
                ''.join(config.get(section, 'multilevel_mode')).title())

        if config.has_option(section, 'automatic_tank_refill'):
            settings.AUTOMATIC_TANK_REFILL = eval(
                ''.join(config.get(section, 'automatic_tank_refill')).title())

    #dives = { 'dive1': { 'tanks': {}, 'segments': {}, 'surface_interval':0} }
    dives = {}
    dive_number = 1  # initialization
    while config.has_section('dive%s' % dive_number):
        section = 'dive%s' % dive_number
        dives[section] = {'tanks': {}, 'segments': {}, 'surface_interval': 0}
        for parameter_name, parameter_value in config.items(section):
            if parameter_name == 'surface_interval':
                dives[section]['surface_interval'] = eval(parameter_value)
            elif parameter_name[0:4] == 'tank':
                #number = parameter_name[4:]
                (name, f_o2, f_he, volume, pressure, rule) =\
                    parameter_value.split(";")
                dives[section]['tanks'][name] = Tank(
                    float(f_o2),
                    float(f_he),
                    max_ppo2=settings.DEFAULT_MAX_PPO2,
                    tank_vol=float(eval(volume)),
                    tank_pressure=float(eval(pressure)),
                    tank_rule=rule)

        if dives[section]['tanks'] == {}:
            # no tank provided, try to get the previous tanks
            try:
                dives[section]['tanks'] = \
                    dives['dive%s' % (dive_number - 1)]['tanks']
            except KeyError:
                print "Error : no tank provided for this dive !"
                sys.exit(0)

        for parameter_name, parameter_value in config.items(section):
            if parameter_name[0:7] == 'segment':
                #number = parameter_name[4:]
                (depth, time, tankname, setpoint) = parameter_value.split(";")
                try:
                    dives[section]['segments'][parameter_name] = SegmentDive(
                        float(eval(depth)),
                        float(eval(time)),
                        dives[section]['tanks'][tankname],
                        float(setpoint))
                except KeyError:
                    print("Error : tank name (%s) in not found in tank list "
                    "!" % tankname)
                    sys.exit(0)
                except:
                    raise

        dives[section]['segments'] = OrderedDict(
            sorted(dives[section]['segments'].items(), key=lambda t: t[0]))
        dive_number += 1
    return OrderedDict(sorted(dives.items(), key=lambda t: t[0]))


def parse_arguments():
    """parse all command lines options

    could also exit from program because of wrong arguments

    *Keyword Arguments:*
        <none>

    *Returns:*
        a tuple of two dicts:
            :args:
            :dives:

            * args is the result of argpaser

            * dives dict is in the following form:

            .. code-block:: python

                dives = { 'dive1': { 'tanks': {},
                                     'segments': {},
                                     'surface_interval':0 },
                          'dive2': { 'tanks': {},
                                     'segments': {},
                                     'surface_interval':60 }}

    *Raise:*
        Nothing, but can exit
    """
    import argparse

    usage = """%(prog)s [options]"""
    description = """%(prog)s calculates and output dive profile
  Thomas Chiroux, 2011-2012 - see http://dipplanner.org
  """

    epilog = ""

    parser = argparse.ArgumentParser(
        description=description,
        usage=usage,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--version',
                        action='version',
                        version=settings.__VERSION__)

    group1 = parser.add_argument_group(
        "Mandatory Options",
        """Either presence of tank and segment inside a config file or
  this mandatory options (at leat one of each) are needed for this program to
   run""")
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
    group2 = parser.add_argument_group("Dive Parameters")
    group2.add_argument(
        "--model", metavar="VAL", type=str,
        default="ZHL16c", choices=['ZHL16b', 'ZHL16c'],
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
        "--samegasfordeco", action="store_true",
        help="if set, do not use deco tanks (or bailout) for decompressions")
    group2.add_argument(
        "--forcesegmenttime", action="store_true",
        help="""if set, each input segment will be dove
  at the full time of the segment.
  By default the segment time is shortened by descent or ascent time
  """)

    group3 = parser.add_argument_group("Advanced Parameters")
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

    group4 = parser.add_argument_group("Output Parameters")
    group4.add_argument(
        "--template", metavar="TEMPLATE",
        type=str,
        help="""Name of the template to be used
  The template file should be present in ./templates""")

    # parse the options
    args = parser.parse_args()

    dives = parse_config_file(args.config_files)
    if dives is None:
        dives = {}

    if args.gflow:
        try:
            settings.GF_LOW = float(eval(args.gflow.strip('%'))) / 100
        except ValueError:
            parser.error("Error while parsing option gflow : %s" % args.gflow)

    if args.gfhigh:
        try:
            settings.GF_HIGH = float(eval(args.gfhigh.strip('%'))) / 100
        except ValueError:
            parser.error("Error while parsing option gfhigh: %s" % args.gfhigh)

    if args.water:
        if args.water.lower() == "sea":
            settings.WATER_DENSITY = settings.SEA_WATER_DENSITY
        if args.water.lower() == "fresh":
            settings.WATER_DENSITY = settings.FRESH_WATER_DENSITY

    if args.altitude:
        settings.AMBIANT_PRESSURE_SURFACE = altitude_to_pressure(args.altitude)

    if args.diveconsrate:
        try:
            settings.DIVE_CONSUMPTION_RATE = \
                float(eval(args.diveconsrate)) / 60
        except ValueError:
            parser.error("Error while parsing option diveconsrate : %s" %
                         args.diveconsrate)

    if args.decoconsrate:
        try:
            settings.DECO_CONSUMPTION_RATE = \
                float(eval(args.decoconsrate)) / 60
        except ValueError:
            parser.error("Error while parsing option decoconsrate : %s" %
                         args.decoconsrate)

    if args.descentrate:
        try:
            settings.DESCENT_RATE = float(eval(args.descentrate)) / 60
        except ValueError:
            parser.error("Error while parsing option descentrate : %s" %
                         args.descentrate)

    if args.ascentrate:
        try:
            settings.ASCENT_RATE = float(eval(args.ascentrate)) / 60
        except ValueError:
            parser.error("Error while parsing option ascentrate : %s" %
                         args.ascentrate)

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

    if args.depthcalcmethod == 'simple' or args.depthcalcmethod == 'complex':
        settings.METHOD_FOR_DEPTH_CALCULATION = args.depthcalcmethod

    if args.travelswitch == 'late' or args.travelswitch == 'early':
        settings.TRAVEL_SWITCH = args.travelswitch

    if args.surfacetemp is not None:
        settings.SURFACE_TEMP = args.surfacetemp

    if args.ambiantpressureatsea:
        print "---------------- %s ---------------------" % \
              args.ambiantpressureatsea
        settings.AMBIANT_PRESSURE_SEA_LEVEL = args.ambiantpressureatsea

    # try to find tank(s) and segment(s).
    # if found, add this dive to the (eventually) other dives defined in config
    # files.
    # this will be the last dive
    tanks = {}
    if args.tanks:
        for tank in args.tanks:
            (name, f_o2, f_he, volume, pressure, rule) = tank.split(";")

            tanks[name] = Tank(
                float(f_o2),
                float(f_he),
                max_ppo2=settings.DEFAULT_MAX_PPO2,
                tank_vol=float(eval(volume)),
                tank_pressure=float(eval(pressure)),
                tank_rule=rule)

    if tanks == {}:
        # no tank provided, try to get the previous tanks
        try:
            tanks = dives[dives.items()[-1][0]]['tanks']
        except (KeyError, IndexError):
            print "Error : no tank provided for this dive !"
            sys.exit(0)

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
                    float(eval(depth)),
                    float(eval(time)),
                    tanks[tankname],
                    float(setpoint))
            except KeyError:
                parser.error(
                    "Error : tank name (%s) in not found in tank list !" %
                    tankname)
            except:
                pass
            num_seg += 1
        segments = OrderedDict(sorted(segments.items(), key=lambda t: t[0]))
        if args.surfaceinterval:
            dives['diveCLI'] = {'tanks': tanks, 'segments': segments,
                                'surface_interval': eval(args.surfaceinterval)}
        else:
            dives['diveCLI'] = {'tanks': tanks, 'segments': segments,
                                'surface_interval': 0}

    if args.template:
        settings.TEMPLATE = args.template
        # returns
    return (args, dives)


def main():
    """main

    main uses the parameters, tanks and dives given in config file(s)
    and/or command line, calculates the dives and return the output in stdout.

    *Keyword Arguments:*
        <none>

    *Return:*
        <nothing>

    *Raise:*
        <nothing>
    """
    if sys.version_info < (2, 7):
        raise SystemExit("ERROR: This programm needs python 2.7 or greater")

    activate_debug()

    # get the version
    try:
        f = open("RELEASE-VERSION", "r")

        try:
            version = f.readlines()[0]
            settings.__VERSION__ = version.strip()

        finally:
            f.close()
    except:
        settings.__VERSION__ = "unknown"

    (args, dives) = parse_arguments()

    profiles = []
    previous_dive = None
    for dive in dives:
        if previous_dive is None:
            current_dive = Dive(
                dives[dive]['segments'].values(),
                dives[dive]['tanks'].values())
        else:
            current_dive = Dive(
                dives[dive]['segments'].values(),
                dives[dive]['tanks'].values(),
                previous_dive
            )
        if dives[dive]['surface_interval']:
            current_dive.do_surface_interval(dives[dive]['surface_interval'])

        current_dive.do_dive_without_exceptions()
        profiles.append(current_dive)
        previous_dive = current_dive
        # now, dive exceptins do not stop the program anymore, but can be
        # displayed in the output template instead. The used MUST take care of
        # the result.

    # now calculate no flight time based on the last dive
    try:
        current_dive.no_flight_time_wo_exception()
    except Exception, unhandled_exc:
        LOGGER.error("Exception while calculating no flight time: %s" %
                     unhandled_exc)

    # now Prepare the output
    env = Environment(loader=PackageLoader('dipplanner', 'templates'))
    tpl = env.get_template(settings.TEMPLATE)
    text = tpl.render(settings=settings, dives=profiles)
    print text
