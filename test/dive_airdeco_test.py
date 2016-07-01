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
"""Test Dives with air and deco."""
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
        self.air12l = Tank(tank_vol=12.0, tank_pressure=200,
                           tank_rule='10b')
        self.airtank = Tank(tank_vol=18.0, tank_pressure=200,
                            tank_rule='10b')
        self.airtank12 = Tank(tank_vol=12.0, tank_pressure=200,
                              tank_rule='10b')
        self.airdouble = Tank(tank_vol=30.0, tank_pressure=200,
                              tank_rule='10b')  # bi15l 200b
        self.txtank1 = Tank(0.21, 0.30, tank_vol=20.0,
                            tank_pressure=200, tank_rule='10b')
        self.txtanknormodbl = Tank(0.21, 0.30, tank_vol=30.0,
                                   tank_pressure=200, tank_rule='10b')
        self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200,
                          tank_rule='10b')
        self.deco2 = Tank(0.5, 0.0, tank_vol=7.0, tank_pressure=200,
                          tank_rule='10b')
        self.decoo2 = Tank(1.0, 0.0, tank_vol=7.0, tank_pressure=200,
                           tank_rule='10b')


# AIR + DECO Nx80 =============================================================
# ==================================================== 10m tests ==============

class TestDiveAirDecoNx8010m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 10 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 11:00', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.133348222351, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.0722537642857, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas, 339.7312725, 7,
                               'bad used gas (%s)'
                               % self.airtank12.used_gas)

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
        self.assertEqual(no_flight_time, 120, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         7800,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8010m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 20 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 21:00', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

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
        self.assertAlmostEqual(self.airtank12.used_gas, 683.7568725, 7,
                               'bad used gas (%s)'
                               % self.airtank12.used_gas)

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
        self.assertEqual(no_flight_time, 1080, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         16020,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8010m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 30 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 31:43', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               0.21242071169232696, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               0.10277490873015875, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas, 1027.7824725,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         24000,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8010m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 40 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 41:43', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

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
        self.assertAlmostEqual(self.airtank12.used_gas, 1371.8080725,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         32280,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8010m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 50 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 51:43', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

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
        self.assertAlmostEqual(self.airtank12.used_gas, 1715.8336725,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         40440,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8010m60min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 60 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 61:43', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

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
        self.assertAlmostEqual(self.airtank12.used_gas, 2059.8592725,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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
        self.assertEqual(no_flight_time, 60, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         48600,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8010m70min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 70 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         55680,
                         "Bad full desat time: %s" % desat)

# ==================================================== 20m tests ==============

class TestDiveAirDecoNx8020m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 10 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 12:43', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               3.2127113311532223, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               1.6670237705722641, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas, 544.96697445,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         15060,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8020m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 20 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 23:26', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               6.66899215901469, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               3.4643499947438046, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas, 1060.76567445,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         31620,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8020m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 30 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 34:28', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               10.496570342281812, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               5.446659191137561, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas, 1576.56437445,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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
        self.assertEqual(no_flight_time, 720, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         48120,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8020m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 40 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 46:42', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               16.253214686866055, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               8.140859970864614, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas, 2092.36307445,
                               7, 'bad used gas (%s)'
                               % self.airtank12.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         60900,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8020m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 50 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
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

class TestDiveAirDecoNx8030m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 10 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 15:09', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               6.7936390215947835, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               2.6314043714007243, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas, 755.43696195, 7,
                               'bad used gas (%s)'
                               % self.airtank.used_gas)

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
        self.assertEqual(no_flight_time, 120, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         21780,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8030m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 20 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 28:39', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               17.632512091238272, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               7.1314043714006985, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas, 1468.1369130000003, 7,
                               'bad used gas (%s)'
                               % self.airtank.used_gas)

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
        self.assertEqual(no_flight_time, 600, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         45360,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8030m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 44:17', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               31.23016072588735, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               13.886034001030481, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas, 2192.96263575, 7,
                               'bad used gas (%s)'
                               % self.airtank.used_gas)

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
        self.assertEqual(no_flight_time, 1560, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         64320,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8030m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 40 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 62:58', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               46.31049522903472, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               21.270293260290142, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas, 2950.42348815, 7,
                               'bad used gas (%s)'
                               % self.airtank.used_gas)

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
        self.assertEqual(no_flight_time, 2460, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         78660,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8030m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 50 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
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

class TestDiveAirDecoNx8040m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 17:37', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               10.339585073605225, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               3.99598729542606, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas, 999.6237555000001, 7,
                               'bad used gas (%s)'
                               % self.airtank.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         27420,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8040m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 20 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 37:25', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               29.53217156600471, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               12.994236846351944, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas, 1979.9778561000003, 7,
                               'bad used gas (%s)'
                               % self.airtank.used_gas)

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
        self.assertEqual(no_flight_time, 1200, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         58200,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8040m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 61:09', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               52.19868777575691, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               24.727162205027113, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas, 3005.018696250001, 7,
                               'bad used gas (%s)'
                               % self.airtank.used_gas)

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
        self.assertEqual(no_flight_time, 2520, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         79380,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8040m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 40 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
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

class TestDiveAirDecoNx8050m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 10 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 21:13', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               14.395286777547831, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               6.234166771268431, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 1269.9274399500002,
                               7, 'bad used gas (%s)'
                               % self.airdouble.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         32400,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8050m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 20 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 47:34', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               41.368433819105924, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               19.475240723754137, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 2570.642118,
                               7, 'bad used gas (%s)'
                               % self.airdouble.used_gas)

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
        self.assertEqual(no_flight_time, 1860, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         69720,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8050m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 30 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 81:49', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               74.72885607387359, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               35.52806866020751, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 3960.6382561500013,
                               7, 'bad used gas (%s)'
                               % self.airdouble.used_gas)

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
        self.assertEqual(no_flight_time, 4020, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         92580,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8050m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 40 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         '119:09', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               112.03356686942743, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               55.79970608710789, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 5414.702920950001,
                               7, 'bad used gas (%s)'
                               % self.airdouble.used_gas)

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
        self.assertEqual(no_flight_time, 9240, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         108960,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8050m50min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 50 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
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

class TestDiveAirDecoNx8060m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 10 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 24:54', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               17.563839359046515, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               8.76001601293505, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 1571.4821277000005, 7,
                               'bad used gas (%s)'
                               % self.airdouble.used_gas)

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

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         37980,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8060m20min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 20 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 60:21', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               54.796381440990686, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               29.151680123365054, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 3227.1197769000005,
                               7, 'bad used gas (%s)'
                               % self.airdouble.used_gas)

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
        self.assertEqual(no_flight_time, 2520, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         79200,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8060m25min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 25 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 82:47', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               77.28036418765986, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               40.305456926484, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 4117.8769281, 7,
                               'bad used gas (%s)'
                               % self.airdouble.used_gas)

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
        self.assertEqual(no_flight_time, 4200, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         93420,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8060m30min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 30 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         '104:27', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               99.82503972790087, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               53.391405346073505, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas, 5009.309585850001,
                               7, 'bad used gas (%s)'
                               % self.airdouble.used_gas)

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
        self.assertEqual(no_flight_time, 6900, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         103740,
                         "Bad full desat time: %s" % desat)

class TestDiveAirDecoNx8060m40min(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 40 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
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

class TestDiveAirDecoNx8070m10min(TestDive):

    def setUp(self):
        TestDive.setUp(self)

    def runTest(self):
        try:
            diveseg1 = SegmentDive(70, 10 * 60, self.airdouble, 0)
            self.profile1 = Dive([diveseg1], [self.airdouble,
                                 self.deco1])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail('should raise UnauthorizedMod')


# ======================= Multilevel Dive =====================================

class TestDiveMultilevel(TestDive):

    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.airdouble, 0)
        diveseg2 = SegmentDive(50, 12 * 60, self.airdouble, 0)
        diveseg3 = SegmentDive(30, 15 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3],
                             [self.airdouble, self.deco1])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         ' 75:56', 'bad dive runtime ? (%s)'
                         % seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               64.4961716914454, 7, 'bad dive OTU ? (%s)'
                               % self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               29.86079286354883, 7, 'bad dive CNS ? (%s)'
                               % (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,  3723.0441732000004,
                               7, 'bad used gas (%s)'
                               % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(), True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)'
                         % self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time, 3420, 'Bad no flight time: %s'
                         % no_flight_time)

    def test_full_desat(self):
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         88920,
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
