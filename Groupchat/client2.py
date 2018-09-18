import socket
from threading import Thread

tcpIP = 'localhost'
tcpPort = 5009
serverAddr= (tcpIP,tcpPort)
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect(('localhost',tcpPort))

def always_sending():
    while(1):

        name = input()
        clientSocket.send(bytes(name, "utf8"))

sendThread = Thread(target=always_sending)
sendThread.start()


while(1):

    msg = clientSocket.recv(1024).decode("utf8")
    print (msg)
clientSocket.close()




