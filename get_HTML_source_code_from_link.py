import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService

def get_HTML_source_code_from_link(url):
    # Specify the path to the Microsoft Edge WebDriver executable
    edge_driver_path = r"C:\Users\c95031653\Downloads\edgedriver_win64\msedgedriver.exe"  # Change this to your Edge WebDriver path

    # Set up Microsoft Edge WebDriver options
    edge_options = Options()
    edge_service = EdgeService(executable_path=edge_driver_path)
    # Add any specific options if needed (e.g., headless mode)
    # edge_options.use_chromium = True  # Ensure using Edge Chromium
    # edge_options.add_argument('--headless')  # Uncomment to run in headless mode
    # edge_options.add_argument('--disable-gpu')  # If running in headless mode

    driver = None
    try:
        # Initialize Edge WebDriver with options
        driver = webdriver.Edge(service=edge_service)

        # Open the URL in Microsoft Edge
        driver.get(url)
        
        # Wait for the page to load (adjust sleep time as needed)
        time.sleep(20)  # Wait for 20 seconds (you can adjust this based on your page load time)
        
        # Get the page source
        page_source = driver.page_source
        
        return page_source

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        if driver:
            # Quit the WebDriver session
            driver.quit()

# Example usage:
# url = 'https://suchen.mobile.de/fahrzeuge/details.html?id=392195401&action=eyeCatcher&dam=false&fr=2022%3A&isSearchRequest=true&rd=100&ref=srp&refId=dbeec509-3508-8775-d4af-b95365158750&s=Car&sb=rel&searchId=dbeec509-3508-8775-d4af-b95365158750&vc=Car'
# page_source = get_HTML_source_code_from_link(url)

# if page_source:
#     print("Page source code successfully retrieved.")
# else:
#     print("Failed to retrieve page source code.")
