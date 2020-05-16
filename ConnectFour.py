import pygame

# Ta klasa odpowiedzialna jest za rysowanie planszy,
# oraz przetrzymuje wartości każdego pola
class Board:
    def __init__(self, window):
        self.window = window
        self.rects = []
        self.stateHeight = 100

        # 0 - empty
        # 1 - player 1
        # 2 - player 2
        self.fields = [[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0]]

    def draw(self):
        self.drawLines()

    # Poziome i pionowe linie rysowane na ekranie
    # Oddzielają one od siebie pojedyńcze pola
    def drawLines(self):
        width = self.window.get_rect()[2]
        height = self.window.get_rect()[3]
        x = width / 7

        pygame.draw.line(self.window, (255, 255, 255), (0, 0), (0, height))
        pygame.draw.line(self.window, (255, 255, 255), (width - 1, 0), (width - 1, height))
        pygame.draw.line(self.window, (255, 255, 255), (0, height - 1), (width, height - 1))

        for i in range(6):
            width = width - x
            pygame.draw.line(self.window, (255, 255, 255), (width, self.stateHeight), (width, height + self.stateHeight))

        width = self.window.get_rect()[2]

        for i in range(6):
            height = height - x
            pygame.draw.line(self.window, (255, 255, 255), (0, height), (width, height))

# Główna klasa gry. Łączy powyższe klasy w spójną i przedewszystkim
# działającą całość
class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board(window)
        self.isRunning = True

    # Eventy takie jak ruch myszy, czy też kliknięcie jej klawisza
    def events(self):
        for event in pygame.event.get():
            # Zamknięcie okna
            if event.type == pygame.QUIT:
                self.isRunning = False

    # Rysowanie wszystkich elementów na ekranie
    def draw(self):
        self.window.fill((0, 0, 0, 0))
        self.board.draw()
        pygame.display.flip()

class StateMachine:
    def __init__(self, gameState):
        self._previousState = ""
        self._state = None
        self._gameState = gameState
    def getState(self, state):
        if self._state == None:
            self._state = self._gameState
            self._previousState = "game"
        else:
            newState = state.getState()
            print(newState)
            if newState != self._previousState:
                self._previousState = newState
                if newState == "game":
                    self._state = self._gameState
                elif newState == "endofgame":
                    self._state = EndOfGame()
                else:
                    raise GameExceptions.WrongStateNameException("Wrong state name: {}".format(newState))
        return self._state

# Klasa odpowiedzialna za uruchomienie okna.
# Tutaj znajduje się główna pętla gry.
class Application:
    def __init__(self):
        self.window = None

    def createWindow(self):
        pygame.init()
        pygame.display.set_caption('Connect Four')
        self.window = pygame.display.set_mode((700, 700))

    def run(self):
        self.createWindow()
        game = Game(self.window)

        while game.isRunning:
            game.events()
            game.draw()

#===============================================================

if __name__ == "__main__":
    app = Application()
    app.run()
