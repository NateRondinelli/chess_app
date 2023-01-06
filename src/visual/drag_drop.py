# https://www.reddit.com/r/learnpython/comments/nnn27l/how_to_make_a_tkinter_canvas_drag_and_drop/
# TicklesMcFancy
import tkinter as tk


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=500, height=300)
        self.canvas.grid(row=0,column=0)
        self._cLabel = tk.Label(self.canvas, text='Hello World', bg='blue')
        self.id_cLabel = self.canvas.create_window(100,100, window=self._cLabel,    tags="motion_bound")
        self.update()
        self._cLabel.bind("<B1-Motion>", self.relocate)

    def relocate(self, event):
        print(self.canvas.winfo_pointerxy())
        x0,y0 = self.canvas.winfo_pointerxy()
        x0 -= self.canvas.winfo_rootx()
        y0 -= self.canvas.winfo_rooty()
        self.canvas.coords(self.id_cLabel,x0,y0)


if __name__ == "__main__":
    main = Main()
    main.mainloop()