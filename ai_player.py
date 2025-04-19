import random
import time

class AIPlayer:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
    
    def make_move(self, board):
        """Make a move based on the current board state."""
        # Add a small delay to make it seem like the AI is thinking
        time.sleep(0.5)
        
        # Find all empty cells
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    empty_cells.append((row, col))
        
        if not empty_cells:
            return None
        
        # Different strategies based on difficulty
        if self.difficulty == 'easy':
            return self._make_easy_move(empty_cells)
        elif self.difficulty == 'hard':
            return self._make_hard_move(board, empty_cells)
        else:  # Medium difficulty (default)
            return self._make_medium_move(board, empty_cells)
    
    def _make_easy_move(self, empty_cells):
        """Make a random move."""
        return random.choice(empty_cells)
    
    def _make_medium_move(self, board, empty_cells):
        """
        Medium difficulty:
        - 70% chance to make the best move
        - 30% chance to make a random move
        """
        if random.random() < 0.7:
            return self._make_hard_move(board, empty_cells)
        else:
            return self._make_easy_move(empty_cells)
    
    def _make_hard_move(self, board, empty_cells):
        """
        Hard difficulty:
        - First try to win
        - Then try to block the player from winning
        - Then try to take the center
        - Then try to take a corner
        - Finally take any available cell
        """
        # Try to win
        for row, col in empty_cells:
            board_copy = [row[:] for row in board]
            board_copy[row][col] = 'O'
            if self._check_winner(board_copy, 'O'):
                return row, col
        
        # Try to block
        for row, col in empty_cells:
            board_copy = [row[:] for row in board]
            board_copy[row][col] = 'X'
            if self._check_winner(board_copy, 'X'):
                return row, col
        
        # Take center if available
        if board[1][1] == '':
            return 1, 1
        
        # Take a corner if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners if board[corner[0]][corner[1]] == '']
        if available_corners:
            return random.choice(available_corners)
        
        # Take any available cell
        return random.choice(empty_cells)
    
    def _check_winner(self, board, symbol):
        """Check if the given symbol has won on this board."""
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] == symbol:
                return True
        
        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] == symbol:
                return True
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] == symbol:
            return True
        
        if board[0][2] == board[1][1] == board[2][0] == symbol:
            return True
        
        return False