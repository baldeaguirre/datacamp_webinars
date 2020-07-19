import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import missingno as msno
import datetime as dt

# Read in the dataset
airbnb = pd.read_csv('https://github.com/adelnehme/python-for-spreadsheet-users-webinar/blob/master/datasets/airbnb.csv?raw=true', index_col='Unnamed: 0')
# Print the header of the DataFrame
airbnb.head()
# Print data types of DataFrame
airbnb.dtypes
# Print info of DataFrame
airbnb.info()
# Print number of missing values
airbnb.isna().sum()
# Print description of DataFrame
airbnb.describe()

# Visualize the distribution of the rating column
sns.distplot(airbnb['rating'], bins=20)
plt.title('Distribution of listing ratings')
plt.show()

# Find number of unique values in room_type column
airbnb['room_type'].unique()
# How many values of different room_types do we have?
airbnb['room_type'].value_counts()

# Data type problems
# Remove "(" and ")" from coordinates
airbnb['coordinates'] = airbnb['coordinates'].str.replace("(", "")
airbnb['coordinates'] = airbnb['coordinates'].str.replace(")", "")
# Print the header of the column
airbnb['coordinates'].head()

# Split column into two
lat_long = airbnb['coordinates'].str.split(",", expand=True)
lat_long.head()

# Assign correct columns to latitude and longitude columns in airbnb
airbnb['latitude'] = lat_long[0]
airbnb['longitude'] = lat_long[1]
# Print the header and confirm new column creation
airbnb.head()

# Convert latitude and longitude to float
airbnb['latitude'] = airbnb['latitude'].astype('float')
airbnb['longitude'] = airbnb['longitude'].astype('float')
# Print dtypes again
airbnb.dtypes

# Drop coordinates column
airbnb.drop('coordinates', axis=1, inplace=True)

# Remove $ from price before conversion to float
airbnb['price'] = airbnb['price'].str.strip("$")
# Print header to make sure change was done
airbnb['price'].head()
# Convert price to float
airbnb['price'] = airbnb['price'].astype('float')
# Calculate mean of price after conversion
airbnb['price'].mean()

# Visualize distribution of prices
sns.distplot(airbnb['price'], bins=20)
plt.show()

# Convert listing_added and last_review columns to 'datetime'
# Print header of two columns
airbnb[['listing_added', 'last_review']].head()
# Convert both columns to datetime
airbnb['listing_added'] = pd.to_datetime(airbnb['listing_added'], format='%Y-%m-%d')
airbnb['last_review'] = pd.to_datetime(airbnb['last_review'], format='%Y-%m-%d')
# Print header and datatypes of both columns again
airbnb[['listing_added', 'last_review']].head()
airbnb[['listing_added', 'last_review']].dtypes

# Text and categorical data problems
# Print unique values of `room_type`
airbnb['room_type'].unique()
# Deal with capitalized values
airbnb['room_type'] = airbnb['room_type'].str.lower()
airbnb['room_type'].unique()
# Deal with trailing spaces
airbnb['room_type'] = airbnb['room_type'].str.strip()
airbnb['room_type'].unique()

# Replace values to 'Shared room', 'Entire place', 'Private room' and 'Hotel room' (if applicable).
mappings = {'private room': 'Private Room',
            'private': 'Private Room',
            'entire home/apt': 'Entire place',
            'shared room': 'Shared room',
            'home': 'Entire place'}

# Replace values and collapse data
airbnb['room_type'] = airbnb['room_type'].replace(mappings)
airbnb['room_type'].unique()

# Divide neighbourhood_full into 2 columns and making sure they are clean
# Print header of column
airbnb['neighbourhood_full'].head()
# Split neighbourhood_full
borough_neighbourhood = airbnb['neighbourhood_full'].str.split(",", expand=True)
borough_neighbourhood.head()
# Create borough and neighbourhood columns
airbnb['borough'] = borough_neighbourhood[0]
airbnb['neighbourhood'] = borough_neighbourhood[1]
# Print header of columns
airbnb[['neighbourhood_full', 'borough', 'neighbourhood']].head()
# Drop neighbourhood_full column
airbnb.drop('neighbourhood_full', axis=1, inplace=True)
# Print out unique values of borough and neighbourhood
airbnb['borough'].unique()
airbnb['neighbourhood'].unique()
# Strip white space from neighbourhood column
airbnb['neighbourhood'] = airbnb['neighbourhood'].str.strip()
# Print unique values again
airbnb['neighbourhood'].unique()

