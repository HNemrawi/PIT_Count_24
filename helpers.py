import streamlit as st
from predefined_lists_dicts import NE_mapping, WI_mapping 
from datetime import datetime
import pytz

def initialize_session_state():
    default_values = {
        'logged_in': False,
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

def clear_session_state():
    """Resets the session state variables except for the login state."""
    logged_in = st.session_state.get('logged_in', False)
    st.session_state.clear()
    st.session_state['logged_in'] = logged_in

def get_current_time(timezone):
    return datetime.now(pytz.timezone(timezone)).strftime('%Y-%m-%d_%H-%M-%S')

def select_region_and_mapping():
    """Select a region and get the corresponding mapping."""
    region = st.selectbox('Select an Implementation', ['', 'New England', 'Dashgreatlake'], index=0)
    timezone = "UTC"  # Default timezone

    if region == "New England":
        timezone = "America/New_York"
    elif region == "Dashgreatlake":
        timezone = "America/Chicago"

    current_time = get_current_time(timezone)
    mapping = None

    if region:
        mapping = WI_mapping if region == 'Dashgreatlake' else NE_mapping

    return region, mapping, current_time



