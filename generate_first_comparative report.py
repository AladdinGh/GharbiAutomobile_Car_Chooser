import pandas as pd


# Read preprocessed data
file_path = "translated_preprocessed_df.xlsx"
df = pd.read_excel(file_path)

# Convert 'Erstzulassung' to datetime format
df['Erstzulassung'] = pd.to_datetime(df['Erstzulassung'], format='%m/%Y')

# Define the number of bins for price and mileage ranges
num_bins = 3

# Calculate price ranges
price_bins = pd.cut(df['Brutto Price'], bins=num_bins, retbins=True)[1]
price_ranges = [(int(price_bins[i]), int(price_bins[i+1])) for i in range(len(price_bins)-1)]

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
mileage_ranges = [(int(mileage_bins[i]), int(mileage_bins[i+1])) for i in range(len(mileage_bins)-1)]

# Define a list of attribute columns
feature_columns = ['Abstandstempomat', 'Abstandswarner', 'Adaptives Kurvenlicht', 'Alarmanlage', 'Allradantrieb',
                   'Allwetterreifen', 'Ambiente-Beleuchtung', 'Anhängerkupplung abnehmbar', 'Anhängerkupplung fest',
                   'Anhängerkupplung-Vorbereitung', 'Armlehne', 'Beheizbare Frontscheibe', 'Beheizbares Lenkrad',
                   'Berganfahrassistent', 'Bi-Xenon Scheinwerfer', 'Blendfreies Fernlicht', 'Bluetooth',
                   'Bordcomputer', 'CD-Spieler', 'Dachreling', 'ESP', 'Elektr. Fensterheber', 'Elektr. Heckklappe',
                   'Elektr. Seitenspiegel', 'Elektr. Sitzeinstellung', 'Elektr. Wegfahrsperre', 'Fernlichtassistent',
                   'Freisprecheinrichtung', 'Garantie', 'Gepäckraumabtrennung', 'Geschwindigkeitsbegrenzer',
                   'Innenspiegel autom. abblendend', 'Isofix', 'Isofix Beifahrersitz', 'Kurvenlicht',
                   'LED-Scheinwerfer', 'LED-Tagfahrlicht', 'Lederlenkrad', 'Leichtmetallfelgen', 'Lichtsensor',
                   'Lordosenstütze', 'Multi-CD-Wechsler', 'Multifunktionslenkrad', 'Musikstreaming integriert',
                   'Müdigkeitswarner', 'Navigationssystem', 'Nebelscheinwerfer', 'Nichtraucher-Fahrzeug',
                   'Notbremsassistent', 'Notrad', 'Notrufsystem', 'Pannenkit', 'Panorama-Dach', 'Partikelfilter',
                   'Radio DAB', 'Raucherpaket', 'Regensensor', 'Reifendruckkontrolle', 'Reserverad', 'Schaltwippen',
                   'Scheckheftgepflegt', 'Scheinwerferreinigung', 'Schiebedach', 'Schlüssellose Zentralverriegelung',
                   'Servolenkung', 'Sitzheizung', 'Sitzheizung hinten', 'Skisack', 'Sommerreifen', 'Soundsystem',
                   'Sportfahrwerk', 'Sportpaket', 'Sportsitze', 'Sprachsteuerung', 'Spurhalteassistent',
                   'Standheizung', 'Start/Stopp-Automatik', 'TV', 'Tagfahrlicht', 'Taxi', 'Tempomat',
                   'Totwinkel-Assistent', 'Touchscreen', 'Traktionskontrolle', 'Tuner/Radio', 'USB',
                   'Verkehrszeichenerkennung', 'WLAN / Wifi Hotspot', 'Winterpaket', 'Winterreifen', 'Xenonscheinwerfer',
                   'Zentralverriegelung', 'ABS']

# Filter out feature columns that are not present in the DataFrame
feature_columns = [col for col in feature_columns if col in df.columns]

# Translation dictionary
feature_columns_translation = {
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
}

# Filter feature_columns_translation to only include columns present in the DataFrame
feature_columns_translation = {key: value for key, value in feature_columns_translation.items() if key in df.columns}

# Calculate the number of attributes for each car
df['Feature Count'] = df[feature_columns].sum(axis=1)

# # Calculate the distribution of cars based on price range
# price_distribution = []
# for price_range in price_ranges:
#     count = df[(df['Brutto Price'] >= price_range[0]) & (df['Brutto Price'] < price_range[1])].shape[0]
#     filtered_cars = df[(df['Brutto Price'] >= price_range[0]) & (df['Brutto Price'] < price_range[1])]
#     price_distribution.append((price_range, count, filtered_cars))
    


# # Calculate the distribution of cars based on construction year
# year_distribution = df['Year Bin'].value_counts().sort_index()

