import streamlit as st
import pandas as pd
from predefined_lists_dicts import *
from data_processing import process_data
from data_loading import DataLoading
from template_mapping import *
from handle_tabs import *
from populate_temp import calculate_and_store_stats

HTML_HEADER_LOGO = """
            <div style="font-style: italic; color: #808080; text-align: left;">
            <a href="https://icalliances.org/" target="_blank"><img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="250"></a>
            </div>
            """
HTML_HEADER_TITLE = f'<h2 style="color:#00629b; text-align:center;">Point in Time Count</h2>'

HTML_FOOTER = """
                <div style="font-style: italic; color: #808080; text-align: center;">
                    <a href="https://icalliances.org/" target="_blank">
                        <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="99">
                    </a>
                    DASH™ is a trademark of Institute for Community Alliances.
                </div>
                <div style="font-style: italic; color: #808080; text-align: center;">
                    <a href="https://icalliances.org/" target="_blank">
                        <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/1475614371395-KFTYP42QLJN0VD5V9VB1/ICA+Official+Logo+PNG+%28transparent%29.png?format=1500w" width="99">
                    </a>
                    © 2024 Institute for Community Alliances (ICA). All rights reserved.
                </div>
                    """

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
            st.dataframe(stats_data)

def initialize_session_state():
    default_values = {
        'uploaded_data': {},
        'dfs_dict': {},
        'dfs_dict_vet': {},
        'dfs_dict_youth': {},
        'dfs_dict_sub': {},
        'dfs_dict_sum': {},
        'processed_dfs' : []
 }
    
    # Initialize session state variables if not already set
    for var, default_val in default_values.items():
        if var not in st.session_state:
            st.session_state[var] = default_val

def setup_header():
    """Set up the header of the Streamlit page."""
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(HTML_HEADER_LOGO, unsafe_allow_html=True)
    with col2:
        st.markdown(HTML_HEADER_TITLE, unsafe_allow_html=True)

def setup_footer():
    """Set up the footer of the Streamlit page."""
    st.markdown(HTML_FOOTER, unsafe_allow_html=True)

def select_region_and_mapping():
    """Select a region and get the corresponding mapping."""
    region = st.selectbox('Select an Implementation', ['New England', 'Wisconsin'], index=0)
    mapping = WI_mapping if region == 'Wisconsin' else NE_mapping
    return region, mapping

