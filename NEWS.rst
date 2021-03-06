Release Notes
=============

v0.3 (ongoing)
--------------

.. note::
    v0.3 is not released yet.

    Below are the feature already developed for the 0.3 target release.

    See GitHub Issues for more infos.

Python
******

* dipplanner is now (only) python 3.4+ compatible
  now old python 2.7 compatible version is frozen in py2.7 branch.

New features
************

* No-flight time calculation
* non-blocking dive situations errors

Bug corrections
***************

* tank infos on repetitive dives was wrong (only last tank status was
  diven, even for the firs(s) dive(s).

v0.2
----

New features
************

* New submodel: buhlmann ZH-L16C
* Handle repetitive dives
* Variable ppH2O in surface based on Temp and % humidity
* Limit CCR dive depth based on diluant values
* Export dive plannification in different format
* Config Files
* Tanks:
    * More accurate calculation of tank volume
    * minimum gas remaining rules in tanks
    * handle double tanks

Bug corrections
***************

* Automatic gas selection was not well handled on Hypoxic trimix dives

v0.1
----

New features
************

* Same 'base' functionnality as MVPlan (v1.5):
    * buhlmann ZH-L16B
    * mv-value gradient conservatism (adjustable)
    * oxygen toxicity (OTU and CNS) calculation
    * support Open Circuit dives : air, nitrox, trimix, heliox...
    * support CCR dives with OC deco/bailout if wanted
    * support dive in altitude
    * automatic selection of deco when ascending
    * ...
* But some differences:
    * command line only (or direct use in python) : no GUI, no automatic update
    * only in english
    * the unit system is only SI:
        * meter
        * seconds
        * bar (almost SI: 1 bar = 10E5 pascal)
        * liter (dm3)
    * Uses 'Tanks' instead of 'Gases' in order to calculate gas consumption for each tank and raise error when dive reach empty tank
    * All time parameters and calculations are by default in seconds instead of minutes
    * the END 'Equivalent Narcosis depth' is calculated based on narcosis index of every breathed gases (N2, He and O2) instead of the 'Only N2 is narcotic' in MVPlan
    * water pressure is by default calculated using the 'real pressure' of water (wich can change between fresh or sea water) instead of '10m == 1bar'
