import pandas as pd
from tabulate import tabulate

# Sample car attributes DataFrame
data = {
    'Brand': ['Toyota', 'Honda', 'Ford', 'Chevrolet'],
    'Model': ['Camry', 'Civic', 'F-150', 'Silverado'],
    'Price': [25000, 23000, 35000, 40000],
    'Fuel Efficiency (mpg)': [33, 36, 20, 18],
    'Horsepower': [203, 158, 290, 355]
}





file_path = "translated_preprocessed_df.xlsx"
translated_df = pd.read_excel(file_path)


# Limit "Brand" to the first two words
translated_df['Car Title'] = translated_df['Car Title'].str.split().str[:3].str.join(' ')


# Select attributes for the comparative table
attributes = ['Car Title', 'Brutto Price', 'Kraftstoffverbrauch', 'PS']

# Generate and print the comparative table
print(tabulate(translated_df[attributes], headers='keys', tablefmt='grid'))
