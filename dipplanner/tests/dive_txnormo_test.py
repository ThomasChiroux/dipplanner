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


class TestDiveTxNormoDecoNx80(TestDive):
    """Class for test air dive."""

    results = {
        # m:time  RT,       OTU, CNS, NoFl,desat,Rem. gas, gasok, gas1, gas1ok
        '10:10': [' 11:00', 0.133348, 0.072254, 600, 5040, 25.813905, True, 339.731273, True],
        '10:20': [' 21:43', 0.212421, 0.102775, 0, 10260, 39.938473, True, 683.756872, True],
        '10:30': [' 31:43', 0.212421, 0.102775, 0, 15540, 39.938473, True, 1027.782473, True],
        '10:40': [' 41:43', 0.212421, 0.102775, 120, 20760, 39.938473, True, 1371.808072, True],
        '10:50': [' 51:43', 0.212421, 0.102775, 420, 25140, 39.938473, True, 1715.833672, True],
        '10:60': [' 61:43', 0.212421, 0.102775, 720, 28680, 39.938473, True, 2059.859273, True],
        '10:70': [' 71:43', 0.212421, 0.102775, 1020, 31620, 39.938473, True, 2403.884872, True],

        '20:10': [' 13:26', 3.326470, 1.709964, 0, 7380, 54.376533, True, 544.966974, True],
        '20:20': [' 23:26', 6.668992, 3.464350, 420, 15420, 54.376533, True, 1060.765674, True],
        '20:30': [' 35:32', 11.637293, 5.891104, 1140, 23160, 97.688715, True, 1576.564374, True],
        '20:40': [' 48:39', 18.576637, 9.039008, 1680, 28800, 149.406947, True, 2092.363074, True],
        '20:50': [' 62:05', 26.202040, 12.443857, 2340, 33000, 209.401213, True, 2608.161774, True],

        '30:10': [' 15:09', 6.793639, 2.631404, 180, 10560, 75.836823, True, 755.436962, True],
        '30:20': [' 29:39', 18.912924, 7.955478, 1020, 20700, 142.167097, True, 1469.027219, True],
        '30:30': [' 47:03', 34.077757, 15.193904, 1860, 29460, 250.711826, True, 2200.975393, True],
        '30:40': [' 66:06', 49.755754, 22.476312, 3060, 38580, 365.653188, True, 2959.912038, True],
        '30:50': [' 85:45', 65.787192, 30.860571, 4620, 48240, 482.167437, True, 3743.001438, True],

        '40:10': [' 18:48', 10.898068, 4.213580, 360, 13680, 96.389724, True, 1028.419767, True],
        '40:20': [' 39:30', 31.797569, 14.401644, 1500, 27660, 232.386383, True, 1988.615952, True],
        '40:30': [' 64:07', 55.633750, 25.854477, 3120, 41220, 405.354444, True, 3010.298217, True],
        '40:40': [' 91:34', 80.690974, 38.291855, 5520, 54360, 588.100180, True, 4092.286356, True],
        '40:50': ['118:53', 106.308251, 51.304069, 8160, 63540, 783.923231, True, 5160.530601, True],

        '50:10': [' 22:14', 15.029240, 6.635194, 540, 16500, 122.525275, True, 1297.879155, True],
        '50:20': [' 51:05', 44.718384, 20.671561, 2220, 35220, 325.622954, True, 2587.232346, True],
        '50:30': [' 83:45', 78.131576, 37.890081, 4980, 53340, 567.483269, True, 3938.262729, True],
        '50:40': ['122:44', 115.370323, 56.291568, 8820, 66840, 850.172106, True, 5398.308106, False],
        '50:50': ['161:19', 152.044072, 74.944524, 13140, 76320, 1132.086813, True, 6860.856836, False],

        '60:10': [' 26:41', 18.568976, 9.277572, 720, 18900, 145.728323, True, 1629.794282, True],
        '60:20': [' 63:11', 58.171105, 30.248464, 3060, 43020, 425.133215, True, 3231.609470, True],
        '60:25': [' 83:40', 79.402428, 42.003637, 4980, 54120, 578.456070, True, 4091.293758, True],
        '60:30': ['107:25', 102.727521, 54.381171, 7560, 63420, 752.354292, True, 4995.630620, True],
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
                               self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                                          self.deco1])
        self.profile1.do_dive()
        self.print_details()


