import pandas as pd
import plotly.express as px
import streamlit as st
from calculate_stats import calculate_summary_stats
from streamlit_extras.metric_cards import style_metric_cards


# Constants
HOUSEHOLD_KEYS = [
    'Households_with_Child', 'Households_without_Children', 'Households_with_Only_Children'
]

GENDER_KEYS = [
    'Woman_Girl', 'Man_Boy', 'Culturally_Specific_Identity', 'Transgender', 
    'Non_Binary', 'Questioning', 'Different_Identity'
]

INCLUDE_GENDER_KEYS = [
    'Includes_Woman_Girl', 'Includes_Man_Boy', 'Includes_Culturally_Specific_Identity',
    'Includes_Transgender', 'Includes_Non_Binary', 'Includes_Questioning', 'Includes_Different_Identity'
]

RACE_ETHNICITY_KEYS = [
    'Indigenous', 'Indigenous_Hispanic', 'Asian', 'Asian_Hispanic',
    'Black', 'Black_Hispanic', 'Hispanic', 'Middle_Eastern_North_African',
    'Middle_Eastern_North_African_Hispanic', 'Native_Hawaiian',
    'Native_Hawaiian_Hispanic', 'White', 'White_Hispanic',
    'Multi_Racial_Hispanic', 'Multi_Racial_Non_Hispanic'
]

AGE_GROUPS_KEYS = [
    'Number_of_children', 'Number_of_young_adults', 'Number_of_adults_25-34',
    'Number_of_adults_35-44', 'Number_of_adults_45-54', 'Number_of_adults_55-64',
    'Number_of_adults_65+'
]

CHRONIC_CONDITION_KEYS = [
    'Adults_with_a_Serious_Mental_Illness', 'Adults_with_a_Substance_Use_Disorder',
    'Adults_with_a_Physical_Condition', 'Adults_with_a_HIV_AIDS',
    'Adults_with_a_Developmental_Condition', 'Adults_with_a_other_Condition'
]

DESIRED_ORDER = [
    'Number_of_children', 'Number_of_young_adults', 'Number_of_adults_25-34',
    'Number_of_adults_35-44', 'Number_of_adults_45-54', 'Number_of_adults_55-64',
    'Number_of_adults_65+'
]

def calculate_metrics(df):
    """Calculate unique household and person counts."""
    unique_households_df = df.drop_duplicates(subset='Household_ID')
    num_household = unique_households_df['Household_ID'].nunique()
    num_person = len(df)
    return num_household, num_person

def sort_data(data_dict):
    """Sort a dictionary by its values in descending order."""
    return dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))

def create_bar_chart(data, title, x_label, y_label, height=560):
    """Create a bar chart from the provided data."""
    df = pd.DataFrame(list(data.items()), columns=[x_label, y_label])
    fig = px.bar(df, x=x_label, y=y_label, title=title, labels={'x': x_label, 'y': y_label}, height=height)
    return fig

def update_plot_layout(fig, tickvals, ticktext, bottom_margin=100, figure_width=800, figure_height=560):
    """Update plot layout with custom settings, fixed bottom margin, and dynamic bar sizes."""
    custom_palette = ['#00629b', '#008bb2', '#004d70', '#08a88d', '#2cbba9', '#067066']
    
    # Calculate dynamic bar width based on number of categories
    num_categories = len(ticktext)
    max_bar_width = 0.8  # Adjust this as necessary
    dynamic_bar_width = max_bar_width / max(1, num_categories / 10)  # Example heuristic for bar width
    
    fig.update_xaxes(tickvals=tickvals, ticktext=list(ticktext.keys()), tickangle=45)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        template="plotly_white",
        font=dict(size=12),
        margin=dict(l=50, r=50, t=50, b=220),
        xaxis_fixedrange=True,
        width=figure_width,
        height=figure_height,
    )
    fig.update_traces(
        text=list(ticktext.values()),
        texttemplate='%{text}',
        textposition='outside',
        marker_color=custom_palette[:len(ticktext)],
        textfont_size=12,
        width=dynamic_bar_width  # Use dynamic bar width
    )
    return fig

@st.cache_data
def get_merged_df(processed_dfs):
    return pd.concat(processed_dfs, ignore_index=True)