# # Calculate the distribution of cars based on mileage
# mileage_distribution = []
# for mileage_range in mileage_ranges:
#     count = df[(df['Kilometerstand'] >= mileage_range[0]) & (df['Kilometerstand'] < mileage_range[1])].shape[0]
#     mileage_distribution.append((mileage_range, count))


# Sort the DataFrame to find the top 10 best economical matches
df_sorted = df.sort_values(by=['Brutto Price', 'Kilometerstand', 'Erstzulassung', 'Feature Count'])
best_fit_cars = df_sorted.head(10)

# Generate the textual report
rapport = "### Rapport Comparatif de Tous les Éléments dans le DataFrame Prétraité\n\n"

# for index, row in df.iterrows():
#     rapport += f"#### Voiture {index + 1}\n"
#     rapport += f"- **Date de Première Immatriculation**: {row['Erstzulassung'].strftime('%m/%Y')}\n"
#     rapport += f"- **Prix Brut**: {row['Brutto Price']} EUR\n"
#     rapport += f"- **URL : {row['URL']}\n"
#     rapport += f"- **Kilométrage**: {row['Kilometerstand']} km\n"
#     rapport += f"- **Couleur**: {row['Farbe']}\n"
#     rapport += f"- **Nom de la Couleur (Fabricant)**: {row['Farbe (Hersteller)']}\n"
#     rapport += f"- **Nombre d'Attributs**: {row['Feature Count']} options\n"
#     rapport += "---\n\n"

rapport += f"Nous avons trouvé {len(df)} voitures correspondant à vos critères.\n"
# rapport += "Distribution des voitures selon la gamme de prix\n\n"

# for price_range, count, filtered_cars in price_distribution:
#     rapport += f"Nous avons trouvé {count} voitures dans la gamme de prix de {price_range[0]} à {price_range[1]} Euros.\n"
#     # for index, row in filtered_cars.iterrows():
#     #     rapport += f"- **Voiture {index + 1}**: {row['URL'][:10]})\n"
# rapport += "\n"


# rapport += "Distribution des voitures selon l'année de construction\n\n"
# for interval, count in year_distribution.items():
#     rapport += f"Nous avons trouvé {count} voitures dans la gamme d'années de construction de {interval.left} à {interval.right - 1}.\n"
# rapport += "\n"

# rapport += "Distribution des voitures selon le kilométrage\n\n"
# for mileage_range, count in mileage_distribution:
#     rapport += f"Nous avons trouvé {count} voitures dans la gamme de kilométrage de {mileage_range[0]} à {mileage_range[1]} km.\n"
# rapport += "\n"

# Find the best match based on the lowest price, the least mileage, the latest construction year, and the highest number of options.
meilleure_voiture = df_sorted.iloc[0]
rapport += "\n"
rapport += "##################################################################################################################\n"
rapport += f"La meilleure correspondance économique avec le moindre kilométrage, l'année de construction la plus récente et le plus grand nombre d'options est **Voiture {meilleure_voiture.name + 1}** :\n"
rapport += f"- Nom de l'Annonce : {meilleure_voiture['Car Title']}\n"
rapport += f"- Kilométrage : {meilleure_voiture['Kilometerstand']} km\n"
rapport += f"- Couleur : {meilleure_voiture['Farbe'] if pd.notnull(meilleure_voiture['Farbe']) else meilleure_voiture['Farbe (Hersteller)']}\n"
rapport += f"- Prix : {meilleure_voiture['Brutto Price']} EUR\n"
rapport += f"- URL : {meilleure_voiture['URL']}\n"
rapport += "- Les options :\n"
for feature in feature_columns:
    if feature in meilleure_voiture.index and meilleure_voiture[feature] == 1:
        rapport += f"  - {feature_columns_translation[feature]}\n"
rapport += "##################################################################################################################\n"
# Loop through each row in the DataFrame to generate the report
rapport += "\nLes 10 meilleures correspondances :\n"
for i, car in best_fit_cars.iterrows():
    rapport += f"Voiture {car.name + 1} :\n"
    rapport += f"- Nom de l'Annonce : {car['Car Title']}\n"
    rapport += f"- Kilométrage : {car['Kilometerstand']} km\n"
    rapport += f"- Couleur : {car['Farbe'] if pd.notnull(car['Farbe']) else car['Farbe (Hersteller)']}\n"
    rapport += f"- Prix : {car['Brutto Price']} EUR\n"
    rapport += f"- URL : {car['URL']}\n"
    rapport += "- Les options :\n"
    for feature in feature_columns:
        if feature in car.index and car[feature] == 1:
            rapport += f"  - {feature_columns_translation[feature]}\n"
    rapport += "\n"

print(rapport)
# Save the report to a text file
with open("car_report_Alexander.txt", "w") as txt_file:
    txt_file.write(rapport)

print("Text file saved")