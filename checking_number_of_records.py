import sqlite3

def get_total_records():
    # Connect to the SQLite database
    conn = sqlite3.connect('pubmed_articles.db')
    c = conn.cursor()
    
    # Execute a query to count the total number of records in the 'articles' table
    c.execute('SELECT COUNT(*) FROM articles')
    
    # Fetch the result, which is the total number of records
    total_records = c.fetchone()[0]
    
    # Close the database connection
    conn.close()
    
    return total_records

# Example usage
total_records = get_total_records()
print(f"Total number of records in the database: {total_records}")
