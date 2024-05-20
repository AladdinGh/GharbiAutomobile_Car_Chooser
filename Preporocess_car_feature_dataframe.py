import pandas as pd
import re
import numpy as np

def preprocess_dataframe(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        ########################## Create a column for each equipment ########################
        # Split the 'Equipment' column by commas and expand it into multiple columns
        equipment_split = df['Equipment'].str.get_dummies(sep=',')
        df = pd.concat([df, equipment_split], axis=1)
        
        ########################## Remove Brutto/Netto from Price ###########################
        # Function to clean the Price column
        def clean_price(price):
            if isinstance(price, str):
                match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*€', price)
                if match:
                    return float(match.group(1).replace('.', '').replace(',', '.'))
            return None
        
        # Apply the clean_price function to the 'Price' columns
        df['Brutto Price'] = df['Brutto Price'].apply(clean_price)
        df['Netto Price'] = df['Netto Price'].apply(clean_price)
        
        ########################## Separate KW from PS ###########################
        df['KW'] = df['Leistung'].str.extract(r'(\d+)\s*kW', expand=False).astype(float)
        df['PS'] = df['Leistung'].str.extract(r'(\d+)\s*PS', expand=False).astype(float)
        
        ########################## Convert Kilometerstand to numerical ###########################
        def clean_kilometerstand(km):
            if isinstance(km, str):
                numeric_km = re.sub(r'[^\d]', '', km)
                return int(numeric_km) if numeric_km else None
            return None
        
        df['Kilometerstand'] = df['Kilometerstand'].apply(clean_kilometerstand)
        
        ########################## Extract first value from Verbrauch ###########################
        def extract_first_consumption(verbrauch):
            if isinstance(verbrauch, str):
                match = re.search(r'(\d{1,2},\d)\s*l/100km', verbrauch)
                if match:
                    return float(match.group(1).replace(',', '.'))
            return None
        
        
        # Update Kraftstoffverbrauch2 with values from Verbrauch
        df['Kraftstoffverbrauch2'] = df['Verbrauch'].apply(extract_first_consumption)
        
        ########################## Extract values from Energieverbrauch (komb.)2 ##################
        def extract_energy_consumption(energy):
            if isinstance(energy, str):
                match = re.search(r'(\d{1,2},\d)\s*l/100km', energy)
                if match:
                    return float(match.group(1).replace(',', '.'))
            return None
        
        # Update Kraftstoffverbrauch2 with values from Energieverbrauch (komb.)2 where 0
        df['Kraftstoffverbrauch2'] = df['Kraftstoffverbrauch2'].combine_first(df['Energieverbrauch (komb.)2'].apply(extract_energy_consumption))
        
        ########################## Rename and Delete Columns #############################
        df.rename(columns={'Kraftstoffverbrauch2': 'Kraftstoffverbrauch'}, inplace=True)
        df.drop(columns=['Energieverbrauch (komb.)2'], inplace=True)
        
        
        df['Kraftstoffverbrauch'] = df['Kraftstoffverbrauch'].fillna(0)
        ####################################################################################
        # Save the preprocessed DataFrame to Excel and CSV files
        excel_file_path = 'preprocessed_df.xlsx'
        df.to_excel(excel_file_path, index=False)
        csv_file_path = 'preprocessed_df.csv'
        df.to_csv(csv_file_path, index=False)
        
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
file_path = "search_list_car_features.csv"  # Replace with your file path
df = preprocess_dataframe(file_path)

if df is not None:
    print(df.iloc[1])
else:
    print("Preprocessing failed.")
