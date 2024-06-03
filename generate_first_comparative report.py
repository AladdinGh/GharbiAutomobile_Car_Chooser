import logging
import pandas as pd
import re
from docx import Document
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

        # Create a Word document
        doc = Document()

        # Generate the textual report
        doc.add_heading('Rapport Comparatif de Tous les Éléments dans le DataFrame Prétraité', level=1)
        doc.add_paragraph(f"Nous avons trouvé {len(df)} voitures correspondant à vos critères.")
        doc.add_paragraph("##################################################################################################################")
        # # Find the best match based on the lowest price, the least mileage, the latest construction year, and the highest number of options.
        # meilleure_voiture = df_sorted.iloc[0]
        # doc.add_paragraph("\n")
        # doc.add_paragraph("##################################################################################################################")
        # doc.add_paragraph(f"La meilleure correspondance économique avec le moindre kilométrage, l'année de construction la plus récente et le plus grand nombre d'options est Voiture {meilleure_voiture.name + 1} :")
        # doc.add_paragraph(f"Nom de l'Annonce : {meilleure_voiture['Car Title']}")
        # doc.add_paragraph(f"Kilométrage : {meilleure_voiture['Kilometerstand']} km")
        # doc.add_paragraph(f"Date de mise en circulation : {meilleure_voiture['Erstzulassung']} km\n")
        # doc.add_paragraph(f"Couleur : {meilleure_voiture['Farbe'] if pd.notnull(meilleure_voiture['Farbe']) else meilleure_voiture['Farbe(constructeur)']}")
        # doc.add_paragraph(f"Prix : {meilleure_voiture['Brutto Price']} EUR")
        # doc.add_paragraph(f"URL : {meilleure_voiture['URL']}")
        # doc.add_paragraph("Les options :")
        # for feature in df.columns:
        #     if feature not in ['Fahrzeughalter', 'Anzahl der Fahrzeughalter'] and feature in meilleure_voiture.index and meilleure_voiture[feature] == 1:
        #         doc.add_paragraph(f"  - {feature}")
        # doc.add_paragraph("Description :")
        # # Format description into paragraphs
        # description = meilleure_voiture['Description']
        # paragraphs = re.split(r'[\n.]', description)
        # for paragraph in paragraphs:
        #     doc.add_paragraph(f" {paragraph.strip()}")
        # doc.add_paragraph("##################################################################################################################")
        
        # Loop through each row in the DataFrame to generate the report for top 10 matches
        doc.add_paragraph("\nLes 10 meilleures correspondances :")
        for i, car in best_fit_cars.iterrows():
            #doc.add_paragraph(f"Voiture {i} :")
            doc.add_paragraph(f"Nom de l'Annonce : {car['Car Title']}")
            doc.add_paragraph(f"Kilométrage : {car['Kilometerstand']} km")
            doc.add_paragraph(f"Date de mise en circulation : {car['Erstzulassung']} km")
            doc.add_paragraph(f"Couleur : {car['Farbe'] if pd.notnull(car['Farbe']) else car['Farbe(constructeur)']}")
            doc.add_paragraph(f"Prix : {car['Brutto Price']} EUR")
            doc.add_paragraph(f"URL : {car['URL']}")
            doc.add_paragraph("Les options :")
            for feature in df.columns:
                if feature not in ['Fahrzeughalter', 'Anzahl der Fahrzeughalter'] and feature in car.index and car[feature] == 1:
                    doc.add_paragraph(f"  - {feature}")
            doc.add_paragraph("Description :")
            # Format description into paragraphs
            description = car['Description']
            paragraphs = re.split(r'[\n.]', description)
            for paragraph in paragraphs:
                doc.add_paragraph(f" {paragraph.strip()}")
            doc.add_paragraph("##################################################################################################################")
            
        # Save the report to a Word document
        doc.save("car_report_Example.docx")
        logging.info("Report saved as 'car_report_Example.docx'")
    except Exception as e:
        logging.error(f"Error in print_report: {e}")

def prepare_and_print_report():
    try:
        # file_path = "search_list_car_features_Alexander_diesel.xlsx" 
        # preprocess_search_list(file_path)
        
        # file_path = "preprocessed_search_result.xlsx"
        # translate_preprocessed_search_result(file_path)
        
        file_path = "translated_preprocessed_df.xlsx"
        print_report(file_path)
    except Exception as e:
        logging.error(f"Error in prepare_and_print_report: {e}")

prepare_and_print_report()
