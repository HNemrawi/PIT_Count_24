import streamlit as st
from header_footer import setup_header, setup_footer
from helpers import select_region_and_mapping, initialize_session_state
from data_loader import DataLoading
from login import authenticate_user
from data_processing import process_data
from handle_tabs import handle_tabs_for_households, display_processed_data
from predefined_lists_dicts import *
from download import handle_download
from dashboard import display_dashboard

# Suppress warnings and set display options
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

# Set page configuration
st.set_page_config(page_title="Point in Time", page_icon=":house:", layout="wide")

def display_main_content():
    if st.session_state.get('logged_in', False):
        tab_titles = ["UPLOAD", "HDX_Totals", "HDX_Veterans", "HDX_Youth", "HDX_Subpopulations", "PIT Summary", "Dashboard", "DOWNLOAD"]
        tabs = st.tabs(tab_titles)
        tabs_dict = {title: tab for title, tab in zip(tab_titles, tabs)}

        with tabs_dict['UPLOAD']:
            region, mapping, current_time = select_region_and_mapping()
            if region:
                st.session_state['region'] = region
                st.session_state['mapping'] = mapping
                st.session_state['current_time'] = current_time
                setup_header()
                upload_dict = DataLoading.load_and_display_data()
                initialize_session_state()

                for pop_name, df in upload_dict.items():
                    df.dropna(subset=['Timestamp'], inplace=True)
                    st.info(pop_name)
                    st.dataframe(df)
                    df, Household_with_children, Household_without_children, Household_with_only_children = process_data(df, mapping)
                    st.session_state.uploaded_data[pop_name] = (df, Household_with_children, Household_without_children, Household_with_only_children)

                    df_copy = df.copy()
                    df_copy['Household_ID'] = df_copy['Household_ID'].astype(str) + '_' + pop_name
                    df_copy['source'] = pop_name
                    st.session_state.processed_dfs.append(df_copy)

                    # Handle tabs for different household types
                    handle_tabs_for_households(tabs_dict, df, pop_name, Household_with_children, Household_without_children, Household_with_only_children)

                setup_footer()

                # Display processed data in each tab
                display_processed_data(tabs_dict)
            else:
                st.warning("Please select an Implementation to get started.")
            

            if region:
                with tabs_dict['Dashboard']:
                    display_dashboard()

                with tabs_dict['DOWNLOAD']:
                    handle_download(region, current_time)
                    st.markdown("[HMIS and Non-HMIS Combiner](https://combinepit.streamlit.app/)")
                    if region == "New England":
                        st.markdown("[Breakdown by Project Name on HIC](https://hic-project.streamlit.app/)")


def main():
    initialize_session_state()
    if not st.session_state['logged_in']:
        authenticate_user()
    else:
        display_main_content()

if __name__ == "__main__":
    main()