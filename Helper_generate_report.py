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