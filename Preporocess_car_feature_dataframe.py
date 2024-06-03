import pandas as pd
import re
import numpy as np
import logging
from datetime import datetime

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
        # Convert MM/YYYY to a datetime object
        date_obj = datetime.strptime(date_str, "%m/%Y")
        # Calculate the age of the car in years
        age = (datetime.now() - date_obj).days / 365.25
        return age
    except Exception as e:
        logging.error(f"Error in convert_erstzulassung_to_age: {e}")
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
        # Weights for scoring
        weights = {
            'Brutto Price': 0.5,
            'Erstzulassung_years': 0.5,
        }
        
        # Normalize columns
        df_normalized = processed_df.copy()
        # use invert = True : the higher the normalized value (1) the lower the price for example
        df_normalized['Brutto Price'] = normalize(processed_df['Brutto Price'], invert=True)
        df_normalized['Erstzulassung_years'] = normalize(processed_df['Erstzulassung_years'], invert=True)
        
        # Calculate scores
        df_normalized['Score'] = (
            df_normalized['Brutto Price'] * weights['Brutto Price'] +
            df_normalized['Erstzulassung_years'] * weights['Erstzulassung_years']
        )
        
        # Copy the Score column back to the original dataframe
        processed_df['Score'] = df_normalized['Score']
        
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

# # # Call the preprocess_search_list function
file_path = "search_list_car_features_GLK.xlsx" 
preprocess_search_list(file_path)
