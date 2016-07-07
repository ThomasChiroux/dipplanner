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
"""Test for tank class."""
import unittest

# local imports
from dipplanner.main import activate_debug_for_tests

from dipplanner.tank import Tank, InvalidGas, InvalidTank, InvalidMod


class TestTank(unittest.TestCase):
    """Base class for test tanks."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        # temporary hack (tests):
        activate_debug_for_tests()

class TestTankisAir(TestTank):
    """Test Air Tank."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank()

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Air'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 66

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))

    def test_tank_info(self):
        """Check str output."""
        self.assertEqual(self.mytank.tank_info,
                         '12.0l-100.0% (2423.10/2423.10l)',
                         "Wrong Tank infos: %s"
                         % self.mytank.tank_info)


class TestTankNitrox32(TestTank):
    """Test Nitrox32 Tank."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.32)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Nitrox 32'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 40

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisO2(TestTank):
    """Test O2 Tank."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=1)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Oxygen'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 6

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix2030(TestTank):
    """Test Tx2030 Tank."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.2, f_he=0.3)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Trimix 20/30'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 70

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               43.3498554235, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               27.4879482229, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix870(TestTank):
    """Test Tx8/70 Tank."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.1, f_he=0.7)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Trimix 10/70'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 150

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               79.0122229175, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               12.4620912698, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisHeliox2080(TestTank):
    """Test Heliox2080 Tank."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.2, f_he=0.8)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Heliox 20/80'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 70

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               96.8666243516, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               8.70562703148, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisAir2(TestTank):
    """Test Air Tank 2."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(max_ppo2=1.4)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Air'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 56

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisNitrox32_2(TestTank):
    """Test Nitrox32 Tank Z."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.32, max_ppo2=1.4)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Nitrox 32'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 33

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisO2_2(TestTank):
    """Test O2 Tank 2."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=1, max_ppo2=1.4)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Oxygen'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 4

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix2030_2(TestTank):
    """Test Tx2030 Tank 2."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.2, f_he=0.3, max_ppo2=1.4)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Trimix 20/30'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 59

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               43.3498554235, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               27.4879482229, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix870_2(TestTank):
    """Test Tx8/70 Tank 2."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.08, f_he=0.7, max_ppo2=1.4)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Trimix 8/70'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 165

    def test_min_od(self):
        """Check Calculated minimum od."""
        assert self.mytank.get_min_od() == 10

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               79.0122229175, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               12.4620912698, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisHeliox2080_2(TestTank):
    """Test Heliox2080 Tank 2."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(f_o2=0.2, f_he=0.8, max_ppo2=1.4)

    def test_name(self):
        """Check Name."""
        assert str(self.mytank) == 'Heliox 20/80'

    def test_mod(self):
        """Check Calculated mod."""
        assert self.mytank.mod == 59

    def test_mod_at_end(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               96.8666243516, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        """Check Calculated mod at given end."""
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               8.70562703148, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankVolume1(TestTank):
    """Test Tank Volume 1."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(tank_vol=15, tank_pressure=207)

    def test_vol(self):
        """Test volume calc."""
        self.assertAlmostEqual(self.mytank.total_gas, 3116, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.total_gas)


class TestTankVolume2(TestTank):
    """Test Tank Volume 2."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(tank_vol=18, tank_pressure=230)

    def test_vol(self):
        """Test volume calc."""
        self.assertAlmostEqual(self.mytank.total_gas, 4064.6008, 4,
                               'Wrong Tank Volume : %s'
                               % self.mytank.total_gas)


class TestTankVolume3(TestTank):
    """Test Tank Volume 3."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(tank_vol=15, tank_pressure=207)

    def test_vol(self):
        """Test volume calc."""
        self.mytank.consume_gas(405)
        self.assertAlmostEqual(self.mytank.remaining_gas, 2711, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.remaining_gas)


