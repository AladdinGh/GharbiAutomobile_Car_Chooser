import re
import pandas as pd
from Helper_feature_extraction import get_HTML_source_code_from_link , extract_features_from_HTML
import logging


# Setup logging configuration
logging.basicConfig(filename='processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


i = 0
def get_car_features_from_search_result(html_file_path, output_excel_file):
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
        
        try:
            extracted_features_df_list = []
            for source_page in source_pages:
                extracted_features_df_list.append(extract_features_from_HTML(source_page))
            print("out of extracted_features_df_list")
            extracted_features_df = pd.concat(extracted_features_df_list, ignore_index=True)
            print("extracted_features_df created")
            print(extracted_features_df)
        except Exception as e:
            print(f"Error: {e}")
            print("problem with extract features")
        
        for car_title,modified_url in zip(car_titles,modified_urls):
            print()
            print()
            print("car_title", car_title)
            print("modified_url", modified_url)
        print("car_titles", car_titles)
        print("length car_titles", len(car_titles))
        print("modified_urls", modified_urls)
        print("length modified_urls", len(modified_urls))
        
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

# Example usage:
html_file_path = 'SuchErgebnis_wasserstoff.txt'
output_excel_file = 'output/search_list_car_features.xlsx'

get_car_features_from_search_result(html_file_path, output_excel_file)
