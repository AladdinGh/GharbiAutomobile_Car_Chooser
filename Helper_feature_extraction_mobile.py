import pandas as pd
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


import random


def extract_netto_price(prices):
    netto_price = ''  # Default value for netto price

    # Regular expression pattern to match a numeric value followed by "Netto"
    pattern = r'(\d[\d,.]*\s*€)\s*\(Netto\)'

    for price in prices:
        match = re.search(pattern, price)
        if match:
            netto_price = match.group(1)
            break  # Stop searching once netto price is found

    return netto_price



def extract_features_from_HTML_mobile(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract specific elements from the HTML using BeautifulSoup
    titles = [title.get_text().strip() for title in soup.find_all(class_=["listing-title", "listing-subtitle"])]
    link = soup.find('link', {'rel': 'canonical'})
    print("link", link)
    
    prices = [price.get_text().strip() for price in soup.find_all(class_=["main-price-and-rating-row", "price-and-financing-row-secondary"])]   
    print("prices", prices)
    
    dealer_name = soup.find(class_=["link--muted u-text-decoration-none seller-title"]).get_text().strip()
    print("dealer_name", dealer_name)     
    
    
    dealer_location = soup.find(class_=["seller-address"]).get_text().strip()
    print("dealer_location", dealer_location)
    # Extract key features and map them to attribute-value pairs
    main_features = {}
    labels = soup.find_all(class_=["key-feature__label"])
    values = soup.find_all(class_=["key-feature__value"])
    for label, value in zip(labels, values):
        label_text = label.get_text().strip()
        value_text = value.get_text().strip()
        main_features[label_text] = value_text
        
        
    print("main_features", main_features)
    # Extract technical features and map them to attribute-value pairs
    technical_features = {}
    rows = soup.find_all(class_="g-row u-margin-bottom-9")
    for row in rows:
        elements = row.find_all(class_=["g-col-6", "g-col-6"])
        if len(elements) == 2:
            label_element = elements[0]
            value_element = elements[1]
            label_text = label_element.get_text().strip()
            value_text = value_element.get_text().strip()
            technical_features[label_text] = value_text
    
    print("technical_features", technical_features)
    
    
    # Extract equipment and combine into a single column
    try:
        equipment = ', '.join(item.get_text().strip() for item in soup.find_all(class_=["bullet-list"]))
        print("equipment", equipment)
    except Exception as e:
        equipment = " "
        print("equipment not found")

    # Extract description
    try:    
        description = soup.find(class_=["g-col-12 description"]).get_text().strip()
        print("description", description)
    except Exception as e:
        description = " "
        print("description not found")

    # Create a DataFrame with the extracted data
    data = {
        'Title': titles[0],
        'Secondary Title': titles[1] if len(titles) > 1 else '',
        'Brutto Price': prices[0],
        'Netto Price': extract_netto_price(prices),
        'Dealer Name': dealer_name,
        'Dealer Location': dealer_location,
        **main_features,
        **technical_features,
        'Equipment': equipment,
        'Description': description
    }
    
    df = pd.DataFrame([data])
    print(df)
    return df

      
def get_HTML_source_code_from_link(url):
    
    edge_driver_path = r"C:\Users\c95031653\Downloads\edgedriver_win64\msedgedriver.exe"
    edge_options = Options()
    edge_service = EdgeService(executable_path=edge_driver_path)

    # proxy = "http://127.0.0.1:9000/localproxy-7944404c"
    # edge_options.add_argument(f'--proxy-server={proxy}')
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    try:
        driver = webdriver.Edge(service=edge_service, options=edge_options)
        driver.get(url)
        time.sleep(1)
        page_source = driver.page_source
        return page_source
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if driver:
            driver.quit()
 
            
# def get_HTML_source_code_from_link(url):
    
#     # Set up Chrome options
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")  # Run in headless mode (optional)
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("user-agent=your custom user agent string")
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    
#     # Initialize the Chrome driver
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
#     # Open the website
#     driver.get(url)
    
#     # appear more like a real user
#     cookies = driver.get_cookies()
#     for cookie in cookies:
#         driver.add_cookie(cookie)
    
    
#     # Allow some time for the page to load

#     time.sleep(random.uniform(2, 5))  # Random delay between 2 to 5 seconds
#     source_page = driver.page_source
    
#     with open('source_code_test.txt', 'w', encoding='utf-8') as file:
#         file.write(source_page)
    
#     # Quit the driver
#     driver.quit()
        
    
# url = 'https://suchen.mobile.de/fahrzeuge/details.html?id=391618886&dam=false&fr=2010%3A2013&isSearchRequest=true&ms=24100%3B28%3B%3B&pageNumber=8&ref=srp&refId=e6f455f4-559a-2018-58f7-c3f8d92181c6&s=Car&sb=rel&searchId=e6f455f4-559a-2018-58f7-c3f8d92181c6&vc=Car'    
# get_HTML_source_code_from_link(url)   
    
    
    
    # Example usage:
# url = 'https://suchen.mobile.de/fahrzeuge/details.html?id=392195401&action=eyeCatcher&dam=false&fr=2022%3A&isSearchRequest=true&rd=100&ref=srp&refId=dbeec509-3508-8775-d4af-b95365158750&s=Car&sb=rel&searchId=dbeec509-3508-8775-d4af-b95365158750&vc=Car'
# page_source = get_HTML_source_code_from_link(url)

# if page_source:
#     print("Page source code successfully retrieved.")
# else:
#     print("Failed to retrieve page source code.")
