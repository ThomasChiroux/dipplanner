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


from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner.tools import seconds_to_mmss

from dipplanner.tests.common import TestDive, TMethodsMixinDeco


class TestDiveAirDecoNx80(TestDive):
    """Class for test air dive."""

    results = {
        # m:time  RT,       OTU, CNS, NoFl,desat,Rem. gas, gasok, gas1, gas1ok
        '10:10': [' 11:00', 0.133348, 0.072254, 120, 7800, 25.813905, True, 339.731273, True],
        '10:20': [' 21:00', 0.133348, 0.072254, 1500, 16020, 25.813905, True, 683.756872, True],
        '10:30': [' 31:43', 0.212421, 0.102775, 0, 24000, 39.938473, True, 1027.782473, True],
        '10:40': [' 41:43', 0.212421, 0.102775, 0, 32280, 39.938473, True, 1371.808072, True],
        '10:50': [' 51:43', 0.212421, 0.102775, 0, 40440, 39.938473, True, 1715.833672, True],
        '10:60': [' 61:43', 0.212421, 0.102775, 360, 48600, 39.938473, True, 2059.859273, True],
        '10:70': [' 71:43', 0.212421, 0.102775, 720, 55680, 39.938473, True, 2403.884872, False],

        '20:10': [' 12:43', 3.212711, 1.667024, 0, 15060, 36.584104, True, 544.966974, True],
        '20:20': [' 23:26', 6.668992, 3.464350, 180, 31620, 54.376533, True, 1060.765674, True],
        '20:30': [' 34:28', 10.496570, 5.446659, 1020, 48120, 80.839064, True, 1576.564374, True],
        '20:40': [' 46:42', 16.253215, 8.140860, 1740, 60900, 116.360524, True, 2092.363074, True],
        '20:50': [' 60:28', 24.164326, 11.659135, 2400, 70500, 180.953422, True, 2608.161774, False],

        '30:10': [' 15:09', 6.793639, 2.631404, 120, 21780, 75.836823, True, 755.436962, True],
        '30:20': [' 28:39', 17.632512, 7.131404, 900, 45360, 124.532694, True, 1468.136913, True],
        '30:30': [' 45:05', 32.085703, 14.219367, 1920, 63960, 222.383594, True, 2192.962636, True],
        '30:40': [' 64:51', 48.594790, 22.152238, 3000, 78000, 349.636601, True, 2950.423488, False],
        '30:50': [' 86:04', 65.695588, 30.457793, 4260, 89520, 481.155879, True, 3751.985901, False],

        '40:10': [' 17:33', 10.242556, 3.958950, 240, 27420, 87.176763, True, 999.623756, True],
        '40:20': [' 37:25', 29.532172, 12.994237, 1680, 58200, 201.021785, True, 1979.977856, True],
        '40:30': [' 63:02', 54.515149, 25.620681, 3060, 78720, 389.822864, True, 3005.018696, False],
        '40:40': [' 91:26', 80.916287, 38.922459, 5100, 94560, 588.171426, True, 4098.232760, False],
        '40:50': ['120:22', 107.516121, 53.245102, 7920, 105780, 793.626743, True, 5205.602174, False],

        '50:10': [' 21:36', 14.561924, 6.227787, 300, 31860, 116.473316, True, 1288.530938, True],
        '50:20': [' 49:03', 42.969754, 20.102434, 2340, 68880, 302.376669, True, 2566.536952, False],
        '50:30': [' 84:36', 78.516093, 37.977143, 4680, 91800, 570.902471, True, 3960.638256, False],
        '50:40': ['124:12', 116.938661, 58.799706, 8940, 108480, 860.577279, True, 5451.811741, False],
        '50:50': ['166:14', 154.131598, 77.675884, 15180, 120480, 1142.793423, True, 7022.514087, False],

        '60:10': [' 25:06', 17.703425, 8.654978, 480, 37140, 133.842750, True, 1585.764885, True],
        '60:20': [' 62:09', 57.005878, 29.990886, 3060, 78480, 410.148959, True, 3224.026169, False],
        '60:25': [' 85:33', 81.055882, 42.775364, 4800, 92700, 590.641388, True, 4117.876928, False],
        '60:30': ['109:31', 104.776035, 56.416868, 7080, 103200, 771.681141, True, 5045.366995, False],
    }

    def print_details(self):
        """print detailed results."""
        print("['%s', %f, %f, %d, %d, %f, %s, %f, %s], " % (
              seconds_to_mmss(self.profile1.run_time),
              self.profile1.model.ox_tox.otu,
              self.profile1.model.ox_tox.cns * 100,
              self.profile1.no_flight_time(),
              self.profile1.full_desat_time(),
              self.profile1.tanks[0].used_gas,
              self.profile1.tanks[0].check_rule(),
              self.profile1.tanks[1].used_gas,
              self.profile1.tanks[1].check_rule()))

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        self.name = '%s:%s' % (self.params[0], self.params[1])
        diveseg1 = SegmentDive(self.params[0], self.params[1] * 60,
                               self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
        self.profile1.do_dive()
        # self.print_details()


# ======================= Multilevel Dive =====================================
# ======================= Multilevel Dive =====================================
class TestDiveMultilevel(TestDive, TMethodsMixinDeco):
    """Multilevel dive test."""

    results = {
        'multilevel1': [' 78:42', 68.185237, 32.018200, 4020, 88080, 489.759198, True, 3723.044173, True],
    }

    def print_details(self):
        """print detailed results."""
        print("['%s', %f, %f, %d, %d, %f, %s, %f, %s], " % (
              seconds_to_mmss(self.profile1.run_time),
              self.profile1.model.ox_tox.otu,
              self.profile1.model.ox_tox.cns * 100,
              self.profile1.no_flight_time(),
              self.profile1.full_desat_time(),
              self.profile1.tanks[0].used_gas,
              self.profile1.tanks[0].check_rule(),
              self.profile1.tanks[1].used_gas,
              self.profile1.tanks[1].check_rule()))

    def setUp(self):
        """Init of multilevel test."""
        super().setUp()
        self.params = (999, 999)
        self.name = 'multilevel1'

        diveseg1 = SegmentDive(40, 10 * 60, self.airdouble, 0)
        diveseg2 = SegmentDive(50, 12 * 60, self.airdouble, 0)
        diveseg3 = SegmentDive(30, 15 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3],
                             [self.airdouble, self.deco1])
        self.profile1.do_dive()
        # self.print_details()


