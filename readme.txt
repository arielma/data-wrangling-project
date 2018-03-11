##Directory
data_wrangling_case_studt_MongoDB
This is the directory of all case study quizzes

##Files

Data Wrangling Project.pdf
Documenting my work of the project.

map_region.txt
A description of the map area I am using and the download link of the OSM file.

generate_sample_osm.py
The code provided with the project to generate sample OSM file.

sample.osm
Sample file created using generate_sample_osm.py


auditing_street_types.py
Auditing street types and generate a map with unexpected street types as keys and correct street type as values.
This map will be used later in the cleaning step.

auditing_cities.py
Checking the value of k=addr:city attribute and finding out if the value is correct.


Australian_Post_Codes_Lat_Lon.csv
This file will be filtered down to Melbourne suburbs and imported as a standard list of Melbourne suburb names.
This imported list will be used when auditing suburb/city names.


auditing_suburb_city_names.py
Auditing suburb and city names by comparing with value of suburb and city names with a standard list of Melbourne suburbs.
This code generates a map with unexpected suburb/city names as key and correct suburb/city names as values.
This map will be used later in the cleaning step.


convert_xml_to_json.py
Cleaning street types, suburb/city names and removing unnecessary tags. Converting cleaned data into JSON and generate JSON file.

references.txt
References used to complete the project.


