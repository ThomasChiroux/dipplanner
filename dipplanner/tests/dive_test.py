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
"""Test for Dive class.

TODO: more test profiles
"""
import unittest

# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.dive import Dive
from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive
from dipplanner.tools import seconds_to_mmss
from dipplanner import settings

from dipplanner.tests.common import TestDive


class TestDiveNotEnoughGas1(TestDive):
    """Test a profile with not enough gas."""

    def runTest(self):
        """Not enought gas test"""
        diveseg1 = SegmentDive(60, 30 * 60, self.air12l, 0)
        self.profile1 = Dive([diveseg1], [self.air12l])
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

class TestDiveAirDiveOutput1(TestDive):
    """Test segments output for air dive 1."""

    expected_result = [
        " DESCENT: at  30m for   1:30 [RT:  1:30], on Air,  SP:0.0, END:29m",
        "   CONST: at  30m for  28:30 [RT: 30:00], on Air,  SP:0.0, END:29m",
        "  ASCENT: at  15m for   1:30 [RT: 31:30], on Air,  SP:0.0, END:14m",
        "    DECO: at  15m for   0:01 [RT: 31:31], on Air,  SP:0.0, END:14m",
        "  ASCENT: at  12m for   1:00 [RT: 32:31], on Air,  SP:0.0, END:11m",
        "    DECO: at  12m for   0:20 [RT: 32:51], on Air,  SP:0.0, END:11m",
        "  ASCENT: at   9m for   1:00 [RT: 33:51], on Air,  SP:0.0, END:8m",
        "    DECO: at   9m for   2:39 [RT: 36:30], on Air,  SP:0.0, END:8m",
        "  ASCENT: at   6m for   1:00 [RT: 37:30], on Air,  SP:0.0, END:5m",
        "    DECO: at   6m for   4:59 [RT: 42:29], on Air,  SP:0.0, END:5m",
        "  ASCENT: at   3m for   1:00 [RT: 43:29], on Air,  SP:0.0, END:2m",
        "    DECO: at   3m for  12:42 [RT: 56:11], on Air,  SP:0.0, END:2m",
        "  ASCENT: at   0m for   1:00 [RT: 57:11], on Air,  SP:0.0, END:0m", ]

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        diveseg1 = SegmentDive(30, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_segments(self):
        """Check all segments."""
        for idx in range(len(self.expected_result)):
            self.assertEqual(
                str(self.profile1.output_segments[idx]),
                self.expected_result[idx],
                'bad segment n°%s (%s)' % (
                    idx, self.profile1.output_segments[idx]))


class TestDiveAirDiveOutput_woExc(TestDive):
    """Test segments output for air dive 1 without exc."""

    expected_result = [
        " DESCENT: at  30m for   1:30 [RT:  1:30], on Air,  SP:0.0, END:29m",
        "   CONST: at  30m for  28:30 [RT: 30:00], on Air,  SP:0.0, END:29m",
        "  ASCENT: at  15m for   1:30 [RT: 31:30], on Air,  SP:0.0, END:14m",
        "    DECO: at  15m for   0:01 [RT: 31:31], on Air,  SP:0.0, END:14m",
        "  ASCENT: at  12m for   1:00 [RT: 32:31], on Air,  SP:0.0, END:11m",
        "    DECO: at  12m for   0:20 [RT: 32:51], on Air,  SP:0.0, END:11m",
        "  ASCENT: at   9m for   1:00 [RT: 33:51], on Air,  SP:0.0, END:8m",
        "    DECO: at   9m for   2:39 [RT: 36:30], on Air,  SP:0.0, END:8m",
        "  ASCENT: at   6m for   1:00 [RT: 37:30], on Air,  SP:0.0, END:5m",
        "    DECO: at   6m for   4:59 [RT: 42:29], on Air,  SP:0.0, END:5m",
        "  ASCENT: at   3m for   1:00 [RT: 43:29], on Air,  SP:0.0, END:2m",
        "    DECO: at   3m for  12:42 [RT: 56:11], on Air,  SP:0.0, END:2m",
        "  ASCENT: at   0m for   1:00 [RT: 57:11], on Air,  SP:0.0, END:0m", ]


    def setUp(self):
        """Init of the tests."""
        super().setUp()
        diveseg1 = SegmentDive(30, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive_without_exceptions()

    def test_segments(self):
        """Check all segments."""
        for idx in range(len(self.expected_result)):
            self.assertEqual(
                str(self.profile1.output_segments[idx]),
                self.expected_result[idx],
                'bad segment n°%s (%s)' % (
                    idx, self.profile1.output_segments[idx]))


class TestDiveAirDiveOutput2(TestDive):
    """Test segments output for air dive 2."""

    expected_result = [
        " DESCENT: at  20m for   1:00 [RT:  1:00], on Air,  SP:0.0, END:19m",
        "   CONST: at  20m for  29:00 [RT: 30:00], on Air,  SP:0.0, END:19m",
        "  ASCENT: at   9m for   1:06 [RT: 31:06], on Air,  SP:0.0, END:8m",
        "    DECO: at   9m for   0:01 [RT: 31:07], on Air,  SP:0.0, END:8m",
        "  ASCENT: at   6m for   1:00 [RT: 32:07], on Air,  SP:0.0, END:5m",
        "    DECO: at   6m for   0:01 [RT: 32:08], on Air,  SP:0.0, END:5m",
        "  ASCENT: at   3m for   1:00 [RT: 33:08], on Air,  SP:0.0, END:2m",
        "    DECO: at   3m for   0:50 [RT: 33:58], on Air,  SP:0.0, END:2m",
        "  ASCENT: at   0m for   1:00 [RT: 34:58], on Air,  SP:0.0, END:0m", ]

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        diveseg2 = SegmentDive(20, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg2], [self.airtank])
        self.profile1.do_dive()

    def test_segments(self):
        """Check all segments."""
        for idx in range(len(self.expected_result)):
            self.assertEqual(
                str(self.profile1.output_segments[idx]),
                self.expected_result[idx],
                'bad segment n°%s (%s)' % (
                    idx, self.profile1.output_segments[idx]))


class TestDiveAirDiveOutput3(TestDive):
    """Test segments output for air dive 3."""

    expected_result = [
        " DESCENT: at  55m for   2:45 [RT:  2:45], on Air,  SP:0.0, END:53m",
        "   CONST: at  55m for  27:15 [RT: 30:00], on Air,  SP:0.0, END:53m",
        "  ASCENT: at  30m for   2:30 [RT: 32:30], on Air,  SP:0.0, END:29m",
        "    DECO: at  30m for   0:01 [RT: 32:31], on Air,  SP:0.0, END:29m",
        "  ASCENT: at  27m for   1:00 [RT: 33:31], on Air,  SP:0.0, END:26m",
        "    DECO: at  27m for   1:11 [RT: 34:42], on Air,  SP:0.0, END:26m",
        "  ASCENT: at  24m for   1:00 [RT: 35:42], on Air,  SP:0.0, END:23m",
        "    DECO: at  24m for   1:27 [RT: 37:09], on Air,  SP:0.0, END:23m",
        "  ASCENT: at  21m for   1:00 [RT: 38:09], on Air,  SP:0.0, END:20m",
        "    DECO: at  21m for   2:34 [RT: 40:43], on Air,  SP:0.0, END:20m",
        "  ASCENT: at  18m for   1:00 [RT: 41:43], on Air,  SP:0.0, END:17m",
        "    DECO: at  18m for   3:17 [RT: 45:00], on Air,  SP:0.0, END:17m",
        "  ASCENT: at  15m for   1:00 [RT: 46:00], on Air,  SP:0.0, END:14m",
        "    DECO: at  15m for   5:24 [RT: 51:24], on Air,  SP:0.0, END:14m",
        "  ASCENT: at  12m for   1:00 [RT: 52:24], on Air,  SP:0.0, END:11m",
        "    DECO: at  12m for   7:02 [RT: 59:26], on Air,  SP:0.0, END:11m",
        "  ASCENT: at   9m for   1:00 [RT: 60:26], on Air,  SP:0.0, END:8m",
        "    DECO: at   9m for  13:49 [RT: 74:15], on Air,  SP:0.0, END:8m",
        "  ASCENT: at   6m for   1:00 [RT: 75:15], on Air,  SP:0.0, END:5m",
        "    DECO: at   6m for  25:28 [RT:100:43], on Air,  SP:0.0, END:5m",
        "  ASCENT: at   3m for   1:00 [RT:101:43], on Air,  SP:0.0, END:2m",
        "    DECO: at   3m for  52:20 [RT:154:03], on Air,  SP:0.0, END:2m",
        "  ASCENT: at   0m for   1:00 [RT:155:03], on Air,  SP:0.0, END:0m", ]

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        diveseg3 = SegmentDive(55, 30 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg3], [self.airdouble])
        self.profile1.do_dive()

    def test_segments(self):
        """Check all segments."""
        for idx in range(len(self.expected_result)):
            self.assertEqual(
                str(self.profile1.output_segments[idx]),
                self.expected_result[idx],
                'bad segment n°%s (%s)' % (
                    idx, self.profile1.output_segments[idx]))


