#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>
#
# This module is part of dipplanner, a Dive planning Tool written in python
"""global setup
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

from setuptools import setup, find_packages
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.rst')).read()

version = '0.3nightly'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'jinja2',
    # below are dependencies for develop phaes only
    # TODO: find a way to install only this tools with setup.py develop
    "ipython",
    "pylint",
    "pep8",
    "sphinx", ]

setup(name='dipplanner',
      version=version,
      description="Dive planner and decompression calculation program",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      ],
      keywords='diving plannification',
      author='Thomas Chiroux',
      author_email='',
      url='http://dipplanner.org',
      license='GPLv3',
      entry_points = {
        'console_scripts': [ 'dipplanner = dipplanner.main:main' ],
      },
      packages=find_packages('src'),
      package_dir={'': 'src'}, include_package_data=True,
      zip_safe=False,
      provides=('dipplanner',),
      install_requires=install_requires,
      #test_suite = 'test.run_all_tests.run_all_tests',
      tests_require = [ 'nose', 'coverage', ],
      test_suite = 'nose.collector',
      extras_require = {
          'doc':  ["sphinx", ],
          'devel_tools':  ["ipython", "pylint", "pep8" ],
      },)
