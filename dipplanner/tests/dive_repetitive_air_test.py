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
"""Test repetitive Dives with air."""
import json
import pkg_resources

from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod

from dipplanner.tests.common import TestDive, TMethodsMixin


class TestDiveAirBase(TestDive):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        # load json results file
        self.results = json.loads(
            pkg_resources.resource_string(
                "dipplanner.tests",
                __name__.split('.')[-1] + '.json').decode('utf-8'))


class TestDiveAir(TestDiveAirBase):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.dive_tank = self.airtank
        self.all_tanks = [self.airtank]
        self.do_repetitive_dive()


# =============================================================================
# ======= S Y S T E M A T I C        T E S T S ================================
# =============================================================================

# AIR =========================================================================
class TestRepetitiveDive1(TestDiveAir, TMethodsMixin):
    """Repetitive dive test 1."""

    params = ((40, 20, 0), (40, 20, 20))
    name = 'repetitive1'


class TestRepetitiveDive2(TestDiveAir, TMethodsMixin):
    """Repetitive dive test 2."""

    params = ((40, 20, 0), (30, 40, 30), (25, 35, 60))
    name = 'repetitive2'


class TestRepetitiveDive3(TestDiveAir, TMethodsMixin):
    """Repetitive dive test 3."""

    params = ((40, 20, 0), (30, 40, 30), (25, 35, 60), (40, 20, 12 * 60))
    name = 'repetitive3'
