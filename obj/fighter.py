import pygame
import os
from .health_bars import HealthBar


class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.frame_index = 0
        self.action = 0

        self.update_time = pygame.time.get_ticks()
        self.animation_list_types = ["Idle", "Attack", "Hurt", "Death"]
        self.animation_list = self.load_animation()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def load_animation(self):
        scale_image_amount = 3
        temp_master_list = []
        for animation_type in self.animation_list_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.name}/{animation_type}"))

            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.name}/{animation_type}/{i}.png")
                img = pygame.transform.scale(img, (img.get_width()*scale_image_amount,
                                                    img.get_height()*scale_image_amount))
                temp_list.append(img)
            temp_master_list.append(temp_list)
        return temp_master_list

    def update(self, action="Idle"):
        animation_cooldown = 100
        self.action = self.animation_list_types.index(action)
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
