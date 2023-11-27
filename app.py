import streamlit as st
import pandas as pd
from predefined_lists_dicts import *
from excel import create_and_download_excel
from data_processing import process_data
from datetime import datetime
from data_loading import DataLoading
from template_mapping import *
from handle_tabs import *
from streamlit_extras.metric_cards import style_metric_cards
from dash import *
from calculate_stats import calculate_summary_stats


# Suppress warnings and set display options
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

# Set page configuration
st.set_page_config(page_title="Point in Time", page_icon=":house:", layout="wide")

# Current time for file naming
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def main():
    initialize_session_state()

    # Setup layout and header
    setup_header()

    tab_titles = ["UPLOAD", "HDX_Totals", "HDX_Veterans", "HDX_Youth", "HDX_Subpopulations", "PIT Summary", "Dashboard", "DOWNLOAD"]
    tabs = st.tabs(tab_titles)
    tabs_dict = {title: tab for title, tab in zip(tab_titles, tabs)}

    with tabs_dict['UPLOAD']:

        region, mapping = select_region_and_mapping()

        upload_dict = DataLoading.load_and_display_data()

        for pop_name, df in upload_dict.items():
            df.dropna(subset='Timestamp', inplace=True)
            st.info(pop_name)
            st.dataframe(df)
            df,Household_with_children,Household_without_children,Household_with_only_children = process_data(df,mapping)
            st.session_state.uploaded_data[pop_name] = (df,Household_with_children, Household_without_children, Household_with_only_children)

            df_copy = df.copy()
            df_copy['Household_ID'] = df_copy['Household_ID'].astype(str) + '_' + pop_name
            df_copy['source'] = pop_name
            st.session_state.processed_dfs.append(df_copy)

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
        
        setup_footer()

        # Display processed data in each tab
        for tab_title, dfs_dict in [('HDX_Totals', st.session_state.dfs_dict), 
                                    ('HDX_Veterans', st.session_state.dfs_dict_vet), 
                                    ('HDX_Youth', st.session_state.dfs_dict_youth),
                                    ('HDX_Subpopulations', st.session_state.dfs_dict_sub),
                                    ('PIT Summary', st.session_state.dfs_dict_sum)]:
            if tab_title in tabs_dict:
                process_and_display(dfs_dict, tabs_dict[tab_title])


        # Check if st.session_state.processed_dfs is not empty
        with tabs_dict['Dashboard']:
                if st.session_state.processed_dfs:

                        # Concatenate processed DataFrames and store them in session state
                        if 'merged_df' not in st.session_state:
                                st.session_state.merged_df = pd.concat(st.session_state.processed_dfs, ignore_index=True)

                        # Get unique location and household options
                        unique_locations = st.session_state.merged_df['source'].unique()
                        unique_households = st.session_state.merged_df['household_type'].unique()

                        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])

                        # Create select widgets to filter data
                        selected_locations = col1.multiselect('Location', list(unique_locations), default=list(unique_locations))
                        selected_households = col2.multiselect('Household Type', list(unique_households), default=list(unique_households))
                        selected_CH = col3.selectbox('Chronically Homeless', ["Yes"],index=None,placeholder="")
                        selected_Vet = col4.selectbox('Veteran Status', ["Yes"],index=None,placeholder="")
                        selected_Youth = col5.selectbox('Youth Households', ["Yes"],index=None,placeholder="")


                        # Filter the DataFrame based on user's selections
                        filtered_df = st.session_state.merged_df[
                        (st.session_state.merged_df['source'].isin(selected_locations)) &
                        (st.session_state.merged_df['household_type'].isin(selected_households))
                        ]
                        if selected_CH == "Yes":
                                filtered_df = filtered_df[filtered_df['CH'] == 'Yes']
                        if selected_Vet == "Yes":
                                filtered_df = filtered_df[filtered_df['vet'] == 'Yes']
                        if selected_Youth == "Yes":
                                filtered_df = filtered_df[filtered_df['youth'] == 'Yes']                                
                        # Create columns for displaying metrics
                        col1, col2 = st.columns(2)
                        # Calculate metrics
                        num_household, num_person = calculate_metrics(filtered_df)
                        # Display Metrics
                        col1.metric("Total Number of Households", num_household)
                        col2.metric("Total Number of Clients", num_person)
                        style_metric_cards(border_left_color='#00629b')

                        #gender chart
                        summary = calculate_summary_stats(filtered_df)
                        if not filtered_df.empty:
                                col1, col2 = st.columns(2)
                                # household chart
                                household_data = {key: summary[key] for key in HOUSEHOLD_KEYS if summary[key] > 0}
                                sorted_household_data = sort_data(household_data)
                                household_chart = create_bar_chart(sorted_household_data, 'Number of Households by Household Type', 'Household Type', 'Count')
                                household_chart = update_plot_layout(household_chart, list(range(len(HOUSEHOLD_KEYS))), sorted_household_data)
                                col1.plotly_chart(household_chart, use_container_width=True)

                                #gender chart
                                gender_data = {key: summary[key] for key in GENDER_KEYS if summary[key] > 0}
                                sorted_gender_data = sort_data(gender_data)
                                gender_chart = create_bar_chart(sorted_gender_data, 'Gender Distribution', 'Gender Identity', 'Count')
                                gender_chart = update_plot_layout(gender_chart, list(range(len(GENDER_KEYS))), sorted_gender_data)
                                col1.plotly_chart(gender_chart, use_container_width=True)

                                # Race/Ethnicity data chart
                                race_ethnicity_data = {key: summary[key] for key in RACE_ETHNICITY_KEYS if summary[key] > 0}
                                sorted_race_ethnicity_data = sort_data(race_ethnicity_data)
                                race_ethnicity_chart = create_bar_chart(sorted_race_ethnicity_data, 'Race/Ethnicity Distribution', 'Race/Ethnicity', 'Count')
                                race_ethnicity_chart = update_plot_layout(race_ethnicity_chart, list(range(len(RACE_ETHNICITY_KEYS))), sorted_race_ethnicity_data)
                                col2.plotly_chart(race_ethnicity_chart, use_container_width=True)


                                # Include_gender_data chart
                                Include_gender_data = {key: summary[key] for key in INCLUDE_GENDER_KEYS if summary[key] > 0}
                                sorted_Include_gender_data = sort_data(Include_gender_data)
                                Include_gender_chart = create_bar_chart(
                                        sorted_Include_gender_data, 
                                        f"{summary['More_Than_One_Gender']} Clients with More Than One Gender", 
                                        'More Than One Gender Includes', 'Count'
                                )
                                Include_gender_chart = update_plot_layout(
                                        Include_gender_chart, 
                                        list(range(len(INCLUDE_GENDER_KEYS))), 
                                        sorted_Include_gender_data  # Pass the sorted dictionary directly
                                )
                                col2.plotly_chart(Include_gender_chart, use_container_width=True)

                                # Age groups data chart
                                age_groups_data = {key: summary[key] for key in AGE_GROUPS_KEYS if summary[key] > 0}
                                sorted_age_groups_data = {key: age_groups_data[key] for key in DESIRED_ORDER if key in age_groups_data}
                                age_groups_chart = create_bar_chart(sorted_age_groups_data, 'Age Groups Distribution', 'Age Group', 'Count')
                                age_groups_chart = update_plot_layout(age_groups_chart, list(range(len(sorted_age_groups_data))), sorted_age_groups_data)
                                col1.plotly_chart(age_groups_chart, use_container_width=True)

                                # Chronic condition data chart
                                chronic_condition_data = {key: summary[key] for key in CHRONIC_CONDITION_KEYS if summary[key] > 0}
                                sorted_chronic_condition_data = sort_data(chronic_condition_data)
                                chronic_condition_chart = create_bar_chart(sorted_chronic_condition_data, 'Adult withChronic Condition COunt', 'Chronic Condition', 'Count')
                                chronic_condition_chart = update_plot_layout(chronic_condition_chart, list(range(len(CHRONIC_CONDITION_KEYS))), sorted_chronic_condition_data)
                                col2.plotly_chart(chronic_condition_chart, use_container_width=True)
                        else:
                                st.write("No data available.")

                else:
                        st.text("No data available. Please upload data.")



        with tabs_dict['DOWNLOAD']:
            tabs_data_dict = {
                'HDX_TOTAL': st.session_state.dfs_dict,
                'HDX_Veterans': st.session_state.dfs_dict_vet,
                'HDX_Youth': st.session_state.dfs_dict_youth,
                'HDX_Subpopulations': st.session_state.dfs_dict_sub,
                'PIT Summary': st.session_state.dfs_dict_sum
            }
            
            st.session_state.excel_file = create_and_download_excel(tabs_data_dict)

            if st.download_button(
                'Download Excel file',
                st.session_state.excel_file,
                file_name=f'{region}_PIT_Count_{current_time}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ):
                st.cache_data.clear()
                # Reset the session state variables
                st.session_state.uploaded_data = {}
                st.session_state.dfs_dict = {}
                st.session_state.dfs_dict_vet = {}
                st.session_state.dfs_dict_youth = {}
                st.session_state.dfs_dict_sub = {}
                st.session_state.dfs_dict_sum = {}
                # Remove the excel_file from session state
                del st.session_state.excel_file


if __name__ == "__main__":
    main()