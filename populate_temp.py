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
        if key in summary_stats:
            df_template.at[index, (column_name)] = summary_stats[key]
        else:
            df_template.at[index, (column_name)] = 'N/A'

def calculate_and_store_stats(input_df, name, stored_dfs, column_name, INDEX_TUPLES, mapping, condition_column=None, condition=None):
    """Calculate statistics and store them in a provided dictionary of dataframes."""
    summary_stats = calculate_summary_stats(input_df, condition_column, condition)
    if name not in stored_dfs:
        stored_dfs[name] = get_empty_template(INDEX_TUPLES)
    populate_template(stored_dfs[name], summary_stats, mapping, column_name)
    
