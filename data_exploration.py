import pandas as pd

price_file= "raw_data/airbnb_price.csv"
prices=pd.read_csv(price_file)
print(prices.head())
