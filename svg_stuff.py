# https://stackoverflow.com/questions/55943631/putting-svg-images-into-tkinter-frame
# User rizerphe on Mar 31, 2020 at 13:33

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
from tkinter import *

drawing = svg2rlg("safari-pinned-tab.f387b3f2.svg")
renderPM.drawToFile(drawing, "temp.png", fmt="PNG")

tk = Tk()

img = Image.open('temp.png')
pimg = ImageTk.PhotoImage(img)
size = img.size

frame = Canvas(tk, width=size[0], height=size[1])
frame.pack()
frame.create_image(0, 0, anchor='nw', image=pimg)

tk.mainloop()
