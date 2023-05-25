#!/usr/bin/env python
# coding: utf-8

# # Exploring eBay Car Sales Data

# ## Table of content

# - Introduction
# - 1.0 Data Exploration
# - 2.0 Data Cleaning
# - 2.1 Cleaning column names
# - 2.2 Cleaning rows wth Numerique Values (price and odometer_km)
# - 2.3 Cleaning date columns
# - 2.4 Dealing with Incorrect Registration Year Data
# - 3.0 Exploring Price by Brand
# - 4.0 Storing Aggregate Data in a DataFrame

# # Introduction

# In this project, we wil be working with a dataset of used cars for 'ebay kleinanzeigen', a classified section of the German ebay website. The original dataset for this project can be found [here](https://app.dataquest.io/c/54/m/293/data-cleaning-basics/12/challenge-clean-a-string-column).
# 
# The aim of this project is to clean the data and analyze the included used car listings so as to make informed decision. 

# ## 1.0 Data Exploration

# In[1]:


# Importing libraries which we will use to explore and clean our data
import pandas as pd
import numpy as np


# In[2]:


# Reading our file into pandas to crate a dataframe
autos = pd.read_csv('autos.csv', encoding='Latin-1')


# In[3]:


autos


# In[4]:


print(autos.info())
print(autos.head())
      


# The dataset has 20 colums and 50,000 rowa. Some important attritubes which will help our analysis have wrong data types. Forexample, price odometer columns are strings instead of int or a float. Also the date columns need to be formatted dates from object. We can also notice that there are missing values in the some columns: vehicletype, gearbox, model, fueltype and notRepaireddamage. In addition, the column names are mixed with box upper and lower case letters. Lastly, some words are writeen in foregin languages which will need to be translated to English.

# ## 2 Data Cleaning
# 
# In this section,  we are going to clean and prepare our data for analysis. We will be addressing the column names, null values, data types and more.

# ### 2.1 Cleaning column names
# 
# The colums names are carmel case. We need to convert them to snakecase and also rename some of the columns for better ifentifactio

# In[5]:


def clean_col(col):
    col = col.replace('yearOfRegistration', 'registration_year')
    col = col.replace('monthOfRegistration', 'registration_month')
    col = col.replace('notRepairedDamage', 'unrepaired_damage')
    col = col.replace('dateCreated', 'ad_created')
    col = col.replace('vehicleType', 'type_of_vehicle')
    col = col.replace('offerType', 'type_of_offer')
    col = col.replace('powerPS', 'power_per_second')
    col = col.replace('dateCrawled', 'date_crawled')
    col = col.replace('nrOfPictures', 'number_of_pictures')
    col = col.replace('postalCode', 'postal_code')
    col = col.replace('lastSeen', 'last_seen')
    return col
new_columns = []
for c in autos.columns:
    clean_c = clean_col(c)
    new_columns.append(clean_c)

autos.columns = new_columns


# In[6]:


print(autos.head())


# We defined a 'clean_col' function that
# - Uses the str.replace() function to rename the columns we want
# - Returns the modified srting.
# 
# Used a loop to apply the function to each item in the index object and assign it back to the DataFrame.columns attribute.
# 
# Lastly we verified the new state of the autos dataframe by printing the first five rows.

# ### 2.2 Cleaning rows wth Numerique Values (price and odometer_km)
# 
# We need to make sure we remove any odd values and deal with null values that will can hinder us from doing our analysis

# In[7]:


autos.describe(include='all')  # Looking at the descriptive statistics of the dataframe

Looking at the statistics above, we determiined that: 
1. The following columns will not help in our analysis and so nee to be removed: dateCrawled, nrOfPictures, postalCode, and lastSeen.
2. Some columns have missing values and will need further investigation. These are type_of_vehicle, gearbox, model,  fuel_type, and unrepaired_damage.
3. Some numeric columns have but string formats. These are price and odometer columns. These will need to be formated.
# In[8]:


