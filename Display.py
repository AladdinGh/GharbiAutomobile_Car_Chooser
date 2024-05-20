import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import tkinter as tk
import webbrowser
import math

# Function to open URL in Microsoft Edge
def open_url_in_edge(url):
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Microsoft//Edge//Application//msedge.exe"))
    webbrowser.get('edge').open(url)

# Function to fill missing values in 'Farbe' with values from 'Farbe (Hersteller)' if available
def fill_missing_color(row):
    if pd.isnull(row['Farbe']):
        return row['Farbe (Hersteller)']
    return row['Farbe']

def plot_cars_by_month_and_year(file_path):
    try:
        # Read the preprocessed DataFrame
        df = pd.read_csv(file_path)

        # Extract month and year from the 'Erstzulassung' column
        df['Erstzulassung'] = pd.to_datetime(df['Erstzulassung']).dt.to_period('M')
        df['Month'] = df['Erstzulassung'].dt.month
        df['Year'] = df['Erstzulassung'].dt.year

        # Fill missing colors
        df['Farbe'] = df.apply(fill_missing_color, axis=1)

        # Group by month and year and count the number of cars
        car_count_by_month_year = df.groupby(['Year', 'Month']).size().reset_index(name='Car Count')

        # Plot the results
        plt.figure(figsize=(15, 5))

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

        # Function to display car URLs and basic features for selected month and year
        def on_click(event):
            if event.button == 1:  # Check if left mouse button clicked
                month_index = int(event.xdata)  # Get the index of the clicked point
                year, month = months_years[month_index]
                selected_cars = df[(df['Year'] == year) & (df['Month'] == month)][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)']]
                urls_and_features = selected_cars.apply(lambda row: [row['URL'], row['Brutto Price'], row['Kilometerstand'], row['Farbe']], axis=1)
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
                        for c, value in enumerate(row):
                            if c == 0:
                                label = tk.Label(popup_window, text=value[:30] + '...', bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                                label.bind('<Button-1>', lambda e, url=value: open_url_in_edge(url))  # Pass the original URL
                            else:
                                label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")

                    popup_window.mainloop()

        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        plt.show()
    except Exception as e:
        print(f"Error: {e}")

def plot_cars_by_price_category(file_path):
    try:
        # Read the preprocessed DataFrame
        df = pd.read_csv(file_path)

        # Fill missing colors
        df['Farbe'] = df.apply(fill_missing_color, axis=1)

        # Determine the minimum and maximum price in the dataset
        min_price = df['Brutto Price'].min()
        max_price = df['Brutto Price'].max()

        # Define price categories with bins of 2000 Euros, starting from the minimum price
        price_bins = list(range(int(min_price), int(max_price) + 2000, 2000))
        price_labels = [f"{price_bins[i]} to {price_bins[i+1]}" for i in range(len(price_bins) - 1)]

        # Create a 'Price Category' column based on 'Brutto Price'
        df['Price Category'] = pd.cut(df['Brutto Price'], bins=price_bins, labels=price_labels, right=False)

        # Group by 'Price Category' and count the number of cars
        car_count_by_price_category = df['Price Category'].value_counts().sort_index().reset_index()
        car_count_by_price_category.columns = ['Price Category', 'Car Count']

        # Plot the results
        plt.figure(figsize=(15, 5))

        # Plot circles for each price category
        for i, row in car_count_by_price_category.iterrows():
            price_category = row['Price Category']
            car_count = row['Car Count']
            plt.scatter(i, 0, s=car_count * 200, alpha=0.5)
            plt.text(i, 0, car_count, ha='center', va='center', color='white')

        # Set x-axis ticks and labels
        plt.xticks(range(len(price_labels)), price_labels, rotation=45, ha='right')

        # Hide y-axis ticks and labels
        plt.yticks([])

        # Set labels and title
        plt.xlabel('Price Category')
        plt.title('Number of Cars by Price Category')

        plt.grid(axis='x')
        plt.tight_layout()

        # Function to display car URLs and basic features for selected price category
        def on_click(event):
            if event.button == 1:  # Check if left mouse button clicked
                price_index = int(event.xdata)  # Get the index of the clicked point
                selected_price_category = price_labels[price_index]
                selected_cars = df[df['Price Category'] == selected_price_category][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)']]
                urls_and_features = selected_cars.apply(lambda row: [row['URL'], row['Brutto Price'], row['Kilometerstand'], row['Farbe']], axis=1)
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
                        for c, value in enumerate(row):
                            if c == 0:
                                label = tk.Label(popup_window, text=value[:30] + '...', bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                                label.bind('<Button-1>', lambda e, url=value: open_url_in_edge(url))  # Pass the original URL
                            else:
                                label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")

                    popup_window.mainloop()

        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        plt.show()
    except Exception as e:
        print(f"Error: {e}")

def plot_cars_by_kilometerstand(file_path):
    try:
        # Read the preprocessed DataFrame
        df = pd.read_csv(file_path)

        # Fill missing colors
        df['Farbe'] = df.apply(fill_missing_color, axis=1)

        # Determine the minimum and maximum kilometerstand in the dataset
        min_km = df['Kilometerstand'].min()
        max_km = df['Kilometerstand'].max()

        # Define kilometerstand categories with bins of 10000 km, starting from the minimum kilometerstand
        km_bins = list(range(int(min_km), int(max_km) + 10000, 10000))
        km_labels = [f"{km_bins[i]} to {km_bins[i+1]}" for i in range(len(km_bins) - 1)]

        # Create a 'Kilometerstand Category' column based on 'Kilometerstand'
        df['Kilometerstand Category'] = pd.cut(df['Kilometerstand'], bins=km_bins, labels=km_labels, right=False)

        # Group by 'Kilometerstand Category' and count the number of cars
        car_count_by_km_category = df['Kilometerstand Category'].value_counts().sort_index().reset_index()
        car_count_by_km_category.columns = ['Kilometerstand Category', 'Car Count']

        # Plot the results
        plt.figure(figsize=(15, 5))

        # Create an array of kilometerstand categories
        km_categories = car_count_by_km_category['Kilometerstand Category']

        # Plot circles for each kilometerstand category
        for i, km_category in enumerate(km_categories):
            car_count = car_count_by_km_category.loc[car_count_by_km_category['Kilometerstand Category'] == km_category, 'Car Count'].iloc[0]
            plt.scatter(i, 0, s=car_count * 200, alpha=0.5)
            plt.text(i, 0, car_count, ha='center', va='center', color='white')

        # Set x-axis ticks and labels
        plt.xticks(range(len(km_categories)), km_categories, rotation=45, ha='right')

        # Hide y-axis ticks and labels
        plt.yticks([])

        # Set labels and title
        plt.xlabel('Kilometerstand Category')
        plt.title('Number of Cars by Kilometerstand Category')

        plt.grid(axis='x')
        plt.tight_layout()

        # Function to display car URLs and basic features for selected kilometerstand category
        def on_click(event):
            if event.button == 1:  # Check if left mouse button clicked
                km_index = int(event.xdata)  # Get the index of the clicked point
                selected_km_category = km_categories[km_index]
                selected_cars = df[df['Kilometerstand Category'] == selected_km_category][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)']]
                urls_and_features = selected_cars.apply(lambda row: [row['URL'], row['Brutto Price'], row['Kilometerstand'], row['Farbe']], axis=1)
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
                        for c, value in enumerate(row):
                            if c == 0:
                                label = tk.Label(popup_window, text=value[:30] + '...', bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                                label.bind('<Button-1>', lambda e, url=value: open_url_in_edge(url))  # Pass the original URL
                            else:
                                label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")

                    popup_window.mainloop()

        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        plt.show()
    except Exception as e:
        print(f"Error: {e}")
        
        
        
        
def plot_cars_by_Kraftstoffverbrauch(file_path):
    try:
        # Read the preprocessed DataFrame
        df = pd.read_csv(file_path)

        # Ensure 'Kraftstoffverbrauch' is a numerical column
        df['Kraftstoffverbrauch'] = pd.to_numeric(df['Kraftstoffverbrauch'], errors='coerce')

        # Fill missing colors
        df['Farbe'] = df.apply(fill_missing_color, axis=1)

        # Determine the minimum and maximum fuel consumption in the dataset
        min_fuel = df['Kraftstoffverbrauch'].min()
        max_fuel = df['Kraftstoffverbrauch'].max()

        # Define fuel consumption categories with bins, starting from the minimum to maximum consumption
        fuel_bins = list(np.arange(math.floor(min_fuel), math.ceil(max_fuel) + 1, 1))
        fuel_labels = [f"{fuel_bins[i]} to {fuel_bins[i+1]}" for i in range(len(fuel_bins) - 1)]

        # Create a 'Fuel Consumption Category' column based on 'Kraftstoffverbrauch'
        df['Fuel Consumption Category'] = pd.cut(df['Kraftstoffverbrauch'], bins=fuel_bins, labels=fuel_labels, right=False)

        # Group by 'Fuel Consumption Category' and count the number of cars
        car_count_by_fuel_category = df['Fuel Consumption Category'].value_counts().sort_index().reset_index()
        car_count_by_fuel_category.columns = ['Fuel Consumption Category', 'Car Count']

        # Plot the results
        plt.figure(figsize=(15, 5))

        # Plot circles for each fuel consumption category
        for i, row in car_count_by_fuel_category.iterrows():
            fuel_category = row['Fuel Consumption Category']
            car_count = row['Car Count']
            plt.scatter(i, 0, s=car_count * 200, alpha=0.5)
            plt.text(i, 0, car_count, ha='center', va='center', color='white')

        # Set x-axis ticks and labels
        plt.xticks(range(len(fuel_labels)), fuel_labels, rotation=45, ha='right')

        # Hide y-axis ticks and labels
        plt.yticks([])

        # Set labels and title
        plt.xlabel('Fuel Consumption Category')
        plt.title('Number of Cars by Fuel Consumption Category')

        plt.grid(axis='x')
        plt.tight_layout()

        # Function to display car URLs and basic features for selected fuel consumption category
        def on_click(event):
            if event.button == 1:  # Check if left mouse button clicked
                fuel_index = int(event.xdata)  # Get the index of the clicked point
                selected_fuel_category = fuel_labels[fuel_index]
                selected_cars = df[df['Fuel Consumption Category'] == selected_fuel_category][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)', 'Kraftstoffverbrauch']]
                urls_and_features = selected_cars.apply(lambda row: [row['URL'], row['Brutto Price'], row['Kilometerstand'], row['Farbe'], row['Kraftstoffverbrauch']], axis=1)
                urls_and_features_list = urls_and_features.values.tolist()
                if urls_and_features_list:
                    # Create a new popup window
                    popup_window = tk.Tk()
                    popup_window.title('Selected Cars Information')
                    popup_window.configure(bg='#f0f0f0')  # Set background color

                    # Create a header row with attribute names
                    header = ['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Kraftstoffverbrauch']
                    for c, attr_name in enumerate(header):
                        label = tk.Label(popup_window, text=attr_name, bg='#f0f0f0', font=('Helvetica', 10, 'bold'))
                        label.grid(row=0, column=c, padx=5, pady=2, sticky="w")

                    # Create a table to display URLs and features
                    for r, row in enumerate(urls_and_features_list):
                        for c, value in enumerate(row):
                            if c == 0:
                                label = tk.Label(popup_window, text=value[:30] + '...', bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                                label.bind('<Button-1>', lambda e, url=value: open_url_in_edge(url))  # Pass the original URL
                            else:
                                label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")

                    popup_window.mainloop()

        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        plt.show()
    except Exception as e:
        print(f"Error: {e}")
        
        
        
        
def plot_cars_by_farbe(file_path):
    try:
        # Read the preprocessed DataFrame
        df = pd.read_csv(file_path)

        # Fill missing colors
        df['Farbe'] = df.apply(fill_missing_color, axis=1)

        # Group by 'Farbe' and count the number of cars
        car_count_by_farbe = df['Farbe'].value_counts().reset_index()
        car_count_by_farbe.columns = ['Farbe', 'Car Count']

        # Plot the results
        plt.figure(figsize=(15, 5))

        # Plot circles for each color
        for i, row in car_count_by_farbe.iterrows():
            color = row['Farbe']
            car_count = row['Car Count']
            plt.scatter(color, 0, s=car_count * 100, alpha=0.5)
            plt.text(color, 0, car_count, ha='center', va='center', color='white')

        # Set x-axis ticks and labels
        plt.xticks(rotation=45, ha='right')

        # Hide y-axis ticks and labels
        plt.yticks([])

        # Set labels and title
        plt.xlabel('Color (Farbe)')
        plt.title('Number of Cars by Color')

        plt.grid(axis='x')
        plt.tight_layout()

        # Function to display car URLs and basic features for selected color category
        def on_click(event):
            if event.button == 1:  # Check if left mouse button clicked
                color_index = int(event.xdata)  # Get the index of the clicked point
                selected_color = car_count_by_farbe.loc[color_index, 'Farbe']
                selected_cars = df[df['Farbe'] == selected_color][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)']]
                urls_and_features = selected_cars.apply(lambda row: [row['URL'], row['Brutto Price'], row['Kilometerstand'], row['Farbe']], axis=1)
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
                        for c, value in enumerate(row):
                            if c == 0:
                                label = tk.Label(popup_window, text=value[:30] + '...', bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                                label.bind('<Button-1>', lambda e, url=value: open_url_in_edge(url))  # Pass the original URL
                            else:
                                label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")

                    popup_window.mainloop()

        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        plt.show()
    except Exception as e:
        print(f"Error: {e}")


def plot_cars_by_hubraum(file_path):
    try:
        # Read the preprocessed DataFrame
        df = pd.read_csv(file_path)

        # Group by 'Hubraum' and count the number of cars
        car_count_by_hubraum = df['Hubraum'].value_counts().reset_index()
        car_count_by_hubraum.columns = ['Hubraum', 'Car Count']

        # Plot the results
        plt.figure(figsize=(15, 5))

        # Plot circles for each engine displacement category
        for i, row in car_count_by_hubraum.iterrows():
            hubraum = row['Hubraum']
            car_count = row['Car Count']
            plt.scatter(hubraum, 0, s=car_count * 100, alpha=0.5)
            plt.text(hubraum, 0, car_count, ha='center', va='center', color='white')

        # Set x-axis ticks and labels
        plt.xticks(rotation=45, ha='right')

        # Hide y-axis ticks and labels
        plt.yticks([])

        # Set labels and title
        plt.xlabel('Hubraum (cm³)')
        plt.title('Number of Cars by Engine Displacement')

        plt.grid(axis='x')
        plt.tight_layout()

        # Function to display car URLs and basic features for selected engine displacement category
        def on_click(event):
            if event.button == 1:  # Check if left mouse button clicked
                hubraum_index = int(event.xdata)  # Get the index of the clicked point
                selected_hubraum = car_count_by_hubraum.loc[hubraum_index, 'Hubraum']
                selected_cars = df[df['Hubraum'] == selected_hubraum][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)']]
                urls_and_features = selected_cars.apply(lambda row: [row['URL'], row['Brutto Price'], row['Kilometerstand'], row['Farbe']], axis=1)
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
                        for c, value in enumerate(row):
                            if c == 0:
                                label = tk.Label(popup_window, text=value[:30] + '...', bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                                label.bind('<Button-1>', lambda e, url=value: open_url_in_edge(url))  # Pass the original URL
                            else:
                                label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")

                    popup_window.mainloop()

        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        plt.show()
    except Exception as e:
        print(f"Error: {e}")

def plot_cars_by_PS(file_path):
    try:
        # Read the preprocessed DataFrame
        df = pd.read_csv(file_path)

        # Ensure 'PS' is a numerical column
        df['PS'] = pd.to_numeric(df['PS'], errors='coerce')

        # Fill missing colors
        df['Farbe'] = df.apply(fill_missing_color, axis=1)

        # Determine the minimum and maximum PS in the dataset
        min_ps = df['PS'].min()
        max_ps = df['PS'].max()

        # Define PS categories with bins, starting from the minimum to maximum PS
        ps_bins = list(range(int(min_ps), int(max_ps) + 10, 10))
        ps_labels = [f"{ps_bins[i]} to {ps_bins[i+1]}" for i in range(len(ps_bins) - 1)]

        # Create a 'PS Category' column based on 'PS'
        df['PS Category'] = pd.cut(df['PS'], bins=ps_bins, labels=ps_labels, right=False)

        # Group by 'PS Category' and count the number of cars
        car_count_by_ps_category = df['PS Category'].value_counts().sort_index().reset_index()
        car_count_by_ps_category.columns = ['PS Category', 'Car Count']

        # Plot the results
        plt.figure(figsize=(15, 5))

        # Create an array of PS categories
        ps_categories = car_count_by_ps_category['PS Category']

        # Plot circles for each PS category
        for i, ps_category in enumerate(ps_categories):
            car_count = car_count_by_ps_category.loc[car_count_by_ps_category['PS Category'] == ps_category, 'Car Count'].iloc[0]
            plt.scatter(i, 0, s=car_count * 200, alpha=0.5)
            plt.text(i, 0, car_count, ha='center', va='center', color='white')

        # Set x-axis ticks and labels
        plt.xticks(range(len(ps_labels)), ps_labels, rotation=45, ha='right')

        # Hide y-axis ticks and labels
        plt.yticks([])

        # Set labels and title
        plt.xlabel('PS Category')
        plt.title('Number of Cars by PS Category')

        plt.grid(axis='x')
        plt.tight_layout()

        # Function to display car URLs and basic features for selected PS category
        def on_click(event):
            if event.button == 1:  # Check if left mouse button clicked
                ps_index = int(event.xdata)  # Get the index of the clicked point
                selected_ps_category = ps_labels[ps_index]
                selected_cars = df[df['PS Category'] == selected_ps_category][['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'Farbe (Hersteller)', 'PS']]
                urls_and_features = selected_cars.apply(lambda row: [row['URL'], row['Brutto Price'], row['Kilometerstand'], row['Farbe'], row['PS']], axis=1)
                urls_and_features_list = urls_and_features.values.tolist()
                if urls_and_features_list:
                    # Create a new popup window
                    popup_window = tk.Tk()
                    popup_window.title('Selected Cars Information')
                    popup_window.configure(bg='#f0f0f0')  # Set background color

                    # Create a header row with attribute names
                    header = ['URL', 'Brutto Price', 'Kilometerstand', 'Farbe', 'PS']
                    for c, attr_name in enumerate(header):
                        label = tk.Label(popup_window, text=attr_name, bg='#f0f0f0', font=('Helvetica', 10, 'bold'))
                        label.grid(row=0, column=c, padx=5, pady=2, sticky="w")

                    # Create a table to display URLs and features
                    for r, row in enumerate(urls_and_features_list):
                        for c, value in enumerate(row):
                            if c == 0:
                                label = tk.Label(popup_window, text=value[:30] + '...', bg='#ffffff', font=('Helvetica', 10, 'underline'), cursor='hand2')
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")
                                label.bind('<Button-1>', lambda e, url=value: open_url_in_edge(url))  # Pass the original URL
                            else:
                                label = tk.Label(popup_window, text=value, bg='#ffffff', font=('Helvetica', 10), wraplength=200)
                                label.grid(row=r+1, column=c, padx=5, pady=2, sticky="w")

                    popup_window.mainloop()

        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        plt.show()
    except Exception as e:
        print(f"Error: {e}")


# Example usage:
file_path = "preprocessed_df.csv"
plot_cars_by_PS(file_path)
#plot_cars_by_hubraum(file_path)
#plot_cars_by_farbe(file_path)
#plot_cars_by_Kraftstoffverbrauch(file_path)
# plot_cars_by_price_category(file_path)
# plot_cars_by_month_and_year(file_path)
# plot_cars_by_kilometerstand(file_path)



