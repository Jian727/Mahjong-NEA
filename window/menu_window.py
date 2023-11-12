import tkinter as tk
from PIL import Image, ImageTk

def on_click_play():
    """Open the second window when the button is clicked."""
    second_window = tk.Toplevel(root)
    second_window.title("Second Window")
    second_window.geometry("300x200")
    tk.Label(second_window, text="You have clicked the 'Navigate' button.").pack()

def on_click_quit():
    """Close the window."""
    root.quit()

windowDims = (960, 540)

root = tk.Tk()
root.geometry(f"{windowDims[0]}x{windowDims[1]}")
root.wm_title("Mahjong: Menu")

canvas = tk.Canvas(root, width=windowDims[0], height=windowDims[1], highlightthickness=0)
canvas.pack()

image = Image.open("window/background_img.png")
image = image.resize((windowDims[0], windowDims[1]), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
canvas.create_image(windowDims[0]//2, windowDims[1]//2, image=photo)

canvas.create_text(windowDims[0]//2,  windowDims[1]//2-100, text="Mahjong!", font="calibri 60 bold", fill="white")

button_play = tk.Button(root, text="Play", font=("calibri", 30), command=on_click_play)
button_play.place(x=windowDims[0]//2-75, y=windowDims[1]//2-25, width=150, height=50)

button_quit = tk.Button(root, text="Quit", font=("calibri", 30), command=on_click_quit)
button_quit.place(x=windowDims[0]//2-75, y=windowDims[1]//2+50, width=150, height=50)

root.mainloop()