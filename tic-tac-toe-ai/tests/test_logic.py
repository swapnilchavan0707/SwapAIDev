import pytest
from src.game_logic import TicTacToeLogic

def test_initial_board():
    logic = TicTacToeLogic()
    assert all(cell == ' ' for row in logic.board for cell in row)
    assert logic.current_player == 'X'

def test_win_horizontal():
    logic = TicTacToeLogic()
    # Mock a horizontal win for X
    logic.board = [
        ['X', 'X', 'X'],
        ['O', ' ', 'O'],
        [' ', ' ', ' ']
    ]
    assert logic.check_winner() == 'X'

def test_win_vertical():
    logic = TicTacToeLogic()
    # Mock a vertical win for O
    logic.board = [
        ['O', 'X', ' '],
        ['O', 'X', ' '],
        ['O', ' ', ' ']
    ]
    assert logic.check_winner() == 'O'

def test_tie_condition():
    logic = TicTacToeLogic()
    # Mock a full board with no winner
    logic.board = [
        ['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X']
    ]
    assert logic.check_winner() == 'Tie'
