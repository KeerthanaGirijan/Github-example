#!/usr/bin/env python
# coding: utf-8

#  Project Description
#  
# One of an intriguing topic used in Data science is to compare neighborhoods of two cities or districts are similar or disimilar. People who are planning to do a bussiness, restaurants or want to construct a house would be benefitted from the comparison of these. The main purpose of the project is to ana;yse geographical locations and to help people understand the geographical advantages when starting or planning to do any sorts of investments.
# 

# Data used in this project
# 
# To make good use of the foursquare location data, the labs done for Toronto segmented and clustered neighborhoods gave me good examples for new ideas.
# I would need to leverage the foursquare location data to solve or execute. Data science problems always target an audience and are meant to help a group of stakeholders solve a problem, so make sure that I explicitly describe the audience and why they would care about my problem.
# From the results on New York, the lab especially tells 10 most common venues in each district. The data set is about Toronto Venues. After transforming the data to Json files, it is easy to use Pandas to transform them into DataFrame. Then select the required data columns to appear and get the information we want. Geopy library is used to get the latitude and longitude values. With the locations the maps can be created and we will have a direct understanding of the neighborhoods and the purposed areas. The Folium library is also used to show maps on different requirements
# 

# In[16]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system("conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab")
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

get_ipython().system("conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab")
import folium 
# map rendering library

print('Libraries imported.')


# In[2]:


address = 'Toronto, Canada'

geolocator = Nominatim(user_agent='capstone_project')
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# In[3]:


from bs4 import BeautifulSoup 
import requests 
import bs4

html = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
fsa=requests.get(html)
fsa.raise_for_status()
fsa.encoding=fsa.apparent_encoding
fsa.text

x=fsa.text
soup = BeautifulSoup(x)
content = soup.findAll('td')
tables=[]
for data in content:
    tables.append(data.text.strip())
    new_tables=[tables[i:i+3] for i in range(0,len(tables),3)]
new_tables


# In[4]:


import pandas as pd
column_names = ['Postcode','Borough', 'Neighborhood'] 
neighborhoods =pd.DataFrame(columns=column_names)


# In[5]:


neighborhoods


# In[18]:


for x in range(0,289):   
    neighborhoods = neighborhoods.append(
            {'Postcode': new_tables[x][0],
             'Borough': new_tables[x][1],
             'Neighborhood': new_tables[x][2]
            },ignore_index=True)


# In[19]:



neighborhoods


# In[20]:


df1=neighborhoods.copy()
df1=df1[~df1['Borough'].isin(['Not assigned'])]
df1['Neighborhood']= df1['Neighborhood'].replace('Not assigned', df1['Borough'])
df1


# In[21]:


d2=df1.groupby(['Postcode','Borough'], as_index=False)
df1=d2.agg(lambda x: ', '.join(x))
df1.head(20)


# In[22]:


df_cor = pd.read_csv('http://cocl.us/Geospatial_data')
df_cor.head(5)


# In[23]:


df_with_cor = pd.merge(df1, df_cor, left_on='Postcode', right_on='Postal Code', suffixes=('', '')).drop('Postal Code', 1)
df_with_cor.head(10)


# In[29]:



map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

for lat, lng, borough, neighborhood in zip(df_with_cor['Latitude'], df_with_cor['Longitude'], df_with_cor['Borough'], df_with_cor['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill_color='#3186cc',
        fill_opacity=0.7,
    ).add_to(map_toronto)
    
map_toronto


# In[30]:



def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius)
            
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
                  'Postcode Latitude', 
                  'Postcode Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# In[31]:


boroughs = set(df_with_cor['Borough'])
toronto_boroughs = {borough for borough in boroughs if 'Toronto' in borough}
toronto_data = df_with_cor[df_with_cor['Borough'].isin(toronto_boroughs)].reset_index(drop=True)
toronto_data.head(5)


# In[38]:


CLIENT_ID = 'PXXFRZXNDT3HAAGE2PTLXXZTSNVD0PKRE41KMGDP3JOSRDN5' # your Foursquare ID
CLIENT_SECRET = 'UO2TGIOWALSIT1QK4XLNIZYT2NJFNN4KC5HDGSJVRRCFYAY1' # your Foursquare Secret
VERSION = '20190101' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# Methodology
# This was only an exploratory analysis.First of all, the Foursquare API was utilized because basic geographical location information and particular venues can be explored through Foursquare API. With a specific credentials client ID and secret, the required foursquare data can be accessed.
# 
# Second, Folium is a great visualization library, the map can directly show us the overall shape of the place we want to know. The detailed information on different venues such as restaurants can be seen in a direct way. The investors can have a better understanding of the city of Toronto to choose his properties. People feel free to zoom into the above map, and click on each circle mark to reveal the name of the neighborhood and its respective borough

# Results 
# In Toronto, venues types are various and investors can choose their preferable neighborhoods to open the restaurants and the companies. In my opinion, their should be more crowds to make the neighborhood more developed. Data shown in my notebook told us comprehensive kinds of venues in different areas of Toronto

# Discussion
# From data of top 10 common venues in Toronto, the best place for investors to open a restaurant or start a company should not be one, but also several choices. The data only showed us the current numbers of each kind of venues but no other factors such as cost of the place or environment.

# Coclusion
# The investors should consider the competitive restaurants in the district. Try not to compete with those nearby with more similar kinds of restaurants as yours, that may do bad for the kind of investment. But for start a company, it is good to choose the place with more kinds of restaurants so that you will attract more employees to be hired.