# Make sure we set the correct maximum for rating column out of range values
# Isolate rows of rating > 5.0
airbnb[airbnb['rating'] > 5.0]
airbnb[airbnb['rating'] > 5.0]['rating']
# Drop these rows and make sure we have effected changes
airbnb.drop(airbnb[airbnb['rating'] > 5.0].index, inplace=True)
# airbnb['rating'] = airbnb[airbnb['rating'] > 5.0].replace(5)
# Visualize the rating column again
sns.distplot(airbnb['rating'], bins=20)
plt.show()
# Get the maximum
airbnb['rating'].max()

# Dealing with missing data
# Visualize the missingness
msno.matrix(airbnb)
plt.show()
# Visualize the missingness on sorted values
msno.matrix(airbnb.sort_values(by='rating'))
plt.show()
# Missingness barplot
msno.bar(airbnb)
plt.show()
# Understand DataFrame with missing values in rating, number_of_stays, 5_stars, reviews_per_month
airbnb[airbnb['rating'].isna()].describe()
# Understand DataFrame with NO missing values in rating, number_of_stays, 5_stars, reviews_per_month
airbnb[~airbnb['rating'].isna()].describe()

# Impute missing data
airbnb = airbnb.fillna({'reviews_per_month': 0,
                        'number_of_stays': 0,
                        '5_stars': 0})

# Create is_rated column
is_rated = np.where(airbnb['rating'].isna() == True, 0, 1)
airbnb['is_rated'] = is_rated

# Investigate DataFrame with missing values in price
airbnb[airbnb['price'].isna()].describe()
# Investigate DataFrame with NO missing values in price
airbnb[~airbnb['price'].isna()].describe()

# Visualize relationship between price and room_type
sns.boxplot(x='room_type', y='price', data=airbnb)
plt.ylim(0, 400)
plt.xlabel('Room Type')
plt.ylabel('Price')
plt.show()
# Get median price per room_type
airbnb.groupby('room_type').median()['price']
# Impute price based on conditions
airbnb.loc[(airbnb['price'].isna()) & (airbnb['room_type'] == 'Entire place'), 'price'] = 163.0
airbnb.loc[(airbnb['price'].isna()) & (airbnb['room_type'] == 'Private Room'), 'price'] = 70.0
airbnb.loc[(airbnb['price'].isna()) & (airbnb['room_type'] == 'Shared Room'), 'price'] = 50.0
# Confirm price has been imputed
airbnb.isna().sum()

# Doing some sanity checks on date data
today = dt.date.today()
# Are there reviews in the future?
airbnb[airbnb['last_review'].dt.date > today]
# Are there listings in the future?
airbnb[airbnb['listing_added'].dt.date > today]
# Drop these rows since they are only 4 rows
airbnb = airbnb[~(airbnb['listing_added'].dt.date > today)]
# Are there any listings with listing_added > last_review
inconsistent_dates = airbnb[airbnb['listing_added'].dt.date > airbnb['last_review'].dt.date]
# Drop these rows since they are only 2 rows
airbnb.drop(inconsistent_dates.index, inplace=True)

# Task 9: Let's deal with duplicate data
# Find duplicates
duplicates = airbnb.duplicated(subset='listing_id', keep=False)
# airbnb[duplicates]
airbnb[duplicates].sort_values('listing_id')
# Remove identical duplicates
airbnb = airbnb.drop_duplicates()
# Find non-identical duplicates
nonidentical_duplicates = airbnb.duplicated(subset='listing_id', keep=False)
# Show all non-identical duplicates
airbnb[nonidentical_duplicates].sort_values('listing_id')

# Get column names from airbnb
column_names = airbnb.columns
# Create dictionary comprehension with 'first' as value for all columns not being aggregated
aggregations = {column_name: 'first' for column_name in column_names.difference(['listing_id', 'listing_added', 'rating', 'price'])}
aggregations['price'] = 'mean'
aggregations['rating'] = 'mean'
aggregations['listing_added'] = 'max'

# Remove non-identical duplicates
airbnb = airbnb.groupby('listing_id').agg(aggregations).reset_index()
# Make sure no duplication happened
airbnb[airbnb.duplicated('listing_id', keep=False)]

# TODO: What is the average price of listings by borough? Visualize your results with a bar plot
# TODO: What is the average availability in days of listings by borough? Visualize your results with a bar plot
# TODO: What is the median price per room type in each borough? Visualize your results with a bar plot
# TODO: Visualize the number of listings over time
# Functions that should/could be used:
# .groupby() and .agg(})
# sns.barplot(x = , y = , hue = , data = )
# sns.lineplot(x = , y = , data = )
# .dt.strftime() for extracting specific dates from a datetime column