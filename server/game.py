import random
from tiles import *
from deck import *

class Game:
    def __init__(self):
        self.tiles = [] #represent all the tiles
        self.tilesremain= [] #represent the avaliable tiles on table 
        self.tilesoutside=[] #represent the tiles discarded on table
        self.players=[]
        self.condition=False
    
    def get_tilesoutside(self):
        return self.tilesoutside
    
    def pop_tilesoutside(self):
        self.tilesoutside.pop(-1)
    
    def get_tilesremain(self):
        return self.tilesremain
    
    def get_tiles(self):
        return self.tiles
    
    def get_players(self):
        return self.players

    def get_condition(self):
        for i in self.players:
            if i.get_deck().determine_winning_deck() == True:
                self.endgame()
                i.set_win()
        if len(self.get_tilesremain()) == 0:
            self.endgame()
        return self.condition
    
    def draw_tile(self):
        if len(self.tilesremain) != 0:
            tile = self.tilesremain[0]
            self.tilesremain.remove(tile)
            return tile
        else:
            self.endgame()
            return None
    
    def add_tilesoutside(self, tile):
        self.tilesoutside.append(tile)

    def add_players(self, player):
        self.players.append(player)
    
    def initialize_tiles(self):
        # Define the set of Mahjong tiles
        # Randomised after initializing
        tiles = []
        onetime = True

        for i in range(4):
            #dots, bamboo, characters
            for type in range(0, 19, 9): #type = 0,9,18
                for value in range(9): #value = 0-8
                    tiles.append(Suited(type, value))
                    if onetime:
                        self.tiles.append(tiles[-1])

            #winds
            for value in range(4): #value = 0-3
                tiles.append(Honor(27, value))
                if onetime:
                    self.tiles.append(tiles[-1])
            
            #dragons
            for value in range(3): #value = 0-2
                tiles.append(Honor(31, value))
                if onetime:
                    self.tiles.append(tiles[-1])
            
            onetime = False

        random.shuffle(tiles)
        self.tilesremain = tiles

    def show_info(self, player):
        global deck, showed
        print(f"Name: {player.get_name()}")
        deck, showed = self.display_tiles(player)
        print(f"deck: {tilesToNum(deck)}, showed: {tilesToNum(showed)}")

    #can't pung first discarded tile
    def check_pung(self, player_num):
        count_temp = player_num + 1
        for i in range(3): #pung check 
            count_temp = count_temp % 4
            player_check = self.get_players()[count_temp]
            player_deck_check = player_check.get_deck()
            pungset = player_deck_check.findPung()
            if pungset != None:
                return(count_temp, pungset)
            count_temp += 1
        return None
    
    def check_chow(self, player_num):
        player = self.get_players()[player_num]
        player_deck = player.get_deck()
        chowsets = player_deck.findChow()
        if chowsets != None: #chow check
            return(chowsets)
        return None


    def round(self, player_num): #need to return next player_num
        #check if can win or not
        #discard
        player = self.get_players()[player_num]
        player_deck  = player.get_deck()
        self.show_info(player)
        discard = int(input("Please input the tile you want to discard: "))
        player_deck.discard_tile(discard)
        print(f"tile discarded, tiles remain:{len(self.get_tilesremain())}")
        print(f"tile outside: {tilesToNum(self.get_tilesoutside())}")
        print()

        #check pung
        count_temp = player_num + 1
        for i in range(3): #pung check 
            count_temp = count_temp % 4
            player_check = self.get_players()[count_temp]
            print(f"player pung check: {player_check.get_name()}")
            player_deck_check = player_check.get_deck()
            pungset = player_deck_check.findPung()
            if pungset != None:
                self.show_info(player_check)
                decision = input(f"Name: {player_check.get_name()} can pung {tilesToNum(pungset)}! do you want to pung? (y/n)")
                if decision == "y":
                    player_deck_check.Pung(pungset)
                    print()
                    return count_temp
                else:
                    print()
            count_temp += 1

        #check next player chow
        next_player_num = (player_num + 1)%4
        next_player = self.get_players()[next_player_num]
        next_player_deck = next_player.get_deck()
        print(f"player chow check: {next_player.get_name()}")
        chowsets = next_player_deck.findChow()
        if chowsets != None: #chow check
            print("have chow")
            for chowset in chowsets:
                self.show_info(next_player)
                decision = input(f"Name: {next_player.get_name()} can chow {tilesToNum(chowset)}! do you want to chow? (y/n)")
                if decision == "y":
                    next_player_deck.Chow(chowset)
                    print()
                    return next_player_num
        print()
        self.get_players()[next_player_num].get_deck().draw_tile() 
        return next_player_num
    
    def initial_deck(self):
        #initiallise deck for each player
        for player in self.players:
            hand = []
            for i in range(13):
                tile=self.tilesremain.pop(0)
                hand.append(tile)
            player_deck = Deck(hand, self)
            player.set_deck(player_deck)
            
    def display_tiles(self, player):
        #display deck for the player stated
        for i in self.players:
            if i == player:
                deck = i.get_deck_tiles()
                displayed = i.get_showed()
                return [deck,displayed]
            
    def endgame(self):
        #end the game by having winner or used all tiles
        self.condition = True
