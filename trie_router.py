"""Trie routing"""

from trie_class import Trie
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

routes_mapper = {
    "/books/genre/:genreid/year/:yearid": genre_books,
    "/books/language/:languageid": language_books,
    "/books/:isbn": book_details,
    "/books": show_books,
    "/borrow/:borrowid": borrow_book,
    "/journals/:journalid": journal_details,
    "/journals": show_journals,
}
for i in range(1, 1001):
    routes_mapper[f"/path_{i}"] = show_books
routes = Trie()


def splitter(word, delimiter):
    return word.split(delimiter)


for route in routes_mapper:
    uri_keys = splitter(route, "/")
    routes.add(uri_keys, routes_mapper[route])


def route_matcher(request):
    uri = query_params_checker(request)
    uri_keys = splitter(uri, "/")
    router_output = routes.search(uri_keys)
    if router_output == "Not a Route!":
        request.controller = not_found
        return request
    request.controller = router_output[0]
    request.path_params = router_output[1]
    return request


def query_params_checker(request):
    uri = request.uri
    uri_pair = uri.split("?")
    if len(uri_pair) == 1:
        request.query_params = {}
        return uri
    query_params = uri_pair[1].split("&")
    for query_param in query_params:
        key, value = query_param.split("=")
        request.query_params[key] = value
    return uri_pair[0]
