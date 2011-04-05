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

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

from optparse import OptionParser, OptionGroup
import logging

import settings
from dive import Dive
from dive import ProcessingError, NothingToProcess, InfiniteDeco
from tank import Tank

LOGGER = logging.getLogger("dipplanner")

def activate_debug():
  """setup the debug parameters"""
  LOGGER.setLevel(logging.DEBUG)
  # create file handler which logs even debug messages
  fh = logging.FileHandler("dipplanner.log")
  fh.setLevel(logging.INFO)
  # create console handler with a higher log level
  ch = logging.StreamHandler()
  ch.setLevel(logging.WARNING)
  # create formatter and add it to the handlers
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)
  # add the handlers to the logger
  LOGGER.addHandler(fh)
  LOGGER.addHandler(ch)
  
def parse_arguments():
  """parse all command lines options"""
  pass

if __name__ == "__main__":
  """run from command line"""
  (options, args) = parse_arguments()