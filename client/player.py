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
        return self.deck.get_deck_tiles()

    def set_deck(self, deck):
        self.deck=deck
