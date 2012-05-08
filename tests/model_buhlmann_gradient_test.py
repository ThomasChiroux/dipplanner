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

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested

from model.buhlmann.gradient import Gradient
import dipplanner
import settings

class TestModelBuhlmannGradient(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
    settings.RUN_TIME = True
    settings.SURFACE_TEMP = 12
    self.gradient1 = Gradient(0.3, 0.8)
    self.gradient2 = Gradient(0.35, 0.75)
  
class TestModelBuhlmannGradientSimple1(TestModelBuhlmannGradient):
  def runTest(self):
    assert self.gradient1.gf_low == 0.3, "wrong gw_low : %s" % self.gradient1.gf_low

class TestModelBuhlmannGradientSimple2(TestModelBuhlmannGradient):
  def runTest(self):
    assert self.gradient1.gf_high == 0.8, "wrong gw_high : %s" % self.gradient1.gf_high

class TestModelBuhlmannGradientSimple3(TestModelBuhlmannGradient):
  def runTest(self):
    assert self.gradient1.gf_slope == 1.0, "wrong gw_slope : %s" % self.gradient1.gf_slope

class TestModelBuhlmannGradientSimple4(TestModelBuhlmannGradient):
  def runTest(self):
    assert self.gradient1.gf == 0.3, "wrong gw_low : %s" % self.gradient1.gf

class TestModelBuhlmannGradientSimple5(TestModelBuhlmannGradient):
  def runTest(self):
    self.gradient2.set_gf_slope_at_depth(12)
    assert round(self.gradient2.gf_slope, 13) == -0.0333333333333, "wrong gw_slope : %s" % self.gradient2.gf_slope
    
class TestModelBuhlmannGradientSimple6(TestModelBuhlmannGradient):
  def runTest(self):
    self.gradient2.set_gf_slope_at_depth(6)
    self.gradient2.set_gf_at_depth(6)
    assert self.gradient2.gf == 0.35, "wrong gw_low : %s" % self.gradient2.gf

if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('tests', metavar='TestName', type=str, nargs='*',
                      help='name of the tests to run (separated by space) [optionnal]')
  args = parser.parse_args()
  if args.tests:
    suite = unittest.TestLoader().loadTestsFromNames(args.tests, sys.modules[__name__])
  else:
    suite = unittest.findTestCases(sys.modules[__name__])
  unittest.TextTestRunner(verbosity=2).run(suite)
