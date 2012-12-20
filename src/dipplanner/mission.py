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

import logging
import json
from collections import OrderedDict

# local imports
from dipplanner import settings
#from dipplanner.python_tools import Singleton
from dipplanner.dive import Dive, Tank


class Mission(object):
    """Mission Class

    a Mission represent all repetitive dives for a given set of time.
    the Mission will keep consistency between repetitive dives

    An isolated dive is a Mission with only one dive inside

    Attributes:
        tanks (dict) -- list of each individual tank used (at least once)
                        during the mission.
        dives (list) -- list of Dive object of the same mission
        description (str) -- description of the mission (OPTIONAL)
        status (???) -- actual status of the mission. Could be either:

        * STATUS_NONE: not calculated
        * STATUS_CHANGED: changed (calculated, but something in input or parameter has changed
          and recalculation is needed)
        * STATUS_OK: calculated (calculation is up to date)


    .. todo:: Insert dive(s) in a certain position

    .. todo:: change dive order, permutations, etc...

    .. todo:: decide if we define a common list of tanks for a given mission
              in this case, each dive will be able to pickup some tank

    .. todo:: decide if settings is included in Mission object or remains
              global

    """
    # Singleton metaclass was necessary for Flask, but is not for bottle (?)
    #__metaclass__ = Singleton

    STATUS_NONE = "Not Calculated"
    STATUS_CHANGED = "Calculated but Changed"
    STATUS_OK = "Calculated and Up to date"

    def __init__(self, dive_or_divelist=None,
                 tank_or_tankdict=None, description=None):
        """Mission constructor

        Initialize the Mission object
        if no parameter is given, instantiate an 'empty' Mission

        *Keyword Arguments:*
            :dive_or_divelist: -- either a Dive object
                                  or a list of Dive object
            :tank_or_tankdict: -- either a Tank object
                                  or a dict of tanks
            :description: (str)-- description of the Mission

        Return:
            <nothing>

        Raise:
            TypeError: if dive_or_divelist contains another type than Dive
        """
        self.logger = logging.getLogger("dipplanner.dive.Dive")
        self.logger.debug("creating an instance of Mission")

        self.settings = settings
        self.tanks = {}
        self.dives = OrderedDict()
        self.description = description
        self.status = self.STATUS_NONE
        if tank_or_tankdict is not None:
            self.add_tank(tank_or_tankdict)
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

    def dumps_dict(self):
        """dumps the Mission object in json format

        *Keyword arguments:*
            <none>

        *Returns:*
            string -- json dumps of Tank object

        *Raise:*
            TypeError : if Mission is not serialisable
        """
        mission_dict = {'description': self.description,
                        'dives': [dive.dumps_dict() for dive in self.dives]}

        return mission_dict

    def loads_json(self, input_json):
        """loads a json structure and update the tank object with the new
        values.

        This method can be used in http PUT method to update object
        value

        *Keyword arguments:*
            :input_json: (string) -- the json structure to be loaded

        *Returns:*
            <none>

        *Raise:*
            * ValueError : if json is not loadable
        """
        if type(input_json) == str:
            mission_dict = json.loads(input_json)
        elif type(input_json) == dict:
            mission_dict = input_json
        else:
            raise TypeError("json must be either str or dict (%s given"
                            % type(input_json))

        if 'description' in mission_dict:
            self.description = mission_dict['description']
        if 'dives' in mission_dict:
            temp_dives = []
            for dict_dive in mission_dict['dives']:
                temp_dives.append(Dive().loads_json(dict_dive))
            self.dives = temp_dives
        return self

    def clean(self, what='all'):
        """clean the mission

        *Keyword arguments:*
            :what: (str) -- what the method should clean
                by default: all (clean all)
                Values allowed: ['all', 'dives', 'description', ]

        *Returns:*
            <none>

        *Raise:*
            * ValueError : if wrong status code is given
        """
        if what == 'all':
            self.tanks = {}
            self.dives = []
            self.description = ""
            self.status = self.STATUS_NONE
        elif what == 'dives':
            self.dives = []
            self.status = self.STATUS_NONE
        elif what == 'tanks':
            self.tanks = {}
            self.status = self.STATUS_NONE
        elif what == 'description':
            self.description = ""

    def change_status(self, status=None):
        """Change the status of the mission

        if no status is given in args, toggle the status from OK to
        CHANGED
        else, update the status with the given value

        *Keyword arguments:*
            :status: (str) -- status code (optionnal)

        *Returns:*
            <none>

        *Raise:*
            * ValueError : if wrong status code is given
        """
        if status is None:
            if self.status == self.STATUS_OK:
                self.status = self.STATUS_CHANGED
        elif status == self.STATUS_NONE:
            self.status = status
        elif status == self.STATUS_CHANGED:
            self.status = status
        elif status == self.STATUS_OK:
            self.status = status
        else:
            raise ValueError("Wrong status code")

    def add_dive(self, dive_or_divelist):
        """add a Dive or a list of dive to the Mission

        they will be added at the end of the list

        *Keyword Arguments:*
            :dive_or_divelist: -- either a Dive object
                                  or a list of Dive objects

        Return:
            <nothing>

        Raise:
            TypeError: if dive_or_divelist contains another type than Dive
        """
        if type(dive_or_divelist) == Dive:
            self.dives[dive_or_divelist.name] = dive_or_divelist
        elif type(dive_or_divelist) == list:
            for dive in dive_or_divelist:
                if type(dive) == Dive:
                    self.dives[dive.name] = dive
                else:
                    raise TypeError("Bad Dive Type: %s " % type(dive))
        else:
            raise TypeError("Bad Dive Type: %s " % type(dive_or_divelist))

    def add_tank(self, tank_or_tankdict):
        """add a Tank or a dict of tanks to the Mission

        if a tank already exists in the dict with the same name, the new
        one will not be added.

        *Keyword Arguments:*
            :tank_or_tanklist: -- either a Tank object
                                  or a list of Tank objects

        Return:
            <nothing>

        Raise:
            TypeError: if tank_or_tanklist contains another type than Tank
        """
        if type(tank_or_tankdict) == Tank:
            self.dives.append(tank_or_tankdict)
        elif type(tank_or_tankdict) == dict:
            for tank_name, tank in tank_or_tankdict:
                if type(tank) == Tank:
                    if tank_name not in self.tanks:
                        self.tanks[tank_name] = tank
                    else:
                        self.logger.error("Same tank name already exists for"
                                          " this mission... "
                                          "ignoring current tank")
                else:
                    raise TypeError("Bad Tank Type: %s " % type(tank))
        else:
            raise TypeError("Bad Tank Type: %s " % type(tank_or_tankdict))

    def calculate(self):
        """Calculate all the decompression planning for all dives in this
        mission

        """
        if len(self.dives) > 0:
            previous_dive = None
            for dive in self.dives.values():
                if previous_dive is not None:
                    # make a copy of the model, to keep the previous_dive
                    # model inchanged by further calculations
                    dive.set_repetitive(previous_dive)
                    dive.do_surface_interval()
                dive.do_dive_without_exceptions()
                previous_dive = dive

            # now calculate no flight time based on the last dive
            if previous_dive is not None:
                previous_dive.no_flight_time_wo_exception()
            self.status = self.STATUS_OK
