#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Thomas Chiroux
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
# Strongly inspired by Guy Wittig's MVPlan 
"""main dipplanner module
runs in command line and output resulting dive profile
also initiate log files
"""

__version__ = "0.2nightly"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import sys
#from optparse import OptionParser, OptionGroup
import logging
from ConfigParser import SafeConfigParser
import argparse
import settings
from dive import Dive
from dive import ProcessingError, NothingToProcess, InfiniteDeco
from tank import Tank
from segment import SegmentDive, SegmentDeco, SegmentAscDesc
from segment import UnauthorizedMod
from tools import pressure_converter

LOGGER = logging.getLogger("dipplanner")

# optparse hack...
    
def activate_debug():
  """setup the default debug parameters
  
  it's mainly used for test cases who needs also logging to be set
  
  Keyword Arguments:
  <none>
  
  Return:
  <nothing>
  
  Raise:
  <nothing>

  """
  LOGGER.setLevel(logging.DEBUG)
  # create file handler which logs even debug messages
  fh = logging.FileHandler("dipplanner.log")
  fh.setLevel(logging.DEBUG)
  # create console handler with a higher log level
  ch = logging.StreamHandler()
  ch.setLevel(logging.WARNING)
  # create formatter and add it to the handlers
  formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)
  # add the handlers to the logger
  LOGGER.addHandler(fh)
  LOGGER.addHandler(ch)

def activate_debug_for_tests():
  """setup the default debug parameters
  
  it's mainly used for test cases who needs also logging to be set
  
  Keyword Arguments:
  <none>
  
  Return:
  <nothing>
  
  Raise:
  <nothing>

  """
  LOGGER.setLevel(logging.CRITICAL)
  ch = logging.StreamHandler()
  ch.setLevel(logging.INFO)
  formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
  ch.setFormatter(formatter)
  LOGGER.addHandler(ch)

