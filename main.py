import pygame
from obj.fighter import Fighter

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

pygame.display.set_caption("Battle Game")

background = pygame.image.load("img/Background/background.png")

panel_img = pygame.image.load("img/Icons/panel.png")


class HealthBar:
    def __init__(self, x, y, hp, max_health):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_health = max_health

    def draw(self, screen):
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
    knight_health_bar.draw(screen)
    draw_text(f"{bandit1.name} HP: {bandit1.hp}", font, red, 500, screen_height - bottom_panel + 10)
    bandit1_health_bar.draw(screen)
    draw_text(f"{bandit2.name} HP: {bandit2.hp}", font, red, 500, screen_height - bottom_panel + 60)
    bandit2_health_bar.draw(screen)

    


        
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            

    pygame.display.update()

pygame.quit()