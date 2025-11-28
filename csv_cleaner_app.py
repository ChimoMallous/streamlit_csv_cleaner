# Imports
import streamlit as st
import plotly.express as px
import pandas as pd
import time

# Set page layout
st.set_page_config(layout="wide")
st.title("CSV Data Cleaner")

# Initialize cleaned dataframe
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'last_file_id' not in st.session_state:
    st.session_state.last_file_id = None

# Create function to load data and data preview
def load_data_preview(file):
    
    # Create data info expanders for data preview
    st.subheader("Original Data Preview")
    expander_tab1, expander_tab2 = st.columns(2)

    with expander_tab1:
        with st.expander("Data Head"):
            st.dataframe(st.session_state.original_df.head(8))
    with expander_tab2:
        with st.expander("Data Description"):
            st.dataframe(st.session_state.original_df.describe())
    st.divider()

    # Collect null counts from data
    num_null_count = st.session_state.original_df.select_dtypes(include=['int64', 'float64']).isnull().sum().sum()
    text_null_count = st.session_state.original_df.select_dtypes(include=['object']).isnull().sum().sum()
    total_null_count = st.session_state.original_df.isnull().sum().sum()
    total_duplicate_count = st.session_state.original_df.duplicated().sum()
    total_row_count = st.session_state.original_df.shape[0]
    total_column_count = st.session_state.original_df.shape[1]

    # Display null data info
    st.subheader("Original Data Statistics")
    info_col1, info_col2, info_col3 = st.columns(3)

    info_col2.metric("Numerical Null Count:", f"{num_null_count:,}")
    info_col1.metric("Text Null Count:", f"{text_null_count:,}")
    info_col1.metric("Total Null Count:", f"{total_null_count:,}")
    info_col3.metric("Total Duplicate Count:", f"{total_duplicate_count:,}")
    info_col2.metric("Total Row Count:", f"{total_row_count:,}")
    info_col3.metric("Total Column Count:", f"{total_column_count:,}")
    
    
    st.divider()

    # Null columns charts
    null_chart_col1, null_chart_col2 = st.columns(2)

    with null_chart_col1:
        # Show which columns have nulls
        st.subheader("Null Values by Column")
        null_summary = st.session_state.original_df.isnull().sum()
        # Sort null summary to only show columns with more than 0 nulls
        null_summary = null_summary[null_summary > 0].sort_values(ascending=False)

        # If more than 0 nulls, create and show graph
        if len(null_summary) > 0:
            null_sum_fig = px.bar(
                x=null_summary.index, y=null_summary.values,
                labels={'x': 'Column', 'y': 'Null Count'},
                color_discrete_sequence=["#B80000"])
            st.plotly_chart(null_sum_fig)
        else: 
            st.success("No Null Values Found")
        
    with null_chart_col2:
        # Show null versus filled per column
        st.subheader("Null versus Filled by Column")
        cols_with_nulls = [col for col in st.session_state.original_df.columns if st.session_state.original_df[col].isnull().sum() > 0]
        col_stats = pd.DataFrame({
            "Column": cols_with_nulls,
            "Missing": [st.session_state.original_df[col].isnull().sum() for col in cols_with_nulls],
            "Filled": [st.session_state.original_df[col].notnull().sum() for col in cols_with_nulls]  
        })

        if cols_with_nulls:
            null_vs_fill_fig = px.bar(
                col_stats,
                x="Column",
                y=["Missing", "Filled"],
                barmode="stack",
                color_discrete_sequence=["#B80000", "#006747"])
            st.plotly_chart(null_vs_fill_fig)
        else: st.success("No Null Values Found")

# Create function to load cleaned data and cleaned data preview
def load_cleaned_preview(df):
    # Create data info expanders
    st.subheader("Cleaned Data Preview")
    expand_tab1, expand_tab2 = st.columns(2)
    with expand_tab1:
        with st.expander("Cleaned Data Head"):
            st.dataframe(df.head(8))
    with expand_tab2:
        with st.expander("Cleaned Data Description"):
            st.dataframe(df.describe())
    st.divider()

    # Collect null information
    text_null_count = df.select_dtypes(include=['object']).isnull().sum().sum()
    num_null_count = df.select_dtypes(include=['int64', 'float64']).isnull().sum().sum()
    total_null_count = df.isnull().sum().sum()
    total_duplicate_count = df.duplicated().sum()
    total_row_count = df.shape[0]
    total_column_count = df.shape[1]

    # Display null information
    st.subheader("Cleaned Data Statistics")
    data_col1, data_col2, data_col3 = st.columns(3)
    data_col2.metric("Numerical Null Count:", f"{num_null_count:,}")
    data_col1.metric("Text Null Count:", f"{text_null_count:,}")
    data_col1.metric("Total Null Count:", f"{total_null_count:,}")
    data_col3.metric("Total Duplicate Count:", f"{total_duplicate_count:,}")
    data_col2.metric("Total Row Count:", f"{total_row_count:,}")
    data_col3.metric("Total Column Count:", f"{total_column_count:,}")
    st.divider()

    
