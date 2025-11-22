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
            null_sum_fig = px.bar(x=null_summary.index, y=null_summary.values,
                                labels={'x': 'Column', 'y': 'Null Count'})
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
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()