class TestDiveAirDiveOutput4(TestDive):
    """Test segments output for air dive 4."""

    expected_result = [
        " DESCENT: at  55m for   2:45 [RT:  2:45], on Air,  SP:0.0, END:53m",
        "   CONST: at  55m for  27:15 [RT: 30:00], on Air,  SP:0.0, END:53m",
        "  ASCENT: at  30m for   2:30 [RT: 32:30], on Air,  SP:0.0, END:29m",
        "    DECO: at  30m for   0:01 [RT: 32:31], on Air,  SP:0.0, END:29m",
        "  ASCENT: at  27m for   1:00 [RT: 33:31], on Air,  SP:0.0, END:26m",
        "    DECO: at  27m for   1:11 [RT: 34:42], on Air,  SP:0.0, END:26m",
        "  ASCENT: at  24m for   1:00 [RT: 35:42], on Air,  SP:0.0, END:23m",
        "    DECO: at  24m for   1:27 [RT: 37:09], on Air,  SP:0.0, END:23m",
        "  ASCENT: at  21m for   1:00 [RT: 38:09], on Air,  SP:0.0, END:20m",
        "    DECO: at  21m for   1:35 [RT: 39:44], on Nitrox 50,  SP:0.0, END:20m",
        "  ASCENT: at  18m for   1:00 [RT: 40:44], on Nitrox 50,  SP:0.0, END:17m",
        "    DECO: at  18m for   2:03 [RT: 42:47], on Nitrox 50,  SP:0.0, END:17m",
        "  ASCENT: at  15m for   1:00 [RT: 43:47], on Nitrox 50,  SP:0.0, END:14m",
        "    DECO: at  15m for   2:55 [RT: 46:42], on Nitrox 50,  SP:0.0, END:14m",
        "  ASCENT: at  12m for   1:00 [RT: 47:42], on Nitrox 50,  SP:0.0, END:11m",
        "    DECO: at  12m for   4:13 [RT: 51:55], on Nitrox 50,  SP:0.0, END:11m",
        "  ASCENT: at   9m for   1:00 [RT: 52:55], on Nitrox 50,  SP:0.0, END:8m",
        "    DECO: at   9m for   6:41 [RT: 59:36], on Nitrox 50,  SP:0.0, END:8m",
        "  ASCENT: at   6m for   1:00 [RT: 60:36], on Nitrox 50,  SP:0.0, END:5m",
        "    DECO: at   6m for   7:20 [RT: 67:56], on Oxygen,  SP:0.0, END:5m",
        "  ASCENT: at   3m for   1:00 [RT: 68:56], on Oxygen,  SP:0.0, END:2m",
        "    DECO: at   3m for  12:32 [RT: 81:28], on Oxygen,  SP:0.0, END:2m",
        "  ASCENT: at   0m for   1:00 [RT: 82:28], on Oxygen,  SP:0.0, END:0m", ]

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        diveseg3 = SegmentDive(55, 30 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg3], [self.airdouble, self.decoo2,
                             self.deco2])
        self.profile1.do_dive()

    def test_segments(self):
        """Check all segments."""
        for idx in range(len(self.expected_result)):
            self.assertEqual(
                str(self.profile1.output_segments[idx]),
                self.expected_result[idx],
                'bad segment n°%s (%s)' % (
                    idx, self.profile1.output_segments[idx]))


