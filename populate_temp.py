import streamlit as st
import pandas as pd
from predefined_lists_dicts import *
from template_mapping import *
from calculate_stats import calculate_summary_stats

def get_empty_template(INDEX_TUPLES):
    """Create an empty dataframe template with a multi-index based on tuples provided."""
    return pd.DataFrame(0, index=pd.MultiIndex.from_tuples(INDEX_TUPLES), columns=COLUMN)

def populate_template(df_template, summary_stats, mapping, column_name):
    """Populate the dataframe template with summary statistics based on a mapping dictionary."""
    for index, key in mapping:
        # Define the special conditions for 'Sheltered_TH' column
        special_conditions = [
            (("Chronically Homeless", "Total number of households"), 'CH_Total_number_of_households'),
            (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
        ]
        
        # Check if column_name is 'Sheltered_TH' and if the current (index, key) pair is in the special conditions
        if column_name == "Sheltered_TH" and (index, key) in special_conditions:
            df_template.at[index, column_name] = 0  # Override with 0
        elif key in summary_stats:
            df_template.at[index, column_name] = summary_stats[key]  # Set actual value
        else:
            df_template.at[index, column_name] = 'N/A'  # Set as 'N/A' if key not found


def calculate_and_store_stats(input_df, name, stored_dfs, column_name, INDEX_TUPLES, mapping, condition_column=None, condition=None):
    """Calculate statistics and store them in a provided dictionary of dataframes."""
    summary_stats = calculate_summary_stats(input_df, condition_column, condition)
    if name not in stored_dfs:
        stored_dfs[name] = get_empty_template(INDEX_TUPLES)
    populate_template(stored_dfs[name], summary_stats, mapping, column_name)
