import pandas as pd

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

# filtering outliers 
filtered_prices = prices.query("price != 0 & price != 7500")
# print(filtered_prices.describe())

# calculating average
avg_price = round(filtered_prices["price"].mean(),2)

# # Comparing costs to the private rental market

# adding price per month column to prices
prices["price_per_month"] = round(prices["price"]*365/12,0).astype(int)

# calculating the average price of the price_per_month
average_price_per_month = round(prices["price_per_month"].mean(),2)

# calculating difference between the avg cost of Airbnb listing versus the private market
# according to Zumper, a 1 bedroom apartment in New York City costs, on average, $3,100 per month
difference = round(average_price_per_month - 3100,2)

# # Cleaning the room_type column

# changing all values in the room_type column to lowercase
rooms["room_type"] = rooms["room_type"].str.lower()

# converting the room_type column to a str dtype
rooms["room_type"] = rooms["room_type"].astype('string')

# storing the count of values for room_type as room_frequencies
room_frequencies = rooms["room_type"].value_counts().to_string()

# # What timeframe are we working with?

# changing the dtype of the last_review to datetime
reviews["last_review"] = pd.to_datetime(reviews["last_review"]).dt.date

# finding first and last reviews
first_reviewed = reviews["last_review"].min()
last_reviewed = reviews["last_review"].max()

# # Joining the DataFrames

# outer merging dataframes
rooms_and_prices = pd.merge(prices, rooms, on="listing_id")

airbnb_merged = pd.merge(rooms_and_prices, reviews, on = "listing_id")
# print(airbnb_merged.columns)
# print(airbnb_merged[airbnb_merged.isnull().any(axis=1)])

# removing missing observations
airbnb_merged.dropna(inplace=True)

# checking for duplicate values in airbnb_merged
# print(airbnb_merged.duplicated().sum())

# Analyzing listing prices by NYC borough