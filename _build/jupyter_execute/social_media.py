#!/usr/bin/env python
# coding: utf-8

# # Social Media Content Analysis
# 
# I analyzed the performance of social media posts by content categories and social media platforms (Facebook, Instagram, Twitter, and LinkedIn) to identify the most optimal platform to communicate a company's value propositions. 
# 
# The analysis relived that not only the posts about the company's core values were underperforming compared to other content categories but also the value of posts the core values was much smaller. This result led me to focus on reinforcing the brand messaging as one of the strategic plans. 

# ## Background
# My social media team's goal was to communicate the company's value propositions in engaging ways while maximizing the exposure (=impressions) of individual posts. In order to acquire high impressions (due to most of the social media's algorithms), constantly posting highly engaging content is essential. However, the company's core values are not necessarily "fun" topics to discuss, and it's tempting to just post engagement-driven posts such as memes and pretty images.
# 
# The social media team used to post the exact same content across 4 major social media channels (Facebook, LinkedIn, Instagram, and Twitter). However, as each platform has a different audience, it is required to create content that caters to each platform.
# 
# 
# ## Objective
# Identify the most optimal platform(s) for each core value. 
# 
# 
# ## Measure of Success
# 
# - Engagement rate (# of post engagement / # of impression) *– Engagement is user' behaivors such as "Like", "Comments", and "Share". Higher the engagement rate, the higher the quality of content is.
# - The number of posts
# - The number of impression *– This indicate how much a single social media post is shown on user's timeline. This is usually used as an indirect measure of brand awareness*
# 
# ## Data Source
# The raw data of social media posts published between the past 12 months (January 1, 2020, December 21, 2020) were exported from a social media management platform, Sprout Social as `.csv`.
# 
# Each post has a few tags representing the content categories and subcategories. Content categories are consist of company's core values, values, and social media-specific content categories (such as memes, or user generated content). Subcategories are used to label campaigns, experimental posts, and types of products.
# 
# For confidentiality, any information that can identify the company was scraped out for this case study. Content categories and subcategories are modified as below:
# 
# - Company's core values: core value 1, core value 2, core value 3
# - Company's values: value, 4, value 5, value 6
# - Social media specific categories: corgi, husky
# - Subcategories: Pokemon names
# 
# 
# ## Results
# - All three core values (core value 1, core value 2, core value 3) were not performing well across the platforms. Also, the number of posts about these core values is fewer than the other categories. 
# - The number of posts is heavily skewed to the "value 4" category on social media, and the category is performing well. 
# - The "value 5" content generates the highest engagement on LinkedIn while the category does not perform as much on other platforms. 
# - The "value 6" content performs well on all channels except Facebook. 
#  - The engagement of the "value 4" category on Facebook is higher than other content categories. However, the impression is not necessarily higher, which implies there might not be a strong correlation between post engagements and impression on Facebook.
#  
# ## Insights
# Core values are not necessarily easy topics to cover on social media and making the topic engaging requires creativity. My assumption was the team did not fully understand the company's values and how to talk about them. That's why they tried to avoid the topic. Instead, they posted value 4 content because it's an "easy win". 
# 
# 
# ## Action items
# - As the low performance of content about the three core values is a critical issue, reinforce the brand messaging to communicate core values by providing the social media team with brand training.
# - Continue to produce the "value 4" content as it helps maintain the social media accounts' engagement.
# - Post more of the "value 5" content on LinkedIn.
# - Reduce the amount of the "value 6" content on Facebook. 
# - Explore new ways to improve Facebook's organic impression since there is little correlation between post engagements and impressions. The basic strategy for social media is to improve engagement, which also helps organic impressions, but Facebook needs a different strategy.
# 
# 
# ## Limitation and future project
# The social media team had to manually tag the content type, which was extremely time-consuming. Also, tagging can be subjective without a clear guideline. This process could be improved by using NLP.

# In[1]:



import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 999) #This option force Jupyternotebook to show all columns. 


# In[2]:


cols_to_use =['Date', 'Post ID', 'Network','Post Type','Impressions',
       'Organic Impressions', 'Engagement Rate (per Impression)',
       'Engagements', 'Reactions', 'Comments',
       'Shares','Tags']
post_raw = pd.read_csv('Projects/Social Media Content Analysis/modifiled_post_performance_data.csv', parse_dates=['Date'], usecols=cols_to_use)


# In[3]:


#Pull only "Post" type data
post_type_to_keep = (post_raw['Post Type'] == 'Post')| (post_raw['Post Type'] == 'Tweet')
post_raw = post_raw[post_type_to_keep]
#fill na with 0
post_raw = post_raw.fillna(0)


# In[4]:


post_raw.head(5)


# In[5]:


post_raw.info()


# In[6]:


# A function to change dtype of engagement and impression to int64 if their dtype if object
def change_dtype(platform):
    if platform["Engagements"].dtype == "object":
        platform['Engagements'] = platform['Engagements'].str.replace(",","")
        platform['Engagements'] = platform['Engagements'].fillna(0)
        platform['Engagements'] = platform['Engagements'].astype('int64')
    
    if platform['Impressions'].dtype == "object":
        platform['Impressions'] = platform['Impressions'].str.replace(",","")
        platform['Impressions'] = platform['Impressions'].fillna(0)
        platform['Impressions'] = platform['Impressions'].astype('int64')

#A function to calculate engagement rate
def engagement_calculator(platform):
    platform['Engagement Rate'] = platform['Engagements']/platform['Impressions']

    data_to_check = ['Date', 'Network','Impressions', 'Engagements','Post ID', 'Engagement Rate']
    platform['Engagement Rate'].replace(np.inf, np.nan, inplace = True)
    platform.dropna(subset=data_to_check, inplace=True)


# In[7]:


#A function to clean data by network except facebook

def clean_data_by_network(network, data):
    network = data[data['Network']==network]
    network = network[['Date', 'Network','Impressions', 'Engagements', 'Post ID', 'Tags']]

    change_dtype(network)
    engagement_calculator(network)
    
    return network

    


# In[8]:


#A function to clean facebook data

def clean_facebook_data(data):
    Facebook = data[data['Network']=='Facebook']
    Facebook = Facebook[['Date', 'Network','Organic Impressions', 'Comments', 'Shares', 'Reactions', 'Post ID', 'Tags']]

    cols_to_check_dtype = ['Organic Impressions', 'Comments', 'Shares', 'Reactions']
    
    for d in cols_to_check_dtype:
        if Facebook[d].dtype == "object":
            Facebook[d] = Facebook[d].str.replace(",","")
            Facebook[d] = Facebook[d].fillna(0)
            Facebook[d] = Facebook[d].astype('int64')
            
    
    #Conbine Reaction, Comments and Share
    Facebook['Facebook Engagements'] = Facebook['Reactions']+ Facebook['Comments']+ Facebook['Shares']
    
    #Calculate engagement rate
    Facebook['Engagement Rate'] = Facebook['Facebook Engagements']/Facebook['Organic Impressions']
    Facebook['Engagement Rate'].replace(np.inf, np.nan, inplace = True)
    
    #remove reactions, Comments, and Shares
    to_keep = ['Date', 'Network','Organic Impressions', 'Facebook Engagements','Post ID', 'Engagement Rate','Tags']
    Facebook = Facebook[to_keep]
    
    Facebook.rename(columns = {"Organic Impressions": "Impressions", "Facebook Engagements":"Engagements"}, inplace = True)
    data_to_check = ['Date', 'Network','Impressions', 'Engagements','Post ID', 'Engagement Rate']
    Facebook.dropna(inplace=True, subset=data_to_check)
    
    return Facebook
    


# In[9]:


