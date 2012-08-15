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

"""Defines Exceptions for buhlmann model
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

#import math
import logging

# local imports
#import settings
from dipplanner.dipp_exception import DipplannerException


class ModelException(DipplannerException):
    """Generic Model Exception"""
    def __init__(self, description):
        """constructor : call the upper constructor and set the logger"""
        DipplannerException.__init__(self, description)
        self.logger = logging.getLogger(
            "dipplanner.DipplannerException.ModelException")
        self.logger.error(
            "Raising an exception: ModelException ! (%s)" % description)


class ModelStateException(DipplannerException):
    """Model State Exception"""
    def __init__(self, description):
        """constructor : call the upper constructor and set the logger"""
        DipplannerException.__init__(self, description)
        self.logger = logging.getLogger(
            "dipplanner.DipplannerException.ModelStateException")
        self.logger.error(
            "Raising an exception: ModelStateException ! (%s)" % description)
