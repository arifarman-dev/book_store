from app import app
from database_connection import DatabaseConnection
from playwright.sync_api import Page

def test_create_new_book(page: Page):

    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button").click()

    page.goto("http://localhost:5001/books")
    page.get_by_placeholder("Title").fill("The Chroicles of Geronimo (the cat)")
    page.get_by_placeholder("Author").fill("Geronimo")
    page.get_by_role("button", name="Submit").click()
    books = page.locator('li')
    new_book = books.all_inner_texts()[-1]
    assert new_book == "The Chroicles of Geronimo (the cat) by Geronimo"


def test_auth_integration():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    response = client.post('/sessions', data={
        'username': 'test',
        'password': '1234'
    })

    assert response.status_code == 302
    # this assertion might be new to you :)
    assert response.headers['Location'].endswith('/books')

def test_auth_playwright(page: Page):

    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button").click()

    assert page.url == "http://localhost:5001/books"