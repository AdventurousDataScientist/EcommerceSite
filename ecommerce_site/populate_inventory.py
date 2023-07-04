import requests
from models import Item
import pandas as pd
products_json_data_df = pd.read_csv('../FAKE_STORE_PRODUCTS.csv')
for index, row in products_json_data_df.iterrows():
    name = row["name"]
    price = row["price"]
    description = row["description"]
    stock = row["stock"]
    rating = row["rating"]
    category = row["category"]
    item = Item(name=name, price=price, description=description, stock=stock, rating=rating, category=category)
    item.save()


