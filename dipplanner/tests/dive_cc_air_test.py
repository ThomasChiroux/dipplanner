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
import json
import pkg_resources

from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner import settings

from dipplanner.tests.common import TestDive, TMethodsMixin


# ============================================================================
# ======= S Y S T E M A T I C        T E S T S ===============================
# ============================================================================
class TestDiveCCAirBase(TestDive):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        # load json results file
        self.results = json.loads(
            pkg_resources.resource_string(
                "dipplanner.tests",
                __name__.split('.')[-1] + '.json').decode('utf-8'))


class TestDiveCCAir(TestDiveCCAirBase):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        settings.RUN_TIME = False
        self.setpoint = 1.2
        self.dive_tank = self.ccair
        self.all_tanks = [self.ccair]
        self.do_dive()


# AIR =========================================================================
# =============================================s====== 10m tests ==============
class TestDiveCCAir10m10min(TestDiveCCAir, TMethodsMixin):
    """Test air 10m 10min."""

    params = ((10, 10), )



class TestDiveCCAir10m20min(TestDiveCCAir, TMethodsMixin):
    """Test air 10m 20min."""

    params = ((10, 20), )


class TestDiveCCAir10m30min(TestDiveCCAir, TMethodsMixin):
    """Test air 10m 30min."""

    params = ((10, 30), )


class TestDiveCCAir10m40min(TestDiveCCAir, TMethodsMixin):
    """Test air 10m 40min."""

    params = ((10, 40), )


class TestDiveCCAir10m50min(TestDiveCCAir, TMethodsMixin):
    """Test air 10m 50min."""

    params = ((10, 50), )


class TestDiveCCAir10m60min(TestDiveCCAir, TMethodsMixin):
    """Test air 10m 60min."""

    params = ((10, 60), )


class TestDiveCCAir10m70min(TestDiveCCAir, TMethodsMixin):
    """Test air 10m 70min."""

    params = ((10, 70), )


# ==================================================== 20m tests ==============
class TestDiveCCAir20m10min(TestDiveCCAir, TMethodsMixin):
    """Test air 20m 10min."""

    params = ((20, 10), )

class TestDiveCCAir20m20min(TestDiveCCAir, TMethodsMixin):
    """Test air 20m 20min."""

    params = ((20, 20), )

class TestDiveCCAir20m30min(TestDiveCCAir, TMethodsMixin):
    """Test air 20m 30min."""

    params = ((20, 30), )

class TestDiveCCAir20m40min(TestDiveCCAir, TMethodsMixin):
    """Test air 20m 40min."""

    params = ((20, 40), )

class TestDiveCCAir20m50min(TestDiveCCAir, TMethodsMixin):
    """Test air 20m 50min."""

    params = ((20, 50), )


# ==================================================== 30m tests ==============
class TestDiveCCAir30m10min(TestDiveCCAir, TMethodsMixin):
    """Test air 30m 10min."""

    params = ((30, 10), )


class TestDiveCCAir30m20min(TestDiveCCAir, TMethodsMixin):
    """Test air 30m 20min."""

    params = ((30, 20), )


class TestDiveCCAir30m30min(TestDiveCCAir, TMethodsMixin):
    """Test air 30m 30min."""

    params = ((30, 30), )

class TestDiveCCAir30m40min(TestDiveCCAir, TMethodsMixin):
    """Test air 30m 40min."""

    params = ((30, 40), )

class TestDiveCCAir30m50min(TestDiveCCAir, TMethodsMixin):
    """Test air 30m 50min."""

    params = ((30, 50), )

# ==================================================== 40m tests ==============
class TestDiveCCAir40m10min(TestDiveCCAir, TMethodsMixin):
    """Test air 40m 10min."""

    params = ((40, 10), )

class TestDiveCCAir40m20min(TestDiveCCAir, TMethodsMixin):
    """Test air 40m 20min."""

    params = ((40, 20), )


class TestDiveCCAir40m30min(TestDiveCCAir, TMethodsMixin):
    """Test air 40m 30min."""

    params = ((40, 30), )

class TestDiveCCAir40m40min(TestDiveCCAir, TMethodsMixin):
    """Test air 40m 40min."""

    params = ((40, 40), )

class TestDiveCCAir40m50min(TestDiveCCAir, TMethodsMixin):
    """Test air 40m 50min."""

    params = ((40, 50), )

# ==================================================== 70m tests ==============
class TestDiveCCAir50m10min(TestDive):
    """Test air 70m 10min."""

    params = ((50, 10), )

    def runTest(self):
        """Run one test."""
        try:
            self.setpoint = 1.2
            self.dive_tank = self.ccair
            self.all_tanks = [self.ccair]
            diveseg1 = SegmentDive(self.params[0][0], self.params[0][1] * 60,
                                   self.dive_tank, self.setpoint)
            self.profile1 = Dive([diveseg1], self.all_tanks)
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")


# ======================= Multilevel Dive =====================================
class TestDiveCCAirMultilevel1(TestDiveCCAir, TMethodsMixin):
    """Multilevel dive test."""

    params = ((40, 10), (45, 12), (30, 15))
    name = 'multilevel1'
