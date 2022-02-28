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

# In[ ]:




