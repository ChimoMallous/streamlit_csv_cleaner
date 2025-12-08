# Streamlit CSV Cleaner

This program creates an interactive CSV-cleaning tool that allows users to upload and preview a CSV file, see data descriptions, apply various cleaning operations, visualize missing values, and download the cleaned results. It is built with Streamlit, Pandas, and Plotly to make data cleaning simple and accessible.

## Project Status: In Progress

This project is still being developed and is not yet fully finished.

## Current Features

- Displays the first 8 rows of the uploaded data  
- Shows data description such as column names, dtypes, and example values  
- Summary information including:  
  - Numeric null counts per column  
  - Text null counts per column  
  - Total number of null values  
  - Duplicate row count  
- Bar chart visualization of null values per column  
- Numeric cleaning options (with support for custom input values)  
- Text cleaning options (with support for custom input values)  
- Data formatting options  
- Drop operations (for removing columns or specific rows)  
- Preview of cleaned data  
- Download cleaned CSV file  

## How to Run

Install the required libraries:

```bash
pip install streamlit pandas plotly
```

Run the application:

```bash
streamlit run csv_cleaner_app.py
```


