import pandas as pd
import re
import numpy as np

def preprocess_dataframe(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        ########################## Create a column for each equipment ########################
        # Split the 'Equipment' column by commas and expand it into multiple columns
        if 'Equipment' in df.columns:
            equipment_split = df['Equipment'].dropna().str.split(',').apply(lambda x: [s.strip() for s in x]).str.join('|').str.get_dummies()
            df = pd.concat([df, equipment_split], axis=1)
        
        ########################## Remove Brutto/Netto from Price ###########################
        # Function to clean the Price columns
        def clean_price(price):
            if isinstance(price, str):
                match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*€', price)
                if match:
                    return float(match.group(1).replace('.', '').replace(',', '.'))
            return None
        
        # Apply the clean_price function to the 'Brutto Price' and 'Netto Price' columns
        if 'Brutto Price' in df.columns:
            df['Brutto Price'] = df['Brutto Price'].apply(clean_price)
        if 'Netto Price' in df.columns:
            df['Netto Price'] = df['Netto Price'].apply(clean_price)
        
        ########################## Separate KW from PS ###########################
        if 'Leistung' in df.columns:
            df['KW'] = df['Leistung'].str.extract(r'(\d+)\s*kW', expand=False).astype(float)
            df['PS'] = df['Leistung'].str.extract(r'(\d+)\s*PS', expand=False).astype(float)
        
        ########################## Convert Kilometerstand to numerical ###########################
        def clean_kilometerstand(km):
            if isinstance(km, str):
                numeric_km = re.sub(r'[^\d]', '', km)
                return int(numeric_km) if numeric_km else None
            return None
        
        if 'Kilometerstand' in df.columns:
            df['Kilometerstand'] = df['Kilometerstand'].apply(clean_kilometerstand)
        
        ########################## Extract first value from Verbrauch ###########################
        def extract_first_consumption(verbrauch):
            if isinstance(verbrauch, str):
                match = re.search(r'(\d{1,2},\d)\s*l/100km', verbrauch)
                if match:
                    return float(match.group(1).replace(',', '.'))
            return None
        
        if 'Verbrauch' in df.columns:
            df['Kraftstoffverbrauch'] = df['Verbrauch'].apply(extract_first_consumption)
        else:
            df['Kraftstoffverbrauch'] = np.nan
        
        ########################## Extract values from Energieverbrauch (komb.)2 ##################
        def extract_energy_consumption(energy):
            if isinstance(energy, str):
                match = re.search(r'(\d{1,2},\d)\s*kWh/100km', energy)
                if match:
                    return float(match.group(1).replace(',', '.'))
            return None
        
        if 'Energieverbrauch (komb.)2' in df.columns:
            df['Kraftstoffverbrauch'] = df['Kraftstoffverbrauch'].combine_first(df['Energieverbrauch (komb.)2'].apply(extract_energy_consumption))
        
        ########################## Fill missing values in Kraftstoffverbrauch ##################
        df['Kraftstoffverbrauch'].fillna(0, inplace=True)
        
        ########################## Rename and Delete Columns #############################
        df.drop(columns=['Energieverbrauch (komb.)2'], inplace=True, errors='ignore')
        
        ####################################################################################
        # Save the preprocessed DataFrame to Excel and CSV files
        excel_file_path = 'preprocessed_df_Alexander_diesel.xlsx'
        df.to_excel(excel_file_path, index=False)
        csv_file_path = 'preprocessed_df_Alexander_diesel.csv'
        df.to_csv(csv_file_path, index=False)
        
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
file_path = "search_list_car_features_Alexander_diesel.xlsx"  # Replace with your file path
df = preprocess_dataframe(file_path)

if df is not None:
    print(df.head())
else:
    print("Preprocessing failed.")
