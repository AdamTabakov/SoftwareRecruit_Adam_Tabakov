import socket

# Constants
HOST = '127.0.0.1'
PORT = 5555
BUFFER_SIZE = 4096
HEADER_SIZE = 16

# Recieving function
def recieve(connection: socket.socket, size: int):
    # create an empty byte array
    data = b""

    # loop until we have received the full amount of data
    while len(data) < size:
        chunk = connection.recv(size - len(data))
        if not chunk:
            raise ConnectionError("connection broke")
        data += chunk

    return data

# TCP IPv4 Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    # allow the socket to be reused immediately after it is closed
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind to the host and port
    serv.bind((HOST, PORT))
    # listen to connections, allow 1 at a time
    serv.listen(1)

    # accept a connection
    connection, address = serv.accept()

    # handle the connection when it occurs
    with connection:
        # recieve the header and establish constants
        header = recieve(connection, HEADER_SIZE)
        file_size = int(header)
        recieved = 0

        # open the file and read the data
        with open('output.bmp', 'wb') as f:
            while recieved < file_size:
                chunk = connection.recv(min(BUFFER_SIZE, file_size - recieved))
                if not chunk:
                    raise ConnectionError("connection broke")
                # write the chunk to the file and update recieved count
                f.write(chunk)
                recieved += len(chunk)
