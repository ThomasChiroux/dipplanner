#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011-2012 Thomas Chiroux
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
"""module generating the GUI

It uses flask micro-framework to publish a full REST/json API over the
dipplanner objects and methods
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# imports

# dependencies imports
from flask import Flask
from flask import request
from flask.views import MethodView
from flask import make_response
from flask import Blueprint

# local imports
from dipplanner.tank import Tank
from dipplanner.mission import Mission

WEBAPP = Flask(__name__)


class TankApi(MethodView):
    """RestFull API for Tank Class
    """
    def __init__(self, name, mission):
        """Constructor for TankApi object

        *Keyword Arguments:*
            :name: (str) -- api name
            :mission: (Mission) -- mission object

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        self.name = name
        self.mission = mission
        bp = Blueprint(name, __name__)
        bp_endpoint = '{0}_api'.format(name)
        bp_url = '/{0}/'.format(name)
        bp_pk = '{0}_name'.format(name)
        self.register_api(bp, bp_endpoint, bp_url, bp_pk)
        self._blueprint = bp

    def register_api(self, blueprint, endpoint, url, p_key, pk_type=None):
        """register a REST Api for a dipplanner object

        *Keyword Arguments:*
            :app: (Flask) -- Flask application object
            :view: (MethodView) -- MethodView herited object
            :endpoint: (str) -- name for the view
            :url: (str) -- base url for the api
            :p_key: (str) -- primary key name
            :pk_type: (str) -- type of primary key

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        view_func = self.as_view(endpoint, self.name, self.mission)
        blueprint.add_url_rule(url, defaults={p_key: None},
                               view_func=view_func, methods=['GET', ])
        blueprint.add_url_rule(url, view_func=view_func, methods=['POST', ])
        if pk_type is None:
            blueprint.add_url_rule('%s<%s>' % (url, p_key),
                                   view_func=view_func,
                                   methods=['GET', 'PUT', 'PATCH', 'DELETE'])
        else:
            blueprint.add_url_rule('%s<%s:%s>' % (url, pk_type, p_key),
                                   view_func=view_func,
                                   methods=['GET', 'PUT', 'PATCH', 'DELETE'])

    def json_resp(self, message, code):
        """Return a pure json Flask response with
        application/json content type and message

        *Keyword Arguments:*
            :message: (str) -- json message

            .. note :: this method does not validate the correctness of the
                       json message : this must be done before

            :code: (int) -- http response code

        *Returns:*
            resp -- Flask response objec

        *Raise:*
            <nothing>
        """
        resp = make_response(message, code)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def get(self, tank_name):
        """GET method for the Tank object Api

        *Keyword Arguments:*
        :tank_name: (str) -- name of the tank (or None if no tank name is
                             provided)

        *Returns:*
            resp -- Flask response object: either:
            * list of tanks if no tank_name is given
            * tank datas if tank_name is given

        *Raise:*
            <nothing>
        """
        if tank_name is None:
            return self.json_resp('', 200)
        else:
            return self.json_resp(self.mission[0].tanks[0].dumps_json(), 200)

    def post(self):
        """POST method for the Tank object Api

        *Keyword Arguments:*
            <nothing>

        *Returns:*
            resp -- Flask response object with the json dump of the newly
                    created object

        *Raise:*
            <nothing>
        """
        print 'post tank'
        if request.headers['Content-Type'] == 'application/json':
            temp_tank = Tank()
            temp_tank.loads_json(request.json)
            return self.json_resp(temp_tank.dumps_json(), 201)
        else:
            return self.json_resp('{ "message": "400: Bad ContentType" }',
                                  400)

    def put(self, tank_name):
        """PUT method for the Tank object Api

        *Keyword Arguments:*
        :tank_name: (str) -- name of the tank (MANDATORY)

        *Returns:*
            resp -- Flask response object with the json dump of the
                    updated object

        *Raise:*
            <nothing>
        """
        temp_tank = Tank()
        print 'put tank: %s' % tank_name
        return self.json_resp(temp_tank.dumps_json(), 201)

    def patch(self, tank_name):
        """PATCH method for the Tank object Api

        *Keyword Arguments:*
        :tank_name: (str) -- name of the tank (MANDATORY)

        *Returns:*
            resp -- Flask response object with the json dump of the
                    updated object

        *Raise:*
            <nothing>
        """
        temp_tank = Tank()
        print 'patch tank: %s' % tank_name
        return self.json_resp(temp_tank.dumps_json(), 200)

    def delete(self, tank_name):
        """DELETE method for the Tank object Api

        *Keyword Arguments:*
        :tank_name: (str) -- name of the tank (MANDATORY)

        *Returns:*
            resp -- Flask response object (empty)

        *Raise:*
            <nothing>
        """

        #temp_tank = Tank()
        print 'delete tank: %s' % tank_name
        return self.json_resp('', 204)


def start_gui(mission=None):
    """Starts the html GUI server
    """
    if mission is None:
        tank_api = TankApi('tank', Mission())
    else:
        tank_api = TankApi('tank', mission)
    WEBAPP.register_blueprint(tank_api._blueprint)
    WEBAPP.run(debug=True)  # TODO: remove debug infos before release

if __name__ == "__main__":
    # for debug purposes
    start_gui()