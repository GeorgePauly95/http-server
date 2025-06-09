import socket

hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hs.bind((socket.gethostname(), 2002))
hs.listen(5)
i = 1
while True:
    clientsocket, address = hs.accept()
    message = clientsocket.recv(10000).decode("utf-8")
    message_array = message.split("\n")
    request_line = message_array[0]
    request_line_array = request_line.split(" ")
    method = request_line_array[0]
    URI = request_line_array[1]
    protocol = request_line_array[2]
    print(f"The method is: {method}")
    print(f"The URI is: {URI}")
    print(f"The protocol is: {protocol}")
    print(f"\n{message}")

    send_message = "Thank you for the request!"
    clientsocket.send(bytes(send_message, "utf-8"))
