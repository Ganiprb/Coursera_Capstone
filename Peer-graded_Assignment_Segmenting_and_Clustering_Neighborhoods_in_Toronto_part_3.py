#!/usr/bin/env python
# coding: utf-8

# In[97]:


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
df_pc.columns = ['PostalCode', 'Borough', 'Neighborhood']
df_pc.head()


# In[98]:


url = requests.get('https://en.wikipedia.org/w/index.php?title=List_of_postal_codes_of_Canada:_M&oldid=945633050').text
soup = BeautifulSoup(url,'lxml')


# In[99]:


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
df_pc.columns = ['PostalCode', 'Borough', 'Neighborhood']


# In[100]:


df_pc['Borough'].replace('Not assigned', np.nan, inplace=True)
df_pc.dropna(subset=['Borough'], inplace=True)


# In[101]:


#join table with same value
df_pcn = df_pc.groupby(['PostalCode', 'Borough'])['Neighborhood'].apply(', '.join).reset_index()
df_pcn.columns = ['PostalCode', 'Borough', 'Neighborhood']
df_pcn['Neighborhood'].replace('Not assigned', "Queen's Park", inplace=True)


# In[102]:


#table with location
lat_lng_coords = pd.read_csv("https://cocl.us/Geospatial_data")
lat_lng_coords.rename(columns={'Postal Code':'PostalCode'}, inplace=True) 


# In[103]:


#merge modified table with location
df_with_location = pd.merge(df_pcn, lat_lng_coords, how='inner', left_on='PostalCode', right_on='PostalCode')


# In[104]:


#only borough with toronto
toronto_data = df_with_location[df_with_location['Borough'].str.contains("Toronto")].reset_index(drop=True)
toronto_data.head()


# In[105]:


# create map of Toronto using latitude and longitude values
latitude = toronto_data.loc[0, 'Latitude']
longitude = toronto_data.loc[0, 'Longitude']
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=11)

# add markers to map
for lat, lng, label in zip(toronto_data['Latitude'], toronto_data['Longitude'], toronto_data['Neighborhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# In[106]:


CLIENT_ID = 'XEDPVZFLOUWNOKEOOBZCP1FL4FZY5RVEOCXNW34RKFKQWUSW' # your Foursquare ID
CLIENT_SECRET = 'RDQZWMP1EYSR5OOWB334OONRIBPW0HA3PIIH42D5N4DBVWD5' # your Foursquare Secret
VERSION = '20180605' # Foursquare API version
toronto_data.loc[0, 'Neighborhood']


# In[107]:


neighborhood_latitude = toronto_data.loc[0, 'Latitude'] # neighborhood latitude value
neighborhood_longitude = toronto_data.loc[0, 'Longitude'] # neighborhood longitude value

neighborhood_name = toronto_data.loc[0, 'Neighborhood'] # neighborhood name

print('Latitude and longitude values of {} are {}, {}.'.format(neighborhood_name, 
                                                               neighborhood_latitude, 
                                                               neighborhood_longitude))


# In[108]:


LIMIT = 100 # limit of number of venues returned by Foursquare API

radius = 500 # define radius

# create URL
url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    neighborhood_latitude, 
    neighborhood_longitude, 
    radius, 
    LIMIT)
url # display URL


# In[109]:


results = requests.get(url).json()


# In[110]:


# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']


# In[111]:


venues = results['response']['groups'][0]['items']
    
nearby_venues = json_normalize(venues) # flatten JSON

# filter columns
filtered_columns = ['venue.name', 'venue.categories', 'venue.location.lat', 'venue.location.lng']
nearby_venues =nearby_venues.loc[:, filtered_columns]

# filter the category for each row
nearby_venues['venue.categories'] = nearby_venues.apply(get_category_type, axis=1)

# clean columns
nearby_venues.columns = [col.split(".")[-1] for col in nearby_venues.columns]

nearby_venues.head()


# In[112]:


# Neighborhood in Toronto 
def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)

toronto_venues = getNearbyVenues(names=toronto_data['Neighborhood'],
                                latitudes=toronto_data['Latitude'],
                                longitudes=toronto_data['Longitude']
                                )


# In[113]:


print(toronto_venues.shape)
print ("Neighborhood in Toronto")
toronto_venues.head()


# In[ ]:




