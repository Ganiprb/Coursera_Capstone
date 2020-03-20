#!/usr/bin/env python
# coding: utf-8

# In[29]:


# library to handle data in a vectorized manner
import numpy as np 

# library for data analsysis
import pandas as pd 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# library to handle JSON files
import json 


# convert an address into latitude and longitude values
from geopy.geocoders import Nominatim 

# library to handle requests
import requests 

# tranform JSON file into a pandas dataframe
from pandas.io.json import json_normalize 

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

# for webscraping import Beautiful Soup 
from bs4 import BeautifulSoup

import xml

# install anaconda package
get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')
get_ipython().system('conda install -c conda-forge geopy --yes ')

# map rendering library
import folium 

# get data from wikipedia url
url = requests.get('https://en.wikipedia.org/w/index.php?title=List_of_postal_codes_of_Canada:_M&oldid=945633050').text
soup = BeautifulSoup(url,'lxml')

table_post = soup.find('table')
fields = table_post.find_all('td')

postcode = []
borough = []
neighbourhood = []

#adding index
for i in range(0, len(fields), 3):
    postcode.append(fields[i].text.strip())
    borough.append(fields[i+1].text.strip())
    neighbourhood.append(fields[i+2].text.strip())

#change column names
df_pc = pd.DataFrame(data=[postcode, borough, neighbourhood]).transpose()
df_pc.columns = ['PostalCode', 'Borough', 'Neighbourhood']
df_pc.head()


# In[30]:


url = requests.get('https://en.wikipedia.org/w/index.php?title=List_of_postal_codes_of_Canada:_M&oldid=945633050').text
soup = BeautifulSoup(url,'lxml')


# In[31]:


table_post = soup.find('table')
fields = table_post.find_all('td')

postcode = []
borough = []
neighbourhood = []

for i in range(0, len(fields), 3):
    postcode.append(fields[i].text.strip())
    borough.append(fields[i+1].text.strip())
    neighbourhood.append(fields[i+2].text.strip())
        
df_pc = pd.DataFrame(data=[postcode, borough, neighbourhood]).transpose()
df_pc.columns = ['Postalcode', 'Borough', 'Neighbourhood']


# In[32]:


df_pc['Borough'].replace('Not assigned', np.nan, inplace=True)
df_pc.dropna(subset=['Borough'], inplace=True)


# In[33]:


df_pcn = df_pc.groupby(['Postalcode', 'Borough'])['Neighbourhood'].apply(', '.join).reset_index()
df_pcn.columns = ['Postalcode', 'Borough', 'Neighbourhood']


# In[34]:


df_pcn['Neighbourhood'].replace('Not assigned', "Queen's Park", inplace=True)


# In[35]:


df_geo = pd.read_csv('http://cocl.us/Geospatial_data')
df_geo.columns = ['Postalcode', 'Latitude', 'Longitude']


# In[36]:


df_pos = pd.merge(df_pcn, df_geo, on=['Postalcode'], how='inner')

df_tor = df_pos[['Borough', 'Neighbourhood', 'Postalcode', 'Latitude', 'Longitude']].copy()

df_tor.head()


# In[37]:


address = 'Toronto, Canada'

geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of the City of Toronto are {}, {}.'.format(latitude, longitude))


# In[ ]:




