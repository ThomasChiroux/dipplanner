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
"""Test Dives in hypoxic trimix."""
import json
import pkg_resources

from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner import settings

from dipplanner.tests.common import TestDive, TMethodsMixin


class TestDiveCCTxHypoBase(TestDive):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        # load json results file
        self.results = json.loads(
            pkg_resources.resource_string(
                "dipplanner.tests",
                __name__.split('.')[-1] + '.json').decode('utf-8'))


class TestDiveCCTxHypo(TestDiveCCTxHypoBase):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        settings.RUN_TIME = False
        self.setpoint = 1.2
        self.dive_tank = self.cctxhypo
        self.all_tanks = [self.cctxhypo]
        self.do_dive()


# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ====================================
# ==================================================== 50m tests ==============
class TestDiveCCTxHypo50m10min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 50m 10min."""

    params = ((50, 10), )


class TestDiveCCTxHypo50m20min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 50m 20min."""

    params = ((50, 20), )


class TestDiveCCTxHypo50m30min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 50m 30min."""

    params = ((50, 30), )


class TestDiveCCTxHypo50m40min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 50m 40min."""

    params = ((50, 40), )


class TestDiveCCTxHypo50m50min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 50m 50min."""

    params = ((50, 50), )


# ==================================================== 60m tests ==============
class TestDiveCCTxHypo60m10min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 60m 10min."""

    params = ((60, 10), )


class TestDiveCCTxHypo60m20min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 60m 20min."""

    params = ((60, 20), )


class TestDiveCCTxHypo60m30min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 60m 30min."""

    params = ((60, 30), )


class TestDiveCCTxHypo60m40min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 60m 40min."""

    params = ((60, 40), )

# ==================================================== 70m tests ==============
class TestDiveCCTxHypo70m10min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 70m 10min."""

    params = ((70, 10), )


class TestDiveCCTxHypo70m20min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 70m 20min."""

    params = ((70, 20), )


class TestDiveCCTxHypo70m30min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 70m 30min."""

    params = ((70, 30), )


# ==================================================== 80m tests ==============
class TestDiveCCTxHypo80m10min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 80m 10min."""

    params = ((80, 10), )


class TestDiveCCTxHypo80m20min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 80m 20min."""

    params = ((80, 20), )


class TestDiveCCTxHypo80m30min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 80m 30min."""

    params = ((80, 30), )

# ==================================================== 90m tests ==============
class TestDiveCCTxHypo90m10min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 90m 10min."""

    params = ((90, 10), )


class TestDiveCCTxHypo90m20min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 90m 20min."""

    params = ((90, 20), )


class TestDiveCCTxHypo90m30min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 90m 30min."""

    params = ((90, 30), )


# =================================================== 100m tests ==============
class TestDiveCCTxHypo100m5min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 100m 5min."""

    params = ((100, 5), )

class TestDiveCCTxHypo100m10min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 100m 10min."""

    params = ((100, 10), )


class TestDiveCCTxHypo100m15min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 100m 15min."""

    params = ((100, 15), )


class TestDiveCCTxHypo100m20min(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo 100m 20min."""

    params = ((100, 20), )

# =================================================== 160m tests ==============
class TestDiveCCTxHypo110m10min(TestDive):
    """test CC tx hypo 110m 10min."""

    params = ((110, 10), )

    def runTest(self):
        """Should raise and error."""
        try:
            self.setpoint = 1.2
            self.dive_tank = self.cctxhypo
            self.all_tanks = [self.cctxhypo]
            diveseg1 = SegmentDive(self.params[0][0], self.params[0][1] * 60,
                                   self.dive_tank, self.setpoint)
            self.profile1 = Dive([diveseg1], self.all_tanks)
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")


# ======================== Multilevel Dive ====================================

class TestDiveMultilevel(TestDiveCCTxHypo, TMethodsMixin):
    """Test tx hypo multilevel 1."""

    params = ((40, 10), (50, 12), (30, 15))
    name = 'multilevel1'

