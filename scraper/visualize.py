import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Fetch headlines from the SQLite database
def fetch_headlines():
    conn = sqlite3.connect('bbc_news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT headline FROM headlines')
    rows = cursor.fetchall()
    conn.close()
    
    return [row[0] for row in rows]

# Fetch the headlines
headlines = fetch_headlines()

# Keywords to search for
keywords = ['politics', 'economy', 'science', 'technology', 'world']

# Create a dictionary to count occurrences of each keyword
keyword_counts = {keyword: sum(keyword.lower() in headline.lower() for headline in headlines) for keyword in keywords}

# Create a DataFrame for visualization
df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Count'])

# Save the keyword counts to a CSV file
if not os.path.exists('data'):
    os.makedirs('data')  # Create the directory if it doesn't exist
file_path = 'data/keyword_counts.csv'  # Define the file path
df.to_csv(file_path, index=False)  # Save the DataFrame as a CSV file

print(f"Keyword counts saved to {file_path}")

# Plot a bar chart
df.plot(kind='bar', x='Keyword', y='Count', legend=False, color='skyblue', figsize=(10, 6))
plt.title('Keyword Frequency in Headlines')
plt.xlabel('Keyword')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
