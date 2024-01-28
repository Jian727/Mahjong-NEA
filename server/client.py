import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from network import Network
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

        self.image = Image.open("img/main_background.png")
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
    def __init__(self, master, currentgame):
        super().__init__(master, width=windowDims[0], height=windowDims[1])

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

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
    def __init__(self, master, game, network, name):
        super().__init__(master, width=windowDims[0], height=windowDims[1])

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("img/main_background.png")
        self.image = self.image.resize((windowDims[0], windowDims[1]), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=self.photo)

        self.game = game
        self.network = network

        #get player number
        for i, player in enumerate(self.game.get_players()):
            if player.get_name() == name:
                self.player_num = i

        #index 0-34, 34 is the back of tile
        self.img_path = []
        for i in range(36):
            self.img_path.append("img/{}.png".format(i))

        self.create_tiles()

    def get_player_num(self):
        return self.player_num
    
    def get_game(self):
        return self.game

    def update_game(self, game):
        self.game = game

    def rotate_image(self, img):
        result =img.rotate(90, expand=True)
        return result.resize((40, 29),Image.LANCZOS)

    def create_tiles(self):
        deck = self.game.get_players()[self.player_num].get_deck().get_deck_tiles()
        self.buttons = []
        self.discard = False

        #create button for own deck
        for i, tile in enumerate(deck):
            num = tile.get_cal_value()
            image = Image.open(self.img_path[num])
            photo = ImageTk.PhotoImage(image)
            button1 = Button(self, image=photo, compound="center")
            button1.config(command=lambda n=num, b=button1: self.click(n, b))
            button1.image = photo
            self.canvas.create_window(i*40+200, windowDims[1]-40, window=button1)
            self.buttons.append(button1)
        

        #create image for others deck
        print(self.img_path[34])
        back =Image.open(self.img_path[34])
        photo_back = ImageTk.PhotoImage(back)
        rotated_photo_back = ImageTk.PhotoImage(self.rotate_image(back))
        self.photo_back= photo_back
        self.rotated_photo_back = rotated_photo_back

        self.left_player = []
        self.opp_player = []
        self.right_player = []

        for i in range(13):
            self.left_player.append(self.canvas.create_image(20, i*33+60, anchor=tk.NW, image=self.rotated_photo_back))
            self.opp_player.append(self.canvas.create_image(i*40+200, 0, anchor=tk.NW, image=self.photo_back))
            self.right_player.append(self.canvas.create_image(windowDims[0]-60, i*33+60, anchor=tk.NW, image=self.rotated_photo_back))

        self.opp_player.reverse()
        self.right_player.reverse()

    def update_tile_button(self):
        self.discard = True

        deck = self.game.get_players()[self.player_num].get_deck().get_deck_tiles()

        for i, tile in enumerate(deck):

            num = tile.get_cal_value()
            image = Image.open(self.img_path[num])
            photo = ImageTk.PhotoImage(image)
            
            if i < 14:
                button = self.buttons[i]
                button.config(command= lambda n=num, b=button : self.click(n), image=photo)
            else:
                button = Button(self, image=photo, command=lambda n=num, b=button: self.click(n,b), compound="center")
                button.config(command=lambda n=num, b=button: self.click(n, b))
                self.canvas.create_window(i*40+200, windowDims[1]-40, window=button)
                self.buttons.append(button)



        
        


    
    def click(self, num, button):
        if not self.discard:
            pass
        else:
            self.game
            self.discard = False


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

    def update_game(network, game):
        global mahjong_game

        while True:
            try:
                round_count = int(network.receive_string())
                if mahjong_game.get_player_num() == round_count:
                    player = game.get_players()[0] 
                    player.get_deck().draw_tile()

            except Exception as e:
                print(f"Error receiving notification: {e}")
                break

    def joinToRoom():
        global joining_page
        global n
        global room_page
        global name

        name = joining_page.name_var.get()
        n = Network()
        n.getGame()
        currentgame = n.send(name)
        joining_page.destroy()

        room_page = RoomPage(root, currentgame)
        room_page.pack()

        listen_thread = threading.Thread(target=listen_for_notifications, args=(n, name))
        listen_thread.start()

    def roomToGame():
        global room_page
        global n
        global name
        global mahjong_game

        currentgame = n.send("start")
        room_page.destroy()

        mahjong_game = MahjongGamePage(root, currentgame, n, name)
        mahjong_game.pack()
        currentgame = mahjong_game.get_game()
        listen_thread2 =  threading.Thread(target=update_game, args=(n, currentgame))
        listen_thread2.start()

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
