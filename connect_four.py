import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import numpy as np
import random


BOARD_SIZE = (600, 700)  # (y, x)
GAME_FIELDS = (6, 7)  # (y, x)
PLAYER_FONT_SIZE = 32
MENU_FONT_SIZE = 52
GAME_BACKGROUND_COLOR = "white"
GAME_FOREGROUND_COLOR = "black"
GAME_ACTIVE_BUTTON_COLOR = "grey"
GAME_ACTIVE_BUTTON_COLOR_2 = GAME_BACKGROUND_COLOR
PLAYER1_COLOR = "blue"
PLAYER2_COLOR = "green"
MENU_BACKGROUND_COLOR = "black"
MENU_BUTTON_COLOR = "grey"
PLAYER1_NAME = "gracz1"
PLAYER2_NAME = "gracz2"
AI_NAME = "komputer"
EMPTY_FILED_NO = 0
PLAYER1_FILED_NO = 1
PLAYER2_FILED_NO = 2
COMPUTER_FIELD_NO = 3
MINIMAX_DEPTH = 5
DIRECTIONS = np.array([[1, 0], [0, 1], [1, 1], [-1, 1]])
FINAL_SCORE = 99999
MIN_WAIT_TIME = 50
MAX_WAIT_TIME = 3000
WINNING_LENGTH = 4
GAME_WITH_PLAYER = 0
GAME_WITH_COMPUTER = 1
PLAYER1_TURN = 0
PLAYER2_TURN = 1
TOKEN_POSITION = (15, 15, 85, 85)


class MyError(Exception):
    """Główna klasa wyjątków dla tego modułu."""

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value


class InvalidFrameNameException(MyError):
    """Wyjątek oznaczający nieprawidłową nazwę ramki."""

    def __init__(self, value):
        super().__init__(value)


class Application(tk.Tk):
    """Główna klasa aplikacji."""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Connect Four")

        self.resizable(False, False)

        # Kontener, w którym umieszczane będą ramki aplikacji
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Inicjowanie ramek
        self.frames = {F.__name__: F(parent=container, controller=self)
                       for F in (Game, MainMenu)}
        for frame in self.frames:
            self.frames[frame].grid(row=0, column=0, sticky="nsew")

        # Ramka startowa
        try:
            self.show_frame("MainMenu")
        except InvalidFrameNameException as e:
            messagebox.showerror("Error!", e)
            self.destroy()

    # Zmiana ramki
    def show_frame(self, page_name):
        """Zmiana aktywnej ramki."""
        if page_name not in self.frames:
            raise InvalidFrameNameException(
                "Ramka {} nie istnieje".format(page_name))
            return

        frame = self.frames[page_name]
        frame.tkraise()
        return frame


class IScanable:
    """Skanowanie planszy w poszukiwaniu czterech żetonów w rzędzie."""

    def scan(self, board, x, y, player_number):
        """Zwraca prawdę w przypadku wygranej."""
        for dir in DIRECTIONS:
            ok = 0
            for i in range(2):
                point = np.array([y, x])
                if i == 1:
                    ok -= 1
                while board[point[0]][point[1]] == player_number:
                    ok += 1
                    if ok >= WINNING_LENGTH:
                        return True
                    if i == 0:
                        point += dir
                    else:
                        point -= dir
                    if (point[0] < 0 or point[0] >= GAME_FIELDS[0] or
                            point[1] < 0 or point[1] >= GAME_FIELDS[1]):
                        break
        return False


class GameBoard(IScanable):
    """Klasa planszy gry."""

    def __init__(self):
        self.board = np.zeros(GAME_FIELDS)

    def scan(self, x, y, player_number):
        """Skanowanie planszy."""
        return super().scan(self.board, x, y, player_number)

    def clear_board(self):
        """Czyszczenie planszy."""
        self.board = np.zeros(GAME_FIELDS)


