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
"""Base Class for exceptions for dipplanner module
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import logging

class DipplannerException(Exception):
  """Base exception class for dipplanner
  """
  def __init__(self, description):
    self.logger = logging.getLogger("dipplanner.DipplannerException")
    self.description = description
  
  def __str__(self):
    return repr(self.description)