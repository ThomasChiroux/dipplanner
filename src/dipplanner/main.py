#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011-2012 Thomas Chiroux
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

"""main dipplanner module for command line usage.

This module is used by the only "executable" of the project:
bin/dipplanner (which is an empty shell)

runs in command line and output resulting dive profile
also initiate log files

.. todo:: logger.tutu("message %s", allo)
          au lieu de logger.tutu("message %s" % allo)

.. todo:: revoir tous les dump_dict
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import sys
import logging

# dependencies imports
from jinja2 import Environment, PackageLoader

# local imports
from dipplanner import settings
from dipplanner.gui import start_gui

LOGGER = logging.getLogger("dipplanner")
MISSION = None


def activate_debug():
    """setup the default debug parameters

    it's mainly used for test cases who needs also logging to be set

    *Keyword Arguments:*
        <none>

    *Return:*
        <nothing>

    *Raise:*
        <nothing>

    """
    LOGGER.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    file_handler = logging.FileHandler("dipplanner.log")
    file_handler.setLevel(logging.DEBUG)
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
    """setup the default debug parameters

    it's mainly used for test cases who needs also logging to be set

    *Keyword Arguments:*
        <none>

    *Return:*
        <nothing>

    *Raise:*
        <nothing>
    """
    LOGGER.setLevel(logging.CRITICAL)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)


def main(cli_arguments=sys.argv):
    """main

    main uses the parameters, tanks and dives given in config file(s)
    and/or command line, calculates the dives and return the output in stdout.

    *Keyword Arguments:*
        arguments (list of string) -- list of arguments, like sys.argv

    *Return:*
        <nothing>

    *Raise:*
        <nothing>
    """
    if not hasattr(sys, 'version_info') or sys.version_info < (2, 7, 0,
                                                               'final'):
        raise SystemExit("dipplanner requires Python 2.7 or later.")

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

    from dipplanner.parse_cli_args import DipplannerCliArguments

    dipplanner_arguments = DipplannerCliArguments(cli_arguments)
    mission = dipplanner_arguments.mission
    mission.calculate()

    if dipplanner_arguments.args.gui:
        start_gui(mission)
    else:
        # now Prepare the output
        env = Environment(loader=PackageLoader('dipplanner', 'templates'))
        tpl = env.get_template(settings.TEMPLATE)
        text = tpl.render(settings=settings, dives=mission)
        print text
