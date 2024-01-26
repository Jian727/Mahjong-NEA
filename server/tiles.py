'''
bamboo = 0-8
char = 9-17
dots = 18-26
winds = 27-30
dragons = 31-33
'''

class Tiles:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.cal_value = type + value

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value
    
    def get_cal_value(self):
        return self.cal_value

class Suited(Tiles):
    pass

class Honor(Tiles):
    pass

