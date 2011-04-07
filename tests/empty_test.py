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
"""
Test for XXXXX class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
import dipplanner

class TestXXXXXXX(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
      
class TestXXXXXXXSimple1(TestXXXXXXX):
  def runTest(self):
    pass
    
if __name__ == "__main__":
  import sys
  suite = unittest.findTestCases(sys.modules[__name__])  
  #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  unittest.TextTestRunner(verbosity=2).run(suite)