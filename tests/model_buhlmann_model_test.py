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
Test for Model class
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
import settings
from model.buhlmann.model import Model
from model.buhlmann.model_exceptions import ModelStateException
import dipplanner
import settings

class TestModelBuhlmannModel(unittest.TestCase):
    def setUp(self):
        # temporary hack (tests):
        dipplanner.activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        # simples test
        self.model1 = Model()

        # OC tests
        self.model2 = Model()
        self.model2.const_depth(30, 12*60, 0.0, 0.79, 0.0)

class TestModelBuhlmannModelSimple1(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.units == "metric", "Error in model unit : %s" % self.model1.units

class TestModelBuhlmannModelSimple2(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.gradient.gf_low == settings.GF_LOW, "Error in model gradient gf low : %s" % self.model1.gradient.gf_low

class TestModelBuhlmannModelSimple3(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.gradient.gf_high == settings.GF_HIGH, "Error in model gradient gf high : %s" % self.model1.gradient.gf_high

class TestModelBuhlmannModelSimple3b(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.gradient.gf == settings.GF_LOW, "Error in model gradient gf : %s" % self.model1.gradient.gf

class TestModelBuhlmannModelSimple4(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.metadata == "(none)", "Error in model metadata : %s" % self.model1.metadata

class TestModelBuhlmannModelSimple5(TestModelBuhlmannModel):
    def runTest(self):
        assert len(self.model1.tissues) == 16, "Error in tissues number : %s" % len(self.model1.tissues)

class TestModelBuhlmannModelSimple6(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.ox_tox.otu == 0.0, "Error in model ox tox otu : %s" % self.model1.ox_tox_otu

class TestModelBuhlmannModelSimple7(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.validate_model() == self.model1.MODEL_VALIDATION_SUCCESS, "Error in model validation : %s" % self.model1.validate_model()

class TestModelBuhlmannModelSimple8(TestModelBuhlmannModel):
    def runTest(self):
        # empty model should have the first compartement for control compartment ??
        assert self.model1.control_compartment() == 1, "Error in control compartement : %s" % self.model1.control_compartment()

class TestModelBuhlmannModelSimple9(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model1.ceiling() == 0.0, "Error in model ceiling : %s" % self.model1.ceiling()

class TestModelBuhlmannModelSimple10(TestModelBuhlmannModel):
    def runTest(self):
        mv = self.model1.m_value(12)
        self.assertAlmostEqual(mv,0.0575659327931, 13, "Error in model m_value : %s" % mv)

class TestModelBuhlmannModelOutput1(TestModelBuhlmannModel):
    def runTest(self):
        assert str(self.model1) == """C:0 He:0.0 N2:0.789444359701 gf:0.3 mv_at:2.98611129437 max_amb:0.354301769605 MV:0.264372048419
C:1 He:0.0 N2:0.789444359701 gf:0.3 mv_at:2.55549585508 max_amb:0.421736098719 MV:0.30892022702
C:2 He:0.0 N2:0.789444359701 gf:0.3 mv_at:2.26480470784 max_amb:0.4759777647 MV:0.348570610512
C:3 He:0.0 N2:0.789444359701 gf:0.3 mv_at:2.05108817891 max_amb:0.519283115855 MV:0.384890502425
C:4 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.91362345557 max_amb:0.551292972875 MV:0.412539027676
C:5 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.76138724212 max_amb:0.588654476709 MV:0.44819466204
C:6 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.66029300587 max_amb:0.613368228075 MV:0.475484963745
C:7 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.58720538721 max_amb:0.631276306694 MV:0.49738009086
C:8 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.53314126705 max_amb:0.644524155141 MV:0.514919516335
C:9 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.47853129473 max_amb:0.65883000245 MV:0.533938214575
C:10 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.43699477412 max_amb:0.669849285232 MV:0.549371768026
C:11 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.39988162289 max_amb:0.679806017916 MV:0.563936512055
C:12 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.35416745806 max_amb:0.692479753463 MV:0.582973955698
C:13 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.33536177703 max_amb:0.697338972914 MV:0.59118388236
C:14 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.30754890648 max_amb:0.704987899053 MV:0.603758953711
C:15 He:0.0 N2:0.789444359701 gf:0.3 mv_at:1.28237367658 max_amb:0.711956470078 MV:0.615611794066
""", "Error in model output : %s" % str(self.model1)

class TestModelBuhlmannModelGf1(TestModelBuhlmannModel):
    def runTest(self):
        assert self.model2.gradient.gf == settings.GF_LOW, "Error in model gf : %s" % self.model2.gradient.gf

class TestModelBuhlmannModelOutput2(TestModelBuhlmannModel):
    def runTest(self):
        assert str(self.model2) == """C:0 He:0.0 N2:19.9991340314 gf:0.3 mv_at:2.98611129437 max_amb:15.8731803417 MV:6.6973840088
C:1 He:0.0 N2:16.1102290026 gf:0.3 mv_at:2.55549585508 max_amb:13.6230894631 MV:6.3041499248
C:2 He:0.0 N2:12.3062955138 gf:0.3 mv_at:2.26480470784 max_amb:10.8013122031 MV:5.43371155634
C:3 He:0.0 N2:9.37174702982 gf:0.3 mv_at:2.05108817891 max_amb:8.44101928733 MV:4.56915852091
C:4 He:0.0 N2:7.07309062624 gf:0.3 mv_at:1.91362345557 max_amb:6.42833419682 MV:3.69617680303
C:5 He:0.0 N2:5.41592414804 gf:0.3 mv_at:1.76138724212 max_amb:4.97102273912 MV:3.07480604977
C:6 He:0.0 N2:4.15546491885 gf:0.3 mv_at:1.66029300587 max_amb:3.83411612526 MV:2.50285034278
C:7 He:0.0 N2:3.21615828015 gf:0.3 mv_at:1.58720538721 max_amb:2.97208187465 MV:2.02630252271
C:8 He:0.0 N2:2.53070372621 gf:0.3 mv_at:1.53314126705 max_amb:2.33513221976 MV:1.65066571529
C:9 He:0.0 N2:2.10191571236 gf:0.3 mv_at:1.47853129473 max_amb:1.93890390881 MV:1.42162409403
C:10 He:0.0 N2:1.82052001107 gf:0.3 mv_at:1.43699477412 max_amb:1.67880563388 MV:1.26689396779
C:11 He:0.0 N2:1.60007278966 gf:0.3 mv_at:1.39988162289 max_amb:1.47528290992 MV:1.14300578242
C:12 He:0.0 N2:1.42704210161 gf:0.3 mv_at:1.35416745806 max_amb:1.31969342603 MV:1.05381508995
C:13 He:0.0 N2:1.28955655665 gf:0.3 mv_at:1.33536177703 max_amb:1.19038405262 MV:0.965698269057
C:14 He:0.0 N2:1.18200241273 gf:0.3 mv_at:1.30754890648 max_amb:1.0927244828 MV:0.903983328561
C:15 He:0.0 N2:1.09786259985 gf:0.3 mv_at:1.28237367658 max_amb:1.01708414861 MV:0.856117541951
""", "Error in model output : %s" % str(self.model2)

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
