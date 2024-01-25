import socket
from _thread import *
import pickle
from player import Player
from game import Game

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("waiting for a connection, server started")

currentPlayer=0
currentPlayerlist = [["", Player()], ["", Player()], ["", Player()], ["", Player()]]
connlist = []

def broadcast_to_clients(exclude_player):
    global currentPlayerlist
    global game

    for i, client in enumerate(currentPlayerlist):
        if i != exclude_player and client.get_connection():
            try:
                client.get_connection().send(pickle.dumps(game))
            except socket.error:
                # Handle disconnected client
                currentPlayerlist[i][0].disconnect()

def threaded_client(conn, player):
    global currentPlayerlist
    global game

    conn.send(pickle.dumps(currentPlayerlist[player][1]))
    data = pickle.loads(conn.recv(2048))
    currentPlayerlist[player][1] = data
    currentPlayerlist[player][1].set_connection()
    currentPlayerlist[player][0] = conn

    game.add_players(currentPlayerlist[player][1])
    print(type(game))
    conn.send(pickle.dumps(game))
    broadcast_to_clients(currentPlayerlist[player][1])

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("disconnected")
                break
            else:
                currentPlayerlist[player] = data

                conn.send(pickle.dumps(game))

                print("received: ", data.get_name())
                print("player name: ", currentPlayerlist[player][1].get_name())

        except:
            break


    print("lost connection")
    conn.close()

game = Game()

while True:
    
    if currentPlayer<4:

        conn, addr = s.accept()
        print("connected to: ", conn)
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer +=1
    
    else:
        game.ready = True
