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

__version__ = "0.2working"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import sys
from optparse import OptionParser, OptionGroup
import logging

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
      """Without this mandatory options (at leat one of each), 
the program will not run""")
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
  group2.add_option("--gflow", metavar="VAL", type="string", default="30",
                    help="""GF low, in %, default value : 30%""")
  group2.add_option("--gfhigh", metavar="VAL", type="string", default="80",
                    help="""GF high, in %, default value : 80%""")
  group2.add_option("--water", metavar="VAL", type="string", default="sea",
                  help="""type of water : sea or fresh, default:sea""")
  
  group2.add_option("--altitude", metavar="VAL", type="int", default=0,
    help="""altitude of the dive in meter. default: sea altitude: 0m""")
  group2.add_option("--diveconsrate", metavar="VAL", type="string", default="20",
    help="""gas consumption rate during dive (in l/minute). default: 20l/min""")
  group2.add_option("--decoconsrate", metavar="VAL", type="string", default="15",
    help="""gas consumption rate during deco (in l/minute). default: 15l/min""")
  group2.add_option("--descentrate", metavar="VAL", type="string", default="20",
    help="""descent rate (in m/minute). default: 20m/min""")
  group2.add_option("--ascentrate", metavar="VAL", type="string", default="10",
    help="""ascent rate (in m/minute). default: 10m/min""")  
  
  group2.add_option("--maxppo2", metavar="VAL", type="float", default=1.6,
    help="max allowed ppo2 for this dive. default: 1.6")
  group2.add_option("--minppo2", metavar="VAL", type="float", default=0.19,
    help="minimum allowed ppo2 for this dive. default: 0.19")  
  group2.add_option("--samegasfordeco", action="store_true", default=False,
    help="if set, do not use deco tanks (or bailout) for decompressions")  
  group2.add_option("--forcesegmenttime", action="store_true", default=False,
    help="""if set, each input segment will be dove
at the full time of the segment. 
By default the segment time is shortened by descent or ascent time
""")
    
  parser.add_option_group(group2)
  
  group3 = OptionGroup(parser, "Internal Parameters")
  group3.add_option("--depthcalcmethod", metavar="simple|complex", 
                    type="string", default='complex',
          help="""method used for pressure from depth calculation. 
          Simple method uses only +10m = +1bar
          Complex methods uses real water density""")
  group3.add_option("--ambiantpressureatsea", metavar="VAL",
                    type=float, default=1.01325,
                    help="""Change ambiant pressure at sea level (in bar)""")
  parser.add_option_group(group3)
  
  # parse the options
  (options, args) = parser.parse_args()

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
      parser.error("Error while parsing option diveconsrate : %s" % options.diveconsrate)
      
  if options.decoconsrate:
    try:
      settings.DECO_CONSUMPTION_RATE = float(eval(options.decoconsrate))/60
    except:
      parser.error("Error while parsing option decoconsrate : %s" % options.decoconsrate)  

  if options.descentrate:
    try:
      settings.DESCENT_RATE = float(eval(options.descentrate))/60
    except:
      parser.error("Error while parsing option descentrate : %s" % options.descentrate)
      
  if options.ascentrate:
    try:
      settings.ASCENT_RATE = float(eval(options.ascentrate))/60
    except:
      parser.error("Error while parsing option ascentrate : %s" % options.ascentrate)  
  
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
    
  # sanity checks
  if not options.tanks:
    parser.error("You must provides at least one Tank for the dive")
     
  # returns
  return (options, args)


if __name__ == "__main__":
  """run from command line"""
  activate_debug()
  (options, args) = parse_arguments()
  tanks = {}
  for tank in options.tanks:
    (name, fO2, fHe, volume, pressure) = tank.split(";")
    tanks[name] = Tank(float(fO2), 
                       float(fHe),
                       max_ppo2=settings.DEFAULT_MAX_PPO2,
                       tank_vol=float(eval(volume)), 
                       tank_pressure=float(eval(pressure)))
  
  segments = []
  for seg in options.segments:
    (depth, time, tankname, setpoint) = seg.split(";")
    # looks for tank in tanks
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
      
  profile = Dive(segments, tanks.values())
  profile.do_dive()
  print profile