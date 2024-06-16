import re
import pandas as pd
from Helper_feature_extraction_mobile import get_HTML_source_code_from_link , extract_features_from_HTML_mobile
import logging


# Setup logging configuration
logging.basicConfig(filename='processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


i = 0
# Example usage:
html_file_path = 'SuchErgebnis_mobile.txt'
output_excel_file = 'mobile_search_list_car_features.xlsx'



try:
    # Read the HTML content from the file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Define the pattern to search for car titles and URLs
    #pattern_car = r'"segment":"Car","title":"([^"]+)"'
    pattern_car = r'"segment":"Car"(?:,"partnerName":"[^"]*")?,"title":"([^"]+)"'
    pattern_url = r'"relativeUrl":"([^"]+)"'

    # Use regular expressions to find all matches in the HTML content
    car_titles = re.findall(pattern_car, html_content)
    urls = re.findall(pattern_url, html_content)
    
    # Replace '\u002F' with '/' and prepend 'https://suchen.mobile.de/' for each URL
    modified_urls = ["https://suchen.mobile.de/" + url.replace(r'\u002F', '/') for url in urls]
    # for debugging
    i = 0 
    source_pages = []
    for url in modified_urls:
        source_pages.append(get_HTML_source_code_from_link(url)) 
        i = i+1
        print(i)
        print(url)
 
    extracted_features_df = pd.DataFrame()
    try:
        extracted_features_df_list = []
        for source_page in source_pages:
            extracted_features_df_list.append(extract_features_from_HTML_mobile(source_page))

        extracted_features_df = pd.concat(extracted_features_df_list, ignore_index=True)

        print(extracted_features_df)
    except Exception as e:
        print(f"Error: {e}")

    
    # Create a DataFrame to hold the data
    URL_df = pd.DataFrame({'Car Title': car_titles, 'URL': modified_urls})
    print("URL_df created")  
    print(URL_df)
    # Concatenate URL_df with extracted_features_df along columns (axis=1)
    Result_df = pd.concat([URL_df, extracted_features_df], axis=1)

    # Write the DataFrame to an Excel file
    Result_df.to_excel(output_excel_file, index=False)

    print(f"Data successfully exported to '{output_excel_file}'.")
    
except FileNotFoundError:
    print(f"Error: File '{html_file_path}' not found.")
except Exception as e:
    print(f"Error: {e}")



