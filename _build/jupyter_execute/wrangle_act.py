#!/usr/bin/env python
# coding: utf-8

# # WeRateDogs Twitter Analysis

# ### Introduction
# In this project, we will analyze a popular Twitter account [@dog_rates](twitter.com/dog_rates), also known as WeRateDogs. WeRateDogs rates people's dogs with a humorous comment about the dog. These ratings almost always have a denominator of 10 and a numerator that greater than 10, such as as11/10, 12/10, 13/10, etc. People love WeRateDogs's tweets because of this fun rating system! 
# 
# Through this analysis, we will find out the relationship between WeRateDog's rating and people's reactions; likes and retweets. Does a higher rating bring more like or retweet? Let's find out!
# 
# Also, we will find out the popular dog breed by the number of retweets and likes to find out internet users' favorite dog breeds.
# 
# ![weratedogs](images/WeRateDogs_Twitter.png)
# 
# 
# ### Analysis
# 
# We are going to analyze:
# 1.  Relationship between the ratings and people's response (Retweet and Like)
# 2.  Relationship between the ratings and the god stage
# 3.  Relationship between the ratings and god breeds
# 
# #### Relationship between the ratings and people's response (Retweet and Like)
# > The dog rating and the number of retweets and the number of likes have a positive relationship. i.e. the higher the rating is, the more retweets and likes the account gets.
# 
# > Due to its WeRateDogs's unique rating system, there a few extream ratings that exceed 20/10 such as 1750/10, 420/10 and 75/10. 
# 
# > Interestingly, these extrez
# mely high ratings do not affect the user's response.  Also, the rating of 13/10 is most likely to get many retweets and likes.  The number of retweets and likes are a positive relationship. The more retweets a tweet gets, the more like the tweet gets, and vise visa.  This makes sense as a tweet is retweeted or liked, there is a higher chance to be seen by many other users. 
# 
# 
# 
# #### Relationship between the ratings and the god stage
# > Dog stage does not so much affect the rating but dogs in 'puppo' stage get slightly higher ratings
# 
# #### Relationship between the ratings and god breeds
# >The most frequently posted dog breeds are Golden retriever, Pembroke, and Labrador retriever. The most highly rated dog breeds by WeRateDogs are Samoyed, Chow, Golden retriever. 
# From these results, we can tell that WeRateDogs have a tendency to post Golden retriever because WeRateDogs personally like Golden retriever. As this twitter account is so popular, I expect WeRateDogs receives a lot of submission from users and WeRateDogs prescreens based on their preference. If you want to be featured on WeRateDogs account, sending Golden retriever's picture might be a good idea.
# 
# 
# >On the other hand, the most retweeted dog breeds are Labrador retriever, French Bulldog, and Samoyed and the most liked dog breeds are French bulldog, Labrador retriever, and Samoyed. The followers of WeRateDogs like French Bulldogs and Samoyed. If you want your dog picture to be seen by many Twitter users, sending French Bulldog and Samoyed might be a good idea.
# 
# #### Note
# I extracted image prediction data with more than 70% of confidence rate to enhance the accuracy of the analysis. Also, I selected the 10 most frequently posted dog breeds for this analysis. 
# 
# 
# ```python
# 
# ```

# ## Gater

# In[1]:


#import necessary libraries

import pandas as pd
import numpy as np
import requests
import os


# First, we need to collect 3 types of data below: 
# 
# 1) `twitter-archive-enhanced.csv` : The WeRateDogs Twitter archive provided by Udacity.
# 
# 2) `image_predictions.tsv` : The tweet image predictions, i.e., what breed of dog (or other object, animal, etc.) is present in each tweet according to a neural network. This data is hosted on Udacity's servers. This can be donwloaded from [here](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv)
# 
# 3) `tweet_json.txt` : Tweet's JSON data containing retweet count, favorite count, and tweet ID etc.

# In[2]:


# read twitter_archive_enhanced.csv
tw_archive = pd.read_csv('twitter-archive-enhanced.csv')
tw_archive.head()


# In[4]:


#Donwload image_predictions.tsv from Udacity's servers

