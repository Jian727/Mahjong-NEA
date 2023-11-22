from deck import *
from functions import *
from game import *
from player import *
from tiles import *

game = Game()
tiles = [2,2,2,3,3,3,4,4,4,31,31,31,32]
new_tiles = numToTiles(tiles)
print(tiles)
deck = Deck(new_tiles)
win = deck.determine_last_tile(game)
print(win)