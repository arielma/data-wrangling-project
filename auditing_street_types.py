"""
audit function will audit the OSMFILE and return a dictionary of unexpected street types as keys and
street names containing the unexpected street types as values.

The variable 'expected_street_types' will be created manually based on the extracted street type list.
The variable 'street_type_mapping' will be manually created to reflect the changes needed to fix
the unexpected street types to the appropriate ones in the expected list.

"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "melbourne_australia.osm"
SAMPLE_FILE = "sample.osm"

# Regex to match the very last word in a street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected_street_types = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Crescent", "Alley", "Arcade", "Circle", "Circuit",
            "Close", "Grove", "Highway", "Parade", "Rise", "Terrace", "Walk", "Way", "West", "East", "North", "South"]

# UPDATE THIS VARIABLE
street_type_mapping = { "Ave": "Avenue",
            "Av": "Avenue",
            "Avp": "Avenue",
            "avenue": "Avenue",
            "Dr,": "Drive",
            "Dr.": "Drive",
            "Rd": "Road",
            "Ro": "Road",
            "Road1": "Road",
            "Roah": "Road",
            "Roađ": "Road",
            "Rd.": "Road",
            "rd": "Road",
            "road": "Road",
            "St": "Street",
            "St.": "Street",
            "Stree": "Street",
            "Street.": "Street",
            "street": "Street",
            "way": "Way",
            "W": "West"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street_types:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"


def audit_street_types(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    # Get the last word in address split by single whitespace
    bad_street_type = name.split(' ')[-1]
    if bad_street_type in mapping:
        name = name.replace(bad_street_type, mapping[bad_street_type])
    return name


def test():
    st_types = audit_street_types(OSMFILE)
    pprint.pprint(dict(st_types))

    # for st_type, ways in st_types.iteritems():
    #     for name in ways:
    #         better_name = update_name(name, street_type_mapping)
    #         print(name, "=>", better_name)
    #         if name == "West Lexington St.":
    #             assert better_name == "West Lexington Street"
    #         if name == "Baldwin Rd.":
    #             assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()