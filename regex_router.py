"""Regex routing"""

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
    static_controller,
)

routes_mapper = {
    "/books/genre/:genre/year/:year": genre_books,
    "/books/language/:language": language_books,
    "/books/:isbn": book_details,
    "/books": show_books,
    "/borrow/:borrowid": borrow_book,
    "/journals/:journalid": journal_details,
    "/journals": show_journals,
}

route_regexes = {}


def regex_generator(uri):
    path_regex = "^" + re.sub(r":\w+", r"(\\w+)", uri) + "$"
    return path_regex


route_regexes = {regex_generator(route): route for route in routes_mapper}


def route_matcher(request):
    uri = query_params_checker(request)
    for route_regex in route_regexes:
        if re.match(route_regex, uri) is not None:
            request.controller = routes_mapper[route_regexes[route_regex]]
            path_params = re.findall(route_regex, uri)[0]
            if isinstance(path_params, str) is True:
                if "/" in path_params:
                    return request
                request.path_params = (path_params,)
                return request
            if isinstance(path_params, tuple) is True:
                request.path_params = path_params
                return request
            request.path_params = (path_params,)
            return request
    request.controller = not_found
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