facebook_cleaned = clean_facebook_data(post_raw).copy()
twitter_cleaned = clean_data_by_network('Twitter', post_raw ).copy()
instagram_cleaned = clean_data_by_network('Instagram', post_raw ).copy()
linkedin_cleaned = clean_data_by_network('LinkedIn', post_raw ).copy()


# In[10]:


#Concatinate the 4 differente DFs
Networks = [facebook_cleaned, twitter_cleaned, instagram_cleaned, linkedin_cleaned]
all_data = pd.concat(Networks)

#Rearrange the column order
all_data = all_data[['Date', 'Network', 'Impressions', 'Engagements', 'Engagement Rate', 'Post ID', 'Tags']]


# In[11]:


all_data.head()


# In[12]:


all_data.info()


# ## Processing Tags
# 

# In[13]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[14]:


#A main function to process tag strings
def process_tags(df):
    df_tags = df.copy()
    
    #A function clean up tag strings 
    def clean_up_tags(df):
        
       # df_tags = df.dropna()  #Remove Nan because Nan considered as float
        df['Tags'] = df['Tags'].str.lower()  #format the tags data by making them lowercase
        df['Tags'] = df['Tags'].str.split(pat=', ')  #split each of strings into a list
        df = df[df['Tags'].notna()]
        return df
    df_tags = clean_up_tags(df_tags)
    #print(df_tags)
    
    
    #A function to create a list to collect all unique tags from these lists
    def collect_tags(new_df):
        tags = set(new_df['Tags'].explode().values) #Create a set to remove duplicate first
        tags = list(tags) #convert the set to list
        tags = [tag for tag in tags if str(tag)!= 'nan']
        return tags
    global tags
    tags = collect_tags(df_tags)
    #print(tags)


    #A function to create a new boolean colum for each tag
    def create_tag_cols(new_df, tag_list):
        for tag in tag_list:
            new_df[tag] = [tag in new_df['Tags'].loc[i] for i in new_df.index]
        return new_df
    df_tags = create_tag_cols(df_tags, tags)
    

    #A function to create a new df to store data by category
    def create_category_df(df_tags, tags):

        #Creating a list of the number of tags used
        num_of_post = []
        for cat in tags:
            num_of_post.append(df_tags[cat].values.sum())

        data = {'Category': tags, 'Number of posts': num_of_post,}
        cat_df = pd.DataFrame(data)
        cat_df = cat_df.set_index('Category')
        cat_df['Impressions']= np.nan
        cat_df['Engagements']= np.nan  

        #A function to extract key metrics from df_tags
        metrics_to_use = ['Impressions','Engagements']
        def get_metrics(metrics_list):
            for cat in tags:
                for metric in metrics_list:
                    cat_df.loc[cat, metric] = df_tags[df_tags[cat]==1][metric].sum()
            return cat_df

        cat_df = get_metrics(metrics_to_use)

        #function to calculate engagement rate
        def get_engagement_rage(category_df):
            category_df['Engagement Rate']=category_df['Engagements']/category_df['Impressions']
            category_df['Average Engagement']=category_df['Engagements']/category_df['Number of posts']
            category_df['Average Impression']=category_df['Impressions']/category_df['Number of posts']
            category_df = category_df.round(2)
            category_df.sort_values(by='Engagement Rate', inplace = True, ascending=False)
            category_df.reset_index(inplace = True)
            return category_df

        cat_df = get_engagement_rage(cat_df)
        return cat_df
    cat_df = create_category_df(df_tags, tags)
    
    return cat_df
 


# In[15]:


content_category_df = process_tags(all_data)
content_category_df.head()


# In[16]:


def export_tag_report(data, MMYY):
    filename = f"content_category_report_{MMYY}.csv"
    data.to_csv('filename')


# In[17]:


export_tag_report(content_category_df, "2020")


# ## DataFrame by platforms
# #### DATA TO USE
# `twitter_cleaned`
# `facebook_cleaned`
# `instagram_cleaned`
# `linkedin_cleaned`

