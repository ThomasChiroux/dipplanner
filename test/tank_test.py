#!/usr/bin/python2
# -*- coding: utf-8 -*-

#
# Copyright 2011 Thomas Chiroux
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

"""
Test for tank class
"""

__authors__ = ['Thomas Chiroux']  # alphabetical order by last name

import unittest

# local imports
from dipplanner.main import activate_debug_for_tests

from dipplanner.tank import Tank, InvalidGas, InvalidTank, InvalidMod


class TestTank(unittest.TestCase):

    def setUp(self):
        # temporary hack (tests):
        activate_debug_for_tests()

    def tearDown(self):
        pass


class TestTankisAir(TestTank):

    def setUp(self):
        self.mytank = Tank()

    def test_name(self):
        assert str(self.mytank) == 'Air'

    def test_mod(self):
        assert self.mytank.mod == 66

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'

                               % self.mytank.get_end_for_given_depth(40))


class TestTankNitrox32(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.32)

    def test_name(self):
        assert str(self.mytank) == 'Nitrox 32'

    def test_mod(self):
        assert self.mytank.mod == 40

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisO2(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=1)

    def test_name(self):
        assert str(self.mytank) == 'Oxygen'

    def test_mod(self):
        assert self.mytank.mod == 6

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix2030(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.2, f_he=0.3)

    def test_name(self):
        assert str(self.mytank) == 'Trimix 20/30'

    def test_mod(self):
        assert self.mytank.mod == 70

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               43.3498554235, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               27.4879482229, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix870(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.1, f_he=0.7)

    def test_name(self):
        assert str(self.mytank) == 'Trimix 10/70'

    def test_mod(self):
        assert self.mytank.mod == 150

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               79.0122229175, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               12.4620912698, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisHeliox2080(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.2, f_he=0.8)

    def test_name(self):
        assert str(self.mytank) == 'Heliox 20/80'

    def test_mod(self):
        assert self.mytank.mod == 70

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               96.8666243516, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               8.70562703148, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisAir2(TestTank):

    def setUp(self):
        self.mytank = Tank(max_ppo2=1.4)

    def test_name(self):
        assert str(self.mytank) == 'Air'

    def test_mod(self):
        assert self.mytank.mod == 56

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisNitrox32_2(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.32, max_ppo2=1.4)

    def test_name(self):
        assert str(self.mytank) == 'Nitrox 32'

    def test_mod(self):
        assert self.mytank.mod == 33

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisO2_2(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=1, max_ppo2=1.4)

    def test_name(self):
        assert str(self.mytank) == 'Oxygen'

    def test_mod(self):
        assert self.mytank.mod == 4

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               31.0195918624, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               38.7573409377, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix2030_2(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.2, f_he=0.3, max_ppo2=1.4)

    def test_name(self):
        assert str(self.mytank) == 'Trimix 20/30'

    def test_mod(self):
        assert self.mytank.mod == 59

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               43.3498554235, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               27.4879482229, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisTrimix870_2(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.08, f_he=0.7, max_ppo2=1.4)

    def test_name(self):
        assert str(self.mytank) == 'Trimix 8/70'

    def test_mod(self):
        assert self.mytank.mod == 165

    def test_min_od(self):
        assert self.mytank.get_min_od() == 10

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               79.0122229175, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               12.4620912698, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankisHeliox2080_2(TestTank):

    def setUp(self):
        self.mytank = Tank(f_o2=0.2, f_he=0.8, max_ppo2=1.4)

    def test_name(self):
        assert str(self.mytank) == 'Heliox 20/80'

    def test_mod(self):
        assert self.mytank.mod == 59

    def test_mod_at_end(self):
        self.assertAlmostEqual(self.mytank.get_mod_for_given_end(30),
                               96.8666243516, 5, 'wrong mod at end:%s'
                               % self.mytank.get_mod_for_given_end(30))

    def test_end_at_depth(self):
        self.assertAlmostEqual(self.mytank.get_end_for_given_depth(40),
                               8.70562703148, 5, 'wrong end at depth:%s'
                               % self.mytank.get_end_for_given_depth(40))


class TestTankVolume1(TestTank):

    def setUp(self):
        self.mytank = Tank(tank_vol=15, tank_pressure=207)

    def test_vol(self):
        self.assertAlmostEqual(self.mytank.total_gas, 3116, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.total_gas)


class TestTankVolume2(TestTank):

    def setUp(self):
        self.mytank = Tank(tank_vol=18, tank_pressure=230)

    def test_vol(self):
        self.assertAlmostEqual(self.mytank.total_gas, 4064.6008, 4,
                               'Wrong Tank Volume : %s'
                               % self.mytank.total_gas)


class TestTankVolume3(TestTank):

    def setUp(self):
        self.mytank = Tank(tank_vol=15, tank_pressure=207)

    def test_vol(self):
        self.mytank.consume_gas(405)
        self.assertAlmostEqual(self.mytank.remaining_gas, 2711, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.remaining_gas)


class TestTankVolume4(TestTank):

    def setUp(self):
        self.mytank = Tank(tank_vol=15, tank_pressure=207)

    def test_vol(self):
        self.mytank.consume_gas(405)
        self.mytank.consume_gas(2800)
        self.assertEqual(self.mytank.check_rule(), False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)'
                         % self.mytank.check_rule())


class TestTankRefill(TestTank):

    def setUp(self):
        self.mytank = Tank(tank_vol=15, tank_pressure=207)
        self.mytank.consume_gas(405)
        self.mytank.consume_gas(2800)

    def test_vol(self):
        self.assertAlmostEqual(self.mytank.remaining_gas,
                               -88.9813390544, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.remaining_gas)

    def test_refill(self):
        self.mytank.refill()
        self.assertAlmostEqual(self.mytank.remaining_gas,
                               3116.01866095, 0,
                               'Wrong Tank Volume : %s'
                               % self.mytank.remaining_gas)


class TestTankInvalidGas(TestTank):

    def runTest(self):
        try:
            mytank = Tank(f_o2=0.8, f_he=0.3)
        except InvalidGas:
            pass
        else:
            self.fail('should raise Invalid Gas')


class TestTankInvalidTank1(TestTank):

    def runTest(self):
        try:
            mytank = Tank(f_o2=0.8, tank_vol=43)
        except InvalidTank:
            pass
        else:
            self.fail('should raise Invalid Tank')


class TestTankInvalidTank2(TestTank):

    def runTest(self):
        try:
            mytank = Tank(f_o2=0.3, tank_pressure=350)
        except InvalidTank:
            pass
        else:
            self.fail('should raise Invalid Tank')


class TestTankInvalidMod1(TestTank):

    def runTest(self):
        try:
            mytank = Tank(f_o2=0.8, mod=33)
        except InvalidMod:
            pass
        else:
            self.fail('should raise Invalid Mod')


class TestTankInvalidMod2(TestTank):

    def runTest(self):
        try:
            mytank = Tank(f_o2=1, mod=7)
        except InvalidMod:
            pass
        else:
            self.fail('should raise Invalid Mod')


def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('tests', metavar='TestName', type=str, nargs='*',
                        help='name of the tests to run '
                             '(separated by space) [optionnal]')
    args = parser.parse_args()
    if args.tests:
        suite = unittest.TestLoader().loadTestsFromNames(args.tests,
                                                         sys.modules[__name__])
    else:
        suite = unittest.findTestCases(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()
