import sqlite3

email = input("Enter your email: ")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
    "UPDATE users SET is_admin = 1 WHERE email = ?",
    (email,)
)

conn.commit()

if cursor.rowcount > 0:
    print("✅ User is now an admin.")
else:
    print("❌ No user found with that email.")

conn.close()