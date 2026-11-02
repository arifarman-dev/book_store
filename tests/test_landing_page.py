# from playwright.sync_api import Page, expect

# def test_has_title(page: Page):
#     page.goto("http://127.0.0.1:5001/")
#     h1 = page.locator("h1")
#     expect(h1).to_have_text("Welcome to the library of Alexandria")

# def test_book_list_contains_all_books(page: Page):
#     page.goto("http://127.0.0.1:5001/books")

#     books = page.locator("li")

#     expected_books = [
#       'The Gruffalo by Julia Donaldson',
#       'Ada Twist, Scientist by Andrea Beaty',
#       'The Girl Who Drank the Moon by Kelly Barnhill',
#       'Dragons in a Bag by Zetta Elliott'
#     ]

#     actual_books = books.all_inner_texts()

#     assert actual_books == expected_books