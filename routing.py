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


def route_matcher(URL):
    for route_regex in route_regexes:
        if re.match(route_regex, URL) is not None:
            print(f"We can serve this route: with this {route_regex}")
            path_params = re.findall(route_regex, URL)
            print(path_params[0])
            print(re.match(route_regex, URL).group())
            if path_params[0] != re.match(route_regex, URL).group():
                print(f"This is the match: {re.match(route_regex, URL)}")
                print(f"These are the path params: {path_params}")
                return routes[route_regexes[route_regex]], path_params
            return routes[route_regexes[route_regex]], ()
