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
"""Test for Segment class."""
import unittest
# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive, SegmentDeco, SegmentAscDesc
from dipplanner.segment import UnauthorizedMod
from dipplanner import settings


class TestSegment(unittest.TestCase):
    """Test Segment base class."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        # temporary hack (tests):
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        settings.DIVE_CONSUMPTION_RATE = 17.0 / 60  #: liter/s
        settings.DECO_CONSUMPTION_RATE = 12.0 / 60  #: liter/s
        self.airtank = Tank()
        self.trimixtank1 = Tank(f_o2=0.10, f_he=0.70)
        self.nitroxtank1 = Tank(f_o2=0.40)
        self.oxygentank1 = Tank(f_o2=1)
        self.diveseg1 = SegmentDive(30, 10 * 60, self.airtank, 0)
        self.diveseg2 = SegmentDive(150, 10 * 60, self.trimixtank1, 0)
        self.decoseg1 = SegmentDeco(12, 5 * 60, self.nitroxtank1, 0)
        self.decoseg2 = SegmentDeco(3, 15 * 60, self.oxygentank1, 0)
        self.ascseg1 = SegmentAscDesc(150, 50, 20.0 / 60, self.trimixtank1, 0)
        self.ascseg2 = SegmentAscDesc(30, 12, 10.0 / 60, self.nitroxtank1, 0)
        self.descseg1 = SegmentAscDesc(0, 40, 20.0 / 60, self.airtank, 0)
        self.descseg2 = SegmentAscDesc(40, 150, 20.0 / 60, self.trimixtank1, 0)

    def tearDown(self):
        """Restore some settings."""
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 20
        settings.DIVE_CONSUMPTION_RATE = 20.0 / 60  #: liter/s
        settings.DECO_CONSUMPTION_RATE = 17.0 / 60  #: liter/s

    def test_gas_used_1(self):
        """test_gas_used 1."""
        self.assertAlmostEqual(self.diveseg1.gas_used, 687.5718, 4,
                               'Wrong gas used : %s'
                               % self.diveseg1.gas_used)

    def test_gas_end_1(self):
        """test_gas_end 1."""
        self.assertAlmostEqual(self.diveseg1.end,
                               29.0057341025, 5,
                               'wrong E.N.D : %s' % self.diveseg1.end)

    def test_gas_end_2(self):
        """test_gas_end 2."""
        self.assertAlmostEqual(self.diveseg2.end,
                               61.912489531, 5,
                               'wrong E.N.D : %s' % self.diveseg2.end)

    def test_str_1(self):
        """test_str 1."""
        self.assertEqual(
            str(self.diveseg2),
            "   CONST: at 150m for  10:00 [RT:  0:00], on Trimix 10/70,  "
            "SP:0.0, END:61m",
            'wrong name : %s' % str(self.diveseg2))

    def test_deco_1(self):
        """test deco seg gas used 1."""
        self.assertAlmostEqual(self.decoseg1.gas_used,
                               133.54596, 5,
                               'Wrong gas used : %s'
                               % self.decoseg1.gas_used)

    def test_deco_2(self):
        """test deco seg gas used 2."""
        self.assertAlmostEqual(self.decoseg2.gas_used,
                               236.94822, 5, 'Wrong gas used : %s'
                               % self.decoseg2.gas_used)

    def test_asc_1(self):
        """test asc seg gas used 2."""
        self.assertAlmostEqual(self.ascseg1.gas_used,
                               944.99175, 5, 'Wrong gas used : %s'
                               % self.ascseg1.gas_used)

    def test_asc_2(self):
        """test asc seg gas used 2."""
        self.assertAlmostEqual(self.ascseg2.gas_used,
                               95.9356818, 7, 'Wrong gas used : %s'
                               % self.ascseg2.gas_used)

    def test_desc_1(self):
        """test desc seg gas used 2."""
        self.assertAlmostEqual(self.descseg1.gas_used,
                               103.15974, 5, 'Wrong gas used : %s'
                               % self.descseg1.gas_used)

    def test_desc_2(self):
        """test desc seg gas used 2."""
        self.assertAlmostEqual(self.descseg2.gas_used,
                               992.2533225, 7,
                               'Wrong gas used : %s'
                               % self.descseg2.gas_used)

    def test_wrong_mod_1(self):
        """test wrong mod 1."""
        try:
            baddiveseg = SegmentDive(150, 10 * 60, self.airtank, 0)
            baddiveseg.check()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")

    def test_wrong_mod_2(self):
        """test wrong mod 2."""
        try:
            baddiveseg = SegmentDeco(3, 10 * 60, self.trimixtank1, 0)
            baddiveseg.check()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")

    def test_wrong_mod_3(self):
        """test wrong mod 3."""
        try:
            baddiveseg = SegmentAscDesc(150, 3, 10, self.nitroxtank1, 0)
            baddiveseg.check()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")

    def test_wrong_mod_4(self):
        """test wrong mod 4."""
        try:
            baddiveseg = SegmentAscDesc(3, 150, 10, self.trimixtank1, 0)
            baddiveseg.check()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")