def parse_config_file(filenames):
  """parse a config file and change default settings values
  
  Keyword Arguments:
  filename -- name (and path) of the config file to be parsed

  Returns:
  <nothing>

  Raise:
  Nothing, but can exit
  """
  if filenames is not None:
    config = SafeConfigParser()
    filesread = config.read(filenames)
  else:
    LOGGER.warning("No config file found: skip config from files")
    return (None, None)

  missing = set(filenames) - set(filesread)
  if len(filesread) == 0:
    LOGGER.warning("No config file found: skip config from files")
    return (None, None)
    
  if len(missing) > 0:
    if len(missing) == 1:
      LOGGER.warning("Config file : %s not found, skip it" % list(missing)[0])
    else:
      LOGGER.warning("Config files : %s not found, skip them" %\
                                    ', '.join(str(n) for n in list(missing)) )
  
  # now try to find each parameter and set the new setting
  if config.has_section('advanced'):
    section = 'advanced'
    if config.has_option(section, 'fresh_water_density'):
      settings.FRESH_WATER_DENSITY = float(config.get(section, 'fresh_water_density'))
    if config.has_option(section, 'sea_water_density'):
      settings.SEA_WATER_DENSITY = float(config.get(section, 'sea_water_density'))
    if config.has_option(section, 'absolute_max_ppo2'):
      settings.ABSOLUTE_MAX_PPO2 = float(config.get(section, 'absolute_max_ppo2'))
    if config.has_option(section, 'absolute_min_ppo2'):
      settings.ABSOLUTE_MIN_PPO2 = float(config.get(section, 'absolute_min_ppo2'))
    if config.has_option(section, 'absolute_max_tank_pressure'):
      settings.ABSOLUTE_MAX_TANK_PRESSURE = float(config.get(section, 'absolute_max_tank_pressure'))
    if config.has_option(section, 'absolute_max_tank_size'):
      settings.ABSOLUTE_MAX_TANK_SIZE = float(config.get(section, 'absolute_max_tank_size'))
          
    if config.has_option(section, 'pp_h2o_surface'):
      settings.PP_H2O_SURFACE = float(config.get(section, 'pp_h2o_surface'))
    if config.has_option(section, 'he_narcotic_value'):
      settings.HE_NARCOTIC_VALUE = float(config.get(section, 'he_narcotic_value'))
    if config.has_option(section, 'n2_narcotic_value'):
      settings.N2_NARCOTIC_VALUE = float(config.get(section, 'n2_narcotic_value'))
    if config.has_option(section, 'o2_narcotic_value'):
      settings.O2_NARCOTIC_VALUE = float(config.get(section, 'o2_narcotic_value'))
    if config.has_option(section, 'ar_narcotic_value'):
      settings.AR_NARCOTIC_VALUE = float(config.get(section, 'ar_narcotic_value'))
    
    if config.has_option(section, 'stop_depth_increment'):
      settings.STOP_DEPTH_INCREMENT = float(config.get(section, 'stop_depth_increment'))
    if config.has_option(section, 'last_stop_depth'):
      settings.LAST_STOP_DEPTH = float(config.get(section, 'last_stop_depth'))
    if config.has_option(section, 'stop_time_increment'):
      settings.STOP_TIME_INCREMENT = float(config.get(section, 'stop_time_increment'))
    if config.has_option(section, 'force_all_stops'):
      settings.FORCE_ALL_STOPS = eval(config.get(section, 'force_all_stops').title())
    if config.has_option(section, 'ambiant_pressure_sea_level'):
      settings.AMBIANT_PRESSURE_SEA_LEVEL = float(config.get(section, 'ambiant_pressure_sea_level'))
    if config.has_option(section, 'method_for_depth_calculation'):
      if config.get(section, 'method_for_depth_calculation') == 'simple' or \
         config.get(section, 'method_for_depth_calculation') == 'complex':
         settings.METHOD_FOR_DEPTH_CALCULATION = config.get(section, 'method_for_depth_calculation')

  if config.has_section('general'):
    section = 'general'
    if config.has_option(section, 'max_ppo2'):
      settings.DEFAULT_MAX_PPO2 = float(config.get(section, 'max_ppo2'))
    if config.has_option(section, 'min_ppo2'):
      settings.DEFAULT_MIN_PPO2 = float(config.get(section, 'min_ppo2'))
    if config.has_option(section, 'descent_rate'):
      settings.DESCENT_RATE = float(config.get(section, 'descent_rate'))/60
    if config.has_option(section, 'ascent_rate'):
      settings.ASCENT_RATE = float(config.get(section, 'ascent_rate'))/60
      
    if config.has_option(section, 'dive_consumption_rate'):
      settings.DIVE_CONSUMPTION_RATE = \
                        float(config.get(section, 'dive_consumption_rate'))/60
    if config.has_option(section, 'deco_consumption_rate'):
      settings.DIVE_CONSUMPTION_RATE = \
                        float(config.get(section, 'deco_consumption_rate'))/60
    
    if config.has_option(section, 'gf_low'):
      settings.GF_LOW = float(eval(config.get(section, 'gf_low').strip('%')))/100
    if config.has_option(section, 'gf_high'):
      settings.GF_HIGH = float(eval(config.get(section, 'gf_high').strip('%')))/100
      
    if config.has_option(section, 'water'):
      if config.get(section, 'water') == 'sea':
        settings.WATER_DENSITY = settings.SEA_WATER_DENSITY
      elif config.get(section, 'water') == 'fresh':
        settings.WATER_DENSITY = settings.FRESH_WATER_DENSITY        

    if config.has_option(section, 'altitude'):
      settings.AMBIANT_PRESSURE_SURFACE = \
                    pressure_converter(float(config.get(section, 'altitude')))  

    if config.has_option(section, 'run_time'):
      settings.RUN_TIME = eval(config.get(section, 'run_time').title())

    if config.has_option(section, 'use_oc_deco'):
      settings.RUN_TIME = eval(config.get(section, 'use_oc_deco').title())
      
    if config.has_option(section, 'multilevel_mode'):
      settings.RUN_TIME = eval(config.get(section, 'multilevel_mode').title())
  
  tanks = {}
  segments = []
  if config.has_section('tanks'):
    section = 'tanks'
    for parameter_name, parameter_value in config.items(section):
      (name, fO2, fHe, volume, pressure) = parameter_value.split(";")
      tanks[name] = Tank(float(fO2), 
                       float(fHe),
                       max_ppo2=settings.DEFAULT_MAX_PPO2,
                       tank_vol=float(eval(volume)), 
                       tank_pressure=float(eval(pressure)))
  
  if config.has_section('segments'):
    section = 'segments'
    for parameter_name, parameter_value in config.items(section):
      (depth, time, tankname, setpoint) = parameter_value.split(";")
      try:
        segments.append(SegmentDive(float(eval(depth)), 
                                    float(eval(time)), 
                                    tanks[tankname], 
                                    float(setpoint)))
      except KeyError:
        print "Error : tank name (%s) in not found in tank list !" % tankname
        sys.exit(0)
      except:
        raise

  return (tanks, segments)

