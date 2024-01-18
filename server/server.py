import socket
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("waiting for a connection, server started")

def threaded_client(conn, player):
    conn.send(str.encode("Connect"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()

            if not data:
                print("disconnected")
                break
            else:
                if player == 0:
                    reply = "hi player 1"
                else:
                    reply = "hi player 2"
                print("received: ", data)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("lost connection")
    conn.close()

currentPlayer=0
while True:
    conn, addr = s.accept()
    print("connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer +=1