# AIR + DECO Nx80 =============================================================
# ==================================================== 10m tests ==============
class TestDiveAirDecoNx8010m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 10)
        super().setUp()


class TestDiveAirDecoNx8010m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 20)
        super().setUp()


class TestDiveAirDecoNx8010m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 30)
        super().setUp()


class TestDiveAirDecoNx8010m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 40)
        super().setUp()


class TestDiveAirDecoNx8010m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 50)
        super().setUp()


class TestDiveAirDecoNx8010m60min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 60min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 60)
        super().setUp()


class TestDiveAirDecoNx8010m70min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 70min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 70)
        super().setUp()


# ==================================================== 20m tests ==============
class TestDiveAirDecoNx8020m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 10)
        super().setUp()


class TestDiveAirDecoNx8020m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 20)
        super().setUp()


class TestDiveAirDecoNx8020m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 30)
        super().setUp()


class TestDiveAirDecoNx8020m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 40)
        super().setUp()


class TestDiveAirDecoNx8020m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 50)
        super().setUp()


# ==================================================== 30m tests ==============
class TestDiveAirDecoNx8030m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 10)
        super().setUp()


class TestDiveAirDecoNx8030m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 20)
        super().setUp()


class TestDiveAirDecoNx8030m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 30)
        super().setUp()


class TestDiveAirDecoNx8030m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 40)
        super().setUp()


class TestDiveAirDecoNx8030m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 50)
        super().setUp()


# ==================================================== 40m tests ==============
class TestDiveAirDecoNx8040m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 10)
        super().setUp()


class TestDiveAirDecoNx8040m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 20)
        super().setUp()


class TestDiveAirDecoNx8040m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 30)
        super().setUp()


class TestDiveAirDecoNx8040m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 40)
        super().setUp()


class TestDiveAirDecoNx8040m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 50)
        super().setUp()


# ==================================================== 50m tests ==============
class TestDiveAirDecoNx8050m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 10)
        super().setUp()


class TestDiveAirDecoNx8050m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 20)
        super().setUp()


class TestDiveAirDecoNx8050m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 30)
        super().setUp()


class TestDiveAirDecoNx8050m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 40)
        super().setUp()


class TestDiveAirDecoNx8050m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 50)
        super().setUp()


# ==================================================== 60m tests ==============
class TestDiveAirDecoNx8060m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 10)
        super().setUp()


class TestDiveAirDecoNx8060m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 20)
        super().setUp()


class TestDiveAirDecoNx8060m25min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 25min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 25)
        super().setUp()


class TestDiveAirDecoNx8060m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 30)
        super().setUp()


# ==================================================== 70m tests ==============
class TestDiveAirDecoNx8070m10min(TestDive):
    """Test air 70m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (70, 10)
        super().setUp()

    def runTest(self):
        """Run one test."""
        try:
            diveseg1 = SegmentDive(self.params[0], self.params[1] * 60,
                                   self.airdouble, 0)
            self.profile1 = Dive([diveseg1], [self.airdouble])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")


# =============================================================================
# ========================= M A I N ===========================================
# =============================================================================
def main():
    """Direct api using python interpreter."""
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
