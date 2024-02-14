import socket
from _thread import *
import pickle
from player import Player
from game import Game
from functions import *

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("waiting for a connection, server started")



def broadcast(data):
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

    broadcast("new_player")

    while True:

        data = conn.recv(2048).decode()
        if not data:
            print("disconnected")
            break
        else:
            if data == "request":
            # send the current state of the game to the client
                conn.sendall(pickle.dumps(game))

            elif data == "start":
                if len(game.get_tilesremain()) == 0:
                    game.initialize_tiles()
                    game.initial_deck()
                conn.sendall(pickle.dumps(game))

            elif data == "draw":
                conn.sendall(pickle.dumps(game))
                conn.sendall(str.encode(str(round_count)))

            elif data == "discard":
                global count_temp
                global pungset

                game = pickle.loads(conn.recv(2048*8))
                round_count +=1
                round_count = round_count % 4
                broadcast("pung check")
                broadcast(game)

                pung = game.check_pung(player)
                if pung != None:
                    count_temp, pungset = pung
                    broadcast(str(count_temp))

                else:
                    broadcast("no pung")

            elif data == "pung":
                
                response = conn.recv(2048).decode()#receive pung or not
                if response == "True":
                    game.get_players()[count_temp].get_deck().Pung(pungset)
                    round_count = count_temp
                    broadcast("have pung")
                else:
                    broadcast("didn't have pung")

                #wait for respond
                    
            elif data == "check chow":
                chowsets = game.check_chow(player)
                if chowsets == None:
                    conn.send(str.encode("no chow"))
                    broadcast("chow done 2")
                    
                else:
                    num_of_chow = len(chowsets)
                    conn.send(str.encode(str(num_of_chow)))
    
                    response = conn.recv(2048).decode()#receive chow or not
                    if response == "True":
                        print(f"response = {response}")
                        if num_of_chow == 1:
                            chowset = chowsets[0]
                            game.get_players()[player].get_deck().Chow(chowset)
                        else:
                            for chowset in chowsets:
                                cal_val_chowset = tilesToNum(chowset)
                                cal_val_chowset = ','.join(map(str, cal_val_chowset))
                                conn.send(str.encode(cal_val_chowset))
                            set_decision = conn.recv(2048).decode()
                            game.get_players()[player].get_deck().Chow(chowsets[int(set_decision)])

                        broadcast("chow done 1")
                    else: 
                        broadcast("chow done 2")

            else:
                pass




    print(f"lost connection, player: {player}")
    conn.close()

currentPlayer=0
# [conn, playerobject]
currentPlayerlist = [["", Player()], ["", Player()], ["", Player()], ["", Player()]]

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

