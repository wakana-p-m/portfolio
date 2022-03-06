#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 999) #This option force Jupyternotebook to show all columns. 


# In[2]:


cols_to_use =['Date', 'Post ID', 'Network','Post Type', 'Impressions',
       'Organic Impressions', 'Engagement Rate (per Impression)',
       'Engagements', 'Reactions', 'Comments',
       'Shares','Tags']
df = pd.read_csv('Projects\Social Media Content Analysis\Post Performance_January 1, 2020 - December 31, 2020.csv', parse_dates=True, usecols=cols_to_use)


# In[36]:


df.head()


# In[37]:


df["Tags"] = df["Tags"].replace({'Student Artwork':'Student Work','alumni success':'success','Student success':'success','faculty success':'faculty'}, regex=True)
df['Tags'] = df['Tags'].str.lower()  #format the tags data by making them lowercase
df['Tags'] = df['Tags'].str.split(pat=', ')  #split each of strings into a list


# In[38]:


df.head()


# In[41]:


#create a tag list
tags = df[df['Tags'].notna()]
tags = set(df['Tags'].explode().values) #Create a set to remove duplicate first
tags = list(tags) #convert the set to list
tags = [tag for tag in tags if str(tag)!= 'nan']


# In[44]:


len(tags)


# In[45]:


new_core_values = ["ideal","limitless", "inviting","outstanding","fast", "quality"]
pokemon = pd.read_csv("pokemon.csv")


# In[ ]:




