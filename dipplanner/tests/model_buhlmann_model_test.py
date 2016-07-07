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
# pylint: disable=too-many-public-methods, protected-access, no-self-use
# pylint: disable=too-few-public-methods, duplicate-code, invalid-name
# pylint: disable=too-many-ancestors, attribute-defined-outside-init
"""Test for Model class."""
import unittest
# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner import settings
from dipplanner.model.buhlmann.model import Model
from dipplanner.model.buhlmann.model_exceptions import ModelStateException


class TestModelBuhlmannModel(unittest.TestCase):
    """Test the buhlmann model."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        # temporary hack (tests):
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        # simples test
        self.model1 = Model()

        # OC tests
        self.model2 = Model()
        self.model2.const_depth(30, 12 * 60, 0.0, 0.79, 0.0)

    def test_model_units(self):
        """check units."""
        self.assertEqual(self.model1.units, "metric",
                         "Error in model unit : %s" % self.model1.units)

    def test_model_gf_low(self):
        """check gf low."""
        self.assertEqual(self.model1.gradient.gf_low, settings.GF_LOW,
                         "Error in model gradient gf low : %s"
                         % self.model1.gradient.gf_low)

    def test_model_gf_high(self):
        """check gf high."""
        self.assertEqual(self.model1.gradient.gf_high, settings.GF_HIGH,
                         "Error in model gradient gf high : %s"
                         % self.model1.gradient.gf_high)

    def test_model_gf(self):
        """check gf."""
        self.assertEqual(self.model1.gradient.gf, settings.GF_LOW,
                         "Error in model gradient gf : %s"
                         % self.model1.gradient.gf)

    def test_metadata(self):
        """check metadata."""
        self.assertEqual(self.model1.metadata, "(none)",
                         "Error in model metadata : %s"
                         % self.model1.metadata)

    def test_model_tissues(self):
        """check tissues."""
        self.assertEqual(len(self.model1.tissues), 16,
                         "Error in tissues number : %s"
                         % len(self.model1.tissues))

    def test_model_otu(self):
        """check otu."""
        self.assertEqual(self.model1.ox_tox.otu, 0.0,
                         "Error in model ox tox otu : %s"
                         % self.model1.ox_tox.otu)

    def test_model_validation(self):
        """check validation."""
        self.assertTrue(
            self.model1.validate_model(),
            "Error in model validation : %s" % self.model1.validate_model())

    def test_model_control_compartment(self):
        """check control compartement."""
        # empty model should have the first compartement
        # for control compartment ??
        self.assertEqual(self.model1.control_compartment(), 1,
                         "Error in control compartement : %s"
                         % self.model1.control_compartment())

    def test_model_ceiling(self):
        """check ceiling."""
        self.assertEqual(self.model1.ceiling(), 0.0,
                         "Error in model ceiling : %s"
                         % self.model1.ceiling())

    def test_model_mv(self):
        """check m value."""
        mv = self.model1.m_value(12)
        self.assertAlmostEqual(mv, 0.0575659327931, 13,
                               "Error in model m_value : %s" % mv)

    def test_model_output1(self):
        """check str output of model 1."""
        self.assertEqual(str(self.model1),
                         """C:0 He:0.000000 N2:0.789444 gf:0.30 mv_at:3.266336 max_amb:0.317972 MV:0.241691
C:1 He:0.000000 N2:0.789444 gf:0.30 mv_at:2.555496 max_amb:0.421736 MV:0.308920
C:2 He:0.000000 N2:0.789444 gf:0.30 mv_at:2.264805 max_amb:0.475978 MV:0.348571
C:3 He:0.000000 N2:0.789444 gf:0.30 mv_at:2.051088 max_amb:0.519283 MV:0.384891
C:4 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.866923 max_amb:0.564396 MV:0.422858
C:5 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.705687 max_amb:0.604483 MV:0.462831
C:6 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.606593 max_amb:0.628783 MV:0.491378
C:7 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.537205 max_amb:0.645745 MV:0.513558
C:8 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.489441 max_amb:0.657253 MV:0.530027
C:9 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.448731 max_amb:0.667549 MV:0.544921
C:10 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.416795 max_amb:0.675779 MV:0.557204
C:11 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.384082 max_amb:0.684457 MV:0.570374
C:12 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.352667 max_amb:0.692922 MV:0.583620
C:13 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.322662 max_amb:0.701095 MV:0.596860
C:14 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.303249 max_amb:0.706262 MV:0.605751
C:15 He:0.000000 N2:0.789444 gf:0.30 mv_at:1.282374 max_amb:0.711956 MV:0.615612
""", "Error in model output : %s" % str(self.model1))

    def test_model_2_gf(self):
        """check gf of model 2."""
        self.assertEqual(self.model2.gradient.gf, settings.GF_LOW,
                         "Error in model gf : %s" % self.model2.gradient.gf)

    def test_model2_output_2(self):
        """check str output of model 1."""
        self.assertEqual(str(self.model2),
                         """C:0 He:0.000000 N2:21.526944 gf:0.30 mv_at:3.266336 max_amb:16.343125 MV:6.590549
C:1 He:0.000000 N2:16.110229 gf:0.30 mv_at:2.555496 max_amb:13.623089 MV:6.304150
C:2 He:0.000000 N2:12.306296 gf:0.30 mv_at:2.264805 max_amb:10.801312 MV:5.433712
C:3 He:0.000000 N2:9.371747 gf:0.30 mv_at:2.051088 max_amb:8.441019 MV:4.569159
C:4 He:0.000000 N2:7.073091 gf:0.30 mv_at:1.866923 max_amb:6.441438 MV:3.788635
C:5 He:0.000000 N2:5.415924 gf:0.30 mv_at:1.705687 max_amb:4.986851 MV:3.175215
C:6 He:0.000000 N2:4.155465 gf:0.30 mv_at:1.606593 max_amb:3.849531 MV:2.586508
C:7 He:0.000000 N2:3.216158 gf:0.30 mv_at:1.537205 max_amb:2.986551 MV:2.092211
C:8 He:0.000000 N2:2.530704 gf:0.30 mv_at:1.489441 max_amb:2.347861 MV:1.699096
C:9 He:0.000000 N2:2.101916 gf:0.30 mv_at:1.448731 max_amb:1.947623 MV:1.450867
C:10 He:0.000000 N2:1.820520 gf:0.30 mv_at:1.416795 max_amb:1.684736 MV:1.284957
C:11 He:0.000000 N2:1.600073 gf:0.30 mv_at:1.384082 max_amb:1.479934 MV:1.156054
C:12 He:0.000000 N2:1.427042 gf:0.30 mv_at:1.352667 max_amb:1.320136 MV:1.054984
C:13 He:0.000000 N2:1.289557 gf:0.30 mv_at:1.322662 max_amb:1.194140 MV:0.974971
C:14 He:0.000000 N2:1.182002 gf:0.30 mv_at:1.303249 max_amb:1.093999 MV:0.906966
C:15 He:0.000000 N2:1.097863 gf:0.30 mv_at:1.282374 max_amb:1.017084 MV:0.856118
""", "Error in model output : %s" % str(self.model2))
