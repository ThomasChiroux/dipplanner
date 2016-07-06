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
"""Test Dives with air."""
import unittest


from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod

from dipplanner.tests.common import TestDive, TMethodsMixin


# ============================================================================
# ======= S Y S T E M A T I C        T E S T S ===============================
# ============================================================================
class TestDiveAir(TestDive):
    """Class for test air dive."""

    results = {
        # m:time  RT,       OTU, CNS, NoFl,desat,Rem. gas,    gasok
        '10:10': [' 11:00', 0.0, 0.0, 120, 7920, 365.545178, True],
        '10:20': [' 21:00', 0.0, 0.0, 1560, 16140, 709.570777, True],
        '10:30': [' 31:43', 0.0, 0.0, 0, 24240, 1067.720946, True],
        '10:40': [' 41:43', 0.0, 0.0, 0, 32520, 1411.746546, True],
        '10:50': [' 51:43', 0.0, 0.0, 0, 40620, 1755.772146, True],
        '10:60': [' 61:43', 0.0, 0.0, 360, 48780, 2099.797746, True],
        '10:70': [' 71:43', 0.0, 0.0, 720, 55800, 2443.823346, False],

        '20:10': [' 12:43', 3.019300, 1.586703, 0, 15300, 581.551078, True],
        '20:20': [' 23:26', 6.361822, 3.341089, 180, 31920, 1115.142208, True],
        '20:30': [' 34:58', 9.704344, 5.095475, 1020, 48840, 1665.301712, True],
        '20:40': [' 49:50', 13.046867, 6.849861, 1860, 63180, 2259.068210, True],
        '20:50': [' 69:49', 16.389389, 8.604247, 2760, 75240, 2943.784887, False],

        '30:10': [' 15:09', 6.340065, 2.412164, 120, 22200, 831.273785, True],
        '30:20': [' 31:12', 13.705485, 5.189942, 1080, 49020, 1637.315862, True],
        '30:30': [' 57:11', 21.072420, 7.970035, 2520, 71580, 2626.430349, False],
        '30:40': [' 89:11', 28.437840, 10.747813, 4020, 88440, 3726.274559, False],
        '30:50': ['125:09', 35.982045, 13.798738, 6540, 101760, 4925.820774, False],

        '40:10': [' 18:13', 9.000305, 3.434155, 240, 28620, 1097.877183, True],
        '40:20': [' 46:07', 20.032685, 7.687034, 2040, 65220, 2333.040427, False],
        '40:30': [' 90:46', 31.399551, 12.213941, 4320, 90240, 3879.493106, False],
        '40:40': ['142:42', 43.333578, 17.075905, 8580, 108000, 5588.270512, False],
        '40:50': ['196:34', 54.967717, 21.768918, 14940, 120360, 7352.853478, False],

        '50:10': [' 23:17', 11.198793, 4.351139, 420, 35160, 1435.111406, True],
        '50:20': [' 67:19', 26.153779, 10.397083, 3000, 78960, 3185.230514, False],
        '50:30': ['132:24', 42.205359, 16.950032, 7680, 105480, 5372.643731, False],
        '50:40': ['208:15', 59.467531, 24.082781, 16500, 123240, 7800.868502, False],
        '50:50': ['294:21', 76.240844, 31.123310, 26880, 135060, 10430.399268, False],

        '60:10': [' 27:56', 13.044585, 6.181109, 720, 41400, 1769.760218, True],
        '60:20': [' 91:08', 32.396348, 15.577201, 4380, 90600, 4139.966752, False],
        '60:25': ['135:25', 43.292968, 20.782976, 7980, 106560, 5584.935055, False],
        '60:30': ['180:56', 53.843507, 25.942999, 13680, 118080, 7087.413066, False],
    }

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        self.name = '%s:%s' % (self.params[0], self.params[1])
        diveseg1 = SegmentDive(self.params[0], self.params[1] * 60,
                               self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()
        # self.print_details()


# ======================= Multilevel Dive =====================================
class TestDiveMultilevel(TestDive, TMethodsMixin):
    """Multilevel dive test."""

    results = {
        'multilevel1': ['117:28', 37.825321, 14.831368, 6300, 100800, 4900.722629, True],
    }

    def setUp(self):
        """Init of multilevel test."""
        super().setUp()
        self.params = (999, 999)
        self.name = 'multilevel1'

        diveseg1 = SegmentDive(40, 10 * 60, self.airdouble, 0)
        diveseg2 = SegmentDive(50, 12 * 60, self.airdouble, 0)
        diveseg3 = SegmentDive(30, 15 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3], [self.airdouble])
        self.profile1.do_dive()
        # self.print_details()


# AIR =========================================================================
# =============================================s====== 10m tests ==============
class TestDiveAir10m10min(TestDiveAir, TMethodsMixin):
    """Test air 10m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 10)
        super().setUp()


class TestDiveAir10m20min(TestDiveAir, TMethodsMixin):
    """Test air 10m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 20)
        super().setUp()


