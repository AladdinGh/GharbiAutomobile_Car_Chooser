import docx
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import logging
import pandas as pd


# Setup logging configuration
logging.basicConfig(filename='processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_hyperlink(paragraph, url, text, color="0000FF", underline=True):
 
    #Add a hyperlink to a paragraph.
    
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    # Create a w:r element and a new w:rPr element
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Add color if specified
    if color:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), color)
        rPr.append(c)

    # Add underline if specified
    if underline:
        u = OxmlElement('w:u')
        u.set(qn('w:val'), 'single')
        rPr.append(u)

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    # Append the hyperlink to the paragraph
    paragraph._p.append(hyperlink)

def add_features_table(doc, car, features):
  
    #Add a table with car features to the Word document.
    num_columns = 4  # Number of columns per row in the table
    table = doc.add_table(rows=1, cols=num_columns)
    table.style = 'Table Grid'

    row_cells = table.rows[0].cells
    col_idx = 0

    for feature in features:
        if feature not in ['Fahrzeughalter', 'Anzahl der Fahrzeughalter'] and feature in car.index and car[feature] == 1:
            row_cells[col_idx].text = feature
            col_idx += 1
            if col_idx == num_columns:
                row_cells = table.add_row().cells
                col_idx = 0

    # Add borders to the table cells
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(9)

            tc_borders = OxmlElement('w:tcBorders')
            for key in ('left', 'right', 'top', 'bottom'):
                new_border = OxmlElement(f'w:{key}')
                new_border.set(qn('w:val'), 'single')
                tc_borders.append(new_border)
            cell._element.get_or_add_tcPr().append(tc_borders)
            
            
def add_features_table_light(car, features):

    cpt = 0 
    for feature in features:
        if feature not in ['Fahrzeughalter', 'Anzahl der Fahrzeughalter'] and feature in car.index and car[feature] == 1:
            cpt = cpt + 1
    return(cpt-1)           

def copy_rows_by_index(df, indices_to_copy, index_column='index'):
    
    try:

        # Verify that the index_column exists
        if index_column not in df.columns:
            raise ValueError(f"Column '{index_column}' does not exist in the DataFrame.")
            
            
        # Filter the DataFrame based on the specified indices
        new_df = df[df[index_column].isin(indices_to_copy)]
        
        # If no rows are selected, log a warning
        if new_df.empty:
            logging.warning("No rows selected. The resulting DataFrame is empty.")
        
        return new_df
    except Exception as e:
        logging.error(f"Error in copy_rows_by_index: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    
    

def normalize(series, invert=False):
    try:
        normalized = (series - series.min()) / (series.max() - series.min())
        return 1 - normalized if invert else normalized
    except Exception as e:
        logging.error(f"Error in normalize: {e}")
        return series
    

def assign_scores_report(file_path, use_weights_flag= False):
    
    try:
                                                                        
        df_translated = pd.read_excel(file_path)
        # Weights for scoring
        weights = {
            'Brutto Price': 0.0,
            'Erstzulassung_years': 1.0,
        }
        
        # Normalize columns
        df_temp = df_translated.copy()
        # use invert = True : the higher the normalized value (1) the lower the price for example
        df_temp['Brutto Price'] = normalize(df_temp['Brutto Price'], invert=True)
        df_temp['Erstzulassung_years'] = normalize(df_temp['Erstzulassung_years'], invert=True)
        
        # we compute the score depending on the price only
        if (use_weights_flag == False):
            # Calculate scores
            df_temp['Score'] = (
                df_temp['Brutto Price'] * 1.0 
            )
            
        # we compute the score depending on the other features   
        else: 
            # Calculate scores
            df_temp['Score'] = (
                df_temp['Brutto Price'] * weights['Brutto Price'] 
                + df_temp['Erstzulassung_years'] * weights['Erstzulassung_years']
            )
        
        # Copy the Score column back to the original dataframe
        df_translated['Score'] = df_temp['Score'].round(2)
        
        if df_translated is not None:
            if (use_weights_flag == False):
                df_translated.to_excel("output/3_translated_preprocessed_sorted_by_price_for_initial_report.xlsx", index=False)
                logging.info("scores are saved as '3_translated_preprocessed_sorted_by_price_for_initial_report.xlsx'")
            else : 
                df_translated.to_excel("output/3_translated_preprocessed_sorted_by_score_for_second_report.xlsx", index=False)
                logging.info("scores are saved as '3_translated_preprocessed_sorted_by_score_for_second_report.xlsx'")
        else:
            logging.error("Assigning scores failed, dataframe not saved.")
            
    except Exception as e:
        logging.error(f"Error in assign_scores: {e}")
        return None
    
    
def select_rows():
    # Get user input for the indices to copy
    indices_input = input("Enter the indices of the rows you want to copy, separated by commas: ")
    
    # Convert the input string to a list of integers
    indices_to_copy = list(map(int, indices_input.split(',')))
    
    # Subtract 2 from all elements of indices_to_copy
    adjusted_indices = [index - 1 for index in indices_to_copy]
    
    # Call the function to get a new DataFrame with the adjusted indices
    file_path = "output/2_translated_preprocessed_df.xlsx"
    df = pd.read_excel(file_path)
    new_df = copy_rows_by_index(df, adjusted_indices)
    new_df.to_excel("output/selected_rows_df.xlsx", index=False)
    logging.info("Selected rows df saved as 'selected_rows_df.xlsx'")