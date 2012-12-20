.. _dipplanner_templates:

Templates
=========

dipplanner uses Jinja2 template engine.

For all documentation about jinja2, please see `their own documentation <http://jinja.pocoo.org/docs/>`_

This document will focus on dipplanner objects sent to jinja2 templating system and
how to use them.

dipplanner sends two objects to the template engine:

* settings: contains all the parameters used for the dives
* [Dive, ...]: a list of Dive objects

It only one dive is calculated, dipplanner still send a list of dive, with one element in the list.

Settings will be usefull to display some dive parameters, like configured GF for example:

::

    Configuration : GF:{{ settings.GF_LOW*100 }}-{{ settings.GF_HIGH*100 }}

mission
-------

the main object passed in template is the mission object.
It contains:

* mission.tanks: the tank dictionnary defined for the mission
* mission.dives: the dives dictionnary
* mission.settings: the global settings for the mission

dives
-----

Dives are in the mission.
To easilly iterate dive, you can use the following snippet:

::

    {% for dive in mission.dives.values() %}

    ...

    {% endfor %}

Dive attributes are described here: :ref:`dipplanner_autodoc_dive`

settings
--------

settings attributes are described here: :ref:`dipplanner_autodoc_settings`