class Player:
    """Klasa gracza."""

    def __init__(self, name, number, color):
        self.name = name
        self.number = number
        self.color = color


class AI(IScanable, Player):
    """Klasa implementująca grę z komputerem."""

    def __init__(self, name, number, opponent_number, color):
        super().__init__(name, number, color)
        self._opponent_number = opponent_number

    def get_next_open_row(self, board, col):
        """Funkcja zwracająca indeks najniższego wolnego pola w kolumnie."""
        for row in range(GAME_FIELDS[0] - 1, -1, -1):
            if board[row][col] == 0:
                return row

    def evaluate_window(self, four_list, player_number):
        """Zwraca wynik dla określonej części planszy."""
        score = 0
        opponent_number = self._opponent_number

        if player_number == self._opponent_number:
            opponent_number = self.number
        if four_list.count(player_number) == 4:
            score += 100
        elif (four_list.count(player_number) == 3 and
              four_list.count(EMPTY_FILED_NO) == 1):
            score += 5
        elif (four_list.count(player_number) == 2 and
              four_list.count(EMPTY_FILED_NO) == 2):
            score += 2
        if (four_list.count(opponent_number) == 3 and
                four_list.count(EMPTY_FILED_NO) == 1):
            score -= 4

        return score

    def score_position(self, board, player_number):
        """Zwraca wynik dla całej planszy."""
        score = 0

        center_array = [int(i) for i in list(board[:, GAME_FIELDS[1] // 2])]
        center_count = center_array.count(player_number)
        score += center_count * 3

        for r in range(GAME_FIELDS[0]):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(GAME_FIELDS[1]-(WINNING_LENGTH-1)):
                four_list = row_array[c:c+WINNING_LENGTH]
                score += self.evaluate_window(four_list, player_number)

        for c in range(GAME_FIELDS[1]):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(GAME_FIELDS[0]-(WINNING_LENGTH-1)):
                four_list = col_array[r:r+WINNING_LENGTH]
                score += self.evaluate_window(four_list, player_number)

        for r in range(GAME_FIELDS[0]-(WINNING_LENGTH-1)):
            for c in range(GAME_FIELDS[1]-(WINNING_LENGTH-1)):
                four_list = [board[r+i][c+i] for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(four_list, player_number)

        for r in range(GAME_FIELDS[0]-(WINNING_LENGTH-1)):
            for c in range(GAME_FIELDS[1]-(WINNING_LENGTH-1)):
                four_list = [board[r+(WINNING_LENGTH-1)-i][c+i]
                             for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(four_list, player_number)

        return score

    def minimax(self, board, depth, alpha, beta,
                maximizing, prev_col=0, prev_row=0):
        """Implementacja algorytmu minimax."""
        valid_locations = []
        for col in range(GAME_FIELDS[1]):
            if board[0][col] == 0:
                valid_locations.append(col)

        if depth == 0:
            return (None, self.score_position(board, self.number))
        elif self.scan(board, prev_col, prev_row,
                       self.number) and not maximizing:
            return (None, FINAL_SCORE)
        elif self.scan(board, prev_col, prev_row,
                       self._opponent_number) and maximizing:
            return (None, 0)
        elif len(valid_locations) == 0:
            return (None, 0)

        if maximizing:
            value = -np.inf
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                board_copy = board.copy()
                board_copy[row][col] = self.number
                new_score = self.minimax(board_copy, depth-1, alpha, beta,
                                         False, col, row)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            value = np.inf
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                board_copy = board.copy()
                board_copy[row][col] = self._opponent_number
                new_score = self.minimax(board_copy, depth-1, alpha, beta,
                                         True, col, row)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break

            return column, value


class Game(tk.Frame):
    """Główna klasa gry."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=GAME_BACKGROUND_COLOR)

        self.current_player = PLAYER1_TURN  # przyjmuje wartość 0 lub 1
        self.player_or_computer = GAME_WITH_COMPUTER

        self._game_board = GameBoard()
        self._players = (Player(PLAYER1_NAME, PLAYER1_FILED_NO, PLAYER1_COLOR),
                         Player(PLAYER2_NAME, PLAYER2_FILED_NO, PLAYER2_COLOR))
        self._computer = AI(AI_NAME, COMPUTER_FIELD_NO,
                            PLAYER1_FILED_NO, PLAYER2_COLOR)

        player_name_font = tkfont.Font(size=PLAYER_FONT_SIZE, weight="bold",
                                       slant="italic")

        self._label = tk.Label(self, text=PLAYER1_NAME, font=player_name_font,
                               anchor="center", bg=GAME_BACKGROUND_COLOR,
                               fg=GAME_FOREGROUND_COLOR)
        self._label.grid(columnspan=GAME_FIELDS[1], sticky=tk.NSEW)
        self._fields = [[] for _ in range(GAME_FIELDS[1])]

        board_height = BOARD_SIZE[0] / GAME_FIELDS[0]
        board_width = BOARD_SIZE[1] / GAME_FIELDS[1]

        for y in range(GAME_FIELDS[0]):
            for x in range(GAME_FIELDS[1]):
                self._fields[y].append(tk.Canvas(self, width=board_width,
                                       height=board_height, cursor="hand1",
                                       bg=GAME_FOREGROUND_COLOR))
                self._fields[y][x].configure(
                    highlightbackground=GAME_BACKGROUND_COLOR)
                self._fields[y][x].grid(row=y+1, column=x, padx=1)
                self._fields[y][x].bind("<Enter>", lambda event,
                                        arg=x: self.field_enter(event, arg))
                self._fields[y][x].bind("<Leave>", lambda event,
                                        arg=x: self.field_leave(event, arg))
                self._fields[y][x].bind("<Button-1>", lambda event,
                                        arg=x: self.field_button1_click(
                                            event, arg))

    def update(self):
        """Aktualizacja nazwy gracza."""
        if self.player_or_computer == GAME_WITH_PLAYER:
            self._label.configure(
                text=self._players[self.current_player].name)

        elif self.current_player == PLAYER2_TURN:
            self._label.configure(text=self._computer.name)

        elif self.current_player == PLAYER1_TURN:
            self._label.configure(
                text=self._players[self.current_player].name)

    def change_player(self):
        """Zmiana tury."""
        if self.current_player == PLAYER1_TURN:
            self.current_player = PLAYER2_TURN
        else:
            self.current_player = PLAYER1_TURN

    def computer_move(self):
        """Ruch komputera."""
        row = 0
        col, minimax_score = self._computer.minimax(
            self._game_board.board, MINIMAX_DEPTH, -np.inf, np.inf, True)

        for i in range(GAME_FIELDS[0] - 1, -1, -1):
            if self._game_board.board[i][col] == 0:
                self._game_board.board[i][col] = self._computer.number
                self._fields[i][col].create_oval(
                    *TOKEN_POSITION, fill=self._computer.color, width=0)
                row = i
                break
        else:
            messagebox.showinfo(None, "Koniec gry")
            try:
                self.controller.show_frame("MainMenu")
            except InvalidFrameNameException as e:
                messagebox.showerror("Error!", e)
                self.controller.destroy()
        if minimax_score == FINAL_SCORE:
            if (self._game_board.scan(col, row, 3)):
                messagebox.showinfo(None, "Komputer wygrał")
                try:
                    self.controller.show_frame("MainMenu")
                except InvalidFrameNameException as e:
                    messagebox.showerror("Error!", e)
                    self.controller.destroy()

        self.change_player()
        self.update()

    def clear_board(self):
        """Czyszczenie planszy."""
        self._game_board.clear_board()

        for y in range(GAME_FIELDS[0]):
            for x in range(GAME_FIELDS[1]):
                self._fields[y][x].delete("all")

    def field_enter(self, event, column):
        """Najechanie kursorem myszy na kolumnę planszy."""
        isHighlighted = False

        for y in range(GAME_FIELDS[0] - 1, -1, -1):
            if (self._game_board.board[y][column] == 0 and
                    isHighlighted is False):
                self._fields[y][column].configure(
                    bg=GAME_ACTIVE_BUTTON_COLOR_2)
                isHighlighted = True
            else:
                self._fields[y][column].configure(bg=GAME_ACTIVE_BUTTON_COLOR)

    def field_leave(self, event, column):
        """Opuszenie kolumny przez kursor."""
        for y in range(GAME_FIELDS[0]):
            self._fields[y][column].configure(bg=GAME_FOREGROUND_COLOR)

    def field_button1_click(self, event, column):
        """Obsługa kliknięcia lewego klawisza myszy."""
        if (self.player_or_computer == GAME_WITH_COMPUTER and
                self.current_player == PLAYER2_TURN):
            messagebox.showwarning(None, "Poczekaj na swoją kolej")
            return

        for i in range(GAME_FIELDS[0] - 1, -1, -1):
            if self._game_board.board[i][column] == 0:
                player_number = self._players[self.current_player].number
                self._game_board.board[i][column] = player_number
                self._fields[i][column].create_oval(
                    *TOKEN_POSITION,
                    fill=self._players[self.current_player].color,
                    width=0)
                self.field_enter(None, column)

                if self._game_board.scan(
                        column, i, player_number):
                    messagebox.showinfo(None, "Koniec gry")

                    try:
                        self.controller.show_frame("MainMenu")
                    except InvalidFrameNameException as e:
                        messagebox.showerror("Error!", e)
                        self.controller.destroy()

                self.change_player()
                self.update()
                break
        else:
            messagebox.showinfo(None, "Ta kolumna jest pełna")

        if self.player_or_computer == GAME_WITH_COMPUTER:
            self.controller.after(random.randint(MIN_WAIT_TIME,
                                  MAX_WAIT_TIME), self.computer_move)


class MainMenu(tk.Frame):
    """Ramka rozpoczęcia gry."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=MENU_BACKGROUND_COLOR)

        font = tkfont.Font(size=MENU_FONT_SIZE)

        komputer_button = tk.Button(self, text="gracz vs komputer",
                                    command=self.play_game_computer,
                                    bg=MENU_BUTTON_COLOR)
        komputer_button.place(relx=0.5, rely=0.33, anchor="center")
        komputer_button['font'] = font

        player_button = tk.Button(self, text="gracz1 vs gracz2",
                                  command=self.play_game_2_players,
                                  bg=MENU_BUTTON_COLOR)
        player_button.place(relx=0.5, rely=0.66, anchor="center")
        player_button['font'] = font

    def play_game_2_players(self):
        """Start gry dwuosobowej."""
        try:
            game = self.controller.show_frame("Game")
        except InvalidFrameNameException as e:
            messagebox.showerror("Error!", e)
            self.destroy()
        game.clear_board()
        game.current_player = PLAYER1_TURN
        game.player_or_computer = GAME_WITH_PLAYER
        game.update()

    def play_game_computer(self):
        """Start gry z komputerem."""
        try:
            game = self.controller.show_frame("Game")
        except InvalidFrameNameException as e:
            messagebox.showerror("Error!", e)
            self.destroy()
        game.clear_board()
        game.current_player = PLAYER1_TURN
        game.player_or_computer = GAME_WITH_COMPUTER

        if random.choice([True, False]):
            game.current_player = PLAYER1_TURN
        else:
            game.current_player = PLAYER2_TURN
            self.controller.after(
                random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME),
                game.computer_move)

        game.update()


def main():
    app = Application()  # inicjalizacja
    app.mainloop()  # główna pętla programu


if __name__ == "__main__":
    main()
