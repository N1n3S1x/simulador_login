import sqlite3


conn = sqlite3.connect('test.db')
c = conn.cursor()

# Drop the table if it exists
c.execute('DROP TABLE IF EXISTS users')
# Create a new table
c.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')



c.close()