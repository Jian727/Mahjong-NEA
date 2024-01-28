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
# [conn, playerobject]
currentPlayerlist = [["", Player()], ["", Player()], ["", Player()], ["", Player()]]

def boardcast(data):
    global currentPlayerlist
    global game

    for client in currentPlayerlist:
        conn = client[0]
        if conn != "":
            try:
                if isinstance(data, Game):
                     conn.send(pickle.dumps(game))
                else:
                    conn.send(str.encode(data))
            except socket.error:
                # Handle disconnected client
                pass
                
def threaded_client(conn, player):
    global currentPlayerlist
    global game
    global round_count

    conn.send(pickle.dumps(game))
    data = conn.recv(2048).decode()
   
    currentPlayerlist[player][1].set_name(data)
    currentPlayerlist[player][1].set_connection()
    currentPlayerlist[player][0] = conn

    game.add_players(currentPlayerlist[player][1])
    
    conn.send(pickle.dumps(game))

    boardcast("new_player")

    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("disconnected")
                break
            else:
                if data == "request":
                # send the current state of the game to the client
                    conn.sendall(pickle.dumps(game))
                elif data == "start":
                    game.initialize_tiles()
                    game.initial_deck()
                    conn.sendall(pickle.dumps(game))
                    conn.send(str.encode(round_count))
                    game = pickle.loads(conn.recv(2048*8))
                    boardcast(game)

                else:
                    pass

        except:
            break


    print("lost connection")
    conn.close()

game = Game()
round_count = 0

while True:
    
    if currentPlayer<4:

        conn, addr = s.accept()
        print("connected to: ", conn)
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer +=1
    
    else:
        game.ready = True
