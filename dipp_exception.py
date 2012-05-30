#! /usr/bin/python
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
# Strongly inspired by Guy Wittig's MVPlan 
"""Base Class for exceptions for dipplanner module
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import logging

class DipplannerException(Exception):
  """Base exception class for dipplanner
  """
  def __init__(self, description):
    self.logger = logging.getLogger("dipplanner.DipplannerException")
    self.description = description
  
  def __str__(self):
    return repr(self.description)

# TODO: ça ne va pas : continuer plutôt à utiliser les Exceptions, et les
#       gerer en try: except: pour les ajouter dans une liste dans Dive()


class DipplannerError(object):
  """Base Error class
    Error is not an exception (in python terms):
    it is not raisable, neither try able
    Errors are created when an abnormal functionnal situation appears:
      it is not not error or problems in program execution, but
      for example possible dive problems (diving below MOD, etc...)
  """

  def __init__(self, description=None):
    """Generic constructor

       type can be, like logging:
       - DEBUG
       - INFO
       - WARNING
       - ERROR
       - CRITICAL
    """
    self.logger = logging.getLogger("dipplanner.DipplannerError")
    self.description = description


class DipplannerErrorDebug(DipplannerError):
  def __init__(self, description):
    super(DipplannerErrorDebug, self).__init__(description)
    self.type = "DEBUG"

class DipplannerErrorInfo(DipplannerError):
  def __init__(self, description):
    super(DipplannerErrorInfo, self).__init__(description)
    self.type = "INFO"

class DipplannerErrorWarning(DipplannerError):
  def __init__(self, description):
    super(DipplannerErrorWarning, self).__init__(description)
    self.type = "WARNING"

class DipplannerErrorError(DipplannerError):
  def __init__(self, description):
    super(DipplannerErrorError, self).__init__(description)
    self.type = "ERROR"

class DipplannerErrorCritical(DipplannerError):
  def __init__(self, description):
    super(DipplannerErrorCritical, self).__init__(description)
    self.type = "CRITICAL"
