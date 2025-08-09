import sqlite3

def fetch_headlines():
    # Connect to SQLite database
    conn = sqlite3.connect('bbc_news.db')
    cursor = conn.cursor()

    # Retrieve all headlines from the database
    cursor.execute('SELECT * FROM headlines')
    rows = cursor.fetchall()

    # Print the headlines
    for row in rows:
        print(row[1])  # Only print the headline (column 1)

    # Close the database connection
    conn.close()

# Call the function to test
fetch_headlines()
