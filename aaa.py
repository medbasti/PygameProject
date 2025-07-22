#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CLEAN SNAKE GAME v1.0
# MALWARE-FREE IMPLEMENTATION - JUST A FUN GAME

import pygame
import sys
import random
class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Classic Snake Game")

        # Game variables
        self.snake_size = 20
        self.snake_speed = 10
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 35)
        self.small_font = pygame.font.SysFont('Arial', 20)

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 120, 255)

        # Game state
        self.reset_game()

    def reset_game(self):
        """Reset game state"""
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = 'RIGHT'
        self.next_direction = self.direction
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        """Generate food at random position"""
        return (
            random.randrange(0, self.width - self.snake_size, self.snake_size),
            random.randrange(0, self.height - self.snake_size, self.snake_size)
        )

    def move_snake(self):
        """Move snake based on direction"""
        head_x, head_y = self.snake[0]

        if self.next_direction == 'RIGHT':
            head_x += self.snake_size
        elif self.next_direction == 'LEFT':
            head_x -= self.snake_size
        elif self.next_direction == 'UP':
            head_y -= self.snake_size
        elif self.next_direction == 'DOWN':
            head_y += self.snake_size

        self.direction = self.next_direction

        # Check collision with walls
        if (head_x < 0 or head_x >= self.width or
                head_y < 0 or head_y >= self.height):
            self.game_over = True
            return

        # Check collision with self
        if (head_x, head_y) in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, (head_x, head_y))

        # Check food collision
        if abs(head_x - self.food[0]) < self.snake_size and abs(head_y - self.food[1]) < self.snake_size:
            self.score += 10
            self.food = self.spawn_food()
            # Increase speed every 50 points
            if self.score % 50 == 0:
                self.snake_speed += 1
        else:
            self.snake.pop()

    def draw_game(self):
        """Draw all game elements"""
        self.screen.fill(self.black)

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = self.green if i == 0 else self.blue
            pygame.draw.rect(self.screen, color, (x, y, self.snake_size, self.snake_size))
            pygame.draw.rect(self.screen, self.black, (x, y, self.snake_size, self.snake_size), 1)

        # Draw food
        pygame.draw.rect(self.screen, self.red, (self.food[0], self.food[1], self.snake_size, self.snake_size))

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, self.white)
        self.screen.blit(score_text, (10, 10))

        # Draw speed
        speed_text = self.small_font.render(f'Speed: {self.snake_speed}', True, self.white)
        self.screen.blit(speed_text, (10, 50))

        # Draw game over
        if self.game_over:
            game_over_text = self.font.render('GAME OVER! Press R to restart', True, self.red)
            self.screen.blit(game_over_text, (self.width // 2 - 200, self.height // 2))

        pygame.display.update()

    def run(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_r:
                        self.reset_game()

                    if not self.game_over:
                        if event.key == pygame.K_UP and self.direction != 'DOWN':
                            self.next_direction = 'UP'
                        elif event.key == pygame.K_DOWN and self.direction != 'UP':
                            self.next_direction = 'DOWN'
                        elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                            self.next_direction = 'LEFT'
                        elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                            self.next_direction = 'RIGHT'

            if not self.game_over:
                self.move_snake()

            self.draw_game()
            self.clock.tick(self.snake_speed)


# === MAIN EXECUTION ===
if __name__ == '__main__':
    game = SnakeGame()
    game.run()