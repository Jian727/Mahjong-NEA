class Player:
    def __init__(self):
        self.name = ""
        self.deck = None
        self.win = False

    def set_name(self, n_name):
        self.name = n_name

    def get_name(self):
        return self.name
    
    def get_deck(self):
        return self.deck
    
    def get_win(self):
        return self.win
    
    def set_win(self):
        self.win = True

    def get_connection(self):
        return self.connection

    def get_deck_tiles(self):
        return self.deck.get_deck_tiles()
    
    def get_showed(self):
        return self.deck.get_showed_tiles()

    def set_deck(self, deck):
        self.deck=deck
