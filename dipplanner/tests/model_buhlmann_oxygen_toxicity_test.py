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
"""Test for oxygen toxicity class."""
import unittest
# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.model.buhlmann.oxygen_toxicity import OxTox
from dipplanner import settings


class TestModelBuhlmannOxTox(unittest.TestCase):
    def setUp(self):
        # temporary hack (tests):
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        self.ox1 = OxTox()
        self.ox2 = OxTox()


class TestModelBuhlmannOxToxCns(TestModelBuhlmannOxTox):
    def runTest(self):
        self.assertEqual(self.ox1.cns, 0.0,
                         "bad cns value : %s" % self.ox1.cns)


class TestModelBuhlmannOxToxOtu(TestModelBuhlmannOxTox):
    def runTest(self):
        self.assertEqual(self.ox1.otu, 0.0,
                         "bad otu value : %s" % self.ox1.otu)


class TestModelBuhlmannOxToxMaxOx(TestModelBuhlmannOxTox):
    def runTest(self):
        self.assertEqual(self.ox1.max_ox, 0.0,
                         "bad max_ox value : %s" % self.ox1.max_ox)


class TestModelBuhlmannOxToxCns2(TestModelBuhlmannOxTox):
    def runTest(self):
        self.ox1.add_o2(10 * 60, 1.3)
        self.assertEqual(round(self.ox1.cns, 13), 0.0555555555556,
                         "bad cns value : %s" % self.ox1.cns)


class TestModelBuhlmannOxToxOtu2(TestModelBuhlmannOxTox):
    def runTest(self):
        self.ox1.add_o2(10 * 60, 1.3)
        self.assertEqual(round(self.ox1.otu, 10), 14.7944872366,
                         "bad otu value : %s" % self.ox1.otu)


class TestModelBuhlmannOxToxCns2(TestModelBuhlmannOxTox):
    def runTest(self):
        self.ox1.add_o2(10 * 60, 1.3)
        self.ox1.remove_o2(4 * 60 * 60)
        self.assertEqual(round(self.ox1.cns, 14), 0.00874945594818,
                         "bad cns value : %s" % self.ox1.cns)


class TestModelBuhlmannOxToxOtu3(TestModelBuhlmannOxTox):
    def runTest(self):
        self.ox1.add_o2(10 * 60, 1.3)
        self.ox1.remove_o2(4 * 60 * 60)
        self.assertEqual(round(self.ox1.otu, 10), 14.7944872366,
                         "bad otu value : %s" % self.ox1.otu)


class TestModelBuhlmannOxToxCns3(TestModelBuhlmannOxTox):
    def runTest(self):
        self.ox1.add_o2(10 * 60, 1.3)
        self.ox1.remove_o2(25 * 60 * 60)
        self.assertEqual(round(self.ox1.cns, 7), 0.0000005,
                         "bad cns value : %s" % round(self.ox1.cns, 7))


class TestModelBuhlmannOxToxOtu4(TestModelBuhlmannOxTox):
    def runTest(self):
        self.ox1.add_o2(10 * 60, 1.3)
        self.ox1.remove_o2(25 * 60 * 60)
        self.assertEqual(round(self.ox1.otu, 11), 0.0,
                         "bad otu value : %s" % self.ox1.otu)