# Create CSV uploader
uploaded = st.file_uploader("Upload CSV Data")

# Check if a new file is uploaded
if uploaded is not None:
    file_id = uploaded.file_id
    # If new file, reset everything
    if st.session_state.last_file_id != file_id:
        with st.spinner("Loading CSV..."):
            time.sleep(1)
            df = pd.read_csv(uploaded)
            st.session_state.original_df = df.copy()
            st.session_state.cleaned_df = df.copy()
            st.session_state.last_file_id = file_id

# Add button to load sample data
if st.button("Load Sample Data", type="secondary"):
    with st.spinner("Loading Sample Data..."):
        time.sleep(1)
        sample_data = pd.DataFrame({
            'Name': ['JOHN DOE', 'jane smith', None, 'Bob  Wilson', 'Alice Lee', 'JOHN DOE', 'Mike Chen', None, '  Sarah Park'],
            'Age': [25, 30, 35, None, 28, 25, 45, 32, None],
            'City': ['NEW YORK', 'los angeles', 'CHICAGO', None, 'boston', 'NEW YORK', 'Seattle', 'Portland', 'Miami  '],
            'Salary': [50000, 60000, None, 70000, 55000, 50000, 80000, None, 62000],
            'Department': ['Sales', 'marketing', 'IT', 'Sales', None, 'Sales', 'it', 'Marketing', 'SALES'],
            'Email': ['john@email.com', 'jane@email.com', None, 'bob@email.com  ', 'alice@email.com', 'john@email.com', None, 'sarah@email.com', 'mike@email.com']
        })
        st.session_state.original_df = sample_data.copy()
        st.session_state.cleaned_df = sample_data.copy()
        st.session_state.last_file_id = 'sample_data'
    st.rerun()

