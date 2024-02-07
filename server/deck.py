
#import websockets
from itertools import combinations, chain
from functions import *

#NOT FINISHED
class Deck:
    def __init__(self, hands, game):
        self.deck_tiles = hands #an array of instances of Tiles
        self.showed_tiles = []
        self.game = game


    def get_deck_tiles(self):

        n = len(self.deck_tiles)  
        if n <= 1:
            return None
        for i in range(1, n):  
            temp = self.deck_tiles[i]  
            j = i-1
            while j >= 0 and temp.get_cal_value() < self.deck_tiles[j].get_cal_value():  
                self.deck_tiles[j+1] = self.deck_tiles[j] 
                j -= 1
            self.deck_tiles[j+1] = temp
        return self.deck_tiles
    
    def get_showed_tiles(self):
        return self.showed_tiles
        
    def draw_tile(self):
        tile = self.game.draw_tile()
        if tile != None:
            self.deck_tiles.append(tile)
        else:
            self.game.endgame()

    def discard_tile(self, num): 
        #need to return the tile for discarding piles for actions
        index = tilesToNum(self.deck_tiles).index(num)
        tile = self.deck_tiles[int(index)]
        self.deck_tiles.remove(tile)
        self.game.add_tilesoutside(tile)
    
    def tiles_attribute(self): #get type and value and cal_value
        attributes = []
        for tile in self.deck_tiles:
            temp = [tile.get_type(), tile.get_value(), tile.get_cal_value()]
            attributes.append(temp)
        return attributes
    
    def determine_winning_deck(self): #determine if the deck is a winning_deck
        attribute_list = self.tiles_attribute()
        sum_of_tiles = sum(sub_arr[1] for sub_arr in attribute_list if len(sub_arr) > 1)
        pairNum = sum_of_tiles%3
        for sub_arr in attribute_list:
            temp = attribute_list.copy()
            if pairNum == 1:
                pairNum = 2
            elif pairNum ==2:
                pairNum =1

            if sub_arr[2] in range(pairNum,34,3):
                temp.remove(sub_arr)
                if sub_arr in temp: #pair exist
                    temp.remove(sub_arr) #remove pair
                    while len(temp)!= 0:
                        check = temp[0]
                        type, value, cal_value= check
                        if temp.count(check) < 3: #remove chow
                            if [type, value+1, cal_value+1] in temp and [type, value+2, cal_value+2] in temp:
                                temp.remove([type, value, cal_value])
                                temp.remove([type, value+1, cal_value+1])
                                temp.remove([type, value+2, cal_value+2])
                            else:
                                break     
                        else: #remove pung
                            temp.remove([type, value, cal_value])
                            temp.remove([type, value, cal_value])
                            temp.remove([type, value, cal_value])
                    if len(temp) == 0:
                        return True
        return False

    def findPung(self):
        discarded_tile = self.game.get_tilesoutside()
        if len(discarded_tile) == 0:
            print("No tile in discarded tile")
            return None
        last_discarded_tile = discarded_tile[-1]
        for pair in combinations(self.deck_tiles, 2):
            temp = list(pair)
            temp.append(last_discarded_tile)
            if checkPung(temp):
                print("Found pung")
                return temp
        print("Can't find pung")
        return None
    
    def findChow(self):
        discarded_tile = self.game.get_tilesoutside()
        if len(discarded_tile) == 0:
            return None
        last_discarded_tile = discarded_tile[-1]
        result_list = []
        for pair in combinations(self.deck_tiles, 2):
            temp = list(pair)
            temp.append(last_discarded_tile)
            if checkChow(temp):
                result_list.append(temp)
        if len(result_list) == 0:
            return None
        return result_list
    
    def findKong(self): #not finished
        for tiles in combinations(self.deck_tiles, 4):
            if checkPung(tiles):
                return True  
        #pung on showed_tiles, draw one more
        #pung in deck_tiles, other discarded one more
        return False
    
    def Pung(self, pung_set): 
        if not checkPung(pung_set): #validate if it is pung
            return None
        
        tile1, tile2, tile3 = pung_set

        self.deck_tiles.remove(tile1)
        self.deck_tiles.remove(tile2)
        self.showed_tiles.append(pung_set)
        self.game.pop_tilesoutside()
        

    def Chow(self, chow_set):
        if not checkChow(chow_set): #validate if it is pung
            return None
        
        tile1, tile2, tile3 = chow_set
        
        self.deck_tiles.remove(tile1)
        self.deck_tiles.remove(tile2)
        self.showed_tiles.append(chow_set)
        self.game.pop_tilesoutside()
    
    def Kong(self, kong_set): #not finished
        pass
    
    


    
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

