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
"""Define Exceptions for buhlmann model."""
from dipplanner.dipp_exception import DipplannerException


class ModelException(DipplannerException):
    """Generic Model Exception."""

    def __init__(self, description):
        """Init of ModelException.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: ModelException ! (%s)", description)


class ModelStateException(ModelException):
    """Model State Exception."""

    def __init__(self, description):
        """Init of ModelStateException.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: ModelStateException ! (%s)", description)


class ModelValidationException(ModelException):
    """Model State Exception."""

    def __init__(self, description):
        """Init of ModelValidationException.

        :param str description: text describing the error
        """
        super().__init__(description)
        self.logger.error(
            "Raising an exception: ModelValidationException ! (%s)",
            description)