# We will use the str.replace() function to remove '$', and 'km' from both the price and odometer olumns
# We will also convert the data type of both columns using the 'astype' function

autos['price'] = autos['price'].str.replace('$', '').str.replace(',', '').astype(int)
autos['odometer'] = autos['odometer'].str.replace('km', '').str.replace(',', '').astype(int)


# In[9]:


# Renaming the odometer column to be more descriptive
autos.rename({'odometer': 'odometer_km'}, axis=1, inplace=True)


# In[10]:


autos['price'].unique().shape
# This is determine the number of unique values in the price column


# In[11]:


autos['price'].describe() 
# This is get the descriptive statistics of the price column


# In[12]:


autos['price'].value_counts().head()


# In[13]:


# We want to investigate the firdt 20 unique values of the price column in ascending order
autos['price'].value_counts().sort_index(ascending=False).head(20)


# We can notice that the first 2 values are significantly higher than the rest of the values and that will defiitely skew our analyis to the right. A closer look shows that the from $350,000, there is a significant jump to the next value. We think the values above this amount should be removed.

# In[14]:


#Now lets look at the last 10 values of the price column.
autos['price'].value_counts().sort_index(ascending=False).tail(250)


# Looking at the bottom of the price column, we realise that there are many rows with price below $1,000. 1,421 rows have price of $0,00. These values  do not reflect the value of a car and therefore will significantly impact our analysis. As such , we shall eliminate any row with price which is below $1000.

# In[15]:


# Removing the outliers. That is values outside $1000 and $350000
autos = autos[autos['price'].between(1000, 350000)]


# We will follow the same process in exploring and cleaning the odometer column

# In[16]:


autos['odometer_km'].unique().shape


# In[17]:


autos['odometer_km'].describe()


# Looking at this statistics, we can determine that there are no extreme values as ve have 13 unique values between 5,000 and 150,000. 

# ### 2.3 Cleaning date columns
# 
# We will now move on to the date columns and understand the date range the data covers.
# 
# There are 5 columns that should represent date values. Some of these columns were created by the crawler, some came from the website itself. We can differentiate by referring to the data dictionary:
# 
# - `date_crawled`: added by the crawler
# - `last_seen`: added by the crawler
# - `ad_created`: from the website
# - `registration_month`: from the website
# - `registration_year`: from the website
# 
# Right now, the date_crawled, last_seen, and ad_created columns are all identified as string values by pandas. Because these three columns are represented as strings, we need to convert the data into a numerical representation so we can understand it quantitatively. The other two columns are represented as numeric values

# In[18]:


# Lets explore the date columns and see what they look like
autos[['date_crawled','ad_created','last_seen']][0:5]


# We notice that the first 10 characters represent the day (e.g. 2016-03-12). To understand the date range, we can extract just the date values, use Series.value_counts() to generate a distribution, and then sort by the index.

# In[19]:


# Selecting the first 10 characters of each row while including missing values, and use percentage.
date_crawled_days = (autos['date_crawled'].
                     str[:10].
                     value_counts(normalize=True, dropna=False).
                     sort_index()
                    )


# In[20]:


ad_created_days = (autos['ad_created'].str[:10].
                     value_counts(normalize=True, dropna=False).
                     sort_index()
                  )


# In[21]:


last_seen_days = (autos['last_seen'].str[:10].
                     value_counts(normalize=True, dropna=False).
                     sort_index()
                 )


# In[22]:


date_crawled_days


# In[23]:


ad_created_days


# In[24]:


last_seen_days


# The date_crawled, ad_created and last_seen columns have an even distrobution from March to April.

# ### 2.4 Dealing with Incorrect Registration Year Data
# 
# Now we want to understand the distrobution of the registration_year, and regidttstion_month columns

# In[25]:


autos[['registration_year', 'registration_month']].describe()


# We can notice that the min and max registration years have odd values, 1000 and 9999 respectively. This years cannot be correct so we have to eliminate them.
# 
# Aslo, the min registration month is 0. This too has to be eliminated. 

