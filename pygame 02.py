"""
Pygame 02 - Pixel Art Fishing Game
A simple and relaxing fishing game with pixel art style
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
WATER_BLUE = (64, 164, 223)
DARK_WATER = (41, 128, 185)
BOAT_BROWN = (139, 69, 19)
BOAT_DARK = (101, 67, 33)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
SKIN_COLOR = (255, 220, 177)
SHIRT_BLUE = (70, 130, 180)
PANTS_BROWN = (101, 67, 33)
HAT_RED = (220, 20, 60)

# Fish colors and values
FISH_TYPES = [
    {"color": ORANGE, "size": 20, "points": 10, "speed": 2, "name": "Goldfish"},
    {"color": GREEN, "size": 25, "points": 20, "speed": 2.5, "name": "Bass"},
    {"color": RED, "size": 30, "points": 30, "speed": 3, "name": "Salmon"},
    {"color": (138, 43, 226), "size": 35, "points": 50, "speed": 3.5, "name": "Rare Fish"},
]

class Boat:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 40
        self.y = 100
        self.width = 80
        self.height = 30
        self.speed = 5
    
    def move_left(self):
        if self.x > 50:
            self.x -= self.speed
    
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width - 50:
            self.x += self.speed
    
    def draw(self, screen):
        # === BOAT SHADOW IN WATER ===
        shadow_y = self.y + self.height + 22
        pygame.draw.ellipse(screen, (20, 80, 120), 
                          (self.x + 8, shadow_y, self.width - 16, 10))
        
        # === BOAT HULL - CURVED BOTTOM (drawn with smooth curves) ===
        hull_color = (139, 69, 19)
        hull_dark = (101, 50, 15)
        hull_light = (180, 90, 40)
        
        # Main hull body - curved like a canoe/rowboat
        hull_main = [
            (self.x + 15, self.y + self.height - 5),  # Left top of hull
            (self.x + self.width - 15, self.y + self.height - 5),  # Right top of hull
            (self.x + self.width - 10, self.y + self.height + 10),  # Right curve point
            (self.x + self.width // 2, self.y + self.height + 20),  # Bottom center point (deepest)
            (self.x + 10, self.y + self.height + 10)  # Left curve point
        ]
        pygame.draw.polygon(screen, hull_dark, hull_main)
        
        # Hull highlight (lighter side showing 3D)
        hull_highlight = [
            (self.x + 15, self.y + self.height - 5),
            (self.x + self.width - 15, self.y + self.height - 5),
            (self.x + self.width - 12, self.y + self.height + 5),
            (self.x + self.width // 2, self.y + self.height + 12),
            (self.x + 12, self.y + self.height + 5)
        ]
        pygame.draw.polygon(screen, hull_light, hull_highlight)
        pygame.draw.polygon(screen, BLACK, hull_highlight, 2)
        
        # === BOAT DECK - OVAL/ELLIPSE SHAPE ===
        deck_color = (200, 120, 60)
        deck_dark = (160, 90, 45)
        
        # Main deck (ellipse for smooth curved boat)
        deck_ellipse = (self.x + 5, self.y, self.width - 10, self.height)
        pygame.draw.ellipse(screen, deck_color, deck_ellipse)
        
        # Deck inner shadow for depth (smaller ellipse inside)
        inner_deck = (self.x + 10, self.y + 5, self.width - 20, self.height - 10)
        pygame.draw.ellipse(screen, deck_dark, inner_deck)
        
        # === BOAT SIDES - CURVED PANELS ===
        # Left side curve (arc-like shape)
        left_side_points = [
            (self.x + 5, self.y + 8),
            (self.x + 5, self.y + self.height - 8),
            (self.x + 12, self.y + self.height - 5),
            (self.x + 12, self.y + 5)
        ]
        pygame.draw.polygon(screen, (170, 100, 50), left_side_points)
        
        # Right side curve
        right_side_points = [
            (self.x + self.width - 5, self.y + 8),
            (self.x + self.width - 5, self.y + self.height - 8),
            (self.x + self.width - 12, self.y + self.height - 5),
            (self.x + self.width - 12, self.y + 5)
        ]
        pygame.draw.polygon(screen, (150, 85, 45), right_side_points)
        
        # === BOAT INTERIOR (oval hole in center) ===
        interior_color = (100, 60, 30)
        interior_ellipse = (self.x + 15, self.y + 8, self.width - 30, self.height - 16)
        pygame.draw.ellipse(screen, interior_color, interior_ellipse)
        pygame.draw.ellipse(screen, BLACK, interior_ellipse, 1)
        
        # === BOAT SEATS (curved to match boat shape) ===
        seat_color = (140, 80, 40)
        # Front seat (curved rectangle/ellipse)
        front_seat = (self.x + 20, self.y + 10, self.width - 40, 6)
        pygame.draw.ellipse(screen, seat_color, front_seat)
        pygame.draw.ellipse(screen, BLACK, front_seat, 1)
        
        # Back seat
        back_seat = (self.x + 20, self.y + 20, self.width - 40, 6)
        pygame.draw.ellipse(screen, seat_color, back_seat)
        pygame.draw.ellipse(screen, BLACK, back_seat, 1)
        
        # === BOAT RIM/EDGE (outline the oval shape) ===
        # Outer rim
        pygame.draw.ellipse(screen, BLACK, deck_ellipse, 2)
        
        # Inner rim for detail
        rim_color = (220, 140, 70)
        rim_ellipse = (self.x + 8, self.y + 3, self.width - 16, self.height - 6)
        pygame.draw.ellipse(screen, rim_color, rim_ellipse, 2)
        
        # === BOW (front pointed part) ===
        bow_points = [
            (self.x + self.width // 2 - 8, self.y),
            (self.x + self.width // 2 + 8, self.y),
            (self.x + self.width // 2, self.y - 8)
        ]
        pygame.draw.polygon(screen, (180, 100, 50), bow_points)
        pygame.draw.polygon(screen, BLACK, bow_points, 2)
        
        # === STERN (back rounded part) ===
        stern_arc = (self.x + 5, self.y + self.height - 15, self.width - 10, 20)
        pygame.draw.arc(screen, hull_light, stern_arc, 3.5, 5.9, 3)
        
        # === DECORATIVE ELEMENTS ===
        # Oar locks (metal holders on sides)
        oarlock_color = (160, 160, 160)
        # Left oarlock
        pygame.draw.circle(screen, oarlock_color, (self.x + 15, self.y + self.height // 2), 3)
        pygame.draw.circle(screen, BLACK, (self.x + 15, self.y + self.height // 2), 3, 1)
        # Right oarlock
        pygame.draw.circle(screen, oarlock_color, (self.x + self.width - 15, self.y + self.height // 2), 3)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 15, self.y + self.height // 2), 3, 1)
        
        # Wood grain lines (curved to follow boat shape)
        grain_color = (120, 70, 35)
        for i in range(2):
            y_offset = self.y + 10 + i * 10
            pygame.draw.arc(screen, grain_color, (self.x + 10, y_offset - 5, self.width - 20, 15), 0, 3.14, 1)
        
        # === WATER EFFECTS ===
        wave_color = (150, 220, 255)
        wave_dark = (100, 180, 220)
        
        # Left waves
        pygame.draw.arc(screen, wave_color, (self.x - 8, self.y + self.height + 5, 15, 15), 0, 3.14, 2)
        pygame.draw.arc(screen, wave_dark, (self.x - 12, self.y + self.height + 8, 15, 15), 0, 3.14, 1)
        
        # Right waves
        pygame.draw.arc(screen, wave_color, (self.x + self.width - 7, self.y + self.height + 5, 15, 15), 0, 3.14, 2)
        pygame.draw.arc(screen, wave_dark, (self.x + self.width - 3, self.y + self.height + 8, 15, 15), 0, 3.14, 1)
    
    def draw(self, screen):
        # Boat body
        pygame.draw.rect(screen, BOAT_BROWN, (self.x, self.y, self.width, self.height))
        # Boat bottom (triangle-ish)
        pygame.draw.polygon(screen, BOAT_DARK, [
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
            (self.x + self.width - 10, self.y + self.height + 10),
            (self.x + 10, self.y + self.height + 10)
        ])
        # Boat outline
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        # Upgraded pixel art fisherman character
        char_x = self.x + self.width // 2
        char_base_y = self.y
        
        # === LEGS (draw first so they're behind body) ===
        leg_width = 5
        leg_height = 10
        # Left leg
        pygame.draw.rect(screen, PANTS_BROWN, (char_x - 7, char_base_y - 2, leg_width, leg_height))
        pygame.draw.rect(screen, BLACK, (char_x - 7, char_base_y - 2, leg_width, leg_height), 1)
        # Right leg
        pygame.draw.rect(screen, PANTS_BROWN, (char_x + 2, char_base_y - 2, leg_width, leg_height))
        pygame.draw.rect(screen, BLACK, (char_x + 2, char_base_y - 2, leg_width, leg_height), 1)
        
        # Shoes
        pygame.draw.rect(screen, BLACK, (char_x - 8, char_base_y + 8, 7, 3))
        pygame.draw.rect(screen, BLACK, (char_x + 1, char_base_y + 8, 7, 3))
        
        # === BODY (torso with shirt) ===
        torso_y = char_base_y - 12
        torso_height = 12
        torso_width = 14
        # Shirt body
        pygame.draw.rect(screen, SHIRT_BLUE, (char_x - torso_width//2, torso_y, torso_width, torso_height))
        pygame.draw.rect(screen, BLACK, (char_x - torso_width//2, torso_y, torso_width, torso_height), 1)
        
        # Shirt buttons
        pygame.draw.circle(screen, WHITE, (char_x, torso_y + 3), 1)
        pygame.draw.circle(screen, WHITE, (char_x, torso_y + 7), 1)
        
        # === ARMS ===
        arm_y = torso_y + 3
        arm_width = 4
        arm_length = 12
        
        # Left arm (relaxed)
        left_arm_rect = (char_x - torso_width//2 - arm_width, arm_y, arm_width, arm_length)
        pygame.draw.rect(screen, SHIRT_BLUE, left_arm_rect)
        pygame.draw.rect(screen, BLACK, left_arm_rect, 1)
        # Left hand
        pygame.draw.circle(screen, SKIN_COLOR, (char_x - torso_width//2 - 2, arm_y + arm_length + 2), 3)
        pygame.draw.circle(screen, BLACK, (char_x - torso_width//2 - 2, arm_y + arm_length + 2), 3, 1)
        
        # Right arm (holding fishing rod - angled)
        right_shoulder_x = char_x + torso_width//2
        right_shoulder_y = arm_y
        right_hand_x = char_x + 16
        right_hand_y = arm_y - 6
        # Upper arm
        pygame.draw.line(screen, SHIRT_BLUE, (right_shoulder_x, right_shoulder_y), 
                        (right_shoulder_x + 6, right_shoulder_y - 3), 5)
        pygame.draw.line(screen, BLACK, (right_shoulder_x, right_shoulder_y), 
                        (right_shoulder_x + 6, right_shoulder_y - 3), 1)
        # Lower arm
        pygame.draw.line(screen, SKIN_COLOR, (right_shoulder_x + 6, right_shoulder_y - 3), 
                        (right_hand_x, right_hand_y), 4)
        pygame.draw.line(screen, BLACK, (right_shoulder_x + 6, right_shoulder_y - 3), 
                        (right_hand_x, right_hand_y), 1)
        # Right hand
        pygame.draw.circle(screen, SKIN_COLOR, (right_hand_x, right_hand_y), 3)
        pygame.draw.circle(screen, BLACK, (right_hand_x, right_hand_y), 3, 1)
        
        # === FISHING ROD ===
        rod_start_x = right_hand_x
        rod_start_y = right_hand_y
        rod_end_x = char_x + 24
        rod_end_y = arm_y - 28
        # Rod body (thicker base, thinner tip)
        pygame.draw.line(screen, BOAT_DARK, (rod_start_x, rod_start_y), (rod_end_x, rod_end_y), 3)
        pygame.draw.line(screen, (160, 82, 45), (rod_start_x, rod_start_y), (rod_end_x, rod_end_y), 2)
        # Rod tip
        pygame.draw.circle(screen, BLACK, (rod_end_x, rod_end_y), 2)
        
        # === NECK ===
        neck_y = torso_y - 2
        pygame.draw.rect(screen, SKIN_COLOR, (char_x - 2, neck_y, 4, 3))
        pygame.draw.rect(screen, BLACK, (char_x - 2, neck_y, 4, 3), 1)
        
        # === HEAD ===
        head_y = neck_y - 10
        head_width = 10
        head_height = 10
        # Face
        pygame.draw.ellipse(screen, SKIN_COLOR, (char_x - head_width//2, head_y, head_width, head_height))
        pygame.draw.ellipse(screen, BLACK, (char_x - head_width//2, head_y, head_width, head_height), 1)
        
        # Hair
        pygame.draw.arc(screen, (101, 67, 33), (char_x - head_width//2, head_y - 2, head_width, 6), 0, 3.14, 2)
        
        # Eyes
        eye_y = head_y + 4
        pygame.draw.circle(screen, WHITE, (char_x - 2, eye_y), 2)
        pygame.draw.circle(screen, WHITE, (char_x + 2, eye_y), 2)
        pygame.draw.circle(screen, BLACK, (char_x - 2, eye_y), 1)
        pygame.draw.circle(screen, BLACK, (char_x + 2, eye_y), 1)
        
        # Smile
        pygame.draw.arc(screen, BLACK, (char_x - 3, eye_y, 6, 4), 3.5, 6, 1)
        
        # === FISHING HAT ===
        hat_y = head_y - 2
        # Hat base (brim)
        pygame.draw.ellipse(screen, HAT_RED, (char_x - 8, hat_y + 1, 16, 4))
        pygame.draw.ellipse(screen, BLACK, (char_x - 8, hat_y + 1, 16, 4), 1)
        # Hat top
        pygame.draw.ellipse(screen, HAT_RED, (char_x - 5, hat_y - 6, 10, 8))
        pygame.draw.ellipse(screen, BLACK, (char_x - 5, hat_y - 6, 10, 8), 1)
        # Hat detail/shine
        pygame.draw.circle(screen, (255, 100, 100), (char_x - 1, hat_y - 3), 2)

class FishingLine:
    def __init__(self, boat):
        self.boat = boat
        self.length = 0
        self.max_length = 350
        self.extending = False
        self.retracting = False
        self.speed = 4
        self.hook_size = 8
    
    def extend(self):
        if self.length < self.max_length:
            self.extending = True
            self.retracting = False
    
    def retract(self):
        self.extending = False
        self.retracting = True
    
    def update(self):
        if self.extending:
            self.length += self.speed
            if self.length >= self.max_length:
                self.length = self.max_length
                self.extending = False
        
        if self.retracting:
            self.length -= self.speed * 1.5
            if self.length <= 0:
                self.length = 0
                self.retracting = False
    
    def get_hook_pos(self):
        hook_x = self.boat.x + self.boat.width // 2
        hook_y = self.boat.y + self.boat.height + 10 + self.length
        return hook_x, hook_y
    
    def draw(self, screen):
        if self.length > 0:
            # Fishing line
            start_x = self.boat.x + self.boat.width // 2
            start_y = self.boat.y + self.boat.height + 10
            end_x, end_y = self.get_hook_pos()
            pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y), 2)
            
            # Hook
            pygame.draw.circle(screen, GOLD, (int(end_x), int(end_y)), self.hook_size)
            pygame.draw.circle(screen, BLACK, (int(end_x), int(end_y)), self.hook_size, 2)

class Fish:
    def __init__(self, fish_type):
        self.type = fish_type
        self.size = fish_type["size"]
        self.color = fish_type["color"]
        self.points = fish_type["points"]
        self.speed = fish_type["speed"]
        self.name = fish_type["name"]
        
        # Random starting position
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.x = -self.size
        else:
            self.x = SCREEN_WIDTH + self.size
        
        self.y = random.randint(200, SCREEN_HEIGHT - 50)
        
    def update(self):
        self.x += self.speed * self.direction
    
    def is_off_screen(self):
        return self.x < -100 or self.x > SCREEN_WIDTH + 100
    
    def draw(self, screen):
        # Determine lighter and darker shades for depth
        darker_color = tuple(max(0, c - 40) for c in self.color)
        lighter_color = tuple(min(255, c + 60) for c in self.color)
        
        # Fish main body (ellipse)
        body_rect = (int(self.x - self.size), int(self.y - self.size // 2), 
                    self.size * 2, self.size)
        pygame.draw.ellipse(screen, self.color, body_rect)
        
        # Add body shading (darker bottom half)
        dark_rect = (int(self.x - self.size), int(self.y), 
                    self.size * 2, self.size // 2)
        pygame.draw.ellipse(screen, darker_color, dark_rect)
        
        # Lighter belly/top highlight
        highlight_rect = (int(self.x - self.size // 2), int(self.y - self.size // 3), 
                         self.size, self.size // 3)
        pygame.draw.ellipse(screen, lighter_color, highlight_rect)
        
        # Fish tail with gradient effect
        tail_offset = -self.size if self.direction == 1 else self.size
        tail_points = [
            (int(self.x + tail_offset), int(self.y)),
            (int(self.x + tail_offset * 1.6), int(self.y - self.size // 1.5)),
            (int(self.x + tail_offset * 1.8), int(self.y)),
            (int(self.x + tail_offset * 1.6), int(self.y + self.size // 1.5))
        ]
        pygame.draw.polygon(screen, self.color, tail_points)
        pygame.draw.polygon(screen, darker_color, tail_points, 2)
        
        # Top fin
        fin_offset = self.size // 3 if self.direction == 1 else -self.size // 3
        top_fin = [
            (int(self.x + fin_offset), int(self.y - self.size // 2)),
            (int(self.x + fin_offset - self.size // 4), int(self.y - self.size)),
            (int(self.x + fin_offset + self.size // 4), int(self.y - self.size // 2))
        ]
        pygame.draw.polygon(screen, darker_color, top_fin)
        pygame.draw.polygon(screen, BLACK, top_fin, 1)
        
        # Side fin
        side_fin_x = self.size // 4 if self.direction == 1 else -self.size // 4
        side_fin = [
            (int(self.x + side_fin_x), int(self.y)),
            (int(self.x + side_fin_x * 2), int(self.y + self.size // 2)),
            (int(self.x + side_fin_x), int(self.y + self.size // 4))
        ]
        pygame.draw.polygon(screen, lighter_color, side_fin)
        pygame.draw.polygon(screen, BLACK, side_fin, 1)
        
        # Fish scales (small circles for texture)
        scale_spacing = self.size // 4
        for i in range(3):
            for j in range(2):
                scale_x = int(self.x - self.size // 2 + i * scale_spacing)
                scale_y = int(self.y - self.size // 4 + j * scale_spacing)
                pygame.draw.circle(screen, darker_color, (scale_x, scale_y), 2)
        
        # Fish eye (larger and more detailed)
        eye_offset = self.size // 2 if self.direction == 1 else -self.size // 2
        eye_x = int(self.x + eye_offset)
        eye_y = int(self.y - self.size // 4)
        
        # White of eye
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 5)
        # Black pupil
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)
        # Eye highlight
        pygame.draw.circle(screen, WHITE, (eye_x + 1, eye_y - 1), 1)
        
        # Mouth
        mouth_offset = self.size // 1.3 if self.direction == 1 else -self.size // 1.3
        mouth_x = int(self.x + mouth_offset)
        mouth_y = int(self.y + self.size // 6)
        pygame.draw.arc(screen, BLACK, (mouth_x - 3, mouth_y - 3, 6, 6), 0, 3.14, 2)
        
        # Fish body outline (do this last)
        pygame.draw.ellipse(screen, BLACK, body_rect, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pixel Art Fishing Game")
        self.clock = pygame.time.Clock()
        
        self.boat = Boat()
        self.fishing_line = FishingLine(self.boat)
        self.fishes = []
        self.caught_fish = None
        
        self.score = 0
        self.fish_caught_count = 0
        
        # Timer - 60 seconds (3600 frames at 60 FPS)
        self.time_limit = 60  # seconds
        self.time_remaining = self.time_limit
        self.timer_frames = 0
        
        # Fonts
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)
        
        # Spawn timer
        self.spawn_timer = 0
        self.spawn_delay = 120  # frames
        
        self.running = True
        self.game_over = False
        self.game_message = ""
        self.message_timer = 0
    
    def spawn_fish(self):
        fish_type = random.choice(FISH_TYPES)
        self.fishes.append(Fish(fish_type))
    
    def check_collision(self):
        if self.fishing_line.length > 0 and not self.caught_fish:
            hook_x, hook_y = self.fishing_line.get_hook_pos()
            
            for fish in self.fishes:
                # Check if hook is near fish
                distance = ((hook_x - fish.x) ** 2 + (hook_y - fish.y) ** 2) ** 0.5
                if distance < fish.size + self.fishing_line.hook_size:
                    self.caught_fish = fish
                    self.fishes.remove(fish)
                    self.fishing_line.retract()
                    return True
        return False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    elif self.fishing_line.length == 0:
                        self.fishing_line.extend()
                    elif not self.fishing_line.retracting:
                        self.fishing_line.retract()
    
    def update(self):
        if self.game_over:
            return
        
        # Update timer
        self.timer_frames += 1
        if self.timer_frames >= FPS:
            self.timer_frames = 0
            self.time_remaining -= 1
            
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                return
        
        # Move boat
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.boat.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.boat.move_right()
        
        # Update fishing line
        self.fishing_line.update()
        
        # Update caught fish position
        if self.caught_fish:
            hook_x, hook_y = self.fishing_line.get_hook_pos()
            self.caught_fish.x = hook_x
            self.caught_fish.y = hook_y
            
            # Check if fish reached boat
            if self.fishing_line.length <= 0:
                self.score += self.caught_fish.points
                self.fish_caught_count += 1
                self.game_message = f"Caught {self.caught_fish.name}! +{self.caught_fish.points} points!"
                self.message_timer = 90
                self.caught_fish = None
        
        # Spawn new fish
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_fish()
            self.spawn_timer = 0
            # Make spawning faster over time (but cap it)
            if self.spawn_delay > 60:
                self.spawn_delay -= 1
        
        # Update all fish
        for fish in self.fishes[:]:
            fish.update()
            if fish.is_off_screen():
                self.fishes.remove(fish)
        
        # Check for collisions
        self.check_collision()
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def draw(self):
        # Draw sky
        self.screen.fill(SKY_BLUE)
        
        # Draw water
        water_y = 150
        pygame.draw.rect(self.screen, WATER_BLUE, (0, water_y, SCREEN_WIDTH, SCREEN_HEIGHT - water_y))
        
        # Draw water surface waves
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.arc(self.screen, DARK_WATER, (i, water_y - 10, 40, 20), 0, 3.14, 2)
        
        # Draw all fish
        for fish in self.fishes:
            fish.draw(self.screen)
        
        # Draw caught fish
        if self.caught_fish:
            self.caught_fish.draw(self.screen)
        
        # Draw fishing line and boat
        self.fishing_line.draw(self.screen)
        self.boat.draw(self.screen)
        
        # Draw UI
        score_text = self.small_font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
        caught_text = self.tiny_font.render(f"Fish Caught: {self.fish_caught_count}", True, BLACK)
        self.screen.blit(caught_text, (20, 60))
        
        # Draw timer with color coding
        timer_color = BLACK
        if self.time_remaining <= 10:
            timer_color = RED
        elif self.time_remaining <= 20:
            timer_color = ORANGE
        
        timer_text = self.small_font.render(f"Time: {self.time_remaining}s", True, timer_color)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 180, 20))
        
        # Draw instructions
        instructions = self.tiny_font.render("A/D or LEFT/RIGHT to move | SPACE to cast/reel", True, BLACK)
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 30))
        
        # Draw message
        if self.message_timer > 0:
            message_surface = self.small_font.render(self.game_message, True, GOLD)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            # Draw background for message
            pygame.draw.rect(self.screen, BLACK, message_rect.inflate(20, 10))
            self.screen.blit(message_surface, message_rect)
        
        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game Over text
            game_over_text = self.font.render("TIME'S UP!", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(game_over_text, game_over_rect)
            
            # Final score
            final_score_text = self.font.render(f"Final Score: {self.score}", True, GOLD)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(final_score_text, final_score_rect)
            
            # Fish caught
            fish_count_text = self.small_font.render(f"Fish Caught: {self.fish_caught_count}", True, WHITE)
            fish_count_rect = fish_count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(fish_count_text, fish_count_rect)
            
            # Restart instruction
            restart_text = self.small_font.render("Press SPACE to Play Again", True, GREEN)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def reset_game(self):
        # Reset all game state
        self.score = 0
        self.fish_caught_count = 0
        self.time_remaining = self.time_limit
        self.timer_frames = 0
        self.game_over = False
        self.fishes = []
        self.caught_fish = None
        self.fishing_line.length = 0
        self.fishing_line.extending = False
        self.fishing_line.retracting = False
        self.spawn_timer = 0
        self.spawn_delay = 120
        self.boat.x = SCREEN_WIDTH // 2 - 40
    
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
    Main function to run the fishing game
    """
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
