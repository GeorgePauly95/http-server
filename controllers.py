def restrict_to_methods(methods=None):
    if methods is None:
        methods = []

    def decorator(routing_output):
        def wrapper(request):
            if request.method in methods:
                return routing_output(request)
            return method_not_valid(request)

        return wrapper

    return decorator


def method_not_valid(request):
    response = """HTTP/1.1 405 Method Not Allowed\r

                Incorrect Method!"""
    return response.encode()


def not_found(request):
    response = """HTTP/1.1 404 NOT FOUND\r

                Not a valid URL!"""
    return response.encode()


@restrict_to_methods(methods=["GET"])
def show_books(request):
    response = f"""HTTP/1.1 200 OK\r

                show books!\n

                {request.query_params}"""
    return response.encode()


@restrict_to_methods(methods=["GET", "POST"])
def book_details(request):
    response = f"""HTTP/1.1 200 OK\r

                books details: {request.path_params[0]}!"""

    return response.encode()


@restrict_to_methods(methods=["GET"])
def borrow_book(request):
    response = f"""HTTP/1.1 200 OK\r

                borrow books: {request.path_params[0]}!\n"""
    return response.encode()


@restrict_to_methods(methods=["GET"])
def language_books(request):
    response = f"""HTTP/1.1 200 OK\r

                language books: {request.path_params[0]}!\n"""
    return response.encode()


@restrict_to_methods(methods=["GET"])
def genre_books(request):
    response = f"""HTTP/1.1 200 OK\r

    genre books: {request.path_params[0]}

    year books: {request.path_params[1]}!\n"""

    return response.encode()


@restrict_to_methods(methods=["GET"])
def show_journals(request):
    response = """HTTP/1.1 200 OK\r

    show journals!"""
    return response.encode()


@restrict_to_methods(methods=["GET"])
def journal_details(request):
    response = f"""HTTP/1.1 200 OK\r

    journal details: {request.path_params[0]}\n"""

    return response.encode()


def home(request):
    response = """HTTP/1.1 200 OK\r
    HEY!
    """
    return response.encode()


def controller(socket, request, routing_output):
    response = routing_output(request)
    socket.send(response)
