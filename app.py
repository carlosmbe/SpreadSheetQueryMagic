import streamlit as st
import pandas as pd
from functools import reduce
from collections import Counter
from io import BytesIO

st.header('Spreadsheet Query UI')

# Initialize the session state
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = {}

# Use st.expander for file management section
with st.expander('File Management'):
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xls', 'xlsx', 'xlsm', 'xlsb'])

    # Load data from uploaded Excel files into a dictionary of DataFrames
    if uploaded_file is not None:
        xls = pd.ExcelFile(BytesIO(uploaded_file.read()))
        filepaths = {uploaded_file.name: xls}
        st.session_state['uploaded_files'].update(filepaths)

    # Allow user to remove files
    if st.session_state['uploaded_files']:
        remove_file = st.selectbox('Select a file to remove', list(st.session_state['uploaded_files']))
        if st.button('Remove File'):
            st.session_state['uploaded_files'].pop(remove_file)

data = {}
original_column_names = {}

for path, xls in st.session_state['uploaded_files'].items():
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name, dtype=str)  # Ensure all data is loaded as strings

        # Replace spaces with underscores and remove special characters
        original_column_names.update({col.lower().replace(' ', '_').replace(r'\W', ''): col for col in df.columns})
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace(r'\W', '')
        df.columns = df.columns.str.lower()

        data[f'{path}_{sheet_name}'] = df

# Gather all column names across all DataFrames
column_names = [col for df in data.values() for col in df.columns]

# Count the frequency of each column name
counter = Counter(column_names)
common_columns = [name for name, count in counter.items() if count > 2]
rare_columns = [name for name, count in counter.items() if count == 2]
unique_columns = [name for name, count in counter.items() if count == 1]

st.subheader('Pick Terms to Search For')

# Generate column checkboxes under their respective subheaders
st.markdown('### Common Fields')
selected_common_columns = [column for column in common_columns if st.checkbox(original_column_names[column], key=f'common_{column}')]

with st.expander("Rare Fields"):
    selected_rare_columns = [column for column in rare_columns if st.checkbox(original_column_names[column], key=f'rare_{column}')]

with st.expander("Unique Fields"):
    selected_unique_columns = [column for column in unique_columns if st.checkbox(original_column_names[column], key=f'unique_{column}')]

# Combine all selected columns
selected_columns = selected_common_columns + selected_rare_columns + selected_unique_columns

# Generate dropdowns for selected columns
selected_values = {}
for column in selected_columns:
    options = list(set([str(val) for df in data.values() if column in df.columns for val in df[column].dropna().unique()]))
    selected_values[column] = st.selectbox(f"{original_column_names[column]} values", options, key=f'selectbox_{column}')

# Select logical operator
logical_operator = st.selectbox("Logical Operator", options=["And", "Or"], index=0)
view_all_columns = st.checkbox('View all columns in results')

if st.button("🔍 Search 🔎"):
    results = []
    # Iterate through all DataFrames and filter rows
    for name, df in data.items():
        if logical_operator == "Or":
            conditions = [df[column] == selected_values[column] for column in selected_values if column in df.columns]
            if conditions:  # if there is at least one condition
                matched_df = df[reduce(lambda a, b: a | b, conditions)]
                if not matched_df.empty:
                    results.append({'name': name, 'data': matched_df})
        else:  # "And" operator
            conditions = [df[column] == selected_values[column] for column in selected_values if column in df.columns]
            if conditions:  # if there is at least one condition
                matched_df = df[reduce(lambda a, b: a & b, conditions)]
                if not matched_df.empty:
                    results.append({'name': name, 'data': matched_df})

    # If there are any results, display them
    if results:
        st.subheader('Global Search Results')
        for result in results:
            st.markdown(f'### {result["name"]}')
            # Display all columns if the checkbox is checked, else display the first three columns
            st.dataframe(result['data'] if view_all_columns else result['data'].iloc[:, :3])
    else:
        st.write('No results found')

