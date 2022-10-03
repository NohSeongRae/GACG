#momepy approach
# import momepy
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import networkx as nx
# #test
# streets = gpd.read_file("0001.geojson")
# f, ax = plt.subplots(figsize=(10, 10))
# streets.plot(ax=ax)
# ax.set_axis_off()
# plt.show()
#
# #graph
# graph = momepy.gdf_to_nx(streets, approach='primal')
# f, ax = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
# streets.plot(color='#e32e00', ax=ax[0])
# for i, facet in enumerate(ax):
#     facet.set_title(("Streets", "Primal graph", "Overlay")[i])
#     facet.axis("off")
# nx.draw(graph, {n:[n[0], n[1]] for n in list(graph.nodes)}, ax=ax[1], node_size=15)
# streets.plot(color='#e32e00', ax=ax[2], zorder=-1)
# nx.draw(graph, {n:[n[0], n[1]] for n in list(graph.nodes)}, ax=ax[2], node_size=15)
#
# #dual graph
# dual = momepy.gdf_to_nx(streets, approach='dual')
# f, ax = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
# streets.plot(color='#e32e00', ax=ax[0])
# for i, facet in enumerate(ax):
#     facet.set_title(("Streets", "Dual graph", "Overlay")[i])
#     facet.axis("off")
# nx.draw(dual, {n:[n[0], n[1]] for n in list(dual.nodes)}, ax=ax[1], node_size=15)
# streets.plot(color='#e32e00', ax=ax[2], zorder=-1)
# nx.draw(dual, {n:[n[0], n[1]] for n in list(dual.nodes)}, ax=ax[2], node_size=15)


#pysal approach
import geopandas as gpd
import momepy
import networkx
df2=gpd.read_file("0001.geojson")
df2.geometry=df2.geometry.boundaries
df2_graph=momepy.gdf_to_nx(df2)
print(df2)