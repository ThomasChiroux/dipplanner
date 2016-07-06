#
# Copyright 2011-2016 Thomas Chiroux
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
"""Test for Model class."""
import unittest
# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner import settings
from dipplanner.model.buhlmann.model import Model
from dipplanner.model.buhlmann.model_exceptions import ModelStateException


class TestModelBuhlmannModel(unittest.TestCase):
    def setUp(self):
        # temporary hack (tests):
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        # simples test
        self.model1 = Model()

        # OC tests
        self.model2 = Model()
        self.model2.const_depth(30, 12 * 60, 0.0, 0.79, 0.0)


class TestModelBuhlmannModelSimple1(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model1.units, "metric",
                         "Error in model unit : %s" % self.model1.units)


class TestModelBuhlmannModelSimple2(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model1.gradient.gf_low, settings.GF_LOW,
                         "Error in model gradient gf low : %s"
                         % self.model1.gradient.gf_low)


class TestModelBuhlmannModelSimple3(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model1.gradient.gf_high, settings.GF_HIGH,
                         "Error in model gradient gf high : %s"
                         % self.model1.gradient.gf_high)


class TestModelBuhlmannModelSimple3b(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model1.gradient.gf, settings.GF_LOW,
                         "Error in model gradient gf : %s"
                         % self.model1.gradient.gf)


class TestModelBuhlmannModelSimple4(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model1.metadata, "(none)",
                         "Error in model metadata : %s"
                         % self.model1.metadata)


class TestModelBuhlmannModelSimple5(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(len(self.model1.tissues), 16,
                         "Error in tissues number : %s"
                         % len(self.model1.tissues))


class TestModelBuhlmannModelSimple6(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model1.ox_tox.otu, 0.0,
                         "Error in model ox tox otu : %s"
                         % self.model1.ox_tox.otu)


class TestModelBuhlmannModelSimple7(TestModelBuhlmannModel):
    def runTest(self):
        self.assertTrue(
            self.model1.validate_model(),
            "Error in model validation : %s" % self.model1.validate_model())


class TestModelBuhlmannModelSimple8(TestModelBuhlmannModel):
    def runTest(self):
        # empty model should have the first compartement
        # for control compartment ??
        self.assertEqual(self.model1.control_compartment(), 1,
                         "Error in control compartement : %s"
                         % self.model1.control_compartment())


class TestModelBuhlmannModelSimple9(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model1.ceiling(), 0.0,
                         "Error in model ceiling : %s"
                         % self.model1.ceiling())


class TestModelBuhlmannModelSimple10(TestModelBuhlmannModel):
    def runTest(self):
        mv = self.model1.m_value(12)
        self.assertAlmostEqual(mv, 0.0575659327931, 13,
                               "Error in model m_value : %s" % mv)


class TestModelBuhlmannModelOutput1(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(str(self.model1),
                         """C:0 He:0.000000 N2:0.789444 gf:0.30 mv_at:2.986111 max_amb:0.354302 MV:0.264372
C:1 He:0.000000 N2:0.789444 gf:0.30 mv_at:2.555496 max_amb:0.421736 MV:0.308920
C:2 He:0.000000 N2:0.789444 gf:0.30 mv_at:2.264805 max_amb:0.475978 MV:0.348571
C:3 He:0.000000 N2:0.789444 gf:0.30 mv_at:2.051088 max_amb:0.519283 MV:0.384891
C:4 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.913623 max_amb:0.551293 MV:0.412539
C:5 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.761387 max_amb:0.588654 MV:0.448195
C:6 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.660293 max_amb:0.613368 MV:0.475485
C:7 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.587205 max_amb:0.631276 MV:0.497380
C:8 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.533141 max_amb:0.644524 MV:0.514920
C:9 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.478531 max_amb:0.658830 MV:0.533938
C:10 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.436995 max_amb:0.669849 MV:0.549372
C:11 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.399882 max_amb:0.679806 MV:0.563937
C:12 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.354167 max_amb:0.692480 MV:0.582974
C:13 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.335362 max_amb:0.697339 MV:0.591184
C:14 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.307549 max_amb:0.704988 MV:0.603759
C:15 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.282374 max_amb:0.711956 MV:0.615612
""", "Error in model output : %s" % str(self.model1))


class TestModelBuhlmannModelGf1(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(self.model2.gradient.gf, settings.GF_LOW,
                         "Error in model gf : %s" % self.model2.gradient.gf)


class TestModelBuhlmannModelOutput2(TestModelBuhlmannModel):
    def runTest(self):
        self.assertEqual(str(self.model2),
                         """C:0 He:0.000000 N2:19.999134 gf:0.30 mv_at:2.986111 max_amb:15.873180 MV:6.697384
C:1 He:0.000000 N2:16.110229 gf:0.30 mv_at:2.555496 max_amb:13.623089 MV:6.304150
C:2 He:0.000000 N2:12.306296 gf:0.30 mv_at:2.264805 max_amb:10.801312 MV:5.433712
C:3 He:0.000000 N2:9.371747 gf:0.30 mv_at:2.051088 max_amb:8.441019 MV:4.569159
C:4 He:0.000000 N2:7.073091 gf:0.30 mv_at:1.913623 max_amb:6.428334 MV:3.696177
C:5 He:0.000000 N2:5.415924 gf:0.30 mv_at:1.761387 max_amb:4.971023 MV:3.074806
C:6 He:0.000000 N2:4.155465 gf:0.30 mv_at:1.660293 max_amb:3.834116 MV:2.502850
C:7 He:0.000000 N2:3.216158 gf:0.30 mv_at:1.587205 max_amb:2.972082 MV:2.026303
C:8 He:0.000000 N2:2.530704 gf:0.30 mv_at:1.533141 max_amb:2.335132 MV:1.650666
C:9 He:0.000000 N2:2.101916 gf:0.30 mv_at:1.478531 max_amb:1.938904 MV:1.421624
C:10 He:0.000000 N2:1.820520 gf:0.30 mv_at:1.436995 max_amb:1.678806 MV:1.266894
C:11 He:0.000000 N2:1.600073 gf:0.30 mv_at:1.399882 max_amb:1.475283 MV:1.143006
C:12 He:0.000000 N2:1.427042 gf:0.30 mv_at:1.354167 max_amb:1.319693 MV:1.053815
C:13 He:0.000000 N2:1.289557 gf:0.30 mv_at:1.335362 max_amb:1.190384 MV:0.965698
C:14 He:0.000000 N2:1.182002 gf:0.30 mv_at:1.307549 max_amb:1.092724 MV:0.903983
C:15 He:0.000000 N2:1.097863 gf:0.30 mv_at:1.282374 max_amb:1.017084 MV:0.856118
""", "Error in model output : %s" % str(self.model2))


def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('tests', metavar='TestName', type=str, nargs='*',
                        help='name of the tests to run '
                             '(separated by space) [optionnal]')
    args = parser.parse_args()
    if args.tests:
        suite = unittest.TestLoader().loadTestsFromNames(args.tests,
                                                         sys.modules[__name__])
    else:
        suite = unittest.findTestCases(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
