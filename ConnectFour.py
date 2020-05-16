import tkinter as tk
from tkinter import font as tkfont

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Connect Four")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # Kontener, w którym umieszczane będą ramki aplikacji.
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary comprehension
        self.frames = {F.__name__: F(parent=container, controller=self)
            for F in (Game, GameInfo, EndOfGame)}
        for frame in self.frames:
            self.frames[frame].grid(row=0, column=0, sticky="nsew")

        self.showFrame("Game")

    def showFrame(self, page_name):
        '''Zmiana aktywnej ramki'''
        frame = self.frames[page_name]
        frame.tkraise()


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Player 1", font=controller.title_font, cursor="hand1")
        label.pack(side="top", fill="x", pady=10)


class GameInfo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class EndOfGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
