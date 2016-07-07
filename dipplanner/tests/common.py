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
"""Common methods for tests."""
import unittest

# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.tank import Tank
from dipplanner.tools import seconds_to_mmss
from dipplanner import settings


class TestDive(unittest.TestCase):
    """Generic Test Dive class."""

    def setUp(self):
        """Init of the tests."""
        # temporary hack (tests):
        super().setUp()
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        self.air12l = Tank(tank_vol=12.0,
                           tank_pressure=200,
                           tank_rule="10b")
        self.airtank = Tank(tank_vol=18.0,
                            tank_pressure=200,
                            tank_rule="10b")
        self.airtank12 = Tank(tank_vol=12.0,
                              tank_pressure=200,
                              tank_rule="10b")
        self.airdouble = Tank(tank_vol=30.0,
                              tank_pressure=200,
                              tank_rule="10b")  # bi15l 200b
        self.txtank1 = Tank(0.21,
                            0.30,
                            tank_vol=20.0,
                            tank_pressure=200,
                            tank_rule="10b")
        self.txtanknormodbl = Tank(0.21,
                                   0.30,
                                   tank_vol=30.0,
                                   tank_pressure=200,
                                   tank_rule="10b")

        self.txhypo = Tank(0.10, 0.50,
                           tank_vol=30.0, tank_pressure=200)  # 2x 15l

        self.txtravel = Tank(0.21, 0.30, tank_vol=24.0,
                             tank_pressure=200)  # 2x S80


        self.ccair = Tank(tank_vol=3.0, tank_pressure=200, tank_rule='10b')
        self.cctxhypo = Tank(0.10, 0.50, tank_vol=3.0, tank_pressure=200,
                           tank_rule='10b')
        self.setpoint = 1.2

        self.deco1 = Tank(0.8,
                          0.0,
                          tank_vol=7.0,
                          tank_pressure=200,
                          tank_rule="10b")
        self.deco2 = Tank(0.5,
                          0.0,
                          tank_vol=7.0,
                          tank_pressure=200,
                          tank_rule="10b")
        self.decoo2 = Tank(1.0,
                           0.0,
                           tank_vol=7.0,
                           tank_pressure=200,
                           tank_rule="10b")

        self.setpoint = 0.0
        self.dive_segs = []

    def do_dive(self):
        """do the actual dive.

        self.params is in the form ((depth, time), (depth, time))
        each couple of depth, time is a segment of the same dive.
        """
        if not hasattr(self, 'name'):
            self.name = '%s:%s' % (self.params[0][0], self.params[0][1])

        for param in self.params:
            self.dive_segs.append(SegmentDive(param[0], param[1] * 60,
                                  self.dive_tank, self.setpoint))
        self.profile1 = Dive(self.dive_segs, self.all_tanks)
        self.profile1.do_dive()
        # self.write_details()

    def do_repetitive_dive(self):
        """do the actual dive.

        self.params is in the form:
            ((depth, time, interval), (depth, time, interval))
        each couple of depth, time, interval is a full dive at the given depth
        interval is done before the dive.
        """
        if not hasattr(self, 'name'):
            self.name = '%s:%s' % (self.params[0][0], self.params[0][1])
        self.profiles = []  # repetive dive profiles.
        for param in self.params:
            if len(self.profiles) > 0:
                self.profiles.append(
                    Dive([SegmentDive(param[0], param[1] * 60,
                                      self.dive_tank, self.setpoint)],
                         self.all_tanks,
                         self.profiles[-1]))
                self.profiles[-1].do_surface_interval(param[2] * 60)
            else:
                self.profiles.append(
                    Dive([SegmentDive(param[0], param[1] * 60,
                                      self.dive_tank, self.setpoint)],
                         self.all_tanks))
            self.profiles[-1].do_dive()

        self.profile1 = self.profiles[-1]  # save last dive
        # self.write_details()

    def tearDown(self):
        """After tests."""
        settings.SURFACE_TEMP = 20
        settings.RUN_TIME = True

    @property
    def details(self):
        """Output details of the dive.

        :returns: string
        :rtype: str
        """
        return '"%s": ["%s", %f, %f, %d, %d, %f, %s], ' % (
            self.name,
            seconds_to_mmss(self.profile1.run_time),
            self.profile1.model.ox_tox.otu,
            self.profile1.model.ox_tox.cns * 100,
            self.profile1.no_flight_time(),
            self.profile1.full_desat_time(),
            self.profile1.tanks[0].used_gas,
            str(self.profile1.tanks[0].check_rule()).lower())

    def print_details(self):
        """print detailed results."""
        print(self.details)

    def write_details(self):
        """write in /tmp/details.txt the detailed results."""
        with open('/tmp/details.txt', 'a') as myfile:
            myfile.write(self.details + '\n')


class TMethodsMixin():
    """The real tests."""

    def test_rt(self):
        """Check runtime."""
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         self.results[self.name][0],
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        """Check OTU."""
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               self.results[self.name][1],
                               5,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        """Check CNS."""
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               self.results[self.name][2],
                               5,
                               "bad dive CNS ? (%s)" %
                               self.profile1.model.ox_tox.cns * 100)

    def test_no_flight(self):
        """Check no flight time."""
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         self.results[self.name][3],
                         "Bad no flight time: %s" % no_flight_time)

    def test_full_desat(self):
        """Check full desat time."""
        desat = self.profile1.full_desat_time()
        self.assertEqual(desat,
                         self.results[self.name][4],
                         "Bad full desat time: %s" % desat)

    def test_tank_cons(self):
        """Check consumption of the Tank 0."""
        self.assertAlmostEqual(
            self.profile1.tanks[0].used_gas,
            self.results[self.name][5],
            5,
            "bad used gas (%s)" % self.profile1.tanks[0].used_gas)

    def test_tank_cons_rule(self):
        """Check Tank 0 Rule."""
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         self.results[self.name][6],
                         'Wrong tank status : it should pass the remaining'
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())


class TMethodsMixinDeco(TMethodsMixin):
    """Add tank test for the deco tank."""

    def test_tank_cons_1(self):
        """Check consumption of the Tank 1."""
        self.assertAlmostEqual(
            self.profile1.tanks[1].used_gas,
            self.results[self.name][7],
            5,
            "bad used gas (%s)" % self.profile1.tanks[1].used_gas)

    def test_tank_cons_rule_1(self):
        """Check Tank 1 Rule."""
        self.assertEqual(self.profile1.tanks[1].check_rule(),
                         self.results[self.name][8],
                         'Wrong tank status : it should pass the remaining'
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[1].check_rule())


class TMethodsMixinDecoTravel(TMethodsMixinDeco):
    """Add tank test for the travel tank."""

    def test_tank_cons_2(self):
        """Check consumption of the Tank 2."""
        self.assertAlmostEqual(
            self.profile1.tanks[2].used_gas,
            self.results[self.name][9],
            5,
            "bad used gas (%s)" % self.profile1.tanks[2].used_gas)

    def test_tank_cons_rule_2(self):
        """Check Tank 2 Rule."""
        self.assertEqual(self.profile1.tanks[2].check_rule(),
                         self.results[self.name][10],
                         'Wrong tank status : it should pass the remaining'
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[2].check_rule())
