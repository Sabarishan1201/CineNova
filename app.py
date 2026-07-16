from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_connection
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.secret_key = "cinenova_secret_key"
UPLOAD_FOLDER = "app/static/images/movies"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def save_image(file):

    if file and allowed_file(file.filename):

        extension = file.filename.rsplit(".", 1)[1].lower()

        filename = f"{uuid.uuid4()}.{extension}"

        file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        return filename

    return None
# =====================================================
# Trending Movies
# =====================================================



# =====================================================
# Genres
# =====================================================

genres = [

    {"name": "Action", "icon": "🔥"},
    {"name": "Sci-Fi", "icon": "🚀"},
    {"name": "Comedy", "icon": "😂"},
    {"name": "Horror", "icon": "👻"},
    {"name": "Romance", "icon": "❤️"},
    {"name": "Adventure", "icon": "🏔️"}

]

# =====================================================
# Top Rated Movies
# =====================================================

top_movies = [

    {
        "title": "The Shawshank Redemption",
        "rating": "9.3",
        "genre": "Drama",
        "year": "1994",
        "poster": None,
        "description": "Two imprisoned men bond over decades while finding hope and redemption."
    },

    {
        "title": "The Godfather",
        "rating": "9.2",
        "genre": "Crime",
        "year": "1972",
        "poster": None,
        "description": "The aging patriarch of an organized crime dynasty transfers control to his son."
    },

    {
        "title": "The Dark Knight",
        "rating": "9.0",
        "genre": "Action",
        "year": "2008",
        "poster": "dark-knight.jpg",
        "description": "Batman faces the Joker, who spreads fear throughout Gotham."
    },

    {
        "title": "12 Angry Men",
        "rating": "9.0",
        "genre": "Drama",
        "year": "1957",
        "poster": None,
        "description": "A jury debates the guilt of a young defendant in a murder trial."
    }

]

# =====================================================
# Web Series
# =====================================================

web_series = [

    {
        "title": "Stranger Things",
        "rating": "8.7",
        "genre": "Sci-Fi",
        "year": "2016",
        "poster": None,
        "description": "A group of friends uncover supernatural mysteries in their town."
    },

    {
        "title": "Breaking Bad",
        "rating": "9.5",
        "genre": "Crime",
        "year": "2008",
        "poster": None,
        "description": "A chemistry teacher turns to manufacturing drugs after a terminal diagnosis."
    },

    {
        "title": "Dark",
        "rating": "8.8",
        "genre": "Mystery",
        "year": "2017",
        "poster": None,
        "description": "Families discover a mysterious time travel conspiracy."
    },

    {
        "title": "Money Heist",
        "rating": "8.2",
        "genre": "Thriller",
        "year": "2017",
        "poster": None,
        "description": "A criminal mastermind plans the biggest heist in history."
    }

]

# =====================================================
# Reviews
# =====================================================

reviews = [

    {
        "user": "Sabari",
        "movie": "Interstellar",
        "rating": 5,
        "review": "One of the greatest sci-fi movies ever made."
    },

    {
        "user": "Priya",
        "movie": "Oppenheimer",
        "rating": 4,
        "review": "Excellent storytelling and brilliant performances."
    },

    {
        "user": "Arun",
        "movie": "The Dark Knight",
        "rating": 5,
        "review": "The best superhero movie ever made."
    }

]

# =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    conn = get_connection()

    movies = conn.execute(
        "SELECT * FROM movies"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        movies=movies,
        genres=genres,
        top_movies=top_movies,
        web_series=web_series,
        reviews=reviews
    )
# =====================================================
# Movie Details
# =====================================================

@app.route("/movie/<title>")
def movie_details(title):

    conn = get_connection()

    movie = conn.execute(
        "SELECT * FROM movies WHERE title = ?",
        (title,)
    ).fetchone()

    conn.close()

    if movie is None:
        return "Movie Not Found", 404

    return render_template(
        "movie-details.html",
        movie=movie
    )
    # ==========================================
# Register
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# =====================================================
# Run Application
# =====================================================
# ==========================================
# Login
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]

            return redirect(url_for("home"))

        return "Invalid Email or Password"

    return render_template("login.html")
