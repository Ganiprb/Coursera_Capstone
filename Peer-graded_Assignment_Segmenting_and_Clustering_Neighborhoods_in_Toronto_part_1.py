#!/usr/bin/env python
# coding: utf-8

# In[9]:


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


# In[10]:


#Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned
df_pc['Borough'].replace('Not assigned', np.nan, inplace=True)
df_pc.dropna(subset=['Borough'], inplace=True)


# In[11]:


#join two row with the same postalcode value
df_2 = df_pc.groupby(['PostalCode','Borough'])['Neighbourhood'].apply(', '.join).reset_index()
df_2


# In[12]:


num_rows, num_cols = df_2.shape
print (num_rows, num_cols)


# In[ ]:





# In[ ]:





# In[ ]:




