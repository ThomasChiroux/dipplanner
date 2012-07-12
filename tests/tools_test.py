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

from tools import altitude_to_pressure
from tools import depth_to_pressure
from tools import altitude_or_depth_to_absolute_pressure
from tools import pressure_to_depth
from tools import calculate_ppH2O_surf
from tools import convert_bar_to_psi
from tools import convert_cubicfeet_to_liter
from tools import convert_feet_to_meter
from tools import convert_liter_to_cubicfeet
from tools import convert_meter_to_feet
from tools import convert_psi_to_bar

class TestTools(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()

class TestAltOrDepthToAbsPressure0m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(0), 1.01325, 5, "Wrong pressure at 0m : %s" % altitude_or_depth_to_absolute_pressure(0))
class TestAltOrDepthToAbsPressure1000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(1000), 0.898745604274, 5, "Wrong pressure at 1000m : %s" % altitude_or_depth_to_absolute_pressure(1000))
class TestAltOrDepthToAbsPressure3000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(3000), 0.701085204119, 5, "Wrong pressure at 3000m : %s" % altitude_or_depth_to_absolute_pressure(3000))
class TestAltOrDepthToAbsPressure7000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(7000), 0.4106070795, 5, "Wrong pressure at 7000m : %s" % altitude_or_depth_to_absolute_pressure(7000))
class TestAltOrDepthToAbsPressure_minus10m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(-10), 2.02368, 5, "Wrong pressure at -10m : %s" % altitude_or_depth_to_absolute_pressure(-10))
class TestAltOrDepthToAbsPressure_minus30m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(-30), 4.04454, 5, "Wrong pressure at -30m : %s" % altitude_or_depth_to_absolute_pressure(-30))
class TestAltOrDepthToAbsPressur_minus100m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(-100), 11.11755, 5, "Wrong pressure at -100m : %s" % altitude_or_depth_to_absolute_pressure(-100))
class TestAltOrDepthToAbsPressure_minus160m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_or_depth_to_absolute_pressure(-160), 17.18013, 5, "Wrong pressure at -160m : %s" % altitude_or_depth_to_absolute_pressure(-160))


class TestPressureConverter0m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(0), 1.01325, 5, "Wrong pressure at 0m : %s" % altitude_to_pressure(0))
class TestPressureConverter100m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(100), 1.00129437467, 10, "Wrong pressure at 100m : %s" % altitude_to_pressure(100))
class TestPressureConverter500m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(500), 0.954608340287, 10, "Wrong pressure at 500m : %s" % altitude_to_pressure(500))
class TestPressureConverter1000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(1000), 0.898745604274, 10, "Wrong pressure at 1000m : %s" % altitude_to_pressure(1000))
class TestPressureConverter1500m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(1500), 0.845559905236, 10, "Wrong pressure at 1500m : %s" % altitude_to_pressure(1500))
class TestPressureConverter2000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(2000), 0.794951974353, 10, "Wrong pressure at 2000m : %s" % altitude_to_pressure(2000))
class TestPressureConverter3000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(3000), 0.701085204119, 10, "Wrong pressure at 3000m : %s" % altitude_to_pressure(3000))
class TestPressureConverter4000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(4000), 0.616402064441, 10, "Wrong pressure at 4000m : %s" % altitude_to_pressure(4000))
class TestPressureConverter5000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(5000), 0.540198800085, 10, "Wrong pressure at 5000m : %s" % altitude_to_pressure(5000))
class TestPressureConverter6000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(6000), 0.471809934056, 10, "Wrong pressure at 6000m : %s" % altitude_to_pressure(6000))
class TestPressureConverter7000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(7000), 0.4106070795, 10, "Wrong pressure at 7000m : %s" % altitude_to_pressure(7000))
class TestPressureConverter8000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(8000), 0.355997759308, 10, "Wrong pressure at 8000m : %s" % altitude_to_pressure(8000))
class TestPressureConverter9000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(9000), 0.307424233586, 10, "Wrong pressure at 9000m : %s" % altitude_to_pressure(9000))
class TestPressureConverter10000m(TestTools):
  def runTest(self):
    self.assertAlmostEqual(altitude_to_pressure(10000), 0.264362335127, 10, "Wrong pressure at 10000m : %s" % altitude_to_pressure(10000))