# Load data when uploaded
if st.session_state.cleaned_df is not None:
    try:
        load_data_preview(uploaded)
        cleaned_df = st.session_state.cleaned_df.copy()

    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()

    # Create cleaning sections if file is uploaded
    st.divider()
    st.header("**Data Cleaning**")
    st.subheader("Cleaning Options")
    cleaning_col1, cleaning_col2, cleaning_col3, cleaning_col4 = st.columns(4)

    # Create text cleaning column
    with cleaning_col1:
        st.write("**Text Columns**")

        # Filter text columns from data
        text_cols = cleaned_df.select_dtypes(include=['object']).columns.tolist()
        text_cols_with_nulls = [col for col in text_cols if cleaned_df[col].isnull().sum() > 0]

        # Create selectbox with options for text column cleaning 
        if text_cols:
            text_method = st.selectbox(
                "Select method to handle missing values in text columns:",
                [
                    "Fill with Mode",
                    "Fill with 'Unknown'",
                    "Fill with Empty String",
                    "Fill with Custom Input",
                    "Forward Fill",
                    "Backward Fill"
                ], key="text_method"
            )
            text_input = None

            # Create extra input box if text cleaning option is 'fill with custom input'
            if text_method == "Fill with Custom Input":
                text_input = st.text_input("Enter Custom Input", key="text_input")
                if not text_input:
                    st.warning("Please enter a custom input before applying")

            # Create button to apply text column cleaning operations
            if st.button("Apply to Text Columns", type='primary', key='apply_text'):
                for col in text_cols_with_nulls:

                    # Text mode
                    if text_method == "Fill with Mode":
                        cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else 'Unknown', inplace=True)
                    # Text 'unknown'
                    elif text_method == "Fill with 'Unknown'":
                        cleaned_df[col].fillna('Unknown', inplace=True)
                    # Text empty string
                    elif text_method == "Fill with Empty String":
                        cleaned_df[col].fillna('', inplace=True)
                    # Text forward fill
                    elif text_method == "Forward Fill":
                        cleaned_df[col].ffill(inplace=True)
                    # Text backward fill
                    elif text_method == "Backward Fill":
                        cleaned_df[col].bfill(inplace=True)
                    # Text custom input
                    elif text_method == "Fill with Custom Input":
                        cleaned_df[col].fillna(text_input, inplace=True)
                
                # Save cleaned dataframe state
                st.session_state.cleaned_df = cleaned_df

    # Create numeric cleaning column
    with cleaning_col2:
        st.write("**Numeric Columns**")

        # Filter numeric columns from data
        numeric_cols = cleaned_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        numeric_cols_with_nulls = [col for col in numeric_cols if cleaned_df[col].isnull().sum() > 0]

        # Create selectbox with options for numeric column cleaning
        if numeric_cols:
            numeric_method = st.selectbox(
                "Select method to handle missing values in numeric columns:",
                [
                    "Fill with Mean",
                    "Fill with Median",
                    "Fill with Mode",
                    "Forward Fill",
                    "Backward Fill",
                    "Fill with Custom Value"
                ]
            )
            numeric_input = None

            # Create extra input box if text cleaning option is 'fill with custom value'
            if numeric_method == "Fill with Custom Value":
                numeric_input = st.text_input("Enter Custom Input", key="num_input")
                
                # Make sure numeric input is a proper numeric value before proceeding 
                if numeric_input:
                    try:
                        numeric_input = float(numeric_input)
                    except:
                        st.error("Please enter a valid numeric value")
                        st.stop()
                else:
                    st.warning("Please enter a custom value before applying")

            # Create button to apply numeric column cleaning operations
            if st.button("Apply to Numeric Columns", type="primary", key="apply_numeric"):

                for col in numeric_cols_with_nulls:

                    # Numeric mean
                    if numeric_method == "Fill with Mean":
                        cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
                    # Numeric median
                    elif numeric_method == "Fill with Median":
                        cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
                    # Numeric mode
                    elif numeric_method == "Fill with Mode":
                        cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else 0, inplace=True)
                    # Numeric forward fill
                    elif numeric_method == "Forward Fill":
                        cleaned_df[col].ffill(inplace=True)
                    # Numeric backward fill
                    elif numeric_method == "Backward Fill":
                        cleaned_df[col].bfill(inplace=True)
                    # Numeric custom value
                    elif numeric_method == "Fill with Custom Value":
                        cleaned_df[col].fillna(numeric_input, inplace=True)

                # Save cleaned dataframe state
                st.session_state.cleaned_df = cleaned_df
    
    # Create data formatting column
    with cleaning_col3:
        st.write("**Data Formatting**")

        # Get text columns
        text_cols = cleaned_df.select_dtypes(include=['object']).columns.tolist()

        if text_cols:
            # Create selectbox for data formatting options
            format_method = st.selectbox(
                "Select method to apply formatting to text columns in dataset:",
                [
                    "Uppercase",
                    "Lowercase",
                    "Title Case",
                    "Strip Whitespace"
                ], key="format_method"
            )

            # Create button to apply data formatting
            if st.button("Apply to All Text", type='primary', key='apply_format'):
                for col in text_cols:
                    # Convert cols to string before formatting
                    cleaned_df[col] = cleaned_df[col].astype(str)

                    # Format uppercase
                    if format_method == "Uppercase":
                        cleaned_df[col] = cleaned_df[col].str.upper()
                    # Format lowercase
                    if format_method == "Lowercase":
                        cleaned_df[col] = cleaned_df[col].str.lower()
                    # Format title case
                    if format_method == "Title Case":
                        cleaned_df[col] = cleaned_df[col].str.title()
                    # Format strip whitespace
                    if format_method == "Strip Whitespace":
                        cleaned_df[col] = cleaned_df[col].str.strip()

                # Save cleaned data
                st.session_state.cleaned_df = cleaned_df

    # Create drop options column
    with cleaning_col4:
        st.write("**Drop Options**")

        # Create selectbox for drop choices
        drop_choice = st.selectbox(
            "Select method to handle rows, columns, and duplicates in dataset:",
            [
                "Drop Duplicate Rows",
                "Drop Rows with any Nulls",
                "Drop Columns with any Nulls"
            ], key='drop_choice'
        )

        # Create button to apply drop options
        if st.button("Apply Method", type="primary", key='apply_drop'):
            # Drop duplicate rows
            if drop_choice == "Drop Duplicate Rows":
                cleaned_df.drop_duplicates(inplace=True)
            # Drop rows with nulls
            elif drop_choice == "Drop Rows with any Nulls":
                cleaned_df.dropna(axis=0, inplace=True)
            # Drop columns with any nulls
            elif drop_choice == "Drop Columns with any Nulls":
                cleaned_df.dropna(axis=1, inplace=True)
            
            # Save cleaned data
            st.session_state.cleaned_df = cleaned_df
    
    # Load cleaned data preview
    load_cleaned_preview(cleaned_df)

    # Create columns for download and reset buttons
    button_col1, button_col2, button_col3 = st.columns(3)

    # Create button to reset cleaned dataframe
    with button_col1:
        if st.button("Reset Cleaned Dataframe"):
            if st.session_state.original_df is not None:
                st.session_state.cleaned_df = st.session_state.original_df.copy()
                st.rerun()
    
    # Create button to download cleaned csv data
    with button_col3:
        csv = st.session_state.cleaned_df.to_csv(index=False)
        st.download_button("Download Current Cleaned CSV", csv, "cleaned_data.csv", "text/csv")    