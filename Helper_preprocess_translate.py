import logging
import pandas as pd
from googletrans import Translator
import spacy
from tqdm import tqdm
import re
from datetime import datetime
import requests



#########################################    Translate functions ######################################################
# Setup logging configuration
logging.basicConfig(filename='processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load the French language model for spaCy
nlp = spacy.load("fr_core_news_sm")

# Function to correct spelling mistakes in French text
def correct_spelling(text):
    try:
        # Process the text with spaCy
        doc = nlp(text)
        
        # Correct spelling mistakes
        corrected_text = ' '.join(token.text for token in doc)
        
        return corrected_text
    except Exception as e:
        logging.error(f"Error in correct_spelling: {e}")
        return text

# Initialize the Translator
translator = Translator()

# Function to translate a single text
def translate_text(text):
    try:
        translation = translator.translate(text, src='de', dest='fr').text
        return translation
    except Exception as e:
        logging.error(f"Error occurred during translation: {e}")
        return text  # Return original text if translation fails

# Function to translate values in selected columns
def translate_column_values(preprocessed_df, column):
    try:
        # Use tqdm to display progress bar
        translated_values = []
        for value in tqdm(preprocessed_df[column], desc=f"Translating {column}"):
            translated_text = translate_text(value)
            corrected_text = correct_spelling(translated_text)
            translated_values.append(corrected_text)
        return translated_values
    except Exception as e:
        logging.error(f"Error occurred during translation of column {column}: {e}")
        return preprocessed_df[column]  # Return original values if translation fails

def translate_df(file_path):   
    try:
        # Load dataframe from Excel file
        preprocessed_df = pd.read_excel(file_path)
        
        # Define the columns to be translated
        columns_to_translate = ['Farbe', 'Description']
        
        # Translate values in selected columns
        preprocessed_df['Description'] = preprocessed_df['Description'].astype(str)
        for col in columns_to_translate:
            preprocessed_df[col] = translate_column_values(preprocessed_df, col)
        
        preprocessed_df.rename(columns={'Getriebe': 'Boite_vitesse', 'Kraftstoffart': 'carburant', 'Fahrzeugzustand': 'Etat_voiture'
                           , 'Kategorie': 'categorie', 'Klimatisierung': 'climatisation'
                           , 'Einparkhilfe': 'Aide_parking'
                           , 'Innenausstattung': 'Options', 'Kraftstoffverbrauch': 'Consommation'}, inplace=True)

        # Translation dictionary
        preprocessed_df.rename(columns={
            'Abstandstempomat': 'Régulateur de distance',
            'Abstandswarner': 'Avertisseur de distance',
            'Adaptives Kurvenlicht': 'Éclairage adaptatif en virage',
            'Alarmanlage': 'Alarme',
            'Allradantrieb': 'Transmission intégrale',
            'Allwetterreifen': 'Pneus toutes saisons',
            'Ambiente-Beleuchtung': 'Éclairage d’ambiance',
            'Anhängerkupplung abnehmbar': 'Attelage amovible',
            'Anhängerkupplung fest': 'Attelage fixe',
            'Anhängerkupplung-Vorbereitung': 'Préparation pour attelage',
            'Armlehne': 'Accoudoir',
            'Beheizbare Frontscheibe': 'Pare-brise chauffant',
            'Beheizbares Lenkrad': 'Volant chauffant',
            'Berganfahrassistent': 'Assistance au démarrage en côte',
            'Bi-Xenon Scheinwerfer': 'Phares bi-xénon',
            'Blendfreies Fernlicht': 'Feux de route anti-éblouissement',
            'Bluetooth': 'Bluetooth',
            'Bordcomputer': 'Ordinateur de bord',
            'CD-Spieler': 'Lecteur CD',
            'Dachreling': 'Barres de toit',
            'ESP': 'ESP',
            'Elektr. Fensterheber': 'Lève-vitres électriques',
            'Elektr. Heckklappe': 'Hayon électrique',
            'Elektr. Seitenspiegel': 'Rétroviseurs extérieurs électriques',
            'Elektr. Sitzeinstellung': 'Réglage électrique des sièges',
            'Elektr. Wegfahrsperre': 'Antidémarrage électronique',
            'Fernlichtassistent': 'Assistant feux de route',
            'Freisprecheinrichtung': 'Kit mains libres',
            'Garantie': 'Garantie',
            'Gepäckraumabtrennung': 'Séparation du compartiment à bagages',
            'Geschwindigkeitsbegrenzer': 'Limiteur de vitesse',
            'Innenspiegel autom. abblendend': 'Rétroviseur intérieur électrochrome',
            'Isofix': 'Isofix',
            'Isofix Beifahrersitz': 'Isofix siège passager',
            'Kurvenlicht': 'Éclairage en virage',
            'LED-Scheinwerfer': 'Phares LED',
            'LED-Tagfahrlicht': 'Feux de jour LED',
            'Lederlenkrad': 'Volant en cuir',
            'Leichtmetallfelgen': 'Jantes en alliage léger',
            'Lichtsensor': 'Capteur de lumière',
            'Lordosenstütze': 'Support lombaire',
            'Multi-CD-Wechsler': 'Changeur de CD',
            'Multifunktionslenkrad': 'Volant multifonction',
            'Musikstreaming integriert': 'Streaming musical intégré',
            'Müdigkeitswarner': 'Détecteur de somnolence',
            'Navigationssystem': 'Système de navigation',
            'Nebelscheinwerfer': 'Phares antibrouillard',
            'Nichtraucher-Fahrzeug': 'Véhicule non-fumeur',
            'Notbremsassistent': 'Assistant de freinage d’urgence',
            'Notrad': 'Roue de secours',
            'Notrufsystem': 'Système d’appel d’urgence',
            'Pannenkit': 'Kit de dépannage',
            'Panorama-Dach': 'Toit panoramique',
            'Partikelfilter': 'Filtre à particules',
            'Radio DAB': 'Radio DAB',
            'Raucherpaket': 'Pack fumeur',
            'Regensensor': 'Capteur de pluie',
            'Reifendruckkontrolle': 'Contrôle de la pression des pneus',
            'Reserverad': 'Roue de secours',
            'Schaltwippen': 'Palettes de changement de vitesse',
            'Scheckheftgepflegt': 'Carnet d’entretien complet',
            'Scheinwerferreinigung': 'Lave-phares',
            'Schiebedach': 'Toit ouvrant',
            'Schlüssellose Zentralverriegelung': 'Verrouillage centralisé sans clé',
            'Servolenkung': 'Direction assistée',
            'Sitzheizung': 'Sièges chauffants',
            'Sitzheizung hinten': 'Sièges arrière chauffants',
            'Skisack': 'Sac à skis',
            'Sommerreifen': 'Pneus été',
            'Soundsystem': 'Système audio',
            'Sportfahrwerk': 'Châssis sport',
            'Sportpaket': 'Pack sport',
            'Sportsitze': 'Sièges sport',
            'Sprachsteuerung': 'Commande vocale',
            'Spurhalteassistent': 'Assistant de maintien de voie',
            'Standheizung': 'Chauffage d’appoint',
            'Start/Stopp-Automatik': 'Système Start/Stop automatique',
            'TV': 'TV',
            'Tagfahrlicht': 'Feux de jour',
            'Tempomat': 'Régulateur de vitesse',
            'Totwinkel-Assistent': 'Assistant d’angle mort',
            'Touchscreen': 'Écran tactile',
            'Traktionskontrolle': 'Contrôle de traction',
            'Tuner/Radio': 'Radio',
            'USB': 'USB',
            'Verkehrszeichenerkennung': 'Reconnaissance des panneaux de signalisation',
            'WLAN / Wifi Hotspot': 'Hotspot WLAN / Wifi',
            'Winterpaket': 'Pack hiver',
            'Winterreifen': 'Pneus hiver',
            'Xenonscheinwerfer': 'Phares au xénon',
            'Zentralverriegelung': 'Verrouillage centralisé',
            'ABS': 'ABS'
            }, inplace=True)

        return preprocessed_df
    except Exception as e:
        logging.error(f"Error in translate_df: {e}")
        return None

def translate_preprocessed_search_result(file_path):    
    try:
        translated_df = translate_df(file_path)
        if translated_df is not None:
            translated_df.to_excel("2_translated_preprocessed_df.xlsx", index=False)
            logging.info("Translated dataframe saved as 'translated_preprocessed_df.xlsx'")
        else:
            logging.error("Translation failed, dataframe not saved.")
    except Exception as e:
        logging.error(f"Error in translate_preprocessed_search_result: {e}")

##############################################################################################################################

############################################### Preprocessing functions  #####################################################
def preprocess_dataframe(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # remove dups
        df = df.drop_duplicates()
        
        #shorten the URL
        df['Short_URL'] = df['URL'].apply(shorten_url)
        
        # Create a Title column with the first three words of the Car Title
        df['Title'] = df['Car Title'].str.split().str[:3].str.join(' ')
        
        # Create a column for each equipment
        if 'Equipment' in df.columns:
            equipment_split = df['Equipment'].dropna().str.split(',').apply(lambda x: [s.strip() for s in x]).str.join('|').str.get_dummies()
            df = pd.concat([df, equipment_split], axis=1)
        
        # Remove Brutto/Netto from Price
        if 'Brutto Price' in df.columns:
            df['Brutto Price'] = df['Brutto Price'].apply(clean_price).astype(float)
        
        # Separate KW from PS
        if 'Leistung' in df.columns:
            df['KW'] = df['Leistung'].str.extract(r'(\d+)\s*kW', expand=False).astype(float)
            df['PS'] = df['Leistung'].str.extract(r'(\d+)\s*PS', expand=False).astype(float)
        
        # Convert Kilometerstand to numerical
        if 'Kilometerstand' in df.columns:
            df['Kilometerstand'] = df['Kilometerstand'].apply(clean_kilometerstand).astype(float)
        
        # Process Verbrauch and Energieverbrauch (komb.)2
        if 'Verbrauch' in df.columns or 'Energieverbrauch (komb.)2' in df.columns:
            df['Kraftstoffverbrauch'] = df.apply(lambda row: extract_first_consumption(row, df), axis=1).astype(float)
        
        average_consumption = df['Kraftstoffverbrauch'].mean()
        df['Kraftstoffverbrauch'].fillna(average_consumption, inplace=True)
        
        # Drop the Energieverbrauch (komb.)2 column
        df.drop(columns=['Energieverbrauch (komb.)2'], inplace=True, errors='ignore')
        
        # Update Farbe column
        if 'Farbe (Hersteller)' in df.columns:
            df['Farbe'] = df['Farbe'].fillna(df['Farbe (Hersteller)'])
            df.drop(columns=['Farbe (Hersteller)'], inplace=True, errors='ignore')
        
        # Convert Erstzulassung to age in years
        if 'Erstzulassung' in df.columns:
            df['Erstzulassung_years'] = df['Erstzulassung'].apply(convert_erstzulassung_to_age)
        
        return df
    except Exception as e:
        logging.error(f"Error in preprocess_dataframe: {e}")
        return None

def clean_price(price):
    try:
        if isinstance(price, str):
            match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*€', price)
            if match:
                return float(match.group(1).replace('.', '').replace(',', '.'))
        return None
    except Exception as e:
        logging.error(f"Error in clean_price: {e}")
        return None

def clean_kilometerstand(km):
    try:
        if isinstance(km, str):
            numeric_km = re.sub(r'[^\d]', '', km)
            return int(numeric_km) if numeric_km else None
        return None
    except Exception as e:
        logging.error(f"Error in clean_kilometerstand: {e}")
        return None

def extract_first_consumption(row, df):
    try:
        if 'Verbrauch' in df.columns:
            verbrauch = row['Verbrauch']
            if pd.notnull(verbrauch):
                match = re.search(r'(\d{1,2},\d)\s*l/100km', verbrauch)
                if match:
                    return float(match.group(1).replace(',', '.'))
        if 'Energieverbrauch (komb.)2' in df.columns:
            energieverbrauch = row['Energieverbrauch (komb.)2']
            if pd.notnull(energieverbrauch):
                match = re.search(r'(\d{1,2},\d)\s*l/100km', energieverbrauch)
                if match:
                    return float(match.group(1).replace(',', '.'))
        return None
    except Exception as e:
        logging.error(f"Error in extract_first_consumption: {e}")
        return None

def convert_erstzulassung_to_age(date_str):
    try:
        # Check if the input is empty
        if not date_str:
            raise ValueError("The date string is empty.")
        
        # Ensure the input is a string
        if isinstance(date_str, float):
            date_str = str(int(date_str))
        
        # Convert MM/YYYY to a datetime object
        date_obj = datetime.strptime(date_str, "%m/%Y")
        
        # Calculate the age of the car in years
        age = (datetime.now() - date_obj).days / 365.25
        return age
    except Exception as e:
        logging.error(f"Error in convert_erstzulassung_to_age: {e}")
        return None

def shorten_url(long_url):
    try:
        response = requests.get(f'http://tinyurl.com/api-create.php?url={long_url}')
        if response.status_code == 200:
            return response.text
        else:
            # Handle error response
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        # Handle exceptions
        print(f"Exception occurred: {e}")
        return None
    
    


def preprocess_search_list(file_path):
    try:
        processed_df = preprocess_dataframe(file_path)
        if processed_df is not None:
            # Save the preprocessed DataFrame to Excel and CSV files
            excel_file_path = '1_preprocessed_search_result.xlsx'
            processed_df.to_excel(excel_file_path, index=False)
            logging.info("Preprocessed search result excel file saved")
            return excel_file_path
        return None
    except Exception as e:
        logging.error(f"Error in preprocess_search_list: {e}")
        return None

##########################################################################################################################
# file_path = "search_list_car_features_GLK.xlsx" 
# preprocess_search_list(file_path)

# file_path = "preprocessed_search_result.xlsx"
# translate_preprocessed_search_result(file_path)