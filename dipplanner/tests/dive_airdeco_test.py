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
import json
import pkg_resources
import unittest


from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner.tools import seconds_to_mmss

from dipplanner.tests.common import TestDive, TMethodsMixinDeco


class TestDiveAirDecoNx80Base(TestDive):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        # load json results file
        self.results = json.loads(
            pkg_resources.resource_string(
                "dipplanner.tests",
                __name__.split('.')[-1] + '.json').decode('utf-8'))

    @property
    def details(self):
        """print detailed results."""
        return '"%s": ["%s", %f, %f, %d, %d, %f, %s, %f, %s], ' % (
            self.name,
            seconds_to_mmss(self.profile1.run_time),
            self.profile1.model.ox_tox.otu,
            self.profile1.model.ox_tox.cns * 100,
            self.profile1.no_flight_time(),
            self.profile1.full_desat_time(),
            self.profile1.tanks[0].used_gas,
            str(self.profile1.tanks[0].check_rule()).lower(),
            self.profile1.tanks[1].used_gas,
            str(self.profile1.tanks[1].check_rule()).lower())


class TestDiveAirDecoNx80(TestDiveAirDecoNx80Base):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.dive_tank = self.airtank12
        self.all_tanks = [self.airtank12, self.deco1]
        self.do_dive()


class TestDiveMultilevel(TestDiveAirDecoNx80Base):
    """Multilevel dive test."""

    def setUp(self):
        """Init of multilevel test."""
        super().setUp()
        self.dive_tank = self.airdouble
        self.all_tanks = [self.airdouble, self.deco1]
        self.do_dive()


# AIR + DECO Nx80 =============================================================
# ==================================================== 10m tests ==============
class TestDiveAirDecoNx8010m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 10min."""

    params = ((10, 10), )

class TestDiveAirDecoNx8010m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 20min."""

    params = ((10, 20), )

class TestDiveAirDecoNx8010m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 30min."""

    params = ((10, 30), )

class TestDiveAirDecoNx8010m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 40min."""

    params = ((10, 40), )

class TestDiveAirDecoNx8010m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 50min."""

    params = ((10, 50), )

class TestDiveAirDecoNx8010m60min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 60min."""

    params = ((10, 60), )


class TestDiveAirDecoNx8010m70min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 10m 70min."""

    params = ((10, 70), )


# ==================================================== 20m tests ==============
class TestDiveAirDecoNx8020m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 10min."""

    params = ((20, 10), )


class TestDiveAirDecoNx8020m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 20min."""

    params = ((20, 20), )


class TestDiveAirDecoNx8020m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 30min."""

    params = ((20, 30), )


class TestDiveAirDecoNx8020m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 40min."""

    params = ((20, 40), )


class TestDiveAirDecoNx8020m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 20m 50min."""

    params = ((20, 50), )


# ==================================================== 30m tests ==============
class TestDiveAirDecoNx8030m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 10min."""

    params = ((30, 10), )


class TestDiveAirDecoNx8030m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 20min."""

    params = ((30, 20), )


class TestDiveAirDecoNx8030m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 30min."""

    params = ((30, 30), )


class TestDiveAirDecoNx8030m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 40min."""

    params = ((30, 40), )

class TestDiveAirDecoNx8030m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 30m 50min."""

    params = ((30, 50), )


# ==================================================== 40m tests ==============
class TestDiveAirDecoNx8040m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 10min."""

    params = ((40, 10), )


class TestDiveAirDecoNx8040m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 20min."""

    params = ((40, 20), )


class TestDiveAirDecoNx8040m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 30min."""

    params = ((40, 30), )


class TestDiveAirDecoNx8040m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 40min."""

    params = ((40, 40), )


class TestDiveAirDecoNx8040m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 40m 50min."""

    params = ((40, 50), )


# ==================================================== 50m tests ==============
class TestDiveAirDecoNx8050m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 10min."""

    params = ((50, 10), )


class TestDiveAirDecoNx8050m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 20min."""

    params = ((50, 20), )


class TestDiveAirDecoNx8050m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 30min."""

    params = ((50, 30), )


class TestDiveAirDecoNx8050m40min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 40min."""

    params = ((50, 40), )


class TestDiveAirDecoNx8050m50min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 50m 50min."""

    params = ((50, 50), )


# ==================================================== 60m tests ==============
class TestDiveAirDecoNx8060m10min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 10min."""

    params = ((60, 10), )


class TestDiveAirDecoNx8060m20min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 20min."""

    params = ((60, 20), )

class TestDiveAirDecoNx8060m25min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 25min."""

    params = ((60, 25), )


class TestDiveAirDecoNx8060m30min(TestDiveAirDecoNx80, TMethodsMixinDeco):
    """Test air 60m 30min."""

    params = ((60, 30), )


# ==================================================== 70m tests ==============
class TestDiveAirDecoNx8070m10min(TestDive):
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
class TestDiveMultilevel1(TestDiveMultilevel, TMethodsMixinDeco):
    """Multilevel dive test."""

    params = ((40, 10), (50, 12), (30, 15))
    name = 'multilevel1'
