import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import tkinter as tk
import webbrowser

# Read the preprocessed DataFrame
file_path = "preprocessed_df.csv"  # Replace with your preprocessed DataFrame file path
df = pd.read_csv(file_path)

# Extract month and year from the 'Erstzulassung' column
df['Erstzulassung'] = pd.to_datetime(df['Erstzulassung']).dt.to_period('M')
df['Month'] = df['Erstzulassung'].dt.month
df['Year'] = df['Erstzulassung'].dt.year

# Function to fill missing values in 'Farbe' with values from 'Farbe (Hersteller)' if available
def fill_missing_color(row):
    if pd.isnull(row['Farbe']):
        return row['Farbe (Hersteller)']
    return row['Farbe']

# Fill missing colors
df['Farbe'] = df.apply(fill_missing_color, axis=1)

# Group by month and year and count the number of cars
car_count_by_month_year = df.groupby(['Year', 'Month']).size().reset_index(name='Car Count')

# Plot the results
plt.figure(figsize=(15, 3))  # Adjust vertical space here

# Create an array of months and years
months_years = [(y, m) for y in car_count_by_month_year['Year'].unique() for m in range(1, 13)]

# Plot circles for each month
for i, (year, month) in enumerate(months_years):
    filtered_row = car_count_by_month_year[(car_count_by_month_year['Year'] == year) & (car_count_by_month_year['Month'] == month)]
    if not filtered_row.empty:
        car_count = filtered_row['Car Count'].iloc[0]
        plt.scatter(i, 0, s=car_count * 500, alpha=0.5)
        plt.text(i, 0, car_count, ha='center', va='center', color='white')

# Set x-axis ticks and labels
plt.xticks(range(len(months_years)), [f"{calendar.month_abbr[month]} {year}" for year, month in months_years], rotation=45, ha='right')

# Hide y-axis ticks and labels
plt.yticks([])

# Set labels and title
plt.xlabel('Month and Year')
plt.title('Number of Cars by Month and Year of First Registration')

plt.grid(axis='x')
plt.tight_layout()

# Function to open URL in Microsoft Edge
def open_url_in_edge(url):
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Microsoft//Edge//Application//msedge.exe"))
    webbrowser.get('edge').open(url)

# Function to display car URLs and basic features for selected month and year
def on_click(event):
    if event.button == 1:  # Check if left mouse button clicked
        month_index = int(event.xdata)  # Get the index of the clicked point
        year, month = months_years[month_index]
        selected_cars = df[(df['Year'] == year) & (df['Month'] == month)][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)']]
        urls_and_features = selected_cars.apply(lambda row: [row['URL'][:30] + '...', row['Brutto Price'], row['Kilometerstand'], row['Farbe'], row['Farbe (Hersteller)']], axis=1)
        urls_and_features_list = urls_and_features.values.tolist()
        if urls_and_features_list:
            # Create a new popup window
            popup_window = tk.Tk()
            popup_window.title('Selected Cars Information')
            popup_window.configure(bg='#f0f0f0')  # Set background color
            
            # Create a header row with attribute names
            header = ['URL', 'Brutto Price', 'Kilometerstand', 'Farbe']
            for c, attr_name in enumerate(header):
                label = tk.Label(popup_window, text=attr_name, bg='#f0f0f0', font=('Helvetica', 10, 'bold'))
                label.grid(row=0, column=c, padx=5, pady=2, sticky="w")
            
            # Create a table to display URLs and features
            for r, row in enumerate(urls_and_features_list):
                for c, value in enumerate(row[:-1]):  # Exclude the last element (Farbe (Hersteller))
                    if c == 0:
                        label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                        label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                        label.bind('<Button-1>', lambda e, url=row[-1]: open_url_in_edge(url))  # Pass the original URL
                    else:
                        label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                        label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
            
            popup_window.mainloop()

plt.gcf().canvas.mpl_connect('button_press_event', on_click)

plt.show()
