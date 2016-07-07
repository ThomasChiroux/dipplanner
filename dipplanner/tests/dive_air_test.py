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
# pylint: disable=too-many-public-methods, protected-access, no-self-use
# pylint: disable=too-few-public-methods, duplicate-code, invalid-name
# pylint: disable=too-many-ancestors, attribute-defined-outside-init
"""Test Dives with air."""
import json
import pkg_resources

from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod

from dipplanner.tests.common import TestDive, TMethodsMixin


# ============================================================================
# ======= S Y S T E M A T I C        T E S T S ===============================
# ============================================================================
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

        self.dive_tank = self.airtank12
        self.all_tanks = [self.airtank12]
        self.do_dive()


class TestDiveAirMultilevel(TestDiveAirBase):
    """Multilevel dive test."""

    def setUp(self):
        """Init of multilevel test."""
        super().setUp()

        self.dive_tank = self.airdouble
        self.all_tanks = [self.airdouble]
        self.do_dive()


# AIR =========================================================================
# =============================================s====== 10m tests ==============
class TestDiveAir10m10min(TestDiveAir, TMethodsMixin):
    """Test air 10m 10min."""

    params = ((10, 10), )



class TestDiveAir10m20min(TestDiveAir, TMethodsMixin):
    """Test air 10m 20min."""

    params = ((10, 20), )


class TestDiveAir10m30min(TestDiveAir, TMethodsMixin):
    """Test air 10m 30min."""

    params = ((10, 30), )


class TestDiveAir10m40min(TestDiveAir, TMethodsMixin):
    """Test air 10m 40min."""

    params = ((10, 40), )


class TestDiveAir10m50min(TestDiveAir, TMethodsMixin):
    """Test air 10m 50min."""

    params = ((10, 50), )


class TestDiveAir10m60min(TestDiveAir, TMethodsMixin):
    """Test air 10m 60min."""

    params = ((10, 60), )


class TestDiveAir10m70min(TestDiveAir, TMethodsMixin):
    """Test air 10m 70min."""

    params = ((10, 70), )


# ==================================================== 20m tests ==============
class TestDiveAir20m10min(TestDiveAir, TMethodsMixin):
    """Test air 20m 10min."""

    params = ((20, 10), )

class TestDiveAir20m20min(TestDiveAir, TMethodsMixin):
    """Test air 20m 20min."""

    params = ((20, 20), )

class TestDiveAir20m30min(TestDiveAir, TMethodsMixin):
    """Test air 20m 30min."""

    params = ((20, 30), )

class TestDiveAir20m40min(TestDiveAir, TMethodsMixin):
    """Test air 20m 40min."""

    params = ((20, 40), )

class TestDiveAir20m50min(TestDiveAir, TMethodsMixin):
    """Test air 20m 50min."""

    params = ((20, 50), )


# ==================================================== 30m tests ==============
class TestDiveAir30m10min(TestDiveAir, TMethodsMixin):
    """Test air 30m 10min."""

    params = ((30, 10), )


class TestDiveAir30m20min(TestDiveAir, TMethodsMixin):
    """Test air 30m 20min."""

    params = ((30, 20), )


class TestDiveAir30m30min(TestDiveAir, TMethodsMixin):
    """Test air 30m 30min."""

    params = ((30, 30), )

class TestDiveAir30m40min(TestDiveAir, TMethodsMixin):
    """Test air 30m 40min."""

    params = ((30, 40), )

class TestDiveAir30m50min(TestDiveAir, TMethodsMixin):
    """Test air 30m 50min."""

    params = ((30, 50), )

# ==================================================== 40m tests ==============
class TestDiveAir40m10min(TestDiveAir, TMethodsMixin):
    """Test air 40m 10min."""

    params = ((40, 10), )

class TestDiveAir40m20min(TestDiveAir, TMethodsMixin):
    """Test air 40m 20min."""

    params = ((40, 20), )


class TestDiveAir40m30min(TestDiveAir, TMethodsMixin):
    """Test air 40m 30min."""

    params = ((40, 30), )

class TestDiveAir40m40min(TestDiveAir, TMethodsMixin):
    """Test air 40m 40min."""

    params = ((40, 40), )

class TestDiveAir40m50min(TestDiveAir, TMethodsMixin):
    """Test air 40m 50min."""

    params = ((40, 50), )

# ==================================================== 50m tests ==============
class TestDiveAir50m10min(TestDiveAir, TMethodsMixin):
    """Test air 50m 10min."""

    params = ((50, 10), )

class TestDiveAir50m20min(TestDiveAir, TMethodsMixin):
    """Test air 50m 20min."""

    params = ((50, 20), )

class TestDiveAir50m30min(TestDiveAir, TMethodsMixin):
    """Test air 50m 30min."""

    params = ((50, 30), )

class TestDiveAir50m40min(TestDiveAir, TMethodsMixin):
    """Test air 50m 40min."""

    params = ((50, 40), )


class TestDiveAir50m50min(TestDiveAir, TMethodsMixin):
    """Test air 50m 50min."""

    params = ((50, 50), )


# ==================================================== 60m tests ==============
class TestDiveAir60m10min(TestDiveAir, TMethodsMixin):
    """Test air 60m 10min."""

    params = ((60, 10), )


class TestDiveAir60m20min(TestDiveAir, TMethodsMixin):
    """Test air 60m 20min."""

    params = ((60, 20), )


class TestDiveAir60m25min(TestDiveAir, TMethodsMixin):
    """Test air 60m 25min."""

    params = ((60, 25), )

class TestDiveAir60m30min(TestDiveAir, TMethodsMixin):
    """Test air 60m 30min."""

    params = ((60, 30), )


# ==================================================== 70m tests ==============
class TestDiveAir70m10min(TestDive):
    """Test air 70m 10min."""

    params = ((70, 10), )

    def runTest(self):
        """Run one test."""
        try:
            diveseg1 = SegmentDive(self.params[0][0], self.params[0][1] * 60,
                                   self.airdouble, 0)
            self.profile1 = Dive([diveseg1], [self.airdouble])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")


# ======================= Multilevel Dive =====================================
class TestDiveAirMultilevel1(TestDiveAirMultilevel, TMethodsMixin):
    """Multilevel dive test."""

    params = ((40, 10), (50, 12), (30, 15))
    name = 'multilevel1'