class TestPressureConverternegative(TestTools):
  def runTest(self):
    try:
      altitude_to_pressure(-10)
    except ValueError:
      pass
    else:
      self.fail("Negative pressure should raise ValueError")

class TestPressureConverterMore10000m(TestTools):
  def runTest(self):
    try:
      altitude_to_pressure(15000)
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

class TestPressureToDeph(TestTools):
  def setUp(self):
    TestTools.setUp(self)

  def test_depth_to_pressure_100(self):
    self.assertAlmostEqual(pressure_to_depth(10.1043), 100, 5, "Wrong depth pressure at 100m : %s" % depth_to_pressure(10.1043))

  def test_depth_to_pressure_90(self):
    self.assertAlmostEqual(pressure_to_depth(9.09387), 90, 5, "Wrong depth pressure at 90m : %s" % depth_to_pressure(9.09387))

  def test_depth_to_pressure_80(self):
    self.assertAlmostEqual(pressure_to_depth(8.08344), 80, 5, "Wrong depth pressure at 80m : %s" % depth_to_pressure(8.08344))

  def test_depth_to_pressure_70(self):
    self.assertAlmostEqual(pressure_to_depth(7.07301), 70, 5, "Wrong depth pressure at 70m : %s" % depth_to_pressure(7.07301))

  def test_depth_to_pressure_60(self):
    self.assertAlmostEqual(pressure_to_depth(6.06258), 60, 5, "Wrong depth pressure at 60m : %s" % depth_to_pressure(6.06258))

  def test_depth_to_pressure_50(self):
    self.assertAlmostEqual(pressure_to_depth(5.05215), 50, 5, "Wrong depth pressure at 50m : %s" % depth_to_pressure(5.05215))

  def test_depth_to_pressure_40(self):
    self.assertAlmostEqual(pressure_to_depth(4.04172), 40, 5, "Wrong depth pressure at 40m : %s" % depth_to_pressure(4.04172))

  def test_depth_to_pressure_30(self):
    self.assertAlmostEqual(pressure_to_depth(3.03129), 30, 5, "Wrong depth pressure at 30m : %s" % depth_to_pressure(3.03129))

  def test_depth_to_pressure_20(self):
    self.assertAlmostEqual(pressure_to_depth(2.02086), 20, 5, "Wrong depth pressure at 20m : %s" % depth_to_pressure(2.02086))

  def test_depth_to_pressure_10(self):
    self.assertAlmostEqual(pressure_to_depth(1.01043), 10, 5, "Wrong depth pressure at 10m : %s" % depth_to_pressure(1.01043))

  def test_depth_to_pressure_0(self):
    self.assertAlmostEqual(pressure_to_depth(0.0), 0, 0, "Wrong depth pressure at 0m : %s" % depth_to_pressure(0.0))


class TestCalculate_ppH2O_surf(TestTools):
  def setUp(self):
    TestTools.setUp(self)

  def test_calculate_ppH2O_surf_moins10(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(-10.0), 0.00651325686767, 7, "Wrong ppH2O surf at -10° : %s" % calculate_ppH2O_surf(-10))

  def test_calculate_ppH2O_surf_0(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(0.0), 0.00651325686767, 7, "Wrong ppH2O surf at 0° : %s" % calculate_ppH2O_surf(0))

  def test_calculate_ppH2O_surf_1(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(1), 0.00651325686767, 7, "Wrong ppH2O surf at 1° : %s" % calculate_ppH2O_surf(1))

  def test_calculate_ppH2O_surf_5(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(5), 0.00866264906268, 7, "Wrong ppH2O surf at 5° : %s" % calculate_ppH2O_surf(5))

  def test_calculate_ppH2O_surf_10(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(10), 0.0122107541129, 7, "Wrong ppH2O surf at 10° : %s" % calculate_ppH2O_surf(10))

  def test_calculate_ppH2O_surf_15(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(15), 0.0169758994956, 7, "Wrong ppH2O surf at 15° : %s" % calculate_ppH2O_surf(15))

  def test_calculate_ppH2O_surf_20(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(20), 0.0232957591939, 7, "Wrong ppH2O surf at 20° : %s" % calculate_ppH2O_surf(20))

  def test_calculate_ppH2O_surf_25(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(25), 0.0315792952353, 7, "Wrong ppH2O surf at 25° : %s" % calculate_ppH2O_surf(25))

  def test_calculate_ppH2O_surf_30(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(30), 0.0423167530545, 7, "Wrong ppH2O surf at 30° : %s" % calculate_ppH2O_surf(30))

  def test_calculate_ppH2O_surf_35(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(35), 0.0560901835181, 7, "Wrong ppH2O surf at 35° : %s" % calculate_ppH2O_surf(35))

  def test_calculate_ppH2O_surf_40(self):
    self.assertAlmostEqual(calculate_ppH2O_surf(40), 0.0735844054898, 7, "Wrong ppH2O surf at 40° : %s" % calculate_ppH2O_surf(40))

  def test_calculate_ppH2O_surf_500(self):
    try:
      calculate_ppH2O_surf(500)
    except ValueError:
      pass
    else:
      self.fail("Should raise ValueError")

