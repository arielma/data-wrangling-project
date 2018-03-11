'''
In Australia, city name is not required to be in the address.
Therefore auditing the nodes to see if there is city in address tag and check the value of addr:city and addr:suburb.
If both addr:city and addr:suburb exist and have different value, audit_city_and_suburb() function will
print out the map with city names as the key and its suburb names as the values.
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
    both_exist = 0
    # number of nodes where only addr:city exists
    only_city = 0
    # number of nodes where only addr:suburb exists
    only_suburb = 0
    # number of notes where both addr:city and addr:suburb NOT exist
    both_not_exist = 0
    # number of nodes where addr:city and addr:suburb has the same value
    both_same_value = 0
    # number of nodes where addr:city and addr:suburb has different value.
    # Should equal to (both_exists - both_same_value)
    different_value = 0
    city_suburb = defaultdict(set)
    city = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            total_number_of_nodes += 1
            attrib_map = {}

            for tag in elem.iter("tag"):
                attrib_map[tag.attrib["k"]] = tag.attrib["v"]

            if "addr:city" in attrib_map and "addr:suburb" in attrib_map:
                both_exist += 1
                if attrib_map["addr:city"] == attrib_map["addr:suburb"]:
                    both_same_value += 1
                else:
                    different_value += 1
                    city_suburb[attrib_map["addr:city"]].add(attrib_map["addr:suburb"])
            elif "addr:city" in attrib_map and "addr:suburb" not in attrib_map:
                only_city += 1
                city.add(attrib_map["addr:city"])
            elif "addr:suburb" in attrib_map and "addr:city" not in attrib_map:
                only_suburb += 1
            elif "addr:suburb" not in attrib_map and "addr:city" not in attrib_map:
                both_not_exist += 1
    print("city suburb maps:")
    pprint.pprint(dict(city_suburb))
    print("city set:")
    pprint.pprint(city)
    print('total_number_of_nodes: {}\n both_exist: {}\n both_same_value: {}\n different_value: {}\n '
          'only_city: {}\n only_suburb: {}\n both_not_exists: {}'.
          format(total_number_of_nodes, both_exist, both_same_value, different_value, only_city, only_suburb,
                 both_not_exist))
    osm_file.close()


if __name__ == '__main__':
    audit_city_and_suburb(OSMFILE)