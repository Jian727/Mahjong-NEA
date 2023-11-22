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

class Bonus:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
    