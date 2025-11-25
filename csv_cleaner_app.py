# Imports
import streamlit as st
import plotly.express as px
import pandas as pd

# Set page layout
st.set_page_config(layout="wide")
st.title("CSV Data Cleaner")

# Initialize cleaned dataframe
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None

# Create function to load data and data preview
def load_data_preview(file):
    
    # Read CSV and create copy
    if st.session_state.cleaned_df is None:
        df = pd.read_csv(file)
        st.session_state.cleaned_df = df.copy()
    else:
        df = pd.read_csv(file)
    
    # Create data info expanders for data preview
    st.subheader("Original Data Preview")
    expander_tab1, expander_tab2 = st.columns(2)

    with expander_tab1:
        with st.expander("Data Head"):
            st.dataframe(df.head(8))
    with expander_tab2:
        with st.expander("Data Description"):
            st.dataframe(df.describe())
    st.divider()

    # Collect null counts from data
    num_null_count = df.select_dtypes(include=['int64', 'float64']).isnull().sum().sum()
    text_null_count = df.select_dtypes(include=['object']).isnull().sum().sum()
    total_null_count = df.isnull().sum().sum()
    total_duplicate_count = df.duplicated().sum()

    # Display null data info
    info_col1, info_col2, info_col3, info_col4 = st.columns(4)

    with info_col1:
        st.metric("Numerical Null Count:", f"{num_null_count:,}")
    with info_col2:
        st.metric("Text Null Count:", f"{text_null_count:,}")
    with info_col3:
        st.metric("Total Null Count:", f"{total_null_count:,}")
    with info_col4:
        st.metric("Total Duplicate Count:", f"{total_duplicate_count:,}")
    
    # Null columns charts
    null_chart_col1, null_chart_col2 = st.columns(2)

    with null_chart_col1:
        # Show which columns have nulls
        st.subheader("Null Values by Column")
        null_summary = df.isnull().sum()
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
        cols_with_nulls = [col for col in df.columns if df[col].isnull().sum() > 0]
        col_stats = pd.DataFrame({
            "Column": cols_with_nulls,
            "Missing": [df[col].isnull().sum() for col in cols_with_nulls],
            "Filled": [df[col].notnull().sum() for col in cols_with_nulls]  
        })
        null_vs_fill_fig = px.bar(
            col_stats,
            x="Column",
            y=["Missing", "Filled"],
            barmode="stack",
            color_discrete_sequence=["#B80000", "#006747"])
        
        st.plotly_chart(null_vs_fill_fig)

    
# Create CSV uploader
uploaded = st.file_uploader("Upload CSV Data")

# Load data when uploaded
if uploaded:
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
    cleaning_col1, cleaning_col2, cleaning_col3 = st.columns(3)

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

