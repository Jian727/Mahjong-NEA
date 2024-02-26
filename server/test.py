from deck import *
from tiles import *
from functions import *
from game import *

game = Game()
game.add_tilesoutside(Tiles(9,0))
hand = numToTiles([1,1,2,3,5,6,9,15,16,17,27,27])
deck = Deck(hand, game)
print(f"input: {hand}")
print(f"outside: {game.get_tilesoutside()}")
print()
print(f"readable input:{tilesToNum(hand)}")
print(f"readable outside: {tilesToNum(game.get_tilesoutside())}")

print()

result = deck.findChow()
print(f"result: {result}")
if result != None:
    print(f"readable result: {tilesToNum(result)}")