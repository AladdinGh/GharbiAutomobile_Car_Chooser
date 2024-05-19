import pandas as pd
import re 



def preprocess_dataframe(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        ########################## Create a column for each equipment ########################
        # Split the 'Equipment' column by commas and expand it into multiple columns
        equipment_split = df['Equipment'].str.split(',', expand=True)
        
        # Extract unique items from all the split columns
        unique_items_list = equipment_split.stack().unique().tolist()

        # Define all possible equipment items
        all_equipment_items = unique_items_list

        # Iterate through each cell in the 'Equipment' column
        for item in all_equipment_items:
            df[item] = df['Equipment'].apply(lambda x: 'yes' if item in x.split(',') else 'no')
        
        # Drop the original 'Equipment' column
        df.drop(columns=['Equipment'], inplace=True)
        
        ########################## Remove Brutto/Netto from Price ###########################
        # Function to clean the Price column
        def clean_price(price):
            if isinstance(price, str):
                match = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2})\s*€', price)
                if match:
                    return match.group(1).replace('.', '').replace(',', '.')
                else:
                    match = re.search(r'(\d{1,3}(?:\.\d{3})*)\s*€', price)
                    if match:
                        return match.group(1).replace('.', '')
            return None
        
        # Apply the clean_price function to the 'Price' column
        df['Brutto Price'] = df['Brutto Price'].apply(clean_price)
        df['Netto Price'] = df['Netto Price'].apply(clean_price)
        
        ########################## seperate KW from PS ###########################
   
        df['KW'] = df['Leistung'].apply(lambda x: re.search(r'(\d+)\s*kW', x).group(1) if isinstance(x, str) and re.search(r'(\d+)\s*kW', x) else None)
        
        # Extract the PS value
        df['PS'] = df['Leistung'].apply(lambda x: re.search(r'(\d+)\s*PS', x).group(1) if isinstance(x, str) and re.search(r'(\d+)\s*PS', x) else None)
        
        # Drop the original 'Leistung' column
        #df.drop(columns=['Leistung'], inplace=True)
        
        
        ####################################################################################
        # Save the preprocessed DataFrame to an Excel file
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
