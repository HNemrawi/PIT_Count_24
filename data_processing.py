import warnings
import streamlit as st
import pandas as pd
import numpy as np
from predefined_lists_dicts import *

# Disable pandas warnings and set pandas display option
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

def preprocess_df(df, column_mapping):
    """
    Renames specified columns in a DataFrame based on a mapping and retains only those columns.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.
    column_mapping (dict): A dictionary mapping from old column names to new names.

    Returns:
    pandas.DataFrame: The processed DataFrame with renamed and filtered columns.
    """

    # Strip whitespace from column names and remove duplicate columns
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated(keep='first')]

    # Check for missing columns
    missing_columns = [col for col in column_mapping if col not in df.columns]
    if missing_columns:
        st.error(f"Missing columns in data: {', '.join(missing_columns)}")

    # Filter and rename valid columns
    valid_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
    df = df[valid_columns.keys()]
    df.rename(columns=valid_columns, inplace=True)

    return df

def initialize_count_columns(df):
    """
    Initialize count columns for different age groups in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with initialized count columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    age_group_columns = ['count_adult', 'count_youth', 'count_child_hoh', 'count_child_hh']
    for column in age_group_columns:
        df[column] = 0

    return df

def update_age_group_counts(df, age_related_cols, child_related_cols):
    """
    Update count columns based on age group categories present in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be updated.
    age_related_cols (list): List of column names related to age groups.
    child_related_cols (list): List of column names related to children in the household.

    Returns:
    pandas.DataFrame: The DataFrame with updated age group counts.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    adult_ages = ['25-34', '35-44', '45-54', '55-64', '65+']
    youth_ages = ['18-24']
    child_age = ['Under 18']

    for col in age_related_cols:
        if col not in df.columns:
            continue

        df[col] = df[col].fillna('')
        df['count_adult'] += df[col].isin(adult_ages).astype(int)
        df['count_youth'] += df[col].isin(youth_ages).astype(int)
        df['count_child_hoh'] += df[col].isin(child_age).astype(int)

    for col in child_related_cols:
        if col not in df.columns:
            continue

        df[col] = df[col].fillna('No')
        df['count_child_hh'] += (df[col] == 'Yes').astype(int)

    return df

def count_age_groups(df):
    """
    Count the number of adults, youth, and children in each household.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with counted age groups.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    age_related_cols = [col for col in ['age_range', 'adult_2_age_range', 'adult_3_age_range'] if col in df.columns]
    child_related_cols = [f'child_{i}' for i in range(1, 7) if f'child_{i}' in df.columns]

    df = initialize_count_columns(df)
    df = update_age_group_counts(df, age_related_cols, child_related_cols)

    df['total_person_in_household'] = df['count_adult'] + df['count_youth'] + df['count_child_hoh'] + df['count_child_hh']
    df['youth'] = df['count_adult'].apply(lambda x: 'Yes' if x == 0 else 'No')

    return df

def classify_household_type(df):
    """
    Classify the household based on the age groups present.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with a new column 'household_type' classifying the household.

    Raises:
    ValueError: If required columns are missing in the DataFrame.
    """

    required_columns = ['count_adult', 'count_youth', 'count_child_hh', 'count_child_hoh']
    if not all(column in df.columns for column in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

    # Define conditions for classifying households
    has_adults_or_youth = df['count_adult'] + df['count_youth'] > 0
    has_children = df['count_child_hh'] > 0
    only_children = df['count_child_hoh'] > 0

    # Set up the conditions and choices for classification
    conditions = [
        has_adults_or_youth & has_children,
        has_adults_or_youth & ~has_children,
        only_children
    ]
    choices = ['Household with Children', 'Household without Children', 'Household with Only Children']
    
    # Apply conditions to classify households
    df['household_type'] = np.select(conditions, choices, default='Unknown')

    return df

def flatten_entire_dataset(df):
    """
    Transforms a household-based DataFrame into a member-based DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be flattened.

    Returns:
    pandas.DataFrame: A flattened DataFrame where each row represents a member.

    Raises:
    ValueError: If the input is not a DataFrame or required columns are missing.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    # Reset index and create a Household_ID column
    df.reset_index(drop=True, inplace=True)
    df['Household_ID'] = df.index + 1

    def create_member(row, member_type, member_number):
        """
        Create a dictionary representing a member with household and individual attributes.
        """
        # Set prefix based on member type and define columns
        prefix = f'child_{member_number}_' if member_type == 'Child' else (f'adult_{member_number}_' if member_number != 1 else '')
        member_attrs = ['Gender', 'Race/Ethnicity', 'age_range', 'DV', 'vet', 'chronic_condition', 'disability', 'first_time', 'homeless_long', 'homeless_long_this_time', 'homeless_times', 'homeless_total','specific_homeless_long_this_time', 'specific_homeless_long']
        household_attrs = ['count_adult', 'count_youth', 'count_child_hoh', 'count_child_hh', 'total_person_in_household', 'household_type', 'youth']

        # Initialize and populate member dictionary
        member = {'Household_ID': row['Household_ID'], 'Member_Type': member_type, 'Member_Number': f'{member_type}{member_number}'}
        member.update({attr: row.get(f'{prefix}{attr}', None) for attr in member_attrs})
        member.update({attr: row.get(attr) for attr in household_attrs})

        # Check if the member exists based on key attributes
        return member if any(pd.notnull(member[attr]) for attr in ['Gender', 'Race/Ethnicity']) else None

    # Create flattened list of member dictionaries
    members = [member for _, row in df.iterrows() for member_type in ['Adult', 'Child'] for i in range(1, 4 if member_type == 'Adult' else 7) if (member := create_member(row, member_type, i))]

    return pd.DataFrame(members)