url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response = requests.get(url)
response


# In[5]:


with open (url.split('/')[-1], mode = 'wb') as file:
    file.write(response.content)


# In[4]:


image_predict = pd.read_csv('image-predictions.tsv', sep='\t')
image_predict.head(5)




# In[5]:


#read twitter data as Json file

import tweepy
from tweepy import OAuthHandler
import json
from timeit import default_timer as timer

# Query Twitter API for each tweet in the Twitter archive and save JSON in a text file
# These are hidden to comply with Twitter's API terms and conditions
consumer_key = 'YOUR API KEY'
consumer_secret = 'YOUR API KEY'
access_token = 'YOUR API KEY'
access_secret = 'YOUR API KEY'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

tweet_ids = tw_archive.tweet_id.values
len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepError as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)


# In[9]:


import json
from pandas.io.json import json_normalize
json_df = pd.DataFrame()
arr = []
with open('tweet_json.txt') as json_file:
    for row in json_file:
        data = json.loads(row)
        arr.append(data)

jason_df = pd.DataFrame(json_normalize(arr))
jason_df.head()


# ## Assess

# In[10]:


#Change the number of columns to be displayed to assess all of the columns
pd.options.display.max_columns = 999


# ####  Enhanced Twitter Archive

# In[11]:


tw_archive.head()


# In[12]:


tw_archive.info()


# In[13]:


tw_archive.describe()


# In[14]:


tw_archive.query('rating_numerator == 1776').tweet_id.unique()


# The max `rating_numerator` value 1776 looks invalid but when I checked [the original tweet](https://twitter.com/dog_rates/status/749981277374128128), WeRateDogs actually gave 1776/10 rating to the dog.

# In[15]:


tw_archive['tweet_id'].duplicated().sum()


# #### Image Predictions

# In[16]:


image_predict.info()


# In[17]:


image_predict['tweet_id'].duplicated().sum()


# In[18]:


image_predict.head(10)


# #### Additional Data via the Twitter API

# In[19]:


jason_df.info()


# In[20]:


jason_df.head()


# Take out necessary tweet objects from 'jason_df'. I referred to the [twitter's documentation](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object). Here is the list of tweet objects we need for this analysis. 

# - `id`: The integer representation of the unique identifier for this Tweet.
# - `retweet_count`: Number of times this Tweet has been retweeted. 
# - `favorite_count`: Indicates approximately how many times this Tweet has been liked by Twitter users.
# 
# 
# - `in_reply_to_status_id`: If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID. 
# - `quoted_status_id`: This field only surfaces when the Tweet is a quote Tweet. This field contains the integer value Tweet ID of the quoted Tweet.
# - `is_quote_status`: Indicates whether this is a Quoted Tweet. 
# - `retweeted_status.id`: Retweets can be distinguished from typical Tweets by the existence of a retweeted_status attribute.
# 
# 

# In[21]:


tweet_performance = jason_df[['id', 'retweet_count','favorite_count','in_reply_to_status_id','quoted_status_id','is_quote_status', 'retweeted_status.id']]


# In[22]:


tweet_performance.head()


# In[23]:


tweet_performance.info()


# In[24]:


tweet_performance.describe()


# In[25]:


tweet_performance.query('favorite_count == 0').id.unique


# ### Quality issues
# 
# ##### Enhanced Twitter Archive table 
# - There are some invalid rating: the numerator and denominator values are wrong
# - Timestamp is a wrong datatype: Object
# 
# ##### Image Predictions table 
# - Some images are not a dog - We only want to analyze dog data
# - Not all predictions are accurate: The predictions in p1 show the predictions with the highest accuracy level among 3 image predictions
# - Dog names in image predictions contain underscores between words
# 
# ##### Additional Data via the Twitter API table 
# - Replies, quoted retweets, and retweets are included in the tweet data. We want to analyze the dog rating tweet only.
# - Some tweets got only 1 retweet and 0 favorite, which is not likely to happen to such a famous twitter account. - Maybe cause they are retweet or favorite for non-dog rating tweets.
# - The description of individual tweet IDs are different from other data: 'id' need to align with `tweet_id` which are used in other 2 data.
# 
# 
# 
# ### Tidiness issues
# - Take out only the necessary columns
# - dog "stage" should be in one column
# - Retweets and favorite count data should be included in the enhanced Twitter Archive table
# - Image prediction data should be included in the enhanced Twitter Archive table

