import pygame
import math

class GameBoard:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.cell_size = size // 3
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        
        # Colors
        self.line_color = (80, 80, 80)
        self.x_color = (66, 134, 244)  # Blue
        self.o_color = (241, 90, 90)   # Red
        self.highlight_color = (220, 220, 220)
        self.board_bg_color = (255, 255, 255)
        self.cell_bg_color = (248, 248, 248)
        
        # Line thickness
        self.line_thickness = 8
        self.symbol_thickness = 10
        
        # Padding for X and O
        self.symbol_padding = 20
        
        # Animation properties
        self.draw_X_progress = {}  # {(row, col): progress}
        self.draw_O_progress = {}  # {(row, col): progress}
        self.animation_speed = 0.05
        
    def reset(self):
        """Reset the board to its initial state."""
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.draw_X_progress = {}
        self.draw_O_progress = {}
    
    def draw(self, surface, animation=None):
        """Draw the board on the given surface."""
        # Draw board background with shadow
        shadow_offset = 10
        shadow_surface = pygame.Surface((self.size + shadow_offset, self.size + shadow_offset))
        shadow_surface.fill((0, 0, 0, 0))
        shadow_surface.set_alpha(30)
        pygame.draw.rect(shadow_surface, (0, 0, 0), 
                         (0, 0, self.size + shadow_offset, self.size + shadow_offset), 
                         border_radius=15)
        surface.blit(shadow_surface, (self.x - shadow_offset//2, self.y - shadow_offset//2))
        
        # Draw main board background
        pygame.draw.rect(surface, self.board_bg_color, 
                         (self.x, self.y, self.size, self.size), 
                         border_radius=10)
        
        # Draw cells with subtle background
        for row in range(3):
            for col in range(3):
                cell_x = self.x + col * self.cell_size
                cell_y = self.y + row * self.cell_size
                
                # Draw cell background
                pygame.draw.rect(surface, self.cell_bg_color,
                                (cell_x + 3, cell_y + 3, 
                                 self.cell_size - 6, self.cell_size - 6),
                                border_radius=5)
        
        # Draw grid lines
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(surface, self.line_color, 
                             (self.x + i * self.cell_size, self.y + 5),
                             (self.x + i * self.cell_size, self.y + self.size - 5),
                             self.line_thickness)
            
            # Horizontal lines
            pygame.draw.line(surface, self.line_color, 
                             (self.x + 5, self.y + i * self.cell_size),
                             (self.x + self.size - 5, self.y + i * self.cell_size),
                             self.line_thickness)
        
        # Update and draw X's and O's with animation
        self._update_animations()
        
        for row in range(3):
            for col in range(3):
                cell_x = self.x + col * self.cell_size
                cell_y = self.y + row * self.cell_size
                
                # Draw symbols with animation
                if self.board[row][col] == 'X':
                    progress = self.draw_X_progress.get((row, col), 1.0)
                    self._draw_x_animated(surface, cell_x, cell_y, progress)
                elif self.board[row][col] == 'O':
                    progress = self.draw_O_progress.get((row, col), 1.0)
                    self._draw_o_animated(surface, cell_x, cell_y, progress)
                
        # Draw hover effect
        if not self.is_full() and not self.check_winner()[0]:
            mouse_pos = pygame.mouse.get_pos()
            cell = self._get_cell_from_pos(mouse_pos)
            if cell:
                row, col = cell
                # Make sure row and col are valid indices
                if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '':
                    cell_x = self.x + col * self.cell_size
                    cell_y = self.y + row * self.cell_size
                    
                    if animation:
                        # Use animated hover effect if animation object is provided
                        animation.draw_hover_effect(surface, cell_x, cell_y, self.cell_size)
                    else:
                        # Fallback to simple hover effect
                        pygame.draw.rect(surface, self.highlight_color, 
                                        (cell_x, cell_y, self.cell_size, self.cell_size), 0)
    
    def _update_animations(self):
        """Update all animation progresses."""
        # Update X drawing animations
        for pos in list(self.draw_X_progress.keys()):
            self.draw_X_progress[pos] += self.animation_speed
            if self.draw_X_progress[pos] >= 1.0:
                self.draw_X_progress[pos] = 1.0
        
        # Update O drawing animations
        for pos in list(self.draw_O_progress.keys()):
            self.draw_O_progress[pos] += self.animation_speed
            if self.draw_O_progress[pos] >= 1.0:
                self.draw_O_progress[pos] = 1.0
    
    def _draw_x_animated(self, surface, x, y, progress):
        """Draw an X with animation progress."""
        # Calculate endpoints for both lines
        start1_x = x + self.symbol_padding
        start1_y = y + self.symbol_padding
        end1_x = x + self.cell_size - self.symbol_padding
        end1_y = y + self.cell_size - self.symbol_padding
        
        start2_x = x + self.cell_size - self.symbol_padding
        start2_y = y + self.symbol_padding
        end2_x = x + self.symbol_padding
        end2_y = y + self.cell_size - self.symbol_padding
        
        # Draw first line with progress
        if progress <= 0.5:  # First half of animation draws first line
            line_progress = progress * 2  # Scale to 0-1 range
            current_end_x = start1_x + (end1_x - start1_x) * line_progress
            current_end_y = start1_y + (end1_y - start1_y) * line_progress
            
            pygame.draw.line(surface, self.x_color, 
                            (start1_x, start1_y),
                            (current_end_x, current_end_y),
                            self.symbol_thickness)
        else:  # First line complete
            pygame.draw.line(surface, self.x_color, 
                            (start1_x, start1_y),
                            (end1_x, end1_y),
                            self.symbol_thickness)
            
            # Draw second line with progress
            if progress > 0.5:  # Second half of animation draws second line
                line_progress = (progress - 0.5) * 2  # Scale to 0-1 range
                current_end_x = start2_x + (end2_x - start2_x) * line_progress
                current_end_y = start2_y + (end2_y - start2_y) * line_progress
                
                pygame.draw.line(surface, self.x_color, 
                                (start2_x, start2_y),
                                (current_end_x, current_end_y),
                                self.symbol_thickness)
    
    def _draw_o_animated(self, surface, x, y, progress):
        """Draw an O with animation progress."""
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        radius = self.cell_size // 2 - self.symbol_padding
        
        # Calculate the arc angle based on progress
        end_angle = progress * 360
        
        # Draw partial or complete circle based on progress
        if progress < 1.0:
            # Draw partial circle as arc
            arc_rect = pygame.Rect(
                center_x - radius, center_y - radius,
                radius * 2, radius * 2
            )
            # Convert angles to radians for calculations
            start_angle_rad = math.radians(0)
            end_angle_rad = math.radians(end_angle)
            
            # Draw the arc as a series of small lines
            points = []
            for angle in range(0, int(end_angle) + 1, 5):
                angle_rad = math.radians(angle)
                point_x = center_x + radius * math.cos(angle_rad)
                point_y = center_y - radius * math.sin(angle_rad)
                points.append((point_x, point_y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.o_color, False, points, self.symbol_thickness)
        else:
            # Draw complete circle
            pygame.draw.circle(surface, self.o_color, 
                              (center_x, center_y), radius, self.symbol_thickness)
    
    def _draw_x(self, surface, x, y):
        """Draw an X in the specified cell."""
        pygame.draw.line(surface, self.x_color, 
                         (x + self.symbol_padding, y + self.symbol_padding),
                         (x + self.cell_size - self.symbol_padding, 
                          y + self.cell_size - self.symbol_padding),
                         self.symbol_thickness)
        
        pygame.draw.line(surface, self.x_color, 
                         (x + self.cell_size - self.symbol_padding, y + self.symbol_padding),
                         (x + self.symbol_padding, 
                          y + self.cell_size - self.symbol_padding),
                         self.symbol_thickness)
    
    def _draw_o(self, surface, x, y):
        """Draw an O in the specified cell."""
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        radius = self.cell_size // 2 - self.symbol_padding
        
        pygame.draw.circle(surface, self.o_color, 
                           (center_x, center_y), radius, self.symbol_thickness)
    
    def _get_cell_from_pos(self, pos):
        """Convert screen position to board cell coordinates."""
        x, y = pos
        
        # Check if position is within board boundaries
        if (x < self.x or x >= self.x + self.size or
            y < self.y or y >= self.y + self.size):
            return None
        
        # Calculate row and column
        col = (x - self.x) // self.cell_size
        row = (y - self.y) // self.cell_size
        
        # Ensure row and col are within valid range (0-2)
        if 0 <= row < 3 and 0 <= col < 3:
            return row, col
        
        return None
    
    def make_move(self, pos, symbol):
        """Make a move at the position with the given symbol."""
        cell = self._get_cell_from_pos(pos)
        if cell:
            row, col = cell
            if self.board[row][col] == '':
                self.board[row][col] = symbol
                
                # Start animation for the new symbol
                if symbol == 'X':
                    self.draw_X_progress[(row, col)] = 0.0
                elif symbol == 'O':
                    self.draw_O_progress[(row, col)] = 0.0
                
                return True
        return False
    
    def set_cell(self, row, col, symbol):
        """Set the value of a cell directly."""
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '':
            self.board[row][col] = symbol
            
            # Start animation for the new symbol
            if symbol == 'X':
                self.draw_X_progress[(row, col)] = 0.0
            elif symbol == 'O':
                self.draw_O_progress[(row, col)] = 0.0
                
            return True
        return False
    
    def get_board_state(self):
        """Return a copy of the current board state."""
        return [row[:] for row in self.board]
    
    def is_full(self):
        """Check if the board is full."""
        for row in self.board:
            if '' in row:
                return False
        return True
    
    def check_winner(self):
        """
        Check if there's a winner. 
        Returns a tuple (winner, win_type) where:
            - winner is the winning symbol or None
            - win_type indicates which line won (row0, col1, diag1, etc.)
        """
        # Check rows
        for row_idx, row in enumerate(self.board):
            if row[0] != '' and row[0] == row[1] == row[2]:
                return row[0], f'row{row_idx}'
        
        # Check columns
        for col in range(3):
            if (self.board[0][col] != '' and 
                self.board[0][col] == self.board[1][col] == self.board[2][col]):
                return self.board[0][col], f'col{col}'
        
        # Check diagonals
        if (self.board[0][0] != '' and 
            self.board[0][0] == self.board[1][1] == self.board[2][2]):
            return self.board[0][0], 'diag1'
        
        if (self.board[0][2] != '' and 
            self.board[0][2] == self.board[1][1] == self.board[2][0]):
            return self.board[0][2], 'diag2'
        
        return None, None