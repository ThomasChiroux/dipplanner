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
"""tools modules

Contains:
seconds_to_strtime -- function
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

def seconds_to_strtime(duration):
  """Convert a value in seconds into a string representing the time in
  minutes and seconds
  (like 2:06)
  It does returns only minutes and seconds, not hours, minutes and seconds
  
  Keyword Arguments:
  duration - the duration in seconds
  
  Returns:
  <string> : the time in minutes and seconds
  
  Raise:
  ValueError: when bad time values
  
  """
  if duration < 0:
    raise ValueError("time can not be negative")
    
  text = "%3d:%02d" % (int(duration/60), int(duration % 60))
  return text