import pygame
import sys
import random
import math
from game_board import GameBoard
from ai_player import AIPlayer
from animation_effects import AnimationEffects
from button_effects import ButtonEffects

def main():
    # Initialize pygame
    pygame.init()
    
    # Constants
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 800
    BOARD_SIZE = 500
    
    # Colors
    WHITE = (255, 255, 255)
    BACKGROUND_COLOR = (25, 25, 35)  # Darker background
    TEXT_COLOR = (220, 220, 220)  # Lighter text
    BUTTON_COLOR = (80, 140, 250)
    BUTTON_HOVER_COLOR = (100, 160, 255)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    DIFFICULTY_EASY_COLOR = (76, 187, 23)
    DIFFICULTY_MEDIUM_COLOR = (255, 165, 0)
    DIFFICULTY_HARD_COLOR = (241, 90, 90)
    
    # Font setup - using cursive fonts
    try:
        font = pygame.font.Font('fonts/Pacifico.ttf', 48)
        medium_font = pygame.font.Font('fonts/Pacifico.ttf', 36)
        small_font = pygame.font.Font('fonts/Pacifico.ttf', 28)
    except:
        # Fallback to default font if custom font not found
        font = pygame.font.SysFont('cursive', 48)
        medium_font = pygame.font.SysFont('cursive', 36)
        small_font = pygame.font.SysFont('cursive', 28)
    
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    
    # Create game board
    board_x = (SCREEN_WIDTH - BOARD_SIZE) // 2
    board_y = (SCREEN_HEIGHT - BOARD_SIZE) // 2
    game_board = GameBoard(board_x, board_y, BOARD_SIZE)
    
    # Create animation effects
    animation = AnimationEffects()
    button_effects = ButtonEffects()
    
    # Create AI player with default difficulty
    ai_difficulty = 'medium'
    ai_player = AIPlayer(ai_difficulty)
    
    # Game state
    game_over = False
    player_turn = True  # True for player, False for AI
    winner = None
    win_type = None
    show_menu = True
    start_game = False
    
    # Button states
    restart_button_active = False
    menu_button_active = False
    easy_button_active = False
    medium_button_active = True  # Default is medium
    hard_button_active = False
    start_button_active = False
    
    # Button dimensions
    button_width = 180
    button_height = 60
    button_spacing = 20
    
    # Button positions
    easy_button = pygame.Rect(
        (SCREEN_WIDTH - 3 * button_width - 2 * button_spacing) // 2,
        SCREEN_HEIGHT - 200,
        button_width,
        button_height
    )
    medium_button = pygame.Rect(
        easy_button.right + button_spacing,
        SCREEN_HEIGHT - 200,
        button_width,
        button_height
    )
    hard_button = pygame.Rect(
        medium_button.right + button_spacing,
        SCREEN_HEIGHT - 200,
        button_width,
        button_height
    )
    start_button = pygame.Rect(
        (SCREEN_WIDTH - button_width) // 2,
        SCREEN_HEIGHT - 120,
        button_width,
        button_height
    )
    
    # Menu particles
    menu_particles = []
    
    # Background stars
    stars = []
    for _ in range(200):  # Increased from 100 to 200
        stars.append({
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT),
            'size': random.randint(1, 4),
            'speed': random.uniform(0.1, 0.8),
            'twinkle': random.random(),
            'color': (
                random.randint(180, 255),
                random.randint(180, 255),
                random.randint(200, 255)
            )
        })
    
    # Game loop
    clock = pygame.time.Clock()
    
    # Transition animation
    transition_alpha = 255
    fading_out = False
    fade_speed = 5
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if show_menu:
                    # Difficulty buttons
                    if easy_button.collidepoint(mouse_pos):
                        ai_difficulty = 'easy'
                        ai_player = AIPlayer(ai_difficulty)
                        # Update button states
                        easy_button_active = True
                        medium_button_active = False
                        hard_button_active = False
                    elif medium_button.collidepoint(mouse_pos):
                        ai_difficulty = 'medium'
                        ai_player = AIPlayer(ai_difficulty)
                        # Update button states
                        easy_button_active = False
                        medium_button_active = True
                        hard_button_active = False
                    elif hard_button.collidepoint(mouse_pos):
                        ai_difficulty = 'hard'
                        ai_player = AIPlayer(ai_difficulty)
                        # Update button states
                        easy_button_active = False
                        medium_button_active = False
                        hard_button_active = True
                    
                    # Start button
                    if start_button.collidepoint(mouse_pos):
                        start_button_active = True
                        fading_out = True
                
                elif not fading_out:
                    # Game board clicking (only when it's player's turn and game is not over)
                    if not game_over and player_turn:
                        if game_board.make_move(mouse_pos, 'X'):
                            player_turn = False
                            
                            # Check for win or draw
                            winner, win_type = game_board.check_winner()
                            if winner:
                                game_over = True
                                # Start win animation if we have win type
                                if win_type:
                                    animation.start_win_animation(
                                        win_type, 
                                        game_board.cell_size, 
                                        game_board.x, 
                                        game_board.y
                                    )
                            elif game_board.is_full():
                                game_over = True
                    
                    # Check for button clicks during gameplay
                    restart_button = pygame.Rect(
                        SCREEN_WIDTH // 2 - button_width - 10, 
                        SCREEN_HEIGHT - 100,
                        button_width, 
                        button_height
                    )
                    
                    menu_button = pygame.Rect(
                        SCREEN_WIDTH // 2 + 10, 
                        SCREEN_HEIGHT - 100,
                        button_width, 
                        button_height
                    )
                    
                    if restart_button.collidepoint(mouse_pos):
                        restart_button_active = True
                        game_board.reset()
                        animation.reset()
                        game_over = False
                        player_turn = True
                        winner = None
                        win_type = None
                    elif menu_button.collidepoint(mouse_pos):
                        menu_button_active = True
                        fading_out = True
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Reset active states for buttons
                restart_button_active = False
                menu_button_active = False
                start_button_active = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not show_menu:
                    # Reset the game
                    game_board.reset()
                    animation.reset()
                    game_over = False
                    player_turn = True
                    winner = None
                    win_type = None
                elif event.key == pygame.K_m and not fading_out:
                    # Return to menu
                    fading_out = True
                    # Will go back to menu after fade out
        
        # Update stars with color cycling
        for star in stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
            star['twinkle'] = (star['twinkle'] + 0.02) % 1.0  # Faster twinkling
            
            # Cycle through colors
            r, g, b = star['color']
            star['color'] = (
                180 + int(75 * abs(math.sin(star['twinkle'] * math.pi))),
                180 + int(75 * abs(math.sin(star['twinkle'] * math.pi + 2))),
                200 + int(55 * abs(math.sin(star['twinkle'] * math.pi + 4)))
            )
        
        # Handle transition animation
        if fading_out:
            transition_alpha += fade_speed
            if transition_alpha >= 255:
                transition_alpha = 255
                fading_out = False
                if show_menu:
                    show_menu = False
                    start_game = True
                    # Reset the game
                    game_board.reset()
                    animation.reset()
                    game_over = False
                    player_turn = True
                    winner = None
                    win_type = None
                else:
                    show_menu = True
        elif transition_alpha > 0:
            transition_alpha -= fade_speed
            if transition_alpha < 0:
                transition_alpha = 0
        
        # AI's turn (only when game is active)
        if not show_menu and not game_over and not player_turn and transition_alpha == 0:
            # AI makes a move
            ai_move = ai_player.make_move(game_board.get_board_state())
            if ai_move is not None:
                row, col = ai_move
                game_board.set_cell(row, col, 'O')
                player_turn = True
                
                # Check for win or draw
                winner, win_type = game_board.check_winner()
                if winner:
                    game_over = True
                    # Start win animation if we have win type
                    if win_type:
                        animation.start_win_animation(
                            win_type, 
                            game_board.cell_size, 
                            game_board.x, 
                            game_board.y
                        )
                elif game_board.is_full():
                    game_over = True
        
        # Update animations
        animation.update_animations()
        button_effects.update()
        
        # Menu particle effects
        if show_menu and random.random() < 0.1:
            menu_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(2, 5),
                'color': random.choice([
                    DIFFICULTY_EASY_COLOR, 
                    DIFFICULTY_MEDIUM_COLOR, 
                    DIFFICULTY_HARD_COLOR, 
                    BUTTON_COLOR
                ]),
                'speed': random.uniform(0.5, 2.0),
                'angle': random.uniform(0, math.pi * 2)
            })
        
        # Update menu particles
        for particle in menu_particles[:]:
            particle['x'] += math.cos(particle['angle']) * particle['speed']
            particle['y'] += math.sin(particle['angle']) * particle['speed']
            particle['size'] -= 0.02
            
            if particle['size'] <= 0 or (
                particle['x'] < 0 or particle['x'] > SCREEN_WIDTH or
                particle['y'] < 0 or particle['y'] > SCREEN_HEIGHT
            ):
                menu_particles.remove(particle)
        
        # Drawing
        screen.fill(BACKGROUND_COLOR)
        
        # Draw stars with new colors
        for star in stars:
            brightness = abs(math.sin(star['twinkle'] * math.pi * 2))
            color = tuple(int(c * brightness) for c in star['color'])
            pygame.draw.circle(
                screen, 
                color, 
                (int(star['x']), int(star['y'])), 
                star['size']
            )
        
        # Get mouse position for button hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw menu
        if show_menu:
            # Draw title with shadow
            title_text = font.render("Tic Tac Toe", True, TEXT_COLOR)
            shadow_offset = 3
            title_shadow = font.render("Tic Tac Toe", True, (200, 200, 200))
            screen.blit(title_shadow, (
                SCREEN_WIDTH // 2 - title_text.get_width() // 2 + shadow_offset, 
                150 + shadow_offset
            ))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
            
            # Draw subtitle
            subtitle_text = medium_font.render("Select AI Difficulty", True, TEXT_COLOR)
            screen.blit(subtitle_text, (
                SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 
                220
            ))
            
            # Draw Easy button with effects
            button_effects.draw_button(
                surface=screen,
                rect=easy_button,
                color=DIFFICULTY_EASY_COLOR,
                text="Easy",
                text_color=BUTTON_TEXT_COLOR,
                font=small_font,
                is_hovered=easy_button.collidepoint(mouse_pos),
                is_active=easy_button_active,
                is_selected=ai_difficulty == 'easy'
            )
            
            # Draw Medium button with effects
            button_effects.draw_button(
                surface=screen,
                rect=medium_button,
                color=DIFFICULTY_MEDIUM_COLOR,
                text="Medium",
                text_color=BUTTON_TEXT_COLOR,
                font=small_font,
                is_hovered=medium_button.collidepoint(mouse_pos),
                is_active=medium_button_active,
                is_selected=ai_difficulty == 'medium'
            )
            
            # Draw Hard button with effects
            button_effects.draw_button(
                surface=screen,
                rect=hard_button,
                color=DIFFICULTY_HARD_COLOR,
                text="Hard",
                text_color=BUTTON_TEXT_COLOR,
                font=small_font,
                is_hovered=hard_button.collidepoint(mouse_pos),
                is_active=hard_button_active,
                is_selected=ai_difficulty == 'hard'
            )
            
            # Draw Start button with effects
            button_effects.draw_button(
                surface=screen,
                rect=start_button,
                color=BUTTON_COLOR,
                text="Start Game",
                text_color=BUTTON_TEXT_COLOR,
                font=small_font,
                is_hovered=start_button.collidepoint(mouse_pos),
                is_active=start_button_active
            )
            
            # Draw menu particles
            for particle in menu_particles:
                pygame.draw.circle(
                    screen, 
                    particle['color'], 
                    (int(particle['x']), int(particle['y'])), 
                    int(particle['size'])
                )
        else:
            # Draw game screen
            # Title with shadow
            title_text = font.render("Tic Tac Toe", True, TEXT_COLOR)
            shadow_offset = 2
            title_shadow = font.render("Tic Tac Toe", True, (200, 200, 200))
            screen.blit(title_shadow, (
                SCREEN_WIDTH // 2 - title_text.get_width() // 2 + shadow_offset, 
                50 + shadow_offset
            ))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
            
            # Draw difficulty indicator
            difficulty_color = DIFFICULTY_MEDIUM_COLOR
            if ai_difficulty == 'easy':
                difficulty_color = DIFFICULTY_EASY_COLOR
                difficulty_text = "Easy AI"
            elif ai_difficulty == 'medium':
                difficulty_color = DIFFICULTY_MEDIUM_COLOR
                difficulty_text = "Medium AI"
            else:
                difficulty_color = DIFFICULTY_HARD_COLOR
                difficulty_text = "Hard AI"
            
            diff_text = small_font.render(difficulty_text, True, difficulty_color)
            diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(diff_text, diff_rect)
            
            # Draw game board
            game_board.draw(screen, animation)
            
            # Draw animations
            animation.draw_animations(screen)
            
            # Draw status
            status_text = ""
            if game_over:
                if winner == 'X':
                    status_text = "You Win!"
                    status_color = (50, 205, 50)  # Green
                elif winner == 'O':
                    status_text = "AI Wins!"
                    status_color = (241, 90, 90)  # Red
                else:
                    status_text = "Draw!"
                    status_color = TEXT_COLOR
            else:
                if player_turn:
                    status_text = "Your Turn"
                    status_color = (66, 134, 244)  # Blue (player color)
                else:
                    status_text = "AI Thinking..."
                    status_color = (241, 90, 90)  # Red (AI color)
            
            status_render = font.render(status_text, True, status_color)
            screen.blit(status_render, (
                SCREEN_WIDTH // 2 - status_render.get_width() // 2, 
                SCREEN_HEIGHT - 150
            ))
            
            # Create buttons
            restart_button = pygame.Rect(
                SCREEN_WIDTH // 2 - button_width - 10, 
                SCREEN_HEIGHT - 100,
                button_width, 
                button_height
            )
            
            menu_button = pygame.Rect(
                SCREEN_WIDTH // 2 + 10, 
                SCREEN_HEIGHT - 100,
                button_width, 
                button_height
            )
            
            # Draw restart button with effects
            button_effects.draw_button(
                surface=screen,
                rect=restart_button,
                color=BUTTON_COLOR,
                text="Restart",
                text_color=BUTTON_TEXT_COLOR,
                font=small_font,
                is_hovered=restart_button.collidepoint(mouse_pos),
                is_active=restart_button_active
            )
            
            # Draw menu button with effects
            button_effects.draw_button(
                surface=screen,
                rect=menu_button,
                color=BUTTON_COLOR,
                text="Menu",
                text_color=BUTTON_TEXT_COLOR,
                font=small_font,
                is_hovered=menu_button.collidepoint(mouse_pos),
                is_active=menu_button_active
            )
        
        # Draw transition overlay
        if transition_alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, transition_alpha))
            screen.blit(overlay, (0, 0))
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()