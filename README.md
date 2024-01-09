# Spreadsheet Query UI

## Introduction
This Streamlit application provides a user-friendly interface for querying and managing data across multiple Excel spreadsheets. It leverages the power of Pandas for data manipulation and Streamlit for an interactive frontend, making it easy to filter and analyze data from various Excel files.

## Features
- **Excel File Management:** Upload and manage multiple Excel files (.xls, .xlsx, .xlsm, .xlsb).
- **Dynamic Data Parsing:** Parses sheets from uploaded Excel files into dataframes.
- **Column Name Standardization:** Standardizes column names for consistency across different sheets.
- **Search Functionality:** Provides options to search for common, rare, and unique fields across the data.
- **Customizable Search Options:** Select specific values for each field to narrow down the search.
- **Logical Search Operators:** Choose between "And" & "Or" logical operators for search queries.
- **Result Display:** Displays the search results with an option to view all columns or a limited view.

## Usage
1. **Start the Application:** Launch the Streamlit app to interact with the interface.
2. **Upload Excel Files:** Use the file uploader to add Excel files for querying.
3. **Manage Files:** Remove unwanted files from the session.
4. **Column Selection:** Choose from common, rare, and unique fields to create a search query.
5. **Define Search Criteria:** Select specific values for each chosen field.
6. **Execute Search:** Click the search button to execute the query.
7. **View Results:** Review the search results displayed on the interface.

## Installation
To get the application running locally:

1. Clone the repository:
`git clone https://github.com/carlosmbe/SpreadSheetQueryMagic`

2. Install dependencies using the requirements file: `pip install -r requirements.txt`

3. Run the application:
`streamlit run app.py`


## Contributing
Contributions are welcome and greatly appreciated. To contribute:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## Beautiful Pictures
<img width="1792" alt="Screenshot 2024-01-09 at 2 31 14 PM" src="https://github.com/carlosmbe/SpreadSheetQueryMagic/assets/53784701/e24938f6-e8f2-4ee9-99b1-ece33fc73eef">
<img width="1792" alt="Screenshot 2024-01-09 at 2 31 06 PM" src="https://github.com/carlosmbe/SpreadSheetQueryMagic/assets/53784701/2b46e4ed-0df7-45b6-aa0f-47a0fa182ed5">
<img width="1792" alt="Screenshot 2024-01-09 at 2 29 32 PM" src="https://github.com/carlosmbe/SpreadSheetQueryMagic/assets/53784701/273e2a99-7279-4866-9f83-4fa817f2dae0">
<img width="1792" alt="Screenshot 2024-01-09 at 2 29 19 PM" src="https://github.com/carlosmbe/SpreadSheetQueryMagic/assets/53784701/bb6185a9-ca13-446f-a85c-806e1d9f1e2e">


### The Spread Sheet in this video example has names removed for privacy reasons



https://github.com/carlosmbe/SpreadSheetQueryMagic/assets/53784701/0f31c1ad-1a07-4cad-a143-316120498741





## License
This project is licensed under the MIT License - see the `LICENSE` file for details.
