import pandas as pd
from bs4 import BeautifulSoup
import re


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



def extract_features_from_HTML(html_content):
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
