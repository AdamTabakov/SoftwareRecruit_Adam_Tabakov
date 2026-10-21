import socket

# constants
HOST = '127.0.0.1'
PORT = 5555
HEADER_SIZE = 16
CHUNK_SIZE = 4096

# read the file
with open("Utah.bmp", "rb") as f:
    data = f.read()
file_size = len(data)

# in case file is too large
if file_size >= 10 ** HEADER_SIZE:
    raise ValueError("too large file")

# create header
header = str(file_size).zfill(HEADER_SIZE).encode('ascii')

# send header and data to the base station
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rov:
    rov.connect((HOST, PORT))
    rov.sendall(header)

    for start in range(0, file_size, CHUNK_SIZE):
        chunk = data[start: start + CHUNK_SIZE]
        rov.sendall(chunk)
print("success!")
