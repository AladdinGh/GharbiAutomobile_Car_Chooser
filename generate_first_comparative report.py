import pandas as pd

# Read the preprocessed DataFrame
file_path = "preprocessed_df.csv"  # Replace with your preprocessed DataFrame file path
df = pd.read_csv(file_path)

# Convert 'Erstzulassung' to datetime format
df['Erstzulassung'] = pd.to_datetime(df['Erstzulassung'], format='%m/%Y')

# Define the number of bins for price ranges and mileage
num_bins = 3

# Calculate price ranges
price_bins = pd.cut(df['Brutto Price'], bins=num_bins, retbins=True)[1]
price_ranges = [(int(price_bins[i]), int(price_bins[i+1])) for i in range(len(price_bins)-1)]

# Define yearly intervals for construction year
df['Construction Year'] = df['Erstzulassung'].dt.year

min_year = df['Construction Year'].min()
max_year = df['Construction Year'].max()

# Generate bins for every year
year_bins = range(min_year, max_year + 2)  # +2 to include the last year properly in the interval

# Calculate construction year ranges (yearly intervals)
df['Year Bin'] = pd.cut(df['Construction Year'], bins=year_bins, right=False)

# Calculate mileage ranges
mileage_bins = pd.cut(df['Kilometerstand'], bins=num_bins, retbins=True)[1]
mileage_ranges = [(int(mileage_bins[i]), int(mileage_bins[i+1])) for i in range(len(mileage_bins)-1)]

# Define a list of feature columns
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

# Calculate the number of features for each car
df['Feature Count'] = df[feature_columns].sum(axis=1)

# Calculate car distribution based on price range
price_distribution = []
for price_range in price_ranges:
    count = df[(df['Brutto Price'] >= price_range[0]) & (df['Brutto Price'] < price_range[1])].shape[0]
    price_distribution.append((price_range, count))

# Calculate car distribution based on construction year
year_distribution = df['Year Bin'].value_counts().sort_index()

# Calculate car distribution based on mileage
mileage_distribution = []
for mileage_range in mileage_ranges:
    count = df[(df['Kilometerstand'] >= mileage_range[0]) & (df['Kilometerstand'] < mileage_range[1])].shape[0]
    mileage_distribution.append((mileage_range, count))

# Sort the DataFrame to find the top 10 best cost-efficient fits
df_sorted = df.sort_values(by=['Brutto Price', 'Kilometerstand', 'Erstzulassung', 'Feature Count'])
best_fit_cars = df_sorted.head(10)

# Generate the textual report
report = "### Comparative Report of All Elements in the Preprocessed DataFrame\n\n"

for index, row in df.iterrows():
    report += f"#### Car {index + 1}\n"
    report += f"- **Erstzulassung (First Registration Date)**: {row['Erstzulassung'].strftime('%m/%Y')}\n"
    report += f"- **Brutto Price**: {row['Brutto Price']} EUR\n"
    report += f"- **Kilometerstand (Mileage)**: {row['Kilometerstand']} km\n"
    report += f"- **Farbe (Color)**: {row['Farbe']}\n"
    report += f"- **Farbe (Hersteller) (Manufacturer Color Name)**: {row['Farbe (Hersteller)']}\n"
    report += f"- **Feature Count**: {row['Feature Count']} attributes\n"
    report += "---\n\n"

report += f"We found {len(df)} cars satisfying your criteria.\n\n"

report += "Car distribution"
report += " depending on Price range\n\n"
for price_range, count in price_distribution:
    report += f"We found {count} cars from the Price range of {price_range[0]} to {price_range[1]} Euros.\n"
report += "\n"

report += "Car distribution depending on construction year\n\n"
for interval, count in year_distribution.items():
    report += f"We found {count} cars from the construction year range of {interval.left} to {interval.right - 1}.\n"
report += "\n"

report += "Car distribution depending on Mileage\n\n"
for mileage_range, count in mileage_distribution:
    report += f"We found {count} cars from the mileage range of {mileage_range[0]} to {mileage_range[1]} km.\n"
report += "\n"

# Find the best fit based on the lowest price, least mileage, latest construction year, and most number of options
best_fit_car = df_sorted.iloc[0]
report += f"The best cost-efficient fit with the least mileage, latest construction year, and most options is **Car {best_fit_car.name + 1}**:\n"
report += f"- Listing Name: {best_fit_car['Car Title']}\n"
report += f"- Mileage: {best_fit_car['Kilometerstand']} km\n"
report += f"- Color: {best_fit_car['Farbe'] if pd.notnull(best_fit_car['Farbe']) else best_fit_car['Farbe (Hersteller)']}\n"
report += f"- Price: {best_fit_car['Brutto Price']} EUR\n"
report += f"- URL: {best_fit_car['URL']}\n"
report += "- Features:\n"
for feature in feature_columns:
    if best_fit_car[feature] == 1:
        report += f"  - {feature}\n"

# List the top 10 best fits
report += "\nTop 10 Best Fits:\n"
for i, car in best_fit_cars.iterrows():
    report += f"{i+1}. Car {car.name + 1}:\n"
    report += f"- Listing Name: {car['Car Title']}\n"
    report += f"- Mileage: {car['Kilometerstand']} km\n"
    report += f"- Color: {car['Farbe'] if pd.notnull(car['Farbe']) else car['Farbe (Hersteller)']}\n"
    report += f"- Price: {car['Brutto Price']} EUR\n"
    report += f"- URL: {car['URL']}\n"
    report += "- Features:\n"
    for feature in feature_columns:
        if car[feature] == 1:
            report += f"  - {feature}\n"
    report += "\n"

print(report)
