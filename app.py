from flask import Flask, jsonify, render_template, request, redirect, session
from database_connection import DatabaseConnection
from book_repository import BookRepository
from book import Book
from film_repository import FilmRepository
from user import User
from user_repository import UserRepository
from authenticate import is_authenticated
from login_required import login_required

# instantiate a Flask app object
app = Flask(__name__)
app.secret_key = "some_really_secret_key"

# Declares a route that listens for a GET requests to the path /hello
# and a method to execute when that request comes in
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello to you too"

# Duplicate route
@app.route('/hello', methods=['GET'])
def hello_again():
    return "Hello, hello and hello again"

# Exercise
@app.route('/books', methods=['GET'])
def get_all_books():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    books = book_repository.all()
    print(books)
    return render_template("books.html", books=books)

@app.route('/books', methods=['POST'])
@login_required
def create_book():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    book_details = request.form
    book = Book(title=book_details["title"], author=book_details["author"])
    book_repository.create(book)
    return redirect("/books")

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = [
        {"title": "The Gruffalo"},
        {"title": "Ada Twist, Scientist"},
        {"title": "The Girl Who Drank the Moon"},
        {"title": "Dragons in a Bag"}
    ]

    return jsonify(authors)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/films", methods=["GET"])
def get_films():
    connection = DatabaseConnection()
    connection.connect()
    film_repository = FilmRepository(connection)
    films = film_repository.all()
    print(films)
    films_json = []
    for film in films:
        item = {"title": film.title, "release_year": film.release_year}
        films_json.append(item)
    return jsonify(films_json)


@app.route('/quotes', methods=['GET'])
def get_quotes():
    quotes = [
        {"quote": "You can never get a cup of tea large enough or a book long enough to suit me.", "author": "C.S. Lewis"}, 
        {"quote": "Never trust anyone who has not brought a book with them.", "author": "Lemony Snicket, Horseradish: Bitter Truths You Can't Avoid"},
        {"quote": "We read to know we're not alone.", "author": "William Nicholson, Shadowlands: A Play"},
        {"quote": """Sometimes, you read a book and it fills you with this weird evangelical zeal, and you become convinced that the shattered world will 
        never be put back together unless and until all living humans read the book.""", "author": "John Green, The Fault in Our Stars"},
        {"quote": "If one cannot enjoy reading a book over and over again, there is no use in reading it at all.", "author": "Oscar Wilde"}
        ]
    return quotes

@app.route('/team', methods=['GET'])
def get_team():
    team = ["Dorothy", "Rose", "Blanche", "Sophia"]
    return render_template("team.html", team=team)

@app.route('/users/new', methods=['GET'])
def get_signup_form():
    return render_template("signup_form.html")

@app.route('/users', methods=['POST'])
def create_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)
    user_details = request.form
    user = User(username=user_details["username"], password=user_details["password"])
    user_repository.create(user)
    return redirect("/books")

@app.route('/sessions/new', methods=['GET'])
def get_login_form():
    return render_template("login_form.html")

@app.route('/sessions', methods=['POST'])
def create_session():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)

    username = request.form["username"]
    password = request.form["password"]

    user = user_repository.find_by_username(username)

    if user and user.password == password:
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/books")
    else:
        return redirect("/sessions/new")

# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

# Test