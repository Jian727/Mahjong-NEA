import random
import asyncio
from tiles import *
from deck import *

class Game:
    def __init__(self):
        self.tiles = [] #represent all the tiles
        self.tilesremain= self.initialize_tiles() #represent the avaliable tiles on table 
        self.tilesoutside=[] #represent the tiles discarded on table
        self.roomnum=0
        self.playerconns=[]
        self.players=[]
        self.names=[]
        self.condition=False
        self.queue=asyncio.Queue()
        self.message=False
        
    async def updatequeue(self,data):
        await self.queue.put(data)

    async def getqueue(self):
        temp=await self.queue.get()
        return temp
    
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

        #bonus
        for value in range(8):
            tiles.append(Bonus(value))

        random.shuffle(tiles)
        return tiles
    
    def initial_deck(self):
        #initiallise deck for each player
        for player in self.players:
            hand = []
            for i in range(13):
                tile = self.tilesremain.pop(0)
                hand.append(tile)
            player_deck = Deck(hand)
            player.set_deck(player_deck)

    def display_tiles(self, player):
        #display deck for the player stated
        for i in self.players:
            if i == player:
                deck = i.get_deck()
                return deck
    
    def add_tilesoutside(self, tile):
        self.tilesoutside.append(tile)
    
    def get_tilesoutside(self):
        return self.tilesoutside
    
    def get_tilesremain(self):
        return self.tilesremain
    
    def get_tiles(self):
        return self.tiles
