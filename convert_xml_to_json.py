import xml.etree.cElementTree as ET
import auditing_street_types
import auditing_suburb_names

import re
import codecs
import json
import pprint

OSMFILE = "melbourne_australia.osm"
SAMPLE_FILE = "sample.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


# Update wrong street types based on map created in auditing_street_types.py
def update_street_type(street_address):
    street_type = street_address.split(' ')[-1]
    if street_type in auditing_street_types.street_type_mapping:
        street_address = street_address.replace(street_type, auditing_street_types.street_type_mapping[street_type])
    return street_address


# Update wrong city/suburb names based on map created in auditing_suburb_names.py
def update_suburb_name(suburb_name):
    if suburb_name in auditing_suburb_names.suburb_name_mapping:
        suburb_name = auditing_suburb_names.suburb_name_mapping[suburb_name]
    return suburb_name


def update_addr(element):
    if element.tag == "node" or element.tag == "way":
        for tag in element.iter("tag"):
            if auditing_street_types.is_street_name(tag):
                tag.attrib['v'] = update_street_type(tag.attrib['v'])
            elif auditing_suburb_names.is_suburb_name(tag):
                tag.attrib['v'] = update_suburb_name(tag.attrib['v'])


# If both addr:city and addr:suburb existing in tags, then remove addr:city element;
# If addr:city exists and addr:suburb not exists, then replace addr:city with addr:suburb.
def improve_addr(element):
    if element.tag == "node" or element.tag == "way":
        attrib_list = [tag.attrib["k"] for tag in element.iter('tag')]
        if 'addr:city' in attrib_list and 'addr:suburb' in attrib_list:
            element.remove(element.find(".//tag[@k='addr:city']"))
        elif 'addr:city' in attrib_list and 'addr:suburb' not in attrib_list:
            element.find(".//tag[@k='addr:city']").attrib['k'] = 'addr:suburb'


# Converting xml element to dictionary
def shape_element(element):
    node = {}
    created = {}
    pos = [None, None]
    address = {}
    node_refs = []
    if element.tag == "node" or element.tag == "way":
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
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            update_addr(element)
            # Remove redundant addr:city tag
            improve_addr(element)
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == '__main__':
    data = process_map(OSMFILE, True)
    pprint.pprint(data)

