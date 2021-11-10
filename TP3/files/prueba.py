#!/usr/bin/python
# -*- coding: utf-8 -*-

#%%
import numpy as np
import matplotlib.pyplot as plt
from geopandas import GeoSeries, GeoDataFrame
from database import DB

#%%
def test():
    codes = DB.SelectRows("SELECT code2, code FROM country")
    dicCodes = dict(codes)
    print(dicCodes)
test()


#%%
#QUERY
world = GeoDataFrame.from_file('./docs/ne_10m_admin_0_countries.shp')
world['prueba'] = range(len(world))
world2 = world.loc[world['ADMIN'] == 'Argentina']
world2
# print(world.columns)

#%%
world.plot(column='prueba', colormap='Greens', alpha=0.5, categorical=False, legend=False, axes=None)
world.plot(column='prueba', colormap='binary', alpha=0.5, categorical=False, legend=False, axes=None)
world.plot()
world.plot(column=None, colormap='Greens', alpha=0.5, categorical=False, legend=False, axes=None)

print(world['CONTINENT'].unique())

south = world[world['CONTINENT'] == 'South America']
south.plot(column='prueba', colormap='binary', alpha=0.5, categorical=False, legend=False, axes=None)

world.plot(column='prueba', cmap='Greens', alpha=0.5, categorical=False, legend=False, ax=None)

plt.show()


# %%
