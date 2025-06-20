import socket
from JSON_Parser import parse_json

hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hs.bind((socket.gethostname(), 2002))
hs.listen(5)


# def HTTP_parser(message):
#     message_array = message.split("\r\n")
#     request_line_array = message_array[0].split(" ")
#     rest_line_array = message_array[1:-1]
#     request_body = message_array[-1]
#     # print(request_body)
#     request_dict = {
#         "Method": request_line_array[0],
#         "URI": request_line_array[1],
#         "Protocol": request_line_array[2],
#     }
#     rest_dict = {
#         header.split(": ")[0]: header.split(": ")[1]
#         for header in rest_line_array
#         if header != ""
#     }
#     return request_dict | rest_dict | {"Body": parse_json(request_body)}


def HTTP_parser(message):
    message_array = message.split("\r\n\n")
    print(message_array[0])
    print(message_array[1])
    return message_array[1]


while True:
    clientsocket, address = hs.accept()
    message = clientsocket.recv(10000).decode("utf-8")
    print(message)
    HTTP_parser(message)
    send_message = "Thank you for the request!"
    clientsocket.send(bytes(send_message, "utf-8"))
