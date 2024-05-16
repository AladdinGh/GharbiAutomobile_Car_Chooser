import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def get_HTML_source_code_from_link(url):
    # Specify the path to the Microsoft Edge WebDriver executable
    edge_driver_path = r"C:\Users\c95031653\Downloads\edgedriver_win64\msedgedriver.exe"  # Change this to your Edge WebDriver path

    # Set up Microsoft Edge WebDriver options
    options = Options()
    # Add any specific options if needed

    # Set up Edge service (not always necessary)
    service = Service(edge_driver_path)

    try:
        # Initialize Edge WebDriver
        driver = webdriver.Edge(service=service, options=options)

        # Open the URL in Microsoft Edge
        driver.get(url)
        
        # Wait for the page to load (adjust sleep time as needed)
        time.sleep(10)  # Wait for 20 seconds (you can adjust this based on your page load time)
        
        # Get the page source
        page_source = driver.page_source
        
        return page_source

    finally:
        # Quit the WebDriver session
        driver.quit()

# Example usage:
#url = 'https://suchen.mobile.de/fahrzeuge/details.html?id=392195401&action=eyeCatcher&dam=false&fr=2022%3A&isSearchRequest=true&rd=100&ref=srp&refId=dbeec509-3508-8775-d4af-b95365158750&s=Car&sb=rel&searchId=dbeec509-3508-8775-d4af-b95365158750&vc=Car'
#page_source = get_HTML_source_code_from_link(url)


# Now you have the page source in the `page_source` variable
# You can save it to a file or process it further as needed
