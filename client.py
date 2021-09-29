import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 2021
hostname = socket.gethostname() 

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(hostname + " -> " + Input ))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()