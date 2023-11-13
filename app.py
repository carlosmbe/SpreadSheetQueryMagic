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

    if uploaded_file is not None:
        xls = pd.ExcelFile(BytesIO(uploaded_file.read()))
        filepaths = {uploaded_file.name: xls}
        st.session_state['uploaded_files'].update(filepaths)

    if st.session_state['uploaded_files']:
        remove_file = st.selectbox('Select a file to remove', list(st.session_state['uploaded_files']))
        if st.button('Remove File'):
            st.session_state['uploaded_files'].pop(remove_file)

data = {}
original_column_names = {}

for path, xls in st.session_state['uploaded_files'].items():
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name, dtype=str)
        original_column_names.update({col.lower().replace(' ', '_').replace(r'\W', ''): col for col in df.columns})
        df.columns = df.columns.str.replace(' ', '_').str.replace(r'\W', '').str.lower()
        data[f'{path}_{sheet_name}'] = df

column_names = [col for df in data.values() for col in df.columns]
counter = Counter(column_names)
common_columns = [name for name, count in counter.items() if count > 2]
rare_columns = [name for name, count in counter.items() if count == 2]
unique_columns = [name for name, count in counter.items() if count == 1]

st.subheader('Pick Terms to Search For')
st.markdown('### Common Fields')
selected_common_columns = [column for column in common_columns if st.checkbox(original_column_names.get(column, column), key=f'common_{column}')]

with st.expander("Rare Fields"):
    selected_rare_columns = [column for column in rare_columns if st.checkbox(original_column_names.get(column, column), key=f'rare_{column}')]

with st.expander("Unique Fields"):
    selected_unique_columns = [column for column in unique_columns if st.checkbox(original_column_names.get(column, column), key=f'unique_{column}')]

selected_columns = selected_common_columns + selected_rare_columns + selected_unique_columns
selected_values = {}
for column in selected_columns:
    options = list(set(str(val) for df in data.values() if column in df.columns for val in df[column].dropna().unique()))
    selected_values[column] = st.selectbox(f"{original_column_names.get(column, column)} values", options, key=f'selectbox_{column}')

logical_operator = st.selectbox("Logical Operator", options=["And", "Or"], index=0)
view_all_columns = st.checkbox('View all columns in results')

if st.button("🔍 Search 🔎"):
    results = []
    for name, df in data.items():
        conditions = [df[column] == selected_values[column] for column in selected_values if column in df.columns]
        if conditions:
            matched_df = df[reduce(lambda a, b: a | b, conditions) if logical_operator == "Or" else reduce(lambda a, b: a & b, conditions)]
            if not matched_df.empty:
                results.append({'name': name, 'data': matched_df})

    if results:
        st.subheader('Global Search Results')
        for result in results:
            st.markdown(f'### {result["name"]}')
            st.dataframe(result['data'] if view_all_columns else result['data'].iloc[:, :3])
    else:
        st.write('No results found')
