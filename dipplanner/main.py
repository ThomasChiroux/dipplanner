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
"""Main dipplanner module for command line usage.

This module is used by the only "executable" of the project:
bin/dipplanner (which is an empty shell)

runs in command line and output resulting dive profile
also initiate log files
"""
import sys
import logging

# dependencies imports
from jinja2 import Environment, PackageLoader

# local imports
from dipplanner.parse_cli_args import DipplannerCliArguments
from dipplanner import settings
from dipplanner.dive import Dive

LOGGER = logging.getLogger("dipplanner")


def activate_debug():
    """Setup the default debug parameters.

    it's mainly used for test cases who needs also logging to be set
    """
    LOGGER.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    file_handler = logging.FileHandler("dipplanner.log")
    file_handler.setLevel(logging.INFO)
    # create console handler with a higher log level
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # add the handlers to the logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)


def activate_debug_for_tests():
    """Setup the default debug parameters.

    it's mainly used for test cases who needs also logging to be set
    """
    LOGGER.setLevel(logging.CRITICAL)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)


def main(cli_arguments=None):
    """Main entry point.

    main uses the parameters, tanks and dives given in config file(s)
    and/or command line, calculates the dives and return the output in stdout.

    :param list cli_arguments: list of arguments, like sys.argv
    """
    if sys.version_info < (3, 4):
        raise SystemExit("ERROR: This programm needs python 3.4 or greater")

    if cli_arguments is None:
        cli_arguments = sys.argv

    activate_debug()

    # get the version
    try:
        version_file = open("RELEASE-VERSION", "r")
        try:
            version = version_file.readlines()[0]
            settings.__VERSION__ = version.strip()
        finally:
            version_file.close()
    except IOError:
        settings.__VERSION__ = "unknown"

    dipplanner_arguments = DipplannerCliArguments(cli_arguments)
    dives = dipplanner_arguments.dives

    profiles = []
    current_dive = None
    previous_dive = None
    for dive in dives:
        if previous_dive is None:
            current_dive = Dive(
                dives[dive]['segments'].values(),
                dives[dive]['tanks'].values())
        else:
            current_dive = Dive(
                dives[dive]['segments'].values(),
                dives[dive]['tanks'].values(),
                previous_dive
            )
        if dives[dive]['surface_interval']:
            current_dive.do_surface_interval(dives[dive]['surface_interval'])

        current_dive.do_dive_without_exceptions()
        profiles.append(current_dive)
        previous_dive = current_dive
        # now, dive exceptins do not stop the program anymore, but can be
        # displayed in the output template instead. The used MUST take care of
        # the result.

    # now calculate no flight time based on the last dive
    current_dive.no_flight_time_wo_exception()

    # now Prepare the output
    env = Environment(loader=PackageLoader('dipplanner', 'templates'))
    tpl = env.get_template(settings.TEMPLATE)
    # pylint: disable=no-member
    text = tpl.render(settings=settings, dives=profiles)
    # pylint: enable=no-member
    print(text)
