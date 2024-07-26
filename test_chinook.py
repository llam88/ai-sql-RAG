import os
import sys
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_community.utilities import SQLDatabase
from langchain_anthropic import ChatAnthropic

# Set up your Claude API key
os.environ["ANTHROPIC_API_KEY"] = "YOUR-CLAUDE-KEY-HERE"

# Email configuration
GMAIL_USER = "YOUR-GMAIL-HERE"
GMAIL_PASSWORD = "GMAIL_PASSWORD_APP_PASSWORD"

# Connect to the Chinook database
try:
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")
    print("Successfully connected to the database.")
    print(f"Tables in the database: {db.get_usable_table_names()}")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    sys.exit(1)

# Function to get all table schemas
def get_all_schemas():
    schemas = {}
    try:
        conn = sqlite3.connect('Chinook.db')
        cursor = conn.cursor()
        
        for table in db.get_usable_table_names():
            cursor.execute(f"PRAGMA table_info({table})")
            schema = cursor.fetchall()
            schemas[table] = "\n".join([f"{col[1]} ({col[2]})" for col in schema])
        
        conn.close()
        return schemas
    except Exception as e:
        print(f"Error getting schemas: {e}")
        return {}

# Set up Claude model
claude = ChatAnthropic(model="claude-2.1")

# Get all schemas
all_schemas = get_all_schemas()
schema_str = "\n\n".join([f"Table: {table}\nSchema:\n{schema}" for table, schema in all_schemas.items()])

# Function to extract SQL query from Claude's response
def extract_sql_query(response):
    match = re.search(r'```sql\n(.*?)\n```', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r'SELECT.*?;', response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return response.strip()

# Function to draft email content
def draft_email(query_result, recipient_name, user_requirements):
    prompt = f"""Based on the following query result, recipient name, and user requirements, draft a professional email:

Query Result:
{query_result}

Recipient Name: {recipient_name}

User Requirements:
{user_requirements}

The email should be concise, professional, and address the user's specific requirements while incorporating relevant information from the query result.
Do not include any email headers or footers, just the body of the email."""

    response = claude.invoke(prompt)
    return response.content

# Function to send email
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")

# Main function to process queries
def process_query(query):
    try:
        sql_prompt = f"""You are an AI assistant helping with SQL queries for a SQLite database. Here are the schemas of the tables in the database:

{schema_str}

User query: {query}

Please note:
1. This is a SQLite database, which doesn't support the TOP keyword. Use LIMIT instead for selecting a specific number of rows.
2. When asked about "top" items, consider what criteria might be appropriate (e.g., most tracks, highest sales, most recent, etc.).
3. If the query is ambiguous, make a reasonable assumption and explain your interpretation in a comment.

Based on the schemas provided and these notes, please suggest an appropriate SQL query to answer the user's question. Your response should include:
1. A brief comment explaining your interpretation of the query and any assumptions made.
2. The SQL query itself, enclosed in triple backticks with the sql language specifier.

Example:
-- Assuming "top albums" means albums with the most tracks
```sql
SELECT a.Title, ar.Name AS ArtistName, COUNT(t.TrackId) AS TrackCount
FROM Album a
JOIN Artist ar ON a.ArtistId = ar.ArtistId
JOIN Track t ON a.AlbumId = t.AlbumId
GROUP BY a.AlbumId
ORDER BY TrackCount DESC
LIMIT 10;
```"""

        sql_response = claude.invoke(sql_prompt)
        sql_query = extract_sql_query(sql_response.content)

        result = db.run(sql_query)

        interpret_prompt = f"""You are an AI assistant helping with SQL queries for a database. The user asked the following question:

{query}

The following SQL query was executed:

{sql_query}

And here are the results:

{result}

Please interpret these results and answer the user's question in natural language. Provide a concise summary of the information, highlighting key points or interesting findings. If the result is empty or if there's an error, please mention that as well."""

        interpretation = claude.invoke(interpret_prompt)
        return interpretation.content, result

    except Exception as e:
        return f"Error processing query: {str(e)}", None

# Main loop
def main():
    print("Claude-powered SQL RAG System with Email Functionality initialized. Ready for queries!")
    while True:
        query = input("Enter your question about the Chinook database (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        response, result = process_query(query)
        print("Claude's response:", response)
        
        if result:
            send_email_option = input("Would you like to draft and send an email based on this result? (yes/no): ")
            if send_email_option.lower() == 'yes':
                recipient_name = input("Enter the recipient's name: ")
                recipient_email = input("Enter the recipient's email: ")
                email_subject = input("Enter the email subject: ")
                user_requirements = input("What specific requirements do you have for this email? (e.g., purpose, tone, key points to include): ")
                
                email_body = draft_email(result, recipient_name, user_requirements)
                print("\nDrafted Email:")
                print(email_body)
                
                edit_option = input("\nWould you like to refine this email? (yes/no): ")
                while edit_option.lower() == 'yes':
                    user_feedback = input("Please provide feedback or additional requirements for the email: ")
                    email_body = draft_email(result, recipient_name, user_feedback)
                    print("\nUpdated Email:")
                    print(email_body)
                    edit_option = input("\nWould you like to refine this email further? (yes/no): ")
                
                send_option = input("\nWould you like to send this email? (yes/no): ")
                if send_option.lower() == 'yes':
                    try:
                        send_email(recipient_email, email_subject, email_body)
                    except Exception as e:
                        print(f"Error sending email: {str(e)}")

if __name__ == "__main__":
    main()