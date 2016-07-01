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
"""Test for CC mode."""
import unittest

# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.dive import Dive
from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner.tools import seconds_to_mmss
from dipplanner import settings


class TestDive(unittest.TestCase):

    def setUp(self):

        # temporary hack (tests):

        activate_debug_for_tests()

        self.air = Tank(tank_vol=3.0, tank_pressure=200, tank_rule='10b'
                        )
        self.txhypo = Tank(0.10, 0.50, tank_vol=3.0, tank_pressure=200,
                           tank_rule='10b')
        self.setpoint = 1.2

        settings.RUN_TIME = False
        settings.SURFACE_TEMP = 12


# Diluant: AIR ================================================================
# ==================================================== 10m tests ==============

class TestDiveCCAir10m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 10 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 11:30', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               13.437123003, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               4.83407833333, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         60,
                         "Bad full desat time: %s" % desat)

class TestDiveCCAir10m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 20 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 21:30', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               26.673627586, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               9.59598309524, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         60,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir10m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 30 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 31:30', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               39.9101321691, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               14.3578878571, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         60,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir10m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 40 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 41:30', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               53.1466367522, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               19.119792619, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         60,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir10m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 50 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 51:30', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               66.3831413353, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               23.881697381, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         60,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir10m60min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 60 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 61:30', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               79.6196459184, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               28.6436021429, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         120,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir10m70min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 70 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

# ==================================================== 20m tests ==============

class TestDiveCCAir20m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 10 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 13:00', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               13.6377414229, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               4.90625190476, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 420, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         10680,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir20m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 20 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 23:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               26.989928776184342, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               9.709774174603176, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         21300,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir20m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 30 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 33:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               40.226433359261875, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               14.471678936507931, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         31860,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir20m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 40 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 43:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               53.46293794233939, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               19.233583698412694, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 120, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         42600,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir20m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 50 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())


# ==================================================== 30m tests ==============

class TestDiveCCAir30m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 10 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 15:56', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               14.069725383247963, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               5.0616604920634956, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 60, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         21540,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir30m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 20 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 27:45', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               28.87792824071702, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               10.388992285714304, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 480, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         42000,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir30m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 30 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 41:53', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               46.752587993265855, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               16.819498682539365, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1200, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         59220,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir30m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 40 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 56:01', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               65.46018113734856, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               23.549657412697815, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1980, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         72240,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir30m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 50 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())


# ==================================================== 40m tests ==============

class TestDiveCCAir40m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 20:15', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               16.33275914430105, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               5.875799238095263, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 300, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         31560,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir40m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 20 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 38:32', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               38.867634907293095, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               13.982843777777653, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1260, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         59100,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir40m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 30 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 58:51', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               64.92686666037831, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               23.35779461904639, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2400, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         77400,
                         "Bad full desat time: %s" % desat)


class TestDiveCCAir40m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 40 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.air])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())


# ==================================================== 50m tests ==============

class TestDiveCCAir50m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)

    def runTest(self):
        try:
            diveseg1 = SegmentDive(50, 10 * 60, self.air, self.setpoint)
            self.profile1 = Dive([diveseg1], [self.air])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail('should raise UnauthorizedMod')


# Diluant: Trimix Hypo ========================================================
# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ====================================
# ==================================================== 50m tests ==============

class TestDiveCCHypo50m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 10 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 29:22', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               24.11638171369745, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               8.675999936508044, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 840, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         26100,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo50m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 20 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 58:09', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               60.549587288921494, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               21.783044476189254, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2640, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         40260,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo50m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 30 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 89:14', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               101.69305570131004, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               36.584631777774675, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 5520, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         48180,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo50m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 40 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '122:29', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               144.87150004849605, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               52.11831277777457, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 8580, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         53100,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo50m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 50 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))


# ==================================================== 60m tests ==============

class TestDiveCCHypo60m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 10 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 38:07', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               32.24759917324864, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               11.601249793650988, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1200, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         31140,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo60m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 20 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 76:06', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               80.85838896489913, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               29.089246714283455, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 4500, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         45180,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo60m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 30 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '118:48', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               136.54533014309, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               49.12292771428083, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 8340, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         52620,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo60m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 40 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))


# ==================================================== 70m tests ==============

class TestDiveCCHypo70m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 10 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 48:19', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               41.46517640581184, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               14.917323507936386, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1800, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         35280,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo70m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 20 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 97:31', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               104.92291217147395, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               37.74659026983778, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 6000, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         49200,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo70m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 30 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))


# ==================================================== 80m tests ==============

class TestDiveCCHypo80m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 10 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 59:17', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               52.530485714612006, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               18.89812892063423, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2520, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         39120,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo80m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 20 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '122:31', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               134.56344957851755, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               48.40993536507436, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 8760, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         52740,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo80m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 30 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))


# ==================================================== 90m tests ==============

class TestDiveCCHypo90m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 10 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 71:16', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               64.94150632269152, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               23.363061317458993, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 3660, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         42600,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo90m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 20 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '149:42', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               166.26102376133153, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               59.813310666666865, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 11640, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         55560,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo90m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 30 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))


# =================================================== 100m tests ==============

class TestDiveCCHypo100m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 10 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 85:04', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               79.75715859669238, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               28.693073079362996, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 4860, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         45720,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo100m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 15 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '131:22', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               139.3763080332561, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               50.14138746031232, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 9480, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         53400,
                         "Bad full desat time: %s" % desat)


class TestDiveCCHypo100m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 20 * 60, self.txhypo, self.setpoint)
        self.profile1 = Dive([diveseg1], [self.txhypo])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))


# =================================================== 110m tests ==============

class TestDiveCCHypo110m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)

    def runTest(self):
        try:
            diveseg1 = SegmentDive(110, 10 * 60, self.txhypo,
                                   self.setpoint)
            self.profile1 = Dive([diveseg1], [self.txhypo])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail('should raise UnauthorizedMod')


# ======================= Multilevel Dive =====================================

class TestDiveMultilevel(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.air, self.setpoint)
        diveseg2 = SegmentDive(45, 12 * 60, self.air, self.setpoint)
        diveseg3 = SegmentDive(30, 15 * 60, self.air, self.setpoint)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3], [self.air])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 66:19', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               75.58356156502136, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               27.19159876983997, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.air.used_gas, 0.0, 7,
                               'bad used gas (%s)' % self.air.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2820, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         83160,
                         "Bad full desat time: %s" % desat)


# =============================================================================
# ========================= M A I N ===========================================
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
