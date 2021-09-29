import socket
import os
from _thread import *
import json
import datetime

ServerSocket = socket.socket()
host = '0.0.0.0'
port = 2021
ThreadCount = 0                          

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(10)

def PrintDateTime():
    x = datetime.datetime.now()
    x = x.strftime("%c")
    print(x , "\n")

def threaded_client(connection):
    try:
        connection.send(str.encode('Welcome to the Servern'))
        while True:
            data = connection.recv(2048)
            reply = 'Server Says: ' + data.decode('utf-8')
            print("client says -> " + data.decode('utf-8'))
            PrintDateTime()
            if not data:
                pass
                break
            if(data.decode('utf-8') == "close"):
                connection.close()
            connection.sendall(str.encode(reply))
        connection.close()
    except Exception as ex:
        print("Error -> " , str(ex))
        global ThreadCount
        ThreadCount = ThreadCount - 1
        print('Thread Count: ' + str(ThreadCount))
        return

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Count: ' + str(ThreadCount))
ServerSocket.close()