class TestDiveAir10m30min(TestDiveAir, TMethodsMixin):
    """Test air 10m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 30)
        super().setUp()


class TestDiveAir10m40min(TestDiveAir, TMethodsMixin):
    """Test air 10m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 40)
        super().setUp()


class TestDiveAir10m50min(TestDiveAir, TMethodsMixin):
    """Test air 10m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 50)
        super().setUp()


class TestDiveAir10m60min(TestDiveAir, TMethodsMixin):
    """Test air 10m 60min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 60)
        super().setUp()


class TestDiveAir10m70min(TestDiveAir, TMethodsMixin):
    """Test air 10m 70min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (10, 70)
        super().setUp()


# ==================================================== 20m tests ==============
class TestDiveAir20m10min(TestDiveAir, TMethodsMixin):
    """Test air 20m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 10)
        super().setUp()


class TestDiveAir20m20min(TestDiveAir, TMethodsMixin):
    """Test air 20m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 20)
        super().setUp()


class TestDiveAir20m30min(TestDiveAir, TMethodsMixin):
    """Test air 20m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 30)
        super().setUp()


class TestDiveAir20m40min(TestDiveAir, TMethodsMixin):
    """Test air 20m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 40)
        super().setUp()


class TestDiveAir20m50min(TestDiveAir, TMethodsMixin):
    """Test air 20m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (20, 50)
        super().setUp()


# ==================================================== 30m tests ==============
class TestDiveAir30m10min(TestDiveAir, TMethodsMixin):
    """Test air 30m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 10)
        super().setUp()


class TestDiveAir30m20min(TestDiveAir, TMethodsMixin):
    """Test air 30m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 20)
        super().setUp()


class TestDiveAir30m30min(TestDiveAir, TMethodsMixin):
    """Test air 30m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 30)
        super().setUp()


class TestDiveAir30m40min(TestDiveAir, TMethodsMixin):
    """Test air 30m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 40)
        super().setUp()


class TestDiveAir30m50min(TestDiveAir, TMethodsMixin):
    """Test air 30m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (30, 50)
        super().setUp()


# ==================================================== 40m tests ==============
class TestDiveAir40m10min(TestDiveAir, TMethodsMixin):
    """Test air 40m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 10)
        super().setUp()


class TestDiveAir40m20min(TestDiveAir, TMethodsMixin):
    """Test air 40m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 20)
        super().setUp()


class TestDiveAir40m30min(TestDiveAir, TMethodsMixin):
    """Test air 40m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 30)
        super().setUp()


class TestDiveAir40m40min(TestDiveAir, TMethodsMixin):
    """Test air 40m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 40)
        super().setUp()


class TestDiveAir40m50min(TestDiveAir, TMethodsMixin):
    """Test air 40m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (40, 50)
        super().setUp()


# ==================================================== 50m tests ==============
class TestDiveAir50m10min(TestDiveAir, TMethodsMixin):
    """Test air 50m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 10)
        super().setUp()


class TestDiveAir50m20min(TestDiveAir, TMethodsMixin):
    """Test air 50m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 20)
        super().setUp()


class TestDiveAir50m30min(TestDiveAir, TMethodsMixin):
    """Test air 50m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 30)
        super().setUp()


class TestDiveAir50m40min(TestDiveAir, TMethodsMixin):
    """Test air 50m 40min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 40)
        super().setUp()


class TestDiveAir50m50min(TestDiveAir, TMethodsMixin):
    """Test air 50m 50min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (50, 50)
        super().setUp()


# ==================================================== 60m tests ==============
class TestDiveAir60m10min(TestDiveAir, TMethodsMixin):
    """Test air 60m 10min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 10)
        super().setUp()


class TestDiveAir60m20min(TestDiveAir, TMethodsMixin):
    """Test air 60m 20min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 20)
        super().setUp()


class TestDiveAir60m25min(TestDiveAir, TMethodsMixin):
    """Test air 60m 25min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 25)
        super().setUp()


class TestDiveAir60m30min(TestDiveAir, TMethodsMixin):
    """Test air 60m 30min."""

    def setUp(self):
        """Init of the tests."""
        self.params = (60, 30)
        super().setUp()


# ==================================================== 70m tests ==============
class TestDiveAir70m10min(TestDive):
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
    """Direct acces with python."""
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('tests',
                        metavar='TestName',
                        type=str,
                        nargs='*',
                        help='name of the tests to run (separated by space)'
                        ' [optionnal]')
    args = parser.parse_args()
    if args.tests:
        suite = unittest.TestLoader().loadTestsFromNames(args.tests,
                                                         sys.modules[__name__])
    else:
        suite = unittest.findTestCases(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
