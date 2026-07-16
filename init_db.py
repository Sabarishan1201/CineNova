import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT,

    genre TEXT,

    year INTEGER,

    rating REAL,

    runtime TEXT,

    language TEXT,

    poster TEXT,

    backdrop TEXT,

    description TEXT,

    trailer TEXT,

    director TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    email TEXT,

    password TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    movie_id INTEGER

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    movie_id INTEGER,

    username TEXT,

    rating INTEGER,

    review TEXT,

    date TEXT

)
""")

conn.commit()

conn.close()

print("✅ Database Created Successfully")