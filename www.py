import pygame
import sys
from pygame.locals import * # Import all from pygame.locals for MOUSEBUTTONDOWN etc.

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600 # Using 800x600 for the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebel Interface")
clock = pygame.time.Clock()

# Colors - Dark theme hacker style
BACKGROUND = (10, 10, 15)
TEXT_COLOR = (0, 255, 100)  # Matrix green
BUTTON_COLOR = (30, 30, 40)
BUTTON_HOVER = (50, 80, 50)
BUTTON_TEXT = (0, 255, 150)
EXIT_COLOR = (80, 20, 30)
EXIT_HOVER = (120, 30, 40)
BACK_COLOR = (40, 40, 80)
BACK_HOVER = (60, 60, 120)

# Colors for circles
CIRCLE_COLOR_1 = (255, 255, 255) # White
CIRCLE_COLOR_2 = (255, 255, 255) # White

# Fonts
title_font = pygame.font.SysFont("consolas", 48, bold=True)
button_font = pygame.font.SysFont("consolas", 32)
small_font = pygame.font.SysFont("consolas", 24)
instruction_font = pygame.font.SysFont(None, 28) # Font for instructions in game play

class Button:
    """
    A class to create interactive buttons for the Pygame interface.
    """
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        """
        Draws the button on the given surface.
        Changes color based on hover state.
        """
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=8) # Outline

        text_surf = button_font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        """
        Checks if the mouse position is over the button.
        Updates the is_hovered state.
        """
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def handle_event(self, event):
        """
        Handles mouse click events for the button.
        Returns True if the button is clicked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
            if self.is_hovered:
                return True
        return False

class Circle:
    """
    A class to create draggable circles on the Pygame interface.
    """
    def __init__(self, color, radius, x, y):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.dragging = False
        self.offset_x = 0 # Offset for dragging
        self.offset_y = 0

    def draw(self, surface):
        """
        Draws the circle on the given surface, including an outline.
        """
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius, 2) # White outline

    def is_clicked(self, pos):
        """
        Checks if a given mouse position is within the circle's bounds.
        """
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.radius

    def start_drag(self, pos):
        """
        Initiates dragging for the circle.
        Calculates the offset from the mouse click to the circle's center.
        """
        self.dragging = True
        self.offset_x = self.x - pos[0]
        self.offset_y = self.y - pos[1]

    def drag(self, pos):
        """
        Updates the circle's position based on the mouse position during dragging.
        """
        if self.dragging:
            self.x = pos[0] + self.offset_x
            self.y = pos[1] + self.offset_y

    def stop_drag(self):
        """
        Stops the dragging action for the circle.
        """
        self.dragging = False

# Create buttons
center_x, center_y = screen.get_rect().center
button_width, button_height = 300, 60

start_btn = Button(center_x - 150, center_y - 100, button_width, button_height,
                   "Press To Start", BUTTON_COLOR, BUTTON_HOVER)
char_btn = Button(center_x - 150, center_y, button_width, button_height,
                  "Choose Character", BUTTON_COLOR, BUTTON_HOVER)
instr_btn = Button(center_x - 150, center_y + 100, button_width, button_height,
                   "Instructions", BUTTON_COLOR, BUTTON_HOVER)
exit_btn = Button(20, 20, 200, 40, "Press Space to Exit", EXIT_COLOR, EXIT_HOVER)
back_btn = Button(center_x - 100, HEIGHT - 80, 200, 50, "Back", BACK_COLOR, BACK_HOVER) # Positioned at bottom

# Create circles with initial positions
circle1 = Circle(CIRCLE_COLOR_1, 30, 40, HEIGHT // 2) # Centered vertically
circle2 = Circle(CIRCLE_COLOR_2, 30, WIDTH - 40, HEIGHT // 2) # Centered vertically

# Game states
MAIN_MENU = 0
GAME_PLAY = 1
CHARACTER_MENU = 2
INSTRUCTIONS_MENU = 3

current_state = MAIN_MENU

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE: # Allow SPACE or ESC to exit
                running = False

        # Handle button clicks and other interactions based on current state
        if current_state == MAIN_MENU:
            if start_btn.handle_event(event):
                current_state = GAME_PLAY
            elif char_btn.handle_event(event):
                current_state = CHARACTER_MENU
            elif instr_btn.handle_event(event):
                current_state = INSTRUCTIONS_MENU
            elif exit_btn.handle_event(event):
                running = False

        elif current_state == GAME_PLAY:
            # Handle mouse events for dragging circles
            if event.type == MOUSEBUTTONDOWN:
                if circle1.is_clicked(event.pos):
                    circle1.start_drag(event.pos)
                elif circle2.is_clicked(event.pos):
                    circle2.start_drag(event.pos)
            if event.type == MOUSEBUTTONUP:
                circle1.stop_drag()
                circle2.stop_drag()
            if event.type == MOUSEMOTION:
                circle1.drag(event.pos)
                circle2.drag(event.pos)
            if back_btn.handle_event(event):
                current_state = MAIN_MENU

        elif current_state == CHARACTER_MENU or current_state == INSTRUCTIONS_MENU:
            if back_btn.handle_event(event):
                current_state = MAIN_MENU

    # Update button states (hover effects)
    if current_state == MAIN_MENU:
        start_btn.check_hover(mouse_pos)
        char_btn.check_hover(mouse_pos)
        instr_btn.check_hover(mouse_pos)
        exit_btn.check_hover(mouse_pos)
    elif current_state == GAME_PLAY or current_state == CHARACTER_MENU or current_state == INSTRUCTIONS_MENU:
        back_btn.check_hover(mouse_pos)

    # Drawing section
    screen.fill(BACKGROUND) # Clear the screen with background color

    if current_state == MAIN_MENU:
        # Draw main menu title and subtitle
        title = title_font.render("REBEL SYSTEM", True, TEXT_COLOR)
        subtitle = small_font.render("No adds // free acess", True, (0, 180, 80))
        screen.blit(title, (center_x - title.get_width() // 2, 80))
        screen.blit(subtitle, (center_x - subtitle.get_width() // 2, 140))

        # Draw glitch effect for main menu
        for i in range(3):
            offset = pygame.Vector2(pygame.time.get_ticks() % 5, 0).rotate(i * 120)
            glitch_text = small_font.render(f">> Welcome To // Infinity battle  <<", True, (50, 150, 150))
            screen.blit(glitch_text, (center_x - glitch_text.get_width() // 2 + offset.x, 180 + offset.y))

        # Draw main menu buttons
        start_btn.draw(screen)
        char_btn.draw(screen)
        instr_btn.draw(screen)
        exit_btn.draw(screen)

    elif current_state == GAME_PLAY:
        # Draw circles when in game play state
        circle1.draw(screen)
        circle2.draw(screen)

        # Draw instructions for game play
        instructions = ["Press ESC to exit", "Drag circles with mouse"]
        for i, text in enumerate(instructions):
            text_surface = instruction_font.render(text, True, (200, 200, 220))
            screen.blit(text_surface, (WIDTH - text_surface.get_width() - 20, 20 + i * 30))
        back_btn.draw(screen) # Draw back button in game play

    elif current_state == CHARACTER_MENU:
        # Draw character menu content
        char_title = title_font.render("CHOOSE CHARACTER", True, TEXT_COLOR)
        screen.blit(char_title, (center_x - char_title.get_width() // 2, 80))
        # Placeholder for character selection options
        character_options = ["Character A", "Character B", "Character C"]
        for i, option in enumerate(character_options):
            option_surf = small_font.render(option, True, TEXT_COLOR)
            screen.blit(option_surf, (center_x - option_surf.get_width() // 2, 200 + i * 50))
        back_btn.draw(screen)

    elif current_state == INSTRUCTIONS_MENU:
        # Draw instructions menu content
        instr_title = title_font.render("INSTRUCTIONS", True, TEXT_COLOR)
        screen.blit(instr_title, (center_x - instr_title.get_width() // 2, 80))
        instruction_text = [
            "1. Drag the circles to desired positions.",
            "2. Avoid obstacles (if any).",
            "3. Press ESC or click 'Back' to return to main menu."
        ]
        for i, line in enumerate(instruction_text):
            line_surf = small_font.render(line, True, TEXT_COLOR)
            screen.blit(line_surf, (center_x - line_surf.get_width() // 2, 200 + i * 40))
        back_btn.draw(screen)

    # Draw hacker effect (always active, regardless of state)
    for i in range(100):
        x = pygame.time.get_ticks() % WIDTH
        y = (pygame.time.get_ticks() * i) % HEIGHT
        pygame.draw.line(screen, (0, 20 + i % 10, 0), (x, y), (x, y + 2), 1)

    pygame.display.flip() # Update the full display Surface to the screen
    clock.tick(60) # Control the frame rate

# Quit pygame and exit the system
pygame.quit()
sys.exit()