class TestDiveTxDiveOutput1(TestDive):
    """Test segments output for tx dive 1."""

    expected_result = [
        " DESCENT: at  30m for   1:30 [RT:  1:30], on Trimix 21/30,  SP:0.0, END:19m",
        "   CONST: at  30m for  28:30 [RT: 30:00], on Trimix 21/30,  SP:0.0, END:19m",
        "  ASCENT: at  15m for   1:30 [RT: 31:30], on Trimix 21/30,  SP:0.0, END:8m",
        "    DECO: at  15m for   0:01 [RT: 31:31], on Trimix 21/30,  SP:0.0, END:8m",
        "  ASCENT: at  12m for   1:00 [RT: 32:31], on Trimix 21/30,  SP:0.0, END:6m",
        "    DECO: at  12m for   0:38 [RT: 33:09], on Trimix 21/30,  SP:0.0, END:6m",
        "  ASCENT: at   9m for   1:00 [RT: 34:09], on Trimix 21/30,  SP:0.0, END:4m",
        "    DECO: at   9m for   3:04 [RT: 37:13], on Trimix 21/30,  SP:0.0, END:4m",
        "  ASCENT: at   6m for   1:00 [RT: 38:13], on Trimix 21/30,  SP:0.0, END:1m",
        "    DECO: at   6m for   6:25 [RT: 44:38], on Trimix 21/30,  SP:0.0, END:1m",
        "  ASCENT: at   3m for   1:00 [RT: 45:38], on Trimix 21/30,  SP:0.0, END:0m",
        "    DECO: at   3m for  16:12 [RT: 61:50], on Trimix 21/30,  SP:0.0, END:0m",
        "  ASCENT: at   0m for   1:00 [RT: 62:50], on Trimix 21/30,  SP:0.0, END:0m", ]

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        diveseg1 = SegmentDive(30, 30 * 60, self.txtank1, 0)
        self.profile1 = Dive([diveseg1], [self.txtank1])
        self.profile1.do_dive()

    def test_segments(self):
        """Check all segments."""
        for idx in range(len(self.expected_result)):
            self.assertEqual(
                str(self.profile1.output_segments[idx]),
                self.expected_result[idx],
                'bad segment n°%s (%s)' % (
                    idx, self.profile1.output_segments[idx]))


