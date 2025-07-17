def static_controller(request):
    response = f"""HTTP/1.1 200 OK\r
                
                load testing the HTTP server\n

                using apachebench\n"""
    return response.encode()


def not_found(request):
    response = f"""HTTP/1.1 404 NOT FOUND\r

                Not a valid URL!"""
    return response.encode()


def show_books(request):
    response = f"""HTTP/1.1 200 OK\r

                show books!\n

                {request.query_params}"""
    return response.encode()


def book_details(request):
    isbn = request.path_params

    response = f"""HTTP/1.1 200 OK\r

                books details: {isbn}!"""

    return response.encode()


def borrow_book(request):
    response = f"""HTTP/1.1 200 OK\r

                borrow books: {request.path_params}!\n"""
    return response.encode()


def language_books(request):
    response = f"""HTTP/1.1 200 OK\r

                language books: {request.path_params}!\n"""
    return response.encode()


def genre_books(request):

    response = f"""HTTP/1.1 200 OK\r

    genre books: {request.path_params[0]}

    year books: {request.path_params[1]}!\n"""

    return response.encode()


def show_journals(request):
    response = f"""HTTP/1.1 200 OK\r

    show journals!"""
    return response.encode()


def journal_details(request):
    response = f"""HTTP/1.1 200 OK\r

    journal details: {request.path_params[":journalid"]}\n"""

    return response.encode()


def controller(socket, request):
    response = request.controller(request)

    socket.send(response)
