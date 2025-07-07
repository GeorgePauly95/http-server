import socket
import threading
import routing
from JSON_Parser import parse_json
from controllers import not_found

hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.AF_INET)
print(socket.SOCK_STREAM)
hs.bind(("localhost", 2002))
hs.listen(5)

# rename and modularize


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
    complete_message = b""
    while b"\r\n\r\n" not in complete_message:
        message = conn_socket.recv(10)
        complete_message += message
    request_line_headers = complete_message.split(b"\r\n\r\n")[0]
    initial_body = complete_message.split(b"\r\n\r\n")[1]
    parsed_request = http_parser(message=request_line_headers.decode("utf-8"))

    if "Content-Length" in parsed_request.keys():
        msg_len = int(parsed_request["Content-Length"]) - len(initial_body)
        request_body = b""
        while len(request_body) < msg_len:
            request_body += conn_socket.recv(1)
        complete_body = (initial_body + request_body).decode("utf-8").rstrip()
        if parsed_request["Content-Type"] == "application/json":
            parsed_request["Body"] = parse_json(complete_body)
    ctrl_fn = routing.route_matcher(parsed_request["URI"])
    print(type(ctrl_fn))
    # dunder not required
    if type(ctrl_fn).__name__ == "NoneType":
        not_found(conn_socket)
        conn_socket.shutdown(socket.SHUT_WR)
        conn_socket.close()
    elif type(ctrl_fn).__name__ == "tuple":
        if type(ctrl_fn[1][0]).__name__ == "tuple":
            ctrl_fn[0](conn_socket, *ctrl_fn[1][0])
            conn_socket.shutdown(socket.SHUT_WR)
            conn_socket.close()
        else:
            ctrl_fn[0](conn_socket, ctrl_fn[1][0])
            conn_socket.shutdown(socket.SHUT_WR)
            conn_socket.close()
    elif type(ctrl_fn).__name__ == "function":
        ctrl_fn(conn_socket)
        conn_socket.shutdown(socket.SHUT_WR)
        conn_socket.close()


while True:
    conn_socket, address = hs.accept()
    t = threading.Thread(target=server_response, args=(conn_socket,))
    t.start()
hs.close()
