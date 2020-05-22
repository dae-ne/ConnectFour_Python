import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import numpy as np

BOARD_SIZE = (600, 700) # (y, x)
GAME_FIELDS = (6, 7) # (y, x)
PLAYER_FONT_SIZE = 24
GAME_BACKGROUND_COLOR = "white"
GAME_FOREGROUND_COLOR = "black"
GAME_ACTIVE_BUTTON_COLOR = "grey"
GAME_ACTIVE_BUTTON_COLOR_2 = GAME_BACKGROUND_COLOR
PLAYER1_COLOR = "blue"
PLAYER2_COLOR = "green"
PLAYER1_NAME = "player1"
PLAYER2_NAME = "player2"

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


class MyError(Exception):

    def __init__(self, value):
        self._value = value
        print("There's an error :(")

    def getValue(self):
        return self._value


class InvalidFrameNameException(MyError):

    def __init__(self, value):
        super().__init__(value)


# class ColumnStackedException(MyError):

#     def __init__(self, value):
#         super().__init__(value)


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

        # Ramka startowa
        try:
            self.showFrame("Game")
        except InvalidFrameNameException as e:
            messagebox.showerror("Error!", e.getValue())
            self.destroy()

    # Zmiana ramki
    def showFrame(self, pageName):
        '''Zmiana aktywnej ramki'''
        if not pageName in self.frames:
            raise InvalidFrameNameException("{} frame doesn't exist".format(pageName))
            return

        frame = self.frames[pageName]
        frame.tkraise()


class GameBoard:

    def __init__(self):
        self._board = np.zeros(GAME_FIELDS)

    def getBoardField(self, x, y):
        return self._board[y][x]

    def setBoardField(self, x, y, value):
        self._board[y][x] = value

    def scan(self, x, y, playerNumber):
        ok = []
        for dir in np.array([[1, 0], [0, 1], [1, 1]]):
            ok = []
            for i in range(2):
                point = np.array([y, x])
                if i == 1:
                    point -= dir
                while self._board[point[0]][point[1]] == playerNumber:
                    ok.append([point[0], point[1]])
                    if i == 0:
                        point += dir
                    else:
                        point -= dir
                    if (point[0] < 0 or point[0] >= GAME_FIELDS[0]
                        or point[1] < 0 or point[1] >= GAME_FIELDS[1]):
                        break
                if i == 1 and len(ok) >= 4:
                    return ok
        return None

    def printBoard(self):
        print(self._board)

    
class Player:

    def __init__(self, name, number, color):
        self._name = name
        self._number = number
        self._color = color

    def getName(self):
        return self._name

    def getNumber(self):
        return self._number

    def getColor(self):
        return self._color


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=GAME_BACKGROUND_COLOR)

        self._gameBoard = GameBoard()
        self._players = (Player(PLAYER1_NAME, 1, PLAYER1_COLOR),
            Player(PLAYER2_NAME, 2, PLAYER2_COLOR))
        self._currentPlayer = 0 # zmienna przyjmuje wartość 0 lub 1

        self._label = tk.Label(self, text=PLAYER1_NAME, font=self.controller.title_font,
            anchor="center", bg=GAME_BACKGROUND_COLOR, fg=GAME_FOREGROUND_COLOR)
        self._label.grid(columnspan=GAME_FIELDS[1], sticky=tk.NSEW)
        self._fields = [[] for _ in range(GAME_FIELDS[1])]

        boardHeight = BOARD_SIZE[0] / GAME_FIELDS[0]
        boardWidth = BOARD_SIZE[1] / GAME_FIELDS[1]

        for y in range(GAME_FIELDS[0]):
            for x in range(GAME_FIELDS[1]):
                self._fields[y].append(tk.Canvas(self, width=boardWidth,
                    height=boardHeight, cursor="hand1", bg=GAME_FOREGROUND_COLOR))
                self._fields[y][x].configure(highlightbackground=GAME_BACKGROUND_COLOR)
                self._fields[y][x].grid(row=y+1, column=x, padx=1)
                self._fields[y][x].bind("<Enter>", lambda event,
                    arg=x: self.field_Enter(event, arg))
                self._fields[y][x].bind("<Leave>", lambda event,
                    arg=x: self.field_Leave(event, arg))
                self._fields[y][x].bind("<Button-1>", lambda event,
                    arg=x: self.field_Button1Click(event, arg))
                
        controller.resizable(False, False) # zablokowanie możliwości zmiany rozmiaru okna

    def update(self):
        self._label.configure(text=self._players[self._currentPlayer].getName())

    def changePlayer(self):
        if self._currentPlayer == 0:
            self._currentPlayer = 1
        else:
            self._currentPlayer = 0

    ##################### eventy ##################################

    def field_Enter(self, event, column):
        isHighlighted = False
        for y in range(GAME_FIELDS[0] - 1, -1, -1):
            if self._gameBoard.getBoardField(column, y) == 0 and isHighlighted == False:
                self._fields[y][column].configure(bg=GAME_ACTIVE_BUTTON_COLOR_2)
                isHighlighted = True
            else:
                self._fields[y][column].configure(bg=GAME_ACTIVE_BUTTON_COLOR)

    def field_Leave(self, event, column):
        for y in range(GAME_FIELDS[0]):
            self._fields[y][column].configure(bg=GAME_FOREGROUND_COLOR)

    def field_Button1Click(self, event, column):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for i in range(GAME_FIELDS[0] - 1, -1, -1):
            if self._gameBoard.getBoardField(column, i) == 0:
                self._gameBoard.setBoardField(column, i, self._players[self._currentPlayer].getNumber())
                self._fields[i][column].create_oval(15, 15, 85, 85,
                    fill=self._players[self._currentPlayer].getColor(), width=0)
                self.field_Enter(None, column)
                print(self._gameBoard.scan(column, i, self._players[self._currentPlayer].getNumber()))
                self.changePlayer()
                self.update()
                break
        else:
            messagebox.showinfo(None, "This column is already filled up")
            #self._gameBoard.printBoard()


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
