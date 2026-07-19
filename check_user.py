import sqlite3

conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

users = cursor.execute("SELECT * FROM users").fetchall()

print(f"Total Users: {len(users)}\n")

for user in users:
    print(dict(user))

conn.close()