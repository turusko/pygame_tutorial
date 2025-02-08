import pygame

class HealthBar:
    def __init__(self, x, y, hp, max_health):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_health = max_health

    def draw(self, screen):
        # Draw health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 50 * (self.hp / self.max_health), 10))
