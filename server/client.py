import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from network import Network
import random
import threading

windowDims = (960, 540)

class WelcomePage(tk.Frame):
    def __init__(self, master, welcomeToJoin, quit):
        super().__init__(master, width=windowDims[0], height=windowDims[1])  # Set background and dimensions

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("img/background_img.png")
        self.image = self.image.resize((windowDims[0], windowDims[1]), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=self.photo)

        self.canvas.create_text(windowDims[0]//2,  windowDims[1]//2-100, text="Mahjong!", font="calibri 60 bold", fill="white")

        self.button_play = tk.Button(self, text="Play", font=("calibri", 30), command=welcomeToJoin)
        self.button_play.place(x=windowDims[0]//2-75, y=windowDims[1]//2-25, width=150, height=50)

        self.button_quit = tk.Button(self, text="Quit", font=("calibri", 30), command=quit)
        self.button_quit.place(x=windowDims[0]//2-75, y=windowDims[1]//2+50, width=150, height=50)

class joiningPage(tk.Frame):
    def __init__(self, master, joinToRoom):
        super().__init__(master, width=windowDims[0], height=windowDims[1])

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("window/main_background.png")
        self.image = self.image.resize((windowDims[0], windowDims[1]), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=self.photo)

        self.name_var=tk.StringVar()
        self.canvas.create_text(windowDims[0]//2-200,  windowDims[1]//2-200, text="Please enter your name:", font="calibri 30", fill="white")
        e1 = Entry(self.canvas, textvariable = self.name_var, font=('calibri 24'))
        self.canvas.create_window(windowDims[0]//2+200, windowDims[1]//2-200, width = 400, height =40, window=e1)

        self.button_join = tk.Button(self, text="Join Room", font=("calibri", 30), command=joinToRoom)
        self.button_join.place(x=windowDims[0]//2-120, y=windowDims[1]//2-25, width=240, height=50)

class RoomPage(tk.Frame):
    def __init__(self, master, currentgame, network):
        super().__init__(master, width=windowDims[0], height=windowDims[1])

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.network = network
        self.game = currentgame
        self.status = False

        self.image = Image.open("img/main_background.png")
        self.image = self.image.resize((windowDims[0], windowDims[1]), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=self.photo)

        self.labels = [tk.Label(self, text="Waiting",font="calibri 15") for _ in range(4)]

        # Place labels on each side of the window
        for i, label in enumerate(self.labels):
            if i == 0:
                label.place(x=windowDims[0]//2-20, y=windowDims[1]-40)
            elif i == 1:
                label.place(x=windowDims[0]-80, y=windowDims[1]//2-20)
            elif i == 2:
                label.place(x=windowDims[0]//2-20, y=10)
            else:
                label.place(x=10, y=windowDims[1]//2-20)

    def get_status(self):
        return self.status
        
    def update_names(self, names):
        # Update labels with received names
        for i, name in enumerate(names):
            self.labels[i].config(text=name)

        self.update_idletasks()
        
        if "waiting" not in names:
            self.status = True

class MahjongGamePage(tk.Frame):
    def __init__(self, master, game):
        super().__init__(master, width=windowDims[0], height=windowDims[1])

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("img/main_background.png")
        self.image = self.image.resize((windowDims[0], windowDims[1]), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=self.photo)

        self.game = game

        #index 0-34, 34 is the back of tile
        self.img_path = []
        for i in range(34):
            self.img_path.append("img/{}.png".format(i))
        self.img_path.append("img/concealed.png")

    def create_button(self):

        self.buttons = []

        for i, image_path in enumerate(self.img_path):
            # Check if the image file exists

            image = Image.open(image_path)
            image = image.resize((50, 50), Image.Resampling.LANCZOS)  # Resize image as needed
            photo = ImageTk.PhotoImage(image)

            # Create button with image
            button = tk.Button(self, image=photo, text=f"Button {i+1}", compound="top", command=lambda btn=i: self.on_button_click(btn))
            button.image = photo  # Keep a reference to the image to prevent garbage collection
            button.pack(side=tk.LEFT, padx=5)

            # Add the button to the list
            self.buttons.append(button)


        

        '''# Create the game board
        self.game_board = tk.Frame(self, bg="green")  # Set background
        self.game_board.pack()

        self.tiles = []
        for row in range(4):
            for col in range(9):
                index = row * 9 + col
                tile = tk.Button(
                    self.game_board, text=self.tile_set[index],
                    width=4, height=2, command=lambda i=index: self.handle_tile_click(i),
                    bg="yellow"  # Set background
                )
                tile.grid(row=row, column=col, padx=2, pady=2)
                self.tiles.append(tile)

    def handle_tile_click(self, index):
        # Add your game logic here
        # You may want to handle tile matching, scoring, etc.
        print(f"Clicked tile at index {index}")'''

def main():
    def welcomeToJoin():
        # Destroy the welcome page and show the game page after connecting
        global joining_page
        welcome_page.destroy()
        joining_page = joiningPage(root, joinToRoom)
        joining_page.pack()

    def getPlayersName(game, myname):
        players = game.get_players()
        names = []
        for player in players:
            names.append(player.get_name())

        while len(names) != 4:
            names.append("waiting")
            
        
        index = names.index(myname)
        names = names[index:]+names[:index]
        
        return names
    
    def listen_for_notifications(network, name):
        global room_page
    
        while True:
            #when 4 players, open new game window and start game
            if room_page.get_status() == True:
                roomToGame()
                break
            else:
                try:
                    notification = network.receive_string()
                    if notification == "new_player":
                        # Handle the notification that a new player joined
                        currentgame = network.send("request")
                        room_page.update_names(getPlayersName(currentgame, name))
                    else:
                        # Handle other types of notifications
                        pass
                except Exception as e:
                    print(f"Error receiving notification: {e}")
                    break

    def joinToRoom():
        global joining_page
        global n
        global room_page

        name = joining_page.name_var.get()
        n = Network()
        n.getGame()
        currentgame = n.send(name)
        joining_page.destroy()

        room_page = RoomPage(root, currentgame, n)
        room_page.pack()

        listen_thread = threading.Thread(target=listen_for_notifications, args=(n, name))
        listen_thread.start()

    def roomToGame():
        global room_page
        global n

        currentgame = n.send("start")
        room_page.destroy()

        mahjong_game = MahjongGamePage(root, currentgame)
        mahjong_game.pack()





    def quit():
        root.quit()

    root = tk.Tk()
    root.title("Mahjong Game")

    # Create and show the welcome page initially
    welcome_page = WelcomePage(root, welcomeToJoin, quit)
    welcome_page.pack()



    run = True
    
    while run:
        root.mainloop()

if __name__ == "__main__":
    main()
