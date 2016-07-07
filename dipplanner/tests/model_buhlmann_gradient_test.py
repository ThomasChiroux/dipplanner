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
"""Test for buhlmann model gradient class."""
import unittest
# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.model.buhlmann.gradient import Gradient
from dipplanner import settings


class TestModelBuhlmannGradient(unittest.TestCase):
    """Base class for Buhlmann gradint tests."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        # temporary hack (tests):
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        self.gradient1 = Gradient(0.3, 0.8)
        self.gradient2 = Gradient(0.35, 0.75)


class TestModelBuhlmannGradientSimple1(TestModelBuhlmannGradient):
    """Test Gradients."""

    def test_1(self):
        """test gradients 1."""
        self.assertEqual(self.gradient1.gf_low, 0.3,
                         "wrong gw_low : %s" % self.gradient1.gf_low)

    def test_2(self):
        """test gradients 2."""
        self.assertEqual(self.gradient1.gf_high, 0.8,
                         "wrong gw_high : %s" % self.gradient1.gf_high)

    def test_3(self):
        """test gradients 3."""
        self.assertEqual(self.gradient1.gf_slope, 1.0,
                         "wrong gw_slope : %s" % self.gradient1.gf_slope)

    def test_4(self):
        """test gradients 4."""
        self.assertEqual(self.gradient1.gf, 0.3,
                         "wrong gw_low : %s" % self.gradient1.gf)

    def test_5(self):
        """test gradients 5."""
        self.gradient2.set_gf_slope_at_depth(12)
        self.assertEqual(round(self.gradient2.gf_slope, 13), -0.0333333333333,
                         "wrong gw_slope : %s" % self.gradient2.gf_slope)

    def test_6(self):
        """test gradients 6."""
        self.gradient2.set_gf_slope_at_depth(6)
        self.gradient2.set_gf_at_depth(6)
        self.assertEqual(self.gradient2.gf, 0.35,
                         "wrong gw_low : %s" % self.gradient2.gf)
