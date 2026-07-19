from app.database import get_connection

conn = get_connection()

movies = [
    (
        "Interstellar",
        "Sci-Fi",
        2014,
        8.7,
        "2h 49m",
        "English",
        "interstellar.jpg",
        "",
        "A team travels through a wormhole in search of humanity's future.",
        "https://www.youtube.com/embed/zSWdZVtXT7E",
        "Christopher Nolan"
    ),
    (
        "Oppenheimer",
        "Biography",
        2023,
        8.5,
        "3h",
        "English",
        "oppenheimer.jpg",
        "",
        "The story of J. Robert Oppenheimer and the atomic bomb.",
        "https://www.youtube.com/embed/uYPbbksJxIg",
        "Christopher Nolan"
    ),
    (
        "Inception",
        "Sci-Fi",
        2010,
        8.8,
        "2h 28m",
        "English",
        "inception.jpg",
        "",
        "A thief enters dreams to steal secrets.",
        "https://www.youtube.com/embed/YoHD9XEInc0",
        "Christopher Nolan"
    ),
    (
        "The Dark Knight",
        "Action",
        2008,
        9.0,
        "2h 32m",
        "English",
        "dark-knight.jpg",
        "",
        "Batman faces the Joker.",
        "https://www.youtube.com/embed/EXeTwQWrcwY",
        "Christopher Nolan"
    )
]

for movie in movies:
    conn.execute("""
        INSERT INTO movies
        (title, genre, year, rating, runtime, language, poster, backdrop, description, trailer, director)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, movie)

conn.commit()
conn.close()

print("Movies added successfully!")