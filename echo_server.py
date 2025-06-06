import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 1237))
s.listen(1)
while True:
    clientsocket, address = s.accept()
    message = clientsocket.recv(1024)
    mirror_message = f"\n\nThis is your mirror message:\n\n {message.decode('utf-8')}\n\n This is the address {address}"
    clientsocket.send(bytes(mirror_message, "utf-8"))
    s.close()
