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
"""Test for compartment class."""
import unittest
# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.model.buhlmann.compartment import Compartment
from dipplanner import settings


class TestModelBuhlmannCompartemnt(unittest.TestCase):
    """Test compartements of the buhlmann model."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        # temporary hack (tests):
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        self.compt1 = Compartment(1.88, 5.0,
                                  16.189, 0.4770,
                                  11.696, 0.5578)
        self.compt2 = Compartment(1.88, 5.0,
                                  16.189, 0.4770,
                                  11.696, 0.5578)
        self.compt2.set_pp(0.3 * 5, (1 - 0.21 - 0.3) * 5)
        self.compt3 = Compartment(1.88, 5.0,
                                  16.189, 0.4770,
                                  11.696, 0.5578)
        self.compt3.set_pp(0.0, 3.16)

    def test_compartment_simple_1(self):
        """test_compartment_simple_1."""
        self.assertEqual(self.compt1.pp_he, 0,
                         "wrong pp_he : %s" % self.compt1.pp_he)

    def test_compartment_simple_2(self):
        """test_compartment_simple_2."""
        self.assertEqual(self.compt1.pp_n2, 0,
                         "wrong pp_n2 : %s" % self.compt1.pp_n2)

    def test_compartment_simple_3(self):
        """test_compartment_simple_3."""
        self.assertEqual(round(self.compt1.k_he, 14), 0.00614492181347,
                         "wrong k_he : %s" % self.compt1.k_he)

    def test_compartment_simple_4(self):
        """test_compartment_simple_4."""
        self.assertEqual(round(self.compt1.k_n2, 14), 0.00231049060187,
                         "wrong k_n2 : %s" % self.compt1.k_n2)

    def test_compartment_simple_5(self):
        """test_compartment_simple_5."""
        self.assertEqual(self.compt1.a_he, 1.6189,
                         "wrong a_he : %s" % self.compt1.a_he)

    def test_compartment_simple_6(self):
        """test_compartment_simple_6."""
        self.assertEqual(self.compt1.b_he, 0.4770,
                         "wrong b_he : %s" % self.compt1.b_he)

    def test_compartment_simple_7(self):
        """test_compartment_simple_7."""
        self.assertEqual(self.compt1.a_n2, 1.1696,
                         "wrong a_n2 : %s" % self.compt1.a_n2)

    def test_compartment_simple_8(self):
        """test_compartment_simple_8."""
        self.assertEqual(self.compt1.b_n2, 0.5578,
                         "wrong b_n2 : %s" % self.compt1.b_n2)

    def test_compartment_simple_9(self):
        """test_compartment_simple_9."""
        self.assertEqual(self.compt2.pp_he, 1.5,
                         "wrong pp_he : %s" % self.compt2.pp_he)

    def test_compartment_simple_10(self):
        """test_compartment_simple_10."""
        self.assertEqual(self.compt2.pp_n2, 2.45,
                         "wrong pp_n2 : %s" % self.compt2.pp_n2)

    def test_compartment_simple_11(self):
        """test_compartment_simple_11."""
        self.compt2.const_depth(0.3 * 4.5, (1 - 0.21 - 0.3) * 4.5, 12 * 60)
        self.assertEqual(round(self.compt2.pp_he, 11), 1.35179731087,
                         "wrong pp_he : %s" % self.compt2.pp_he)

    def test_compartment_simple_12(self):
        """test_compartment_simple_12."""
        self.compt2.const_depth(0.3 * 4.5, (1 - 0.21 - 0.3) * 4.5, 12 * 60)
        self.assertEqual(round(self.compt2.pp_n2, 11), 2.25141881985,
                         "wrong pp_n2 : %s" % self.compt2.pp_n2)

    def test_compartment_simple_13(self):
        """test_compartment_simple_13."""
        self.compt2.asc_desc(0.2997, 0.48951, 0.1, 0.163333333333, 9.0)
        self.assertEqual(round(self.compt2.pp_he, 11), 1.45985489718,
                         "wrong pp_he : %s" % self.compt2.pp_he)

    def test_compartment_simple_14(self):
        """test_compartment_simple_14."""
        self.compt2.asc_desc(0.2997, 0.48951, 0.1, 0.163333333333, 9.0)
        self.assertEqual(round(self.compt2.pp_n2, 11), 2.42483220311,
                         "wrong pp_n2 : %s" % self.compt2.pp_n2)

    def test_compartment_mvalue_1(self):
        """test_compartment_mvalue_1."""
        mv = self.compt3.get_m_value_at(0.0)
        self.assertEqual(mv, 1.1696, "wrong M-Value : %s" % mv)

    def test_compartment_mvalue_2(self):
        """test_compartment_mvalue_2."""
        mv = self.compt3.get_m_value_at(1.0)
        self.assertEqual(round(mv, 11), 2.96235726067,
                         "wrong M-Value : %s" % mv)

    def test_compartment_mvalue_3(self):
        """test_compartment_mvalue_3."""
        mv = self.compt3.get_m_value_at(3.0)
        self.assertEqual(round(mv, 9), 6.547871782,
                         "wrong M-Value : %s" % mv)

    def test_compartment_maxamb_1(self):
        """test_compartment_maxamb 1."""
        max_amb = self.compt3.get_max_amb(0.8)
        self.assertEqual(round(max_amb, 11), 1.36110151389,
                         "wrong max_amb for given gf : %s" % max_amb)

    def test_compartment_mv_1(self):
        """test_compartment_mv 1."""
        mv = self.compt3.get_mv(1.0)
        self.assertEqual(round(mv, 11), 1.06671806333,
                         "wrong mv for given amb pressure : %s" % mv)
