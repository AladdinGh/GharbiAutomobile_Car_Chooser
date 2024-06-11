import pandas as pd
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
import json

def get_HTML_source_code_from_link(url):
    """
    Fetch the HTML source code of a webpage given its URL using Microsoft Edge WebDriver.
    
    Args:
        url (str): The URL of the webpage to fetch.
    
    Returns:
        str: The HTML source code of the webpage.
    """
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
        time.sleep(5)  # Wait for 5 seconds (adjust based on your page load time)
        
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

def extract_features_from_HTML(html_content, url):
    """
    Extract features from the HTML content of a car listing webpage and map them to the specified DataFrame header.
    
    Args:
        html_content (str): The HTML content of the webpage.
        url (str): The URL of the webpage.
    
    Returns:
        pd.DataFrame: A DataFrame containing the extracted features mapped to the specified header.
    """
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the JSON data within the script tag
    script_tag = soup.find('script', type='application/json')
    json_data = json.loads(script_tag.string)
    
    # Attempt to extract listing details and vehicle details
    try:
        listing_details = json_data['props']['pageProps']['listingDetails']
    except Exception as e:
        print(f"Error listing_details : {e}")
        listing_details = json_data['props']['pageProps']['properData']['carDetails']
       
    try:
        vehicle_details = json_data['props']['pageProps']['listingDetails']['vehicle']
    except Exception as e:
        print(f"Error vehicle_details: {e}")
        vehicle_details = json_data['props']['pageProps']['properData']['carDetails']['vehicle']
        
    try:
        prices = json_data['props']['pageProps']['listingDetails']['prices']['public']['price']
    except Exception as e:
        print(f"Error prices: {e}")
        prices = json_data['props']['pageProps']['properData']['carDetails']['price']['value']['raw']
        
    try:
        description = json_data['props']['pageProps']['listingDetails']['description']
    except Exception as e:
        print(f"Error description: {e}")
        description = " "
         
    try:
        make = json_data['props']['pageProps']['listingDetails']['vehicle']['make']
        model = json_data['props']['pageProps']['listingDetails']['vehicle']['model']
        second_title = json_data['props']['pageProps']['listingDetails']['vehicle']['modelVersionInput']
    except Exception as e:
        make = json_data['props']['pageProps']['properData']['carDetails']['make']  
        model = json_data['props']['pageProps']['properData']['carDetails']['model']  
        second_title = json_data['props']['pageProps']['properData']['carDetails']['modelVersion'] 
    
    # Extract fuel consumption information
    try: 
        consumption = vehicle_details['fuelConsumptionCombined']['raw']
        if consumption is None:
            consumption = vehicle_details['wltp']['consumptionCombinedWithFallback']['raw'] 
            if consumption is None:
                consumption = vehicle_details['fuelConsumptionCombined']['raw']

    except Exception as e:
        print(f"Error consumption: {e}")
        consumption = " "
        

        

    # Extract CO2 emissions information
    try:
        emissions = vehicle_details['co2EmissionsCombinedWithFallback']['raw']
        
    except Exception as e:
        
        if vehicle_details.get('wltp') and vehicle_details['wltp'].get('co2EmissionsCombinedWithFallback'):
            emissions = vehicle_details['wltp']['co2EmissionsCombinedWithFallback']['raw']
        else:
            emissions = vehicle_details['co2emissionInGramPerKmWithFallback']['raw']   
        print(f"Error emissions: {e}")
        
       
            
    # Flatten the data structure into a dictionary
    data = {
        "Car Title": f"{make} {model}",
        "URL": url,
        "Title": second_title,
        "Secondary Title": "",  # Secondary title not provided in the original data
        "Brutto Price": prices,
        "Netto Price": "",  # Netto price not provided in the original data
        "Dealer Name": "",  # Dealer name not provided in the original data
        "Dealer Location": "",  # Dealer location not provided in the original data
        "Kilometerstand": vehicle_details['mileageInKmRaw'],
        "Erstzulassung": vehicle_details['firstRegistrationDate'],
        "Leistung": "",  # Leistung (power) not directly provided, can be powerInKw or powerInHp
        "Getriebe": vehicle_details['transmissionType'],
        "Fahrzeughalter": "",  # Fahrzeughalter (number of owners) not provided in the original data
        "Kraftstoffart": f"{vehicle_details['fuelCategory']['formatted']}, {vehicle_details['primaryFuel']['formatted']}",
        "Fahrzeugzustand": "",  # Fahrzeugzustand (condition) not provided in the original data
        "Kategorie": vehicle_details['bodyType'],
        "Herkunft": "",  # Herkunft (origin) not provided in the original data
        "Hubraum": vehicle_details['displacementInCCM'],
        "Antriebsart": "",  # Antriebsart (drive type) not provided in the original data
        "Energieverbrauch (komb.)2": consumption,
        "CO₂-Emissionen (komb.)2": emissions,
        "Kraftstoffverbrauch": consumption,
        "Anzahl Sitzplätze": vehicle_details['numberOfSeats'],
        "Anzahl der Türen": vehicle_details['numberOfDoors'],
        "Schadstoffklasse": "",  # Schadstoffklasse (emission standard) not provided in the original data
        "Umweltplakette": "",  # Umweltplakette (environmental sticker) not provided in the original data
        "Anzahl der Fahrzeughalter": "",  # Anzahl der Fahrzeughalter (number of owners) not provided in the original data
        "HU": "",  # HU (inspection) not provided in the original data
        "Klimatisierung": "",  # Klimatisierung (air conditioning) not provided in the original data
        "Einparkhilfe": "",  # Einparkhilfe (parking assistance) not provided in the original data
        "Airbags": "",  # Airbags not provided in the original data
        "Farbe (Hersteller)": vehicle_details['bodyColor'],
        "Farbe": vehicle_details['bodyColor'],
        "Innenausstattung": vehicle_details['upholstery'],
        "Equipment": "",  # Will be concatenated later
        "Description": description,
        "Fahrzeugnummer": "",  # Fahrzeugnummer (vehicle number) not provided in the original data
        "Verbrauch": consumption,
        "CO₂-Emissionen": emissions,
        "Verfügbarkeit": "",  # Verfügbarkeit (availability) not provided in the original data
        "Zugr.-lgd.": "",  # Zugr.-lgd. not provided in the original data
        "Treibstoffart": "",  # Treibstoffart (fuel type) not provided in the original data
        "Energieeffizienzklasse": "",  # Energieeffizienzklasse (energy efficiency class) not provided in the original data
        "CO₂-Effizienz": "",  # CO₂-Effizienz (CO2 efficiency) not provided in the original data
        "KW": vehicle_details['powerInKw'],
        "PS": vehicle_details['powerInHp']
    }

    # Attempt to extract equipment details
    try:
        equipment = listing_details['vehicle']['equipment']
    except Exception as e:
        print(f"Error in equipment = listing_details['vehicle']['equipment'] : {e}")
        equipment = {}

    # Extract comfort and convenience equipment IDs
    try:
        if equipment.get('comfortAndConvenience') is not None:
            comfort_and_convenience_ids = [item['id'] for item in equipment['comfortAndConvenience']]
        elif equipment.get('Komfort') is not None:
            comfort_and_convenience_ids = [item['id'] for item in equipment['Komfort']]
        else:
            comfort_and_convenience_ids = []
    except Exception as e:
        print(f"Error in comfort_and_convenience_ids: {e}")
        comfort_and_convenience_ids = []
        pass
    
    # Extract entertainment and media equipment IDs
    try:
        if equipment.get('entertainmentAndMedia') is not None:
            entertainment_and_media_ids = [item['id'] for item in equipment['entertainmentAndMedia']]
        elif equipment.get('Unterhaltung/Media') is not None:
            entertainment_and_media_ids = [item['id'] for item in equipment['Unterhaltung/Media']]
        else:
            entertainment_and_media_ids = []
    except Exception as e:
        print(f"Error in entertainment_and_media_ids: {e}")
        entertainment_and_media_ids = []
        pass
    
    # Extract safety and security equipment IDs
    try:
        if equipment.get('safetyAndSecurity') is not None:
            safety_and_security_ids = [item['id'] for item in equipment['safetyAndSecurity']]
        elif equipment.get('Sicherheit') is not None:
            safety_and_security_ids = [item['id'] for item in equipment['Sicherheit']]
        else:
            safety_and_security_ids = []
    except Exception as e:
        print(f"Error safety_and_security_ids: {e}")
        safety_and_security_ids = []
        pass
    
    # Extract extras equipment IDs
    try:
        if equipment.get('extras') is not None:
            extras_ids = [item['id'] for item in equipment['extras']]
        elif equipment.get('Extras') is not None:
            extras_ids = [item['id'] for item in equipment['Extras']]
        else:
            extras_ids = []
    except Exception as e:
        print(f"Error in extras_ids: {e}")
        extras_ids = []
        pass

    # Concatenate equipment IDs and add to the data dictionary
    equipment_ids = comfort_and_convenience_ids + entertainment_and_media_ids + safety_and_security_ids + extras_ids
    data['Equipment'] = ', '.join(equipment_ids)

    # Convert the data dictionary to a DataFrame and save it as an Excel file
    df = pd.DataFrame([data])
    df.to_excel('autoscout_search_list_car_features.xlsx', index=False)
    
    return df

# # Example usage:
# url = 'https://www.autoscout24.de/smyle/details/00cfde42-1520-4a87-b746-4790105a784b/'  # Example URL
# page_source = get_HTML_source_code_from_link(url)

# if page_source:
#     print("Page source code successfully retrieved.")
#     print("Extracting features....")
#     extract_features_from_HTML(page_source, url)
# else:
#     print("Failed to retrieve page source code.")
