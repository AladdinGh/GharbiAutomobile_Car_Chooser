import re
import pandas as pd
from get_HTML_source_code_from_link import get_HTML_source_code_from_link
from extract_car_info_from_HTML import extract_features_to_HTML


def get_car_features_from_search_result(html_file_path, output_excel_file):
    try:
        # Read the HTML content from the file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define the pattern to search for car titles and URLs
        pattern_car = r'"segment":"Car","title":"([^"]+)"'
        pattern_url = r'"relativeUrl":"([^"]+)"'

        # Use regular expressions to find all matches in the HTML content
        car_titles = re.findall(pattern_car, html_content)
        urls = re.findall(pattern_url, html_content)

        # Replace '\u002F' with '/' and prepend 'https://suchen.mobile.de/' for each URL
        modified_urls = ["https://suchen.mobile.de/" + url.replace(r'\u002F', '/') for url in urls]

        source_pages = [get_HTML_source_code_from_link(url) for url in modified_urls]
        
        # Extract key features from the HTML content and combine into a single DataFrame
        extracted_features_df_list = [extract_features_to_HTML(source_page) for source_page in source_pages]
        extracted_features_df = pd.concat(extracted_features_df_list, ignore_index=True)

        # Create a DataFrame to hold the data
        URL_df = pd.DataFrame({'Car Title': car_titles, 'URL': modified_urls})

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
html_file_path = 'SuchErgebnis.txt'
output_excel_file = 'car_data.xlsx'

get_car_features_from_search_result(html_file_path, output_excel_file)
