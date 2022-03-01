#!/usr/bin/env python
# coding: utf-8

# # Social Media Content Analysis
# 
# I analyzed the performance of different content categories on social media platforms to identify the most optimal social media platform to communicate the company's value propositions. Also, I generated data visualization so that creative team members intuitively understand which categories are performing or not performing. 
# 
# The analysis relived that the posts about core values are not as many as other content categories, and their performance was the worst. This result led me to shift the strategic marketing plan to focus more on internal brand training so that team members understand the value propositions from the first place. 
# 
# *This project was a good example of how analysis can influence strategic marketing planning and help a marketing team's day-to-day channel performance.*

# ## Background
# An higher education instition that I worked for (Let's say "ABC University") has 6 core values; **faculty, curriculum, career opportunity**, location, diversity, alumni network. (The first three values are the key values.) Our social media team's goal was to communicate these core values in engaging way while maximing the exposure (=impression). In order to acquire high impressions, make the posts highly engaging is essentioal but these core values are not necessarily "fun" topics to discuss.
# 
# The social media team used to post the same content across 4 major social media channels (Facebook, LinkedIn, Instagram, and Twitter) or occationally posted different content on paricular channel, but these creative deicison was not based on any data or assumtion. 
# 
# *This project was a good example of how analysis can influence strategic marketing planning and help a marketing team's day-to-day channel performance.*
# 
# 
# ## Objective
# Identify the most optimal platform(s) for each core value. Make the creative deicision.
# 
# ## Audience
# Social media team
# 
# ## Measure of Success
# 
# - Engagement rate (# of post engagement / # of impression) *– Engagement is user' behaivors such as "Like", "Comments", and "Share". Higher the engagement rate, the higher the quality of content is.
# - The number of posts
# - The number of impression *– This indicate how much a single social media post is shown on user's timeline. This is usually used as an indirect measure of brand awareness*
# 
# ## Data Source
# - The raw data of social media posts that published between past 12 months (January 1, 2020, December 21, 2020) were exported from a social media management platform, Sprout Social as `.csv`.
# - In addition to the 6 core values, a few content category tags are also used. 
# - For confidentiacility, a part of original data is hidden in this report
# 
# ## Insights
# - All of three key values (faculty, curriculum, and career opporunity) were the worst performing content across the platforms.
# - The number of post is heavly skewed to "student work" category on social meida and the category is performing well. However, the post about core values are very little.
# - The engagement of "student work" category on Facebook is significantly higher than other content categories. However, the impression is not necessarily higher. This implies there might not be a strong correlation between post engagements and impression on Facebook.
# 
# 
# ## Action items
# - As the low performance of content about the three key core values are critical issue, I conducted an internal brand training to educate the team members about the company's value proposition. 
# - Explore new ways to improve Facebook's organic impression since there is little correlation between post engagements and impression. The basic strategy for social media is to improve engagement, which also help organic impression, but Facebook needs a different strategy.
# 
# 
# ## Limitation and future project
# Social media team had to manually tag the content type, which was extremly time consuing. Also, tagging can be subjective without a clear guideline. This process can be improved by using NLP.

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 999) #This option force Jupyternotebook to show all columns. 


# In[2]:


cols_to_use =['Date', 'Post ID', 'Network','Post Type','Link', 'Impressions',
       'Organic Impressions', 'Engagement Rate (per Impression)',
       'Engagements', 'Reactions', 'Comments',
       'Shares','Tags']


# In[3]:


post_raw = pd.read_csv('Post Performance (Academy of Art University) January 1, 2020 - December 31, 2020.csv', parse_dates=['Date'], usecols=cols_to_use)


# In[5]:


#Pull only "Post" type data
post_type_to_keep = (post_raw['Post Type'] == 'Post')| (post_raw['Post Type'] == 'Tweet')
post_raw = post_raw[post_type_to_keep]
#fill na with 0
post_raw = post_raw.fillna(0)


# In[5]:


post_raw.head(5)


# In[6]:


post_raw.info()


# In[7]:


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


# In[8]:


#A function to clean data by network except facebook

def clean_data_by_network(network, data):
    network = data[data['Network']==network]
    network = network[['Date', 'Network','Impressions', 'Engagements', 'Post ID', 'Tags']]

    change_dtype(network)
    engagement_calculator(network)
    
    return network

    


# In[9]:


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
    


# In[52]:


facebook_cleaned = clean_facebook_data(post_raw).copy()
twitter_cleaned = clean_data_by_network('Twitter', post_raw ).copy()
instagram_cleaned = clean_data_by_network('Instagram', post_raw ).copy()
linkedin_cleaned = clean_data_by_network('LinkedIn', post_raw ).copy()


# In[53]:


#Concatinate the 4 differente DFs
Networks = [facebook_cleaned, twitter_cleaned, instagram_cleaned, linkedin_cleaned]
all_data = pd.concat(Networks)

#Rearrange the column order
all_data = all_data[['Date', 'Network', 'Impressions', 'Engagements', 'Engagement Rate', 'Post ID', 'Tags']]


# In[15]:


all_data.head()


# In[54]:


export_cols = ['Date', 'Network', 'Impressions', 'Engagements', 'Engagement Rate', 'Post ID']

def export_for_tableau(data_period, data):
    filename = f"Individual_post_performance_{data_period}.csv"
    data.to_csv(filename, columns=export_cols)


# In[55]:


export_for_tableau('January 1, 2020 - December 31, 2020', all_data)


# In[56]:


all_data.info()


# ## Processing Tags
# 

# In[57]:


#Replace "student artwork" with "student work" because in the mid of 2020, we changed the SproutSocial tagging rules

