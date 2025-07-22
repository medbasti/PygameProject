import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

import pygame
import sys

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
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

# Fonts
title_font = pygame.font.SysFont("consolas", 48, bold=True)
button_font = pygame.font.SysFont("consolas", 32)
small_font = pygame.font.SysFont("consolas", 24)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=8)

        text_surf = button_font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False


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
back_btn = Button(center_x - 100, center_y + 200, 200, 50, "Back", BACK_COLOR, BACK_HOVER)

# Game states
MAIN_MENU = 0
SUB_MENU = 1
current_state = MAIN_MENU
active_buttons = [start_btn, char_btn, instr_btn, exit_btn]

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False

        # Handle button clicks
        if current_state == MAIN_MENU:
            if exit_btn.handle_event(event):
                running = False
            for btn in [start_btn, char_btn, instr_btn]:
                if btn.handle_event(event):
                    current_state = SUB_MENU
                    active_buttons = [back_btn]

        elif current_state == SUB_MENU:
            if back_btn.handle_event(event):
                current_state = MAIN_MENU
                active_buttons = [start_btn, char_btn, instr_btn, exit_btn]

    # Update button states
    for btn in active_buttons:
        btn.check_hover(mouse_pos)

    # Drawing
    screen.fill(BACKGROUND)

    # Draw title in main menu
    if current_state == MAIN_MENU:
        title = title_font.render("REBEL SYSTEM", True, TEXT_COLOR)
        subtitle = small_font.render("No adds // free acess", True, (0, 180, 80))
        screen.blit(title, (center_x - title.get_width() // 2, 80))
        screen.blit(subtitle, (center_x - subtitle.get_width() // 2, 140))

        # Draw glitch effect
        for i in range(3):
            offset = pygame.Vector2(pygame.time.get_ticks() % 5, 0).rotate(i * 120)
            glitch_text = small_font.render(f">> Welcome To // Infinity battle  <<", True, (50, 150, 150))
            screen.blit(glitch_text, (center_x - glitch_text.get_width() // 2 + offset.x, 180 + offset.y))

    # Draw active buttons
    for btn in active_buttons:
        btn.draw(screen)

    # Draw hacker effect
    for i in range(100):
        x = pygame.time.get_ticks() % 800
        y = (pygame.time.get_ticks() * i) % 600
        pygame.draw.line(screen, (0, 20 + i % 10, 0), (x, y), (x, y + 2), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
# Screen setup
WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Repositioned Circles")

# Colors
BACKGROUND = (25, 25, 40)
white = (255, 255, 255)
white1= (255,255 ,255)


class Circle:
    def __init__(self, color, radius, x, y):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        # Draw outline
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius, 2)

    def is_clicked(self, pos):
        # Check if mouse click is within the circle
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.radius

    def start_drag(self, pos):
        self.dragging = True
        self.offset_x = self.x - pos[0]
        self.offset_y = self.y - pos[1]

    def drag(self, pos):
        if self.dragging:
            self.x = pos[0] + self.offset_x
            self.y = pos[1] + self.offset_y

    def stop_drag(self):
        self.dragging = False


# Create circles with different positions
circle1 = Circle(white, 30, 40, 360)
circle2 = Circle(white1, 30, 760, 360)

# Font for instructions
font = pygame.font.SysFont(None, 28)

# Game loop
clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            run = False

        # Mouse events for dragging circles
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
    # Fill the background
    win.fill(BACKGROUND)

    # Draw grid
    for x in range(0, WIDTH, 40):
        pygame.draw.line(win, (40, 40, 55), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(win, (40, 40, 55), (0, y), (WIDTH, y), 1)
    # Draw circles
    circle1.draw(win)
    circle2.draw(win)
    # Draw coordinates
    coords_text1 = font.render(f"white: ({circle1.x}, {circle1.y})", True,white)
    coords_text2 = font.render(f"white1: ({circle2.x}, {circle2.y})", True,white1)
    win.blit(coords_text1, (20, 20))
    win.blit(coords_text2, (20, 50))

    # Draw instructions
    instructions = [
        "Press Start ",
        "Press ctrl to exit"
    ]
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, (200, 200, 220))
        win.blit(text_surface, (WIDTH - text_surface.get_width() - 20, 20 + i * 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()