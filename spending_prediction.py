# -*- coding: utf-8 -*-
"""Spending_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Us7KPOg8J8kTs5qz7sp0jIpEBTbvTW-r
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# reading the data

train = pd.read_csv('drive/My Drive/Projects/Club Mahindra/train.csv')
test = pd.read_csv('drive/My Drive/Projects/Club Mahindra/test.csv')
submission = pd.read_csv('drive/My Drive/Projects/Club Mahindra/sample_submission.csv')

# getting the shapes
print("Shape of Train :", train.shape)
print("Shape of Test :", test.shape)
print("Shape of Submission :", submission.shape)

# saving the targets and id

reservation_id = test['reservation_id']
y_train = train['amount_spent_per_room_night_scaled']

# checking the head of train data

train.head()

# deleting the target variable from the train data

train = train.drop(['amount_spent_per_room_night_scaled'], axis = 1)

# checking the shape of train
train.shape

# combining the train and test sets

data = pd.concat([train, test], axis = 0)

# getting the shape
data.shape

# describing the train data

data.describe()

# checking if there is any NULL values present in the data

print(data.isnull().sum())

# imputing missing values

data['season_holidayed_code'].fillna(data['season_holidayed_code'].mode()[0], inplace = True)
data['state_code_residence'].fillna(data['state_code_residence'].mode()[0], inplace = True)

# checking if any NULL value is left
data.isnull().sum().sum()

# deleting some of the useless columns

data = data.drop(['reservation_id', 'memberid', 'resort_id'], axis = 1)

# checking the new shape
data.shape

# checking the new columns

data.columns

# converting dates into datetime format

data['booking_date'] = pd.to_datetime(data['booking_date'], errors = 'coerce')
data['checkin_date'] = pd.to_datetime(data['checkin_date'], errors = 'coerce')
data['checkout_date'] = pd.to_datetime(data['checkout_date'], errors = 'coerce')

# extracting out years, months, days and weeks from the date

data['booking_year'] = data['booking_date'].dt.year
data['booking_month'] = data['booking_date'].dt.month

data['checkin_year'] = data['checkin_date'].dt.year
data['checkin_month'] = data['checkin_date'].dt.month

data['checkout_year'] = data['checkout_date'].dt.year
data['checkout_month'] = data['checkout_date'].dt.month

# now dropping the dates column

data = data.drop(['booking_date', 'checkin_date', 'checkout_date'], axis = 1)

# checking the new columns after feature engineering

data.columns

# analysis of channel code
# checking the count of channel code

plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['channel_code'], palette = 'inferno')
plt.title('Most Frequent Channels for Booking', fontsize = 20)

# checking dependency of channel code with target

plt.subplot(1, 2, 2)
sns.violinplot(train['channel_code'], y_train, palette = 'magma')
plt.title('Dependency of Channel with Target', fontsize = 20)

plt.show()

# analysis of main_product_code

# counting the values in main_product_code
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['main_product_code'], palette = 'plasma')
plt.title('Checking counts of Main Product', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['main_product_code'], y_train)#, palette = 'viridis')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# applying mean ecoding following the graph
# main product code 1 and 2 have huge impact, 3, 6, 7 have good impact and 4, 5 have very less impact
# replacing 4, 5 with 1
# replacing 3, 6, 7 with 2, and
# replacing 1, 2 with 3

data['main_product_code'].replace((1, 2, 3, 4, 5, 6, 7), (3, 3, 2, 1, 1, 2, 2), inplace = True)

# checking the values
data['main_product_code'].value_counts()

# analysis of no. of adults

# counting the values in no. of adults
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['numberofadults'], palette = 'BuPu')
plt.title('Checking counts of No. of Adults', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.boxenplot(train['numberofadults'], y_train, palette = 'PuRd')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as we can see that there is a pattern which says that the spending score increases for no. of adults 1 to 10, but it is very confusing for 10-30 and vey high for 32
# so we can make 3 groups no. of adults 1-10, 11-20, 21+

def groups(numberofadults):
  if numberofadults <= 10:
    return 1
  if numberofadults <= 20 and numberofadults > 10:
    return 2
  else:
    return 3


data['numberofadults'] = data.apply(lambda x: groups(x['numberofadults']), axis = 1)
data['numberofadults'].value_counts()

# analysis of numberofchildren

# counting the values in no. of children
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['numberofchildren'], palette = 'OrRd')
plt.title('Checking counts of No. of Children', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.stripplot(train['numberofchildren'], y_train, palette = 'RdPu')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as we can see that there is a pattern which says that the spending score increases for no. of children 1 to 10, but it is very confusing for 10-30 and vey high for 32
# so we can make 3 groups no. of adults 1-10, 11-20, 21+

def groups(numberofchildren):
  if numberofchildren <= 4:
    return 1
  if numberofchildren <= 8 and numberofchildren > 4:
    return 2
  else:
    return 3


data['numberofchildren'] = data.apply(lambda x: groups(x['numberofchildren']), axis = 1)
data['numberofchildren'].value_counts()

# analysis of persontravellingid
# it states the different types of persons travelling

# counting the values in persontravellingid
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['persontravellingid'], palette = 'hot')
plt.title('Checking counts of Different Persons Travelling', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.boxplot(train['persontravellingid'], y_train, palette = 'copper')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as from the above graph it is clearly visible that all the six type of person travelling have equal weightage we must one-hot encode them

columns = ["persontravellingid"]
data = pd.get_dummies(data, columns = columns)

# analysis of resort region code

# counting the values in resort region code
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['resort_region_code'], palette = 'YlGnBu')
plt.title('Checking counts of Different Regions of Resort', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['resort_region_code'], y_train, color = 'green')#, palette = 'cool')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as from the above graph it is clearly visible that region 1 has huge impact, region 2 has good impact and region 3 has low impact onn amount spent 
# so let's do target encoding

data["resort_region_code"].replace((1, 2, 3), (3, 2, 1), inplace = True)

# checking the values 
data['resort_region_code'].value_counts()

# analysis of resort type code

# counting the values in resort region code
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['resort_type_code'], palette = 'spring')
plt.title('Checking counts of Different Types of Resort', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['resort_type_code'], y_train, color = 'purple')#, palette = 'autumn')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as from the above graph it is clearly visible that all the seven types of resort different weightage
# so let's do target encoding resort type 1, 5 have huge impact, resort no. 4, 2, 5 have good impact and resort type 7 and 3 have poor impact
# encoding 5 and 1 as 3
# encoding 4, 2, 6 as 2
# encoding 7 and 3 as 1

data["resort_type_code"].replace((0, 1, 2, 3, 4, 5, 6, 7), (2, 3, 2, 1, 2, 3, 2, 1), inplace = True)

# checking the values
data['resort_type_code'].value_counts()

# analysis of room type booked

# counting the values in resort room type
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['room_type_booked_code'], palette = 'ocean')
plt.title('Checking counts of Different Rooms Booked', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.boxenplot(train['room_type_booked_code'], y_train, palette = 'Wistia')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as from the above graph it is clearly visible that all the six types of rooms have equal weightage we must one-hot encode them

columns = ["room_type_booked_code"]
data = pd.get_dummies(data, columns = columns)

# analysis of room nights
# it means the no. of room nights booked

# there is a value of -45 so, we are converting it to 45
train['roomnights'].replace(-45, 45, inplace = True)

# counting the values in resort room nights
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['roomnights'], palette = 'hsv')
plt.title('No. of Nights a room was booked', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.boxplot(train['roomnights'], y_train, palette = 'autumn')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as we can see that there is a pattern which says that the spending score increases for no. of rooms 1 to 5, but it is very confusing for 10-30 and vey high for 32
# so we can make 3 groups no. of adults 1-10, 11-20, 21+

def groups(roomnights):
  if roomnights <= 5:
    return 1
  if roomnights <= 20 and roomnights > 5:
    return 2
  if roomnights <= 30 and roomnights > 20:
    return 3
  if roomnights <= 40 and roomnights > 30:
    return 4
  else:
    return 5


data['roomnights'] = data.apply(lambda x: groups(x['roomnights']), axis = 1)
data['roomnights'].value_counts()

# analysis of season holidayed code
# it means in which season the people have holidayed

# counting the values in season holidayed code
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['season_holidayed_code'], palette = 'Greys')
plt.title('In which People Prefer to Holiday', fontsize = 20)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['season_holidayed_code'], y_train, color = 'gray')#, palette = 'seismic')
plt.title('Checking Dependency with the Target', fontsize = 20)

plt.show()

# as from the above graph it is clearly visible that all the four  types of seasons have different impact on the amount spent
# let's target encode them 
# as season holiday code 1 has huge impact , encode it as 4
# as season holiday code 2 has huge impact , encode it as 3
# as season holiday code 3 has huge impact , encode it as 2
# as season holiday code 4 has huge impact , encode it as 1


data["season_holidayed_code"].replace((1, 2, 3, 4), (4, 3, 2, 1), inplace = True)

# checking the values
data['season_holidayed_code'].value_counts()

# analysis of state code residence
# it states the residence code of the members.

# counting the values in state code residence
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['state_code_residence'], palette = 'PiYG')
plt.title('State code of People Holidaying', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.stripplot(train['state_code_residence'], y_train, palette = 'terrain')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

data.columns

# imputing the missing values in state code res.

train['state_code_residence'].fillna(train['state_code_residence'].mode()[0], inplace = True)

# checking the null values
train['state_code_residence'].isnull().any()

# creating a dataset

y = train['state_code_residence']
x = pd.concat([y_train, y], axis = 1).values

# checking the shape
x.shape

from sklearn.cluster import KMeans

wcss = []
for i in range(1, 11):
  kmeans = KMeans(n_clusters = i, n_init = 10, init = 'k-means++', random_state = 0, max_iter = 300)
  kmeans.fit(x)
  wcss.append(kmeans.inertia_)
  
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('No. of Clusters')
plt.ylabel('wcss')
plt.show()

# making the clusters

km = KMeans(n_clusters = 3, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
y_means = km.fit_predict(x)

plt.scatter(x[y_means == 0, 0], x[y_means == 0, 1], s = 100, c = 'pink', label = 'general')
plt.scatter(x[y_means == 1, 0], x[y_means == 1, 1], s = 100, c = 'yellow', label = 'miser')
plt.scatter(x[y_means == 2, 0], x[y_means == 2, 1], s = 100, c = 'cyan', label = 'target')

plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:, 1], s = 50, c = 'blue' , label = 'centeroid')

plt.title('K Means Clustering', fontsize = 20)
plt.xlabel('Amount Spent on Resort')
plt.ylabel('State code Residence')
plt.legend()
plt.show()

# let's target encode state code residence according to the above clusters

def groups(state_code_residence):
  if state_code_residence <= 5:
    return 1
  if state_code_residence <= 15 and state_code_residence > 5:
    return 2
  else:
    return 3
  
data['state_code_residence'] = data.apply(lambda x: groups(x['state_code_residence']), axis = 1)

# checking the values
data['state_code_residence'].value_counts()

# analysis of state code resort
# it states the residence code of the members.

# counting the values in state code resort
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['state_code_resort'], palette = 'Pastel1')
plt.title('State code for resort', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['state_code_resort'], y_train)#, palette = 'Pastel2')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# as from the above graph it is clearly visible that all the thirteen types of states of resorts have different weightage
# so we must target encode them according to the above graph
# 

columns = ["state_code_resort"]
data = pd.get_dummies(data, columns = columns)

# analysis of total pax
# it states the total no. of persons travelling

# counting the values in no. of persons travelling
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['total_pax'], palette = 'rainbow')
plt.title('Total no. of Passengers', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['total_pax'], y_train, color = 'darkblue')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# as we can see that there is a pattern which says that the spending score increases for total no. of passengers, it increases upto 20 and then decreases.
# so we can make 3 groups no. of adults 1-10, 11-20, 21+

def groups(total_pax):
  if total_pax <= 5:
    return 1
  if total_pax <= 10 and total_pax > 5:
    return 2
  if total_pax <= 15 and total_pax > 10:
    return 3
  if total_pax <= 20 and total_pax > 15:
    return 4
  else:
    return 3


data['total_pax'] = data.apply(lambda x: groups(x['total_pax']), axis = 1)
data['total_pax'].value_counts()

# analysis of member age buckets
# it states the age bucket of the members

# counting the values of age buckets of people travelling
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['member_age_buckets'], palette = 'rainbow')
plt.title('Total no. of Passengers', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['member_age_buckets'], y_train, color = 'pink')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# label encoding of the member age buckets
# lets label A, B, G, H as 1 I, J as 2 and C, D, E, F as 3

data['member_age_buckets'].replace(('A', 'B', 'G', 'H'), (1, 1, 1, 1), inplace = True)
data['member_age_buckets'].replace(('I', 'J'), (2, 2), inplace = True)
data['member_age_buckets'].replace(('C', 'D', 'E', 'F'), (3, 3, 3, 3), inplace = True)

data['member_age_buckets'].value_counts()

# analysis of booking type code

# counting the values of types of bookings of people travelling
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['booking_type_code'], palette = 'rainbow')
plt.title('Types of Bookings', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.stripplot(train['booking_type_code'], y_train, palette = 'Set2')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# analysis of cluster code

# counting the values of types of bookings of people travelling
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['cluster_code'], palette = 'PiYG')
plt.title('Types of clusters of Resorts', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['cluster_code'], y_train)#, palette = 'PRGn')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# target encoding for cluster code

data['cluster_code'].replace(('A', 'B', 'C', 'D', 'E', 'F'),(1, 2, 6, 3, 5, 4), inplace = True)

data['cluster_code'].value_counts()

# analysis of res. status

# counting the values of types of reservation status
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['reservationstatusid_code'], palette = 'RdGy')
plt.title('Types of clusters of Resorts', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['reservationstatusid_code'], y_train, color = 'red')#, palette = 'PRGn')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# target encoding for reservation code

data['reservationstatusid_code'].replace(('A', 'B', 'C', 'D'), (3, 4, 2, 1), inplace = True)

data['reservationstatusid_code'].value_counts()

# analysis of booking year

# counting the values of types of reservation status
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['booking_year'], palette = 'RdYlBu')
plt.title('Value counts of Year wise Bookings', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['booking_year'], y_train, color = 'red')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# target encoding for the booking year

data['booking_year'].replace((2014, 2015, 2016, 2017, 2018, 2019), (1, 2, 3, 4, 5, 6), inplace = True)

data['booking_year'].value_counts()

# analysis of booking month

# counting the values of monthly wise
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['booking_month'], palette = 'spring')
plt.title('Value counts Month wise', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['booking_month'], y_train, color = 'pink')#, palette = 'PRGn')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# target encoding for booking month
# i have made some groups according to the graph
# most busy month -march, april, then september and may, then december, october, august, june, july, and at last february, november and January

data['booking_month'].replace((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), (1, 1, 4, 4, 3, 2, 2, 2, 3, 2, 1, 2), inplace = True)

data['booking_month'].value_counts()

# splitting the data into train and test

x_train = data.iloc[:341424,:]
x_test = data.iloc[341424:,:]

# getting the shapes
print("Shape of train :", x_train.shape)
print("Shape of test :", x_test.shape)

# analysis of booking day

# counting the values of monthly wise
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['booking_day'], palette = 'rainbow')
plt.title('Value counts Day wise', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['booking_day'], y_train, color = 'yellow')#, palette = 'PRGn')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# let's apply log transformations onto booking week

data['booking_week'] = np.log1p(data['booking_week'])

# analysis of booking month

# counting the values of monthly wise
plt.rcParams['figure.figsize'] = (18, 8)
plt.subplot(1, 2, 1)
sns.countplot(data['booking_week'], palette = 'cool')
plt.title('Value counts Week wise', fontsize = 20)
plt.xticks(rotation = 90)

# checking dependency with the target variable
plt.subplot(1, 2, 2)
sns.lineplot(train['booking_week'], y_train, color = 'orange')#, palette = 'PRGn')
plt.title('Checking Dependency with the Target', fontsize = 20)
plt.xticks(rotation = 90)

plt.show()

# let's apply log transformations onto booking week

data['booking_week'] = np.log1p(data['booking_week'])

# splitting into train and valid sets

from sklearn.model_selection import train_test_split

x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size = 0.25, random_state = 0)

# getting the shapes
print("Shape of x_train :", x_train.shape)
print("Shape of x_valid :", x_valid.shape)
print("Shape of y_train :", y_train.shape)
print("Shape of y_valid :", y_valid.shape)

train.head()

data.columns

