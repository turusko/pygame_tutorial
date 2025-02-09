import pygame
import os
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont("Times New Roman", 26)

red = (255, 0, 0)
green = (0, 255, 0)

current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90

pygame.display.set_caption("Battle Game")

background = pygame.image.load("img/Background/background.png")

panel_img = pygame.image.load("img/Icons/panel.png")

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
    
    def update_action(self, new_action):
        self.action = self.animation_list_types.index(new_action)

    def update(self):
        animation_cooldown = 100
        
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.update_action("Idle")

    def attack(self, enemy):
        damage = self.strength + random.randint(-5, 5)
        enemy.hp -= damage
        self.update_action("Attack")
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class HealthBar:
    def __init__(self, x, y, hp, max_health):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_health = max_health

    def draw(self, screen, hp):
        self.hp = hp
        # Draw health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 150 * (self.hp / self.max_health), 20))


def draw_text(text, font, text_col, x, y, ):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(background, (0, 0))

def draw_pannel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    draw_text(f"{knight.name} HP: {knight.hp}", font, red, 100, screen_height - bottom_panel + 10)
    knight_health_bar.draw(screen, knight.hp)
    draw_text(f"{bandit1.name} HP: {bandit1.hp}", font, red, 500, screen_height - bottom_panel + 10)
    bandit1_health_bar.draw(screen, bandit1.hp)
    draw_text(f"{bandit2.name} HP: {bandit2.hp}", font, red, 500, screen_height - bottom_panel + 60)
    bandit2_health_bar.draw(screen, bandit2.hp)

        
knight = Fighter(200, 260, "Knight", 30, 10, 3)
bandit1 = Fighter(550, 270, "Bandit", 20, 6, 1)
bandit2 = Fighter(700, 270, "Bandit", 20, 6, 1)

bandit2_health_bar = HealthBar(600, screen_height - bottom_panel - 20, bandit2.hp, bandit2.max_hp)

bandit_list = [bandit1, bandit2]

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40 , knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(500, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(500, screen_height - bottom_panel + 90, bandit2.hp, bandit2.max_hp)



run = True

while run:
    
    clock.tick(fps)
    

    draw_bg()
    draw_pannel()
    knight.update()
    knight.draw(screen)

    for bandit in bandit_list: 
        bandit.update()
        bandit.draw(screen)

    if knight.alive:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                knight.attack(bandit1)
                current_fighter += 1
                action_cooldown = 0

    for count, bandit in enumerate(bandit_list):
        if bandit.alive:
            if current_fighter == count + 2:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    bandit.attack(knight)
                    current_fighter += 1
                    action_cooldown = 0
        else:
            current_fighter += 1
    if current_fighter > total_fighters:
        current_fighter = 1
           

        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            

    pygame.display.update()

pygame.quit()