# ## Clean

# In[26]:


#create copies of each data
tw_archive_clean = tw_archive.copy()
image_predict_clean = image_predict.copy()
tweet_performance_clean = tweet_performance.copy()


# ##### Issue
# There are some invalid rating: the numerator and denominator values are wrong.
# 
# ##### define
# - Drop 0 values from `rating_numerator`.
# - Drop value other than 10 from `rating_denominator`

# ##### Code

# In[27]:


tw_archive_clean = tw_archive_clean[tw_archive_clean.rating_numerator != 0]
tw_archive_clean = tw_archive_clean[tw_archive_clean.rating_denominator == 10]


# ##### Test

# In[28]:


tw_archive_clean.describe()


# ##### Issue
# Timestamp is a wrong datatype: Object
# 
# #### Define
# - Change datatype of 'timestamp' to time stamp using [pandas-to_datetime](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html)

# ##### Code

# In[29]:


tw_archive_clean.timestamp = pd.to_datetime(tw_archive_clean.timestamp)


# ##### Test

# In[30]:


tw_archive_clean.info()


# In[31]:


tw_archive_clean.head()


# ##### Issue
# Some images are not a god - We only want to analyze dog data

# ##### Define
# Drop the rows that `p1_dog`  is False

# ##### Code

# In[32]:


image_predict_clean['p1_dog'] = image_predict_clean[image_predict_clean.p1_dog == True]


# ##### Test

# In[33]:


image_predict_clean[image_predict_clean.p1_dog == False].p1_dog.count()


# ##### Issue
# Not all predictions are accurate: The predictions in p1 show the predictions with the highest accuracy level among 3 image predictions

# ##### Define
# - Compare the values in `p1_conf`, `p2_conf` and `p3_conf` to make sure that `p1_conf` is the highest accuracy level.
# - Drop `p2_conf` and `p3_conf` colums
# 

# ##### Code

# In[34]:


(image_predict_clean['p1_conf'] >= image_predict_clean['p2_conf']).sum()


# In[35]:


(image_predict_clean['p1_conf'] <= image_predict_clean['p3_conf']).sum()


# In[36]:


(image_predict_clean['p2_conf'] <= image_predict_clean['p3_conf']).sum()


# In[37]:


image_predict_clean.drop(['p2','p2_conf', 'p2_dog','p3','p3_conf','p3_dog'], axis =1, inplace = True)


# ##### Test

# In[38]:


image_predict_clean.head()


# ##### Issue
# Dog names in image predictions contain underscores between words.

# ##### Define
# Replace understores in `p1` with whitespaces. 

# In[39]:


image_predict_clean['p1'] = image_predict_clean['p1'].str.replace('_', ' ')


# ##### Test

# In[40]:


image_predict_clean.p1.unique


# ##### Issue
# - Replies, quoted retweets, and retweets are included in the tweet data. We want to analyze the dog rating tweet only.
# - Some tweets got only 1 retweet and 0 favorite, which is not likely to happen to such a famous twitter account. - Maybe cause they are retweet or favorite for non-dog rating tweets.

# ##### Define
# - Drop rows that `in_reply_to_status_id` , `retweeted_status.id`, and `quoted_status_id` is not NaN

# ##### Code

# In[41]:


nan_df = tweet_performance_clean[pd.isnull(tweet_performance_clean['in_reply_to_status_id'])]


# In[42]:


#Create a new column  "retweeted_status_id" because "retweeted_status.id" is invalid column name
nan_df ['retweeted_status_id'] = nan_df['retweeted_status.id']
#Drop the original  "retweeted_status.id"
nan_df = nan_df.drop('retweeted_status.id', axis = 1)


# In[43]:


nan_df = nan_df[pd.isnull(nan_df['retweeted_status_id'])]


# In[44]:


