import pytest
from src.game_logic import TicTacToeLogic
from src.ai_engine import TicTacToeAI

def test_ai_blocks_human():
    logic = TicTacToeLogic()
    ai = TicTacToeAI(ai_player='O', human_player='X')
    # Human (X) is about to win on the first row
    logic.board = [
        ['X', 'X', ' '],
        [' ', 'O', ' '],
        [' ', ' ', ' ']
    ]
    # AI (O) should block at (0, 2)
    best_move = ai.get_best_move(logic)
    assert best_move == (0, 2)

def test_ai_takes_winning_move():
    logic = TicTacToeLogic()
    ai = TicTacToeAI(ai_player='O', human_player='X')
    # AI (O) can win on the diagonal
    logic.board = [
        ['O', 'X', 'X'],
        [' ', 'O', ' '],
        [' ', ' ', ' ']
    ]
    # AI (O) should take (2, 2) to win
    best_move = ai.get_best_move(logic)
    assert best_move == (2, 2)
