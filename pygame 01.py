"""
Pygame 01 - Pong Game
A classic Pong game with player vs computer
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 90
PADDLE_HEIGHT = 15
BALL_SIZE = 15
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 6
    
    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed
    
    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = 5 * random.choice([-1, 1])
        self.max_speed = 10
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce off left and right walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
    
    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = 5 * random.choice([-1, 1])
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
    
    def increase_speed(self):
        # Slightly increase speed after each hit
        if abs(self.speed_x) < self.max_speed:
            self.speed_x *= 1.05
        if abs(self.speed_y) < self.max_speed:
            self.speed_y *= 1.05

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.player_paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30 - PADDLE_HEIGHT)
        self.computer_paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, 30)
        self.ball = Ball()
        
        # Scores
        self.player_score = 0
        self.computer_score = 0
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        self.running = True
        self.paused = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.key == pygame.K_r:
                    self.reset_game()
    
    def update(self):
        if self.paused:
            return
        
        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_paddle.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_paddle.move_right()
        
        # Simple AI for computer
        if self.computer_paddle.rect.centerx < self.ball.rect.centerx:
            self.computer_paddle.move_right()
        elif self.computer_paddle.rect.centerx > self.ball.rect.centerx:
            self.computer_paddle.move_left()
        
        # Move ball
        self.ball.move()
        
        # Check collision with paddles
        if self.ball.rect.colliderect(self.player_paddle.rect):
            self.ball.speed_y = -abs(self.ball.speed_y)
            self.ball.increase_speed()
        
        if self.ball.rect.colliderect(self.computer_paddle.rect):
            self.ball.speed_y = abs(self.ball.speed_y)
            self.ball.increase_speed()
        
        # Check if ball goes out of bounds (scoring)
        if self.ball.rect.top <= 0:
            self.player_score += 1
            self.ball.reset()
        
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.computer_score += 1
            self.ball.reset()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw center line
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.rect(self.screen, GRAY, (x, SCREEN_HEIGHT // 2 - 2, 10, 4))
        
        # Draw paddles and ball
        self.player_paddle.draw(self.screen)
        self.computer_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        computer_text = self.font.render(str(self.computer_score), True, WHITE)
        player_text = self.font.render(str(self.player_score), True, WHITE)
        self.screen.blit(computer_text, (SCREEN_WIDTH // 2 - 30, 80))
        self.screen.blit(player_text, (SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT - 140))
        
        # Draw instructions
        instructions = self.small_font.render("A/D or LEFT/RIGHT to move | SPACE to pause | R to reset", True, GRAY)
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 40))
        
        # Draw pause message
        if self.paused:
            pause_text = self.font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.ball.reset()
        self.player_paddle.rect.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.computer_paddle.rect.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """
    Main function to run Pong game
    """
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