class TestDiveCCRDiveOutput1(TestDive):
    """Test segments output for ccr dive 1."""

    expected_result = [
        " DESCENT: at  55m for   2:45 [RT:  2:45], on Trimix 21/30,  SP:1.4, END:38m",
        "   CONST: at  55m for  27:15 [RT: 30:00], on Trimix 21/30,  SP:1.4, END:38m",
        "  ASCENT: at  30m for   2:30 [RT: 32:30], on Trimix 21/30,  SP:1.4, END:21m",
        "    DECO: at  30m for   0:01 [RT: 32:31], on Trimix 21/30,  SP:1.4, END:21m",
        "  ASCENT: at  27m for   1:00 [RT: 33:31], on Trimix 21/30,  SP:1.4, END:19m",
        "    DECO: at  27m for   0:31 [RT: 34:02], on Trimix 21/30,  SP:1.4, END:19m",
        "  ASCENT: at  24m for   1:00 [RT: 35:02], on Trimix 21/30,  SP:1.4, END:17m",
        "    DECO: at  24m for   1:02 [RT: 36:04], on Trimix 21/30,  SP:1.4, END:17m",
        "  ASCENT: at  21m for   1:00 [RT: 37:04], on Trimix 21/30,  SP:1.4, END:15m",
        "    DECO: at  21m for   1:26 [RT: 38:30], on Trimix 21/30,  SP:1.4, END:15m",
        "  ASCENT: at  18m for   1:00 [RT: 39:30], on Trimix 21/30,  SP:1.4, END:13m",
        "    DECO: at  18m for   1:55 [RT: 41:25], on Trimix 21/30,  SP:1.4, END:13m",
        "  ASCENT: at  15m for   1:00 [RT: 42:25], on Trimix 21/30,  SP:1.4, END:11m",
        "    DECO: at  15m for   2:21 [RT: 44:46], on Trimix 21/30,  SP:1.4, END:11m",
        "  ASCENT: at  12m for   1:00 [RT: 45:46], on Trimix 21/30,  SP:1.4, END:9m",
        "    DECO: at  12m for   3:21 [RT: 49:07], on Trimix 21/30,  SP:1.4, END:9m",
        "  ASCENT: at   9m for   1:00 [RT: 50:07], on Trimix 21/30,  SP:1.4, END:7m",
        "    DECO: at   9m for   5:15 [RT: 55:22], on Trimix 21/30,  SP:1.4, END:7m",
        "  ASCENT: at   6m for   1:00 [RT: 56:22], on Trimix 21/30,  SP:1.4, END:4m",
        "    DECO: at   6m for   6:44 [RT: 63:06], on Oxygen,  SP:0.0, END:5m",
        "  ASCENT: at   3m for   1:00 [RT: 64:06], on Oxygen,  SP:0.0, END:2m",
        "    DECO: at   3m for  12:26 [RT: 76:32], on Oxygen,  SP:0.0, END:2m",
        "  ASCENT: at   0m for   1:00 [RT: 77:32], on Oxygen,  SP:0.0, END:0m", ]

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        diveseg1 = SegmentDive(55, 30 * 60, self.txtank1, 1.4)
        self.profile1 = Dive([diveseg1], [self.txtank1, self.decoo2])
        self.profile1.do_dive()

    def test_segments(self):
        """Check all segments."""
        for idx in range(len(self.expected_result)):
            self.assertEqual(
                str(self.profile1.output_segments[idx]),
                self.expected_result[idx],
                'bad segment n°%s (%s)' % (
                    idx, self.profile1.output_segments[idx]))
