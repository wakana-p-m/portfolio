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
df = pd.read_csv('Post Performance_January 1, 2020 - December 31, 2020.csv', parse_dates=True, usecols=cols_to_use)


# In[290]:


df.tail()


# In[294]:


df["Tags"] = df["Tags"].replace({'[Ss]tudent [aA]rtwork':'Student Work','alumni success':'success','Student success':'success','faculty success':'faculty'}, regex=True)
df['Tags'] = df['Tags'].str.lower()  #format the tags data by making them lowercase


# In[295]:


df_to_modify = df.copy()
df_to_modify.head(10)


# In[296]:


df['Tags'] = df['Tags'].str.split(pat=', ')  #split each of strings into a list


# In[297]:


df.head()
df.info()


# In[298]:


#create a tag list
tags = df[df['Tags'].notna()]
tags = set(df['Tags'].explode().values) #Create a set to remove duplicate first
tags = list(tags) #convert the set to list
tags = [tag for tag in tags if str(tag)!= 'nan']
len(tags)


# In[299]:


tags


# In[301]:


#remove the core values from the list
primary_content = ['curriculum', 'success','awards & honors', 'partnership', 'academy cares','faculty','events', 'engagement','sf', 'student work']
new_core_values = ["ideal","limitless", "inviting","outstanding","fast", "quality"]
primary_content_dict = {'curriculum':'Core value 1', 'success':'Value 4','awards & honors':'Value 5', 'partnership':'Core value 2', 'academy cares':'Value 6','faculty':'Core value 3','events':'Corgi', 'engagement':'Husky','sf':'value 7', 'student work':'German Shepherd'}

for i in tags:
    if i in primary_content:
        tags.remove(i)



#for i in primary_content:
   # if i in tags:
        #tags.remove(i)
len(tags)


# In[302]:


tags


# In[303]:


#replace regular tags with pokemon name
pokemon = pd.read_csv("pokemon.csv")


# In[304]:


pokemon_list = list(pokemon.iloc[:84,1])
len(pokemon_list)


# In[305]:


#create a dict of tags correcspond to pokemon
tag_dict = {}
for key in tags:
    for item in pokemon_list:
        tag_dict[key] = item
        pokemon_list.remove(item)
        break


# In[306]:


tag_dict


# In[307]:


# Modify the original file

df_to_modify["Tags"] = df_to_modify["Tags"].replace(to_replace = primary_content_dict, regex=True)
df_to_modify["Tags"] = df_to_modify["Tags"].replace(to_replace = tag_dict, regex=True)


# In[309]:


df_to_modify["Tags"].tail(20)


# In[310]:


data_removed = df_to_modify[df_to_modify['Tags'].notna()]


# In[311]:


data_removed.to_csv("modifiled_post_data.csv")


# In[ ]:




