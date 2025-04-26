import json

# Load raw data
with open("./Restaurants.json", "r", encoding="utf-8") as infile:
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
        "rating": entry.get("rating", ""),
        "rating_count": entry.get("rating_count", ""),
        "cuisine": entry.get("cuisine", ""),
        "payment_methods": entry.get("payment_methods", ""),
        
        

    }
    cleaned_data.append(cleaned_entry)

# Save cleaned data
with open("./data/knowledgebase.json", "w", encoding="utf-8") as outfile:
    json.dump(cleaned_data, outfile, indent=2, ensure_ascii=False)
