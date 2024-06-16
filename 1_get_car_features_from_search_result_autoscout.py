import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from Helper_feature_extraction_autoscout import get_HTML_source_code_from_link, extract_features_from_HTML_autoscout



# Read the HTML content from the file
with open('SuchErgebnis_autoscout.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Find the script containing JSON data
soup = BeautifulSoup(html_content, 'html.parser')
script_tags = soup.find_all('script', {'type': 'application/json'})

# Initialize a list to store dictionaries of attributes
all_listings_attributes = []

# Extract JSON data containing listings from each script tag
for script_tag in script_tags:
    if 'listings' in script_tag.string:
        listings_json = script_tag.string
        listings_data = json.loads(listings_json)
        listings = listings_data['props']['pageProps']['listings']
        all_listings_attributes.extend(listings)

# Now all_listings_attributes contains attributes from all JSON data in the HTML file
# print(len(all_listings_attributes))
# input()

# Convert list of dictionaries to DataFrame
URL_df = pd.DataFrame(all_listings_attributes)

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
        extracted_features_df_list.append(extract_features_from_HTML_autoscout(source_page, url))
        
        i += 1
        print(f"Processed {i} URLs")
        
    # Concatenate all extracted features into a single DataFrame
    extracted_features_df = pd.concat(extracted_features_df_list, ignore_index=True)
    print(extracted_features_df)
    
    # Save the DataFrame as an Excel file
    extracted_features_df.to_excel('autoscout_search_list_car_features.xlsx', index=False)
    print("DataFrame saved as autoscout_search_list_car_features.xlsx")
    
except Exception as e:
    print(f"Error: {e}")
    print("Problem with extracting features")


