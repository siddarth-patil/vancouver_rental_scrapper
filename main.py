import csv
import json

import requests
from bs4 import BeautifulSoup

CRAIGSLIST_URL = "https://vancouver.craigslist.org/search/hhh#search=1~gallery~0~0"
OUTPUT_JSON = "output.json"

response = requests.get(CRAIGSLIST_URL, timeout=90)

html_soup = BeautifulSoup(response.text, "html.parser")

with open("test.txt", mode="w") as file:
    file.write(str(html_soup))

# get the macro-container for the housing posts
posts = html_soup.find_all("li", class_="cl-static-search-result")

# Create a list to store the data
data_list = []

for post in posts:
    # Fetch post data
    post_data = post.a.text.strip().splitlines()
    post_cleaned_data = [item.strip() for item in post_data if item.strip()]

    # Fetch post link
    post_link = post.find("a").get("href")

    # Create a dictionary with post data
    post_dict = {
        "title": post_cleaned_data[0],
        "price": post_cleaned_data[1],
        "location": post_cleaned_data[2],
        "link": post_link,
    }

    # Append the dictionary to the list
    data_list.append(post_dict)

# Write to JSON
with open(OUTPUT_JSON, mode="w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, indent=2)
