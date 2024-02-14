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
                   
                    print("waiting response")
                    response = conn.recv(2048).decode()#receive pung or not
                    print(f"response: {response}")
                    if response == "True":
                        print('not done')
                        print(count_temp)
                        print(pungset)
                        game.get_players()[count_temp].get_deck().Pung(pungset)
                        print('done')
                        round_count = count_temp
                        broadcast("have pung")
                    else:
                        broadcast("didn't have pung")
                    
                    
                    #wait for respond

                else:
                    pass

        except:
            break


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

