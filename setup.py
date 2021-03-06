#
# Copyright 2011-2016 Thomas Chiroux
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
"""global setup file."""

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from io import open
import os

# local imports
from build_scripts.version import get_git_version

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]


with open("README.rst", encoding='utf-8') as f:
    README = f.read()

with open("NEWS.rst", encoding='utf-8') as f:
    NEWS = f.read()


VERSION = get_git_version()
if VERSION is None:
    try:
        file_name = "dipplanner/RELEASE-VERSION"
        version_file = open(file_name, "r", encoding='utf-8')
        try:
            VERSION = version_file.readlines()[0]
            VERSION = VERSION.strip()
        except:
            VERSION = "0.0.0"
        finally:
            version_file.close()
    except IOError:
        VERSION = "0.0.0"


class my_build_py(build_py):
    def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            target_dirs = []
            target_dirs.append(os.path.join(self.build_lib, 'dipplanner'))
            target_dirs.append('dipplanner')

            # mkpath is a distutils helper to create directories
            for dir in target_dirs:
                self.mkpath(dir)

            try:
                for dir in target_dirs:
                    fobj = open(os.path.join(dir, 'RELEASE-VERSION'), 'w',
                                encoding='utf-8')
                    fobj.write(VERSION)
                    fobj.close()
            except:
                pass

        # distutils uses old-style classes, so no super()
        build_py.run(self)


install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'jinja2', ]


setup(name='dipplanner',
      version=VERSION,
      description="Dive planner and decompression calculation program",
      long_description=README + '\n\n' + NEWS,
      cmdclass={'build_py': my_build_py},
      classifiers=[
          # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5"],
      keywords='diving plannification',
      author='Thomas Chiroux',
      author_email='',
      url='http://dipplanner.org',
      license='GPLv3',
      entry_points={
          'console_scripts': ['dipplanner = dipplanner.main:main', ],
      },
      packages=find_packages(),
      package_data={'dipplanner': ['RELEASE-VERSION', 'templates/*', ]},
      include_package_data=True,
      zip_safe=False,
      provides=('dipplanner', ),
      install_requires=install_requires,
      # test_suite = 'test.run_all_tests.run_all_tests',
      tests_require=['nose', 'coverage', ],
      test_suite='nose.collector',
      extras_require={
          'doc': ["sphinx", ],
          'devel_tools': ["ipython", "pylint", "pep8", ],
      },)
