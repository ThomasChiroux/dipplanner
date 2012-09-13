#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import sys
import codecs

import dipplanner.tank

UDDF_XSD = './uddf_3.1.0.xsd'

# use custom parser removing comments (makes it much easier while developping)
parser = etree.XMLParser(remove_blank_text = True, remove_comments = True)
etree.set_default_parser(parser)

class Gas(object):
    def __init__(self, f_o2 = 0.21, f_he = 0.0):
        self.f_o2 = f_o2
        self.f_he = f_he

    def parse(self, xml_node):
        self.f_o2 = float(xml_node.find('o2').text)
        self.f_he = float(xml_node.find('he').text)
        return self

class Tank(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

class UDDF(object):
    def __init__(self, xsd = UDDF_XSD):
        self.xsd = xsd

        self.tank = {}
        self.mix = {}

    def load(self, filename, encoding):
        # build XMLSchema
        uddf_schema = etree.XMLSchema(etree.parse(self.xsd))

        # load xml file into an XML tree
        with open(filename) as input_file:
            xml_data = unicode(input_file.read(), encoding)
        self.xml = etree.fromstring(xml_data)

        # load references for gasdefinitions/mix links
        for mix in self.xml.xpath('gasdefinitions/mix'):
            self.mix[mix.get('id')] = mix

        # load references for tank links
        for tank in self.xml.xpath('diver/owner/equipment/tank'):
            self.tank[tank.get('id')] = tank

        # validate file against self.xsd
        # TODO: should probably embeded in a try/except statement
        uddf_schema.validate(self.xml)

    def getTankData(self):
        # very very dipplanner oriented!
        tankData = {}
        for data in self.xml.xpath('profiledata/repetitiongroup/dive/tankdata'):
            tank = Tank()
            gas = None
            tank_ref = None
            for c in data.getchildren():
                if c.tag == 'link':
                    idref = c.get('ref')
                    gas = self.mix.get(idref, gas)
                    tank_ref = self.tank.get(idref, tank_ref)
                else:
                    tank[c.tag] = float(c.text)

            # should always have a gas here
            tank['gas'] = Gas().parse(gas)

            # if linked to a tank, get its volume
            if tank_ref is not None:
                tank['tankvolume'] = float(tank_ref.find('tankvolume').text)
            tankData[data.get('id')] = tank
        return tankData


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print """usage: %s uddf_file [encoding]""" % sys.argv[0]
        raise SystemExit(1)

    input_file = sys.argv[1]
    try:
        input_encoding = sys.argv[2]
    except IndexError:
        input_encoding = 'utf-8'

    # load UDDF file
    uddf = UDDF()
    uddf.load(input_file, input_encoding)

    # retrieve tank list from uddf file
    tankData = uddf.getTankData()

    # for fun, build some dipplanner.tank.Tank instances
    ttank = []
    for k in tankData.keys():
        t = tankData[k]
        print str(k) + " " + str(t)
        ttank.append(dipplanner.tank.Tank(f_o2 = t['gas'].f_o2, f_he = t['gas'].f_he, tank_vol = 1000 * t['tankvolume'], tank_pressure = t['tankpressurebegin'] * 0.0000101325))

    print ttank

# vim: et ts=4