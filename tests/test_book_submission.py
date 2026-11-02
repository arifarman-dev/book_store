from database_connection import DatabaseConnection

from playwright.sync_api import Page, expect

def test_creaeting_a_new_book(page: Page):
    # Reset the database
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/books.sql")
    # Go to the form
    page.goto("http://localhost:5001/books")

    # Grab the first field "Title"
    page.get_by_label("Title").fill("The Chroicles of Geronimo (the cat)")
    # Grab the second field "Author"
    page.get_by_label("Author").fill("Geronimo")

    # To press submit
    page.get_by_role("button", name="Submit").click()

    # Exercise
    expected_books = [
        'The Gruffalo by Julia Donaldson',
        'Ada Twist, Scientist by Andrea Beaty',
        'The Girl Who Drank the Moon by Kelly Barnhill',
        'Dragons in a Bag by Zetta Elliott',
        # '1984 by George Orwell',
        # 'Pride and Prejudice by Jane Austen',
        # 'Crime and Punishment by Fyodor Dostoevsky',
        # 'The Great Gatsby by F. Scott Fitzgerald',
        # 'The Book Thief by Markus Zusak',
        # 'Sapiens: A Brief History of Humankind by Yuval Noah Harari',
        'The Chroicles of Geronimo (the cat) by Geronimo'
    ]

    # Go to the list of all books
    books = page.locator('li')

    actual_books = books.all_inner_texts()
    assert actual_books == expected_books