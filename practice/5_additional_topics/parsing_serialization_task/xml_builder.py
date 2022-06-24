"""
For this task, you should write a script that will build the XML file which describes the weather in Spain
for September 25, 2021 with set of parameters:

-mean, minimum, maximum temperature
-mean, minimum, maximum wind speed.

Find the warmest, the coldest and the windiest city in Spain for that date
and include them in the XML file.

17 Folder -> 17 JSON with hourly weather data for September 25, 2021

- General:
    - Field **hourly**: a list of dictionaries with weather data for each hour.
    - Field **temp** in dictionary of hour weather data: temperature.
    - Field **wind_speed** in dictionary of hour weather data: wind speed.

## Steps

1. Parse hourly data from JSON files for each city. Don’t forget to remember names of cities.
2. Calculate mean, maximum, minimum temperature and wind speed for each city.
3. Calculate mean temperature and wind speed  for the whole country by using produced data before. Find the coldest, the warmest and the windiest cities in Spain (you must use mean values from step 2 to do that).
4. Create an XML file with a specific structure and write calculated values in it.

Output XML file structure

- Root element **weather**
  - attribute **country**: country name
  - attribute **date**: date of observation (ex. “2021-09-25”).


  - Child element **summary** (parent: **weather**)
    - attribute **mean_temp**: country’s mean temperature
    - attribute **mean_wind_speed**: country’s mean wind speed
    - attribute **coldest_place**: name of the city with the lowest mean temperature value
    - attribute **warmest_place**: name of the city with the highest mean temperature value
    - attribute **windiest_place**: name of the city with the highest mean wind speed value


  - Child element **cities** (parent: **weather**)
    - collection of child elements with city name as tag (parent: **cities**):
      - attribute **mean_temp**: city’s mean temperature
      - attribute **max_temp**: city’s max temperature
      - attribute **min_temp**: city’s min temperature
      - attribute **mean_wind_speed**: city’s mean wind speed
      - attribute **max_wind_speed**: city’s max wind speed
      - attribute **min_wind_speed**: city’s min wind speed

All decimal values must be rounded to 2 decimal places.
"""
from lxml import etree
import glob
import json
import statistics

# Root element
root = etree.Element('weather')
# Root element attributes
root.set('country', 'Spain')
root.set('date', '2021-09-25')
# Summary element
summary = etree.SubElement(root, 'summary')
# Cities element
cities = etree.SubElement(root, 'cities')


# Make a list to save all abs path for json files
files = glob.glob(
    r'/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/5_additional_topics/parsing_serialization_task/source_data/*/*.json',
    recursive=True)

# Make a dict to save all temperatures from json files
cities_temp = {'Barcelona': [], 'Logrono': [], 'Madrid': [], 'Merida': [], 'Murcia': [], 'Oviedo': [], 'Palma': [],
               'Pamplona': [], 'Santa_Cruz_de_Tenerife': [],
               'Santander': [], 'Santiago_de_Compostela': [], 'Seville': [], 'Toledo': [], 'Valencia': [],
               'Valladolid': [], 'Vitoria-Gasteiz': [], 'Zaragoza': []}

# Make a dict to save all wind speeds from json files
cities_wind = {'Barcelona': [], 'Logrono': [], 'Madrid': [], 'Merida': [], 'Murcia': [], 'Oviedo': [], 'Palma': [],
               'Pamplona': [], 'Santa_Cruz_de_Tenerife': [],
               'Santander': [], 'Santiago_de_Compostela': [], 'Seville': [], 'Toledo': [], 'Valencia': [],
               'Valladolid': [], 'Vitoria-Gasteiz': [], 'Zaragoza': []}

# Make a dict to save all mean temperatures from json files
cities_mean = {'Barcelona': int, 'Logrono': int, 'Madrid': int, 'Merida': int, 'Murcia': int, 'Oviedo': int,
               'Palma': int, 'Pamplona': int, 'Santa_Cruz_de_Tenerife': int,
               'Santander': int, 'Santiago_de_Compostela': int, 'Seville': int, 'Toledo': int, 'Valencia': int,
               'Valladolid': int, 'Vitoria-Gasteiz': int, 'Zaragoza': int}

# Make a dict to save all mean wind speeds from json files
cities_mean_wind = {'Barcelona': int, 'Logrono': int, 'Madrid': int, 'Merida': int, 'Murcia': int, 'Oviedo': int,
                    'Palma': int, 'Pamplona': int, 'Santa_Cruz_de_Tenerife': int,
                    'Santander': int, 'Santiago_de_Compostela': int, 'Seville': int, 'Toledo': int, 'Valencia': int,
                    'Valladolid': int, 'Vitoria-Gasteiz': int, 'Zaragoza': int}

# Make a dict to save all maximum temperatures from json files
cities_max_temp = {'Barcelona': int, 'Logrono': int, 'Madrid': int, 'Merida': int, 'Murcia': int, 'Oviedo': int,
                   'Palma': int, 'Pamplona': int, 'Santa_Cruz_de_Tenerife': int,
                   'Santander': int, 'Santiago_de_Compostela': int, 'Seville': int, 'Toledo': int, 'Valencia': int,
                   'Valladolid': int, 'Vitoria-Gasteiz': int, 'Zaragoza': int}

