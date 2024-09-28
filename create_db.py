import sqlite3

# Create SQLite database and users table
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        bio TEXT NOT NULL
    )
''')

conn.commit()
conn.close()