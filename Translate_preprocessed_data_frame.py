from googletrans import Translator
import pandas as pd
 

def translate_df(file_path, index=False):   
    # Load dataframe from Excel file
    preprocessed_df = pd.read_excel(file_path)
    
    # Define the columns to be translated
    columns_to_translate = ['Getriebe', 'Kraftstoffart', 'Fahrzeugzustand', 'Kategorie', 'Klimatisierung', 'Einparkhilfe', 'Airbags', 'Farbe (Hersteller)', 'Farbe', 'Innenausstattung', 'Description']
    
    # Initialize the Translator
    translator = Translator()
    
    # Function to translate a single text
    def translate_text(text):
        try:
            translation = translator.translate(text, dest='fr').text
            return translation
        except Exception as e:
            print("Error occurred during translation:", e)
            return text  # Return original text if translation fails
    
    # Translate column headers
    translated_columns = {col: translate_text(col) for col in columns_to_translate}
    
    # Apply translated column headers to DataFrame
    # preprocessed_df.rename(columns=translated_columns, inplace=True)
    # print (preprocessed_df.columns)
    # Function to translate values in selected columns
    def translate_column_values(column):
        try:
            translated_values = [translate_text(value) for value in preprocessed_df[column]]
            return translated_values
        except Exception as e:
            print(f"Error occurred during translation of column {column}:", e)
            return preprocessed_df[column]  # Return original values if translation fails
    
    # Translate values in selected columns
    for col in columns_to_translate:
        preprocessed_df[col] = translate_column_values(col)
    
    return(preprocessed_df)
    
    
# Save final dataframe to Excel file
file_path = "preprocessed_df_GLK.xlsx"
preprocessed_df = translate_df(file_path).to_excel("translated_preprocessed_df.xlsx", index=False)

print("Translated dataframe saved as 'translated_preprocessed_df.xlsx'")