# Make a dict to save all minimum temperatures from json files
cities_min_temp = {'Barcelona': int, 'Logrono': int, 'Madrid': int, 'Merida': int, 'Murcia': int, 'Oviedo': int,
                   'Palma': int, 'Pamplona': int, 'Santa_Cruz_de_Tenerife': int,
                   'Santander': int, 'Santiago_de_Compostela': int, 'Seville': int, 'Toledo': int, 'Valencia': int,
                   'Valladolid': int, 'Vitoria-Gasteiz': int, 'Zaragoza': int}

# Make a dict to save all maximum wind speeds from json files
cities_max_wind = {'Barcelona': int, 'Logrono': int, 'Madrid': int, 'Merida': int, 'Murcia': int, 'Oviedo': int,
                   'Palma': int, 'Pamplona': int, 'Santa_Cruz_de_Tenerife': int,
                   'Santander': int, 'Santiago_de_Compostela': int, 'Seville': int, 'Toledo': int, 'Valencia': int,
                   'Valladolid': int, 'Vitoria-Gasteiz': int, 'Zaragoza': int}

# Make a dict to save all minimum wind speed from json files
citties_min_wind = {'Barcelona': int, 'Logrono': int, 'Madrid': int, 'Merida': int, 'Murcia': int, 'Oviedo': int,
                    'Palma': int, 'Pamplona': int, 'Santa_Cruz_de_Tenerife': int,
                    'Santander': int, 'Santiago_de_Compostela': int, 'Seville': int, 'Toledo': int, 'Valencia': int,
                    'Valladolid': int, 'Vitoria-Gasteiz': int, 'Zaragoza': int}

# Helper list
temp_helper_list = []
wind_helper_list = []


# We make a function to get all temperatures and wind speeds from json files
def get_temps_winds(files):
    for file in files:
        # We get the current city name
        city = file.split('/')[-2]
        # We open the file
        with open(file, 'r') as f:
            # Load json data to a dict
            data = json.load(f)
            # If hourly exists in the dict
            if data and data.get('hourly'):
                # We itereate over the hourly dict
                for hour in data['hourly']:
                    # If temp exists in the dict
                    if hour.get('temp'):
                        # We add the temp to the helper list
                        temp_helper_list.append(hour['temp'])
                    if hour.get('wind_speed'):
                        wind_helper_list.append(hour['wind_speed'])
        # We add the helper list to the corresponding city
        cities_temp[city].extend(temp_helper_list)
        cities_wind[city].extend(wind_helper_list)
        # We clear the helper list
        temp_helper_list.clear()
        wind_helper_list.clear()


# We make a function to get all mean, min and max temperatures from json files
def get_mean_min_max_temps(cities_dict: dict):
    # We iterate over the cities dict
    for city in cities_dict:
        # We get the current city temperatures
        for temp in cities_dict[city]:
            # We get the mean temperatures for each city
            cities_mean[city] = round(statistics.mean(cities_temp[city]), 2)
            # We get the mean wind speeds for each city
            cities_mean_wind[city] = round(statistics.mean(cities_wind[city]), 2)
            # We get the min temperatures for each city
            cities_min_temp[city] = round(min(cities_temp[city]), 2)
            # We get the min wind speed for each city
            citties_min_wind[city] = round(min(cities_wind[city]), 2)
            # We get the max temperatures for each city
            cities_max_temp[city] = round(max(cities_temp[city]), 2)
            # We get the max wind speed for each city
            cities_max_wind[city] = round(max(cities_wind[city]), 2)

    # We get the overall mean temperatures for summary
    for city, temp in cities_mean.items():
        temp_helper_list.append(temp)
    summary_mean_temp = round(statistics.mean(temp_helper_list), 2)
    temp_helper_list.clear()

    # We get the overall mean wind speeds for summary
    for city, temp in cities_mean_wind.items():
        temp_helper_list.append(temp)
    summary_mean_wind = round(statistics.mean(temp_helper_list), 2)
    temp_helper_list.clear()

    return cities_mean, cities_mean_wind, cities_min_temp, citties_min_wind, cities_max_temp, cities_max_wind, summary_mean_temp, summary_mean_wind



get_temps_winds(files)
mean_temp, mean_wind, min_temp, min_wind, max_temp, max_wind, summary_temp, summary_wind = get_mean_min_max_temps(cities_temp)

# Setting summary attributes
summary.set('mean_temp', str(summary_temp))
summary.set('mean_wind_speed', str(summary_wind))
summary.set('coldest_place', str(min(min_temp, key=min_temp.get)))
summary.set('warmest_place', str(max(max_temp, key=mean_temp.get)))
summary.set('windiest_place', str(max(max_wind, key=mean_wind.get)))

# Setting cities attributes
for city, temp in mean_temp.items():
    current_city = etree.SubElement(cities, city)
    current_city.set('mean_temp', str(temp) )
    current_city.set('mean_wind_speed', str(mean_wind[city]))
    current_city.set('min_temp', str(min_temp[city]))
    current_city.set('min_wind_speed', str(min_wind[city]))
    current_city.set('max_temp', str(max_temp[city]))
    current_city.set('max_wind_speed', str(max_wind[city]))

etree.ElementTree(root).write("spain_weather.xml", pretty_print=True)