def not_found(request):
    response = """HTTP/1.1 404 NOT FOUND\r

                Not a valid URL!"""
    return response.encode()


def show_books(request):
    response = f"""HTTP/1.1 200 OK\r

                show books!\n

                {request.query_params}"""
    return response.encode()


def book_details(request):
    response = f"""HTTP/1.1 200 OK\r

                books details: {request.path_params[0]}!"""

    return response.encode()


def borrow_book(request):
    response = f"""HTTP/1.1 200 OK\r

                borrow books: {request.path_params[0]}!\n"""
    return response.encode()


def language_books(request):
    response = f"""HTTP/1.1 200 OK\r

                language books: {request.path_params[0]}!\n"""
    return response.encode()


def genre_books(request):
    response = f"""HTTP/1.1 200 OK\r

    genre books: {request.path_params[0]}

    year books: {request.path_params[1]}!\n"""

    return response.encode()


def show_journals(request):
    response = """HTTP/1.1 200 OK\r

    show journals!"""
    return response.encode()


def journal_details(request):
    print(request.path_params)
    response = f"""HTTP/1.1 200 OK\r

    journal details: {request.path_params[0]}\n"""

    return response.encode()


def controller(socket, routing_output):
    request = routing_output[0]
    print(f"outputs: {routing_output[0]}, {routing_output[1]}")
    response = routing_output[1][0](request)
    socket.send(response)
