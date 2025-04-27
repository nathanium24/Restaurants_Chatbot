from scrapers.info_scraper import get_restaurant_info


def scrape_all_data(url_list):
    """Scrapes all data from the urls passed and stores them in a JSON file"""

    restaurant_data = get_restaurant_info(url_list=url_list, file_name="Restaurants.json")
    return restaurant_data


if __name__ == '__main__':
    urls = ["https://www.zomato.com/lucknow/classic-restaurant-treat-mahanagar",
            "https://www.zomato.com/lucknow/ice-cream-sundae-shakes-and-more-hazratganj",
            "https://www.zomato.com/lucknow/neelkanth-green-gomti-nagar",
            "https://www.zomato.com/lucknow/fosho-pan-asian-italian-bistro-hazratganj",
            "https://www.zomato.com/lucknow/tanatan-hazratganj",
            "http://zomato.com/lucknow/curry-leaf-kapoorthala",
            "https://www.zomato.com/lucknow/purple-basil-1-gomti-nagar",
            ]
    
    data = scrape_all_data(urls)
    print("Data Scraped and Saved to JSON")
