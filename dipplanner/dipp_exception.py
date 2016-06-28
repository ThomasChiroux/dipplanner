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
"""Base Class for exceptions for dipplanner module."""

import logging


class DipplannerException(Exception):
    """Base exception class for dipplanner."""

    def __init__(self, description):
        """Init of DipplannerException.

        :param str description: text describing the error
        """
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.description = description

    def __str__(self):
        """String representing the object.

        :returns: a string describing the Exception
        :rtype: str
        """
        return ''.join(self.description)
