#!/usr/bin/env python
# coding: utf-8

# In[116]:


import pandas as pd
import numpy as np


# In[117]:


file_address="https://archive-api.open-meteo.com/v1/archive?latitude=45.508256&longitude=10.13164&start_date=2010-01-01&end_date=2019-12-31&hourly=temperature_2m,relativehumidity_2m,precipitation,cloudcover,windspeed_10m&timezone=Europe%2FBerlin"


# In[118]:


file = pd.read_json(file_address, orient="records")
print(file)


# In[119]:


file2 = pd.read_csv("OpenMeteoTorbole.csv", skiprows=2)


# In[120]:


df = file2.drop(columns =['windspeed_10m (km/h)'])


# In[121]:


df.head()


# In[122]:


print(df.shape)


# In[123]:


df.rename(columns=dict(zip(list(df.columns), list(['time', 'temperature', 'relativehumidity', 'precipitation', 'cloudcover']))), inplace=True)
df


# In[124]:


df['temperature'] = pd.cut(df['temperature'], bins=[-np.inf, 10, 25, np.inf], labels=['Cold', 'Mild', 'Hot'])
df['relativehumidity'] = pd.cut(df['relativehumidity'], bins=[0, 50, 100], labels=['Low', 'High'])
df['precipitation'] = pd.cut(df['precipitation'], bins=[0, 1, np.inf], labels=['None', 'Yes'])
df['cloudcover'] = pd.cut(df['cloudcover'], bins=[0, 30, 100], labels=['Clear', 'Cloudy'])
df


# In[125]:


df = df.dropna()
df = df.reset_index(drop=True)
df


# In[126]:


print(df.shape[0])


# In[127]:


cold_yes = 0
cold_no = 0
mild_yes = 0
mild_no = 0
hot_yes = 0
hot_no = 0

for i in range (df.shape[0]):
    if df['temperature'][i] == "Cold" and df['precipitation'][i] == "Yes":
        cold_yes+=1
    if df['temperature'][i] == "Cold" and df['precipitation'][i] == "None":
        cold_no+=1
    if df['temperature'][i] == "Mild" and df['precipitation'][i] == "Yes":
        mild_yes+=1
    if df['temperature'][i] == "Mild" and df['precipitation'][i] == "None":
        mild_no+=1 
    if df['temperature'][i] == "Hot" and df['precipitation'][i] == "Yes":
        hot_yes+=1
    if df['temperature'][i] == "Hot" and df['precipitation'][i] == "None":
        hot_no+=1 
print("cold_yes : " + str(cold_yes/df.shape[0]))
print("cold_no : " + str(cold_no/df.shape[0]))
print("mild_yes : " + str(mild_yes/df.shape[0]))
print("mild_no : " + str(mild_no/df.shape[0]))
print("hot_yes : " + str(hot_yes/df.shape[0]))
print("hot_no : " + str(hot_no/df.shape[0]))


# In[128]:


high_yes = 0
high_no = 0
low_yes = 0
low_no = 0

for i in range (df.shape[0]):
    if df['relativehumidity'][i] == "High" and df['precipitation'][i] == "Yes":
        high_yes+=1
    if df['relativehumidity'][i] == "High" and df['precipitation'][i] == "None":
        high_no+=1
    if df['relativehumidity'][i] == "Low" and df['precipitation'][i] == "Yes":
        low_yes+=1
    if df['relativehumidity'][i] == "Low" and df['precipitation'][i] == "None":
        low_no+=1 
print("high_yes : " + str(high_yes/df.shape[0]))
print("high_no : " + str(high_no/df.shape[0]))
print("low_yes : " + str(low_yes/df.shape[0]))
print("low_no : " + str(low_no/df.shape[0]))


# In[129]:


clear_yes = 0
clear_no = 0
cloudy_yes = 0
cloudy_no = 0

for i in range (df.shape[0]):
    if df['cloudcover'][i] == "Clear" and df['precipitation'][i] == "Yes":
        clear_yes+=1
    if df['cloudcover'][i] == "Clear" and df['precipitation'][i] == "None":
        clear_no+=1
    if df['cloudcover'][i] == "Cloudy" and df['precipitation'][i] == "Yes":
        cloudy_yes+=1
    if df['cloudcover'][i] == "Cloudy" and df['precipitation'][i] == "None":
        cloudy_no+=1 
print("clear_yes : " + str(clear_yes/df.shape[0]))
print("clear_no : " + str(clear_no/df.shape[0]))
print("cloudy_yes : " + str(cloudy_yes/df.shape[0]))
print("cloudy_no : " + str(cloudy_no/df.shape[0]))


# In[ ]:





# In[130]:


# Then I test some way to put a filter on data, but it's quitte hard


# In[131]:


type(df['time'][0])


# In[132]:


filter = file["time"] == "2020-01-01T03:00"
print(file[filter])


# In[ ]:





# In[ ]:





# In[ ]:




