
The AI-powered SQL Chatbot is a web application that allows users to interact with databases using natural language queries. It leverages Streamlit and Google Gemini API to convert user questions into SQL statements, making data extraction intuitive and accessible.

##Features
Upload CSV files to create SQLite databases.
Generate SQL queries from natural language questions.
Display query results in real time.

##Requirements
Python 3.x
Streamlit
pandas
google-generativeai
sqlite3
python-dotenv
Installation
Clone the repository:

python -m venv venv
source 'venv/bin/activate'   # On Windows use `venv\Scripts\activate`
Install the required packages:


pip install -r requirements.txt
Create a .env file in the project directory and add your Google API key:

Create a .env file 
GOOGLE_API_KEY=your_api_key_here

##Running the Application
Start the Streamlit application:
streamlit run app.py

##Open your web browser and go to http://localhost:8501 to access the chatbot interface.

##Usage
-Upload a CSV file using the sidebar to create a SQLite database.
-Enter your SQL-related questions in the chat input field and hit "Send."
-View the generated SQL queries and their results in real time.
