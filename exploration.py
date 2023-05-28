import pandas as pd
import numpy as np

# # Reading from files(csv, xlsx, tsv)
price_file = "raw_data/airbnb_price.csv"
prices = pd.read_csv(price_file)

xls = pd.ExcelFile("raw_data/airbnb_room_type.xlsx")
rooms = pd.read_excel(xls)

reviews = pd.read_csv("raw_data/airbnb_last_review.tsv", sep= '\t')

# # Cleaning price column

# Removing extra string
prices["price"] = prices["price"].str.replace(" dollars", "")

# converting object to numeric
prices["price"]= pd.to_numeric(prices["price"])

# # Calculating average price

# checking outliers in price
# print(prices.sort_values(by = 'price'))

# filtering outliers (free listings)
prices = prices.query("price != 0")
# print(prices.describe())

# calculating average
avg_price = round(prices["price"].mean(),2)

# # Comparing costs to the private rental market

# adding price per month column to prices
prices["price_per_month"] = prices["price"]*365/12

# calculating the average price of the price_per_month
average_price_per_month = round(prices["price_per_month"].mean(),2)

# calculating difference between the avg cost of Airbnb listing versus the private market
# according to Zumper, a 1 bedroom apartment in New York City costs, on average, $3,100 per month
difference = round((average_price_per_month - 3100),2)

# # Cleaning the room_type column

# changing all values in the room_type column to lowercase
rooms["room_type"] = rooms["room_type"].str.lower()

# converting the room_type column to a str dtype
rooms["room_type"] = rooms["room_type"].astype('string')

# storing the count of values for room_type as room_frequencies
room_frequencies = rooms["room_type"].value_counts()

# # What timeframe are we working with?

# changing the dtype of the last_review to datetime
reviews["last_review"] = pd.to_datetime(reviews["last_review"]).dt.date

# finding first and last reviews
first_reviewed = reviews["last_review"].min()
last_reviewed = reviews["last_review"].max()

# # Joining the DataFrames

# outer merging dataframes
rooms_and_prices = pd.merge(prices, rooms, how = 'outer', on="listing_id")

airbnb_merged = pd.merge(rooms_and_prices, reviews, how = 'outer', on = "listing_id")
# print(airbnb_merged.columns)
# print(airbnb_merged[airbnb_merged.isnull().any(axis=1)])

# removing missing observations
airbnb_merged.dropna(inplace=True)

# checking for duplicate values in airbnb_merged
# print(airbnb_merged.duplicated().sum())

# # Analyzing listing prices by NYC borough

# creating a new column in airbnb_merged called borough
airbnb_merged["borough"] = airbnb_merged["nbhood_full"].str.partition(",")[0]

# grouping airbnb_merged by borough and calculating summary statistics
boroughs = airbnb_merged.groupby("borough")["price"].agg(["sum", "mean", "median", "count"])

# updating the boroughs DataFrame
boroughs = boroughs.round(2).sort_values(by = "mean", ascending= False)
# print(boroughs)

# # Price range by borough

# creating labels list
label_names = ["Budget", "Average", "Expensive", "Extravagant"]

# creating ranges list
ranges = [0, 69, 175, 350, np.inf]

# creating price range column
airbnb_merged["price_range"] = pd.cut(airbnb_merged["price"], bins = ranges, labels = label_names)

# calculating count of price ranges
prices_by_borough = airbnb_merged.groupby(by = ["borough", "price_range"])["price_range"].count()
# Storing the final result

airbnb_analysis = {'avg_price': avg_price,
                   'average_price_per_month': average_price_per_month,
                   'difference': difference,
                   'room_frequencies': room_frequencies,
                   'first_reviewed': first_reviewed,
                   'last_reviewed': last_reviewed,
                   'prices_by_borough': prices_by_borough}
print(airbnb_analysis)