# ======================= Multilevel Dive =====================================
# ======================= Multilevel Dive =====================================
class TestDiveMultilevel(TestDive, TMethodsMixinDeco):
    """Multilevel dive test."""

    results = {
        'multilevel1': [' 78:35', 68.622390, 32.661719, 4380, 49260, 495.629280, True, 3712.057367, True],
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

        diveseg1 = SegmentDive(40, 10 * 60, self.txtanknormodbl, 0)
        diveseg2 = SegmentDive(50, 12 * 60, self.txtanknormodbl, 0)
        diveseg3 = SegmentDive(30, 15 * 60, self.txtanknormodbl, 0)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3],
                             [self.txtanknormodbl, self.deco1])
        self.profile1.do_dive()
        # self.print_details()


# AIR + DECO Nx80 =============================================================
# ==================================================== 10m tests ==============
class TestDiveTxNormoDecoNx8010m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 10m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 10)
        super().setUp()


class TestDiveTxNormoDecoNx8010m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 10m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 20)
        super().setUp()


class TestDiveTxNormoDecoNx8010m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 10m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 30)
        super().setUp()


class TestDiveTxNormoDecoNx8010m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 10m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 40)
        super().setUp()


class TestDiveTxNormoDecoNx8010m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 10m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 50)
        super().setUp()


class TestDiveTxNormoDecoNx8010m60min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 10m 60min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 60)
        super().setUp()


class TestDiveTxNormoDecoNx8010m70min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 10m 70min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 70)
        super().setUp()


# ==================================================== 20m tests ==============
class TestDiveTxNormoDecoNx8020m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 20m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 10)
        super().setUp()


class TestDiveTxNormoDecoNx8020m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 20m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 20)
        super().setUp()


class TestDiveTxNormoDecoNx8020m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 20m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 30)
        super().setUp()


class TestDiveTxNormoDecoNx8020m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 20m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 40)
        super().setUp()


class TestDiveTxNormoDecoNx8020m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 20m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 50)
        super().setUp()


# ==================================================== 30m tests ==============
class TestDiveTxNormoDecoNx8030m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 30m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 10)
        super().setUp()


class TestDiveTxNormoDecoNx8030m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 30m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 20)
        super().setUp()


class TestDiveTxNormoDecoNx8030m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 30m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 30)
        super().setUp()


class TestDiveTxNormoDecoNx8030m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 30m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 40)
        super().setUp()


class TestDiveTxNormoDecoNx8030m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 30m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 50)
        super().setUp()


# ==================================================== 40m tests ==============
class TestDiveTxNormoDecoNx8040m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 40m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 10)
        super().setUp()


class TestDiveTxNormoDecoNx8040m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 40m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 20)
        super().setUp()


class TestDiveTxNormoDecoNx8040m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 40m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 30)
        super().setUp()


class TestDiveTxNormoDecoNx8040m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 40m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 40)
        super().setUp()


class TestDiveTxNormoDecoNx8040m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 40m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 50)
        super().setUp()


# ==================================================== 50m tests ==============
class TestDiveTxNormoDecoNx8050m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 50m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 10)
        super().setUp()


class TestDiveTxNormoDecoNx8050m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 50m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 20)
        super().setUp()


class TestDiveTxNormoDecoNx8050m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 50m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 30)
        super().setUp()


class TestDiveTxNormoDecoNx8050m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 50m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 40)
        super().setUp()


class TestDiveTxNormoDecoNx8050m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 50m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 50)
        super().setUp()


# ==================================================== 60m tests ==============
class TestDiveTxNormoDecoNx8060m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 60m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 10)
        super().setUp()


class TestDiveTxNormoDecoNx8060m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 60m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 20)
        super().setUp()


class TestDiveTxNormoDecoNx8060m25min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 60m 25min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 25)
        super().setUp()


class TestDiveTxNormoDecoNx8060m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test air 60m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 30)
        super().setUp()


# ==================================================== 70m tests ==============
class TestDiveTxNormoDecoNx8070m10min(TestDive):
    """Test air 70m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (70, 10)
        super().setUp()

    def runTest(self):
        """Run one test."""
        try:
            diveseg1 = SegmentDive(self.params[0], self.params[1] * 60,
                                   self.txtanknormodbl, 0)
            self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                                              self.deco1])
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
