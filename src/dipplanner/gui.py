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

# local imports
from dipplanner.tank import Tank

WEBAPP = Flask(__name__)


class TankApi(MethodView):
    """RestFull API for Tank Class
    """

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
        temp_tank = Tank()
        print 'get tank: %s' % tank_name
        return self.json_resp(temp_tank.dumps_json(), 200)

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


def register_api(app, view, endpoint, url, p_key, pk_type=None):
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
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={p_key: None},
                     view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    if pk_type is None:
        app.add_url_rule('%s<%s>' % (url, p_key), view_func=view_func,
                         methods=['GET', 'PUT', 'PATCH', 'DELETE'])
    else:
        app.add_url_rule('%s<%s:%s>' % (url, pk_type, p_key),
                         view_func=view_func,
                         methods=['GET', 'PUT', 'PATCH', 'DELETE'])

if __name__ == "__main__":
    register_api(WEBAPP, TankApi,
                 'tank_api', '/tank/',
                 'tank_name', pk_type=None)
    WEBAPP.run(debug=True)
