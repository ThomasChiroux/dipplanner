#!/usr/bin/python2
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

"""Test for Dive class

TODO: more test profiles
"""

__authors__ = ['Thomas Chiroux']  # alphabetical order by last name

import unittest

# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.dive import Dive
from dipplanner.dive import ProcessingError, NothingToProcess, InfiniteDeco
from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive
from dipplanner.segment import SegmentDeco
from dipplanner.segment import SegmentAscDesc
from dipplanner.segment import UnauthorizedMod
from dipplanner.tools import seconds_to_mmss
from dipplanner import settings


class TestDive(unittest.TestCase):

    def setUp(self):

        # temporary hack (tests):

        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        self.air12l = Tank(tank_vol=12.0, tank_pressure=200)
        self.airtank = Tank(tank_vol=18.0, tank_pressure=200)
        self.airtank12 = Tank(tank_vol=12.0, tank_pressure=200)
        self.airdouble = Tank(tank_vol=30.0, tank_pressure=200)  # bi15l 200b
        self.txtank1 = Tank(0.21, 0.30, tank_vol=20.0,
                            tank_pressure=200)
        self.txtanknormodbl = Tank(0.21, 0.30, tank_vol=30.0,
                                   tank_pressure=200)
        self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200)
        self.deco2 = Tank(0.5, 0.0, tank_vol=7.0, tank_pressure=200)
        self.decoo2 = Tank(1.0, 0.0, tank_vol=7.0, tank_pressure=200)


class TestDiveNotEnoughGas1(TestDive):

    def runTest(self):
        diveseg1 = SegmentDive(60, 30 * 60, self.air12l, 0)
        self.profile1 = Dive([diveseg1], [self.air12l])
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

