import re
import socket
import os
from _thread import *
import json
import datetime
import time
import traceback

from flask import Flask, redirect, url_for, request,Response,Request,send_file,render_template,jsonify
app = Flask(__name__)


ServerSocket = socket.socket()
HOST = '0.0.0.0'
PORT = 20000
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
        Client.settimeout(120.0) #? WORKING
        start_new_thread(threaded_client, (Client, str(address[0]), str(address[1]),))
        global ThreadCount
        ThreadCount += 1
        print('Thread Count: ' + str(ThreadCount))
    ServerSocket.close()


def main():
    print("python main function")
    t = start_new_thread(accept_connections, ())
    print("accept_connections() Thread created")
    
    app.run(port=10000, host="0.0.0.0")

    
@app.route('/')
def index():
    return redirect("/getdata/10000")
    
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response

@app.route('/getdata/<clientid>', methods= ['GET'])
def get_data(clientid):
    try:
        global Connected_Clients
        Current_Client = Connected_Clients[int(clientid)]
        sock = Current_Client["IP"] + Current_Client["Port"]
    
        Current_Client["connection_object"].send(str.encode("Requesting Screenshot"))
        
        """ data = Current_Client["connection_object"].recv(200000000)
    
        #print("client says -> " + data.decode('utf-8'))
    
        #return "In @app.route POST ('/getdata/<clientid>' -> ) " + clientid + " " + sock
        base64data = json.loads(data.decode('utf-8'))
        return "<div> <img src=\"data:image/png;base64, "+ base64data["Data"] +" \"  /> </div>" """
        
        filetodown = open(str(clientid) + ".png", "wb")
        
        data = Current_Client["connection_object"].recv(2000000)
            
        filetodown.write(data)
        filetodown.close()
        Current_Client["connection_object"].send(b"Thank you for connecting.")
        src = str(clientid) +".png"
        return render_template("getdata.html", src= src)
        return "<div> <img src=\"/"+ str(clientid) +".png  \"  /> </div>"

    except Exception as ex:
        print("Error -> ", str(ex))
        global ThreadCount
        ThreadCount = ThreadCount - 1
        print('Thread Count: ' + str(ThreadCount))
        #Connected_Clients.pop(ClientID)
        #print("Removed Client ", ClientID , " from Connected_Clients global Dictionary")
        e = traceback.format_exc()
        print(str(e))
        return "<pre> Exception No user in Connected_Clients global Dictionary " + str(ex)  +  str(e)  +"   </pre>"

@app.route('/<int:filename>.png')
def getpng(filename):
    try:
        return send_file(str(filename) + ".png", mimetype='image/png')
    except Exception as ex:
        e = traceback.format_exc()
        return "<pre> Error -> " + str(e) + "</pre>"

@app.route('/clickonscreen',methods = ['POST'])
def clickonscreen():
    #request.method == 'POST':
    try:
        clientid = request.json['clientID']
        XPOS = request.json['X']
        YPOS = request.json['Y']
        ClickRequested = request.json['ClickRequested']
        print(json.dumps(request.json))
        
    except Exception as ex:
        e = traceback.format_exc()
        print(str(e))
        res = {"error" : "Error not enough arguments " +  str(e)}
        return res
    
    try:
        global Connected_Clients
        Current_Client = Connected_Clients[int(clientid)]
        sock = Current_Client["IP"] + Current_Client["Port"]
    
        Current_Client["connection_object"].sendall(str.encode("Click mouse"))
        Current_Client["connection_object"].sendall(str.encode(json.dumps(request.json)))
        data = Current_Client["connection_object"].recv(1024)
        #return json.dumps(request.json)
        #* reply = { "msg" : data.decode('utf-8')}
        reply = { "msg" : repr(data)}
        #! connection.send(str.encode("Received Thanks user " + str(ClientID)))
        return jsonify(reply)
    
    except Exception as ex:
        e = traceback.format_exc()
        print(str(e))
        res = {"error" : "Error client disconnected " +  str(e)}
        return res


if __name__ == '__main__':
    
    main()
