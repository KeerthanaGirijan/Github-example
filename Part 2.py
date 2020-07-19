#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as uReq
import requests
import lxml
import pandas as pd
from pandas import DataFrame
import numpy as np


# In[2]:


my_url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

r=requests.get(my_url)


# In[3]:


page=bsoup(r.text,"html.parser")
page


# In[5]:


rtable=page.table
rtable


# In[6]:


results=rtable.find_all('tr')
nrows=len(results)
nrows


# In[7]:


results[0:5]


# In[8]:


header=results[0].text.split()
header


# In[9]:



results[85].text


# In[10]:



results[85].text.split('\n')


# In[11]:


Postcode=results[85].text.split('\n')[1]
Postcode


# In[12]:


Borough=results[85].text.split('\n')[2]
Borough


# In[13]:


Neighborhood=results[85].text.split('\n')[3]
Neighborhood


# In[14]:


# iteration loop to harvest all records

records =[]
n=1
while n < nrows :
    Postcode=results[n].text.split('\n')[1]
    Borough=results[n].text.split('\n')[2]
    Neighborhood=results[n].text.split('\n')[3]
    records.append((Postcode, Borough,Neighborhood))
    n=n+1

df=pd.DataFrame(records, columns=['PostalCode', 'Borough', 'Neighbourhood'])
df.head(5)


# In[15]:



df.shape


# In[16]:


# How many rows have Borough equal to 'Not assigned'?
df[df['Borough']=='Not assigned'].count()


# In[17]:


df1=df[~df.Borough.str.contains("Not assigned")]
df1=df1.reset_index(drop=True)


# In[18]:


df1.loc[df1['Neighbourhood'] == 'Not assigned', 'Neighbourhood'] = df1['Borough']


# In[19]:


postalcodes = df1['PostalCode'].nunique()
boroughs = df1['Borough'].nunique()
neighbourhoods= df1['Neighbourhood'].nunique()
print('Unique Postalcodes : ' + str(postalcodes))
print('Unique Boroughs  : '+ str(boroughs))
print('Unique Neighbourhoods  :' + str(neighbourhoods))


# In[20]:


df1.head()


# In[21]:


df2=df1
df2.head()


# In[22]:


nrows2=len(df2)-1
nrows2


# In[23]:



while n < nrows2 :
    post1=df2.iloc[n,0]
    #post1
    m=n+1
    post2=df2.iloc[m,0]
    #post2
    neigh1=df2.iloc[n,2]
    neigh2=df2.iloc[m,2]
    if post1==post2:
        df2.Neighbourhood[n,2] = neigh1=neigh1+','+neigh2
        #df2 = df2[df2.Neighbourhood != 'neigh2']
        df2=df2.drop(df2.index[m])
        nrows2=nrows2-1
        df2 = df2.reset_index(drop=True)
    else:
        n=n+1


#df2 = df2.reset_index(drop=True)
# print(post1, post2, 'Nigh1 is...'+ neigh1,',,,,,,,','Nigh2 is...' + neigh2, n,m)
df2.index


# In[24]:



df2.head()


# In[25]:



df2.head()


# In[26]:



df2.head(15)


# In[27]:



df2.shape


# In[ ]:




