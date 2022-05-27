import pygame
from monster import Monster

pygame.init()

X = 700
Y = 600
display_surface = pygame.display.set_mode((X, Y))

my_monster_group = pygame.sprite.Group()
for i in range(4):
    monster = Monster("blue", 10)
    my_monster_group.add(monster)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill((0, 0, 0))

    my_monster_group.update()
    my_monster_group.draw(display_surface)

    pygame.display.update()
pygame.quit()