import pandas as pd

# # Reading from files(csv, xlsx, tsv)
price_file = "raw_data/airbnb_price.csv"
prices = pd.read_csv(price_file)
# print(prices.head())

xls = pd.ExcelFile("raw_data/airbnb_room_type.xlsx")
rooms = pd.read_excel(xls)
# print(rooms.head())

last_review = pd.read_csv("raw_data/airbnb_last_review.tsv", sep= '\t')
# print(last_review.head())

# # Cleaning price column
# Removing extra string
prices["price"] = prices["price"].str.replace(" dollars", "")
# print(prices.head())

# converting object to numeric
# print(prices["price"].dtype)
prices["price"]= pd.to_numeric(prices["price"])
# print(prices["price"].dtype)

# # Calculating average price
# checking outliers in price
#print(prices.sort_values(by = 'price'))

# filtering outliers 
filtered_prices = prices.query("price != 0 & price != 7500")
# print(filtered_prices.describe())

# calculating average
avg_price = round(filtered_prices["price"].mean(),2)
# print(avg_price)
