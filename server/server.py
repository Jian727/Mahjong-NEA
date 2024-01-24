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
currentPlayerlist = [Player(), Player(), Player(), Player()]

def threaded_client(conn, player, game):
    global currentPlayerlist

    conn.send(pickle.dumps(currentPlayerlist[player]))
    data = pickle.loads(conn.recv(2048))
    currentPlayerlist[player] = data
    game.add_players(currentPlayerlist[player])
    conn.send(pickle.dumps(game))

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
                print("player name: ", currentPlayerlist[player].get_name())

        except:
            break

    print("lost connection")
    conn.close()


while True:
    
    if currentPlayer<4:

        conn, addr = s.accept()
        print("connected to: ", addr)

        game =Game()

        start_new_thread(threaded_client, (conn, currentPlayer, game))
        currentPlayer +=1
    
    else:
        game.ready = True
