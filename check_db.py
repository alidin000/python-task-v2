import sqlite3

def check_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)

    # Describe a table
    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()
    print("Users Table Columns:", columns)

    # Query data
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    print("Users Table Data:", rows)

    conn.close()

check_db()
