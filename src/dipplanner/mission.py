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
"""Mission class module

A Mission a basically a list of repetitive dives.
It could also be called a 'DiveTrip' for example
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]


# local imports
from dipplanner import settings
from dipplanner.dive import Dive

class Mission(object):
    """Mission Class

    a Mission represent all repetitive dives for a given set of time.
    the Mission will keep consistency between repetitive dives

    An isolated dive is a Mission with only one dive inside

    Attributes:
        dives (list) -- list of Dive object of the same mission
        description (str) -- description of the mission (OPTIONAL)

    .. todo:: Insert dive(s) in a certain position

    .. todo:: change dive order, permutations, etc...

    .. todo:: decide if we define a common list of tanks for a given mission
              in this case, each dive will be able to pickup some tank

    .. todo:: decide if settings is included in Mission object or remains
              global
    """

    def __init__(self, dive_or_divelist=None, description=None):
        """Mission constructor

        Initialize the Mission object
        if no parameter is given, instantiate an 'empty' Mission

        *Keyword Arguments:*
            :dive_or_divelist: -- either on Dive object
                                  or a list of Dive object
            :description: (str)-- description of the Mission

        Return:
            <nothing>

        Raise:
            TypeError: if dive_or_divelist contains another type than Dive
        """
        self.dives = []
        self.description = description
        if dive_or_divelist is not None:
            self.add_dive(dive_or_divelist)

    def __iter__(self):
        """iterable

        see :py:meth:`dipplanner.mission.Mission._forward` )
        """
        return self._forward()

    def _forward(self):
        """forward generator, used for iteration
        """
        current_item = 0
        total_len = len(self.dives)
        while current_item < total_len:
            dive = self.dives[current_item]
            current_item += 1
            yield dive

    def __len__(self):
        """calculate and return len of Session object

        usage example:

          .. code-block:: python

            print len(my_mission)

        *Args:*
          <none>

        *Returns:*
         :int: number of Dives in this mission
        """
        return len(self.dives)

    def __getitem__(self, _slice):
        """slice operator

        usage examples:

          .. code-block:: python

              dive = my_mission[5]

          .. code-block:: python

              sublist = my_mission[2:8]

          .. code-block:: python

              sublist = my_mission[:5]

          .. code-block:: python

              sublist my_mission[-5:]

        *returns:*
          :Dive: Dive object

        or

          :list: a list of Dive objects if returns more than one value

        """
        return self.dives[_slice]

    def add_dive(self, dive_or_divelist):
        """add a Dive or a list of dive to the Mission

        they will be added at the end of the list

        *Keyword Arguments:*
            :dive_or_divelist: -- either on Dive object
                                  or a list of Dive object

        Return:
            <nothing>

        Raise:
            TypeError: if dive_or_divelist contains another type than Dive
        """
        if type(dive_or_divelist) == Dive:
            self.dives.append(dive_or_divelist)
        elif type(dive_or_divelist) == list:
            for dive in dive_or_divelist:
                if type(dive) == Dive:
                    self.dives.append(dive_or_divelist)
                else:
                    raise TypeError("Bad Dive Type: %s " % type(dive))
        else:
            raise TypeError("Bad Dive Type: %s " % type(dive_or_divelist))
