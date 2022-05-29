import pygame

pygame.init()

X = 960
Y = 640

display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Advanced Pygame Tutorial")

FPS = 60
clock = pygame.time.Clock()

is_running = True
while is_running:
    for event in pygame.event.get()
        if event.type == pygame.QUIT:
            is_running = False

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()