class TestDiveAirDiveOutput1(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_segment1(self):
        self.assertEqual(str(self.profile1.output_segments[0]),
            ' DESCENT: at  30m for   1:30 [RT:  1:30], '
            'on Air,  SP:0.0, END:29m',
            'bad segment (%s)'
            % self.profile1.output_segments[0])

    def test_segment2(self):
        self.assertEqual(str(self.profile1.output_segments[1]),
            '   CONST: at  30m for  28:30 [RT: 30:00], '
            'on Air,  SP:0.0, END:29m',
            'bad segment (%s)'
            % self.profile1.output_segments[1])

    def test_segment3(self):
        self.assertEqual(str(self.profile1.output_segments[2]),
            '  ASCENT: at  15m for   1:30 [RT: 31:30], '
            'on Air,  SP:0.0, END:14m',
            'bad segment (%s)'
            % self.profile1.output_segments[2])

    def test_segment4(self):
        self.assertEqual(str(self.profile1.output_segments[3]),
            '    DECO: at  15m for   0:01 [RT: 31:31], '
            'on Air,  SP:0.0, END:14m',
            'bad segment (%s)'
            % self.profile1.output_segments[3])

    def test_segment5(self):
        self.assertEqual(str(self.profile1.output_segments[4]),
            '    DECO: at  12m for   0:25 [RT: 31:56], '
            'on Air,  SP:0.0, END:11m',
            'bad segment (%s)'
            % self.profile1.output_segments[4])

    def test_segment6(self):
        self.assertEqual(str(self.profile1.output_segments[5]),
            '    DECO: at   9m for   2:42 [RT: 34:38], '
            'on Air,  SP:0.0, END:8m',
            'bad segment (%s)'
            % self.profile1.output_segments[5])

    def test_segment7(self):
        self.assertEqual(str(self.profile1.output_segments[6]),
            '    DECO: at   6m for   5:02 [RT: 39:40], '
            'on Air,  SP:0.0, END:5m',
            'bad segment (%s)'
            % self.profile1.output_segments[6])

    def test_segment8(self):
        self.assertEqual(str(self.profile1.output_segments[7]),
            '    DECO: at   3m for   8:44 [RT: 48:24], '
            'on Air,  SP:0.0, END:2m',
            'bad segment (%s)'
            % self.profile1.output_segments[7])

class TestDiveAirDiveOutput_woExc(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive_without_exceptions()

    def test_segment1(self):
        self.assertEqual(str(self.profile1.output_segments[0]),
                         ' DESCENT: at  30m for   1:30 [RT:  1:30], '
                         'on Air,  SP:0.0, END:29m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[0])

    def test_segment2(self):
        self.assertEqual(str(self.profile1.output_segments[1]),
                         '   CONST: at  30m for  28:30 [RT: 30:00], '
                         'on Air,  SP:0.0, END:29m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[1])

    def test_segment3(self):
        self.assertEqual(str(self.profile1.output_segments[2]),
                         '  ASCENT: at  15m for   1:30 [RT: 31:30], '
                         'on Air,  SP:0.0, END:14m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[2])

    def test_segment4(self):
        self.assertEqual(str(self.profile1.output_segments[3]),
                         '    DECO: at  15m for   0:01 [RT: 31:31], '
                         'on Air,  SP:0.0, END:14m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[3])

    def test_segment5(self):
        self.assertEqual(str(self.profile1.output_segments[4]),
                         '    DECO: at  12m for   0:25 [RT: 31:56], '
                         'on Air,  SP:0.0, END:11m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[4])

    def test_segment6(self):
        self.assertEqual(str(self.profile1.output_segments[5]),
                         '    DECO: at   9m for   2:42 [RT: 34:38], '
                         'on Air,  SP:0.0, END:8m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[5])

    def test_segment7(self):
        self.assertEqual(str(self.profile1.output_segments[6]),
                         '    DECO: at   6m for   5:02 [RT: 39:40], '
                         'on Air,  SP:0.0, END:5m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[6])

    def test_segment8(self):
        self.assertEqual(str(self.profile1.output_segments[7]),
                         '    DECO: at   3m for   8:44 [RT: 48:24], '
                         'on Air,  SP:0.0, END:2m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[7])


class TestDiveAirDiveRunTime1(TestDive):

    def runTest(self):
        diveseg1 = SegmentDive(30, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 48:24', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))


class TestDiveAirDiveOutput2(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg2 = SegmentDive(20, 30 * 60, self.airtank, 0)
        self.profile2 = Dive([diveseg2], [self.airtank])
        self.profile2.do_dive()

    def test_segment1(self):
        self.assertEqual(str(self.profile2.output_segments[0]),
                         ' DESCENT: at  20m for   1:00 [RT:  1:00], '
                         'on Air,  SP:0.0, END:19m',
                         'bad segment (%s)'
                         % self.profile2.output_segments[0])

    def test_segment2(self):
        self.assertEqual(str(self.profile2.output_segments[1]),
                         '   CONST: at  20m for  29:00 [RT: 30:00], '
                         'on Air,  SP:0.0, END:19m',
                         'bad segment (%s)'
                         % self.profile2.output_segments[1])

    def test_segment3(self):
        self.assertEqual(str(self.profile2.output_segments[2]),
                         '  ASCENT: at   9m for   1:06 [RT: 31:06], '
                         'on Air,  SP:0.0, END:8m',
                         'bad segment (%s)'
                         % self.profile2.output_segments[2])

    def test_segment4(self):
        self.assertEqual(str(self.profile2.output_segments[3]),
                         '    DECO: at   9m for   0:01 [RT: 31:07], '
                         'on Air,  SP:0.0, END:8m',
                         'bad segment (%s)'
                         % self.profile2.output_segments[3])

    def test_segment5(self):
        self.assertEqual(str(self.profile2.output_segments[4]),
                         '    DECO: at   6m for   0:01 [RT: 31:08], '
                         'on Air,  SP:0.0, END:5m',
                         'bad segment (%s)'
                         % self.profile2.output_segments[4])

    def test_segment6(self):
        self.assertEqual(str(self.profile2.output_segments[5]),
                         '    DECO: at   3m for   0:56 [RT: 32:04], '
                         'on Air,  SP:0.0, END:2m',
                         'bad segment (%s)'
                         % self.profile2.output_segments[5])


class TestDiveAirDiveRunTime2(TestDive):

    def runTest(self):
        diveseg2 = SegmentDive(20, 30 * 60, self.airtank, 0)
        self.profile2 = Dive([diveseg2], [self.airtank])
        self.profile2.do_dive()
        self.assertEqual(seconds_to_mmss(self.profile2.run_time),
                         ' 32:04', 'bad dive runtime (%s)'
                         % seconds_to_mmss(self.profile2.run_time))


class TestDiveAirDiveOutput3(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg3 = SegmentDive(55, 30 * 60, self.airdouble, 0)
        self.profile3 = Dive([diveseg3], [self.airdouble])
        self.profile3.do_dive()

    def test_segment1(self):
        self.assertEqual(str(self.profile3.output_segments[0]),
                         ' DESCENT: at  55m for   2:45 [RT:  2:45], '
                         'on Air,  SP:0.0, END:53m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[0])

    def test_segment2(self):
        self.assertEqual(str(self.profile3.output_segments[1]),
                         '   CONST: at  55m for  27:15 [RT: 30:00], '
                         'on Air,  SP:0.0, END:53m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[1])

    def test_segment3(self):
        self.assertEqual(str(self.profile3.output_segments[2]),
                         '  ASCENT: at  30m for   2:30 [RT: 32:30], '
                         'on Air,  SP:0.0, END:29m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[2])

    def test_segment4(self):
        self.assertEqual(str(self.profile3.output_segments[3]),
                         '    DECO: at  30m for   0:01 [RT: 32:31], '
                         'on Air,  SP:0.0, END:29m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[3])

    def test_segment5(self):
        self.assertEqual(str(self.profile3.output_segments[4]),
                         '    DECO: at  27m for   1:15 [RT: 33:46], '
                         'on Air,  SP:0.0, END:26m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[4])

    def test_segment6(self):
        self.assertEqual(str(self.profile3.output_segments[5]),
                         '    DECO: at  24m for   1:33 [RT: 35:19], '
                         'on Air,  SP:0.0, END:23m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[5])

    def test_segment7(self):
        self.assertEqual(str(self.profile3.output_segments[6]),
                         '    DECO: at  21m for   2:37 [RT: 37:56], '
                         'on Air,  SP:0.0, END:20m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[6])

    def test_segment8(self):
        self.assertEqual(str(self.profile3.output_segments[7]),
                         '    DECO: at  18m for   3:23 [RT: 41:19], '
                         'on Air,  SP:0.0, END:17m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[7])

    def test_segment9(self):
        self.assertEqual(str(self.profile3.output_segments[8]),
                         '    DECO: at  15m for   5:26 [RT: 46:45], '
                         'on Air,  SP:0.0, END:14m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[8])

    def test_segment10(self):
        self.assertEqual(str(self.profile3.output_segments[9]),
                         '    DECO: at  12m for   6:41 [RT: 53:26], '
                         'on Air,  SP:0.0, END:11m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[9])

    def test_segment11(self):
        self.assertEqual(str(self.profile3.output_segments[10]),
                         '    DECO: at   9m for  11:01 [RT: 64:27], '
                         'on Air,  SP:0.0, END:8m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[10])

    def test_segment12(self):
        self.assertEqual(str(self.profile3.output_segments[11]),
                         '    DECO: at   6m for  21:36 [RT: 86:03], '
                         'on Air,  SP:0.0, END:5m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[11])

    def test_segment13(self):
        self.assertEqual(str(self.profile3.output_segments[12]),
                         '    DECO: at   3m for  45:02 [RT:131:05], '
                         'on Air,  SP:0.0, END:2m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[12])


class TestDiveAirDiveRunTime3(TestDive):

    def runTest(self):
        diveseg3 = SegmentDive(55, 30 * 60, self.airdouble, 0)
        self.profile3 = Dive([diveseg3], [self.airdouble])
        self.profile3.do_dive()
        self.assertEqual(seconds_to_mmss(self.profile3.run_time),
                         '131:05', 'bad dive runtime (%s)'
                         % seconds_to_mmss(self.profile3.run_time))


class TestDiveAirDiveOutput4(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg3 = SegmentDive(55, 30 * 60, self.airdouble, 0)
        self.profile3 = Dive([diveseg3], [self.airdouble, self.decoo2,
                             self.deco2])
        self.profile3.do_dive()

    def test_segment1(self):
        self.assertEqual(str(self.profile3.output_segments[0]),
                         ' DESCENT: at  55m for   2:45 [RT:  2:45], '
                         'on Air,  SP:0.0, END:53m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[0])

    def test_segment2(self):
        self.assertEqual(str(self.profile3.output_segments[1]),
                         '   CONST: at  55m for  27:15 [RT: 30:00], '
                         'on Air,  SP:0.0, END:53m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[1])

    def test_segment3(self):
        self.assertEqual(str(self.profile3.output_segments[2]),
                         '  ASCENT: at  30m for   2:30 [RT: 32:30], '
                         'on Air,  SP:0.0, END:29m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[2])

    def test_segment4(self):
        self.assertEqual(str(self.profile3.output_segments[3]),
                         '    DECO: at  30m for   0:01 [RT: 32:31], '
                         'on Air,  SP:0.0, END:29m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[3])

    def test_segment5(self):
        self.assertEqual(str(self.profile3.output_segments[4]),
                         '    DECO: at  27m for   1:15 [RT: 33:46], '
                         'on Air,  SP:0.0, END:26m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[4])

    def test_segment6(self):
        self.assertEqual(str(self.profile3.output_segments[5]),
                         '    DECO: at  24m for   1:33 [RT: 35:19], '
                         'on Air,  SP:0.0, END:23m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[5])

    def test_segment7(self):
        self.assertEqual(str(self.profile3.output_segments[6]),
                         '    DECO: at  21m for   1:37 [RT: 36:56], '
                         'on Nitrox 50,  SP:0.0, END:20m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[6])

    def test_segment8(self):
        self.assertEqual(str(self.profile3.output_segments[7]),
                         '    DECO: at  18m for   2:09 [RT: 39:05], '
                         'on Nitrox 50,  SP:0.0, END:17m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[7])

    def test_segment9(self):
        self.assertEqual(str(self.profile3.output_segments[8]),
                         '    DECO: at  15m for   2:59 [RT: 42:04], '
                         'on Nitrox 50,  SP:0.0, END:14m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[8])

    def test_segment10(self):
        self.assertEqual(str(self.profile3.output_segments[9]),
                         '    DECO: at  12m for   4:18 [RT: 46:22], '
                         'on Nitrox 50,  SP:0.0, END:11m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[9])

    def test_segment11(self):
        self.assertEqual(str(self.profile3.output_segments[10]),
                         '    DECO: at   9m for   5:48 [RT: 52:10], '
                         'on Nitrox 50,  SP:0.0, END:8m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[10])

    def test_segment12(self):
        self.assertEqual(str(self.profile3.output_segments[11]),
                         '    DECO: at   6m for   6:40 [RT: 58:50], '
                         'on Oxygen,  SP:0.0, END:5m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[11])

    def test_segment13(self):
        self.assertEqual(str(self.profile3.output_segments[12]),
                         '    DECO: at   3m for  11:31 [RT: 70:21], '
                         'on Oxygen,  SP:0.0, END:2m',
                         'bad segment (%s)'
                         % self.profile3.output_segments[12])


class TestDiveAirDiveRunTime4(TestDive):

    def runTest(self):
        diveseg3 = SegmentDive(55, 30 * 60, self.airdouble, 0)
        self.profile3 = Dive([diveseg3], [self.airdouble, self.deco2,
                             self.decoo2])
        self.profile3.do_dive()
        self.assertEqual(seconds_to_mmss(self.profile3.run_time),
                         ' 70:21', 'bad dive runtime (%s)'
                         % seconds_to_mmss(self.profile3.run_time))


class TestDiveTxDiveOutput1(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 30 * 60, self.txtank1, 0)
        self.profile1 = Dive([diveseg1], [self.txtank1])
        self.profile1.do_dive()

    def test_segment1(self):
        self.assertEqual(str(self.profile1.output_segments[0]),
                         ' DESCENT: at  30m for   1:30 [RT:  1:30], '
                         'on Trimix 21/30,  SP:0.0, END:19m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[0])

    def test_segment2(self):
        self.assertEqual(str(self.profile1.output_segments[1]),
                         '   CONST: at  30m for  28:30 [RT: 30:00], '
                         'on Trimix 21/30,  SP:0.0, END:19m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[1])

    def test_segment3(self):
        self.assertEqual(str(self.profile1.output_segments[2]),
                         '  ASCENT: at  15m for   1:30 [RT: 31:30], '
                         'on Trimix 21/30,  SP:0.0, END:8m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[2])

    def test_segment4(self):
        self.assertEqual(str(self.profile1.output_segments[3]),
                         '    DECO: at  15m for   0:01 [RT: 31:31], '
                         'on Trimix 21/30,  SP:0.0, END:8m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[3])

    def test_segment5(self):
        self.assertEqual(str(self.profile1.output_segments[4]),
                         '    DECO: at  12m for   0:43 [RT: 32:14], '
                         'on Trimix 21/30,  SP:0.0, END:6m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[4])

    def test_segment6(self):
        self.assertEqual(str(self.profile1.output_segments[5]),
                         '    DECO: at   9m for   3:08 [RT: 35:22], '
                         'on Trimix 21/30,  SP:0.0, END:4m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[5])

    def test_segment7(self):
        self.assertEqual(str(self.profile1.output_segments[6]),
                         '    DECO: at   6m for   5:15 [RT: 40:37], '
                         'on Trimix 21/30,  SP:0.0, END:1m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[6])

    def test_segment8(self):
        self.assertEqual(str(self.profile1.output_segments[7]),
                         '    DECO: at   3m for  14:26 [RT: 55:03], '
                         'on Trimix 21/30,  SP:0.0, END:0m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[7])


class TestDiveTxDiveRunTime1(TestDive):

    def runTest(self):
        diveseg1 = SegmentDive(30, 30 * 60, self.txtank1, 0)
        self.profile1 = Dive([diveseg1], [self.txtank1])
        self.profile1.do_dive()
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 55:03', 'bad dive runtime (%s)'
                         % seconds_to_mmss(self.profile1.run_time))


class TestDiveCCRDiveOutput1(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(55, 30 * 60, self.txtank1, 1.4)
        self.profile1 = Dive([diveseg1], [self.txtank1, self.decoo2])
        self.profile1.do_dive()

    def test_segment1(self):
        self.assertEqual(str(self.profile1.output_segments[0]),
                         ' DESCENT: at  55m for   2:45 [RT:  2:45], '
                         'on Trimix 21/30,  SP:1.4, END:38m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[0])

    def test_segment2(self):
        self.assertEqual(str(self.profile1.output_segments[1]),
                         '   CONST: at  55m for  27:15 [RT: 30:00], '
                         'on Trimix 21/30,  SP:1.4, END:38m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[1])

    def test_segment3(self):
        self.assertEqual(str(self.profile1.output_segments[2]),
                         '  ASCENT: at  30m for   2:30 [RT: 32:30], '
                         'on Trimix 21/30,  SP:1.4, END:21m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[2])

    def test_segment4(self):
        self.assertEqual(str(self.profile1.output_segments[3]),
                         '    DECO: at  30m for   0:01 [RT: 32:31], '
                         'on Trimix 21/30,  SP:1.4, END:21m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[3])

    def test_segment5(self):
        self.assertEqual(str(self.profile1.output_segments[4]),
                         '    DECO: at  27m for   0:36 [RT: 33:07], '
                         'on Trimix 21/30,  SP:1.4, END:19m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[4])

    def test_segment6(self):
        self.assertEqual(str(self.profile1.output_segments[5]),
                         '    DECO: at  24m for   1:08 [RT: 34:15], '
                         'on Trimix 21/30,  SP:1.4, END:17m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[5])

    def test_segment7(self):
        self.assertEqual(str(self.profile1.output_segments[6]),
                         '    DECO: at  21m for   1:32 [RT: 35:47], '
                         'on Trimix 21/30,  SP:1.4, END:15m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[6])

    def test_segment8(self):
        self.assertEqual(str(self.profile1.output_segments[7]),
                         '    DECO: at  18m for   2:01 [RT: 37:48], '
                         'on Trimix 21/30,  SP:1.4, END:13m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[7])

    def test_segment9(self):
        self.assertEqual(str(self.profile1.output_segments[8]),
                         '    DECO: at  15m for   2:14 [RT: 40:02], '
                         'on Trimix 21/30,  SP:1.4, END:11m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[8])

    def test_segment10(self):
        self.assertEqual(str(self.profile1.output_segments[9]),
                         '    DECO: at  12m for   3:21 [RT: 43:23], '
                         'on Trimix 21/30,  SP:1.4, END:9m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[9])

    def test_segment11(self):
        self.assertEqual(str(self.profile1.output_segments[10]),
                         '    DECO: at   9m for   5:05 [RT: 48:28], '
                         'on Trimix 21/30,  SP:1.4, END:7m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[10])

    def test_segment12(self):
        self.assertEqual(str(self.profile1.output_segments[11]),
                         '    DECO: at   6m for   6:28 [RT: 54:56], '
                         'on Oxygen,  SP:0.0, END:5m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[11])

    def test_segment13(self):
        self.assertEqual(str(self.profile1.output_segments[12]),
                         '    DECO: at   3m for  11:52 [RT: 66:48], '
                         'on Oxygen,  SP:0.0, END:2m',
                         'bad segment (%s)'
                         % self.profile1.output_segments[12])


# =============================================================================
# ========================== M A I N ==========================================
# =============================================================================

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


if __name__ == '__main__':
    main()