# ==========================================
# Logout
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))
# ==========================================
# Watchlist
# ==========================================

@app.route("/watchlist")
def watchlist():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    movies = conn.execute("""
        SELECT movies.*
        FROM watchlist
        JOIN movies
        ON watchlist.movie_id = movies.id
        WHERE watchlist.user_id = ?
    """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template(
        "watchlist.html",
        movies=movies
    )
# ==========================================
# Add to Watchlist
# ==========================================

@app.route("/watchlist/add/<int:movie_id>")
def add_to_watchlist(movie_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    # Check if movie is already in watchlist
    existing = conn.execute(
        """
        SELECT * FROM watchlist
        WHERE user_id = ? AND movie_id = ?
        """,
        (session["user_id"], movie_id)
    ).fetchone()

    if existing is None:
        conn.execute(
            """
            INSERT INTO watchlist(user_id, movie_id)
            VALUES(?,?)
            """,
            (session["user_id"], movie_id)
        )

        conn.commit()

    conn.close()

    return redirect(url_for("watchlist"))

# ==========================================
# Remove from Watchlist
# ==========================================

@app.route("/watchlist/remove/<int:movie_id>")
def remove_from_watchlist(movie_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM watchlist
        WHERE user_id = ? AND movie_id = ?
        """,
        (session["user_id"], movie_id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("watchlist"))

# ==========================================
# Search Movies
# ==========================================

@app.route("/search")
def search():

    query = request.args.get("q", "").strip()

    conn = get_connection()

    movies = conn.execute(
        """
        SELECT *
        FROM movies
        WHERE title LIKE ?
        """,
        ("%" + query + "%",)
    ).fetchall()

    conn.close()

    return render_template(
        "search.html",
        movies=movies,
        query=query
    )

# ==========================================
# Admin Dashboard
# ==========================================

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if not session.get("is_admin"):
        return "Access Denied", 403

    conn = get_connection()

    movies = conn.execute(
        "SELECT * FROM movies ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        movies=movies
    )

# ==========================================
# Add Movie
# ==========================================

@app.route("/admin/add", methods=["GET", "POST"])
def add_movie():

    if request.method == "POST":

        title = request.form["title"]
        genre = request.form["genre"]
        year = request.form["year"]
        rating = request.form["rating"]
        runtime = request.form["runtime"]
        language = request.form["language"]
        poster = None
        poster_file=request.files.get("poster")
        if poster_file:
            poster=save_image(poster_file)
        backdrop = request.form["backdrop"]
        description = request.form["description"]
        trailer = request.form["trailer"]
        director = request.form["director"]

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO movies
            (
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
            """,
            (
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
        )

        conn.commit()
        conn.close()

        return redirect(url_for("admin"))
    return render_template("add_movie.html")
# ==========================================
# Edit Movie
# ==========================================

@app.route("/admin/edit/<int:movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):

    conn = get_connection()

    movie = conn.execute(
        "SELECT * FROM movies WHERE id=?",
        (movie_id,)
    ).fetchone()

    if movie is None:
        conn.close()
        return "Movie Not Found", 404

    if request.method == "POST":

        # Handle Poster Upload
        poster = movie["poster"]

        poster_file = request.files.get("poster")

        if poster_file and poster_file.filename != "":
            poster = save_image(poster_file)

        conn.execute(
            """
            UPDATE movies
            SET
                title=?,
                genre=?,
                year=?,
                rating=?,
                runtime=?,
                language=?,
                poster=?,
                backdrop=?,
                description=?,
                trailer=?,
                director=?
            WHERE id=?
            """,
            (
                request.form["title"],
                request.form["genre"],
                request.form["year"],
                request.form["rating"],
                request.form["runtime"],
                request.form["language"],
                poster,
                request.form["backdrop"],
                request.form["description"],
                request.form["trailer"],
                request.form["director"],
                movie_id
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("admin"))

    conn.close()

    return render_template(
        "edit_movie.html",
        movie=movie
    )

# ==========================================
# Delete Movie
# ==========================================

@app.route("/admin/delete/<int:movie_id>")
def delete_movie(movie_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM movies WHERE id=?",
        (movie_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)