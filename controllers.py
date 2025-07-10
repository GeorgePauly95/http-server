def not_found():
    response = b"""HTTP/1.1 404 NOT FOUND\r

                Not a valid URL!"""
    return response


def book_details(isbn):
    response = f"""HTTP/1.1 200 OK\r

                books details: {isbn}!\n"""
    return response.encode()


def show_books():
    return b"""HTTP/1.1 200 OK\r

                show books!\n"""


def borrow_book(borrowid):
    response = f"""HTTP/1.1 200 OK\r

                borrow books: {borrowid}!\n"""
    return response.encode()


def language_books(language):
    response = f"""HTTP/1.1 200 OK\r

                language books: {language}!\n"""
    return response.encode()


def genre_books(genre, year):

    response = f"""HTTP/1.1 200 OK\r

    genre books: {genre}

    year books: {year}!\n"""

    return response.encode()


def show_journals():
    return b"""HTTP/1.1 200 OK\r

    show journals!"""


def journal_details(journalid):
    response = f"""HTTP/1.1 200 OK\r

    journal details: {journalid}\n"""

    return response.encode()


def controller(socket, request):
    print(request.path_params)
    response = request.controller(*request.path_params)
    socket.send(response)
