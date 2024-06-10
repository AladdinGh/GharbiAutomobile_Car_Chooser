import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from Helper_feature_extraction_autoscout import get_HTML_source_code_from_link, extract_features_from_HTML

def save_string_to_text_file(string, file_path):
    """
    Save a string to a text file.
    
    Args:
        string (str): The string to save.
        file_path (str): The path of the file where the string will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(string)

# Load the HTML file
with open('SuchErgebnis_autoscout.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Find the script containing JSON data
soup = BeautifulSoup(html_content, 'html.parser')
script_tags = soup.find_all('script', {'type': 'application/json'})

# Extract JSON data containing listings
listings_json = None
for script_tag in script_tags:
    if 'listings' in script_tag.string:
        listings_json = script_tag.string
        break

# Initialize a list to store dictionaries of attributes
all_listings_attributes = []

# Extract attributes of the listings, mainly the URLs to get car features
if listings_json:
    listings_data = json.loads(listings_json)
    listings = listings_data['props']['pageProps']['listings']

# Convert list of dictionaries to DataFrame
URL_df = pd.DataFrame(listings)

# Add prefix to the 'url' attribute
URL_df['url'] = 'https://www.autoscout24.de' + URL_df['url']

# Initialize counters and storage
i = 0
source_pages = []
extracted_features_df_list = []

# Fetch and extract features for each listing URL
try:
    for url in URL_df['url']:
        print(f"Processing URL: {url}")
        
        # Fetch HTML source code
        source_page = get_HTML_source_code_from_link(url)
        source_pages.append(source_page)
        
        # Extract features and add to the list
        extracted_features_df_list.append(extract_features_from_HTML(source_page, url))
        
        i += 1
        print(f"Processed {i} URLs")
        
    # Concatenate all extracted features into a single DataFrame
    extracted_features_df = pd.concat(extracted_features_df_list, ignore_index=True)
    print(extracted_features_df)
    
    # convcert to strings to make easier to preprocess
    extracted_features_df = extracted_features_df.astype(str)
    # Save the DataFrame as an Excel file
    extracted_features_df.to_excel('autoscout_search_list_car_features.xlsx', index=False)
    print("DataFrame saved as autoscout_search_list_car_features.xlsx")
    
except Exception as e:
    print(f"Error: {e}")
    print("Problem with extracting features")
