#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json

firenze_file_path = "firenze_whole_GeoJSON.geojson"

# GeoJSON 파일 읽기
with open(firenze_file_path, "r", encoding='UTF8') as infile:
    geojson_data = json.load(infile)
    
commercial_color = [255, 255, 204]
building_color = [255, 240, 230]
green_color = [102, 153, 102]
water_color = [102, 204, 204]
education_color = [255, 204, 153]
medical_color = [255, 153, 153]
etc_color = [204, 204 ,204]

commercial_data = {"type": "FeatureCollection"}
building_data = {"type": "FeatureCollection"}
green_data = {"type": "FeatureCollection"}
water_data = {"type": "FeatureCollection"}
education_data = {"type": "FeatureCollection"}
medical_data = {"type": "FeatureCollection"}
road_data = {"type": "FeatureCollection"}
etc_data = {"type": "FeatureCollection"}

commercial_list = []
building_list = []
green_list = []
water_list = []
education_list = []
medical_list = []
road_list = []
etc_list = []

color = [commercial_color, building_color, green_color, water_color, education_color, medical_color, etc_color]

dict_list = [commercial_data, building_data, green_data, water_data, education_data, medical_data, etc_data]
type_list = [commercial_list, building_list, green_list, water_list, education_list, medical_list, etc_list]

green_landuse = ['park', 'grassland', 'grass','forest', 'cemetery', 'farmland', 'farmyard', 'greenhouse_horticulture', 'landfill']
commercial = ['marketplace', 'restaurant', 'fast_food', 'cafe', 'bar', 'pub']
water_area = ['water', 'wetland']
education = ['kindergarten', 'school', 'college', 'university', 'language_school', 'educational_instituion']
medical = ['doctors', 'dentist', 'clinic', 'toilets', 'hospital', 'pharmacy', 'harbalist', 'nutrition_supplements']
etc = ['police', 'fire_station', 'atm', 'bank', 'bureau_de_change', 'microfinance', 
       'mobile_money_agent', 'money_transfer', 'court_house', 'townhall', 'embassy', 'post_office',
      'stadium', 'swimming pool', 'pitch', 'sport_centre']


for i in range (len(geojson_data['features'])):
    if geojson_data["features"][i]["properties"].get("sport") is not None:
        etc_list.append(geojson_data["features"][i])
    if geojson_data["features"][i]["properties"].get("leisure") is not None:
        leisure = geojson_data["features"][i]["properties"]['leisure']
        if leisure in etc:
            etc_list.append(geojson_data["features"][i])  
    
    if geojson_data["features"][i]["properties"].get("healthcare") is not None:
        medical_list.append(geojson_data["features"][i])
        
    if geojson_data["features"][i]["properties"].get("aeroway") is not None:
        road_list.append(geojson_data["features"][i])
    if geojson_data["features"][i]["properties"].get("highway") is not None:
        road_list.append(geojson_data["features"][i])
    if geojson_data["features"][i]["properties"].get("railway") is not None:
        road_list.append(geojson_data["features"][i])
        
    if geojson_data["features"][i]["properties"].get("amenity") is not None:
            amenity = geojson_data["features"][i]["properties"]['amenity']
            if amenity in commercial:
                commercial_list.append(geojson_data["features"][i])  
            if amenity in green_landuse:
                green_list.append(geojson_data["features"][i])
            if amenity in education:
                education_list.append(geojson_data["features"][i])
            if amenity in medical:
                medical_list.append(geojson_data["features"][i])
            if amenity in etc:
                etc_list.append(geojson_data["features"][i])
    if geojson_data["features"][i]["properties"].get("shop") is not None:
            commercial_list.append(geojson_data["features"][i])  
    if geojson_data["features"][i]["properties"].get("tourism") is not None:
            commercial_list.append(geojson_data["features"][i])  
            
    if geojson_data["features"][i]["properties"].get("building") is not None:
            building_list.append(geojson_data["features"][i])
            
    if geojson_data["features"][i]["properties"].get("landuse") is not None:
        if geojson_data["features"][i]["properties"]["landuse"] in green_landuse:
            green_list.append(geojson_data["features"][i])
    if 'natural' in geojson_data["features"][i]["properties"]:
        if geojson_data["features"][i]["properties"]['natural'] == green_landuse:
            green_list.append(geojson_data["features"][i])
        if geojson_data["features"][i]["properties"]['natural'] in water_area:
            water_list.append(geojson_data["features"][i])
    if 'leisure' in geojson_data["features"][i]["properties"]:
        if geojson_data["features"][i]["properties"]['leisure'] in green_landuse:
            green_list.append(geojson_data["features"][i])
        
road_data["features"] = road_list
        
# print(green_list)
for i in range (len(dict_list)):
    dict_list[i]["features"] = type_list[i]
    for feature in dict_list[i]["features"]:
        feature["properties"] = {}
    for j in range (len(dict_list[i]["features"])):
        dict_list[i]["features"][j]["properties"]["color"] = color[i]
    filtered_features = [
        feature for feature in dict_list[i]["features"]
        if feature["geometry"]["type"] != 'Point'
    ]
    dict_list[i]["features"] = filtered_features

