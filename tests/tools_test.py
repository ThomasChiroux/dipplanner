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
Test for tools
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
import dipplanner
from tools import pressure_converter
from tools import depth_to_pressure

class TestTools(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
      
class TestPressureConverter0m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(0), 1.01325, 5, "Wrong pressure at 0m : %s" % pressure_converter(0))
class TestPressureConverter100m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(100), 1.00129437467, 10, "Wrong pressure at 100m : %s" % pressure_converter(100))
class TestPressureConverter500m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(500), 0.954608340287, 10, "Wrong pressure at 500m : %s" % pressure_converter(500))
class TestPressureConverter1000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(1000), 0.898745604274, 10, "Wrong pressure at 1000m : %s" % pressure_converter(1000))
class TestPressureConverter1500m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(1500), 0.845559905236, 10, "Wrong pressure at 1500m : %s" % pressure_converter(1500))
class TestPressureConverter2000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(2000), 0.794951974353, 10, "Wrong pressure at 2000m : %s" % pressure_converter(2000))
class TestPressureConverter3000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(3000), 0.701085204119, 10, "Wrong pressure at 3000m : %s" % pressure_converter(3000))
class TestPressureConverter4000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(4000), 0.616402064441, 10, "Wrong pressure at 4000m : %s" % pressure_converter(4000))
class TestPressureConverter5000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(5000), 0.540198800085, 10, "Wrong pressure at 5000m : %s" % pressure_converter(5000))
class TestPressureConverter6000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(6000), 0.471809934056, 10, "Wrong pressure at 6000m : %s" % pressure_converter(6000))
class TestPressureConverter7000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(7000), 0.4106070795, 10, "Wrong pressure at 7000m : %s" % pressure_converter(7000))
class TestPressureConverter8000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(8000), 0.355997759308, 10, "Wrong pressure at 8000m : %s" % pressure_converter(8000))
class TestPressureConverter9000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(9000), 0.307424233586, 10, "Wrong pressure at 9000m : %s" % pressure_converter(9000))
class TestPressureConverter10000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(pressure_converter(10000), 0.264362335127, 10, "Wrong pressure at 10000m : %s" % pressure_converter(10000))

class TestPressureConverternegative(TestTools):
  def runTest(self):
    try:
      pressure_converter(-10)
    except ValueError:
      pass
    else:
      self.fail("Negative pressure should raise ValueError")

class TestPressureConverterMore10000m(TestTools):
  def runTest(self):
    try:
      pressure_converter(15000)
    except ValueError:
      pass
    else:
      self.fail("altiture high than 10000m should raise ValueError")

class TestDepthPressure0m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(0), 0.0, 5, "Wrong depth pressure at 0m : %s" % depth_to_pressure(0))

class TestDepthPressure10m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(10), 1.01043, 5, "Wrong depth pressure at 10m : %s" % depth_to_pressure(10))
class TestDepthPressure20m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(20), 2.02086, 5, "Wrong depth pressure at 20m : %s" % depth_to_pressure(20))
class TestDepthPressure30m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(30), 3.03129, 5, "Wrong depth pressure at 30m : %s" % depth_to_pressure(30))
class TestDepthPressure40m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(40), 4.04172, 5, "Wrong depth pressure at 40m : %s" % depth_to_pressure(40))
class TestDepthPressure50m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(50), 5.05215, 5, "Wrong depth pressure at 50m : %s" % depth_to_pressure(50))
class TestDepthPressure60m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(60), 6.06258, 5, "Wrong depth pressure at 60m : %s" % depth_to_pressure(60))
class TestDepthPressure70m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(70), 7.07301, 5, "Wrong depth pressure at 70m : %s" % depth_to_pressure(70))
class TestDepthPressure80m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(80), 8.08344, 5, "Wrong depth pressure at 80m : %s" % depth_to_pressure(80))
class TestDepthPressure90m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(90), 9.09387, 5, "Wrong depth pressure at 90m : %s" % depth_to_pressure(90))
class TestDepthPressure100m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(depth_to_pressure(100), 10.1043, 4, "Wrong depth pressure at 100m : %s" % depth_to_pressure(100))
 
    
if __name__ == "__main__":
  import sys
  suite = unittest.findTestCases(sys.modules[__name__])  
  #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  unittest.TextTestRunner(verbosity=2).run(suite)