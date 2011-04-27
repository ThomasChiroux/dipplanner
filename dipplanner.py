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
from optparse import OptionParser, OptionGroup
import logging
from ConfigParser import SafeConfigParser

from optparse_hack import IndentedHelpFormatterWithNL
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
  a list with 2 tuples: options and args
  
  Raise:
  Nothing, but can exit
  """
  usage = """usage: %prog [options]"""
  description = """%prog calculates and output dive profile
(c)Thomas Chiroux, 2011 - see http://dipplanner.org 
"""

  epilog = ""
  parser = OptionParser(description=description, usage=usage, epilog=epilog,
                        version="%prog v"+__version__,
                        formatter=IndentedHelpFormatterWithNL() )
                        
  group1 = OptionGroup(parser, "Mandatory Options",
      """Either presence of tank and segment inside a config file or
this mandatory options (at leat one of each) are needed for this program to run""")
  group1.add_option("-c", "--config", dest="config_files", 
                     action="append", type="string", metavar = "STRING",
                     help="""path for config file. 
Default : ./config.cfg"
see manual for more infos on config file
""")

  group1.add_option("-t", "--tank", dest="tanks", 
                     action="append", type="string", metavar = "STRING",
                     help="""Tank used for the dive
Format:  "tank_name;fO2;fHe;Volume(l);Pressure(bar)"
Example: "airtank;0.21;0.0;12;200"
""")
  group1.add_option("-s", "--segment", dest="segments", 
                     action="append", type="string", metavar = "STRING",
                     help="""Input segments used for the dive\n\
Format:  "depth;duration;tank;setpoint"
Example: "30;20*60;airtank;0.0"
* depth: in meter
* duration : in seconds (operations are allowed like: '30*60')
* tank : name of the tank (same name as tank options)
* setpoint : 0 if OC, setpoint if CCR

You can specify multiple args like:
%prog [other_options] -s "30;1000;airtank;0.0" -s "20;800;airtank;0.0"
""")
  parser.add_option_group(group1)
  
  group2 = OptionGroup(parser, "Dive Parameters")
  group2.add_option("--gflow", metavar="VAL", type="string",
                    help="""GF low, in %""")
  group2.add_option("--gfhigh", metavar="VAL", type="string",
                    help="""GF high, in %""")
  group2.add_option("--water", metavar="VAL", type="string",
                  help="""type of water : sea or fresh""")
  
  group2.add_option("--altitude", metavar="VAL", type="int",
    help="""altitude of the dive in meter.""")
  group2.add_option("--diveconsrate", metavar="VAL", type="string",
    help="""gas consumption rate during dive (in l/minute).""")
  group2.add_option("--decoconsrate", metavar="VAL", type="string",
    help="""gas consumption rate during deco (in l/minute).""")
  group2.add_option("--descentrate", metavar="VAL", type="string",
    help="""descent rate (in m/minute).""")
  group2.add_option("--ascentrate", metavar="VAL", type="string",
    help="""ascent rate (in m/minute).""")  
  
  group2.add_option("--maxppo2", metavar="VAL", type="float",
    help="max allowed ppo2 for this dive.")
  group2.add_option("--minppo2", metavar="VAL", type="float",
    help="minimum allowed ppo2 for this dive.")  
  group2.add_option("--samegasfordeco", action="store_true",
    help="if set, do not use deco tanks (or bailout) for decompressions")  
  group2.add_option("--forcesegmenttime", action="store_true",
    help="""if set, each input segment will be dove
at the full time of the segment. 
By default the segment time is shortened by descent or ascent time
""")
    
  parser.add_option_group(group2)
  
  group3 = OptionGroup(parser, "Internal Parameters")
  group3.add_option("--depthcalcmethod", metavar="simple|complex", 
                    type="string",
          help="""method used for pressure from depth calculation. 
          Simple method uses only +10m = +1bar
          Complex methods uses real water density""")
  group3.add_option("--ambiantpressureatsea", metavar="VAL",
                    type=float,
                    help="""Change ambiant pressure at sea level (in bar)""")
  parser.add_option_group(group3)
  
  # parse the options
  (options, args) = parser.parse_args()

  tanks, segments = parse_config_file(options.config_files)
  if tanks is None:
    tanks = {}
  if segments is None:
    segments = []
    
  if options.gflow:
    try:
      settings.GF_LOW = float(eval(options.gflow.strip('%')))/100
    except:
      parser.error("Error while parsing option gflow : %s" % options.gflow)

  if options.gfhigh:
    try:
      settings.GF_HIGH = float(eval(options.gfhigh.strip('%')))/100
    except:
      parser.error("Error while parsing option gfhigh : %s" % options.gfhigh)

  if options.water:
    if options.water.lower() == "sea":
      settings.WATER_DENSITY = settings.SEA_WATER_DENSITY
    if options.water.lower() == "fresh":
      settings.WATER_DENSITY = settings.FRESH_WATER_DENSITY
      
  if options.altitude:
    settings.AMBIANT_PRESSURE_SURFACE = pressure_converter(options.altitude)

  if options.diveconsrate:
    try:
      settings.DIVE_CONSUMPTION_RATE = float(eval(options.diveconsrate))/60
    except:
      parser.error("Error while parsing option diveconsrate : %s" % \
                                                          options.diveconsrate)
      
  if options.decoconsrate:
    try:
      settings.DECO_CONSUMPTION_RATE = float(eval(options.decoconsrate))/60
    except:
      parser.error("Error while parsing option decoconsrate : %s" % \
                                                          options.decoconsrate)  

  if options.descentrate:
    try:
      settings.DESCENT_RATE = float(eval(options.descentrate))/60
    except:
      parser.error("Error while parsing option descentrate : %s" % \
                                                          options.descentrate)
      
  if options.ascentrate:
    try:
      settings.ASCENT_RATE = float(eval(options.ascentrate))/60
    except:
      parser.error("Error while parsing option ascentrate : %s" % \
                                                           options.ascentrate)  
  
  if options.maxppo2:
    settings.DEFAULT_MAX_PPO2 = options.maxppo2

  if options.minppo2:
    settings.DEFAULT_MIN_PPO2 = options.minppo2
  
  if options.samegasfordeco:
    settings.USE_OC_DECO = False
  
  if options.forcesegmenttime:
    settings.RUN_TIME = False
  
  if options.depthcalcmethod == 'simple' or \
     options.depthcalcmethod == 'complex':
    settings.METHOD_FOR_DEPTH_CALCULATION = options.depthcalcmethod
  
  if options.ambiantpressureatsea:
    settings.AMBIANT_PRESSURE_SEA_LEVEL = options.ambiantpressureatsea
   
  if options.tanks: 
    for tank in options.tanks:
      (name, fO2, fHe, volume, pressure) = tank.split(";")
      tanks[name] = Tank(float(fO2), 
                         float(fHe),
                         max_ppo2=settings.DEFAULT_MAX_PPO2,
                         tank_vol=float(eval(volume)), 
                         tank_pressure=float(eval(pressure)))
  
  if options.segments:
    for seg in options.segments:
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
  return (options, args, tanks, segments)

if __name__ == "__main__":
  """run from command line"""
  activate_debug()
  (options, args, tanks, segments) = parse_arguments()
  
  if tanks and segments:
    profile = Dive(segments, tanks.values())
    profile.do_dive()
    print profile
  else:
    print "Error : you must provide tanks and segments"
    sys.exit(0)