# In[18]:


twitter = process_tags(twitter_cleaned)
facebook = process_tags(facebook_cleaned)
instagram = process_tags(instagram_cleaned)
linkedin = process_tags(linkedin_cleaned)


# In[19]:


twitter.describe()


# ## Creating Subsettings for content types

# In[20]:


tags


# In[21]:


#Creating a list of primary content (Value propositions + social media origianl categorids)
primary_content= ['core value 1', 'value 4','value 5', 'core value 2','value 6','core value 3','corgi','husky','value 7', 'german shepherd']


# In[22]:


content_category_df["Category"].unique()


# In[23]:


#subsetting primary content category only
performance_by_primary = content_category_df[content_category_df['Category'].isin(primary_content)]
performance_by_primary


# In[24]:


#subsetting school only
#performance_by_school = content_category_df[content_category_df['Category'].isin(schools)]
#performance_by_school.head()


# In[25]:


#subsetting other content type only
#criteria = ~content_category_df['Category'].isin(schools) | ~content_category_df['Category'].isin(performance_by_primary)
#performance_by_secondary = content_category_df[criteria]
#performance_by_secondary.head()


# ## Visualizayion: Primary Content Category

# In[26]:


from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import seaborn as sns


# In[27]:


#Create color pallet for each category

colors = {'core value 1':'red', 'value 4':'darkorange','value 5':'gold', 'core value 2':'yellow', 'value 6':'yellowgreen', 'core value 3':'green','corgi':'teal','husky':'skyblue','value 7':'blue', 'german shepherd':'pink'}


# In[28]:


#aggregate the category performance using pivot_table
agg_perimary_category = pd.pivot_table(performance_by_primary, index=['Category'], values=['Number of posts', 'Impressions', 'Engagements', 'Engagement Rate', 'Average Engagement', 'Average Impression'], aggfunc={'Number of posts':np.sum, 'Impressions':np.mean, 'Engagements':np.mean, 'Engagement Rate':np.mean, 'Average Impression':np.mean, 'Average Engagement':np.mean})
agg_perimary_category = agg_perimary_category.reset_index()


agg_perimary_category['color']= agg_perimary_category['Category'].apply(lambda x: colors[x])
agg_perimary_category


# ### Performance by Platform

# In[29]:


twitter_primary = twitter[twitter['Category'].isin(primary_content)].reset_index(drop=True)
twitter_primary['color']=twitter_primary['Category'].apply(lambda x: colors[x])

facebook_primary = facebook[facebook['Category'].isin(primary_content)].reset_index(drop=True)
facebook_primary['color']=facebook_primary['Category'].apply(lambda x: colors[x])

instagram_primary = instagram[instagram['Category'].isin(primary_content)].reset_index(drop=True)
instagram_primary['color']=instagram_primary['Category'].apply(lambda x: colors[x])

linkedin_primary = linkedin[linkedin['Category'].isin(primary_content)].reset_index(drop=True)
linkedin_primary['color']=linkedin_primary['Category'].apply(lambda x: colors[x])


# In[30]:


twitter_primary


# In[31]:


fig, axes = plt.subplots(2,2, figsize = (18,10))

fig.suptitle('Average Engagemet Rate by Content Categories')
fig.subplots_adjust(hspace=0.5)

