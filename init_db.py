import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Movies table
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

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
)
""")

# Watchlist table
cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER
)
""")

# Reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    rating INTEGER NOT NULL,
    review TEXT,
    date TEXT,
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("✅ Database Created Successfully")