from app.database import get_connection

conn = get_connection()

movies = conn.execute("SELECT * FROM movies").fetchall()

print("Total Movies:", len(movies))

for movie in movies:
    print(dict(movie))

conn.close()