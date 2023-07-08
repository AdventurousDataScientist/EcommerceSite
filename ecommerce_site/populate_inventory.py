import requests
from main.models import Item, Store
from django.contrib.auth.models import User

import pandas as pd
products_json_data_df = pd.read_csv('FAKE_STORE_PRODUCTS.csv')
for index, row in products_json_data_df.iterrows():
    name = row["name"]
    image = row["image"]
    price = row["price"]
    description = row["description"]
    stock = row["stock"]
    rating = row["rating"]
    category = row["category"]
    main_user = User.objects.get(username='nikhil') # should change this to test_user_1
    store = main_user.store_set.first()
    item = Item(store=store, name=name, image=image, price=price, description=description, stock=stock, rating=rating, category=category)
    item.save()