class TestTankVolume4(TestTank):
    """Test Tank Volume 4."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(tank_vol=15, tank_pressure=207)

    def test_vol(self):
        """Test volume calc."""
        self.mytank.consume_gas(405)
        self.mytank.consume_gas(2800)
        self.assertEqual(self.mytank.check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)'
                         % self.mytank.check_rule())


class TestTankRefill(TestTank):
    """Test Tank Refill."""

    def setUp(self):
        """Init of the tests."""
        super().setUp()

        self.mytank = Tank(tank_vol=15, tank_pressure=207)
        self.mytank.consume_gas(405)
        self.mytank.consume_gas(2800)

    def test_vol(self):
        """Test volume calc."""
        self.assertAlmostEqual(self.mytank.remaining_gas,
                               -88.9813390544, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.remaining_gas)

    def test_refill(self):
        """Test volume calc after refill."""
        self.mytank.refill()
        self.assertAlmostEqual(self.mytank.remaining_gas,
                               3116.01866095, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.remaining_gas)


class TestTankInvalidGas(TestTank):
    """Test Tank InvalidGas."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(f_o2=0.8, f_he=0.3)
        except InvalidGas:
            pass
        else:
            self.fail('should raise Invalid Gas')


class TestTankInvalidTank1(TestTank):
    """Test Tank InvalidTank 1."""

    def runTest(self):
        """Should raise an error."""
        try:
            Tank(f_o2=0.8, tank_vol=43)
        except InvalidTank:
            pass
        else:
            self.fail('should raise Invalid Tank')


class TestTankInvalidTank2(TestTank):
    """Test Tank InvalidTank 2."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(f_o2=0.3, tank_pressure=350)
        except InvalidTank:
            pass
        else:
            self.fail('should raise Invalid Tank')

class TestTankInvalidTank3(TestTank):
    """Test Tank InvalidTank 3."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(f_o2=-0.3)
        except InvalidGas:
            pass
        else:
            self.fail('should raise Invalid Gas')

class TestTankInvalidTank4(TestTank):
    """Test Tank InvalidTank 4."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(tank_vol=-150)
        except InvalidTank:
            pass
        else:
            self.fail('should raise Invalid Tank')

class TestTankInvalidTank5(TestTank):
    """Test Tank InvalidTank 5."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(f_o2=0.3, tank_pressure=-100)
        except InvalidTank:
            pass
        else:
            self.fail('should raise Invalid Tank')

class TestTankInvalidMod1(TestTank):
    """Test Tank InvalidMod 1."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(f_o2=0.8, mod=33)
        except InvalidMod:
            pass
        else:
            self.fail('should raise Invalid Mod')


class TestTankInvalidMod2(TestTank):
    """Test Tank InvalidMod 2."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(f_o2=1, mod=7)
        except InvalidMod:
            pass
        else:
            self.fail('should raise Invalid Mod')


class TestTankInvalidMod3(TestTank):
    """Test Tank InvalidMod 3."""

    def runTest(self):
        """Should raise an error."""
        super().setUp()

        try:
            Tank(f_o2=1, mod=-7)
        except InvalidMod:
            pass
        else:
            self.fail('should raise Invalid Mod')

class TestTankRules(TestTank):
    """Test Tank rules."""

    def setUp(self):
        """Should raise an error."""
        super().setUp()

        TestTank.setUp(self)

    def test_rule_bar_1(self):
        """Check rule rem bars."""
        mytank = Tank(tank_vol=15, tank_pressure=200, tank_rule="50b")
        self.assertAlmostEqual(mytank.min_gas, 767.5548, 4,
                               "bad Tank rule calculation: %s"
                               % mytank.min_gas)

    def test_rule_bar_2(self):
        """Check rule 1/3."""
        mytank = Tank(tank_vol=15, tank_pressure=200, tank_rule="1/3")
        self.assertAlmostEqual(mytank.min_gas, 1009.62376, 4,
                               "bad Tank rule calculation: %s"
                               % mytank.min_gas)

    def test_rule_bar_3(self):
        """Check rule 1/6."""
        mytank = Tank(tank_vol=15, tank_pressure=200, tank_rule="1/6")
        self.assertAlmostEqual(mytank.min_gas, 2019.24752, 4,
                               "bad Tank rule calculation: %s"
                               % mytank.min_gas)
