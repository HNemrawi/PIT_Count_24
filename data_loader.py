import streamlit as st
import pandas as pd
from helpers import clear_session_state

class DataLoading:
    """
    DataLoading facilitates the loading of data files with supported formats (CSV, Excel) into pandas DataFrames. 
    It utilizes Streamlit's caching to speed up data loading on subsequent runs and manages the initialization 
    of session state for storing data.
    """
    supported_formats = ['.csv', '.xlsx']

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_dataframe(uploaded_file, sheet_name=None):
        """
        Load a pandas DataFrame from an uploaded file.

        Parameters:
        uploaded_file: The file uploaded by the user.
        sheet_name: Optional; The specific sheet name to load for Excel files.

        Returns:
        A pandas DataFrame if the file is valid and loaded successfully, or None if no file is uploaded.
        """
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file, sheet_name=sheet_name)
            
    @staticmethod
    def handle_file_upload(text):
        """
        Provide a file uploader widget and load the data from the selected file.

        Parameters:
        text: Display text for the file uploader.

        Returns:
        A pandas DataFrame loaded from the selected file, or None if no file is selected.
        """
        uploaded_file = st.file_uploader(text, type=DataLoading.supported_formats)
        if uploaded_file:
            sheet_name = None
            if uploaded_file.name.endswith('.xlsx'):
                try:
                    xls = pd.ExcelFile(uploaded_file)
                    sheet_names = xls.sheet_names
                    selectbox_key = f"sheet_select_{text}"  # Unique key for each selectbox
                    sheet_name = st.selectbox("Choose the sheet", sheet_names, key=selectbox_key)
                except Exception as e:
                    st.error(f"Error reading Excel file: {e}")
                    return None
            return DataLoading.load_dataframe(uploaded_file, sheet_name)

    @staticmethod
    def load_and_display_data():
        """
        Load data from uploaded files within a form and display success messages. If the form is submitted without 
        any files, an error message is displayed.

        Returns:
        A dictionary containing the loaded dataframes categorized by their types.
        """
        upload_dict = {}
        with st.form("Upload_form"):
            # Upload file handlers for different types of data
            uploaded_file_es = DataLoading.handle_file_upload('Sheltered_ES file (CSV or Excel)')
            uploaded_file_th = DataLoading.handle_file_upload('Sheltered_TH file (CSV or Excel)')
            uploaded_file_unsheltered = DataLoading.handle_file_upload('Unsheltered file (CSV or Excel)')

            # Submit button for the form
            submitted = st.form_submit_button("Submit")
            if submitted:
                clear_session_state()
                if uploaded_file_es is not None:
                    upload_dict['Sheltered_ES'] = uploaded_file_es
                    st.success("Sheltered_ES data loaded successfully!")

                if uploaded_file_th is not None:
                    upload_dict['Sheltered_TH'] = uploaded_file_th
                    st.success("Sheltered_TH data loaded successfully!")

                if uploaded_file_unsheltered is not None:
                    upload_dict['Unsheltered'] = uploaded_file_unsheltered
                    st.success("Unsheltered data loaded successfully!")

                if not upload_dict:
                    st.error("No data loaded. Please upload at least one file.")

        return upload_dict


