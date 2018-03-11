"""
A CSV file of Melbourne suburbs can be downloaded from
http://www.corra.com.au/australian-postcode-location-data/.

The file is downloaded with name Australian_Post_Codes_Lat_Lon.csv

Function import_melbourne_suburbs will return a list of suburbs extracted from the csv file.

Suburbs and cities in the OSMFILE in elements where key value is addr:suburb or addr:city will be compared against
the result returned by import_melbourne_suburbs function.

A map will be generated manually with wrong suburb/city name as key and right suburb/city name as value.
"""

import csv
import xml.etree.cElementTree as ET

OSMFILE = "melbourne_australia.osm"
SAMPLE_FILE = "sample.osm"

# Manually updated based on output of audit()
suburb_name_mapping = {'Mount Waverly': 'Mount Waverley',
                       'South Vermont': 'Vermont South',
                       'Lascelle Drive': 'Vermont South',
                       'Canerbury': 'Canterbury',
                       'Caufield East': 'Caulfield East',
                       'Surrey hills': 'Surrey Hills',
                       '3053': 'Carlton',
                       '93748000': 'Essendon Fields',
                       'Ashvwood': 'Ashwood',
                       'Balwyn Street': 'Balwyn North',
                       'Industrial Gardens': 'Lilydale',
                       'Burwood Street': 'Burwood East',
                       'West Preston': 'Preston West',
                       'Wandin North, Vic': 'Wandin North',
                       'Melboure': 'Melbourne',
                       'rosebud': 'Rosebud',
                       'Boxhill South': 'Box Hill South',
                       'coldstream': 'Coldstream',
                       'Albert Park?': 'Albert Park',
                       'Mount Waverley, VIC.': 'Mount Waverley',
                       'Fishermans Bend': 'Port Melbourne',
                       'Wheeler''s Hill': 'Wheelers Hill',
                       'North Bayswater': 'Bayswater North',
                       'mordialloc': 'Mordialloc',
                       'Pot Melbourne ': 'Port Melbourne',
                       'balaclava': 'Balaclava',
                       'Bayswater Nth': 'Bayswater North',
                       'Norlane ': 'Norlane',
                       'Mt Burnett': 'Mount Burnett',
                       'Port Melboune': 'Port Melbourne',
                       'footscray': 'Footscray',
                       'Bentleigh East, Victoria': 'Bentleigh East',
                       'MITCHAM': 'Mitcham',
                       'South Melboune': 'South Melbourne',
                       'storage': 'Collingwood',
                       'Rosebud West': 'Capel Sound',
                       '14': 'Wheelers Hill',
                       'West footscray': 'West Footscray',
                       'Moorabbin, Melbourne': 'Moorabbin',
                       'reservoir': 'Reservoir',
                       'ocean grove': 'Ocean Grove',
                       'keysborough': 'Keysborough',
                       'StKilda': 'St Kilda',
                       'Ringwood east': 'Ringwood East',
                       'Officer ': 'Officer',
                       'JAN JUC': 'Jan Juc',
                       'Aspendale gardens': 'Aspendale Gardens',
                       'Donvalo': 'Donvale',
                       'Moridalloc': 'Mordialloc',
                       'Hughsdale': 'Hughesdale',
                       'point cook': 'Point Cook',
                       'Port Melborne': 'Port Melbourne',
                       'Maribynrong': 'Maribyrnong',
                       'North Balwyn': 'Balwyn North',
                       'flemington': 'Flemington',
                       'East Reservoir': 'Reservoir East',
                       'Epping North': 'Epping',
                       'Port Melbb': 'Port Melbourne',
                       'KINGLAKE': 'Kinglake',
                       'Wyndhamvale': 'Wyndham Vale',
                       'East Bentleigh': 'Bentleigh East',
                       'North Laverton': 'Laverton North',
                       'North Fiztroy': 'Fitzroy North',
                       'Newton': 'Newtown',
                       'lynbrook': 'Lynbrook',
                       'St. Kilda': 'St Kilda',
                       'West Brunswick': 'Brunswick West',
                       '3763': 'Kinglake',
                       'Hignton': 'Highton',
                       'bayswater North': 'Bayswater North',
                       'Campellfield': 'Campbellfield',
                       'st Kilda': 'St Kilda',
                       'South Oakleigh': 'Oakleigh South',
                       'nORLANE': 'Norlane',
                       'Mt Evelyn': 'Mount Evelyn',
                       'Port Melbourne ': 'Port Melbourne',
                       'Kinglike Central': 'Kinglake Central',
                       'Pakenahm': 'Pakenham',
                       'moonee ponds': 'Moonee Ponds',
                       'Campbellfield.': 'Campbellfield',
                       'Dandenong Southe': 'Dandenong South',
                       'East Keilor': 'Keilor East',
                       'Casey Fields': 'Clyde North',
                       'mount Waverley': 'Mount Waverley',
                       'dandenong': 'Dandenong',
                       'Warburton East': 'Warburton',
                       'Monash University, Clayton': 'Clayton',
                       'East Brunswick': 'Brunswick East',
                       'East Burwood': 'Burwood East',
                       'Hightn': 'Highton',
                       'Andrews': 'St Andrews',
                       'clayton': 'Clayton',
                       'Cauflield East': 'Caulfield East',
                       'camberwell': 'Camberwell',
                       'DIamond Creek': 'Diamond Creek',
                       'south Yarra': 'South Yarra',
                       'Templsestowe Lower': 'Templestowe Lower',
                       'North Melboune': 'North Melbourne',
                       'Albert Park, Melbourne': 'Albert Park',
                       'Port  Melbourne': 'Port Melbourne',
                       'Braesude': 'Braeside',
                       'North Fitzroy': 'North Fitzroy'}


# read csv file and get suburb names in Melbourne
def import_melbourne_suburbs():
    with open('Australian_Post_Codes_Lat_Lon.csv', "r") as suburb_file:
        reader = csv.DictReader(suburb_file)
        full_data = [line for line in reader]
        # Filter the file to only import Victoria suburbs.
        # suburb names in the CSV file are all capitalised. To make it in camel case, using title()
        return [suburb['suburb'].title() for suburb in full_data if suburb['state'] == 'VIC'
                and suburb['type'].strip() == 'Delivery Area']


def audit_suburb(suburbs, suburb_name):
    if suburb_name not in import_melbourne_suburbs():
        suburbs.add(suburb_name)


def is_suburb_name(elem):
    return elem.attrib['k'] == "addr:suburb" or elem.attrib['k'] == 'addr:city'


def audit_suburb_names(osmfile):
    osm_file = open(osmfile, "r")
    unexpected_suburbs = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_suburb_name(tag):
                    audit_suburb(unexpected_suburbs, tag.attrib['v'])
    osm_file.close()
    print(unexpected_suburbs)
    return unexpected_suburbs


if __name__ == '__main__':
    audit_suburb_names(SAMPLE_FILE)