all_data['Tags'] = all_data['Tags'].replace({'Student Artwork':'Student Work','alumni success':'success','Student success':'success','faculty success':'faculty'}, regex=True)
all_data.head()


# In[58]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[59]:


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
 


# In[60]:


content_category_df = process_tags(all_data)
content_category_df.head()


# In[24]:


def export_tag_report(data, MMYY):
    filename = f"content_category_report_{MMYY}.csv"
    data.to_csv('filename')


# In[25]:


export_tag_report(content_category_df, "2020")


# ## DataFrame by platforms
# #### DATA TO USE
# `twitter_cleaned`
# `facebook_cleaned`
# `instagram_cleaned`
# `linkedin_cleaned`

# In[26]:


twitter = process_tags(twitter_cleaned)
facebook = process_tags(facebook_cleaned)
instagram = process_tags(instagram_cleaned)
linkedin = process_tags(linkedin_cleaned)


# In[27]:


twitter.describe()


# ## Creating Subsettings for content types
# - Primary category: Top content hierarchy
#     `curriculum`, `success`,`awards & honors`, `partnership`, `academy cares`,`faculty`,`events`, `engagement`,`sf`, 
#     `student artwork`
# - Secondary category: Internal user only to collect data of spesific campaigns
# - Department
# 
# 

# In[28]:


tags


# In[61]:


#Creating a list of primary content categories
primary_content = ['curriculum', 'success','awards & honors', 'partnership', 'academy cares','faculty','events', 'engagement','sf', 'student work']

#Creating a list of departments
schools = ['act','adv','anm','arch','art edu','art history', 'athletics', 'com', 'fa', 'fsh','gam','gr','iad', 'ids','ill','jem','lan','mptv','mus','ph','vis', 'wnm','wri']


# In[62]:


#subsetting primary content category only
performance_by_primary = content_category_df[content_category_df['Category'].isin(primary_content)]
performance_by_primary.head()


# In[31]:


#subsetting school only
performance_by_school = content_category_df[content_category_df['Category'].isin(schools)]
performance_by_school.head()


# In[32]:


#subsetting other content type only
criteria = ~content_category_df['Category'].isin(schools) | ~content_category_df['Category'].isin(performance_by_primary)
performance_by_secondary = content_category_df[criteria]
performance_by_secondary.head()


# ## Visualizayion: Primary Content Category

# In[63]:


from matplotlib import pyplot as plt
import seaborn as sns


# In[64]:


#Create color pallet for each category
colors = {'curriculum': 'red', 'success':'darkorange','awards & honors':'gold', 'partnership':'yellow', 'academy cares':'yellowgreen','faculty':'green','events':'teal', 'engagement':'skyblue','sf':'blue', 'student work':'pink'}


# In[65]:


#aggregate the category performance using pivot_table
agg_perimary_category = pd.pivot_table(performance_by_primary, index=['Category'], values=['Number of posts', 'Impressions', 'Engagements', 'Engagement Rate', 'Average Engagement', 'Average Impression'], aggfunc={'Number of posts':np.sum, 'Impressions':np.mean, 'Engagements':np.mean, 'Engagement Rate':np.mean, 'Average Impression':np.mean, 'Average Engagement':np.mean})
agg_perimary_category = agg_perimary_category.reset_index()


agg_perimary_category['color']= agg_perimary_category['Category'].apply(lambda x: colors[x])
agg_perimary_category


# ### Overall Performance

# In[70]:


fig1, ax1 = plt.subplots(2,2, figsize = (20,15), squeeze=False)
fig1.subplots_adjust(hspace=0.4)

# The total number of post
g = sns.barplot(ax= ax1[0,0], 
                data=agg_perimary_category, 
                x= 'Category', 
                y = 'Number of posts', 
                palette=agg_perimary_category['color']
               )
g.set_xticklabels(g.get_xticklabels(),rotation=20)
ax1[0,0].set_title('Total number of post')

# Average impression
g = sns.barplot(ax= ax1[0,1], data=agg_perimary_category, x= 'Category', y = 'Average Impression', palette=agg_perimary_category['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
ax1[0,1].set_title('Average impression')

#Average Engagement 
g = sns.barplot(ax= ax1[1,0], data=agg_perimary_category, x= 'Category', y = 'Average Engagement', palette=agg_perimary_category['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
ax1[1,0].set_title('Average Engagement')

#Average Engagement rate
g = sns.barplot(ax= ax1[1,1], data=agg_perimary_category, x= 'Category', y = 'Engagement Rate', palette=agg_perimary_category['color'])
g.set_xticklabels(g.get_xticklabels(),rotation=20)
ax1[1,1].set_title('Median Engagement Rate');


# ### Performance by Platform

# In[71]:


twitter_primary = twitter[twitter['Category'].isin(primary_content)].reset_index(drop=True)
twitter_primary['color']=twitter_primary['Category'].apply(lambda x: colors[x])

facebook_primary = facebook[facebook['Category'].isin(primary_content)].reset_index(drop=True)
facebook_primary['color']=facebook_primary['Category'].apply(lambda x: colors[x])

instagram_primary = instagram[instagram['Category'].isin(primary_content)].reset_index(drop=True)
instagram_primary['color']=instagram_primary['Category'].apply(lambda x: colors[x])

linkedin_primary = linkedin[linkedin['Category'].isin(primary_content)].reset_index(drop=True)
linkedin_primary['color']=linkedin_primary['Category'].apply(lambda x: colors[x])


# In[49]:


twitter_primary


# In[72]:


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


# In[77]:


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


# In[78]:


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


# In[42]:


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

# In[79]:


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

# In[44]:


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

# In[80]:


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

# In[81]:


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




