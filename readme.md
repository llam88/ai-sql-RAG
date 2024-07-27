# AI-Powered SQL Query System with Email Functionality

## Table of Contents
- [System Overview](#system-overview)
- [LangChain's Role](#langchains-role)
- [Files in the Project](#files-in-the-project)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Email Configuration](#email-configuration)
- [Usage](#usage)
- [Database Information](#database-information)
- [Using DB Browser for SQLite](#using-db-browser-for-sqlite)
- [Potential for True RAG Adaptation](#potential-for-true-rag-adaptation)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## System Overview

This project implements an AI-assisted SQL query system that allows users to interact with a SQLite database using natural language. It demonstrates how AI can be used to bridge natural language and structured data queries. The system uses the Anthropic Claude AI model to interpret queries, generate SQL, and explain results, with the additional functionality of drafting and sending emails based on query results.

While it shares some similarities with RAG (Retrieval-Augmented Generation) systems, it differs in key ways:

- It queries structured data (SQL database) rather than unstructured text documents.
- The "retrieval" step is performed through SQL queries rather than semantic search.
- The AI is augmented with database schema information rather than retrieved text passages.

## LangChain's Role

LangChain plays a crucial role in this project:

1. Database Interaction: LangChain's `SQLDatabase` utility provides a simple interface for connecting to and querying the SQLite database.
2. AI Model Integration: LangChain's `ChatAnthropic` class provides a standardized way to interact with the Claude AI model.
3. Prompt Management: The project's structure is influenced by LangChain's approach to managing prompts and responses.
4. Extensibility: LangChain's modular design allows for easy extension of the system.

## Files in the Project

1. `test_chinook.py`: The main script that runs the AI-powered SQL query system.
2. `db_checker.py`: A utility script to check and display the structure of the SQLite database.

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- An email account for sending emails
- An Anthropic API key

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/llam88/ai-sql-query-system.git
   cd ai-sql-query-system
   ```

2. Install the required packages:
   ```
   pip install langchain langchain_community langchain_anthropic anthropic
   ```

3. Download the Chinook SQLite database and place it in the project directory. You can download it from [here](https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite).

4. Set up your environment variables:
   - Create a `.env` file in the project directory
   - Add your Anthropic API key:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     ```

5. Configure email settings in `test_chinook.py`:
   - Set `GMAIL_USER` to your email address
   - Set `GMAIL_PASSWORD` to your email password or app-specific password

## Email Configuration

The system currently uses Gmail SMTP for sending emails, but you can modify it to use other email providers:

### Gmail (Default)
- Ensure `GMAIL_USER` and `GMAIL_PASSWORD` are set correctly in `test_chinook.py`
- Use an app-specific password for added security

### Other Email Providers
To use a different email provider:

1. Open `test_chinook.py`
2. Locate the `send_email` function
3. Update the email configuration:
   ```python
   EMAIL_USER = "your_email@provider.com"
   EMAIL_PASSWORD = "your_email_password"
   SMTP_SERVER = "your_smtp_server"
   SMTP_PORT = your_smtp_port
   ```
4. Modify the email sending code accordingly

For specific instructions on setting up different email providers, consult your email service's SMTP documentation.

## Usage

1. Run the main script:
   ```
   python test_chinook.py
   ```

2. Follow the prompts to:
   - Enter natural language queries about the Chinook database
   - View AI-generated SQL and interpretations of results
   - Optionally draft and send emails based on query results

3. To check the database structure, run:
   ```
   python db_checker.py
   ```

Enter 'exit' when prompted for a query to quit the program.

## Database Information

The system uses the Chinook sample database, which contains information about a digital media store. Tables include:

- Album
- Artist
- Customer
- Employee
- Genre
- Invoice
- InvoiceLine
- MediaType
- Playlist
- PlaylistTrack
- Track

Use the `db_checker.py` script to view detailed schema information.

## Using DB Browser for SQLite

DB Browser for SQLite is a high quality, visual, open source tool to create, design, and edit database files compatible with SQLite.

### Installation

1. Visit the [DB Browser for SQLite website](https://sqlitebrowser.org/dl/).
2. Download and install the appropriate version for your operating system.

### Opening the Chinook Database

1. Launch DB Browser for SQLite.
2. Click on "Open Database" and select your Chinook_Sqlite.sqlite file.

### Exploring the Database

1. Use the "Database Structure" tab to see all tables.
2. Use the "Browse Data" tab to view table contents.

### Executing SQL Queries

1. Go to the "Execute SQL" tab.
2. Enter your SQL query and click "Execute".

### Tips for Testing

- Verify AI-generated query results.
- Experiment with your own SQL queries.
- Use the "Plot" functionality to visualize results (if available).

## Potential for True RAG Adaptation

To evolve this into a true RAG system, consider:

1. Creating text embeddings of your database content.
2. Using a vector database to store these embeddings.
3. Implementing similarity search for relevant database content retrieval.
4. Using retrieved content to augment the AI's knowledge before generating responses.

## Future Enhancements

- Implement full RAG capabilities with document embedding and vector search.
- Add support for multiple AI providers.
- Extend support for various database types beyond SQLite.
- Improve error handling and user input validation.
- Implement a graphical user interface.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Anthropic for the Claude AI model
- SQLite and the Chinook sample database creators
- LangChain library developers

For any questions or issues, please open an issue in the GitHub repository.