# In[26]:


# To detemine how many rows have 0 month
print(autos['registration_month'].value_counts().sort_index())


# 2424 rows have 0 months. 
# 
# We will also look at the registration_year column to see how many rows have the odd values. We will look at bothe the top values and the last values.

# In[27]:


print(autos['registration_year'].
     value_counts(dropna=False).
      sort_index(ascending=False).
      head(10)
     )
# To get the top ten years


# In[28]:


print(autos['registration_year'].
     value_counts(dropna=False).
      sort_index(ascending=False).
      tail(15)
     )
#Last 15 years


# Given that the first car was created in 1886, we will eliminate all values between 1886 and 2019. We will also eliminate the odd months.

# In[29]:


autos = autos[autos['registration_year'].between(1886, 2019)]
autos = autos[autos['registration_month'].between(1, 12)]


# Now lets see the years with the highest percent of cars registered, and also the months.

# In[30]:


print(autos['registration_year'].value_counts(normalize=True).head(10))


# In[31]:


print(autos['registration_month'].value_counts(normalize=True))


# ## 3.0 Exploring Price by Brand
# 
# When working with data on cars, it's natural to explore variations across different car brands. We can use aggregation to understand the brand column. Now we will analyze the price of cars by brand.

# In[32]:


# Get the number of cars for each brand
print(autos['brand'].value_counts(dropna=False))


# Now we want select brands whose aggregate is 5% of the total value.

# In[33]:


brand_pct = autos['brand'].value_counts(normalize=True)
print(brand_pct)


# In[34]:


# printing out those whose % is above or equal to 0.05
brand_pct = brand_pct[brand_pct >= 0.05]
print(brand_pct)


# We htave six brands whose aggregate value is 5% or more of the total. Now we will use calculate the average price of these brands.

# In[35]:


# Creating an empty dicitonary to for a frequency table to get the mean for each brand
brand_price = {}
top_brands = brand_pct

for b in top_brands.index:
    price = autos.loc[autos['brand']==b, 'price']
    avg_price = round(price.mean(), 2)
    brand_price[b] = avg_price
    
print(sorted(brand_price.items(), key=lambda x:x[1]))


# Audi proves to be the most expensive car closely followed by mercedes and bmw. Opel is the cheapest car from the top cars with 5% aggregate. 

# ## 4.0 Storing Aggregate Data in a DataFrame

# For the top 6 brands, let's use aggregation to understand the average mileage for those cars and if there's any visible link with mean price. We will combine the data from both series objects into a single dataframe (with a shared index) and display the dataframe directly.

# In[36]:


# Creating a frequency table to get the avegrage mileage of the top 6 cars
brand_mileage = {}

for b in top_brands.index:
    mileage = autos.loc[autos['brand']==b, 'odometer_km']
    avg_mileage = round(mileage.mean(), 2)
    brand_mileage[b] = avg_mileage
    
print(sorted(brand_mileage.items(), key=lambda x:x[1]))


# In[37]:


# Converting the two dictionaries into a series
price_series = pd.Series(brand_price)
mileage_series = pd.Series(brand_mileage)

print(price_series.sort_values(ascending=False))
print('\n')
print(mileage_series.sort_values(ascending=False))


# In[38]:


# create a dataframe with the mean_price series
top_6_price_mileage = pd.DataFrame(price_series, columns=["mean_price"])
# add mean_mileage series to the dataframe we just created
top_6_price_mileage["mean_mileage"] = mileage_series
top_6_price_mileage


# From the dataframe, we can see that the average mileage for these cars are not too different. However there is a significant difference between the cars with the highest mean milleage, BMW and the least, ford.
# 
# Opel being the least expensive car has a better mean mileage than for, and audi which has the most average price has the third best average mileage, witht the first two being bmw and mercedes benz. 
# 
# The volkswagen is the car between in terms of both price and mileage. 
