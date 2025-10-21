"""
Claw Machine Game - Pixel Art Style
Press ENTER to insert a coin and start playing!
"""

import pygame
import sys
import random
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors - Pixel Art Palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
GRAY = (128, 128, 128)
LIGHT_GRAY = (180, 180, 180)
RED = (220, 50, 50)
YELLOW = (255, 220, 0)
GOLD = (255, 180, 0)
ORANGE = (255, 140, 0)
BROWN = (120, 60, 30)
DARK_BROWN = (80, 40, 20)
BLUE = (60, 120, 200)
LIGHT_BLUE = (120, 180, 255)
PINK = (255, 150, 180)
PURPLE = (180, 100, 220)
GREEN = (80, 200, 120)

# Turtle colors (pixel art style)
TURTLE_COLORS = [
    (100, 200, 100),  # Green
    (60, 130, 60),    # Dark Green
    (120, 150, 170),  # Grey Blue
    (180, 200, 80),   # Yellow-Green
    (30, 60, 120),    # Dark Blue
]

# Owl colors (pixel art style)
OWL_COLORS = [
    (150, 100, 50),   # Brown
    (200, 150, 100),  # Light Brown
    (100, 80, 120),   # Purple-Grey
    (180, 160, 140),  # Beige
    (80, 60, 40),     # Dark Brown
]

