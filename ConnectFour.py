import tkinter as tk
from tkinter import font as tkfont
#from GameExceptions import *

# TODO:
# - zamienić część zmiennych na stałe globalne
# - stworzyć stałe globalne m.in. do rozmiaru czcionki, pól na planszy itp
# - wstawianie żetonów w odpowiednie miejsce
# - po najechaniu na kolumnę w planszy ma zostać wyświetlone na inny kolor
#   pole, w które ma być wstawiony żeton (najniższe wolne)
# - stworzyć klasę "GameBoard" z dwuwymiarową tablicą wartości planszy
#   oraz metodami do jej skanowania. Tablica jako numpy.array, żeby
#   łatwiej było ją skanować
# - optymalizacja skanowania bez zbyt dużej ilości pętli. Jedna dobrze
#   skonstuowana pętla lub skanowanie rekurencyjne (sprawdzę które lepsze)
# - podział na dwóch graczy (teraz dla ułatwienia jest tylko jeden)
# - uzupełnić ramki: "GameInfo" i "EndOfGame"
# - w czasie gry, w górnej części okna ma pojawiać się przycisk
#   do uruchomienia ramki z informacją o zasadach gry i sterowaniu
# - ramka po zakończeniu gry z informacją kto wygrał. Możliwość
#   rozpoczęcia nowej gry lub zamknięcia programu
# - dokumentacja
# - usunięcie okna konsoli
# - testy na klasie GameBoard
# - dopisanie nowych pomysłów

class Error(Exception):

    def __init__(self, value):
        self._value = value
        print("There's an error :(")

    def getValue(self):
        return self._value


class InvalidFrameNameError(Error):

    def __init__(self, value):
        super().__init__(value)

    def getValue(self):
        return self._value


class GameBoard:
    def scan(self):
        pass


class Application(tk.Tk):
    '''Główna klasa aplikacji'''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Connect Four")

        self.title_font = tkfont.Font(size=24, weight="bold", slant="italic")

        # Kontener, w którym umieszczane będą ramki aplikacji
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Inicjowanie ramek
        self.frames = {F.__name__: F(parent=container, controller=self)
            for F in (Game, GameInfo, EndOfGame)}
        for frame in self.frames:
            self.frames[frame].grid(row=0, column=0, sticky="nsew")

        # Ramka startowa
        self.showFrame("Game") # TODO: obsługa wyjątku

    # Zmiana ramki
    def showFrame(self, pageName):
        '''Zmiana aktywnej ramki'''
        if not pageName in self.frames:
            raise InvalidFrameNameError("{} frame doesn't exist".format(pageName))
            return

        frame = self.frames[pageName]
        frame.tkraise()


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")

        tiles = (7,6) # To zmienie na stałą globalną

        label = tk.Label(self, text="Player 1", font=self.controller.title_font, anchor="center", bg="white")
        label.grid(columnspan=tiles[0], sticky=tk.NSEW)
        self._fields = [[] for _ in range(tiles[1])]

        for y in range(tiles[1]):
            for x in range(tiles[0]):
                self._fields[y].append(tk.Canvas(self, width=100, height=100, cursor="hand1", bg="black"))
                self._fields[y][x].grid(row=y+1, column=x, padx=1)
                self._fields[y][x].bind("<Enter>", lambda event, arg=x: self.field_Enter(event, arg))
                self._fields[y][x].bind("<Leave>", lambda event, arg=x: self.field_Leave(event, arg))
                self._fields[y][x].bind("<Button-1>", lambda event, arg=x: self.field_Button1Click(event, arg))
                
        controller.resizable(False, False) # zablokowanie możliwości zmiany rozmiaru okna

    ##################### eventy ##################################

    def field_Enter(self, event, column):
        tiles = (7,6) # To zmienie na stałą globalną
        for y in range(tiles[1]):
            self._fields[y][column].configure(bg="gray")
        # TODO: wyróżnienie najniższego wolnego pola

    def field_Leave(self, event, column):
        tiles = (7,6) # To zmienie na stałą globalną
        for y in range(tiles[1]):
            self._fields[y][column].configure(bg="black")

    def field_Button1Click(self, event, column):
        tiles = (7,6) # To zmienie na stałą globalną
        self._fields[0][column].create_oval(15, 15, 85, 85, outline="white", fill="white", width=20)
        # TODO: wstawianie żetonów w odpowiednie miejsca


class GameInfo(tk.Frame):
    # Ramka, w której wyświetlają się informacje
    # o zasadach gry i sposobie sterowania
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class EndOfGame(tk.Frame):
    # Odpala się po zakończeniu gry
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = Application() # inicjalizacja
    app.mainloop() # główna pętla programu
