'''
In Australia, city name is not required to be in the address.
Therefore auditing the nodes to see if there is city in address tag and check the value of addr:city and addr:suburb.
If both addr:city and addr:suburb exist and have different value, audit_city_and_suburb() function will
print out the map with city names as the key and its suburb names as the values.

Observing this map, the city names do not reflect the right city names of the suburb, therefore when converting xnl to json,
I will not include addr:city tag
'''

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

OSMFILE = "melbourne_australia.osm"
SAMPLE_FILE = "sample.osm"


def audit_city_and_suburb(osmfile):
    osm_file = open(osmfile, "r")
    total_number_of_nodes = 0
    # number of nodes where both addr:city and addr:suburb exist
    both_exists = 0
    # number of nodes where only addr:city exists
    only_city = 0
    # number of nodes where addr:city and addr:suburb has the same value
    both_same_value = 0
    # number of nodes where addr:city and addr:suburb has different value.
    # Should equal to (both_exists - both_same_value)
    different_value = 0
    city_suburb = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            total_number_of_nodes += 1
            attrib_map = {}

            for tag in elem.iter("tag"):
                attrib_map[tag.attrib["k"]] = tag.attrib["v"]

            if "addr:city" in attrib_map and "addr:suburb" in attrib_map:
                both_exists += 1
                if attrib_map["addr:city"] == attrib_map["addr:suburb"]:
                    both_same_value += 1
                else:
                    different_value += 1
                    city_suburb[attrib_map["addr:city"]].add(attrib_map["addr:suburb"])
            elif "addr:city" in attrib_map and "addr:suburb" not in attrib_map:
                only_city += 1
                print(attrib_map["addr:city"])

    pprint.pprint(dict(city_suburb))
    print('total_number_of_nodes: {}\n both_exists: {}\n both_same_value: {}\n different_value: {}\n only_city: {}'.
          format(total_number_of_nodes, both_exists, both_same_value, different_value, only_city))
    osm_file.close()


if __name__ == '__main__':
    audit_city_and_suburb(OSMFILE)