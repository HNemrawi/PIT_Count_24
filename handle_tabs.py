import streamlit as st
import pandas as pd
import pytz
from datetime import datetime
from predefined_lists_dicts import *
from data_processing import process_data
from data_loader import DataLoading
from template_mapping import *
from handle_tabs import *
from populate_temp import calculate_and_store_stats

def handle_tab(tab, df, column_name, filter_conditions, stats_name, dfs_dict, INDEX_TUPLES, mapping, condition_column=None, condition=None):
    """
    Handle the tabulation of data within a given tab context.
    """
    with tab:
        try:
            filtered_df = df.query(filter_conditions) if filter_conditions else df
            calculate_and_store_stats(filtered_df, stats_name, dfs_dict, column_name, INDEX_TUPLES, mapping, condition_column, condition)
            stats_data = dfs_dict[stats_name]
        except Exception as e:
            st.error(f"Error in handle_tab: {e}")
            return pd.DataFrame()

# Function to calculate the 'Total' column
def calculate_total(stats_data):
    numeric_columns = ['Sheltered_ES', 'Sheltered_TH', 'Unsheltered']
    stats_data[numeric_columns] = stats_data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    stats_data['Total'] = stats_data[numeric_columns].sum(axis=1)

# Process and display data in tabs
def process_and_display(dfs_dict, tab):
    with tab:
        for stats_name, stats_data in dfs_dict.items():
            calculate_total(stats_data)  # Calculate the 'Total' column
            st.info(f'{stats_name}:')
            st.dataframe(stats_data, width=1120, height=500)
    

def handle_tabs_for_households(tabs_dict, df, pop_name, Household_with_children, Household_without_children, Household_with_only_children):
    # All Households
    handle_tab(tabs_dict['HDX_Totals'], Household_with_children, pop_name, None, 
            "Households with at Least One Adult and One Child", 
            st.session_state.dfs_dict, TOTAL_with, mapping_with)

    handle_tab(tabs_dict['HDX_Totals'], Household_without_children, pop_name,None, 
            "Households without Children", 
            st.session_state.dfs_dict, TOTAL_without, mapping_without)

    handle_tab(tabs_dict['HDX_Totals'], Household_with_only_children, pop_name, None, 
            "Households with Only Children (under age 18)", 
            st.session_state.dfs_dict, TOTAL_withonly, mapping_withonly)
    
    handle_tab(tabs_dict['HDX_Totals'], df, pop_name, None, 
            "Total Households and Persons", 
            st.session_state.dfs_dict, TOTAL_with, mapping_with)


    # Veteran Households Only
    handle_tab(tabs_dict['HDX_Veterans'], Household_with_children, pop_name, 
            None, 
            "Veteran Households with at Least One Adult and One Child", 
            st.session_state.dfs_dict_vet, VET_with, mapping_vet_with, 
            'vet', 'Yes')

    handle_tab(tabs_dict['HDX_Veterans'], Household_without_children, pop_name, 
            None, 
            "Veteran Households without Children", 
            st.session_state.dfs_dict_vet, VET_without, mapping_vet_without, 
            'vet', 'Yes')
    
    handle_tab(tabs_dict['HDX_Veterans'], df, pop_name, 
            None, 
            "Veteran Total Households and Persons", 
            st.session_state.dfs_dict_vet, VET_with, mapping_vet_with, 
            'vet', 'Yes')

    # Youth Households
    handle_tab(tabs_dict['HDX_Youth'],df,pop_name,
        "(count_child_hh == 0)",
        "Unaccompanied Youth Households",
        st.session_state.dfs_dict_youth, YOUTH_without,mapping_youth_without,
        'youth','Yes'
    )

    handle_tab(tabs_dict['HDX_Youth'], Household_with_children, pop_name, 
            "(Member_Type == 'Adult')", 
            "Parenting Youth Households", 
            st.session_state.dfs_dict_youth, YOUTH_with, mapping_youth_with,
            'youth','Yes')

    # Additional Homeless Populations
    handle_tab(tabs_dict['HDX_Subpopulations'], df, pop_name, 
            "(age_group.isin(['adult', 'youth']))", 
            "Homeless Subpopulations", 
            st.session_state.dfs_dict_sub, INDEX_SUB, mapping_SUB)
    
    # PIT Summary
    handle_tab(tabs_dict['PIT Summary'], df, pop_name, 
            None, 
            "PIT Summary", 
            st.session_state.dfs_dict_sum, TOTAL_Summary, mapping_Summary)
    
def display_processed_data(tabs_dict):
    for tab_title, dfs_dict in [('HDX_Totals', st.session_state.dfs_dict), 
                                ('HDX_Veterans', st.session_state.dfs_dict_vet), 
                                ('HDX_Youth', st.session_state.dfs_dict_youth),
                                ('HDX_Subpopulations', st.session_state.dfs_dict_sub),
                                ('PIT Summary', st.session_state.dfs_dict_sum)]:
        if tab_title in tabs_dict:
            process_and_display(dfs_dict, tabs_dict[tab_title])
