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
"""Test Dives with air and deco."""
import json
import pkg_resources

from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner.tools import seconds_to_mmss

from dipplanner.tests.common import TestDive, TMethodsMixinDeco

class TestDiveTxNormoDecoNx80Base(TestDive):
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


class TestDiveTxNormoDecoNx80(TestDiveTxNormoDecoNx80Base):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.dive_tank = self.txtanknormodbl
        self.all_tanks = [self.txtanknormodbl, self.deco1]
        self.do_dive()

class TestDiveMultilevel(TestDiveTxNormoDecoNx80Base):
    """Multilevel dive test."""

    def setUp(self):
        """Init of multilevel test."""
        super().setUp()
        self.dive_tank = self.txtanknormodbl
        self.all_tanks = [self.txtanknormodbl, self.deco1]
        self.do_dive()


# Trimix Normp + DECO Nx80 ====================================================
# ==================================================== 10m tests ==============
class TestDiveTxNormoDecoNx8010m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 10m 10min."""

    params = ((10, 10), )


class TestDiveTxNormoDecoNx8010m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 10m 20min."""

    params = ((10, 20), )


class TestDiveTxNormoDecoNx8010m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 10m 30min."""

    params = ((10, 30), )


class TestDiveTxNormoDecoNx8010m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 10m 40min."""

    params = ((10, 40), )


class TestDiveTxNormoDecoNx8010m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 10m 50min."""

    params = ((10, 50), )


class TestDiveTxNormoDecoNx8010m60min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 10m 60min."""

    params = ((10, 60), )


class TestDiveTxNormoDecoNx8010m70min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 10m 70min."""

    params = ((10, 70), )


# ==================================================== 20m tests ==============
class TestDiveTxNormoDecoNx8020m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 20m 10min."""

    params = ((20, 10), )


class TestDiveTxNormoDecoNx8020m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 20m 20min."""

    params = ((20, 20), )


class TestDiveTxNormoDecoNx8020m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 20m 30min."""

    params = ((20, 30), )


class TestDiveTxNormoDecoNx8020m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 20m 40min."""

    params = ((20, 40), )


class TestDiveTxNormoDecoNx8020m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 20m 50min."""

    params = ((20, 50), )


# ==================================================== 30m tests ==============
class TestDiveTxNormoDecoNx8030m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 30m 10min."""

    params = ((30, 10), )


class TestDiveTxNormoDecoNx8030m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 30m 20min."""

    params = ((30, 20), )


class TestDiveTxNormoDecoNx8030m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 30m 30min."""

    params = ((30, 30), )

class TestDiveTxNormoDecoNx8030m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 30m 40min."""

    params = ((30, 40), )

class TestDiveTxNormoDecoNx8030m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 30m 50min."""

    params = ((30, 50), )

# ==================================================== 40m tests ==============
class TestDiveTxNormoDecoNx8040m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 40m 10min."""

    params = ((40, 10), )


class TestDiveTxNormoDecoNx8040m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 40m 20min."""

    params = ((40, 20), )

class TestDiveTxNormoDecoNx8040m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 40m 30min."""

    params = ((40, 30), )

class TestDiveTxNormoDecoNx8040m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 40m 40min."""

    params = ((40, 40), )

class TestDiveTxNormoDecoNx8040m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 40m 50min."""

    params = ((40, 50), )

# ==================================================== 50m tests ==============
class TestDiveTxNormoDecoNx8050m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 50m 10min."""

    params = ((50, 10), )

class TestDiveTxNormoDecoNx8050m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 50m 20min."""

    params = ((50, 20), )

class TestDiveTxNormoDecoNx8050m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 50m 30min."""

    params = ((50, 30), )


class TestDiveTxNormoDecoNx8050m40min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 50m 40min."""

    params = ((50, 40), )


class TestDiveTxNormoDecoNx8050m50min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 50m 50min."""

    params = ((50, 50), )


# ==================================================== 60m tests ==============
class TestDiveTxNormoDecoNx8060m10min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 60m 10min."""

    params = ((60, 10), )


class TestDiveTxNormoDecoNx8060m20min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 60m 20min."""

    params = ((60, 20), )

class TestDiveTxNormoDecoNx8060m25min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 60m 25min."""

    params = ((60, 25), )

class TestDiveTxNormoDecoNx8060m30min(TestDiveTxNormoDecoNx80, TMethodsMixinDeco):
    """Test txnormo 60m 30min."""

    params = ((60, 30), )

# ==================================================== 70m tests ==============
class TestDiveTxNormoDecoNx8070m10min(TestDive):
    """Test txnormo 70m 10min."""

    params = ((70, 10), )

    def runTest(self):
        """Run one test."""
        try:
            diveseg1 = SegmentDive(self.params[0][0], self.params[0][1] * 60,
                                   self.txtanknormodbl, 0)
            self.profile1 = Dive([diveseg1], [self.txtanknormodbl,
                                              self.deco1])
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
