import socket
from JSON_Parser import parse_json
import json
import threading
import time

hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hs.bind(("localhost", 2002))
hs.listen(5)


def HTTP_parser(message):
    message_array = message.split("\r\n")
    request_line_array = message_array[0].split(" ")
    rest_line_array = message_array[1:]
    [request_lines, *headers] = message_array
    request_dict = {
        "Method": request_line_array[0],
        "URI": request_line_array[1],
        "Protocol": request_line_array[2],
    }
    rest_dict = {
        header.split(": ")[0]: header.split(": ")[1]
        for header in rest_line_array
        if header != ""
    }
    return request_dict | rest_dict


response_message = b"""HTTP/1.1 200 OK\r
Content-Length: 18\r

Request Received!\n
"""


def server_response(clientsocket):
    complete_message = ""
    while "\r\n\r\n" not in complete_message:
        message = clientsocket.recv(1).decode("utf-8")
        complete_message += message
    correct_complete_message = complete_message.split("\r\n\r\n")[0]
    initial_body = complete_message.split("\r\n\r\n")[1]
    parsed_request = HTTP_parser(correct_complete_message)
    if parsed_request['URI'] == '/books':
        clientsocket.send(b"""HTTP/1.1 200 OK\r

                          <html>
                            <h1> BOOKS! </h1>
                          </html>\n
                          """)
        clientsocket.shutdown(socket.SHUT_WR)
        clientsocket.close()
    if "Content-Length" in parsed_request.keys():
        msg_len = int(parsed_request["Content-Length"])
        request_body = clientsocket.recv(msg_len).decode("utf-8")
        complete_body = (initial_body + request_body).rstrip()
        if parsed_request["Content-Type"] == "application/json":
            parsed_request["Body"] = parse_json(complete_body)
    print(f"This is the complete request: {parsed_request}")
    clientsocket.send(response_message)
    clientsocket.shutdown(socket.SHUT_WR)
    clientsocket.close()


while True:
    clientsocket, address = hs.accept()
    t = threading.Thread(target=server_response, args=(clientsocket,))
    t.start()
hs.close()