nan_df = nan_df[pd.isnull(nan_df['quoted_status_id'])]


# ##### Test

# In[45]:


nan_df.head(5)


# The original amounts of tweets that are not WeRateDogs' dog rating tweet. They should change to 0 non-null.
# 
# - in_reply_to_status_id    77 non-null float64
# - quoted_status_id         26 non-null float64
# - retweeted_status.id      166 non-null float64

# In[46]:


nan_df.info()


# In[47]:


nan_df.describe()


# In[48]:


nan_df.query('retweet_count == 11').id.unique()


# Since we removed all retweets, quoted retweets and replies, we no longer have tweets with 0 retweet or 1 favorite.
# 
# I checked [the original tweet](https://twitter.com/dog_rates/status/666102155909144576) with the minimum number of the retweet, and the number of retweets and favorites are 11 and 76 respectively, which matches with the description above. 

# ##### Issue
# The description of individual tweet IDs are different from other data: 'id' need to align with tweet_id which are used in other 2 data.

# ##### Define
# Rename the column `id` to `tweet_id`.

# In[49]:


nap_df = nan_df.rename({'id': 'tweet_id'}, axis = 1)


# ##### Test

# In[50]:


nap_df.head()


# ### Tidiness
# 
# ##### Issue
# Take out only the necessary columns

# ##### Define
# - Create a new DataFrame to store only necessary columns

# In[51]:


tweet_count = nap_df[['tweet_id','retweet_count','favorite_count']]
tweet_count.head()


# In[52]:


tw_archive_clean = tw_archive_clean[['tweet_id', 'timestamp','text','rating_numerator','rating_denominator','name','doggo','floofer', 'pupper','puppo']]


# ##### Test

# In[53]:


tw_archive_clean.head()


# In[54]:


tw_archive_clean.info()


# ##### Issue
# The dog "stage" should be in one column

# ##### Define
# - Melt the `doggo`, `floofer`, `pupper`, and `puppo` columns to a `dog_stage` colum using [pandas.melt](https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.melt.html) and store the data in `dog_stage`
# - Merge `dog_stage` with `tw_archive_clean`
# - Drop unnecessary columns
# 

# In[55]:


stage = pd.melt(tw_archive_clean, id_vars= ['tweet_id'] , value_vars = ['doggo', 'floofer', 'pupper','puppo'], var_name = 'dog_stage_type', value_name = 'dog_stage')


# In[56]:


stage['dog_stage'].unique()


# In[57]:


dog_stage = stage.query('dog_stage != "None"')


# In[58]:


dog_stage = dog_stage.drop(['dog_stage_type'], axis = 1)


# In[59]:


tw_archive_clean = pd.merge(tw_archive_clean, dog_stage, on='tweet_id', how='left')


# In[60]:


tw_archive_clean = tw_archive_clean.drop(['name','doggo', 'floofer', 'pupper', 'puppo'], axis = 1)


# ##### Test

# In[61]:


tw_archive_clean.head()


# In[62]:


tw_archive_clean['dog_stage'].unique()


# In[63]:


tw_archive_clean.info()


# ##### Issue
# - Retweets and favorite count data should be included in the enhanced Twitter Archive table
# - Image prediction data should be included in the enhanced Twitter Archive table

# ##### Define
# - Merge `tw_archive_clean` with `tweet_count` using `tweet_id` as a key. To remove retweets, quote retweets, and replies, use `inner` merge method.
# - Merge `tw_archive_clean` with `image_predict_clean`  and `tweet_count` using `tweet_id` as a key. To remove retweets, quote retweets, and replies, use `inner` merge method.

# In[64]:


final_tweet_data = pd.merge(tw_archive_clean, tweet_count, on='tweet_id', how = 'inner')


# In[65]:


final_image_predict = pd.merge(tw_archive_clean, image_predict_clean, on='tweet_id', how = 'inner')
final_image_predict = pd.merge(final_image_predict, tweet_count, on='tweet_id', how = 'inner')


# ##### Test

# In[66]:


final_tweet_data.head()


# In[67]:


final_image_predict.head()