class TestConversionsImperialSi(TestTools):
  def setUp(self):
    TestTools.setUp(self)

  def test_convert_bar_to_psi_1(self):
    self.assertAlmostEqual(convert_bar_to_psi(1), 14.5037744, 7, "Wrong conversion:%s" % convert_bar_to_psi(1))

  def test_convert_bar_to_psi_35(self):
    self.assertAlmostEqual(convert_bar_to_psi(35), 507.632104, 7, "Wrong conversion:%s" % convert_bar_to_psi(35))

  def test_convert_bar_to_psi_100(self):
    self.assertAlmostEqual(convert_bar_to_psi(100), 1450.37744, 7, "Wrong conversion:%s" % convert_bar_to_psi(100))

  def test_convert_bar_to_psi_230(self):
    self.assertAlmostEqual(convert_bar_to_psi(230), 3335.868112, 7, "Wrong conversion:%s" % convert_bar_to_psi(230))

  def test_convert_bar_to_psi_300(self):
    self.assertAlmostEqual(convert_bar_to_psi(300), 4351.13232, 7, "Wrong conversion:%s" % convert_bar_to_psi(300))

  def test_convert_psi_to_bar_1(self):
    self.assertAlmostEqual(convert_psi_to_bar(14.5037744), 1, 7, "Wrong conversion:%s" % convert_psi_to_bar(14.5037744))

  def test_convert_psi_to_bar_35(self):
    self.assertAlmostEqual(convert_psi_to_bar(507.632104), 35, 7, "Wrong conversion:%s" % convert_psi_to_bar(507.632104))

  def test_convert_psi_to_bar_100(self):
    self.assertAlmostEqual(convert_psi_to_bar(1450.37744), 100, 7, "Wrong conversion:%s" % convert_psi_to_bar(1450.37744))

  def test_convert_psi_to_bar_230(self):
    self.assertAlmostEqual(convert_psi_to_bar(3335.868112), 230, 7, "Wrong conversion:%s" % convert_psi_to_bar(3335.868112))

  def test_convert_psi_to_bar_300(self):
    self.assertAlmostEqual(convert_psi_to_bar(4351.13232), 300, 7, "Wrong conversion:%s" % convert_psi_to_bar(4351.13232))

  def test_convert_liter_to_cubicfeet_1(self):
    self.assertAlmostEqual(convert_liter_to_cubicfeet(1), 0.0353146667215, 7, "Wrong conversion:%s" % convert_liter_to_cubicfeet(1))

  def test_convert_liter_to_cubicfeet_6(self):
    self.assertAlmostEqual(convert_liter_to_cubicfeet(6), 0.211888000329, 7, "Wrong conversion:%s" % convert_liter_to_cubicfeet(6))

  def test_convert_liter_to_cubicfeet_12(self):
    self.assertAlmostEqual(convert_liter_to_cubicfeet(12), 0.423776000658, 7, "Wrong conversion:%s" % convert_liter_to_cubicfeet(12))

  def test_convert_liter_to_cubicfeet_15(self):
    self.assertAlmostEqual(convert_liter_to_cubicfeet(15), 0.529720000822, 7, "Wrong conversion:%s" % convert_liter_to_cubicfeet(15))

  def test_convert_liter_to_cubicfeet_18(self):
    self.assertAlmostEqual(convert_liter_to_cubicfeet(18), 0.635664000987, 7, "Wrong conversion:%s" % convert_liter_to_cubicfeet(18))

  def test_convert_cubicfeet_to_liter_1(self):
    self.assertAlmostEqual(convert_cubicfeet_to_liter(0.0353146667215), 1, 7, "Wrong conversion:%s" %  convert_cubicfeet_to_liter(0.0353146667215))

  def test_convert_cubicfeet_to_liter_6(self):
    self.assertAlmostEqual(convert_cubicfeet_to_liter(0.211888000329), 6, 7, "Wrong conversion:%s" %  convert_cubicfeet_to_liter(0.211888000329))

  def test_convert_cubicfeet_to_liter_12(self):
    self.assertAlmostEqual(convert_cubicfeet_to_liter(0.423776000658), 12, 7, "Wrong conversion:%s" %  convert_cubicfeet_to_liter(0.423776000658))

  def test_convert_cubicfeet_to_liter_15(self):
    self.assertAlmostEqual(convert_cubicfeet_to_liter(0.529720000822), 15, 7, "Wrong conversion:%s" %  convert_cubicfeet_to_liter(0.529720000822))

  def test_convert_cubicfeet_to_liter_18(self):
    self.assertAlmostEqual(convert_cubicfeet_to_liter(0.635664000987), 18, 7, "Wrong conversion:%s" %  convert_cubicfeet_to_liter(0.635664000987))

  def test_convert_meter_to_feet_1(self):
    self.assertAlmostEqual(convert_meter_to_feet(1), 3.28083989501, 7, "Wrong conversion:%s" % convert_meter_to_feet(1))

  def test_convert_meter_to_feet_15(self):
    self.assertAlmostEqual(convert_meter_to_feet(15), 49.2125984252, 7, "Wrong conversion:%s" % convert_meter_to_feet(15))

  def test_convert_meter_to_feet_30(self):
    self.assertAlmostEqual(convert_meter_to_feet(30), 98.4251968504, 7, "Wrong conversion:%s" % convert_meter_to_feet(30))

  def test_convert_meter_to_feet_50(self):
    self.assertAlmostEqual(convert_meter_to_feet(50), 164.041994751, 7, "Wrong conversion:%s" % convert_meter_to_feet(50))

  def test_convert_meter_to_feet_70(self):
    self.assertAlmostEqual(convert_meter_to_feet(70), 229.658792651, 7, "Wrong conversion:%s" % convert_meter_to_feet(70))

  def test_convert_feet_to_meter_1(self):
    self.assertAlmostEqual(convert_feet_to_meter(3.28083989501), 1, 7, "Wrong conversion:%s" % convert_feet_to_meter(3.28083989501))

  def test_convert_feet_to_meter_15(self):
    self.assertAlmostEqual(convert_feet_to_meter(49.2125984252), 15, 7, "Wrong conversion:%s" % convert_feet_to_meter(49.2125984252))

  def test_convert_feet_to_meter_30(self):
    self.assertAlmostEqual(convert_feet_to_meter(98.4251968504), 30, 7, "Wrong conversion:%s" % convert_feet_to_meter(98.4251968504))

  def test_convert_feet_to_meter_50(self):
    self.assertAlmostEqual(convert_feet_to_meter(164.041994751), 50, 7, "Wrong conversion:%s" % convert_feet_to_meter(164.041994751))

  def test_convert_feet_to_meter_70(self):
    self.assertAlmostEqual(convert_feet_to_meter(229.658792651), 70, 7, "Wrong conversion:%s" % convert_feet_to_meter(229.658792651))


    #from tools import convert_feet_to_meter
  #from tools import convert_meter_to_feet


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
