import pandas as pd
import re
import numpy as np
import logging

# Setup logging configuration
logging.basicConfig(filename='processing.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_dataframe(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Create a Title column with the first three words of the Car Title
        df['Title'] = df['Car Title'].str.split().str[:3].str.join(' ')
        
        # Create a column for each equipment
        if 'Equipment' in df.columns:
            equipment_split = df['Equipment'].dropna().str.split(',').apply(lambda x: [s.strip() for s in x]).str.join('|').str.get_dummies()
            df = pd.concat([df, equipment_split], axis=1)
        
        # Remove Brutto/Netto from Price
        if 'Brutto Price' in df.columns:
            df['Brutto Price'] = df['Brutto Price'].apply(clean_price)
        if 'Netto Price' in df.columns:
            df['Netto Price'] = df['Netto Price'].apply(clean_price)
        
        # Separate KW from PS
        if 'Leistung' in df.columns:
            df['KW'] = df['Leistung'].str.extract(r'(\d+)\s*kW', expand=False).astype(float)
            df['PS'] = df['Leistung'].str.extract(r'(\d+)\s*PS', expand=False).astype(float)
        
        # Convert Kilometerstand to numerical
        if 'Kilometerstand' in df.columns:
            df['Kilometerstand'] = df['Kilometerstand'].apply(clean_kilometerstand)
        
        # Process Verbrauch and Energieverbrauch (komb.)2
        if 'Verbrauch' in df.columns or 'Energieverbrauch (komb.)2' in df.columns:
            df['Kraftstoffverbrauch'] = df.apply(lambda row: extract_first_consumption(row, df), axis=1)
        average_consumption = df['Kraftstoffverbrauch'].mean()
        df['Kraftstoffverbrauch'].fillna(average_consumption, inplace=True)
        average_consumption = df['Kraftstoffverbrauch'].mean()
        df['Kraftstoffverbrauch'].fillna(average_consumption, inplace=True)
        # Drop the Energieverbrauch (komb.)2 column
        df.drop(columns=['Energieverbrauch (komb.)2'], inplace=True, errors='ignore')
        
        # Update Farbe column
        if 'Farbe (Hersteller)' in df.columns:
            df['Farbe'] = df['Farbe'].fillna(df['Farbe (Hersteller)'])
            df.drop(columns=['Farbe (Hersteller)'], inplace=True, errors='ignore')
        
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

def normalize(series, invert=False):
    try:
        normalized = (series - series.min()) / (series.max() - series.min())
        return 1 - normalized if invert else normalized
    except Exception as e:
        logging.error(f"Error in normalize: {e}")
        return series

def assign_scores(processed_df):
    try:
        weights = {
        'Brutto Price': 0.1,
        'Kilometerstand': 0.15,
        'Erstzulassung': 0.2,
        'Leistung': 0.05,
        'Getriebe': 0.05,
        'Fahrzeughalter': 0.03,
        'Kraftstoffart': 0.02,
        'Fahrzeugzustand': 0.03,
        'Kategorie': 0.02,
        'Herkunft': 0.02,
        'Hubraum': 0.03,
        'Antriebsart': 0.02,
        'Anzahl Sitzplätze': 0.02,
        'Anzahl der Türen': 0.02,
        'Schadstoffklasse': 0.02,
        'Umweltplakette': 0.02,
        'Anzahl der Fahrzeughalter': 0.01,
        'HU': 0.01,
        'Klimatisierung': 0.02,
        'Einparkhilfe': 0.01,
        'Airbags': 0.02,
        'Farbe': 0.01,
        'Innenausstattung': 0.01,
        'ABS': 0.01,
        'Abstandstempomat': 0.01,
        'Abstandswarner': 0.01,
        'Adaptives Kurvenlicht': 0.01,
        'Alarmanlage': 0.01,
        'Allradantrieb': 0.01,
        'Allwetterreifen': 0.01,
        'Ambiente-Beleuchtung': 0.01,
        'Anhängerkupplung abnehmbar': 0.01,
        'Anhängerkupplung fest': 0.01,
        'Anhängerkupplung-Vorbereitung': 0.01,
        'Armlehne': 0.01,
        'Beheizbare Frontscheibe': 0.01,
        'Beheizbares Lenkrad': 0.01,
        'Berganfahrassistent': 0.01,
        'Bi-Xenon Scheinwerfer': 0.01,
        'Blendfreies Fernlicht': 0.01,
        'Bluetooth': 0.01,
        'Bordcomputer': 0.01,
        'CD-Spieler': 0.01,
        'Dachreling': 0.01,
        'ESP': 0.01,
        'Elektr. Fensterheber': 0.01,
        'Elektr. Heckklappe': 0.01,
        'Elektr. Seitenspiegel': 0.01,
        'Elektr. Sitzeinstellung': 0.01,
        'Elektr. Wegfahrsperre': 0.01,
        'Fernlichtassistent': 0.01,
        'Freisprecheinrichtung': 0.01,
        'Gepäckraumabtrennung': 0.01,
        'Geschwindigkeitsbegrenzer': 0.01,
        'Innenspiegel autom. abblendend': 0.01,
        'Isofix': 0.01,
        'Kurvenlicht': 0.01,
        'LED-Scheinwerfer': 0.01,
        'LED-Tagfahrlicht': 0.01,
        'Lederlenkrad': 0.01,
        'Leichtmetallfelgen': 0.01,
        'Lichtsensor': 0.01,
        'Lordosenstütze': 0.01,
        'Multi-CD-Wechsler': 0.01,
        'Multifunktionslenkrad': 0.01,
        'Musikstreaming integriert': 0.01,
        'Müdigkeitswarner': 0.01,
        'Navigationssystem': 0.01,
        'Nebelscheinwerfer': 0.01,
        'Nichtraucher-Fahrzeug': 0.01,
        'Notbremsassistent': 0.01,
        'Notrad': 0.01,
        'Notrufsystem': 0.01,
        'Pannenkit': 0.01,
        'Panorama-Dach': 0.01,
        'Partikelfilter': 0.01,
        'Radio DAB': 0.01,
        'Raucherpaket': 0.01,
        'Regensensor': 0.01,
        'Reifendruckkontrolle': 0.01,
        'Reserverad': 0.01,
        'Schaltwippen': 0.01,
        'Scheckheftgepflegt': 0.01,
        'Scheinwerferreinigung': 0.01,
        'Schiebedach': 0.01,
        'Schlüssellose Zentralverriegelung': 0.01,
        'Servolenkung': 0.01,
        'Sitzheizung': 0.01,
        'Sitzheizung hinten': 0.01,
        'Skisack': 0.01,
        'Sommerreifen': 0.01,
        'Soundsystem': 0.01,
        'Sportfahrwerk': 0.01,
        'Sportpaket': 0.01,
        'Sportsitze': 0.01,
        'Sprachsteuerung': 0.01,
        'Spurhalteassistent': 0.01,
        'Standheizung': 0.01,
        'Start/Stopp-Automatik': 0.01,
        'TV': 0.01,
        'Tagfahrlicht': 0.01,
        'Taxi': 0.01,
        'Tempomat': 0.01,
        'Totwinkel-Assistent': 0.01,
        'Touchscreen': 0.01,
        'Traktionskontrolle': 0.01,
        'Tuner/Radio': 0.01,
        'USB': 0.01,
        'Verkehrszeichenerkennung': 0.01,
        'WLAN / Wifi Hotspot': 0.01,
        'Winterpaket': 0.01,
        'Winterreifen': 0.01,
        'Xenonscheinwerfer': 0.01,
        'Zentralverriegelung': 0.01,
        'KW': 0.01,
        'PS': 0.01,
        'Kraftstoffverbrauch': 0.01,
        }
        
        # Copy the original dataframe
        df_normalized = processed_df.copy()
        
        # Normalize and invert price and mileage
        df_normalized['Brutto Price'] = normalize(processed_df['Brutto Price'], invert=True)
        df_normalized['Kilometerstand'] = normalize(processed_df['Kilometerstand'], invert=True)
        
        # Normalize fuel efficiency and horsepower
        df_normalized['Kraftstoffverbrauch'] = normalize(processed_df['Kraftstoffverbrauch'])
        df_normalized['PS'] = normalize(processed_df['PS'])
        
        # Calculate scores
        df_normalized['Score'] = (
            df_normalized['Brutto Price'] * weights['Brutto Price'] +
            df_normalized['Kilometerstand'] * weights['Kilometerstand'] +
            df_normalized['Kraftstoffverbrauch'] * weights['Kraftstoffverbrauch'] +
            df_normalized['PS'] * weights['PS']
        )
        
        # Copy the Score column back to the original dataframe
        processed_df['Score'] = df_normalized['Score']
        
        # Delete the normalized dataframe
        del df_normalized
        
        return processed_df
    except Exception as e:
        logging.error(f"Error in assign_scores: {e}")
        return None

def preprocess_search_list(file_path):
    try:
        processed_df = preprocess_dataframe(file_path)
        if processed_df is not None:
            processed_df = assign_scores(processed_df)
            if processed_df is not None:
                # Save the preprocessed DataFrame to Excel and CSV files
                excel_file_path = 'preprocessed_search_result.xlsx'
                processed_df.to_excel(excel_file_path, index=False)
                logging.info("Preprocessed search result excel file saved")
                return excel_file_path
        return None
    except Exception as e:
        logging.error(f"Error in preprocess_search_list: {e}")
        return None

       

file_path = "search_list_car_features_Alexander_diesel.xlsx" 
preprocess_search_list(file_path)
