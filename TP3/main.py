#%%
from database import DB
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from geopandas import GeoSeries, GeoDataFrame
import matplotlib.colors as mplc
from math import log

# %%
## Add data from country and sites to dataframe

# Read Geopandas
world = GeoDataFrame.from_file('./docs/ne_10m_admin_0_countries.shp')

countryDataWorld = DB.SelectRows("""
SELECT c.code, c.population, c.gnp, site.count_sites
FROM country c
LEFT JOIN (
    SELECT countrycode, count(*) count_sites 
    FROM sitio2 
    GROUP BY countrycode 
) site
ON c.code = site.countrycode
""")

dfCountryDataWorld = pd.DataFrame(countryDataWorld, columns = ['countrycode', 'population', 'gnp', 'count_sites'])
world = world.merge(
                     right = dfCountryDataWorld,
                     left_on = 'ADM0_A3',
                     right_on = 'countrycode',
                     how = 'left'
                     )
world = world.drop('countrycode', axis=1)
world.head()

# %%
## SHOW MAPS
# world['population'].replace(to_replace=0,value = 1)
# world.head()
world = world.dropna('population')

world['population2'] =  np.log2(world['population'])

# # Mapa de población mundial
world.plot(column='population2', colormap='Reds', alpha=1, linewidth = 0.5, edgecolor='black', figsize = (14,8), categorical=False, legend=False, axes=None)

# # Mapa de producto bruto
# world.plot(column='gnp', colormap='Oranges', alpha=1, linewidth = 0.5, edgecolor='black', figsize = (14,8), categorical=False, legend=False, axes=None)

# # Mapa de sitios por pais
# world.plot(column='count_sites', colormap='Blues', alpha=1, linewidth = 0.5, edgecolor='black', figsize = (14,8), categorical=False, legend=False, axes=None)


plt.show()
# %%

