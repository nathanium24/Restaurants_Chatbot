from pymongo import MongoClient
import os
from models import MenuItem, Restaurant  # Assuming models are defined in models.py

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGO_URI"))
db = client["zomato_db"]

def upload_menu_item(menu_item_data):
    """
    Uploads a menu item to the MongoDB collection.
    :param menu_item_data: Dictionary containing menu item data matching the MenuItem model.
    """
    try:
        # Validate data against MenuItem model
        menu_item = MenuItem(**menu_item_data)
        db.menu_items.insert_one(menu_item.dict())
        print("Menu item uploaded successfully.")
    except Exception as e:
        print(f"Error uploading menu item: {e}")

def upload_restaurant(restaurant_data):
    """
    Uploads a restaurant to the MongoDB collection.
    :param restaurant_data: Dictionary containing restaurant data matching the Restaurant model.
    """
    try:
        # Validate data against Restaurant model
        restaurant = Restaurant(**restaurant_data)
        db.restaurants.insert_one(restaurant.dict())
        print("Restaurant uploaded successfully.")
    except Exception as e:
        print(f"Error uploading restaurant: {e}")


