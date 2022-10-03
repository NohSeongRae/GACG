# import pandas as pd
# import geojson
# from pandas.io.json import json_normalize
# df = json_normalize(geojson["features"])
#
# coords = 'properties.geometry.coordinates'
#
# df2 = (df[coords].apply(lambda r: [(i[0],i[1]) for i in r[0]])
#            .apply(pd.Series).stack()
#            .reset_index(level=1).rename(columns={0:coords,"level_1":"point"})
#            .join(df.drop(coords,1), how='left')).reset_index(level=0)
#
# df2[['lat','long']] = df2[coords].apply(pd.Series)
#
# df2

import geopandas as gpd
df=gpd.read_file("0001.geojson")
print(df)
print(type(df))
df2=gpd.GeoDataFrame(df)
print(type(df2))
print(df2)