import pandas as pd
import plotly.express as px
import streamlit as st

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