#Twitter
g = sns.barplot(ax= axes[0,0], data=twitter_primary, x= 'Category', y = 'Engagement Rate', palette=twitter_primary['color'], order=twitter_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes[0,0].set_title('Twitter')


#Facebook
g = sns.barplot(ax= axes[0,1], data=facebook_primary, x= 'Category', y = 'Engagement Rate', palette=facebook_primary['color'],order=facebook_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes[0,1].set_title('Facebook')

#Instagram
g = sns.barplot(ax= axes[1,0], data=instagram_primary, x= 'Category', y = 'Engagement Rate',palette=instagram_primary['color'],order=instagram_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes[1,0].set_title('Instagram')

#LinkedIn
g = sns.barplot(ax= axes[1,1], data=linkedin_primary, x= 'Category', y = 'Engagement Rate',palette=linkedin_primary['color'],order=linkedin_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes[1,1].set_title('LinkedIn');


# In[32]:


#the number of post

fig2, axes2 = plt.subplots(2,2, figsize = (18,10))

fig2.suptitle('The total number of post by Content Categories')
fig2.subplots_adjust(hspace=0.5)

#wtitter
g = sns.barplot(ax= axes2[0,0], data=twitter_primary, x= 'Category', y = 'Number of posts', palette=twitter_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes2[0,0].set_title('Twitter')

#Facebook
g = sns.barplot(ax= axes2[0,1], data=facebook_primary, x= 'Category', y = 'Number of posts', palette=facebook_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes2[0,1].set_title('Facebook')

#Instagram
g = sns.barplot(ax= axes2[1,0], data=instagram_primary, x= 'Category', y = 'Number of posts',palette=instagram_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes2[1,0].set_title('Instagram')


#LinkedIn
g = sns.barplot(ax= axes2[1,1], data=linkedin_primary, x= 'Category', y = 'Number of posts',palette=linkedin_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes2[1,1].set_title('LinkedIn');


# In[33]:


#Median impression

fig3, axes3 = plt.subplots(2,2, figsize = (18,10))

fig3.suptitle('Average impression by Content Categories')
fig3.subplots_adjust(hspace=0.5)

g = sns.barplot(ax= axes3[0,0], data=twitter_primary, x= 'Category', y = 'Average Impression', palette=twitter_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes3[0,0].set_title('Twitter')


#Facebook
g = sns.barplot(ax= axes3[0,1], data=facebook_primary, x= 'Category', y = 'Average Impression', palette=facebook_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes3[0,1].set_title('Facebook')

#Instagram
g = sns.barplot(ax= axes3[1,0], data=instagram_primary, x= 'Category', y = 'Average Impression',palette=instagram_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes3[1,0].set_title('Instagram')

#LinkedIn
g = sns.barplot(ax= axes3[1,1], data=linkedin_primary, x= 'Category', y = 'Average Impression',palette=linkedin_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes3[1,1].set_title('LinkedIn');


# In[34]:


#Median engagement

fig4, axes4 = plt.subplots(2,2, figsize = (18,10))

fig4.suptitle('Average Engagement by Content Categories')
fig4.subplots_adjust(hspace=0.5)


g = sns.barplot(ax= axes4[0,0], data=twitter_primary, x= 'Category', y = 'Average Engagement', palette=twitter_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes4[0,0].set_title('Twitter')


#Facebook
g = sns.barplot(ax= axes4[0,1], data=facebook_primary, x= 'Category', y = 'Average Engagement', palette=facebook_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes4[0,1].set_title('Facebook')

#Instagram
g = sns.barplot(ax= axes4[1,0], data=instagram_primary, x= 'Category', y = 'Average Impression',palette=instagram_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes4[1,0].set_title('Instagram')

#LinkedIn
g = sns.barplot(ax= axes4[1,1], data=linkedin_primary, x= 'Category', y = 'Average Engagement',palette=linkedin_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes4[1,1].set_title('LinkedIn');


# ### Twitter

# In[35]:


fig, axes_t = plt.subplots(2,2, figsize = (18,10))

fig.suptitle('Twitter Performance', fontsize=20)
fig.subplots_adjust(hspace=0.5)


#Number of post
g = sns.barplot(ax= axes_t[0,0], data=twitter_primary, x= 'Category', y = 'Number of posts',palette=twitter_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_t[0,0].set_title('The total number of post')

#Average Impression
g = sns.barplot(ax= axes_t[0,1], data=twitter_primary, x= 'Category', y = 'Average Impression',palette=twitter_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_t[0,1].set_title('Average Impression')


#Engagement rate
g = sns.barplot(ax= axes_t[1,0], data=twitter_primary, x= 'Category', y = 'Engagement Rate', palette=twitter_primary['color'],order=twitter_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_t[1,0].set_title('Engagement Rate')


#Average Engagement
g = sns.barplot(ax= axes_t[1,1], data=twitter_primary, x= 'Category', y = 'Average Engagement', palette=twitter_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_t[1,1].set_title('Average Engagement');


# ## Facebook

# In[36]:


fig, axes_f = plt.subplots(2,2, figsize = (18,10))

fig.suptitle('Facebook Performance', fontsize=20)
fig.subplots_adjust(hspace=0.5)


#Number of post
g = sns.barplot(ax= axes_f[0,0], data=facebook_primary, x= 'Category', y = 'Number of posts',palette=facebook_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_f[0,0].set_title('The total number of post')

#Average Impression
g = sns.barplot(ax= axes_f[0,1], data=facebook_primary, x= 'Category', y = 'Average Impression',palette=facebook_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_f[0,1].set_title('Average Impression')


#Engagement rate
g = sns.barplot(ax= axes_f[1,0], data=facebook_primary, x= 'Category', y = 'Engagement Rate', palette=facebook_primary['color'],order=facebook_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_f[1,0].set_title('Engagement Rate')


#Average Engagement
g = sns.barplot(ax= axes_f[1,1], data=facebook_primary, x= 'Category', y = 'Average Engagement', palette=facebook_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_f[1,1].set_title('Average Engagement');


# ## Instagram

# In[37]:


fig, axes_i = plt.subplots(2,2, figsize = (18,10))

fig.suptitle('Instagram Performance', fontsize=20)
fig.subplots_adjust(hspace=0.5)


#Number of post
g = sns.barplot(ax= axes_i[0,0], data=instagram_primary, x= 'Category', y = 'Number of posts',palette=instagram_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_i[0,0].set_title('The total number of post')

#Average Impression
g = sns.barplot(ax= axes_i[0,1], data=instagram_primary, x= 'Category', y = 'Average Impression',palette=instagram_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_i[0,1].set_title('Average Impression')


#Engagement rate
g = sns.barplot(ax= axes_i[1,0], data=instagram_primary, x= 'Category', y = 'Engagement Rate', palette=instagram_primary['color'],order=instagram_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_i[1,0].set_title('Engagement Rate')


#Average Engagement
g = sns.barplot(ax= axes_i[1,1], data=instagram_primary, x= 'Category', y = 'Average Engagement', palette=instagram_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_i[1,1].set_title('Average Engagement');


# ## LinkedIn

# In[38]:


fig, axes_l = plt.subplots(2,2, figsize = (18,10))

fig.suptitle('LinkedIn Performance', fontsize=20)
fig.subplots_adjust(hspace=0.5)


#Number of post
g = sns.barplot(ax= axes_l[0,0], data=linkedin_primary, x= 'Category', y = 'Number of posts',palette=linkedin_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_l[0,0].set_title('The total number of post')

#Average Impression
g = sns.barplot(ax= axes_l[0,1], data=linkedin_primary, x= 'Category', y = 'Average Impression',palette=linkedin_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_l[0,1].set_title('Average Impression')


#Engagement rate
g = sns.barplot(ax= axes_l[1,0], data=linkedin_primary, x= 'Category', y = 'Engagement Rate', palette=linkedin_primary['color'],order=linkedin_primary.sort_values('Engagement Rate', ascending=False).Category)
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_l[1,0].set_title('Engagement Rate')


#Average Engagement
g = sns.barplot(ax= axes_l[1,1], data=linkedin_primary, x= 'Category', y = 'Average Engagement', palette=linkedin_primary['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
axes_l[1,1].set_title('Average Engagement');


# In[ ]:





# In[ ]:




