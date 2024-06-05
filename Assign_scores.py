import logging
import pandas as pd


''' 
this is intended to assign scores to translated dataframes to avoid preprocessing and translating every time there are weights/importance changes

input : translated df
output : translated df with scores which can be used within initial report and sencond report
'''

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
        df_translated['Score'] = df_temp['Score']
        
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
    
    

    
# file_path = "translated_preprocessed_df.xlsx"
# df_translated_with_scores = assign_scores(file_path)