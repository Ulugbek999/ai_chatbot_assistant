import sqlite3

#function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect("clothing.db")
    conn.row_factory = sqlite3.Row #to make rows dict-like for easier access
    return conn

def connect_db_tech():
    conn = sqlite3.connect('tech.db')
    conn.row_factory = sqlite3.Row #to make rows dict-like
    return conn