def flag_chronically_homeless(df):
    """
    Flags chronically homeless individuals in a DataFrame based on specific criteria.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with an added column 'CH' indicating chronically homeless status.

    Raises:
    ValueError: If required columns are missing in the DataFrame.
    """

    required_columns = ['homeless_long', 'first_time', 'homeless_long_this_time', 'homeless_times', 'homeless_total', 'disability']
    if not all(column in df.columns for column in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

    # Define conditions for chronic homelessness
    cond1 = (df['homeless_long'] == 'One year or more') & (df['first_time'] == 'Yes')
    cond2 = (df['homeless_long_this_time'] == 'One year or more') & (df['first_time'] == 'No')
    cond3 = (df['first_time'] == 'No') & (df['homeless_long_this_time'] == 'Less than one year') & (df['homeless_times'] == '4 or more times') & (df['homeless_total'] == '12 months or more')
    
    # Combine conditions and apply them along with disability status
    chronic_homeless_condition = cond1 | cond2 | cond3
    df['CH'] = np.where(chronic_homeless_condition & (df['disability'] == 'Yes'), 'Yes', 'No')

    return df

def add_age_group_column(df):
    """
    Adds a new column 'age_group' to the DataFrame to categorize individuals into age groups 
    based on their 'age_range'.

    The function maps the following age ranges:
    - 'adult': ['25-34', '35-44', '45-54', '55-64', '65+', '25-59', '60+']
    - 'youth': ['18-24']
    - 'child': ['Under 18']
    Any age range not listed is categorized as 'unknown'.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with the added 'age_group' column.

    Raises:
    ValueError: If the DataFrame or the 'age_range' column is not present.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    if 'age_range' not in df.columns:
        raise ValueError("'age_range' column is missing in the DataFrame.")

    # Define age ranges and create a mapping from age range to group
    age_ranges = {
        'adult': ['25-34', '35-44', '45-54', '55-64', '65+', '25-59', '60+'],
        'youth': ['18-24'],
        'child': ['Under 18']
    }
    age_range_to_group = {ar: grp for grp, ranges in age_ranges.items() for ar in ranges}

    # Map age ranges to groups and fill non-matching entries with 'unknown'
    df['age_group'] = df['age_range'].map(age_range_to_group).fillna('unknown')

    return df

def process_race(df):
    """
    Processes the 'Race/Ethnicity' column of the DataFrame, creating a new 'race' column with 
    specific categories based on the existing data. The original 'Race/Ethnicity' column is then dropped.

    The function categorizes the race/ethnicity data as follows:
    - If multiple races are selected, categorizes as 'Multi-Racial', with a note on Hispanic/Latina/e/o ethnicity if applicable.
    - If only 'Hispanic/Latina/e/o' is selected, categorizes as 'Hispanic/Latina/e/o'.
    - If a single race (other than 'Hispanic/Latina/e/o') is selected, uses that race.
    - If no race is selected or data is missing, categorizes as 'Unknown'.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with the processed 'race' column.

    Raises:
    ValueError: If the DataFrame or the 'Race/Ethnicity' column is not present.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    if 'Race/Ethnicity' not in df.columns:
        raise ValueError("'Race/Ethnicity' column is missing in the DataFrame.")

    def categorize_race(race_ethnicity):
        """
        Categorize the race/ethnicity based on the specified rules.
        """
        if pd.isnull(race_ethnicity):
            return 'Unknown'

        selected_races = race_ethnicity.split(', ')
        hispanic_selected = "Hispanic/Latina/e/o" in selected_races

        # Handle the case where only 'Hispanic/Latina/e/o' is selected
        if hispanic_selected and len(selected_races) == 1:
            return "Hispanic/Latina/e/o"

        if hispanic_selected:
            selected_races.remove("Hispanic/Latina/e/o")

        if len(selected_races) > 1:
            return "Multi-Racial & Hispanic/Latina/e/o" if hispanic_selected else "Multi-Racial (not Hispanic/Latina/e/o)"
        elif selected_races:
            return f"{selected_races[0]} & Hispanic/Latina/e/o" if hispanic_selected else selected_races[0]
        else:
            return "Unknown"

    # Apply the categorization and drop the original column
    df['race'] = df['Race/Ethnicity'].apply(categorize_race)
    df.drop('Race/Ethnicity', axis=1, inplace=True)

    return df

def process_gender(df):
    """
    Adds a 'gender_count' column to the DataFrame, which indicates the count of gender selections.
    The count is categorized as 'unknown' if gender data is missing, 'one' if exactly one gender is selected,
    and 'more' if more than one gender is selected.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The DataFrame with the added 'gender_count' column.

    Raises:
    ValueError: If the DataFrame or the 'Gender' column is not present.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    if 'Gender' not in df.columns:
        raise ValueError("'Gender' column is missing in the DataFrame.")

    def count_gender(gender):
        """
        Counts the number of gender selections and categorizes the count.
        """
        if pd.isnull(gender):
            return 'unknown'  
        return 'one' if len(gender.split(',')) == 1 else 'more'

    # Apply the counting function to the 'Gender' column
    df['gender_count'] = df['Gender'].apply(count_gender)
    
    return df

def standardize_conditions(df, condition_mapping):
    """
    Standardizes the 'chronic_condition' values in the DataFrame using a provided mapping.

    Each 'chronic_condition' value is split by commas, and each split item is then mapped to a new value 
    according to the provided mapping. If a value doesn't exist in the mapping, it's left unchanged.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.
    condition_mapping (dict): A dictionary where keys are original condition strings and values are standardized strings.

    Returns:
    pandas.DataFrame: The DataFrame with standardized 'chronic_condition' values.

    Raises:
    ValueError: If the input is not a DataFrame or the condition mapping is not a dictionary.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame.")

    if not isinstance(condition_mapping, dict):
        raise ValueError("Condition mapping must be a dictionary.")

    def map_conditions(conditions, mapping):
        """
        Maps each condition to its standardized form based on the provided mapping.
        """
        if isinstance(conditions, str):
            return ', '.join(mapping.get(condition.strip(), condition.strip()) for condition in conditions.split(','))
        return conditions

    # Apply the mapping to the 'chronic_condition' column if it exists
    if 'chronic_condition' in df.columns:
        df['chronic_condition'] = df['chronic_condition'].apply(lambda x: map_conditions(x, condition_mapping))

    return df

def process_data(flat_df, column_mapping):
    """
    Processes the data through various steps including preprocessing, counting age groups,
    classifying household types, flattening the dataset, flagging chronically homeless,
    adding age group columns, processing race and gender, and standardizing conditions.

    Parameters:
    flat_df (pandas.DataFrame): The DataFrame to be processed.
    column_mapping (dict): A dictionary for column renaming and filtering in preprocessing.
    condition_mapping (dict): A dictionary for standardizing conditions.

    Returns:
    Tuple[pandas.DataFrame, pandas.DataFrame, pandas.DataFrame, pandas.DataFrame]: 
    A tuple containing the processed DataFrame and three filtered DataFrames based on household types.

    Note: Returns empty DataFrames if an error occurs during processing.
    """

    try:
        # Step-by-step data processing
        flat_df = preprocess_df(flat_df, column_mapping)  # Preprocess DataFrame
        flat_df = count_age_groups(flat_df)  # Count age groups
        flat_df = classify_household_type(flat_df)  # Classify household types
        flat_df = flatten_entire_dataset(flat_df)  # Flatten dataset
        flat_df = flag_chronically_homeless(flat_df)  # Flag chronically homeless individuals
        flat_df = add_age_group_column(flat_df)  # Add age group column
        flat_df = process_race(flat_df)  # Process race data
        flat_df = process_gender(flat_df)  # Process gender data
        flat_df = standardize_conditions(flat_df, condition_mapping)  # Standardize conditions

        # Filter dataframes based on household types
        household_with_children = flat_df[flat_df['household_type'] == 'Household with Children']
        household_without_children = flat_df[flat_df['household_type'] == 'Household without Children']
        household_with_only_children = flat_df[flat_df['household_type'] == 'Household with Only Children']

        return flat_df, household_with_children, household_without_children, household_with_only_children

    except Exception as e:
        st.error(f"Error in process_data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames on error