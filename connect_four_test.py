"""Test modułu connect_four."""

import unittest

import connect_four as cf
from connect_four import np


class ApplicationTest(unittest.TestCase):

    def setUp(self):
        self.app = cf.Application()

    def test_show_frame(self):
        with self.assertRaises(cf.InvalidFrameNameException):
            self.app.show_frame("nieznana ramka")


class GameBoardTest(unittest.TestCase):

    def setUp(self):
        self.game_board = cf.GameBoard()

    def test_scan_empty_board(self):
        self.assertFalse(self.game_board.scan(3, 5, 1))

    def test_horizontal_scan(self):
        self.game_board.board = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 0, 0],
            ])

        self.assertTrue(self.game_board.scan(3, 5, 1))

    def test_vertical_scan(self):
        self.game_board.board = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
            ])

        self.assertTrue(self.game_board.scan(3, 5, 1))

    def test_diagonal1_scan(self):
        self.game_board.board = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
            ])

        self.assertTrue(self.game_board.scan(3, 5, 1))

    def test_diagonal2_scan(self):
        self.game_board.board = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
            ])

        self.assertTrue(self.game_board.scan(3, 5, 1))

    def test_more_than_4_scan(self):
        self.game_board.board = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1],
            ])

        self.assertTrue(self.game_board.scan(3, 5, 1))


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = cf.Player("gracz1", 1, cf.PLAYER1_COLOR)

    def test_name_init_val(self):
        self.assertEqual(self.player.name, "gracz1")

    def test_number_init_val(self):
        self.assertEqual(self.player.number, 1)

    def test_color_init_val(self):
        self.assertEqual(self.player.color, cf.PLAYER1_COLOR)


class AITest(unittest.TestCase):

    def setUp(self):
        self.ai = cf.AI("name", 3, 1, cf.PLAYER2_COLOR)

    def test_winnig_move(self):
        board = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0],
            ])

        col, minimax_score = self.ai.minimax(
            board, cf.MINIMAX_DEPTH, -np.inf, np.inf, True)

        self.assertEqual(minimax_score, cf.FINAL_SCORE)


class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = cf.Application().show_frame("Game")

    def test_field_button1_click(self):
        self.game.player_or_computer = cf.GAME_WITH_PLAYER
        self.game.field_button1_click(None, 2)
        self.game.field_button1_click(None, 3)
        self.game.field_button1_click(None, 2)
        self.game.field_button1_click(None, 3)

        higher_row = [1, 2]
        higher_row_game = [self.game.game_board.board[4][2],
                           self.game.game_board.board[4][3]]

        self.assertEqual(higher_row_game, higher_row)


if __name__ == '__main__':
    unittest.main()
