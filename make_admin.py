import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

email = "sabarishan1201@gmail.com"   # Replace with your login email

cursor.execute(
    "UPDATE users SET is_admin = 1 WHERE email = ?",
    (email,)
)

conn.commit()

print("Rows updated:", cursor.rowcount)

conn.close()