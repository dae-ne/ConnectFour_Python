import tkinter as tk
from tkinter import font as tkfont
import numpy as np
#from GameExceptions import *

WINDOW_SIZE = (700, 700)
GAME_FIELDS = (6, 7) # (y, x)
PLAYER_FONT_SIZE = 24
GAME_BACKGROUND_COLOR = "white"
GAME_FOREGROUND_COLOR = "black"
GAME_ACTIVE_BUTTON_COLOR = "grey"

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


class InvalidFrameNameException(Error):

    def __init__(self, value):
        super().__init__(value)


class ColumnStackedException(Error):

    def __init__(self, value):
        super().__init__(value)


class GameBoard:

    def __init__(self):
        self._board = np.zeros(GAME_FIELDS)

    def getBoardField(self, x, y):
        return self._board[y][x]

    def setBoardField(self, x, y, value):
        self._board[y][x] = value

    def scan(self, x, y):
        tmpX, tmpY = x, y
        ok = []
        directions = ((1, 0), (0, 1), (1, 1))
        for dir in directions:
            if self._board[tmpY][tmpX] == 1:
                ok.append(tmpY, tmpX)

    def printBoard(self):
        print(self._board)


class Application(tk.Tk):
    '''Główna klasa aplikacji'''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Connect Four")

        self.title_font = tkfont.Font(size=PLAYER_FONT_SIZE, weight="bold", slant="italic")

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

        # Ramkka startowa
        self.showFrame("Game") # TODO: obsługa wyjątku

    # Zmiana ramki
    def showFrame(self, pageName):
        '''Zmiana aktywnej ramki'''
        if not pageName in self.frames:
            raise InvalidFrameNameException("{} frame doesn't exist".format(pageName))
            return

        frame = self.frames[pageName]
        frame.tkraise()


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=GAME_BACKGROUND_COLOR)

        self._gameBoard = GameBoard()

        label = tk.Label(self, text="Player 1", font=self.controller.title_font, anchor="center", bg=GAME_BACKGROUND_COLOR, fg=GAME_FOREGROUND_COLOR)
        label.grid(columnspan=GAME_FIELDS[1], sticky=tk.NSEW)
        self._fields = [[] for _ in range(GAME_FIELDS[1])]

        for y in range(GAME_FIELDS[0]):
            for x in range(GAME_FIELDS[1]):
                self._fields[y].append(tk.Canvas(self, width=100, height=100, cursor="hand1", bg=GAME_FOREGROUND_COLOR))
                self._fields[y][x].configure(highlightbackground=GAME_BACKGROUND_COLOR)
                self._fields[y][x].grid(row=y+1, column=x, padx=1)
                self._fields[y][x].bind("<Enter>", lambda event, arg=x: self.field_Enter(event, arg))
                self._fields[y][x].bind("<Leave>", lambda event, arg=x: self.field_Leave(event, arg))
                self._fields[y][x].bind("<Button-1>", lambda event, arg=x: self.field_Button1Click(event, arg))
                
        controller.resizable(False, False) # zablokowanie możliwości zmiany rozmiaru okna

    ##################### eventy ##################################

    def field_Enter(self, event, column):
        for y in range(GAME_FIELDS[0]):
            self._fields[y][column].configure(bg=GAME_ACTIVE_BUTTON_COLOR)
        # TODO: wyróżnienie najniższego wolnego pola

    def field_Leave(self, event, column):
        for y in range(GAME_FIELDS[0]):
            self._fields[y][column].configure(bg=GAME_FOREGROUND_COLOR)

    def field_Button1Click(self, event, column):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for i in range(GAME_FIELDS[0] - 1, -1, -1):
            if self._gameBoard.getBoardField(column, i) == 0:
                self._gameBoard.setBoardField(column, i, 1)
                self._fields[i][column].create_oval(15, 15, 85, 85, fill=GAME_BACKGROUND_COLOR, width=0)
                break
        else:
            #raise ColumnStackedException("This column is already filled")
            self._gameBoard.printBoard()


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
