from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import pandas as pd
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to convert CSV to SQLite database
def csv_to_db(csv_file, db_file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        
        # Connect to (or create) the SQLite database
        conn = sqlite3.connect(db_file)
        
        # Export the DataFrame to the SQLite database
        df.to_sql('TEST', conn, if_exists='replace', index=False)
        
        # Close the database connection
        conn.close()
        st.success(f"CSV file '{csv_file.name}' has been successfully converted to '{db_file}'.")
    except Exception as e:
        st.error(f"Error converting CSV to DB: {e}")

# Function to get response from Gemini model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    # Join the list into a single string
    combined_prompt = "\n".join(prompt)
    # Generate content based on the combined prompt and question
    response = model.generate_content(combined_prompt + "\n" + question)
    return response.text

# Function to extract table schema and pass it to the prompt
def get_db_schema(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = "Database Schema:\n"
    for table in tables:
        table_name = table[0]
        schema += f"Table: {table_name}\n"
        
        # Get column names for the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema += "Columns: " + ", ".join([col[1] for col in columns]) + "\n"
        
    conn.close()
    return schema

# Function to execute the SQL query with error handling
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        curr = conn.cursor()
        # Execute the SQL query
        curr.execute(sql)
        rows = curr.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.OperationalError as e:
        # Print error to Streamlit and return None
        st.error(f"SQL Execution Error: {e}")
        return None

# SQL Prompt
base_prompt = [
"""
You are an expert in converting English questions to SQL query!
Read the SQL database headers and the columns.
For example:

1. "Tell me all the students studying in Data Science class?"
   SQL Query: SELECT * FROM "TABLE NAME" WHERE CLASS = "DATA science";

English Question: 'List all employees working in the Marketing department who joined the company after January 1, 2020, and have a salary greater than $50,000.'
SQL Query: SELECT * FROM "Employees" WHERE "Department" = 'Marketing' AND "JoinDate" > '2020-01-01' AND "Salary" > 50000;

English Question: 'What are the total sales and average order value for each product category in the last quarter, sorted by highest sales first?'
SQL Query: SELECT "Category", SUM("Sales") AS "TotalSales", AVG("OrderValue") AS "AvgOrderValue" FROM "Orders" WHERE "OrderDate" BETWEEN '2023-07-01' AND '2023-09-30' GROUP BY "Category" ORDER BY "TotalSales" DESC;

and make sure you give just the response not to give "your generated response is this..." or "The generated query is this..." or "Here is your response..."
"""
]

# Streamlit App for Chatbot
st.set_page_config(page_title="MySQL Chatbot")
st.header("Ask any thing to your own MySQL Chatbot")

# Initialize the conversation
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input through chat
if prompt := st.chat_input("Ask about the SQL data"):
    # Add user message to conversation
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ensure the database file exists before proceeding
    if not os.path.exists("TEST.db"):
        bot_reply = "No database found. Please upload a CSV file first."
    else:
        # Get database schema
        schema = get_db_schema("TEST.db")
        
        # Combine the base prompt with schema for accurate context
        full_prompt = base_prompt + [schema]
        
        # Get response from the Gemini model
        response = get_gemini_response(prompt, full_prompt)

        # If the response is valid, display the query results
        if response.strip().lower().startswith("select"):
            data = read_sql_query(response, "TEST.db")
            bot_reply = f"Generated SQL Query:\n```{response}```\n\n"

            if data:
                bot_reply += "Query Results:\n"
                for row in data:
                    bot_reply += f"{row}\n"
            else:
                bot_reply += "No data found or invalid query."
        else:
            bot_reply = "Generated SQL query is not valid or does not start with SELECT."

    # Add bot reply to conversation
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Display bot message in chat
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# File uploader for CSV to SQLite conversion
st.sidebar.header("Upload a CSV file")
csv_file = st.sidebar.file_uploader("Upload a CSV file to convert it to a SQLite database", type=["csv"])

if csv_file:
    db_file = "TEST.db"
    # Convert the uploaded CSV to a SQLite database
    csv_to_db(csv_file, db_file)
