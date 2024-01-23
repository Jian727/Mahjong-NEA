import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from network import Network
import random
from player import Player

windowDims = (960, 540)

class WelcomePage(tk.Frame):
    def __init__(self, master, welcomeToJoin, quit):
        super().__init__(master, width=windowDims[0], height=windowDims[1])  # Set background and dimensions

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("window/background_img.png")
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
    def __init__(self, master, roomToGame, currentPlayer, n):
        super().__init__(master, width=windowDims[0], height=windowDims[1])

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("window/main_background.png")
        self.image = self.image.resize((windowDims[0], windowDims[1]), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=self.photo)

class MahjongGamePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="green", width=800, height=600)  # Set background and dimensions

        # Sample tile set (numbers 1 to 9, four of each)
        self.tile_set = [str(i) for i in range(1, 10)] * 4

        # Shuffle the tiles
        random.shuffle(self.tile_set)

        # Create the game board
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
        print(f"Clicked tile at index {index}")

def main():
    def welcomeToJoin():
        # Destroy the welcome page and show the game page after connecting
        global joining_page
        welcome_page.destroy()
        joining_page = joiningPage(root, joinToRoom)
        joining_page.pack()

    def joinToRoom():
        global joining_page
        global n
        name = joining_page.name_var.get()
        n = Network()
        p = n.getPlayer()
        p.set_name(name)
        currentplayers = n.send(p)
        joining_page.destroy()
        room_page = RoomPage(root, roomToGame, currentplayers, n)
        room_page.pack()

    def roomToGame():
        pass

    
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
