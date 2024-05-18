import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = 'output.csv'

# Load the CSV file into a DataFrame
try:
    df = pd.read_csv(file_path)
    
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")

except pd.errors.EmptyDataError:
    print(f"Error: File '{file_path}' is empty.")

except pd.errors.ParserError:
    print(f"Error: Unable to parse file '{file_path}'.")


# Print the column names
#print("Column names:")
print(df.columns.tolist())
#print (df['Einparkhilfe'])




import matplotlib.pyplot as plt
import seaborn as sns




# Histogram of car prices
plt.figure(figsize=(10, 6))
sns.histplot(df['Hubraum'], bins=20, kde=True)
plt.title('Distribution of Car Prices')
plt.xlabel('Hubraum (€)')
plt.ylabel('Frequency')
plt.show()

# # Scatter plot of mileage vs. price
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='Kilometerstand', y='Brutto Price', data=df)
# plt.title('Kilometerstand vs. Brutto Price')
# plt.xlabel('Kilometerstand')
# plt.ylabel('Brutto Price (€)')
# plt.show()

