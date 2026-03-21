import math


class TicTacToeAI:
    def __init__(self, ai_player='O', human_player='X'):
        self.ai_player = ai_player
        self.human_player = human_player

    def get_best_move(self, logic):
        best_score = -math.inf
        move = None
        for r in range(3):
            for c in range(3):
                if logic.board[r][c] == ' ':
                    logic.board[r][c] = self.ai_player
                    score = self.minimax(logic.board, 0, False)
                    logic.board[r][c] = ' '
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        return move

    def minimax(self, board, depth, is_maximizing):
        from src.game_logic import TicTacToeLogic
        logic_check = TicTacToeLogic()
        res = logic_check.check_winner(board)

        if res == self.ai_player: return 1
        if res == self.human_player: return -1
        if res == 'Tie': return 0

        if is_maximizing:
            best_score = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = self.ai_player
                        score = self.minimax(board, depth + 1, False)
                        board[r][c] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = self.human_player
                        score = self.minimax(board, depth + 1, True)
                        board[r][c] = ' '
                        best_score = min(score, best_score)
            return best_score
