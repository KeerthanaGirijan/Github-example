#!/usr/bin/env python
# coding: utf-8

# In[1]:


#install Beautiful Soup and requests for Web Scaping
get_ipython().system('pip install BeautifulSoup4')
get_ipython().system('pip install requests')


# In[3]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#get html from wiki page and create soup object
source = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
soup = BeautifulSoup(source.text, 'lxml')

#using soup object, iterate the .wikitable to get the data from the HTML page and store it into a list
data = []
columns = []
table = soup.find(class_='wikitable')
for index, tr in enumerate(table.find_all('tr')):
    section = []
    for td in tr.find_all(['th','td']):
        section.append(td.text.rstrip())
    
    #First row of data is the header
    if (index == 0):
        columns = section
    else:
        data.append(section)

#convert list into Pandas DataFrame
canada_df = pd.DataFrame(data = data,columns = columns)
canada_df.head()


# In[10]:


#Remove Boroughs that are 'Not assigned'
canada_df = canada_df[canada_df['Borough'] != 'Not assigned']
canada_df.head()


# In[19]:




canada_df.shape


# In[ ]:




