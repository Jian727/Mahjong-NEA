import socket
import pickle
from game import Game

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.game = self.connect()

    def getGame(self):
        return self.game

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def onlysend(self, data): #only send no return
        try:
            if isinstance(data, Game):
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
        except:
            pass

    def send(self, data): #return object
        try:
            if isinstance(data, Game):
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))

            result = self.client.recv(2048*8)
            return pickle.loads(result)
            
        except socket.error as e:
            print(e)


    def receive_object(self):#return object
        try:
            data = self.client.recv(2048*8)
            if not data:
                return None
            deserialized_data = pickle.loads(data)
            return deserialized_data
        except:
            pass

    def receive_string(self):#return string
        try:
            data = self.client.recv(2048).decode()
            if not data:
                return None
            return data
        except:
            pass

    

