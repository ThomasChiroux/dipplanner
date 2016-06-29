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
"""Test Dives with normoxic trimix."""
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


# TxNormo + DECO Nx80 =========================================================
# ==================================================== 10m tests ==============

class TestDiveTxNormoDecoNx8010m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 10 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 11:00', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.133348222351, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.0722537642857, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns
                               * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               339.7312725, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 420, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8010m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 20 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 21:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.21242071169232696, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.10277490873015875, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns
                               * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               683.7568725, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8010m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 30 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 31:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.21242071169232696, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.10277490873015875, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns
                               * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1027.7824725, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8010m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 40 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 41:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.21242071169232696, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.10277490873015875, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns
                               * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1371.8080725, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8010m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 50 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 51:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.21242071169232696, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.10277490873015875, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns
                               * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1715.8336725, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 240, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8010m60min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 60 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 61:43', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.21242071169232696, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.10277490873015875, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns
                               * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               2059.8592725, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 480, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8010m180min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 180 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))


# ==================================================== 20m tests ==============

class TestDiveTxNormoDecoNx8020m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 10 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 13:26', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               3.326469763155965, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               1.7099640298315233, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               544.96697445, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 0, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8020m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 20 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 23:26', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               6.66899215901469, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               3.4643499947438046, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1060.76567445, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 360, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8020m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 30 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 35:12', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               11.280817165418886, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               5.752214746693103, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1576.56437445, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 900, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8020m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 40 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 47:58', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               17.768659688698744, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               8.726508119012736, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               2092.36307445, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1380, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8020m120min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 120 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))


# ==================================================== 30m tests ==============

class TestDiveTxNormoDecoNx8030m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 10 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 15:09', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               6.7936390215947835, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               2.6314043714007243, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               755.43696195, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 180, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8030m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 20 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 29:17', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               18.520800395905415, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               7.802700667696954, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1469.0272194000001, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 840, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8030m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 30 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 45:59', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               32.834098311034644, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               14.712422889919507, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               2200.97539335, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1620, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8030m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 40 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 64:34', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               47.8432711848202, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               21.43233029732718, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               2959.91203755, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2820, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8030m90min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 90 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))


# ==================================================== 40m tests ==============

class TestDiveTxNormoDecoNx8040m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 18:48', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               10.898067626295214, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               4.21357988801865, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1028.41976745, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 300, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8040m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 20 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 38:46', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               30.903952820428824, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               14.05673684635214, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1988.6159523000001, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1320, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8040m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 30 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 62:33', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               53.66664772382799, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               24.76419924206414, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               3010.298216850001, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2880, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8040m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 40 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 88:38', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               78.16475289122931, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               37.02333666896555, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               4066.9143154500007, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 5640, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8040m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 50 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '115:53', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               103.68441854479023, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               49.79480978592461, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               5131.678733700001, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 7680, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8040m60min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 60 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))


# ==================================================== 50m tests ==============

class TestDiveTxNormoDecoNx8050m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 10 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 22:15', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               15.035300168431299, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               6.644453359231391, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1298.5668114000005, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 420, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8050m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 20 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 49:57', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               43.245552567942504, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               19.875265090225973, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               2587.2323460000002, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 1980, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8050m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 30 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 81:14', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               75.70909008555574, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               36.58452577521722, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               3922.1973601500013, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 5100, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8050m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 40 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '119:09', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               112.65795324809258, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               54.874901018881985, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               5353.1708317500015, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 8460, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8050m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 50 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))


# ==================================================== 60m tests ==============

class TestDiveTxNormoDecoNx8060m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 10 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 26:42', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               18.581097017428778, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               9.296090901823927, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               1630.7244411000004, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 540, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8060m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 20 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 61:35', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               56.14938362042132, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               29.111889675021956, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               3231.6094701000006, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 2880, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8060m25min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 25 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 81:10', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               77.00309590709813, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               40.70039657414481, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               4074.54073305, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 5100, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8060m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 30 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == '104:15', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               99.93118435358029, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               52.78857883535263, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               4963.967500650001, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

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

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 7140, 'Bad no flight time: %s'
                         % no_flight_time)


class TestDiveTxNormoDecoNx8060m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 40 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                             self.deco1])
        self.profile1.do_dive()

    def test_tank0_cons(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[0].check_rule(),
                         self.profile1.tanks[0].name))

    def test_tank1_cons(self):
        self.assertEqual(self.profile1.tanks[1].check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s on %s)'
                         % (self.profile1.tanks[1].check_rule(),
                         self.profile1.tanks[1].name))


# ==================================================== 70m tests ==============

class TestDiveTxNormoDecoNx8070m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)

    def runTest(self):
        try:
            diveseg1 = SegmentDive(70, 10 * 60, self.txtanknormodbl, 0)
            self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                                 self.deco1])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail('should raise UnauthorizedMod')


# ======================== Multilevel Dive ====================================

class TestDiveMultilevel(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.txtanknormodbl, 0)
        diveseg2 = SegmentDive(50, 12 * 60, self.txtanknormodbl, 0)
        diveseg3 = SegmentDive(30, 15 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3],
                             [self.txtanknormodbl, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        assert seconds_to_mmss(self.profile1.run_time) == ' 76:35', \
            'bad dive runtime ? (%s)' \
            % seconds_to_mmss(self.profile1.run_time)

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               66.62197180843947, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               31.534403974660012, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.txtanknormodbl.used_gas,
                               3700.038231, 7, 'bad used gas (%s)'
                               % self.txtanknormodbl.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 4380, 'Bad no flight time: %s'
                         % no_flight_time)


# =============================================================================
# ========================== M A I N ==========================================
# =============================================================================

if __name__ == '__main__':
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
