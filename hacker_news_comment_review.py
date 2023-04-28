#!/usr/bin/env python
# coding: utf-8

# # Exploring Hacker News Post

# ## 1. Introduction

# In this project, we'll be working with a dataset of submissions to popular technology site Hacker News.Hacker News is a site started by the startup incubator Y Combinator, where user-submitted stories (known as "posts") receive votes and comments, similar to reddit. Hacker News is extremely popular in technology and startup circles, and posts that make it to the top of the Hacker News listings can get hundreds of thousands of visitors as a result.
# 
# You can find the data set [here](https://www.kaggle.com/datasets/hacker-news/hacker-news-posts "click here")
# 
# We're specifically interested in posts with titles that begin with either Ask HN or Show HN. Users submit Ask HN posts to ask the Hacker News community a specific question. 
# 
# We'll compare these two types of posts to determine the following:
# 
# - Do Ask HN or Show HN receive more comments on average?
# - Do posts created at a certain time receive more comments on average?

# ### 2. Extracting Data 

# In[1]:


from csv import reader #Importing libraries

opened_file = open('hacker_news.csv')
read_file = reader(opened_file)
hn = list(read_file)

print(hn[:5])


# ## 3. Data Cleaning

# We are going to drop the headers so that it will ease our analysis

# In[2]:


headers = hn[0] #Extracting the header
hn = hn[1:]

print(headers)
print('\n')
print(hn[:5])
    


# ### Extracting Ask HN and Show HN Posts

# Now that we've removed the headers from hn, we're ready to filter our data. Since we're only concerned with post titles beginning with Ask HN or Show HN, we'll create new lists of lists containing just the data for those titles.
# 
# To find the posts that begin with either Ask HN or Show HN, we'll use the string method startswith. 

# In[3]:


ask_posts = []
show_posts = []
other_posts = []

#lets loop through the dataset
for row in hn:
    title = row[1]
    
    if title.lower().startswith("ask hn"):
        ask_posts.append(row)
    elif title.lower().startswith("show hn"):
        show_posts.append(row)
    else:
        other_posts.append(row)
        
#Check the number of posts in each list

print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))


# ## 4. Data Analysis

# ### Calculating the Average Number of Comments for Ask HN and Show HN Posts
For 'ask hn' Posts
# In[4]:


total_ask_comments = 0
for val in ask_posts:
    num_comments = val[4]
    total_ask_comments += int(num_comments)
    
avg_ask_comments = total_ask_comments / len(ask_posts)
print(avg_ask_comments)


# In[5]:


total_show_comments = 0
for val in show_posts:
    num_comments = val[4]
    total_show_comments += int(num_comments)

avg_show_comments = total_show_comments / len(show_posts)
print(avg_show_comments)


# From the analysis, 'ask posts' reveive more comments averagely than 'show posts'.

# ### Finding the Number of Ask Posts and Comments by Hour Created

# Next, we'll determine if ask posts created at a certain time are more likely to attract comments. We'll use the following steps to perform this analysis:
# 
# - Calculate the number of ask posts created in each hour of the day, along with the number of comments received.
# - Calculate the average number of comments ask posts receive by hour created.

# In[6]:


# Importing the datetime module
import datetime as dt


# In[10]:


result_list = []

for post in ask_posts:
    result_list.append(
        [post[6], int(post[4])]
    )
#For each posts in ask_posts, a new list is appended to result_list that contains two values: posts[6] (the date and time of the post) and int(posts[4]) (the number of comments the post received, converted to an integer).

# We need to create two empty dictionaries and date format
counts_by_hour = {}
comments_by_hour = {}
date_format = '%m/%d/%Y %H:%M'

for row in result_list:
    hour = row[0]
    comment = row[1]
    time = dt.datetime.strptime(hour, date_format)
    time = time.strftime('%H')
    
    if time in counts_by_hour:
        comments_by_hour[time] += comment
        counts_by_hour[time] += 1
    else:
        comments_by_hour[time] = comment
        counts_by_hour[time] = 1
        
comments_by_hour
# We created two empty dictionaries count_by_hour and comments_by_hour, and a date format assigned to the variable date_format
# We created a loop to iterate over each row in result_list
# Next we create two variables within the loop, hour and comments and assigned the two columns of result_list to each
# We used the strptime() method to convert the hour from string to datetime object and assigned it to the variable, time
# Then strtime was used to convert time back to a strning
# If the hour (time) is already in counts_by_hour, then the number of comments for that hour (comments_by_hour[time]) is incremented by the number of comments for the current post (comment), and the count for that hour (counts_by_hour[time]) is incremented by 1.
# If the hour is not already in counts_by_hour, then a new key-value pair is added to comments_by_hour and counts_by_hour, with the hour as the key.
# This code is intended to count the number of coments per hour on the Hacker News website


# Next, we'll use the two dictionaries created above to calculate the average number of comments for posts created during each hour of the day.

# In[12]:


avg_by_hour = []

for hours in comments_by_hour:
    avg_by_hour.append([hours, comments_by_hour[hours] / counts_by_hour[hours]])
    
avg_by_hour


# Although we now have the results we need, this format makes it difficult to identify the hours with the highest values. Let's finish by sorting the list of lists and printing the five highest values in a format that's easier to read.

# In[14]:


swap_avg_by_hour = []
for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
print(swap_avg_by_hour)

# Sorting the columns so that it is easy to read

sorted_swap = sorted(swap_avg_by_hour, reverse=True)
sorted_swap


# In[16]:


# Now lets get the top 5 ask comments
print("Top 5 Hours for Ask Posts Comments")
for avg, hr in sorted_swap[:5]:
    print(
        "{}: {:.2f} average comment per post".format(
            dt.datetime.strptime(hr, "%H").strftime("%H:%M"),avg
        )
    )


# From the analysis, posts made at 15:00 received the most comments with average comment of 38.59 comments made. There is a 62% increase in the average comments between the first and the second top hours.
# 
# According to the data set [documentation](https://www.kaggle.com/datasets/hacker-news/hacker-news-posts), the timezone used is Eastern Time in the US. So, we could also write 15:00 as 3:00 pm est. To convert to my timezone, it will be 16:00 as 4:00 pm WAT.
# 
# Therefore to make sure you receive a comment to your post, you should consider posting within these five hours. It is important to note that this is only associated to the Hacker News website and may not apply to other sites. Our analysis is based on data gotten directly from the Hacker News website which will not apply to the other sites. Aslo the content, topic, audience can also impact when comments are made. It is neccessary to consider other factors when creating content for any online platform.

# ## 5. Conclusion

# In this analysis, we examined the average number of comments per post for Ask HN and Show HN posts on the Hacker News website. We found that Ask HN posts received more comments on average than Show HN posts. We also analyzed the average number of comments per post for Ask HN posts by the hour of the day to determine which periods of the day receive the most comments. We found that the top 5 hours for Ask Posts comments were 15:00, 02:00, 20:00, 16:00, and 21:00 in the Eastern Standard Time (EST) time zone.

# In[ ]:




