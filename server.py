import socket
import threading
from JSON_Parser import parse_json

hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hs.bind(("localhost", 2002))
hs.listen(5)


def http_parser(message):
    message_array = message.split("\r\n")
    [request_lines, *headers] = message_array
    request_line_array = request_lines.split(" ")
    request_dict = {
        "Method": request_line_array[0],
        "URI": request_line_array[1],
        "Protocol": request_line_array[2],
    }
    rest_dict = {
        header.split(": ")[0]: header.split(": ")[1]
        for header in headers
        if header != ""
    }
    return request_dict | rest_dict


def server_response(conn_socket):
    complete_message = ""
    while "\r\n\r\n" not in complete_message:
        message = conn_socket.recv(1).decode("utf-8")
        complete_message += message
    correct_complete_message = complete_message.split("\r\n\r\n")[0]
    initial_body = complete_message.split("\r\n\r\n")[1]
    parsed_request = http_parser(correct_complete_message)

    if parsed_request["URI"] not in URLS:
        conn_socket.send(
            b"""HTTP/1.1 404 NOT FOUND\r
                        Content-Length: 34\r

                        Resource requested does not exist!\n
                         """
        )
        print(f"Resource: {parsed_request["URI"]} does not exist")
        conn_socket.shutdown(socket.SHUT_WR)
        conn_socket.close()
        return
    if "Content-Length" in parsed_request.keys():
        msg_len = int(parsed_request["Content-Length"])
        request_body = conn_socket.recv(msg_len).decode("utf-8")
        complete_body = (initial_body + request_body).rstrip()
        if parsed_request["Content-Type"] == "application/json":
            parsed_request["Body"] = parse_json(complete_body)
    print(f"This is the complete request: {parsed_request}")
    URLS[parsed_request["URI"]](conn_socket)
    conn_socket.shutdown(socket.SHUT_WR)
    conn_socket.close()


def root_function(s):
    s.send(
        b"""HTTP/1.1 200 OK\r

                     root!\n
                     """
    )


def books_function(s):
    s.send(
        b"""HTTP/1.1 200 OK\r

        Content-Length: 6\r

                    BOOKS!\n
                    """
    )


URLS = {"/": root_function, "/books": books_function}


while True:
    conn_socket, address = hs.accept()
    t = threading.Thread(target=server_response, args=(conn_socket,))
    t.start()

hs.close()