# ### Save the clean DataFrames

# In[68]:


final_tweet_data.to_csv('twitter_archive_master.csv', index = False)
final_image_predict.to_csv('image_predict_master.csv', index = False)


# ## Analysis
# 
# We are going to analyze:
# 1.  Relationship between the ratings and people's response (Retweet and Like)
# 2.  Relationship between the ratings and the god stage
# 3.  Relationship between the ratings and god breeds

# In[69]:


tweets = pd.read_csv('twitter_archive_master.csv')
tweets.head()


# In[70]:


import matplotlib.pyplot as plt

x = tweets['rating_numerator']
y = tweets['favorite_count']

plt.scatter(x,y);


# In[71]:


x = tweets['rating_numerator']
y = tweets['retweet_count']

plt.scatter(x,y);


# #### Retweets

# In[72]:


#Remove outliers from the chart for better analysis
tweets.sort_values(by = ['rating_numerator'], ascending = False)


# In[73]:


wo_outliers =  tweets.query('rating_numerator <= 20')


# In[74]:


x = wo_outliers['rating_numerator']
y = wo_outliers['retweet_count']

plt.scatter(x,y)

plt.title('Relationship between dog rating and retweets')
plt.xlabel('rating numerator')
plt.ylabel('the number of retweets');


# ##### Likes

# In[75]:


x = wo_outliers['rating_numerator']
y = wo_outliers['favorite_count']

plt.scatter(x,y)

plt.title('Relationship between dog rating and likes')
plt.xlabel('rating numerator')
plt.ylabel('the number of likes');


# ##### Relationship between retweets and likes

# In[76]:


x = wo_outliers['retweet_count']
y = wo_outliers['favorite_count']

colors = wo_outliers['rating_numerator']
sizes =  wo_outliers['rating_numerator'] * 20

plt.scatter(x,y, c= colors, s=sizes, alpha = 0.3, cmap = 'viridis')

plt.colorbar();  # show color scale

plt.title('Relationship between retweets and likes')
plt.xlabel('the number of retweets')
plt.ylabel('the number of likes');


# ##### Dog Stage

# In[77]:


mean_rating = wo_outliers.groupby('dog_stage').rating_numerator.mean()


# In[78]:


mean_rating = pd.DataFrame(data=mean_rating)
mean_rating.head()


# In[79]:


x = ['doggo', 'floofer', 'pupper', 'puppo']
y = mean_rating['rating_numerator']

plt.bar(x,y)

plt.title('Relationship between god stage and rating')
plt.ylim([9,13])
plt.xlabel('the number of retweets')
plt.ylabel('the number of likes');


# ### Insights
# > The dog rating and the number of retweets and the number of likes have a positive relationship. i.e. the higher the rating is, the more retweets and likes the account gets.
# 
# > Due to its WeRateDogs's unique rating system, there a few extream ratings that exceed 20/10 such as 1750/10, 420/10 and 75/10. 
# 
# > Interestingly, these extremely high ratings do not affect the user's response.  Also, the rating of 13/10 is most likely to get many retweets and likes.  The number of retweets and likes are a positive relationship. The more retweets a tweet gets, the more like the tweet gets, and vise visa.  This makes sense as a tweet is retweeted or liked, there is a higher chance to be seen by many other users. 
# 
# > Dog stage does not so much affect the rating but dogs in 'puppo' stage get  slightly higher ratings

# ### Dog breed

# In[80]:


images = pd.read_csv('image_predict_master.csv')
images.head()


# In[81]:


images.describe()


# Even for p1 images, the accuracy of image recognition is questionable. So we only use the images with more than 70% of confidence rate to analyze popular dog breed.

# In[82]:


accurate_predict = images.query('p1_conf >= 0.7')
accurate_predict.head()


# In[83]:


#Dog breed by the nuber of post
dog_posts = accurate_predict.groupby('p1').p1.count()
dog_posts = pd.DataFrame(data = dog_posts)
dog_posts= dog_posts.rename({'p1': 'frequency'}, axis = 1)
dog_posts['dog_name'] = dog_posts['frequency'].index

