import logging
import pandas as pd
import re
from Preporocess_car_feature_dataframe import preprocess_search_list
from Translate_preprocessed_data_frame import translate_preprocessed_search_result

# Setup logging configuration
logging.basicConfig(filename='processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def print_report(file_path):
    try:
        # Read the data from the Excel file
        df = pd.read_excel(file_path)
        
        # Rank cars based on scores
        df_sorted = df.sort_values(by='Score', ascending=False)
        best_fit_cars = df_sorted.head(10)

        # Generate the textual report
        rapport = "### Rapport Comparatif des voitures sur mobile.de\n\n"
        rapport += f"Nous avons trouvé {len(df)} voitures correspondant à vos critères.\n"
        
        # Find the best match based on the lowest price, the least mileage, the latest construction year, and the highest number of options.
        meilleure_voiture = df_sorted.iloc[0]
        rapport += "\n"
        rapport += "##################################################################################################################\n"
        rapport += f"La meilleure correspondance économique avec le moindre kilométrage, l'année de construction la plus récente et le plus grand nombre d'options est **Voiture {meilleure_voiture.name + 1}** :\n"
        rapport += f"- Nom de l'Annonce : {meilleure_voiture['Car Title']}\n"
        rapport += f"- Kilométrage : {meilleure_voiture['Kilometerstand']} km\n"
        rapport += f"- Date de mise en circulation : {meilleure_voiture['Erstzulassung']} km\n"
        rapport += f"- Couleur : {meilleure_voiture['Farbe'] if pd.notnull(meilleure_voiture['Farbe']) else meilleure_voiture['Farbe(constructeur)']}\n"
        rapport += f"- Prix : {meilleure_voiture['Brutto Price']} EUR\n"
        rapport += f"- URL : {meilleure_voiture['URL']}\n"
        rapport += "- Les options :\n"
        for feature in df.columns:
            if feature not in ['Fahrzeughalter', 'Anzahl der Fahrzeughalter'] and feature in meilleure_voiture.index and meilleure_voiture[feature] == 1:
                rapport += f"  - {feature}\n"
        rapport += "- Description :\n"
        # Format description into paragraphs
        description = meilleure_voiture['Description']
        paragraphs = re.split(r'[\n.]', description)
        for paragraph in paragraphs:
            rapport += f" {paragraph.strip()}\n" 
        rapport += "##################################################################################################################\n"
        
        # Loop through each row in the DataFrame to generate the report for top 10 matches
        rapport += "\nLes 10 meilleures correspondances :\n"
        for i, car in best_fit_cars.iterrows():
            rapport += f"Voiture {car.name + 1} :\n"
            rapport += f"- Nom de l'Annonce : {car['Car Title']}\n"
            rapport += f"- Kilométrage : {car['Kilometerstand']} km\n"
            rapport += f"- Date de mise en circulation : {car['Erstzulassung']} km\n"
            rapport += f"- Couleur : {car['Farbe'] if pd.notnull(car['Farbe']) else car['Farbe(constructeur)']}\n"
            rapport += f"- Prix : {car['Brutto Price']} EUR\n"
            rapport += f"- URL : {car['URL']}\n"
            rapport += "- Les options :\n"
            for feature in df.columns:
                if feature not in ['Fahrzeughalter', 'Anzahl der Fahrzeughalter'] and feature in car.index and car[feature] == 1:
                    rapport += f"  - {feature}\n"
            rapport += "- Description :\n "
            # Format description into paragraphs
            description = car['Description']
            paragraphs = re.split(r'[\n.]', description)
            for paragraph in paragraphs:
                rapport += f" {paragraph.strip()}\n"   
            rapport += "##################################################################################################################\n"
            
        # Save the report to a text file
        with open("car_report_Example.txt", "w" , encoding='utf-8') as txt_file:
            txt_file.write(rapport)
        logging.info("Report saved as 'car_report_Example.txt'")
    except Exception as e:
        logging.error(f"Error in print_report: {e}")

def prepare_and_print_report():
    try:
        file_path = "search_list_car_features_GLK.xlsx" 
        preprocess_search_list(file_path)
        print("preprocessing finished")
        
        file_path = "preprocessed_search_result.xlsx"
        translate_preprocessed_search_result(file_path)
        print("translation finished")
        
        file_path = "translated_preprocessed_df.xlsx"
        print_report(file_path)
        print("report generated")
    except Exception as e:
        logging.error(f"Error in prepare_and_print_report: {e}")

prepare_and_print_report()
