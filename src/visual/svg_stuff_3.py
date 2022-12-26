# https://stackoverflow.com/questions/55943631/putting-svg-images-into-tkinter-frame
# User Andoo (OP) on Dec 15, 2020 at 0:45
import cairosvg

import io
import tkinter as tk
from PIL import Image,ImageTk

# cairosvg.svg2png(url="example.svg", write_to="output.png")

main=tk.Tk()

image_data = cairosvg.svg2png(url="example.svg")
image = Image.open(io.BytesIO(image_data))
tk_image = ImageTk.PhotoImage(image)

button=tk.Label(main, image=tk_image)
button.pack(expand=True, fill="both")
main.mainloop()