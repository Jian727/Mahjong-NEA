import tkinter as tk
from PIL import Image, ImageTk 

# Create the main window
root = tk.Tk()
root.geometry("300x200")

# Load images
image1 = Image.open("img/0.png")
image2 = Image.open("img/1.png")
image3 = Image.open("img/2.png")

# Resize images to fit the button (adjust size as needed)
image1 = image1.resize((36, 50), Image.ANTIALIAS)
image2 = image2.resize((36, 50), Image.ANTIALIAS)
image3 = image3.resize((36, 50), Image.ANTIALIAS)

# Combine images
combined_image = Image.new("RGB", (108, 50))
combined_image.paste(image1, (0, 0))
combined_image.paste(image2, (36, 0))
combined_image.paste(image3, (72, 0))

# Convert combined image to Tkinter PhotoImage
photo = ImageTk.PhotoImage(combined_image)

# Create button with combined image
button = tk.Button(root, image=photo, command=lambda: print("Button Clicked"))
button.image = photo  # Keep a reference to avoid garbage collection
button.pack()

# Start the Tkinter event loop
root.mainloop()
