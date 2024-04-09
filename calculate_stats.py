import streamlit as st
import pandas as pd
from predefined_lists_dicts import *
from template_mapping import *

def calculate_basic_counts(df, unique_households_df):
    """
    Calculate basic counts such as total number of households, persons, and unique household types.
    """
    return {
        'Total_number_of_households': df['Household_ID'].nunique(),
        'Total_number_of_persons': unique_households_df['total_person_in_household'].sum(),
        **{household_categories[household]: unique_households_df[unique_households_df['household_type'] == household].shape[0] for household in household_categories}
    }

def calculate_household_composition(df, unique_households_df):
    """
    Calculate statistics related to the composition of households.
    """
    return {
        **{f'Households_{n}_members': unique_households_df[(unique_households_df['household_type'] == 'Household with Children') & (unique_households_df['total_person_in_household'] == n)].shape[0] for n in range(2, 5)},
        'Households_5+_members' : unique_households_df[(unique_households_df['household_type'] == 'Household with Children') & (unique_households_df['total_person_in_household'] >= 5)].shape[0],
        'Number_of_children': unique_households_df[['count_child_hh', 'count_child_hoh']].sum().sum(),
        'Number_of_young_adults': unique_households_df['count_youth'].sum(),
        **{f'Number_of_adults_{age_range.replace("-", "-")}': df[df['age_range'] == age_range].shape[0] for age_range in age_ranges},
        'Unreported_Age' : df[(df['Member_Type'] == 'Adult') & (pd.isnull(df['age_range']))].shape[0],

    }

def calculate_demographic_info(df, unique_households_df):
    """
    Calculate demographic information such as age, gender, race, and condition categories.
    """
    return {
        'Total number of veterans':df[df['vet'] == 'Yes'].shape[0],
        'CH_Total_number_of_households': df[df['CH'] == 'Yes']['Household_ID'].nunique(),
        'CH_Total_number_of_persons': df[df['CH'] == 'Yes'].drop_duplicates(subset='Household_ID')['total_person_in_household'].sum(),
        **{f'Adults_with_a_{condition_categories[condition]}': df[(df['chronic_condition'].str.contains(condition, na=False, regex=False)) & (df['age_group'].isin(['adult', 'youth']))].shape[0] for condition in condition_categories},
        **{f'childs_with_a_{condition_categories[condition]}': df[(df['chronic_condition'].str.contains(condition, na=False, regex=False)) & (df['age_group'].isin(['child', 'unknown']))].shape[0] for condition in condition_categories},
        'Victims_of_Domestic_Violence_(fleeing)' : df[df['DV'] == 'Yes'].shape[0],
        'Victims_of_Domestic_Violence_(Household)' : df[df['DV'] == 'Yes']['Household_ID'].nunique(),
        **{gender_categories[gender]: df[(df['gender_count'] == 'one') & (df['Gender'] == gender)].shape[0] for gender in gender_categories},
        'More_Than_One_Gender': df[df['gender_count'] == 'more'].shape[0],
        **{f'Includes_{gender_categories[gender]}': df[(df['gender_count'] == 'more') & (df['Gender'].str.contains(gender, na=False, regex=False))].shape[0] for gender in gender_categories if gender != 'More Than One Gender'},
        **{race_categories[race]: df[df['race'] == race].shape[0] for race in race_categories},
    }

def calculate_youth_numbers(df, unique_households_df):
    """
    Calculate statistics for special categories such as parenting youth, unaccopanied youth, etc.
    """
    return {
        'Total_Parenting_Youth': df[(df['youth'] == 'Yes') & (df['Member_Type'] == 'Adult')].shape[0],
        'Total_Parenting_Youth_hh': unique_households_df[(unique_households_df['youth'] == 'Yes') & (unique_households_df['Member_Type'] == 'Adult') & (unique_households_df['household_type'] == 'Household with Children')].shape[0],
        'Total_Unaccompanied_Youth_hh': df[(df['youth'] == 'Yes') & (df['Member_Type'] == 'Adult') & (df['count_child_hh'] == 0)]['Household_ID'].nunique(),
        'Number_of_parenting_youth_under_age_18': df[(df['Member_Type'] == 'Adult') & (df['age_group'] == 'child')].shape[0],
        'Children_with_parenting_youth_under_18': unique_households_df[unique_households_df['age_group'] == 'child']['count_child_hh'].sum(),
        'Number_of_parenting_youth_18_24': df[(df['Member_Type'] == 'Adult') & (df['age_group'] == 'youth')].shape[0],
        'Children_with_parenting_youth_18_24': unique_households_df[unique_households_df['age_group'] == 'youth']['count_child_hh'].sum(),
    }

