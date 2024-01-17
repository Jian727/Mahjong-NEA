import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from network import Network

class WelcomePage(tk.Frame):
    def __init__(self, master, on_connect, on_quit):
        super().__init__(master, bg="lightblue", width=960, height=540)  # Set background and dimensions
        self.on_connect = on_connect
        self.windowDims = (960, 540)

        self.canvas = tk.Canvas(self, width=self.windowDims[0], height=self.windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("window/background_img.png")
        self.image = self.image.resize((self.windowDims[0], self.windowDims[1]), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.windowDims[0]//2, self.windowDims[1]//2, image=self.photo)

        self.canvas.create_text(self.windowDims[0]//2,  self.windowDims[1]//2-100, text="Mahjong!", font="calibri 60 bold", fill="white")

        self.button_play = tk.Button(self, text="Play", font=("calibri", 30), command=self.on_click_play)
        self.button_play.place(x=self.windowDims[0]//2-75, y=self.windowDims[1]//2-25, width=150, height=50)

        self.button_quit = tk.Button(self, text="Quit", font=("calibri", 30), command=on_quit)
        self.button_quit.place(x=self.windowDims[0]//2-75, y=self.windowDims[1]//2+50, width=150, height=50)


    def on_click_play(self):
        # Implement your server connection logic here
        # For simplicity, let's assume the connection is successful
        messagebox.showinfo("Connection", "Connected to the server successfully!")
        self.on_connect()


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
    def on_connect():
        # Destroy the welcome page and show the game page after connecting
        welcome_page.destroy()
        MahjongGamePage(root).pack()
    
    def on_quit():
        root.quit()

    root = tk.Tk()
    root.title("Mahjong Game")

    # Create and show the welcome page initially
    welcome_page = WelcomePage(root, on_connect, on_quit)
    welcome_page.pack()



    run = True
    n = Network()
    startId = n.getId()
    n.send("hello")
    n.send(startId)
    while run:
        root.mainloop()

if __name__ == "__main__":
    main()
