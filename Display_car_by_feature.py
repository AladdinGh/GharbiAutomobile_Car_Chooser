import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

def create_feature_selection_gui(preprocessed_df):
    def show_cars_with_feature(feature):
        if feature in preprocessed_df.columns:
            cars_with_feature = preprocessed_df[preprocessed_df[feature] == 1]
            if not cars_with_feature.empty:
                popup = tk.Toplevel(root)
                popup.title(f"Cars with {feature}")
                
                # Create a canvas for scrolling
                popup_canvas = tk.Canvas(popup)
                popup_canvas.pack(side="left", fill="both", expand=True)
                
                # Add a scrollbar to the canvas
                popup_scrollbar = ttk.Scrollbar(popup, orient="vertical", command=popup_canvas.yview)
                popup_scrollbar.pack(side="right", fill="y")
                
                # Configure the canvas to use the scrollbar
                popup_canvas.configure(yscrollcommand=popup_scrollbar.set)
                popup_canvas.bind("<Configure>", lambda e: popup_canvas.configure(scrollregion=popup_canvas.bbox("all")))
                
                # Create a frame inside the canvas to hold the labels
                popup_frame = ttk.Frame(popup_canvas)
                popup_canvas.create_window((0, 0), window=popup_frame, anchor="nw")

                for idx, url in enumerate(cars_with_feature['URL']):
                    label = tk.Label(popup_frame, text=url)
                    label.grid(column=0, row=idx, sticky="w")

            else:
                messagebox.showinfo("Info", f"No cars found with feature '{feature}'.")
        else:
            messagebox.showerror("Error", f"Feature '{feature}' not found in DataFrame columns.")

    def filter_cars():
        selected_features = [specified_features[idx] for idx, var in enumerate(feature_vars) if var.get() == 1]
        if selected_features:
            filtered_cars = preprocessed_df[preprocessed_df[selected_features].eq(1).any(axis=1)]
            
            if not filtered_cars.empty:
                popup = tk.Toplevel(root)
                popup.title("Filtered Cars")
                
                for idx, row in filtered_cars.iterrows():
                    label = tk.Label(popup, text=f"URL: {row['URL']}, Kilometerstand: {row['Kilometerstand']}")
                    label.pack()
            else:
                messagebox.showinfo("Info", "No cars found matching the selected features.")
        else:
            messagebox.showinfo("Info", "No features selected for filtering.")

    def on_closing():
        root.quit()

    # Create Tkinter window
    root = tk.Tk()
    root.title("Feature Selection")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Create a canvas for scrolling
    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame inside the canvas to hold the checkboxes
    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Define your specified features
    specified_features = [col.strip() for col in preprocessed_df.columns[75:-2]]

    # Create checkboxes
    feature_vars = []
    for idx, feature in enumerate(specified_features):
        var = tk.IntVar(value=0)  # Set initial value to 0
        ttk.Checkbutton(frame, text=feature, variable=var, command=lambda f=feature: show_cars_with_feature(f)).grid(column=0, row=idx, sticky="w")
        feature_vars.append(var)

    # Add the canvas to a scrollable region
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Create filter button
    filter_button = ttk.Button(root, text="Filter", command=filter_cars)
    filter_button.pack(pady=(5, 0))

    root.mainloop()

# Usage example:
if __name__ == "__main__":
    # Load your data into a pandas DataFrame
    # For demonstration purposes, let's create a sample DataFrame
    preprocessed_df = pd.read_csv("preprocessed_df.csv")
    create_feature_selection_gui(preprocessed_df)
