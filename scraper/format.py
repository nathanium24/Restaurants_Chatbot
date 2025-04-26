
# import json

# # Function to determine dietary options based on the menu items
# def determine_dietary_options(menu):
#     non_veg_keywords = ["chicken", "mutton", "prawn", "fish", "egg", "beef", "lamb"]
    
#     has_non_veg = False
#     has_veg = False

#     # Check each menu item for non-veg or veg keywords
#     for item in menu:
#         name = item[0].lower()  # Menu item name in lowercase
#         if any(kw in name for kw in non_veg_keywords):
#             has_non_veg = True
#         else:
#             has_veg = True

#     # Determine the dietary options based on what is found
#     if has_non_veg and has_veg:
#         return ["Non-Veg", "Veg"]
#     elif has_non_veg:
#         return ["Non-Veg"]
#     elif has_veg:
#         return ["Pure Veg"]
#     else:
#         return []  # If no veg or non-veg dishes are found, return an empty list

# # Function to extract menu items from the raw data
# def extract_menu_items(entry):
#     menu_items = []

#     # Get the 'menu' key from the entry and extract items as name and price pairs
#     menu = entry.get("menu", [])

#     for item in menu:
#         if len(item) == 2:
#             name = item[0]
#             price = item[1]

#             # Ensure rupees symbol is correctly formatted
#             price = price.replace("\\u20b9", "₹").replace("\u20b9", "₹")
            
#             menu_items.append({
#                 "item": name.strip(),
#                 "price": price.strip()
#             })

#     return menu_items

# # Load raw data
# with open("Restaurants.json", "r") as infile:
#     raw_data = json.load(infile)

# cleaned_data = []

# for entry in raw_data:
#     address_data = entry.get("address", {})
#     full_address = ", ".join(filter(None, [
#         address_data.get("street", ""),
#         address_data.get("locality", ""),
#         address_data.get("region", ""),
#         address_data.get("postal_code", ""),
#         address_data.get("country", "")
#     ]))

#     menu_items = extract_menu_items(entry)  # Extract formatted menu items
#     dietary_options = determine_dietary_options(entry.get("menu", []))  # Determine dietary options based on menu

#     cleaned_entry = {
#         "name": entry.get("name", ""),
#         "menu_items": menu_items,  # Get formatted menu items
#         "dietary_options": dietary_options,  # Add dietary options
#         "price_range": entry.get("price_range", "").replace("\u20b9", "₹").replace("\\u20b9", "₹"),
#         "address": full_address,
#         "opening_hours": entry.get("opening_hours", ""),
#         "image_url": entry.get("image_url", ""),
#         "phone_number": entry.get("telephone", "")
#     }
#     cleaned_data.append(cleaned_entry)

# # Save cleaned data to knowledgebase.json
# with open("knowledgebase.json", "w", encoding="utf-8") as outfile:
#     json.dump(cleaned_data, outfile, indent=2, ensure_ascii=False)


import json

# Load raw data
with open("Restaurants.json", "r", encoding="utf-8") as infile:
    raw_data = json.load(infile)

cleaned_data = []

for entry in raw_data:
    address_data = entry.get("address", {})
    full_address = ", ".join(filter(None, [
        address_data.get("street", ""),
        address_data.get("locality", ""),
        address_data.get("region", ""),
        address_data.get("postal_code", ""),
        address_data.get("country", "")
    ]))

    menu = entry.get("menu", [])
    formatted_menu = []

    for item in menu:
        if isinstance(item, dict):
            # If item already has full information, use it directly
            formatted_menu.append(item)
        elif isinstance(item, list) and len(item) == 2:
            name, price = item
            # Remove currency symbol if present
            clean_price = price.replace("\\u20b9", "").replace("\u20b9", "").replace("₹", "").strip()

            try:
                price_value = float(clean_price)
            except ValueError:
                price_value = 0.0

            formatted_menu.append({
                "name": name,
                "description": "",
                "price": price_value,
                "attributes": {}
            })

    # Determine dietary options from the menu
    dietary_options = []
    for menu_item in formatted_menu:
        veg_nonveg = menu_item.get("attributes", {}).get("veg_nonveg")
        if veg_nonveg and veg_nonveg not in dietary_options:
            dietary_options.append(veg_nonveg)

    cleaned_entry = {
        "name": entry.get("name", ""),
        "menu_items": formatted_menu,
        "dietary_options": dietary_options,
        "price_range": entry.get("price_range", "").replace("\u20b9", "₹").replace("\\u20b9", "₹"),
        "address": full_address,
        "opening_hours": entry.get("opening_hours", ""),
        "image_url": entry.get("image_url", ""),
        "phone_number": entry.get("telephone", "")
    }
    cleaned_data.append(cleaned_entry)

# Save cleaned data
with open("knowledgebase.json", "w", encoding="utf-8") as outfile:
    json.dump(cleaned_data, outfile, indent=2, ensure_ascii=False)
