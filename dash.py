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

# Cache function to calculate metrics
@st.cache
def calculate_metrics(df):
    """Calculate unique household and person counts."""
    unique_households_df = df.drop_duplicates(subset='Household_ID')
    num_household = unique_households_df['Household_ID'].nunique()
    num_person = len(df)
    return num_household, num_person

# Function to sort data
def sort_data(data_dict):
    """Sort a dictionary by its values in descending order."""
    return dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))

# Function to create bar charts
def create_bar_chart(data, title, x_label, y_label, height=560):
    """Create a bar chart from the provided data."""
    df = pd.DataFrame(list(data.items()), columns=[x_label, y_label])
    fig = px.bar(df, x=x_label, y=y_label, title=title, labels={'x': x_label, 'y': y_label}, height=height)
    return fig

def update_plot_layout(fig, tickvals, ticktext):
    """Update plot layout with custom settings."""
    custom_palette = ['#00629b', '#008bb2', '#004d70', '#08a88d', '#2cbba9', '#067066']
    fig.update_xaxes(tickvals=tickvals, ticktext=list(ticktext.keys()))
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(template="plotly_white")
    fig.update_traces(text=list(ticktext.values()), texttemplate='%{text}', textposition='outside', marker_color=custom_palette[:len(ticktext)])
    return fig
