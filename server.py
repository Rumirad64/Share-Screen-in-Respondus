import socket
import os
from _thread import *
import json
import datetime
import time

from flask import Flask, redirect, url_for, request
app = Flask(__name__)


ServerSocket = socket.socket()
HOST = '0.0.0.0'
PORT = 2021
ThreadCount = 0
abort = False

Connected_Clients = {}

try:
    ServerSocket.bind((HOST, PORT))
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
        connection.send(str.encode("Received Thanks user " + str(ClientID)))
        
    except Exception as exx:
        print("Error -> ", str(exx))
        ThreadCount = ThreadCount - 1
        print('Thread Count: ' + str(ThreadCount))
        return

    try:
        while True:
            #connection.sendall(str.encode("Requesting Screenshot"))
            #data = connection.recv(2048)
            #print("client says -> " + data.decode('utf-8'))
            time.sleep(1)
            """ data = connection.recv(2048)
            reply = 'Server Says: ' + data.decode('utf-8')
            print("client says -> " + data.decode('utf-8'))
            PrintDateTime()
            if not data:
                pass
            if(data.decode('utf-8') == "close"):
                connection.close()
            connection.sendall(str.encode(reply)) """
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
    
    app.run(port=2022)

    
@app.route('/')
def index():
    return "hi"

@app.route('/getdata/<clientid>', methods= ['GET'])
def hello_name(clientid):
    global Connected_Clients
    Current_Client = Connected_Clients[int(clientid)]
    sock = Current_Client["IP"] + Current_Client["Port"]
    
    Current_Client["connection_object"].send(str.encode("Requesting Screenshot"))
    data = Current_Client["connection_object"].recv(20000000)
    
    #print("client says -> " + data.decode('utf-8'))
    
    #return "In @app.route POST ('/getdata/<clientid>' -> ) " + clientid + " " + sock
    base64data = json.loads(data.decode('utf-8'))
    return "<div> <img src=\"data:image/png;base64, "+ base64data["Data"] +" \"  /> </div>"


if __name__ == '__main__':
    
    main()
