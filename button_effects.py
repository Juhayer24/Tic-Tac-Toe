import pygame
import math

class ButtonEffects:
    def __init__(self):
        # Button style constants
        self.shadow_offset = 5
        self.shadow_alpha = 100
        self.pulse_speed = 0.015  # Reduced from 0.03 for smoother animation
        self.hover_glow_size = 8  # Reduced from 10 for subtler effect
        
        # Animation states
        self.pulse_factor = 0
        self.pulse_direction = 1
        self.hover_buttons = set()  # Track button coordinates instead of Rect objects
        self.selected_buttons = set()  # Track selected buttons
        
        # Colors
        self.glow_color = (255, 255, 255, 80)  # Semi-transparent white
    
    def update(self):
        """Update all animation states."""
        # Update pulse effect
        self.pulse_factor += self.pulse_speed * self.pulse_direction
        if self.pulse_factor > 1:
            self.pulse_factor = 1
            self.pulse_direction = -1
        elif self.pulse_factor < 0:
            self.pulse_factor = 0
            self.pulse_direction = 1
    
    def draw_button(self, surface, rect, color, text, text_color, font, 
                    border_radius=10, is_hovered=False, is_active=False, is_selected=False):
        """Draw a button with hover and active states."""
        # Create button surfaces
        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        shadow_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Track if this button is being hovered using tuple of coordinates
        button_key = (rect.x, rect.y, rect.width, rect.height)
        if is_hovered and button_key not in self.hover_buttons:
            self.hover_buttons.add(button_key)
        elif not is_hovered and button_key in self.hover_buttons:
            self.hover_buttons.remove(button_key)
        
        # Track if this button is selected
        if is_selected:
            self.selected_buttons.add(button_key)
        elif button_key in self.selected_buttons:
            self.selected_buttons.remove(button_key)
        
        # Draw shadow first (more prominent when button is active)
        shadow_offset = self.shadow_offset * (1.5 if is_active else 1)
        shadow_alpha = self.shadow_alpha * (1.2 if is_active else 1)
        
        # Softer shadow effect
        pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), 
                        (0, 0, rect.width, rect.height), 
                        border_radius=border_radius)
        surface.blit(shadow_surface, (rect.x + shadow_offset//2, rect.y + shadow_offset//2))
        
        # Button color modifications
        button_color = color
        if is_selected:
            # Brighten the button when selected
            button_color = tuple(min(c + 20, 255) for c in color)
        elif is_active:
            # Darken the button
            button_color = tuple(max(c - 30, 0) for c in color)
        
        # Draw the main button
        pygame.draw.rect(button_surface, button_color, 
                        (0, 0, rect.width, rect.height), 
                        border_radius=border_radius)
        
        # Add borders
        if is_selected:
            # Draw white border for selected state
            pygame.draw.rect(button_surface, (255, 255, 255), 
                           (0, 0, rect.width, rect.height), 
                           width=3, border_radius=border_radius)
        else:
            border_color = (0, 0, 0) if is_active else (50, 50, 50)
            pygame.draw.rect(button_surface, border_color, 
                           (0, 0, rect.width, rect.height), 
                           width=2, border_radius=border_radius)
        
        # Draw the button to the surface
        surface.blit(button_surface, (rect.x, rect.y))
        
        # Add hover effect (only if not selected)
        if is_hovered and not is_selected:
            self._draw_hover_effect(surface, rect, border_radius)
        
        # Draw text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        
        # Apply a slight offset when button is active (pressed)
        if is_active:
            text_rect.x += 1
            text_rect.y += 1
            
        surface.blit(text_surface, text_rect)
    
    def _draw_hover_effect(self, surface, rect, border_radius):
        """Draw a pulsing glow effect around the button when hovered."""
        # Calculate pulse size
        glow_size = self.hover_glow_size * (0.5 + self.pulse_factor * 0.5)
        
        # Create a larger surface for the glow
        glow_rect = pygame.Rect(
            rect.x - glow_size,
            rect.y - glow_size,
            rect.width + glow_size * 2,
            rect.height + glow_size * 2
        )
        
        # Draw glow using multiple semi-transparent rectangles
        for i in range(int(glow_size), 0, -2):
            alpha = 100 - (i * 7)
            if alpha < 0:
                continue
                
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            current_glow = pygame.Rect(
                i, i, 
                glow_rect.width - i*2, 
                glow_rect.height - i*2
            )
            
            # Adjust radius for the glow
            current_radius = border_radius + (glow_size - i)
            
            pygame.draw.rect(
                glow_surface, 
                (*self.glow_color[:3], alpha), 
                current_glow, 
                border_radius=int(current_radius)
            )
            
            surface.blit(glow_surface, (glow_rect.x, glow_rect.y))