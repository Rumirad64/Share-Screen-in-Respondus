import socket
import random
import json
from time import sleep, time
import pyautogui
import base64


host = '127.0.0.1'
port = 20000
TIMEOUT_SECONDS = 20.0
#hostname = socket.gethostname()

with open('serverip.txt') as f:
    lines = f.readline()
    host = lines



clientID = random.randint(10000, 90000)

with open('clientID.txt') as f:
    lines = f.readline()
    clientID = lines
clientID = str(clientID)

""" with open('clientID.txt', 'w') as f:
    f.write(str(clientID)) """
while True:
    try:
        ClientSocket = socket.socket()
        ClientSocket.settimeout(TIMEOUT_SECONDS)
        print('Connecting socket to ' + host)
        ClientSocket.connect((host, port))

        print("Client ID -> ", clientID)
        ClientSocket.send(str.encode(clientID))
        ack = Response = ClientSocket.recv(1024)

        while True:
            Response = ClientSocket.recv(1024)
            res = Response.decode('utf-8')

            if(res == "Requesting Screenshot"):
                print(res)
                screenshot = pyautogui.screenshot("Capture.PNG")
                filetosend = open("Capture.PNG", "rb")
                data = filetosend.read()
                print("Sending... len -> " , len(data))
                ClientSocket.sendall(data)
                filetosend.close()
                print("Done Sending.")
                print(ClientSocket.recv(1024))
        
            elif(res == "Click mouse"):
                print(res)
                Response = ClientSocket.recv(1024)
                jsondata = Response.decode('utf-8')
                print("jsondata -> " + jsondata)
                jsondata = json.loads(jsondata)
                pyautogui.leftClick(x = jsondata["X"] , y = jsondata["Y"])
                ClientSocket.sendall(str.encode("Clicked"))
    except Exception as e:
        print(str(e))
        for i in range(1,5):
            print("Error trying in " + str(i) + " sec")
            sleep(1)
        continue


ClientSocket.close()
