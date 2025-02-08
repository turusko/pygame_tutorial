import pygame
from obj.fighter import Fighter

pygame.init()

clock = pygame.time.Clock()
fps = 60

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Battle Game")

background = pygame.image.load("img/Background/background.png")

panel_img = pygame.image.load("img/Icons/panel.png")

def draw_bg():
    screen.blit(background, (0, 0))

def draw_pannel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))


knight = Fighter(200, 260, "Knight", 30, 10, 3)
bandit1 = Fighter(550, 270, "Bandit", 20, 6, 1)
bandit2 = Fighter(700, 270, "Bandit", 20, 6, 1)

bandit_list = [bandit1, bandit2]



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