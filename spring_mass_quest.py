import pygame
import numpy as np
import math
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

class GameState(Enum):
    HOME = 1
    LEVEL_1 = 2
    LEVEL_2 = 3
    LEVEL_3 = 4
    LEVEL_4 = 5
    LEVEL_COMPLETE = 6

class SpringMassSystem:
    def __init__(self, mass=1.0, damping=0.1, spring_constant=10.0, force=0.0):
        self.mass = mass
        self.damping = damping
        self.spring_constant = spring_constant
        self.force = force
        
        # Initial conditions
        self.x = 0.0  # Position
        self.v = 0.0  # Velocity
        self.a = 0.0  # Acceleration
        
        # Simulation parameters
        self.dt = 1.0 / FPS
        self.time = 0.0
        
        # Visual parameters
        self.equilibrium_x = SCREEN_WIDTH // 2
        self.max_displacement = 200
        
    def update(self):
        # Spring-mass-damping equation: M(d2x/dt2) + b(dx/dt) + kx = F(t)
        # Solving for acceleration: a = (F - b*v - k*x) / M
        self.a = (self.force - self.damping * self.v - self.spring_constant * self.x) / self.mass
        
        # Update velocity and position using Euler integration
        self.v += self.a * self.dt
        self.x += self.v * self.dt
        
        self.time += self.dt
        
    def reset(self):
        self.x = 0.0
        self.v = 0.0
        self.a = 0.0
        self.time = 0.0
        
    def get_visual_x(self):
        return self.equilibrium_x + self.x * 2  # Scale for visibility
        
    def get_spring_energy(self):
        return 0.5 * self.spring_constant * self.x**2
        
    def get_kinetic_energy(self):
        return 0.5 * self.mass * self.v**2
        
    def get_total_energy(self):
        return self.get_spring_energy() + self.get_kinetic_energy()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Spring Mass Quest")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.state = GameState.HOME
        self.current_level = 1
        self.level_complete = False
        
        # Spring-mass system
        self.system = SpringMassSystem()
        
        # Level objectives
        self.level_objectives = {
            1: {"target_height": 50, "description": "Adjust mass and damping to make the system jump higher!"},
            2: {"case_study": "Earthquake simulation", "description": "Set parameters to minimize building oscillation"},
            3: {"case_study": "Car suspension", "description": "Optimize for smooth ride over bumpy road"},
            4: {"case_study": "Bridge resonance", "description": "Calculate spring energy to prevent catastrophic failure"}
        }
        
        # Level completion criteria
        self.level_criteria = {
            1: lambda: abs(self.system.x) > 40 and self.system.v > 0,
            2: lambda: abs(self.system.x) < 10 and abs(self.system.v) < 5,
            3: lambda: abs(self.system.x) < 15 and abs(self.system.v) < 8,
            4: lambda: self.system.get_spring_energy() > 1000
        }
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state != GameState.HOME:
                        self.state = GameState.HOME
                    else:
                        return False
                elif event.key == pygame.K_SPACE and self.state == GameState.HOME:
                    self.start_level(1)
                elif event.key == pygame.K_r:
                    self.system.reset()
                elif event.key == pygame.K_n and self.level_complete:
                    self.next_level()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.HOME:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 500 <= mouse_x <= 700 and 400 <= mouse_y <= 450:
                        self.start_level(1)
        return True
    
    def start_level(self, level):
        self.current_level = level
        self.state = GameState(level + 1)
        self.level_complete = False
        self.system.reset()
        
        # Set level-specific parameters
        if level == 1:
            self.system.mass = 1.0
            self.system.damping = 0.1
            self.system.spring_constant = 10.0
            self.system.force = 50.0
        elif level == 2:
            self.system.mass = 2.0
            self.system.damping = 0.5
            self.system.spring_constant = 15.0
            self.system.force = 30.0
        elif level == 3:
            self.system.mass = 1.5
            self.system.damping = 0.3
            self.system.spring_constant = 20.0
            self.system.force = 40.0
        elif level == 4:
            self.system.mass = 3.0
            self.system.damping = 0.2
            self.system.spring_constant = 25.0
            self.system.force = 100.0
    
    def next_level(self):
        if self.current_level < 4:
            self.start_level(self.current_level + 1)
        else:
            self.state = GameState.HOME
            self.current_level = 1
    
    def adjust_parameters(self):
        keys = pygame.key.get_pressed()
        
        # Mass adjustment
        if keys[pygame.K_q]:
            self.system.mass = max(0.1, self.system.mass - 0.1)
        if keys[pygame.K_w]:
            self.system.mass = min(10.0, self.system.mass + 0.1)
            
        # Damping adjustment
        if keys[pygame.K_a]:
            self.system.damping = max(0.0, self.system.damping - 0.01)
        if keys[pygame.K_s]:
            self.system.damping = min(2.0, self.system.damping + 0.01)
            
        # Spring constant adjustment
        if keys[pygame.K_z]:
            self.system.spring_constant = max(1.0, self.system.spring_constant - 0.5)
        if keys[pygame.K_x]:
            self.system.spring_constant = min(50.0, self.system.spring_constant + 0.5)
            
        # Force adjustment
        if keys[pygame.K_e]:
            self.system.force = max(0.0, self.system.force - 1.0)
        if keys[pygame.K_r]:
            self.system.force = min(200.0, self.system.force + 1.0)
    
    def check_level_completion(self):
        if self.current_level in self.level_criteria:
            if self.level_criteria[self.current_level]():
                self.level_complete = True
                self.state = GameState.LEVEL_COMPLETE
    
    def draw_home(self):
        self.screen.fill(LIGHT_BLUE)
        
        # Title
        title = self.font.render("Spring Mass Quest", True, DARK_BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.small_font.render("Master the Physics of Spring-Mass-Damping Systems", True, DARK_BLUE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Level descriptions
        y_offset = 300
        for i in range(1, 5):
            level_text = f"Level {i}: {self.get_level_description(i)}"
            level_surface = self.small_font.render(level_text, True, BLACK)
            self.screen.blit(level_surface, (50, y_offset))
            y_offset += 30
        
        # Start button
        pygame.draw.rect(self.screen, GREEN, (500, 400, 200, 50))
        start_text = self.font.render("START", True, WHITE)
        start_rect = start_text.get_rect(center=(600, 425))
        self.screen.blit(start_text, start_rect)
        
        # Instructions
        instructions = [
            "Press SPACE or click START to begin",
            "Press ESC to return to home",
            "Use Q/W, A/S, Z/X, E/R to adjust parameters"
        ]
        y_offset = 500
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, BLACK)
            self.screen.blit(inst_surface, (50, y_offset))
            y_offset += 25
    
    def get_level_description(self, level):
        descriptions = {
            1: "Basic parameter adjustment",
            2: "Case study: Earthquake simulation",
            3: "Advanced: Car suspension",
            4: "Master: Bridge resonance + Energy calculation"
        }
        return descriptions.get(level, "")
    
    def draw_simulation(self):
        self.screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT//2 + 100), (SCREEN_WIDTH, SCREEN_HEIGHT//2 + 100), 3)
        
        # Draw spring
        spring_x = self.system.equilibrium_x
        mass_x = self.system.get_visual_x()
        spring_y = SCREEN_HEIGHT//2 + 50
        
        # Draw spring coils
        spring_length = abs(mass_x - spring_x)
        if spring_length > 0:
            coils = max(3, int(spring_length // 20))
            for i in range(coils):
                coil_x = spring_x + (mass_x - spring_x) * i / coils
                coil_y = spring_y + 10 * math.sin(i * math.pi / 2)
                pygame.draw.circle(self.screen, GRAY, (int(coil_x), int(coil_y)), 3)
        
        # Draw mass
        pygame.draw.rect(self.screen, BLUE, (mass_x - 25, spring_y - 25, 50, 50))
        pygame.draw.rect(self.screen, BLACK, (mass_x - 25, spring_y - 25, 50, 50), 2)
        
        # Draw equilibrium position
        pygame.draw.line(self.screen, RED, (self.system.equilibrium_x, spring_y - 30), (self.system.equilibrium_x, spring_y + 30), 2)
        
        # Draw level info
        level_text = f"Level {self.current_level}"
        level_surface = self.font.render(level_text, True, BLACK)
        self.screen.blit(level_surface, (50, 50))
        
        # Draw objective
        objective = self.level_objectives[self.current_level]["description"]
        obj_surface = self.small_font.render(objective, True, BLACK)
        self.screen.blit(obj_surface, (50, 90))
        
        # Draw parameters
        param_y = 150
        params = [
            f"Mass (Q/W): {self.system.mass:.2f}",
            f"Damping (A/S): {self.system.damping:.2f}",
            f"Spring Constant (Z/X): {self.system.spring_constant:.2f}",
            f"Force (E/R): {self.system.force:.2f}"
        ]
        for param in params:
            param_surface = self.small_font.render(param, True, BLACK)
            self.screen.blit(param_surface, (50, param_y))
            param_y += 25
        
        # Draw system state
        state_y = 300
        state_info = [
            f"Position: {self.system.x:.2f}",
            f"Velocity: {self.system.v:.2f}",
            f"Acceleration: {self.system.a:.2f}",
            f"Spring Energy: {self.system.get_spring_energy():.2f}",
            f"Kinetic Energy: {self.system.get_kinetic_energy():.2f}",
            f"Total Energy: {self.system.get_total_energy():.2f}"
        ]
        for info in state_info:
            info_surface = self.small_font.render(info, True, BLACK)
            self.screen.blit(info_surface, (50, state_y))
            state_y += 25
        
        # Draw controls
        controls = [
            "Controls:",
            "Q/W - Mass",
            "A/S - Damping", 
            "Z/X - Spring Constant",
            "E/R - Force",
            "R - Reset",
            "ESC - Home"
        ]
        control_y = 500
        for control in controls:
            control_surface = self.small_font.render(control, True, GRAY)
            self.screen.blit(control_surface, (50, control_y))
            control_y += 20
    
    def draw_level_complete(self):
        self.screen.fill(GREEN)
        
        complete_text = self.font.render(f"Level {self.current_level} Complete!", True, WHITE)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(complete_text, complete_rect)
        
        if self.current_level < 4:
            next_text = self.small_font.render("Press N for next level", True, WHITE)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH//2, 350))
            self.screen.blit(next_text, next_rect)
        else:
            final_text = self.small_font.render("Congratulations! You've mastered Spring Mass Quest!", True, WHITE)
            final_rect = final_text.get_rect(center=(SCREEN_WIDTH//2, 350))
            self.screen.blit(final_text, final_rect)
        
        home_text = self.small_font.render("Press ESC to return home", True, WHITE)
        home_rect = home_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(home_text, home_rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if self.state != GameState.HOME and self.state != GameState.LEVEL_COMPLETE:
                self.adjust_parameters()
                self.system.update()
                self.check_level_completion()
            
            # Draw current state
            if self.state == GameState.HOME:
                self.draw_home()
            elif self.state == GameState.LEVEL_COMPLETE:
                self.draw_level_complete()
            else:
                self.draw_simulation()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()