def parse_arguments():
  """parse all command lines options
  
  could also exit from program because of wrong arguments
  
  Keyword Arguments:
  none
  
  Returns:
  a list with args, tanks and segments
  
  Raise:
  Nothing, but can exit
  """
  usage = """%(prog)s [options]"""
  description = """%(prog)s calculates and output dive profile
Thomas Chiroux, 2011-2012 - see http://dipplanner.org
"""

  epilog = ""

  parser = argparse.ArgumentParser(
                        description = description,
                        usage = usage,
                        epilog = epilog,
                        formatter_class = argparse.RawTextHelpFormatter )
                        
  group1 = parser.add_argument_group("Mandatory Options",
      """Either presence of tank and segment inside a config file or
this mandatory options (at leat one of each) are needed for this program to run""")
  group1.add_argument("-c", "--config", dest="config_files",
                     action="append", type=str, metavar = "STRING",
                     help="""path for config file.
Default : ./config.cfg
see manual for more infos on config file""")

  group1.add_argument("-t", "--tank", dest="tanks",
                     action="append", type=str, metavar = "STRING",
                     help="""Tank used for the dive
Format:  "tank_name;fO2;fHe;Volume(l);Pressure(bar)"
Example: "airtank;0.21;0.0;12;200"
""")
  group1.add_argument("-s", "--segment", dest="segments",
                     action="append", type=str, metavar = "STRING",
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

  group2 = parser.add_argument_group("Dive Parameters")
  group2.add_argument("--gflow", metavar="VAL", type=str,
                    help="""GF low, in """)
  group2.add_argument("--gfhigh", metavar="VAL", type=str,
                    help="""GF high, in """)
  group2.add_argument("--water", metavar="VAL", type=str,
                  help="""type of water : sea or fresh""")

  group2.add_argument("--altitude", metavar="VAL", type=int,
    help="""altitude of the dive in meter.""")
  group2.add_argument("--diveconsrate", metavar="VAL", type=str,
    help="""gas consumption rate during dive (in l/minute).""")
  group2.add_argument("--decoconsrate", metavar="VAL", type=str,
    help="""gas consumption rate during deco (in l/minute).""")
  group2.add_argument("--descentrate", metavar="VAL", type=str,
    help="""descent rate (in m/minute).""")
  group2.add_argument("--ascentrate", metavar="VAL", type=str,
    help="""ascent rate (in m/minute).""")

  group2.add_argument("--maxppo2", metavar="VAL", type=float,
    help="max allowed ppo2 for this dive.")
  group2.add_argument("--minppo2", metavar="VAL", type=float,
    help="minimum allowed ppo2 for this dive.")
  group2.add_argument("--samegasfordeco", action="store_true",
    help="if set, do not use deco tanks (or bailout) for decompressions")
  group2.add_argument("--forcesegmenttime", action="store_true",
    help="""if set, each input segment will be dove
at the full time of the segment.
By default the segment time is shortened by descent or ascent time
""")
  
  group3 = parser.add_argument_group("Internal Parameters")
  group3.add_argument("--depthcalcmethod", metavar="simple|complex",
                    type=str,
          help="""method used for pressure from depth calculation.
          Simple method uses only +10m = +1bar
          Complex methods uses real water density""")
  group3.add_argument("--ambiantpressureatsea", metavar="VAL",
                    type=float,
                    help="""Change ambiant pressure at sea level (in bar)""")

  # parse the options
  args = parser.parse_args()

  tanks, segments = parse_config_file(args.config_files)
  if tanks is None:
    tanks = {}
  if segments is None:
    segments = []
    
  if args.gflow:
    try:
      settings.GF_LOW = float(eval(args.gflow.strip('%')))/100
    except:
      parser.error("Error while parsing option gflow : %s" % args.gflow)

  if args.gfhigh:
    try:
      settings.GF_HIGH = float(eval(args.gfhigh.strip('%')))/100
    except:
      parser.error("Error while parsing option gfhigh : %s" % args.gfhigh)

  if args.water:
    if args.water.lower() == "sea":
      settings.WATER_DENSITY = settings.SEA_WATER_DENSITY
    if args.water.lower() == "fresh":
      settings.WATER_DENSITY = settings.FRESH_WATER_DENSITY
      
  if args.altitude:
    settings.AMBIANT_PRESSURE_SURFACE = pressure_converter(args.altitude)

  if args.diveconsrate:
    try:
      settings.DIVE_CONSUMPTION_RATE = float(eval(args.diveconsrate))/60
    except:
      parser.error("Error while parsing option diveconsrate : %s" %\
                   args.diveconsrate)
      
  if args.decoconsrate:
    try:
      settings.DECO_CONSUMPTION_RATE = float(eval(args.decoconsrate))/60
    except:
      parser.error("Error while parsing option decoconsrate : %s" %\
                   args.decoconsrate)

  if args.descentrate:
    try:
      settings.DESCENT_RATE = float(eval(args.descentrate))/60
    except:
      parser.error("Error while parsing option descentrate : %s" %\
                   args.descentrate)
      
  if args.ascentrate:
    try:
      settings.ASCENT_RATE = float(eval(args.ascentrate))/60
    except:
      parser.error("Error while parsing option ascentrate : %s" %\
                   args.ascentrate)
  
  if args.maxppo2:
    settings.DEFAULT_MAX_PPO2 = args.maxppo2

  if args.minppo2:
    settings.DEFAULT_MIN_PPO2 = args.minppo2
  
  if args.samegasfordeco:
    settings.USE_OC_DECO = False
  
  if args.forcesegmenttime:
    settings.RUN_TIME = False
  
  if args.depthcalcmethod == 'simple' or\
     args.depthcalcmethod == 'complex':
    settings.METHOD_FOR_DEPTH_CALCULATION = args.depthcalcmethod
  
  if args.ambiantpressureatsea:
    settings.AMBIANT_PRESSURE_SEA_LEVEL = args.ambiantpressureatsea
   
  if args.tanks:
    for tank in args.tanks:
      (name, fO2, fHe, volume, pressure) = tank.split(";")
      tanks[name] = Tank(float(fO2), 
                         float(fHe),
                         max_ppo2=settings.DEFAULT_MAX_PPO2,
                         tank_vol=float(eval(volume)), 
                         tank_pressure=float(eval(pressure)))
  
  if args.segments:
    for seg in args.segments:
      (depth, time, tankname, setpoint) = seg.split(";")
      # looks for tank in tanks
      try:
        segments.append(SegmentDive(float(eval(depth)), 
                                    float(eval(time)), 
                                    tanks[tankname], 
                                    float(setpoint)))
      except KeyError:
        parser.error("Error : tank name (%s) in not found in tank list !" % tankname)
      except:
        raise
     
  # returns
  return (args, tanks, segments)

if __name__ == "__main__":
  activate_debug()
  (args, tanks, segments) = parse_arguments()
  
  if tanks and segments:
    profile = Dive(segments, tanks.values())
    profile.do_dive()
    print profile
  else:
    print "Error : you must provide tanks and segments"
    sys.exit(0)