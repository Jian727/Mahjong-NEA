from client import *
from game import *
from player import Player

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

root = tk.Tk()
root.title("Mahjong Game")
n = Network()

mahjong_game = MahjongGamePage(root, game, "1")
mahjong_game.pack()

run = True
    
while run:
    root.mainloop()