#Sort by frequency
dog_posts = dog_posts.sort_values(by=['frequency'], ascending = False)


# In[84]:


dog_posts.head()


# In[85]:


#Popularity by rating, number of retweet and  likes
#Remove outlierts from rating
wo_outliers_ranking =  accurate_predict.query('rating_numerator <= 20')
popular_breed_by_rating = wo_outliers_ranking.groupby('p1').rating_numerator.mean()
popular_breed_by_rating = pd.DataFrame(data=popular_breed_by_rating)
popular_breed_by_rating['dog_name'] = popular_breed_by_rating['rating_numerator'].index

popular_breed_by_rt = wo_outliers_ranking.groupby('p1').retweet_count.mean()
popular_breed_by_rt = pd.DataFrame(data=popular_breed_by_rt)
popular_breed_by_rt['dog_name'] = popular_breed_by_rt['retweet_count'].index

popular_breed_by_like = wo_outliers_ranking.groupby('p1').favorite_count.mean()
popular_breed_by_like = pd.DataFrame(data=popular_breed_by_like)
popular_breed_by_like['dog_name'] = popular_breed_by_like['favorite_count'].index


# In[86]:


popular_breed_by_rating.head()


# In[87]:


#Merge these 3 popular_breed df with god_posts df
popular_breed = pd.merge(dog_posts, popular_breed_by_rating, on = 'dog_name')
popular_breed = pd.merge(popular_breed, popular_breed_by_rt, on = 'dog_name')
popular_breed = pd.merge(popular_breed, popular_breed_by_like, on = 'dog_name')


# In[88]:


popular_breed.head(10)


# In[89]:


top10_popular_breed = popular_breed.head(10)


# In[90]:


top10_popular_breed


# In[91]:


import numpy as np

N = 10
rating = top10_popular_breed['rating_numerator']

fig, ax = plt.subplots()

ind = np.arange(N)    # the x locations for the groups
width = 0.35         # the width of the bars


rt = top10_popular_breed['retweet_count']
p1 = ax.bar(ind, rt, width)


like = top10_popular_breed['favorite_count']
p2 = ax.bar(ind + width, like, width)


ax.set_title('Dog breed popularity')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(top10_popular_breed['dog_name'], rotation='vertical')

ax.legend((p1[0], p2[0]), ('Retweet', 'Like'))

ax.autoscale_view()

plt.show()


# In[92]:


#Dog breed by frequency
top10_popular_breed_freq = top10_popular_breed.sort_values('frequency',ascending=False)
top10_popular_breed_freq.head(10)


# In[93]:


x = top10_popular_breed_freq['dog_name']
y = top10_popular_breed_freq['frequency']

plt.bar(x,y)

plt.title('Dog breed by frequency')
plt.xticks(rotation='vertical')
plt.xlabel('dog breed')
plt.ylabel('rating');


# In[94]:


x = top10_popular_breed_freq['dog_name']
y = top10_popular_breed_freq['rating_numerator']

plt.bar(x,y)
plt.title('Dog breed by rating')
plt.xticks(rotation='vertical')
plt.xlabel('dog breed')
plt.ylim(10,12.5)
plt.ylabel('rating');


# ### Insight
# >The most frequently posted dog breeds are Golden retriever, Pembroke, and Labrador retriever. The most highly rated dog breeds by WeRateDogs are Samoyed, Chow, Golden retriever. 
# From these results, we can tell that WeRateDogs have a tendency to post Golden retriever because WeRateDogs personally like Golden retriever. As this twitter account is so popular, I expect WeRateDogs receives a lot of submission from users and WeRateDogs prescreens based on their preference. If you want to be featured on WeRateDogs account, sending Golden retriever's picture might be a good idea.
# 
# 
# >On the other hand, the most retweeted dog breeds are Labrador retriever, French Bulldog, and Samoyed and the most liked dog breeds are French bulldog, Labrador retriever, and Samoyed. The followers of WeRateDogs like French Bulldogs and Samoyed. If you want your dog picture to be seen by many Twitter users, sending French Bulldog and Samoyed might be a good idea.

# In[ ]:




