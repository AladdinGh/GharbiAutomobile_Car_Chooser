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



def extract_features_to_HTML(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract specific elements from the HTML using BeautifulSoup
    titles = [title.get_text().strip() for title in soup.find_all(class_=["listing-title", "listing-subtitle"])]
    prices = [price.get_text().strip() for price in soup.find_all(class_=["main-price-and-rating-row", "price-and-financing-row-secondary"])]
    dealer_name = soup.find(class_=["link--muted u-text-decoration-none seller-title"]).get_text().strip()
    dealer_location = soup.find(class_=["seller-address"]).get_text().strip()

    # Extract key features and map them to attribute-value pairs
    main_features = {}
    labels = soup.find_all(class_=["key-feature__label"])
    values = soup.find_all(class_=["key-feature__value"])
    for label, value in zip(labels, values):
        label_text = label.get_text().strip()
        value_text = value.get_text().strip()
        main_features[label_text] = value_text

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

    # Extract equipment and combine into a single column
    equipment = ', '.join(item.get_text().strip() for item in soup.find_all(class_=["bullet-list"]))

    # Extract description
    description = soup.find(class_=["g-col-12 description"]).get_text().strip()

    # Create a DataFrame with the extracted data
    data = {
        'Title': titles[0],
        'Secondary Title': titles[1] if len(titles) > 1 else '',
        'Brutto Price': prices[0],
        'Netto Price': extract_netto_price(prices),
        'Dealer Name': dealer_name,
        'Dealer Location': dealer_location,
        #'Link': link,  # Include the link in the extracted features
        **main_features,
        **technical_features,
        'Equipment': equipment,
        'Description': description
    }

    df = pd.DataFrame([data])

    return df


# Example usage:
if __name__ == "__main__":
    html_content = input("Paste or type the HTML content for the car listing: ")
   
    try:
        # Extract key features from the HTML content
        extracted_features_df = extract_features_to_HTML(html_content)

        # Save extracted features to Excel
        output_file_path = 'extracted_features.xlsx'
        extracted_features_df.to_excel(output_file_path, index=False)
        print(f"Extracted features saved to {output_file_path}")
    except Exception as e:
        print(f"Error extracting features: {e}")
    #extract_features_to_excel(html_content, link)
