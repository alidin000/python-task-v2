import sqlite3

def check_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)

    # Describe a table
    cursor.execute("PRAGMA table_info(auto_response_settings);")
    columns = cursor.fetchall()
    print("auto_response_settings Table Columns:", columns)

    # Query data
    cursor.execute("SELECT * FROM auto_response_settings;")
    rows = cursor.fetchall()
    print("auto_response_settings Table Data:", rows)

    conn.close()

check_db()