def calculate_history_homelessness(df, unique_households_df):
    """
    Calculate statistics for history of homelessness.
    """

    def sum_total_persons(condition):
        return unique_households_df[condition]['total_person_in_household'].sum()

    def count_households(condition):
        return unique_households_df[condition].shape[0]

    first_time_condition = unique_households_df['first_time'] == 'Yes'
    less_than_one_month_conditions = unique_households_df['specific_homeless_long'].isin(['1 day or less', '2 days - 1 week', 'More than 1 week - Less than 1 month']) | unique_households_df['specific_homeless_long_this_time'].isin(['1 day or less', '2 days - 1 week', 'More than 1 week - Less than 1 month'])
    one_to_three_months_condition = unique_households_df['specific_homeless_long'].isin(['1-3 Months']) | unique_households_df['specific_homeless_long_this_time'].isin(['1-3 Months'])
    three_months_to_one_year_condition = unique_households_df['specific_homeless_long'].isin(['More than 3 months - Less than 1 year']) | unique_households_df['specific_homeless_long_this_time'].isin(['More than 3 months - Less than 1 year'])
    one_year_or_more_condition = unique_households_df['specific_homeless_long'].isin(['1 year or more']) | unique_households_df['specific_homeless_long_this_time'].isin(['1 year or more'])

    return {
        'History_First_Time_Homeless': sum_total_persons(first_time_condition),
        'History_Less_than_One_Month': sum_total_persons(less_than_one_month_conditions),
        'History_One_to_Three_Months': sum_total_persons(one_to_three_months_condition),
        'History_Three_Months_to_One_Year': sum_total_persons(three_months_to_one_year_condition),
        'History_One_Year_or_More': sum_total_persons(one_year_or_more_condition),
        
        'History_HHs_First_Time_Homeless': count_households(first_time_condition),
        'History_HHs_Less_than_One_Month': count_households(less_than_one_month_conditions),
        'History_HHs_One_to_Three_Months': count_households(one_to_three_months_condition),
        'History_HHs_Three_Months_to_One_Year': count_households(three_months_to_one_year_condition),
        'History_HHs_One_Year_or_More': count_households(one_year_or_more_condition),
    }

@st.cache_data
def calculate_summary_stats(df, condition_column=None, condition=None):
    """
    Calculate a summary of various statistics from the dataframe, skipping any calculation that causes an error.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be analyzed.
    condition_column (str, optional): The column name to apply a filter condition.
    condition (str, optional): The condition value to filter the DataFrame.

    Returns:
    dict: A dictionary containing calculated summary statistics, excluding any that caused errors.
    """

    summary_stats = {}

    try:
        # Validate input DataFrame
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        # Optional filtering based on condition
        if condition_column and condition:
            if condition_column not in df.columns:
                raise ValueError(f"'{condition_column}' column is missing in the DataFrame.")
            df = df[df[condition_column] == condition]

        unique_households_df = df.drop_duplicates(subset='Household_ID')

        # List of calculation functions and their descriptions
        calculations = [
            (calculate_basic_counts, "Basic Counts"),
            (calculate_household_composition, "Household Composition"),
            (calculate_demographic_info, "Demographic Info"),
            (calculate_youth_numbers, "Youth Numbers"),
            (calculate_history_homelessness, "History of Homelessness")
        ]

        # Perform each calculation, skipping any that cause errors
        for calc_func, description in calculations:
            try:
                summary_stats.update(calc_func(df, unique_households_df))
            except Exception as e:
                st.error(f"Error in {description}: {e}")

        return summary_stats

    except Exception as e:
        st.error(f"Error in setting up calculate_summary_stats: {e}")
        return {}