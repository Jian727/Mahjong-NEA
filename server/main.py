from deck import *
from functions import *
from game import *
from player import *
from tiles import *

player1 = Player()
player1.set_name("1")
player2 = Player()
player2.set_name("2")
player3 = Player()
player3.set_name("3")
player4 = Player()
player4.set_name("4")

game = Game()

game.add_players(player1)
game.add_players(player2)
game.add_players(player3)
game.add_players(player4)

game.initialize_tiles()
game.initial_deck()

for i in game.get_players():
    game.show_info(i)
    print()

count = 0
player = game.get_players()[0] 
player.get_deck().draw_tile()
while game.get_condition() != True:
    next = game.round(count)
    count = next

for player in game.get_players():
    if player.get_win():
        print(f"winner is {player.get_name()}")

