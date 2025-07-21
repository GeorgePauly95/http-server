import socket
import threading

from trie_router import route_matcher

# from regex_router import route_matcher
from JSON_Parser import parse_json
from controllers import controller
from request import Request

hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
hs.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)
hs.bind(("localhost", 2002))
hs.listen(5)


def request_line_headers_parser(message):
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
    return request_dict | {"headers": rest_dict}


def http_request_parser(conn_socket):
    complete_message = b""
    while b"\r\n\r\n" not in complete_message:
        message = conn_socket.recv(10)
        complete_message += message
    request_line_headers, initial_body = complete_message.split(b"\r\n\r\n")
    parsed_request = request_line_headers_parser(
        message=request_line_headers.decode("utf-8")
    )
    if "Content-Length" in parsed_request["headers"].keys():
        msg_len = int(parsed_request["headers"]["Content-Length"]) - len(initial_body)
        request_body = b""
        while len(request_body) < msg_len:
            request_body += conn_socket.recv(1)
        complete_body = (initial_body + request_body).decode("utf-8").rstrip()
        if parsed_request["headers"]["Content-Type"] == "application/json":
            parsed_request["Body"] = parse_json(complete_body)
            request = Request(parsed_request)
            request.body = parsed_request["Body"]
            server_response(request)
            return
    request = Request(parsed_request)
    print(request.headers)
    server_response(request)


def server_response(request):
    routing_output = route_matcher(request)
    controller(conn_socket, routing_output)
    conn_socket.shutdown(socket.SHUT_WR)
    conn_socket.close()


while True:
    conn_socket, address = hs.accept()
    threads = []
    t = threading.Thread(target=http_request_parser, args=(conn_socket,))
    threads.append(t)
    t.start()
    t.join()
hs.close()