@st.cache_data
def filter_dataframe(df, locations, households, CH, Vet, Youth):
    filtered_df = df[(df['source'].isin(locations)) & (df['household_type'].isin(households))]
    if CH == "Yes":
        filtered_df = filtered_df[filtered_df['CH'] == 'Yes']
    if Vet == "Yes":
        filtered_df = filtered_df[filtered_df['vet'] == 'Yes']
    if Youth == "Yes":
        filtered_df = filtered_df[filtered_df['youth'] == 'Yes']
    return filtered_df

def display_dashboard():
    if st.session_state.processed_dfs:
            if 'merged_df' not in st.session_state:
                    st.session_state.merged_df = get_merged_df(st.session_state.processed_dfs)

            # Initialize filtered_df
            filtered_df = st.session_state.merged_df

            unique_locations = st.session_state.merged_df['source'].unique()
            unique_households = st.session_state.merged_df['household_type'].unique()

            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])

            selected_locations = col1.multiselect('Location', list(unique_locations), default=list(unique_locations))
            selected_households = col2.multiselect('Household Type', list(unique_households), default=list(unique_households))
            selected_CH = col3.selectbox('Chronically Homeless', ["Yes"], index=None, placeholder="")
            selected_Vet = col4.selectbox('Veteran Status', ["Yes"], index=None, placeholder="")
            selected_Youth = col5.selectbox('Youth Households', ["Yes"], index=None, placeholder="")

            filtered_df = filter_dataframe(st.session_state.merged_df, selected_locations, selected_households, selected_CH, selected_Vet, selected_Youth)
                    
            # Create columns for displaying metrics
            col1, col2 = st.columns(2)
            # Calculate metrics
            num_household, num_person = calculate_metrics(filtered_df)
            # Display Metrics
            col1.metric("Total Number of Households", num_household)
            col2.metric("Total Number of Clients", num_person)
            style_metric_cards(border_left_color='#00629b')

            summary = calculate_summary_stats(filtered_df)
            if not filtered_df.empty:
                    col1, col2 = st.columns(2)

                    # household chart
                    household_data = {key: summary[key] for key in HOUSEHOLD_KEYS if summary[key] > 0}
                    sorted_household_data = sort_data(household_data)
                    household_chart = create_bar_chart(sorted_household_data, 'Number of Households by Household Type', 'Household Type', 'Households Count')
                    household_chart = update_plot_layout(household_chart, list(range(len(HOUSEHOLD_KEYS))), sorted_household_data)
                    col1.plotly_chart(household_chart, use_container_width=True)

                    #gender chart
                    gender_data = {key: summary[key] for key in GENDER_KEYS if summary[key] > 0}
                    sorted_gender_data = sort_data(gender_data)
                    gender_chart = create_bar_chart(sorted_gender_data, 'Gender Distribution', 'Gender Identity', 'Clients Count')
                    gender_chart = update_plot_layout(gender_chart, list(range(len(GENDER_KEYS))), sorted_gender_data)
                    col1.plotly_chart(gender_chart, use_container_width=True)

                    # Race/Ethnicity data chart
                    race_ethnicity_data = {key: summary[key] for key in RACE_ETHNICITY_KEYS if summary[key] > 0}
                    sorted_race_ethnicity_data = sort_data(race_ethnicity_data)
                    race_ethnicity_chart = create_bar_chart(sorted_race_ethnicity_data, 'Race/Ethnicity Distribution', 'Race/Ethnicity', 'Clients Count')
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
                    age_groups_chart = create_bar_chart(sorted_age_groups_data, 'Age Groups Distribution', 'Age Group', 'Clients Count')
                    age_groups_chart = update_plot_layout(age_groups_chart, list(range(len(sorted_age_groups_data))), sorted_age_groups_data)
                    col1.plotly_chart(age_groups_chart, use_container_width=True)

                    # Chronic condition data chart
                    chronic_condition_data = {key: summary[key] for key in CHRONIC_CONDITION_KEYS if summary[key] > 0}
                    sorted_chronic_condition_data = sort_data(chronic_condition_data)
                    chronic_condition_chart = create_bar_chart(sorted_chronic_condition_data, 'Adult withChronic Condition Count', 'Chronic Condition', 'Adults Count')
                    chronic_condition_chart = update_plot_layout(chronic_condition_chart, list(range(len(CHRONIC_CONDITION_KEYS))), sorted_chronic_condition_data)
                    col2.plotly_chart(chronic_condition_chart, use_container_width=True)
            else:
                    st.warning("No data available with these filters.")

    else:
            st.warning("No data available. Please upload data.")

