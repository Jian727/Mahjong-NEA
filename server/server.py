import socket
from _thread import *
import sys

server = "192.168.0.116"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(s)

s.listen(4)
print("waiting for a connection, server started")

def threaded_client(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("disconnected")
                break
            else:
                print("received: ", reply)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

while True:
    conn, addr = s.accept()
    print("connected to: ", addr)

    start_new_thread(threaded_client, (conn, ))
