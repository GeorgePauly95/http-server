import socket
from .utils import splitter
from .request import Request
from .JSON_Parser import parse_json


class Connection:
    def __init__(self, conn_socket):
        self.socket = conn_socket

    def parse_request(self):
        complete_message = b""
        print(f"socket id: {id(self.socket)}")
        while b"\r\n\r\n" not in complete_message:
            message = self.socket.recv(10)
            complete_message += message
        request_line_headers, initial_body = splitter(complete_message, b"\r\n\r\n")
        parsed_request = self.parse_request_line_headers(
            message=request_line_headers.decode("utf-8")
        )

        #Non Chunked Request
        if "Content-Length" in parsed_request["headers"].keys():
            if parsed_request["headers"]["Content-Length"] == '0':
                return Request(parsed_request)
            msg_len = int(parsed_request["headers"]["Content-Length"]) - len(
                initial_body
            )
            request_body = b""
            while len(request_body) < msg_len:
                request_body += self.socket.recv(1)
            complete_body = (initial_body + request_body).decode("utf-8").rstrip()
            if parsed_request["headers"]["Content-Type"] == "application/json":
                parsed_request["body"] = parse_json(complete_body)
                request = Request(parsed_request)
                request.body = parsed_request["body"]
                return request

        #Chunked request
        if "Transfer-Encoding" in parsed_request["headers"].keys():
            chunk_data = initial_body
            while b"0\r\n" not in chunk_data:
                chunk_data += self.socket.recv(1)
            chunks = splitter(chunk_data, b"\r\n")
            print(f"Chunks are: {chunks}")
            complete_body = b"".join([chunks[i] for i in range(len(chunks)) if i%2==1])
            parsed_request["body"] = complete_body.decode("utf-8")
            request = Request(parsed_request)
            request.body = parsed_request["body"]
            return request
        return Request(parsed_request)

    def parse_request_line_headers(self, message):
        message_array = splitter(message, "\r\n")
        [request_lines, *headers] = message_array
        request_line_array = request_lines.split(" ")
        request_dict = {
            "method": request_line_array[0],
            "uri": request_line_array[1],
            "protocol": request_line_array[2],
        }
        rest_dict = {
            splitter(header, ": ")[0]: splitter(header, ": ")[1]
            for header in headers
            if header != ""
        }
        return request_dict | {"headers": rest_dict}

    def respond(self, response, request):
        if request.close_connection == True:
            self.socket.send(response)
            self.socket.shutdown(socket.SHUT_WR)
            self.socket.close()
            return
        self.socket.send(response)


