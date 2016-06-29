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
"""Test Dives in hypoxic trimix."""
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

        self.txhypo = Tank(0.10, 0.50,
                           tank_vol=30.0, tank_pressure=200)  # 2x 15l
        self.txtravel = Tank(0.21, 0.30, tank_vol=24.0,
                             tank_pressure=200)  # 2x S80
        self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200)  # 1x S80

        self.divesegdesc1 = SegmentDive(40, 130, self.txtravel, 0)
        self.divesegdesc2 = SegmentDive(40, 30, self.txhypo, 0)

        settings.RUN_TIME = False
        settings.SURFACE_TEMP = 12


# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ====================================
# ==================================================== 50m tests ==============

class TestDiveTxHypo50m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 34:40', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 14, 0,
                               'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 8,
                               0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 1063.50427732, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1140, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo50m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 70:35', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 39, 0,
                               'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               23, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2094.62227732, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 4320, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo50m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '113:19', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               68.41018165372607, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               40, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3125.74027732, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 8220, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo50m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 40 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '160:26', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               102.25472115141113, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               58.59929779247194, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4156.85827732, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 13440, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo50m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 50 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# ==================================================== 60m tests ==============

class TestDiveTxHypo60m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 44:03', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 21, 0,
                               'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               12, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 1291.12760482, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1560, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo60m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 91:26', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               58.27243170631685, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               32, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2494.01870482, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 6120, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo60m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '146:52', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               100.9401275017839, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               56, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3696.90980482, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 12420, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo60m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 40 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# ==================================================== 70m tests ==============

class TestDiveTxHypo70m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 53:46', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 30, 0,
                               'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               16, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 1580.95197052, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2340, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo70m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '114:36', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               78.67797998734787, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               42.49520678854243, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2955.61617052, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 8280, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo70m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# ==================================================== 80m tests ==============

class TestDiveTxHypo80m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 65:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               39.97131998326519, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               21, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 1971.80768302, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 3060, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo80m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '140:39', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               103.048494213224, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               55, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3518.24498302, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 11520, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo80m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# ==================================================== 90m tests ==============

class TestDiveTxHypo90m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 77:14', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               49.78981737617727, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               27, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2388.42936052, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 4440, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo90m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '170:17', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               129.52062953350546, 5,
                               'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               68.5234776437918, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4106.63976052, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 14460, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo90m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# =================================================== 100m tests ==============

class TestDiveTxHypo100m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 91:32', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               61.24430791066309, 3, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               32, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2830.81700302, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 5700, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo100m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '143:38', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               107.74900015134172, 0,
                               'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               57, 0, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3775.80875302, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 11640, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo100m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# =================================================== 110m tests ==============

class TestDiveTxHypo110m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(110, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '106:23', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               74.27833402994307, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               39.73311873051845, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3298.97061052, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 6660, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo110m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(110, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '167:54', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               128.3582279940003, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               68.80253012506343, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4424.666418673434, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 13980, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo110m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(110, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# =================================================== 120m tests ==============

class TestDiveTxHypo120m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(120, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '122:46', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               87.45903983744498, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               47.095873055392815, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3887.7076911734343, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 8400, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo120m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(120, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# =================================================== 130m tests ==============

class TestDiveTxHypo130m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(130, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '141:11', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               103.24989705478667, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               57.99808348439559, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4617.614088073433, 1,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 10620, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo130m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(130, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# =================================================== 140m tests ==============

class TestDiveTxHypo140m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(140, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '160:21', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               119.71933135854655, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               80.98821829365991, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 5424.244738573434, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 12840, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo140m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(140, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# =================================================== 150m tests ==============

class TestDiveTxHypo150m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(150, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '184:02', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               138.68333026220657, 5, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               151.09048726727502, 5, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 6285.765894673433, 5,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank_cons_rule_2(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 14940, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxHypo150m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(150, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))


# =================================================== 160m tests ==============

class TestDiveTxHypo160m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)

    def runTest(self):
        try:
            diveseg1 = SegmentDive(160, 10 * 60, self.txhypo, 0)
            self.profile1 = Dive([diveseg1], [self.txtravel,
                                 self.txhypo, self.deco1])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail('should raise UnauthorizedMod')


# ======================== Multilevel Dive ====================================

class TestDiveMultilevel(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.txhypo, 0)
        diveseg2 = SegmentDive(50, 12 * 60, self.txhypo, 0)
        diveseg3 = SegmentDive(30, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3],
                             [self.txtravel, self.txhypo, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '102:29', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               52.12326676000943, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               31.797127780758593, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3347.1747525, 7,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 6720, 'Bad no flight time: %s'
                         % no_flight_time)


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
