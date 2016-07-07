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
"""Test Dives in hypoxic trimix with forced travel.

switch from travel to bottom mix at 40m
"""
import json
import pkg_resources


from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner.tools import seconds_to_mmss

from dipplanner.tests.common import TestDive, TMethodsMixinDecoTravel


class TestDiveTxHypoBase(TestDive):
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
        return '"%s": ["%s", %f, %f, %d, %d, %f, %s, %f, %s, %f, %s], ' % (
            self.name,
            seconds_to_mmss(self.profile1.run_time),
            self.profile1.model.ox_tox.otu,
            self.profile1.model.ox_tox.cns * 100,
            self.profile1.no_flight_time(),
            self.profile1.full_desat_time(),
            self.profile1.tanks[0].used_gas,
            str(self.profile1.tanks[0].check_rule()).lower(),
            self.profile1.tanks[1].used_gas,
            str(self.profile1.tanks[1].check_rule()).lower(),
            self.profile1.tanks[2].used_gas,
            str(self.profile1.tanks[2].check_rule()).lower())


class TestDiveTxHypo(TestDiveTxHypoBase):
    """Class for test air dive."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()
        self.dive_segs.append(SegmentDive(40, 130, self.txtravel, 0))
        self.dive_segs.append(SegmentDive(40, 30, self.txhypo, 0))
        self.dive_tank = self.txhypo
        self.all_tanks = [self.txtravel, self.txhypo, self.deco1]
        self.do_dive()


# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ====================================
# ==================================================== 50m tests ==============
class TestDiveTxHypo50m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 50m 10min."""

    params = ((50, 10), )


class TestDiveTxHypo50m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 50m 20min."""

    params = ((50, 20), )


class TestDiveTxHypo50m30min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 50m 30min."""

    params = ((50, 30), )


class TestDiveTxHypo50m40min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 50m 40min."""

    params = ((50, 40), )


class TestDiveTxHypo50m50min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 50m 50min."""

    params = ((50, 50), )


# ==================================================== 60m tests ==============
class TestDiveTxHypo60m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 60m 10min."""

    params = ((60, 10), )


class TestDiveTxHypo60m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 60m 20min."""

    params = ((60, 20), )


class TestDiveTxHypo60m30min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 60m 30min."""

    params = ((60, 30), )


class TestDiveTxHypo60m40min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 60m 40min."""

    params = ((60, 40), )

# ==================================================== 70m tests ==============
class TestDiveTxHypo70m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 70m 10min."""

    params = ((70, 10), )


class TestDiveTxHypo70m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 70m 20min."""

    params = ((70, 20), )


class TestDiveTxHypo70m30min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 70m 30min."""

    params = ((70, 30), )


# ==================================================== 80m tests ==============
class TestDiveTxHypo80m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 80m 10min."""

    params = ((80, 10), )


class TestDiveTxHypo80m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 80m 20min."""

    params = ((80, 20), )


class TestDiveTxHypo80m30min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 80m 30min."""

    params = ((80, 30), )

# ==================================================== 90m tests ==============
class TestDiveTxHypo90m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 90m 10min."""

    params = ((90, 10), )


class TestDiveTxHypo90m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 90m 20min."""

    params = ((90, 20), )


class TestDiveTxHypo90m30min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 90m 30min."""

    params = ((90, 30), )


# =================================================== 100m tests ==============
class TestDiveTxHypo100m5min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 100m 5min."""

    params = ((100, 5), )

class TestDiveTxHypo100m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 100m 10min."""

    params = ((100, 10), )


class TestDiveTxHypo100m15min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 100m 15min."""

    params = ((100, 15), )


class TestDiveTxHypo100m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 100m 20min."""

    params = ((100, 20), )


# =================================================== 110m tests ==============
class TestDiveTxHypo110m5min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 110m 5min."""

    params = ((110, 5), )

class TestDiveTxHypo110m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 110m 10min."""

    params = ((110, 10), )


class TestDiveTxHypo110m15min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 110m 15min."""

    params = ((110, 15), )


class TestDiveTxHypo110m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 110m 20min."""

    params = ((110, 20), )


# =================================================== 120m tests ==============
class TestDiveTxHypo120m5min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 120m 5min."""

    params = ((120, 5), )

class TestDiveTxHypo120m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 120m 10min."""

    params = ((120, 10), )


class TestDiveTxHypo120m15min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 120m 15min."""

    params = ((120, 15), )


class TestDiveTxHypo120m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 120m 20min."""

    params = ((120, 20), )

# =================================================== 130m tests ==============
class TestDiveTxHypo130m5min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 130m 5min."""

    params = ((130, 5), )

class TestDiveTxHypo130m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 130m 10min."""

    params = ((130, 10), )


class TestDiveTxHypo130m15min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 130m 15min."""

    params = ((130, 15), )


class TestDiveTxHypo130m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 130m 20min."""

    params = ((130, 20), )


# =================================================== 140m tests ==============
class TestDiveTxHypo140m5min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 140m 5min."""

    params = ((140, 5), )

class TestDiveTxHypo140m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 140m 10min."""

    params = ((140, 10), )


class TestDiveTxHypo140m15min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 140m 15min."""

    params = ((140, 15), )


class TestDiveTxHypo140m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 140m 20min."""

    params = ((140, 20), )


# =================================================== 150m tests ==============
class TestDiveTxHypo150m5min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 150m 5min."""

    params = ((150, 5), )

class TestDiveTxHypo150m10min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 150m 10min."""

    params = ((150, 10), )


class TestDiveTxHypo150m15min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 150m 15min."""

    params = ((150, 15), )


class TestDiveTxHypo150m20min(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo 150m 20min."""

    params = ((150, 20), )


# =================================================== 160m tests ==============
class TestDiveTxHypo160m10min(TestDive):
    """Test tx hypo 160m 10min."""

    params = ((160, 10), )

    def runTest(self):
        """Should raise an error."""
        try:
            diveseg1 = SegmentDive(self.params[0][0], self.params[0][1] * 60,
                                   self.txhypo, 0)
            self.profile1 = Dive([SegmentDive(40, 130, self.txtravel, 0),
                                  SegmentDive(40, 30, self.txhypo, 0),
                                  diveseg1],
                                 [self.txtravel, self.txhypo, self.deco1])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail('should raise UnauthorizedMod')


# ======================== Multilevel Dive ====================================

class TestDiveMultilevel(TestDiveTxHypo, TMethodsMixinDecoTravel):
    """Test tx hypo multilevel 1."""

    params = ((40, 10), (50, 12), (30, 15))
    name = 'multilevel1'
