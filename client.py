import socket

# kill PID 1234 and 1235
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), 1236))
message = input("Please type your message here, and we'll mirror it back to you:\n\n")

s.send(bytes(message, "utf-8"))
mirror_message = s.recv(1024)
print(mirror_message.decode("utf-8"))
