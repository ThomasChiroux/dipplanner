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
    self.airtank = Tank()
    self.txtank1 = Tank(0.21, 0.30)

  def test_air_dive1(self):
    diveseg1 = SegmentDive(30, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    assert str(self.profile1) == "", "bad output segments ? (%s)" % str(self.profile1)

  def test_air_dive2(self):
    diveseg2 = SegmentDive(20, 30*60, self.airtank, 0)
    self.profile2 = Dive([diveseg2], [self.airtank])
    self.profile2.do_dive()
    assert str(self.profile2) == "", "bad output segments ? (%s)" % str(self.profile2)
    #pass
    
  def test_air_dive3(self):
    diveseg3 = SegmentDive(55, 30*60, self.airtank, 0)
    self.profile3 = Dive([diveseg3], [self.airtank])
    self.profile3.do_dive()
    assert str(self.profile3) == "", "bad output segments ? (%s)" % str(self.profile3)
    #pass
    
  def test_tx_dive1(self):
    #diveseg1 = SegmentDive(30, 30*60, self.txtank1, 0)
    #self.profile1 = Dive([diveseg1], [self.txtank1])
    #self.profile1.do_dive()
    #assert str(self.profile1) == "", "bad output segments ? (%s)" % str(self.profile1)
    pass
    
if __name__ == "__main__":
  unittest.main() 