# Sound Generator Class
class SoundGenerator:
    """Generate simple sound effects using pygame"""
    
    @staticmethod
    def generate_tone(frequency, duration, volume=0.3):
        """Generate a simple tone"""
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        
        # Generate sine wave
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(frequency * t * 2 * np.pi)
        
        # Apply envelope (fade in/out)
        envelope = np.ones(n_samples)
        fade_len = int(sample_rate * 0.01)  # 10ms fade
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)
        wave = wave * envelope * volume
        
        # Convert to 16-bit integers
        wave = (wave * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo_wave = np.column_stack((wave, wave))
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    @staticmethod
    def coin_sound():
        """Coin insertion sound - bright metallic clink with echo"""
        sample_rate = 22050
        duration = 0.3
        n_samples = int(sample_rate * duration)
        
        # Create two metallic hits with echo effect
        t = np.linspace(0, duration, n_samples, False)
        
        # Main hit (high frequency)
        main_freq = 1200
        wave1 = np.sin(main_freq * t * 2 * np.pi) * np.exp(-t * 15)
        
        # Second harmonic
        wave2 = np.sin(main_freq * 1.5 * t * 2 * np.pi) * np.exp(-t * 20) * 0.5
        
        # Echo (delayed quieter hit)
        echo_start = int(n_samples * 0.15)
        wave_echo = np.zeros(n_samples)
        if echo_start < n_samples:
            wave_echo[echo_start:] = wave1[:n_samples-echo_start] * 0.3
        
        # Combine
        wave = (wave1 + wave2 + wave_echo) * 0.4
        
        # Convert to 16-bit
        wave = np.clip(wave * 32767, -32767, 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    @staticmethod
    def move_sound():
        """Claw movement sound - short motor whir with slight pitch variation"""
        sample_rate = 22050
        duration = 0.08
        n_samples = int(sample_rate * duration)
        
        # Create motor-like sound with frequency modulation
        t = np.linspace(0, duration, n_samples, False)
        
        # Base frequency with slight vibration
        base_freq = 180
        vibrato = 20 * np.sin(40 * t * 2 * np.pi)  # Fast vibration
        freq = base_freq + vibrato
        
        # Generate wave
        phase = np.cumsum(freq * 2 * np.pi / sample_rate)
        wave = np.sin(phase)
        
        # Add harmonics for mechanical sound
        wave += 0.3 * np.sin(2 * phase)  # Octave
        wave += 0.2 * np.sin(3 * phase)  # Fifth
        
        # Quick fade in/out envelope
        envelope = np.ones(n_samples)
        fade_in = int(n_samples * 0.1)
        fade_out = int(n_samples * 0.2)
        envelope[:fade_in] = np.linspace(0, 1, fade_in)
        envelope[-fade_out:] = np.linspace(1, 0, fade_out)
        
        wave = wave * envelope * 0.15
        
        # Convert to 16-bit
        wave = np.clip(wave * 32767, -32767, 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    @staticmethod
    def victory_sound():
        """Victory sound - happy ascending notes"""
        sample_rate = 22050
        duration = 0.6
        n_samples = int(sample_rate * duration)
        
        # Three ascending notes
        freqs = [523, 659, 784]  # C, E, G
        wave = np.zeros(n_samples)
        
        for i, freq in enumerate(freqs):
            start = int(i * n_samples / 3)
            end = int((i + 1) * n_samples / 3)
            t = np.linspace(0, duration/3, end - start, False)
            note = np.sin(freq * t * 2 * np.pi)
            
            # Add envelope
            envelope = np.exp(-t * 3)  # Decay
            wave[start:end] = note * envelope * 0.3
        
        # Convert to 16-bit
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    @staticmethod
    def fall_sound():
        """Falling sound - descending pitch"""
        sample_rate = 22050
        duration = 0.4
        n_samples = int(sample_rate * duration)
        
        # Descending frequency
        t = np.linspace(0, duration, n_samples, False)
        freq_start = 600
        freq_end = 200
        freq = np.linspace(freq_start, freq_end, n_samples)
        
        # Generate wave with changing frequency
        phase = np.cumsum(freq * 2 * np.pi / sample_rate)
        wave = np.sin(phase) * 0.3
        
        # Fade out
        envelope = np.exp(-t * 2)
        wave = wave * envelope
        
        # Convert to 16-bit
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    @staticmethod
    def grab_sound():
        """Grab sound - positive chirp when catching a turtle"""
        sample_rate = 22050
        duration = 0.25
        n_samples = int(sample_rate * duration)
        
        # Two quick ascending notes (happy chirp)
        t = np.linspace(0, duration, n_samples, False)
        
        # First note (lower)
        freq1 = 600
        note1_end = int(n_samples * 0.4)
        wave = np.zeros(n_samples)
        wave[:note1_end] = np.sin(freq1 * t[:note1_end] * 2 * np.pi) * np.exp(-t[:note1_end] * 8)
        
        # Second note (higher, overlapping slightly)
        freq2 = 800
        note2_start = int(n_samples * 0.3)
        if note2_start < n_samples:
            t2 = t[note2_start:] - t[note2_start]
            wave[note2_start:] += np.sin(freq2 * t2 * 2 * np.pi) * np.exp(-t2 * 6)
        
        # Add some harmonic richness
        wave += 0.3 * np.sin(1200 * t * 2 * np.pi) * np.exp(-t * 10)
        
        # Overall volume
        wave = wave * 0.35
        
        # Convert to 16-bit
        wave = np.clip(wave * 32767, -32767, 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)

class Turtle:
    """A cute chubby pixel art turtle doll"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 24
        self.caught = False
        self.falling = False  # Is the turtle falling?
        self.fall_speed = 0  # Vertical speed when falling
        self.original_y = y  # Remember the original Y position
        self.rect = pygame.Rect(x - self.size, y - self.size, self.size * 2, self.size * 2)
    
    def update(self):
        """Update turtle position if falling"""
        if self.falling:
            self.fall_speed += 0.5  # Gravity
            self.y += self.fall_speed
            
            # Stop falling when reaching original position or below
            if self.y >= self.original_y:
                self.y = self.original_y
                self.falling = False
                self.fall_speed = 0
            
            self.update_rect()
    
    def draw(self, screen):
        # Draw a super round and chubby turtle!
        shell_color = self.color
        darker_shell = tuple(max(0, c - 50) for c in shell_color)
        light_shell = tuple(min(255, c + 30) for c in shell_color)
        
        # Chubby round shell (big circle!)
        pygame.draw.circle(screen, shell_color, (self.x, self.y + 5), self.size)
        pygame.draw.circle(screen, BLACK, (self.x, self.y + 5), self.size, 3)
        
        # Shell pattern - cute hexagonal spots
        # Center large spot
        pygame.draw.circle(screen, darker_shell, (self.x, self.y + 8), 10)
        pygame.draw.circle(screen, BLACK, (self.x, self.y + 8), 10, 2)
        
        # Surrounding smaller spots (arranged in circle)
        spot_positions = [
            (self.x - 12, self.y + 2),
            (self.x + 12, self.y + 2),
            (self.x - 10, self.y + 16),
            (self.x + 10, self.y + 16),
        ]
        for spot_x, spot_y in spot_positions:
            pygame.draw.circle(screen, darker_shell, (spot_x, spot_y), 6)
            pygame.draw.circle(screen, BLACK, (spot_x, spot_y), 6, 1)
        
        # Highlight on shell (makes it look shiny and round)
        pygame.draw.circle(screen, light_shell, (self.x - 6, self.y - 2), 8, 2)
        
        # Chubby head (bigger and rounder!)
        head_color = (180, 230, 180) if shell_color[1] > 150 else (220, 220, 180)
        head_x = self.x
        head_y = self.y - self.size + 8
        pygame.draw.circle(screen, head_color, (head_x, head_y), 14)
        pygame.draw.circle(screen, BLACK, (head_x, head_y), 14, 2)
        
        # HUGE cute eyes (kawaii style!)
        eye_white_size = 6
        # Left eye
        pygame.draw.circle(screen, WHITE, (head_x - 5, head_y), eye_white_size)
        pygame.draw.circle(screen, BLACK, (head_x - 5, head_y), eye_white_size, 2)
        pygame.draw.circle(screen, BLACK, (head_x - 5, head_y + 1), 4)
        pygame.draw.circle(screen, WHITE, (head_x - 4, head_y - 1), 2)  # Sparkle
        
        # Right eye
        pygame.draw.circle(screen, WHITE, (head_x + 5, head_y), eye_white_size)
        pygame.draw.circle(screen, BLACK, (head_x + 5, head_y), eye_white_size, 2)
        pygame.draw.circle(screen, BLACK, (head_x + 5, head_y + 1), 4)
        pygame.draw.circle(screen, WHITE, (head_x + 6, head_y - 1), 2)  # Sparkle
        
        # Blushy cheeks (makes it cuter!)
        blush_color = (255, 150, 150)
        pygame.draw.circle(screen, blush_color, (head_x - 10, head_y + 4), 4)
        pygame.draw.circle(screen, blush_color, (head_x + 10, head_y + 4), 4)
        
        # Tiny smile
        pygame.draw.arc(screen, BLACK, (head_x - 5, head_y + 4, 10, 8), 3.14, 6.28, 2)
        
        # Stubby little legs (short and chubby!)
        leg_color = head_color
        # Front left
        pygame.draw.ellipse(screen, leg_color, (self.x - self.size + 2, self.y + 18, 12, 10))
        pygame.draw.ellipse(screen, BLACK, (self.x - self.size + 2, self.y + 18, 12, 10), 2)
        
        # Front right
        pygame.draw.ellipse(screen, leg_color, (self.x + self.size - 14, self.y + 18, 12, 10))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.size - 14, self.y + 18, 12, 10), 2)
        
        # Back left
        pygame.draw.ellipse(screen, leg_color, (self.x - self.size + 4, self.y + 24, 12, 8))
        pygame.draw.ellipse(screen, BLACK, (self.x - self.size + 4, self.y + 24, 12, 8), 2)
        
        # Back right
        pygame.draw.ellipse(screen, leg_color, (self.x + self.size - 16, self.y + 24, 12, 8))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.size - 16, self.y + 24, 12, 8), 2)
        
        # Tiny stubby tail
        tail_x = self.x
        tail_y = self.y + self.size + 4
        pygame.draw.ellipse(screen, leg_color, (tail_x - 4, tail_y, 8, 6))
        pygame.draw.ellipse(screen, BLACK, (tail_x - 4, tail_y, 8, 6), 2)
    
    def update_rect(self):
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Owl:
    """A cute chubby pixel art owl doll"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 24
        self.caught = False
        self.falling = False
        self.fall_speed = 0
        self.original_y = y
        self.rect = pygame.Rect(x - self.size, y - self.size, self.size * 2, self.size * 2)
    
    def update(self):
        """Update owl position if falling"""
        if self.falling:
            self.fall_speed += 0.5  # Gravity
            self.y += self.fall_speed
            
            # Stop falling when reaching original position or below
            if self.y >= self.original_y:
                self.y = self.original_y
                self.falling = False
                self.fall_speed = 0
            
            self.update_rect()
    
    def draw(self, screen):
        # Draw a super cute, round, chubby owl!
        body_color = self.color
        darker_color = tuple(max(0, c - 40) for c in body_color)
        lighter_color = tuple(min(255, c + 50) for c in body_color)
        
        # Main body - BIG round circle (super chubby!)
        pygame.draw.circle(screen, body_color, (self.x, self.y + 2), 22)
        pygame.draw.circle(screen, BLACK, (self.x, self.y + 2), 22, 3)
        
        # Belly patch (lighter, smaller circle on body)
        pygame.draw.circle(screen, lighter_color, (self.x, self.y + 8), 12)
        pygame.draw.circle(screen, BLACK, (self.x, self.y + 8), 12, 2)
        
        # Head - large overlapping circle (merged with body for round look)
        pygame.draw.circle(screen, body_color, (self.x, self.y - 10), 18)
        pygame.draw.circle(screen, BLACK, (self.x, self.y - 10), 18, 3)
        
        # Cute round ear tufts (small circles instead of triangles)
        # Left tuft
        pygame.draw.circle(screen, darker_color, (self.x - 10, self.y - 22), 5)
        pygame.draw.circle(screen, BLACK, (self.x - 10, self.y - 22), 5, 2)
        
        # Right tuft  
        pygame.draw.circle(screen, darker_color, (self.x + 10, self.y - 22), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y - 22), 5, 2)
        
        # Stubby round wings (small ovals on sides)
        # Left wing
        left_wing_rect = pygame.Rect(self.x - 24, self.y - 2, 10, 16)
        pygame.draw.ellipse(screen, darker_color, left_wing_rect)
        pygame.draw.ellipse(screen, BLACK, left_wing_rect, 2)
        
        # Right wing
        right_wing_rect = pygame.Rect(self.x + 14, self.y - 2, 10, 16)
        pygame.draw.ellipse(screen, darker_color, right_wing_rect)
        pygame.draw.ellipse(screen, BLACK, right_wing_rect, 2)
        
        # HUGE adorable eyes (signature owl feature - make them BIG!)
        # Left eye - white circle
        pygame.draw.circle(screen, WHITE, (self.x - 8, self.y - 12), 9)
        pygame.draw.circle(screen, BLACK, (self.x - 8, self.y - 12), 9, 2)
        # Pupil
        pygame.draw.circle(screen, BLACK, (self.x - 8, self.y - 11), 6)
        # Sparkle
        pygame.draw.circle(screen, WHITE, (self.x - 6, self.y - 13), 2)
        
        # Right eye - white circle
        pygame.draw.circle(screen, WHITE, (self.x + 8, self.y - 12), 9)
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y - 12), 9, 2)
        # Pupil
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y - 11), 6)
        # Sparkle
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y - 13), 2)
        
        # Tiny cute beak (small rounded triangle)
        beak_color = (255, 180, 80)
        beak = [(self.x, self.y - 5), (self.x - 3, self.y - 1), (self.x + 3, self.y - 1)]
        pygame.draw.polygon(screen, beak_color, beak)
        pygame.draw.polygon(screen, BLACK, beak, 2)
        
        # Pink blush cheeks (like the turtle!)
        blush_color = (255, 180, 200)
        # Left cheek
        pygame.draw.circle(screen, blush_color, (self.x - 16, self.y - 8), 4)
        # Right cheek
        pygame.draw.circle(screen, blush_color, (self.x + 16, self.y - 8), 4)
        
        # Tiny round feet at bottom (cute stubby feet)
        feet_color = (255, 200, 120)
        # Left foot
        pygame.draw.circle(screen, feet_color, (self.x - 8, self.y + 22), 4)
        pygame.draw.circle(screen, BLACK, (self.x - 8, self.y + 22), 4, 2)
        
        # Right foot
        pygame.draw.circle(screen, feet_color, (self.x + 8, self.y + 22), 4)
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y + 22), 4, 2)
    
    def update_rect(self):
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Claw:
    """The claw mechanism in pixel art style"""
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = 100
        self.rope_length = 0
        self.max_rope = 370  # Increased to reach all turtles
        self.speed = 3
        self.state = "moving"  # moving, descending, closing, ascending
        self.grabbed_turtle = None
        self.is_closing = False
        self.fall_check_done = False  # Track if we've checked for fall
        self.ascend_frames = 0  # Count frames while ascending
    
    def move_left(self):
        if self.state == "moving" and self.x > 150:
            self.x -= self.speed
    
    def move_right(self):
        if self.state == "moving" and self.x < SCREEN_WIDTH - 150:
            self.x += self.speed
    
    def start_descend(self):
        """Start descending when SPACE is pressed"""
        if self.state == "moving":
            self.state = "descending"
            self.is_closing = False
            return True
        return False
    
    def close_claw(self):
        """Close the claw to grab when SPACE is pressed during descent"""
        if self.state == "descending":
            self.state = "closing"
            self.is_closing = True
            return True
        return False
    
    def update(self):
        if self.state == "descending":
            self.rope_length += 4
            if self.rope_length >= self.max_rope:
                self.rope_length = self.max_rope
                # Auto close if reached bottom
                self.state = "closing"
                self.is_closing = True
        
        elif self.state == "closing":
            # Claw is closing, brief pause then ascend
            self.state = "ascending"
            self.fall_check_done = False  # Reset for new ascent
            self.ascend_frames = 0  # Reset frame counter
        
        elif self.state == "ascending":
            self.rope_length -= 3
            self.ascend_frames += 1  # Count frames while ascending
            
            # Check for fall (60% chance) when halfway up, but after 30 frames delay
            if self.grabbed_turtle and not self.fall_check_done and self.rope_length <= self.max_rope // 2 and self.ascend_frames >= 30:
                self.fall_check_done = True
                if random.random() < 0.6:  # 60% chance to fall
                    # Turtle falls back down!
                    self.grabbed_turtle.caught = False
                    self.grabbed_turtle.falling = True  # Start falling animation
                    self.grabbed_turtle.fall_speed = 0  # Reset fall speed
                    self.grabbed_turtle = None
                    return "fall"  # Signal that turtle fell
            
            if self.rope_length <= 0:
                self.rope_length = 0
                self.state = "moving"
                self.is_closing = False
                self.fall_check_done = False  # Reset for next round
                self.ascend_frames = 0  # Reset frame counter
                if self.grabbed_turtle:
                    return True  # Successfully caught!
                else:
                    return False  # Failed
        
        # Update grabbed turtle position
        if self.grabbed_turtle:
            self.grabbed_turtle.x = self.x
            self.grabbed_turtle.y = self.y + self.rope_length + 30
            self.grabbed_turtle.update_rect()
        
        return None
    
    def get_claw_pos(self):
        return self.x, self.y + self.rope_length
    
    def draw(self, screen):
        # Rope/cable (pixel style - dashed line)
        rope_y = self.y
        while rope_y < self.y + self.rope_length:
            pygame.draw.rect(screen, DARK_GRAY, (self.x - 1, rope_y, 3, 6))
            rope_y += 10
        
        # Claw mechanism top (pixel art box)
        claw_top_y = self.y + self.rope_length
        pygame.draw.rect(screen, GRAY, (self.x - 16, claw_top_y, 32, 12))
        pygame.draw.rect(screen, BLACK, (self.x - 16, claw_top_y, 32, 12), 2)
        pygame.draw.rect(screen, LIGHT_GRAY, (self.x - 14, claw_top_y + 2, 4, 4))
        pygame.draw.rect(screen, LIGHT_GRAY, (self.x + 10, claw_top_y + 2, 4, 4))
        
        # Claw arms (pixel art style) - open when moving/descending, closed when grabbing
        claw_y = claw_top_y + 12
        claw_bottom = claw_top_y + 30
        
        if self.state in ["moving", "descending"] and not self.is_closing:
            # Open claw (wide)
            # Left arm
            pygame.draw.rect(screen, YELLOW, (self.x - 20, claw_y, 6, 18))
            pygame.draw.rect(screen, BLACK, (self.x - 20, claw_y, 6, 18), 1)
            # Right arm
            pygame.draw.rect(screen, YELLOW, (self.x + 14, claw_y, 6, 18))
            pygame.draw.rect(screen, BLACK, (self.x + 14, claw_y, 6, 18), 1)
            # Claw tips
            pygame.draw.rect(screen, GOLD, (self.x - 22, claw_bottom, 8, 6))
            pygame.draw.rect(screen, BLACK, (self.x - 22, claw_bottom, 8, 6), 1)
            pygame.draw.rect(screen, GOLD, (self.x + 14, claw_bottom, 8, 6))
            pygame.draw.rect(screen, BLACK, (self.x + 14, claw_bottom, 8, 6), 1)
        else:
            # Closed claw (narrow) - when closing or ascending
            # Left arm
            pygame.draw.rect(screen, YELLOW, (self.x - 10, claw_y, 6, 18))
            pygame.draw.rect(screen, BLACK, (self.x - 10, claw_y, 6, 18), 1)
            # Right arm
            pygame.draw.rect(screen, YELLOW, (self.x + 4, claw_y, 6, 18))
            pygame.draw.rect(screen, BLACK, (self.x + 4, claw_y, 6, 18), 1)
            # Claw tips
            pygame.draw.rect(screen, GOLD, (self.x - 12, claw_bottom, 8, 6))
            pygame.draw.rect(screen, BLACK, (self.x - 12, claw_bottom, 8, 6), 1)
            pygame.draw.rect(screen, GOLD, (self.x + 4, claw_bottom, 8, 6))
            pygame.draw.rect(screen, BLACK, (self.x + 4, claw_bottom, 8, 6), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 Claw Machine - Pixel Art Edition")
        self.clock = pygame.time.Clock()
        
        self.claw = Claw()
        self.turtles = []
        self.spawn_turtles()
        
        self.coins = 12
        self.score = 0
        self.game_active = False
        self.won_turtles = []
        self.round_over = False
        
        # Timer system
        self.time_limit = 10  # 10 seconds per coin
        self.time_remaining = self.time_limit
        self.timer_frames = 0
        
        # Fonts
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)
        
        # Sound effects
        try:
            self.sounds = {
                'coin': SoundGenerator.coin_sound(),
                'move': SoundGenerator.move_sound(),
                'victory': SoundGenerator.victory_sound(),
                'fall': SoundGenerator.fall_sound(),
                'grab': SoundGenerator.grab_sound()
            }
            self.sound_enabled = True
        except:
            self.sound_enabled = False
            print("Sound generation failed - continuing without sound")
        
        self.running = True
        self.message = "Press ENTER to Insert Coin!"
        self.message_timer = 180
        
        # Play Again button
        self.button_rect = None
    
    def spawn_turtles(self):
        """Spawn cute turtles and owls in the machine"""
        positions = [
            (200, 420), (280, 440), (360, 430), (440, 445), (520, 435), (600, 425),
            (240, 370), (320, 380), (400, 375), (480, 385), (560, 370),
            (280, 320), (380, 325), (480, 320)
        ]
        
        self.turtles = []
        for pos in positions:
            # Randomly choose between turtle and owl (50/50 chance)
            if random.random() < 0.5:
                color = random.choice(TURTLE_COLORS)
                self.turtles.append(Turtle(pos[0], pos[1], color))
            else:
                color = random.choice(OWL_COLORS)
                self.turtles.append(Owl(pos[0], pos[1], color))
    
    def insert_coin(self):
        """Insert a coin to start the game"""
        if self.coins > 0 and not self.game_active and not self.round_over:
            self.coins -= 1
            self.game_active = True
            self.claw.state = "moving"
            self.time_remaining = self.time_limit
            self.timer_frames = 0
            self.message = "Move: ←→ | SPACE: Drop & Close Claw!"
            self.message_timer = 120
            
            # Play coin sound
            if self.sound_enabled:
                self.sounds['coin'].play()

    
    def start_new_round(self):
        """Start a new round with 12 fresh coins"""
        self.coins = 12
        self.score = 0
        self.won_turtles = []
        self.round_over = False
        self.game_active = False
        self.spawn_turtles()
        self.claw = Claw()
        self.message = "New Round! Press ENTER to Insert Coin!"
        self.message_timer = 120
    
    def check_grab(self):
        """Check if claw grabbed a turtle when it closes"""
        if self.claw.is_closing and not self.claw.grabbed_turtle:
            claw_x, claw_y = self.claw.get_claw_pos()
            
            # Claw grab area (pixel perfect)
            claw_rect = pygame.Rect(claw_x - 15, claw_y + 25, 30, 15)
            
            for turtle in self.turtles:
                if claw_rect.colliderect(turtle.rect) and not turtle.caught:
                    # Grabbed!
                    turtle.caught = True
                    self.claw.grabbed_turtle = turtle
                    self.message = "Got a Turtle! 🐢"
                    self.message_timer = 60
                    break
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.round_over:
                        # Start new round
                        self.start_new_round()
                    else:
                        # Insert coin
                        self.insert_coin()
                if event.key == pygame.K_SPACE and self.game_active:
                    if self.claw.state == "moving":
                        # First press: start descending
                        self.claw.start_descend()
                        self.message = "Press SPACE again to close!"
                        self.message_timer = 60
                    elif self.claw.state == "descending":
                        # Second press: close the claw
                        self.claw.close_claw()
                        self.check_grab()  # Check immediately when closing
            
            # Mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if clicked on Play Again button
                    if self.round_over and self.button_rect:
                        if self.button_rect.collidepoint(mouse_pos):
                            self.start_new_round()
    
    def update(self):
        if self.game_active:
            # Update timer
            self.timer_frames += 1
            if self.timer_frames >= FPS:
                self.timer_frames = 0
                self.time_remaining -= 1
                
                if self.time_remaining <= 0:
                    # Time's up!
                    self.game_active = False
                    self.claw.state = "moving"
                    self.claw.rope_length = 0
                    if self.claw.grabbed_turtle:
                        self.claw.grabbed_turtle.caught = False
                        self.claw.grabbed_turtle = None
                    self.message = "Time's Up! Press ENTER"
                    self.message_timer = 120
            
            # Handle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.claw.move_left()
                if self.sound_enabled and self.claw.state == "moving":
                    self.sounds['move'].play()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.claw.move_right()
                if self.sound_enabled and self.claw.state == "moving":
                    self.sounds['move'].play()
            
            # Update claw
            result = self.claw.update()
            
            if result == True:
                # Successfully caught a turtle!
                self.score += 1
                self.won_turtles.append(self.claw.grabbed_turtle)
                self.turtles.remove(self.claw.grabbed_turtle)
                self.claw.grabbed_turtle = None
                
                # Play grab sound
                if self.sound_enabled:
                    self.sounds['grab'].play()
                
                # Show success message
                self.message = f"🎉🎊 SUCCESS! Score: {self.score}"
                self.message_timer = 120
                self.game_active = False
            elif result == False:
                # Failed to catch anything
                self.game_active = False
                self.message = "Try Again! Press ENTER"
                self.message_timer = 120
            elif result == "fall":
                # Turtle fell - play fall sound
                if self.sound_enabled:
                    self.sounds['fall'].play()
            
            # Check if round is over (all coins used)
            if not self.game_active and self.coins == 0 and not self.round_over:
                self.round_over = True
                if self.score >= 5:
                    self.message = f"🏆 YOU WON! {self.score} dolls!"
                    # Play victory sound for round win
                    if self.sound_enabled:
                        self.sounds['victory'].play()
                else:
                    self.message = f"Round Over! You caught {self.score} dolls!"
                self.message_timer = 300
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def draw(self):
        # Background
        self.screen.fill(BLUE)
        
        # Draw pixel art checkerboard floor
        for i in range(0, SCREEN_WIDTH, 40):
            for j in range(SCREEN_HEIGHT - 80, SCREEN_HEIGHT, 40):
                if (i + j) % 80 == 0:
                    pygame.draw.rect(self.screen, DARK_BROWN, (i, j, 40, 40))
                else:
                    pygame.draw.rect(self.screen, BROWN, (i, j, 40, 40))
        
        # Machine cabinet (pixel art style)
        # Outer frame
        pygame.draw.rect(self.screen, DARK_BROWN, (100, 80, 600, 440))
        pygame.draw.rect(self.screen, BLACK, (100, 80, 600, 440), 4)
        
        # Inner play area
        pygame.draw.rect(self.screen, LIGHT_BLUE, (120, 100, 560, 380))
        pygame.draw.rect(self.screen, BLACK, (120, 100, 560, 380), 3)
        
        # Glass reflection effect (pixel art style)
        pygame.draw.rect(self.screen, WHITE, (130, 110, 80, 100), 2)
        pygame.draw.rect(self.screen, WHITE, (600, 150, 60, 80), 1)
        
        # Prize chute/door at bottom
        pygame.draw.rect(self.screen, DARK_GRAY, (320, 460, 160, 40))
        pygame.draw.rect(self.screen, BLACK, (320, 460, 160, 40), 3)
        pygame.draw.rect(self.screen, GRAY, (340, 470, 120, 20))
        
        # Draw turtles
        for turtle in self.turtles:
            turtle.update()  # Update falling animation
            turtle.draw(self.screen)
        
        # Draw claw
        self.claw.draw(self.screen)
        
        # Draw coin slot (pixel art)
        coin_slot_x = 20
        coin_slot_y = 20
        pygame.draw.rect(self.screen, DARK_GRAY, (coin_slot_x, coin_slot_y, 160, 100))
        pygame.draw.rect(self.screen, BLACK, (coin_slot_x, coin_slot_y, 160, 100), 3)
        pygame.draw.rect(self.screen, BLACK, (coin_slot_x + 40, coin_slot_y + 20, 80, 8))
        
        # Coin display
        coin_text = self.small_font.render(f"Coins: {self.coins}", True, GOLD)
        self.screen.blit(coin_text, (coin_slot_x + 20, coin_slot_y + 40))
        
        # Draw coin icons
        for i in range(min(self.coins, 5)):
            coin_x = coin_slot_x + 20 + (i * 25)
            coin_y = coin_slot_y + 75
            pygame.draw.circle(self.screen, GOLD, (coin_x, coin_y), 8)
            pygame.draw.circle(self.screen, ORANGE, (coin_x, coin_y), 6)
            pygame.draw.circle(self.screen, BLACK, (coin_x, coin_y), 8, 2)
        
        # Score display (pixel art panel)
        pygame.draw.rect(self.screen, DARK_GRAY, (SCREEN_WIDTH - 180, 20, 160, 80))
        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH - 180, 20, 160, 80), 3)
        score_text = self.small_font.render(f"Score: {self.score}", True, GREEN)
        self.screen.blit(score_text, (SCREEN_WIDTH - 160, 50))
        
        # Timer display (when game is active)
        if self.game_active:
            # Determine timer color based on time remaining
            if self.time_remaining > 10:
                timer_color = WHITE
            elif self.time_remaining > 5:
                timer_color = ORANGE
            else:
                timer_color = RED
            
            # Timer panel
            pygame.draw.rect(self.screen, DARK_GRAY, (SCREEN_WIDTH // 2 - 80, 120, 160, 50))
            pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH // 2 - 80, 120, 160, 50), 3)
            
            # Timer text
            timer_text = self.small_font.render(f"Time: {self.time_remaining}s", True, timer_color)
            timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 145))
            self.screen.blit(timer_text, timer_rect)
        
        # Draw message
        if self.message_timer > 0:
            message_surface = self.font.render(self.message, True, YELLOW)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))
            # Pixel art shadow
            shadow_surface = self.font.render(self.message, True, BLACK)
            shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 2, 42))
            self.screen.blit(shadow_surface, shadow_rect)
            self.screen.blit(message_surface, message_rect)
        
        # Instructions at bottom
        if not self.game_active and self.coins > 0 and not self.round_over:
            instruction = self.tiny_font.render("Press ENTER to Insert Coin", True, WHITE)
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 30))
        elif self.game_active and self.claw.state == "moving":
            instruction = self.tiny_font.render("← → to Move | SPACE to Drop Claw", True, WHITE)
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 30))
        elif self.game_active and self.claw.state == "descending":
            instruction = self.tiny_font.render("SPACE to Close Claw and Grab!", True, YELLOW)
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT - 30))
        elif self.round_over:
            # Draw "Play Again" button
            button_width = 200
            button_height = 60
            button_x = SCREEN_WIDTH // 2 - button_width // 2
            button_y = SCREEN_HEIGHT // 2 + 80
            
            # Store button rect for click detection
            self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            # Check if mouse is hovering over button
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = self.button_rect.collidepoint(mouse_pos)
            
            # Button background (lighter when hovering)
            button_color = (120, 230, 120) if is_hovering else GREEN
            pygame.draw.rect(self.screen, button_color, self.button_rect)
            pygame.draw.rect(self.screen, BLACK, self.button_rect, 4)
            
            # Button highlight
            pygame.draw.rect(self.screen, WHITE, (button_x + 5, button_y + 5, button_width - 10, 8))
            
            # Button text
            play_again_text = self.small_font.render("PLAY AGAIN", True, WHITE)
            text_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, button_y + 30))
            self.screen.blit(play_again_text, text_rect)
            
            # Instruction
            instruction = self.tiny_font.render("Click to Play Again", True, WHITE)
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - 80, button_y + button_height + 20))
            
            # Round over message
            if self.score >= 5:
                # Player won!
                game_over = self.font.render("🏆 YOU WON! 🏆", True, GOLD)
                self.screen.blit(game_over, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 60))
                final_score = self.small_font.render(f"Amazing! You caught {self.score} dolls!", True, YELLOW)
                self.screen.blit(final_score, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 10))
            else:
                # Round over, didn't win
                game_over = self.font.render("ROUND OVER!", True, YELLOW)
                self.screen.blit(game_over, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 60))
                final_score = self.small_font.render(f"You caught {self.score} dolls!", True, WHITE)
                self.screen.blit(final_score, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 10))
                need_more = self.tiny_font.render("(Need 5 or more to win)", True, RED)
                self.screen.blit(need_more, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
