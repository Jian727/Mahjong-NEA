import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from network import Network
import threading
from functions import *

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

        self.game = game
        self.network = network

        self.canvas = tk.Canvas(self, width=windowDims[0], height=windowDims[1], highlightthickness=0)
        self.canvas.pack()

        self.image = Image.open("img/main_background.png")
        self.image = self.image.resize((windowDims[0], windowDims[1]), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=self.photo)

        self.outside_tiles = []
        self.outside_tiles_image = []
        self.showed_tiles_image = []
        self.others_showed_tiles_image = []

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
    
    def rotate_image_rev(self, img):
        result =img.rotate(270, expand=True)
        return result.resize((40, 29),Image.LANCZOS)
    
    def rotate_image_opp(self, img):
        result =img.rotate(180, expand=True)
        return result

    def create_tiles(self):
        deck = self.game.get_players()[self.player_num].get_deck().get_deck_tiles()
        self.buttons = []
        self.discard = False
        self.remain_tiles = self.canvas.create_text(windowDims[0]//2, windowDims[1]//2, text = str(len(self.game.get_tilesremain())), font="calibri 30", fill="white")

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

    def decide_pung(self):
        self.decidebutton =[]
        self.pung_decision = None
        button1 = Button(self, text="Pung", font=("calibri", 15), command=self.pung)
        self.decidebutton.append(button1)
        self.canvas.create_window(windowDims[0]-250, windowDims[1]-80, window=button1)
        button2 = Button(self, text="Skip", font=("calibri", 15), command=self.skip)
        self.decidebutton.append(button2)
        self.canvas.create_window(windowDims[0]-200, windowDims[1]-80, window=button2)
        while self.pung_decision == None:
            if self.pung_decision != None:
                return self.pung_decision
    
    def decide_chow(self):
        self.decidebutton =[]
        self.chow_decision = None
        button1 = Button(self, text="chow", font=("calibri", 15), command=self.chow)
        self.decidebutton.append(button1)
        self.canvas.create_window(windowDims[0]-250, windowDims[1]-80, window=button1)
        button2 = Button(self, text="Skip", font=("calibri", 15), command=self.skip)
        self.decidebutton.append(button2)
        self.canvas.create_window(windowDims[0]-200, windowDims[1]-80, window=button2)
        while self.chow_decision == None:
            if self.chow_decision != None:
                return self.chow_decision
            
    def decide_chow_set(self, chowsets):
        self.decidebutton = []
        self.chow_set_decision= -1
        for i, chowset in enumerate(chowsets):
            chowset = sorted(chowset)
            
            image1 = Image.open(self.img_path[chowset[0]])
            image2 = Image.open(self.img_path[chowset[1]])
            image3 = Image.open(self.img_path[chowset[2]])

            # Combine images
            combined_image = Image.new("RGB", (108, 50))
            combined_image.paste(image1, (0, 0))
            combined_image.paste(image2, (36, 0))
            combined_image.paste(image3, (72, 0))

            photo = ImageTk.PhotoImage(combined_image)

            button = Button(self, image = photo, compound="center")
            button.config(command=lambda n=i: self.chow_set(n))
            button.image = photo
            self.decidebutton.append(button)
            self.canvas.create_window(windowDims[0]-200-108*i, windowDims[1]-80, window=button)
        while self.chow_set_decision == -1:
            if self.chow_set_decision != -1:
                return self.chow_set_decision

    def update_tile_button(self):
        deck = self.game.get_players()[self.player_num].get_deck()
        deck_tiles = deck.get_deck_tiles()
        showed_tiles = deck.get_showed_tiles()
        num_of_deck_tiles = len(deck_tiles)
        num_of_showed_tiles = len(showed_tiles)

        if num_of_showed_tiles != 0 and len(self.showed_tiles_image) != num_of_showed_tiles*3:
            tile1, tile2, tile3 = showed_tiles[-1]
            three_tiles = [tile1, tile2, tile3]
            three_tiles = sorted(three_tiles, key=lambda x: x.get_cal_value())

            for i in range(3):
                self.buttons[0].destroy()
                self.buttons.pop(0)

            for i, tile in enumerate(three_tiles):
                num = tile.get_cal_value()
                image = Image.open(self.img_path[num])
                photo = ImageTk.PhotoImage(image)
                self.showed_tiles_image.append(photo)
                self.canvas.create_image((i+num_of_showed_tiles*3)*40+50, windowDims[1]-60, anchor=tk.NW, image=self.showed_tiles_image[-1])
            
        #if no new tile
        elif num_of_deck_tiles %3 == 1:

            for i, tile in enumerate(deck_tiles):
                num = tile.get_cal_value()
                image = Image.open(self.img_path[num])
                photo = ImageTk.PhotoImage(image)
                button = self.buttons[i]
                button.config(command= lambda n=num, b=button : self.click(n, b), image=photo)
                button.image = photo
                self.buttons[i] = button

        #if drew a new tile
        else:
            print("extra tile")
            for i, tile in enumerate(deck_tiles):

                num = tile.get_cal_value()
                image = Image.open(self.img_path[num])
                photo = ImageTk.PhotoImage(image)
                
                if i < num_of_deck_tiles-1:
                    button = self.buttons[i]
                    button.config(command= lambda n=num, b=button : self.click(n, b), image=photo)
                    button.image = photo
                    self.buttons[i] = button
                else:
                    self.discard = True
                    button = Button(self, image=photo, command=lambda n=num, b=button: self.click(n,b), compound="center")
                    button.config(command=lambda n=num, b=button: self.click(n, b))
                    button.image = photo
                    self.canvas.create_window(13*40+200, windowDims[1]-40, window=button)
                    self.buttons.append(button)

    def update_remaining(self):
        if len(self.game.get_tilesoutside()) < len(self.outside_tiles):
            self.outside_tiles_image.pop()
            self.canvas.delete(self.outside_tiles[-1])
            self.outside_tiles.pop()

            left = (self.player_num +3)%4
            opp = (self.player_num +2)%4
            right = (self.player_num +1)%4

            print(f"left: {left}, opp: {opp}, right: {right}")

            left_shown = self.game.get_players()[left].get_deck().get_showed_tiles()
            opp_shown = self.game.get_players()[opp].get_deck().get_showed_tiles()
            right_shown = self.game.get_players()[right].get_deck().get_showed_tiles()

            player_shown_list = [left_shown, opp_shown, right_shown]
            shown_list = [self.left_player, self.opp_player, self.right_player]

            for i, player_shown_deck in enumerate(player_shown_list):
                shown = shown_list[i]
                print("check")
                if len(player_shown_deck) != 0:
                    print("hi")
                    for j, tile_set in enumerate(player_shown_deck):
                        for k, tile in enumerate(tile_set):
                            num = tile.get_cal_value()
                            image = Image.open(self.img_path[num])
                            if i == 2:
                                photo = ImageTk.PhotoImage(self.rotate_image(image))
                            elif i == 1:
                                photo = ImageTk.PhotoImage(self.rotate_image_opp(image))
                            else:
                                photo = ImageTk.PhotoImage(self.rotate_image_rev(image))
                                
                            self.others_showed_tiles_image.append(photo)
                            tile_to_change = shown[3*j+k]
                            self.canvas.itemconfig(tile_to_change, image = self.others_showed_tiles_image[-1])

        elif len(self.game.get_tilesoutside()) != 0:
            discarded = self.game.get_tilesoutside()[-1]
            num = discarded.get_cal_value()
            image = Image.open(self.img_path[num])
            self.outside_tiles_image.append(ImageTk.PhotoImage(image))
            index = len(self.outside_tiles_image)-1
            if index > 61:
                index +=3
            self.outside_tiles.append(self.canvas.create_image(100+40*(index%18), 100+50*(index//18), anchor=tk.NW, image=self.outside_tiles_image[-1]))
        #change the label to show remaining tiles
        self.canvas.itemconfig(self.remain_tiles, text= str(len(self.game.get_tilesremain())))

    #normal discard tile
        
    def click(self, num, button):
        if not self.discard:
            pass
        else:
            deck = self.game.get_players()[self.player_num].get_deck()
            deck.discard_tile(num)
            #send game back to server
            self.discard = False
            self.buttons[-1].destroy()
            self.buttons.pop()
            self.update_tile_button()
            self.network.onlysend("discard")
            self.network.onlysend(self.game)

    def pung(self):
        self.pung_decision = True
        for button in self.decidebutton:
            button.destroy()

    def chow(self):
        self.chow_decision = True
        for button in self.decidebutton:
            button.destroy()

    def chow_set(self, num):
        self.chow_set_decision = num
        for button in self.decidebutton:
            button.destroy()

        

    def skip(self):
        self.pung_decision = False
        for button in self.decidebutton:
            button.destroy()


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

    def update_game():
        global mahjong_game
        global n
        update = True

        n.onlysend("draw")
        game = n.receive_object()
        round_count = n.receive_string()
        print(f"next round :{round_count}")
        player_num = mahjong_game.get_player_num()
        if player_num == 0:
            player = game.get_players()[player_num] 
            player.get_deck().draw_tile()

        while update:
            update = False

            #draw and discard
            if player_num == int(round_count):
                mahjong_game.update_game(game) 
                mahjong_game.update_tile_button() #send discard to server
            
            if n.receive_string() == "pung check":
                game = n.receive_object()
                mahjong_game.update_game(game)
                mahjong_game.update_remaining()
                pung = n.receive_string()
                
                if pung != "no pung":
                    print("pung")
                    count_temp = pung

                    if player_num == int(count_temp):
                        n.onlysend("pung")
                        decision = mahjong_game.decide_pung()
                        n.onlysend(str(decision))

                    while 1:
                        data = n.receive_string()
                        if data == "have pung":
                            print("finish pung check")
                            game = n.send("request")
                            mahjong_game.update_game(game)
                            mahjong_game.update_tile_button()
                            mahjong_game.update_remaining()
                            update = True
                            break
                        elif data == "didn't have pung":
                            break
                    
                elif pung == "no pung":
                    print("no pung")

            if update == False: 

                if player_num == (int(round_count)+1)%4:
                    n.onlysend("check chow")
                    chow = n.receive_string()
                    if chow != "no chow":
                        print("chow")
                        num_of_chow = int(chow)
                        decision = mahjong_game.decide_chow()
                        n.onlysend(str(decision))
                        if decision:
                            if num_of_chow > 1:
                                chowsets = []
                                for i in range(num_of_chow):
                                    chowset = n.receive_string()
                                    chowset = list(map(int, chowset.split(',')))
                                    chowsets.append(chowset)
                                set_decision = mahjong_game.decide_chow_set(chowsets)
                                n.onlysend(str(set_decision))
                            update = True
                        else:
                            print("no chow")
                    else:
                        print("no chow")

                while 1:
                    data = n.receive_string()
                    print(f"505: {data}")
                    if data == "chow done 1":
                        print("finish chow check 2")
                        game = n.send("request")
                        mahjong_game.update_game(game)
                        mahjong_game.update_tile_button()
                        mahjong_game.update_remaining()
                        break
                    elif data == "chow done 2":
                        break
            
            n.onlysend("draw")
            game = n.receive_object()
            round_count = n.receive_string()
            print(f"next round :{round_count}")
            player_num = mahjong_game.get_player_num()

            if player_num == int(round_count) and update != True:
                player = game.get_players()[player_num] 
                player.get_deck().draw_tile()
                
            update = True


    def joinToRoom():
        global joining_page
        global n
        global room_page
        global name

        name = joining_page.name_var.get()
        if name == '':
            print("invalid input")
        else:
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
        listen_thread2 =  threading.Thread(target=update_game, args=())
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
