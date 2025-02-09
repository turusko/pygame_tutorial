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
action_wait_time = 60
attack = False
portion = False
potion_effect = 15
clicked = False
game_over = 0

sword_strike_sound = pygame.mixer.Sound("sounds/sword_strike.wav")
hurt_sound_list = [pygame.mixer.Sound(f"sounds/hurt/hurt{i}.ogg") for i in range(len(os.listdir("sounds/hurt")))]
death_sound = pygame.mixer.Sound("sounds/death/death_cry.wav")
health_sound = pygame.mixer.Sound("sounds/health_potion.wav")
background_music = pygame.mixer.Sound("sounds/background.wav")
pygame.display.set_caption("Battle Game")

background_music.play(-1)

background = pygame.image.load("img/Background/background.png")

panel_img = pygame.image.load("img/Icons/panel.png")
victory_img = pygame.image.load("img/Icons/victory.png")
defeat_img = pygame.image.load("img/Icons/defeat.png")
sword_img = pygame.image.load("img/Icons/sword.png").convert_alpha()
button_img = pygame.image.load("img/Icons/potion.png").convert_alpha()

class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

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

        if not self.alive and self.frame_index >= len(self.animation_list[self.action]) - 1:
            return
        
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]) and self.alive:
            self.frame_index = 0
            self.update_action("Idle")


    def attack(self, enemy):
        if not enemy.alive:
            return False

        damage = self.strength + random.randint(-5, 5)
        sword_strike_sound.play()
        enemy.hp -= damage
        if enemy.hp < 1:
            enemy.hp = 0
            enemy.alive = False
        self.update_action("Attack")
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        enemy.frame_index = 0
        if enemy.alive:
            random.choice(hurt_sound_list).play()
            enemy.update_action("Hurt")
        else:
            death_sound.play()
            enemy.update_action("Death")
        damage_text = DamageText(enemy.rect.centerx, enemy.rect.y-5, str(damage), red)
        damage_text_group.add(damage_text)
        return True



    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def heal(self, amount):
        health_sound.play()
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        damage_text = DamageText(self.rect.centerx, self.rect.y-5, str(amount), green)
        damage_text_group.add(damage_text)    
        self.potions -= 1   


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

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        
    def update (self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()


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

        
knight = Fighter(200, 260, "Knight", 30, 11, 3)
bandit1 = Fighter(550, 270, "Bandit", 20, 6, 1)
bandit2 = Fighter(700, 270, "Bandit", 20, 6, 2)


bandit_list = [bandit1, bandit2]



potion_button = Button(screen, 100, screen_height - bottom_panel + 80, button_img, 50, 50)

run = True

while run:
    alive_bandits = 0
    attack = False
    portion = False
    target = None


    knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40 , knight.hp, knight.max_hp)
    bandit1_health_bar = HealthBar(500, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
    bandit2_health_bar = HealthBar(500, screen_height - bottom_panel + 90, bandit2.hp, bandit2.max_hp)
    
    clock.tick(fps)
    
    draw_bg()
    draw_pannel()

    

    knight.update()
    knight.draw(screen)

    for bandit in bandit_list: 
        bandit.update()
        bandit.draw(screen)


    damage_text_group.update()
    damage_text_group.draw(screen)

    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()

    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos) and bandit.alive:
            pygame.mouse.set_visible(False)
            screen.blit(sword_img, pos)
            if clicked:
                attack = True
                target = bandit_list[count]

 
    
    if potion_button.draw():
         portion = True
    
    draw_text(f'{knight.potions}' if knight.potions > 0 else '0',
              pygame.font.SysFont("Times New Roman", 18), 
              green if knight.potions > 0 else red, 
              135, 
              screen_height - bottom_panel + 80)

    if knight.alive:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                if attack and target != None:
                    if knight.attack(target):
                        current_fighter += 1
                        action_cooldown = 0
                if portion:
                    if knight.potions > 0:
                        knight.heal(potion_effect)
                        current_fighter += 1
                        action_cooldown = 0
    else: 
        game_over = -1


    for count, action_bandit in enumerate(bandit_list):
        if current_fighter == 2 + count:
            if bandit_list[count].alive:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    if action_bandit.hp < action_bandit.max_hp/2 and action_bandit.potions > 0:
                        action_bandit.heal(potion_effect)                 
                        current_fighter += 1
                        action_cooldown = 0
                    else:                        
                        bandit_list[count].attack(knight)
                        current_fighter += 1
                        action_cooldown = 0
            else:
                current_fighter += 1

    if current_fighter > total_fighters:
        current_fighter = 1

    for bandit in bandit_list:
        if bandit.alive:
            alive_bandits += 1

    if alive_bandits == 0:
        game_over = 1

    if game_over == 1:
        screen.blit(victory_img, (250, 100))
        draw_text("Press R to Restart", font, green, 275, 175)
    if game_over == -1:
        screen.blit(defeat_img, (275, 100))
        draw_text("Press R to Restart", font, green, 275, 175)
        
           
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over != 0:
                for i in bandit_list:
                    i.heal(i.max_hp)
                    i.alive = True
                    i.potions = i.start_potions

                knight.heal(knight.max_hp)
                knight.potions = knight.start_potions
                knight.alive = True
                game_over = 0

            if event.key == pygame.K_ESCAPE:
                run = False


    pygame.display.update()

pygame.quit()