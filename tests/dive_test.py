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
"""
Test for Profile class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
from dive import Dive
from dive import ProcessingError, NothingToProcess, InfiniteDeco
from tank import Tank
from segment import SegmentDive, SegmentDeco, SegmentAscDesc
from segment import UnauthorizedMod

class Test(unittest.TestCase):
  def setUp(self):
    airtank = Tank()
    diveseg1 = SegmentDive(30, 30*60, airtank, 0)
    self.profile1 = Dive([diveseg1], [airtank])
    
  def test1(self):
    self.profile1.do_dive()
    assert self.profile1.output_segments == [], "bad output segments ? (%s)" % str(self.profile1.output_segments)
    pass
    
if __name__ == "__main__":
  unittest.main() 