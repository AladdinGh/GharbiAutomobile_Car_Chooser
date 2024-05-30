import pandas as pd
from tabulate import tabulate

file_path = "preprocessed_Alexander_diesel.xlsx"
translated_df = pd.read_excel(file_path)

# Select attributes for the comparative table
attributes = ['Title', 'Brutto Price', 'Kraftstoffverbrauch', 'PS', 'Erstzulassung', 'Kilometerstand']

# Sort by price
df_sorted = translated_df.sort_values(by=['Kilometerstand', 'Erstzulassung'])

# Generate and print the comparative table
print(tabulate(df_sorted[attributes], headers='keys', tablefmt='fancy_grid', showindex=False, numalign="center"))
