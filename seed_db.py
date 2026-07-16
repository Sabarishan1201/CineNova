import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

movies = [

    (
        "Interstellar",
        "Sci-Fi",
        2014,
        8.9,
        "2h 49m",
        "English",
        "interstellar.jpg",
        "interstellar-bg.jpg",
        "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "https://www.youtube.com/watch?v=zSWdZVtXT7E",
        "Christopher Nolan"
    ),

    (
        "Oppenheimer",
        "Drama",
        2023,
        8.6,
        "3h",
        "English",
        "oppenheimer.jpg",
        "oppenheimer-bg.jpg",
        "The story of physicist J. Robert Oppenheimer and the creation of the atomic bomb.",
        "https://www.youtube.com/watch?v=uYPbbksJxIg",
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
        "dark-knight-bg.jpg",
        "Batman faces the Joker, who plunges Gotham City into chaos.",
        "https://www.youtube.com/watch?v=EXeTwQWrcwY",
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
        "inception-bg.jpg",
        "A thief steals secrets through dream-sharing technology.",
        "https://www.youtube.com/watch?v=YoHD9XEInc0",
        "Christopher Nolan"
    )

]

cursor.executemany("""
INSERT INTO movies(
title,
genre,
year,
rating,
runtime,
language,
poster,
backdrop,
description,
trailer,
director
)

VALUES(?,?,?,?,?,?,?,?,?,?,?)

""", movies)

conn.commit()

conn.close()

print("✅ Movies Added Successfully")