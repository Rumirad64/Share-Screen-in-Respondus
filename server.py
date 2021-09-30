import socket
import os
from _thread import *
import json
import datetime
import time

ServerSocket = socket.socket()
host = '0.0.0.0'
port = 2021
ThreadCount = 0
abort = False

Connected_Clients = {}

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(10)


def PrintDateTime():
    x = datetime.datetime.now()
    x = x.strftime("%c")
    print(x, "\n")


def threaded_client(connection , IPaddr,  port):
    ClientID = ""
    global ThreadCount
    global Connected_Clients
    
    try:
        id_data = connection.recv(2048)
        ClientID = id_data.decode('utf-8')
        ClientID = int(ClientID)
        if(ClientID < 10000 or ClientID > 90000):
            raise ValueError('Client ID corrupted')
        print("Client ID -> " , ClientID , " is connected from ", IPaddr)
        
        Connected_Clients[ClientID] = {"connection_object" : connection , "IP" : IPaddr , "Port" : port}
        print("Inserted Client ", ClientID , " to Connected_Clients global Dictionary")
        
    except Exception as exx:
        print("Error -> ", str(exx))
        ThreadCount = ThreadCount - 1
        print('Thread Count: ' + str(ThreadCount))
        return

    try:
        while True:
            data = connection.recv(2048)
            reply = 'Server Says: ' + data.decode('utf-8')
            print("client says -> " + data.decode('utf-8'))
            PrintDateTime()
            if not data:
                pass
            if(data.decode('utf-8') == "close"):
                connection.close()
            connection.sendall(str.encode(reply))
        connection.close()
    except Exception as ex: #?Desktop client closed
        print("Error -> ", str(ex))
        ThreadCount = ThreadCount - 1
        print('Thread Count: ' + str(ThreadCount))
        Connected_Clients.pop(ClientID)
        print("Removed Client ", ClientID , " from Connected_Clients global Dictionary")
        return


def accept_connections():
    print("IN accept_connections()")
    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client, str(address[0]), str(address[1]),))
        global ThreadCount
        ThreadCount += 1
        print('Thread Count: ' + str(ThreadCount))
    ServerSocket.close()


def main():
    print("python main function")
    t = start_new_thread(accept_connections, ())
    print("accept_connections() Thread created")
    while(abort == False):
        time.sleep(1)
        pass


if __name__ == '__main__':
    main()
