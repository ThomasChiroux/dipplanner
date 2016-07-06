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
"""Test Dives in hypoxic trimix with forced travel."""
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
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        self.txhypo = Tank(0.10, 0.50,
                           tank_vol=30.0, tank_pressure=200)  # 2x 15l
        self.txtravel = Tank(0.21, 0.30, tank_vol=24.0,
                             tank_pressure=200)  # 2x S80
        self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200)  # 1x S80

        self.divesegdesc1 = SegmentDive(40, 130, self.txtravel, 0)
        self.divesegdesc2 = SegmentDive(40, 30, self.txhypo, 0)


# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ====================================
# ==================================================== 50m tests ==============

class TestDiveTxHypo50m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 36:25',
                         'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               15.261980881960767, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               9.254998761326787, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 1121.3468175, 7,
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
        self.assertEqual(no_flight_time, 1200, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         29220,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo50m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 73:06',
                         'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               40.598833329371914, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               23.7936518592808, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2152.4648175, 7,
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
        self.assertEqual(no_flight_time, 4500, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         42840,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo50m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '115:46', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               70.07737941194578, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               40.90608663364815, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3183.5828175, 7,
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
        self.assertEqual(no_flight_time, 8460, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         49980,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo50m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 40 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '163:06', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               104.07204564091363, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               59.72994140947689, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4214.7008175, 7,
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
        self.assertEqual(no_flight_time, 13680, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         54360,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo50m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 50 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         58800,
                         "Bad full desat time: %s" % desat)

# ==================================================== 60m tests ==============

class TestDiveTxHypo60m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 46:08', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               22.905063747908372, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               12.301757641394907, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 1348.970145, 7,
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
        self.assertEqual(no_flight_time, 1740, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         33180,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo60m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 94:08', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               60.278437752197064, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               33.57472517960286, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2551.861245, 7,
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
        self.assertEqual(no_flight_time, 6240, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         46440,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo60m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '150:03', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               103.08843644356867, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               56.672056678385296, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3754.752345, 7,
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
        self.assertEqual(no_flight_time, 12660, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         53580,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo60m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 40 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         62880,
                         "Bad full desat time: %s" % desat)

# ==================================================== 70m tests ==============

class TestDiveTxHypo70m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 56:14', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               31.672500800221993, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               17.029865412009602, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 1638.7945107, 7,
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
        self.assertEqual(no_flight_time, 2460, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         36480,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo70m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '117:13', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               80.4635003694687, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               43.63971040870393, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3013.4587107, 7,
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
        self.assertEqual(no_flight_time, 8580, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         49320,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo70m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(70, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         62580,
                         "Bad full desat time: %s" % desat)

# ==================================================== 80m tests ==============

class TestDiveTxHypo80m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 68:05', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               41.6868775987457, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               22.325597177151813, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2029.6502232, 7,
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
        self.assertEqual(no_flight_time, 3360, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         39480,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo80m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '143:27', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               105.09287424293254, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               56.36538206172619, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3576.0875232, 7,
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
        self.assertEqual(no_flight_time, 11880, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         55680,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo80m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(80, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         70740,
                         "Bad full desat time: %s" % desat)

# ==================================================== 90m tests ==============

class TestDiveTxHypo90m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 80:15', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               51.73648632982201, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               27.63851524014282, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2446.2719007, 7,
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
        self.assertEqual(no_flight_time, 4740, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         42180,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo90m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '173:32', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               131.8419065357566, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               69.91549399781893, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4164.4823007, 7,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
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
        self.assertEqual(no_flight_time, 14760, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         63120,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo90m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(90, 30 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         77640,
                         "Bad full desat time: %s" % desat)

# =================================================== 100m tests ==============

class TestDiveTxHypo100m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 94:18', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               63.28263638426435, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               33.74490732986056, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 2888.6595432, 7,
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
        self.assertEqual(no_flight_time, 5880, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         44640,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo100m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '146:42', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               110.08565106336879, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               58.774654565799246, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3833.6512932, 7,
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
                         'Wrong tank status : it should pass the '
                         'remaining gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 12000, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         58260,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo100m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(100, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         68760,
                         "Bad full desat time: %s" % desat)

# =================================================== 110m tests ==============

class TestDiveTxHypo110m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(110, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '109:26', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               76.67705815151193, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               41.11323765553616, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3356.8131507, 7,
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
        self.assertEqual(no_flight_time, 6900, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         47040,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo110m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(110, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '171:31', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               131.03315232201714, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               70.68346358642285, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4482.50895885, 7,
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
                         'Wrong tank status : it should not pass the '
                         'remaining gas rule test (result:%s on %s)'
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
        self.assertEqual(no_flight_time, 14280, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         63840,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo110m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(110, 20 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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
                         'Wrong tank status : it should pass the '
                         'remaining gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         74760,
                         "Bad full desat time: %s" % desat)

# =================================================== 120m tests ==============

class TestDiveTxHypo120m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(120, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '125:57', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               89.80218242979556, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               48.70465080314238, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 3945.550231350001, 7,
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
        self.assertEqual(no_flight_time, 8760, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         52920,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo120m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(120, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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
                         'Wrong tank status : it should pass the '
                         'remaining gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         69000,
                         "Bad full desat time: %s" % desat)

# =================================================== 130m tests ==============

class TestDiveTxHypo130m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(130, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '144:41', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               105.98333411627473, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               59.91029342373505, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 4678.71134085, 7,
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
                         'Wrong tank status : it should pass the '
                         'remaining gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 10980, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         57780,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo130m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(130, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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
                         'Wrong tank status : it should pass the '
                         'remaining gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))

    def test_tank2_cons(self):
        self.assertEqual(self.profile1.tanks[2].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[2].check_rule(),
                         self.profile1.tanks[2].name))

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         73620,
                         "Bad full desat time: %s" % desat)

# =================================================== 140m tests ==============

class TestDiveTxHypo140m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(140, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '164:56', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               123.00215123559246, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               82.33142642254143, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 5492.154545550001, 7,
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
        self.assertEqual(no_flight_time, 13260, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         62640,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo140m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(140, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         78600,
                         "Bad full desat time: %s" % desat)

# =================================================== 150m tests ==============

class TestDiveTxHypo150m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(150, 10 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '188:11', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               141.79347487965896, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               152.93034674675485, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txhypo.used_gas, 6354.160708049999, 7,
                               'bad used gas (%s)'
                               % self.txhypo.used_gas)

    def test_tank_cons_rule_0(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), False,
                         'Wrong tank status : it should not pass the '
                         'remaining gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank_cons_rule_1(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should not pass the '
                         'remaining gas rule test (result:%s on %s)'
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
        self.assertEqual(no_flight_time, 15240, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         66960,
                         "Bad full desat time: %s" % desat)

class TestDiveTxHypo150m15min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(150, 15 * 60, self.txhypo, 0)
        self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                             diveseg1], [self.txtravel, self.txhypo,
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         82320,
                         "Bad full desat time: %s" % desat)

# =================================================== 160m tests ==============

class TestDiveTxHypo160m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)

    def runTest(self):
        try:
            diveseg1 = SegmentDive(160, 10 * 60, self.txhypo, 0)
            self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2,
                                 diveseg1], [self.txtravel,
                                 self.txhypo, self.deco1])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail('should raise UnauthorizedMod')


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
