import sys
import os

# this line is a bit of a hack which allows us to import app without changing anything else
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

def test_get_books_returns_a_200():
    client = app.test_client()

    response = client.get("/books")

    assert response.status_code == 200

def test_get_books_returns_all_the_books():
    client = app.test_client()

    response = client.get("/books")

    # Read the returned response as plain HTML text
    html_content = response.get_data(as_text=True)

    # Assert that each book title is present in the HTML structure
    assert "The Gruffalo" in html_content
    assert "Ada Twist, Scientist" in html_content
    assert "The Girl Who Drank the Moon" in html_content
    assert "Dragons in a Bag" in html_content


def test_get_authors_returns_all_authors():

    client = app.test_client()

    response = client.get("/authors")

    assert response.json == [
        {"title": "The Gruffalo"},
        {"title": "Ada Twist, Scientist"},
        {"title": "The Girl Who Drank the Moon"},
        {"title": "Dragons in a Bag"}
    ]

def test_get_all_films():
    client = app.test_client()
    response = client.get('/films')
    assert response.json == [
        {
            "title" : "King Kong",
            "release_year" : 1933
        },
        {
            "title" : "The Godfather",
            "release_year" : 1972
        },
        {
            "title" : "Star Wars",
            "release_year" : 1977
        }
    ]