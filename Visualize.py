#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import pydeck as pdk

# GeoJSON 파일 읽기
def read_geojson_file(file_path):
    with open(file_path, "r", encoding='UTF8') as f:
        geojson_data = json.load(f)
    return geojson_data

file_path = "clipping_boundary.geojson"

# GeoJSON 데이터를 Python 객체로 로드
firenze_geojson_data = read_geojson_file(file_path)

layer_list = []

layer_list.append(pdk.Layer(
"GeoJsonLayer",
data=firenze_geojson_data,
stroked=True,
filled=True,
extruded=False, 
line_width_min_pixels=0.5,
get_line_color=[255, 255, 255],
get_fill_color=[255, 250, 250],
get_fill_opacity=100,
pickable=True,
))



layer_list.append(pdk.Layer(
"GeoJsonLayer",
data=road_data,
stroked=True,
filled=True,
extruded=False, 
line_width_min_pixels=2.5,
get_line_color=[255, 255, 255],
get_fill_color=[255, 255, 255],
get_fill_opacity=100,
pickable=True,
))

for i in range(len(dict_list)):
    layer_list.append(pdk.Layer(
    "GeoJsonLayer",
    data=dict_list[i],
    stroked=False,
    filled=True,
    extruded=False, 
    line_width_min_pixels=0,
    # get_line_color=[0, 0, 0],
    get_fill_color="properties.color",
    get_fill_opacity=100,
    pickable=True,
))

# GeoJSON 레이어 생성
MAPBOX_API_KEY = "pk.eyJ1IjoibWlzb25nIiwiYSI6ImNsZnM5aGs5cTAzemwzamwyM2QxbWRnaXcifQ.OAA_DdoHeDYHfhzkWo4EFw"
CUSTOM_STYLE_URL = "mapbox://styles/misong/clftcfl32000g01nmt7s0d05v"

# 맵 초기 위치 설정
view_state = pdk.ViewState(latitude=43.7559827, longitude=11.2983995, zoom=12)

# 맵 생성 및 렌더링
deck = pdk.Deck(
    layers=layer_list, 
    initial_view_state=view_state,
    map_style=CUSTOM_STYLE_URL,
    api_keys={'mapbox': MAPBOX_API_KEY})

deck.to_html("geojson_layer.html")

