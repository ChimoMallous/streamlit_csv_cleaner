WORK IN PROGRESS
This project is currently under development, see planned features for future additions.

Streamlit CSV Cleaner

This program creates an interactive CSV cleaning tool built with streamlit, pandas, and plotly to allow the user to upload and preview a CSV file, analyze null values, visualize missing data, apply a wide range of cleaning operations, and then finally download that cleaned data without having to write any code.

Current Features
- Displays first 8 rows of data
- Shows data description
- Summaries of:
    - Numerical null counts
    - Text null counts
    - Total null values
    - Duplicate row count
- Displays bar chart of null values by column

Planned features
- Numeric column cleaning options
- Text column cleaning options
- Drop operations
- Preview of cleaned data
- Ability to download cleaned data
- Restart session data
- Improved UI and layout

How to run app
- Install dependencies:
    - pip install streamlit pandas plotly
- Run the app:
    - type "Streamlit run csv_cleaner_app.py" to run file in streamlit




