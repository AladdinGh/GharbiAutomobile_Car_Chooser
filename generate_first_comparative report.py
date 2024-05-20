import pandas as pd
from Display import plot_cars_by_month_and_year

# Read the preprocessed DataFrame
file_path = "preprocessed_df.csv"  # Replace with your preprocessed DataFrame file path
df = pd.read_csv(file_path)

# Helper function to count the number of non-null attributes
def count_non_null_attributes(row):
    return row.notnull().sum()

# Calculate non-null attribute counts
df['Feature Count'] = df.apply(count_non_null_attributes, axis=1)

# Find the car with the highest and lowest price
max_price_car = df.loc[df['Brutto Price'].idxmax()]
min_price_car = df.loc[df['Brutto Price'].idxmin()]

# Find the car with the highest and lowest mileage
max_mileage_car = df.loc[df['Kilometerstand'].idxmax()]
min_mileage_car = df.loc[df['Kilometerstand'].idxmin()]

# Find the car with the most and least features
most_features_car = df.loc[df['Feature Count'].idxmax()]
least_features_car = df.loc[df['Feature Count'].idxmin()]

# Find the best fit based on the lowest price
best_fit_car = min_price_car

# Generate the textual report
report = "### Comparative Report of All Elements in the Preprocessed DataFrame\n\n"

for index, row in df.iterrows():
    report += f"#### Car {index + 1}\n"
    report += f"- **Erstzulassung (First Registration Date)**: {row['Erstzulassung']}\n"
    report += f"- **Brutto Price**: {row['Brutto Price']} EUR\n"
    report += f"- **Kilometerstand (Mileage)**: {row['Kilometerstand']} km\n"
    report += f"- **Farbe (Color)**: {row['Farbe']}\n"
    report += f"- **Farbe (Hersteller) (Manufacturer Color Name)**: {row['Farbe (Hersteller)']}\n"
    report += f"- **Feature Count**: {row['Feature Count']} attributes\n"
    report += "---\n\n"

report += f"### Best Fit\n\n"
report += f"The best fit given a highest priority of the price is **Car {df.index.get_loc(min_price_car.name) + 1}** due to its lowest price of {min_price_car['Brutto Price']} EUR.\n"
report += f"- URL: {min_price_car['URL']}\n"

print(report)

# Plot cars by month and year
#plot_cars_by_month_and_year(file_path)
