import sqlite3

# Connect to the database
conn = sqlite3.connect('Chinook.db')
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])
    # Get schema for each table
    cursor.execute(f"PRAGMA table_info({table[0]})")
    schema = cursor.fetchall()
    print(f"Schema for {table[0]}:")
    for column in schema:
        print(f"  {column[1]} ({column[2]})")
    print()

conn.close()