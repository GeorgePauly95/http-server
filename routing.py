"""Routing function"""

import re
from controllers import (
    book_details,
    show_books,
    borrow_book,
    language_books,
    genre_books,
    not_found,
    show_journals,
    journal_details,
)
routes = {
    "/books/genre/:genre/year/:year": genre_books,
    "/books/language/:language": language_books,
    "/books/:isbn": book_details,
    "/books": show_books,
    "/borrow/:borrowid": borrow_book,
    "/journals/:journalid": journal_details,
    "/journals": show_journals,
}
route_regexes = {}

# implement tree DS for routing!
def regex_generator(URI):
    path_regex = "^" + re.sub(r":\w+", r"(\\w+)", URI) + "$"
    return path_regex


route_regexes = {regex_generator(route): route for route in routes}
