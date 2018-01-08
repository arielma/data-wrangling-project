#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    created = {}
    pos = [None,None]
    address = {}
    node_refs = []
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node['type'] = element.tag
        for key in element.attrib:
            if key in CREATED:

                created[key] = element.attrib[key]
            elif key == 'lat':
                pos[0] = float(element.attrib[key])
            elif key == 'lon':
                pos[1] = float(element.attrib[key])
            else:
                node[key] = element.attrib[key]
        if created:
            node['created'] = created
        if pos:
            node['pos'] = pos
        for child in element:
            if child.tag == 'nd':
                node_refs.append(child.attrib['ref'])
            else:
                if problemchars.search(child.attrib['k']):
                    pass
                elif child.attrib['k'].startswith('addr:') and lower_colon.search(child.attrib['k']):
                    address[child.attrib['k'].split(':')[1]] = child.attrib['v']
        if address:
            node['address'] = address
        if node_refs:
            node['node_refs'] = node_refs
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                print(el)
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    pass


if __name__ == "__main__":
    test()