def not_found(socket):
    response = b"""HTTP/1.1 404 NOT FOUND\r

                Not a valid URL!"""
    socket.send(response)


def book_details(socket, isbn):
    response = f"""HTTP/1.1 200 OK\r

                books details: {isbn}!\n"""
    socket.send(response.encode())


def show_books(socket):
    socket.send(
        b"""HTTP/1.1 200 OK\r

                show books!\n"""
    )


def borrow_book(socket, borrowid):
    response = f"""HTTP/1.1 200 OK\r

                borrow books: {borrowid}!\n"""
    socket.send(response.encode())


def language_books(socket, language):
    response = f"""HTTP/1.1 200 OK\r

                language books: {language}!\n"""
    socket.send(response.encode())


def genre_books(socket, genre, year):

    response = f"""HTTP/1.1 200 OK\r

    genre books: {genre}

    year books: {year}!\n"""

    socket.send(response.encode())


def show_journals(socket):
    socket.send(
        b"""HTTP/1.1 200 OK\r

    show journals!"""
    )


def journal_details(socket, journalid):
    response = f"""HTTP/1.1 200 OK\r

    journal details: {journalid}\n"""

    socket.send(response.encode())
