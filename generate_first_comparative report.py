import pandas as pd
import re
from Preporocess_car_feature_dataframe import preprocess_search_list
from Translate_preprocessed_data_frame import translate_preprocessed_search_result


def print_report(file_path):
    # Read the data from the Excel file
    df = pd.read_excel(file_path)
    
    # Convert 'Erstzulassung' to datetime format
    df['Erstzulassung'] = pd.to_datetime(df['Erstzulassung'], format='%m/%Y')
    
    # Define the number of bins for price and mileage ranges
    num_bins = 3
    
    # Calculate price ranges
    price_bins = pd.cut(df['Brutto Price'], bins=num_bins, retbins=True)[1]
    price_ranges = [(int(price_bins[i]), int(price_bins[i+1])) for i in range(len(price_bins) - 1)]
    
    # Define yearly intervals for construction year
    df['Construction Year'] = df['Erstzulassung'].dt.year
    
    min_year = df['Construction Year'].min()
    max_year = df['Construction Year'].max()
    
    # Generate bins for each year
    year_bins = range(min_year, max_year + 2)
    
    # Calculate construction year ranges (yearly intervals)
    df['Year Bin'] = pd.cut(df['Construction Year'], bins=year_bins, right=False)
    
    # Calculate mileage ranges
    mileage_bins = pd.cut(df['Kilometerstand'], bins=num_bins, retbins=True)[1]
    mileage_ranges = [(int(mileage_bins[i]), int(mileage_bins[i+1])) for i in range(len(mileage_bins) - 1)]
    
    # # Sort the DataFrame to find the top 10 best economical matches
    # df_sorted = df.sort_values(by=['Brutto Price', 'Kilometerstand', 'Erstzulassung'])
    # 
    
    
    # Rank cars based on scores
    df_sorted = df.sort_values(by='Score', ascending=False)

    best_fit_cars = df_sorted.head(10)


    # Generate the textual report
    rapport = "### Rapport Comparatif de Tous les Éléments dans le DataFrame Prétraité\n\n"
    rapport += f"Nous avons trouvé {len(df)} voitures correspondant à vos critères.\n"
    
    # Find the best match based on the lowest price, the least mileage, the latest construction year, and the highest number of options.
    meilleure_voiture = df_sorted.iloc[0]
    rapport += "\n"
    rapport += "##################################################################################################################\n"
    rapport += f"La meilleure correspondance économique avec le moindre kilométrage, l'année de construction la plus récente et le plus grand nombre d'options est **Voiture {meilleure_voiture.name + 1}** :\n"
    rapport += f"- Nom de l'Annonce : {meilleure_voiture['Car Title']}\n"
    rapport += f"- Kilométrage : {meilleure_voiture['Kilometerstand']} km\n"
    rapport += f"- Farbe : {meilleure_voiture['Farbe'] if pd.notnull(meilleure_voiture['Farbe']) else meilleure_voiture['Farbe(constructeur)']}\n"
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
        rapport += f"- Farbe : {car['Farbe'] if pd.notnull(car['Farbe']) else car['Farbe(constructeur)']}\n"
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
    print("report saved")


def prepare_and_print_report():
    
    file_path = "search_list_car_features_Alexander_diesel.xlsx" 
    preprocess_search_list(file_path)
    
    file_path = "preprocessed_search_result.xlsx"
    translate_preprocessed_search_result(file_path)
    
    file_path = "translated_preprocessed_df.xlsx"
    print_report(file_path)


prepare_and_print_report()                                                                                                                
