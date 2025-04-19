import pygame
import math
import random

class AnimationEffects:
    def __init__(self):
        # Colors
        self.highlight_color = (245, 245, 245, 150)  # Semi-transparent white
        self.win_line_color = (50, 205, 50)  # Green
        
        # Animation properties
        self.animation_speed = 5
        self.pulse_speed = 0.05
        self.win_line_width = 10
        self.win_line_progress = 0
        self.pulse_factor = 0
        self.pulse_direction = 1
        
        # Animation states
        self.animate_win_line = False
        self.win_line_start = None
        self.win_line_end = None
        self.win_animation_done = False
        
        # Particle effects
        self.particles = []
        self.particle_colors = [
            (80, 140, 250),    # Blue
            (241, 90, 90),     # Red
            (255, 215, 0),     # Gold
            (138, 43, 226),    # Purple
            (50, 205, 50),     # Green
            (255, 150, 0),     # Orange
            (0, 255, 255),     # Cyan
        ]
        
        # New particle properties
        self.particle_trails = []
        self.glow_particles = []
    
    def start_win_animation(self, win_type, cell_size, board_x, board_y):
        """Start the winning line animation."""
        self.animate_win_line = True
        self.win_line_progress = 0
        
        half_cell = cell_size / 2
        
        # Set start and end points based on win type
        if win_type.startswith('row'):
            row = int(win_type[3])
            self.win_line_start = (board_x, board_y + row * cell_size + half_cell)
            self.win_line_end = (board_x + 3 * cell_size, board_y + row * cell_size + half_cell)
        
        elif win_type.startswith('col'):
            col = int(win_type[3])
            self.win_line_start = (board_x + col * cell_size + half_cell, board_y)
            self.win_line_end = (board_x + col * cell_size + half_cell, board_y + 3 * cell_size)
        
        elif win_type == 'diag1':  # Top-left to bottom-right
            self.win_line_start = (board_x, board_y)
            self.win_line_end = (board_x + 3 * cell_size, board_y + 3 * cell_size)
        
        elif win_type == 'diag2':  # Top-right to bottom-left
            self.win_line_start = (board_x + 3 * cell_size, board_y)
            self.win_line_end = (board_x, board_y + 3 * cell_size)
    
    def update_animations(self):
        """Update all animation states."""
        # Update win line animation
        if self.animate_win_line and self.win_line_progress < 1:
            self.win_line_progress += 0.03
            if self.win_line_progress >= 1:
                self.win_line_progress = 1
                self.win_animation_done = True
                self._create_celebration_particles()
        
        # Update pulse effect
        self.pulse_factor += self.pulse_speed * self.pulse_direction
        if self.pulse_factor > 1:
            self.pulse_factor = 1
            self.pulse_direction = -1
        elif self.pulse_factor < 0:
            self.pulse_factor = 0
            self.pulse_direction = 1
        
        # Update particles
        self._update_particles()
    
    def draw_animations(self, surface):
        """Draw all active animations."""
        # Draw win line if animating
        if self.animate_win_line:
            current_end_x = self.win_line_start[0] + (self.win_line_end[0] - self.win_line_start[0]) * self.win_line_progress
            current_end_y = self.win_line_start[1] + (self.win_line_end[1] - self.win_line_start[1]) * self.win_line_progress
            
            pygame.draw.line(
                surface, 
                self.win_line_color, 
                self.win_line_start, 
                (current_end_x, current_end_y), 
                self.win_line_width
            )
        
        # Draw particles
        self._draw_particles(surface)
    
    def draw_hover_effect(self, surface, cell_x, cell_y, cell_size):
        """Draw hover effect with pulsing animation."""
        # Calculate pulse size (slightly larger or smaller based on pulse factor)
        pulse_size = int(cell_size * (1 + self.pulse_factor * 0.05))
        offset = (pulse_size - cell_size) // 2
        
        # Create semi-transparent surface for the hover effect
        hover_surface = pygame.Surface((pulse_size, pulse_size), pygame.SRCALPHA)
        pygame.draw.rect(hover_surface, self.highlight_color, 
                        (0, 0, pulse_size, pulse_size), 0)
        
        # Draw the pulsing hover effect
        surface.blit(hover_surface, (cell_x - offset, cell_y - offset))
    
    def reset(self):
        """Reset all animation states."""
        self.animate_win_line = False
        self.win_line_progress = 0
        self.win_animation_done = False
        self.particles = []
    
    def _create_celebration_particles(self):
        """Create enhanced particles for win celebration."""
        center_x = (self.win_line_start[0] + self.win_line_end[0]) / 2
        center_y = (self.win_line_start[1] + self.win_line_end[1]) / 2
        
        # Create more particles with varied effects
        for _ in range(100):  # Increased from 50 to 100
            angle = math.radians(random.uniform(0, 360))
            speed = random.uniform(2, 8)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            color = random.choice(self.particle_colors)
            size = random.randint(4, 12)
            lifetime = random.randint(40, 120)
            
            particle = {
                'x': center_x,
                'y': center_y,
                'vel_x': vel_x,
                'vel_y': vel_y,
                'size': size,
                'color': color,
                'lifetime': lifetime,
                'trail': [],  # Add trail effect
                'angular_vel': random.uniform(-5, 5),  # Add rotation
                'type': random.choice(['circle', 'star', 'spark'])
            }
            
            self.particles.append(particle)
            
            # Add some glowing particles
            if random.random() < 0.3:
                self.glow_particles.append({
                    'x': center_x,
                    'y': center_y,
                    'size': random.randint(20, 40),
                    'color': color,
                    'lifetime': lifetime // 2,
                    'alpha': 255
                })
    
    def _update_particles(self):
        """Update particle positions and lifetimes."""
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            
            # Apply gravity
            particle['vel_y'] += 0.1
            
            # Decrease lifetime
            particle['lifetime'] -= 1
            
            # Update trail
            particle['trail'].append({
                'x': particle['x'],
                'y': particle['y'],
                'size': max(1, particle['size'] // 2),
                'alpha': max(0, int(255 * (particle['lifetime'] / 120)))
            })
            if len(particle['trail']) > 10:
                particle['trail'].pop(0)
            
            # Remove dead particles
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
        
        for glow in self.glow_particles[:]:
            glow['lifetime'] -= 1
            if glow['lifetime'] <= 0:
                self.glow_particles.remove(glow)
    
    def _draw_particles(self, surface):
        """Draw enhanced particles with effects."""
        # Draw glow particles first
        for glow in self.glow_particles[:]:
            glow_surface = pygame.Surface((glow['size'] * 2, glow['size'] * 2), pygame.SRCALPHA)
            color = list(glow['color']) + [glow['alpha']]
            pygame.draw.circle(glow_surface, color, (glow['size'], glow['size']), glow['size'])
            surface.blit(glow_surface, (glow['x'] - glow['size'], glow['y'] - glow['size']), special_flags=pygame.BLEND_ADD)
            glow['alpha'] = max(0, glow['alpha'] - 5)
            glow['lifetime'] -= 1
            if glow['lifetime'] <= 0:
                self.glow_particles.remove(glow)
        
        # Draw regular particles with their trails
        for particle in self.particles:
            # Draw trail
            for trail_pos in particle['trail']:
                size = trail_pos['size']
                alpha = trail_pos['alpha']
                color = list(particle['color']) + [alpha]
                
                trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, color, (size, size), size)
                surface.blit(trail_surface, (trail_pos['x'] - size, trail_pos['y'] - size))
            
            # Draw main particle
            if particle['type'] == 'circle':
                pygame.draw.circle(surface, particle['color'], 
                                (int(particle['x']), int(particle['y'])), 
                                particle['size'])
            elif particle['type'] == 'star':
                self._draw_star(surface, particle)
            else:  # spark
                self._draw_spark(surface, particle)
    
    def _draw_star(self, surface, particle):
        """Draw a star-shaped particle."""
        # Placeholder for star drawing logic
        pass
    
    def _draw_spark(self, surface, particle):
        """Draw a spark-shaped particle."""
        # Placeholder for spark drawing logic
        pass