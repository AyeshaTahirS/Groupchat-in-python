import socket
from threading import Thread

tcpIP = 'localhost'
tcpPort = 5009
buffSize =1024
clients ={}
addresses = {} #storing clients as keys and their addresses as value
socketAddress = (tcpIP,tcpPort)
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(socketAddress)
counter =0
def always_accepting_users():
    while True:
        client , clientAddr = serverSocket.accept()
        print('This client is connected', clientAddr)
        client.send(bytes("Hello, to Ayesha's! Please let us know your name! " ,"utf8"))
        addresses[client] = clientAddr
        Thread(target=one_client, args=(client,)).start()


def one_client(client):
    name = client.recv(1024).decode("utf8")
    new = name.upper()
    greeting = 'Hello,  %s ! if you want to exit, press quit' %new
    client.send(bytes(greeting,"utf8"))
    greetToAll ="Hey Peeps , %s has joined us in our venture " %new
    broadcast(bytes(greetToAll, "utf8"))
    clients[client] = name.lower()

    while True:
        msg = client.recv(1024)
        one2one = msg.decode("utf8")
        newMsg =":"
        oneCheck =0
        if "to:" and " " in one2one:
            nick = ""
            start = one2one.index(':')
            end = one2one.index(' ')
            for i in range(start+1,end):
                nick= nick + one2one[i]
                nick= nick.lower()
            print(nick)
            for c in clients:
                if(clients[c] == nick):
                    print("if checked")
                    for i in range (end+1 , len(one2one)):
                        newMsg= newMsg+ one2one[i]
                    broadcast(bytes(newMsg, "utf8"), name, c)
                    oneCheck=1


            if oneCheck is not 1 :

                print("else checked")
                client.send(bytes("Hello, this user, doesn't exist!","utf8"))

        elif msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def broadcast(msg , prefix="",one2one=""):
    if (one2one) :
        print("isko bhejo-->" ,one2one)
        print(clients)

        one2one.send(bytes(prefix, "utf8") + msg)

    else :

        for c in clients :
            if(clients[c]!=prefix):
                c.send(bytes(prefix, "utf8") + msg)


serverSocket.listen()  # Listens for 5 connections at max.
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=always_accepting_users)
ACCEPT_THREAD.start()  # Starts the infinite loop.
ACCEPT_THREAD.join()
serverSocket.close()


