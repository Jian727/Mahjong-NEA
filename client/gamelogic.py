import random
import asyncio
import websockets

class Tiles:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.cal_value = type + value

    def get_type(self):
        return self.type

class Suited(Tiles):
    pass

class Honor(Tiles):
    pass

class Bonus:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

class Deck:
    def __init__(self, hands):
        self.deck_tiles = hands
        self.showed_tiles = []
        self.winning_tiles = []

    def get_deck_tiles(self):
        return self.deck_tiles
    
    def get_showed_tiles(self):
        return self.showed_tiles
    
    def get_winning_tiles(self):
        return self.winning_tiles
    
    def change_winning_tiles(self, tiles):
        self.winning_tiles = tiles

    def set_deck_tiles(self, tiles):
        self.deck_tiles = tiles

    def set_showed_tiles(self, tiles):
        self.showed_tiles = tiles

class Player:
    def __init__(self,connection,name):
        self.name=name
        self.deck=[]
        self.connection=connection

    def get_name(self):
        return self.name
    
    def get_connection(self):
        return self.connection

    def get_deck(self):
        return self.deck

    def set_deck(self, deck):
        self.deck=deck


class Game:
    def __init__(self):
        self.tiles = self.initialize_tiles()
        self.tilesoutside=[]
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

        for i in range(4):
            #dots, bamboo, characters
            for type in range(0, 19, 9): #type = 0,9,18
                for value in range(9): #value = 0-8
                    tiles.append(Suited(type, value))

            #winds
            for value in range(4): #value = 0-3
                tiles.append(Honor(27, value))
            
            #dragons
            for value in range(3): #value = 0-2
                tiles.append(Honor(31, value))

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
                tile = self.tiles.pop(0)
                hand.append(tile)
            player_deck = Deck(hand)
            player.set_deck(player_deck)

    def display_tiles(self, player):
        #display deck for the player stated
        for i in self.player:
            if i == player:
                deck = i.get_deck()
                return deck
    

        
        
    
'''class MahjongGame(game):

    def initialize_tiles(self):
        # Define the set of Mahjong tiles (simplified for this example)
        # You may want to customize this based on the specific rules you're using
        suits = ["Bamboo", "Character", "Circle"]
        honors = ["East", "South", "West", "North", "Red", "Green", "White"]
        numbers = [str(i) for i in range(1, 10)]

        tiles = [f"{suit} {number}" for suit in suits for number in numbers] + honors * 4
        return tiles

    def shuffle_tiles(self):
        random.shuffle(self.tiles)

    def deal_tiles(self):
        hands = {player: [] for player in self.players}
        for _ in range(self.hand_size):
            for player in self.players:
                tile = self.tiles.pop(0)
                hands[player].append(tile)
        return hands

    def display_tiles(self, player, tiles):
        print(f"{player}'s hand:")
        for tile in tiles:
            print(tile)

    def start_game(self):
        # Initialize and shuffle tiles
        self.tiles = self.initialize_tiles()
        self.shuffle_tiles()

        # Deal tiles to players
        hands = self.deal_tiles()

        # Display each player's hand
        for player, tiles in hands.items():
            self.display_tiles(player, tiles)

        # Implement the game loop here
        # - Allow players to take turns
        # - Implement the game rules (drawing, discarding, declaring Mahjong, etc.)
        # - Determine the winner based on the rules'''

'''if __name__ == "__main__":
    mahjong_game = MahjongGame()
    mahjong_game.start_game()'''

