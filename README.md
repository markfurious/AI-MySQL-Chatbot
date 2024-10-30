

# Streamlit SQL Chatbot

Welcome to the **Streamlit SQL Chatbot**! This application allows users to interact with a SQLite database using natural language questions, generating SQL queries based on user input.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)

## Features

- **Natural Language Processing**: Convert English questions into SQL queries.
- **Database Management**: Upload CSV files to create or update a SQLite database.
- **Query Execution**: Execute generated SQL queries and display results.
- **User-Friendly Interface**: Easy-to-use chat interface with Streamlit.

## Installation

To run this application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/markfurious/AI-MySQL-Chatbot.git
   cd sql-chatbot
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables. Create a `.env` file in the root directory of the project and add your Google API key:

   ```plaintext
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`.

3. Use the sidebar to upload a CSV file. The application will convert it into a SQLite database.

4. Use the chat interface to ask questions about the data. The chatbot will generate SQL queries and return the results.

## How It Works

- **CSV to SQLite Conversion**: The application allows users to upload a CSV file, which is then read into a Pandas DataFrame and exported to a SQLite database.
- **Schema Extraction**: The application retrieves the database schema and prepares it for the AI model.
- **Query Generation**: Using the Google Gemini API, the application converts natural language questions into SQL queries based on the schema.
- **SQL Execution**: The generated SQL queries are executed against the SQLite database, and the results are displayed in the chat interface.

### Code Overview

The application consists of several key functions:

- `csv_to_db(csv_file, db_file)`: Converts a CSV file into a SQLite database.
- `get_gemini_response(question, prompt)`: Interacts with the Google Gemini API to generate SQL queries from natural language questions.
- `get_db_schema(db)`: Extracts the schema of the SQLite database to provide context for the AI model.
- `read_sql_query(sql, db)`: Executes a SQL query on the database and returns the results.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request. 

### Reporting Issues

If you encounter any issues, please open an issue in the repository.


### Notes:
- Replace `yourusername` in the clone URL with your actual GitHub username.
- Ensure you create a `requirements.txt` file that includes all necessary Python dependencies for your application (like `streamlit`, `pandas`, `sqlite3`, `python-dotenv`, and `google-generativeai`).
- Add a `LICENSE` file if you intend to distribute the project or want to specify the terms of use.

Feel free to modify any sections or add more details as needed! Let me know if you need any more help.
