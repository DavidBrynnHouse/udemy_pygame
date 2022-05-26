import pygame

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hello, World!")

VELOCITY = 10
FPS = 60
clock = pygame.time.Clock()

dragon_image = pygame.image.load('basic_tutorial_assets/dragon_right.png')
dragon_rect = dragon_image.get_rect()
dragon_rect.topleft = (0, 64)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_UP] and dragon_rect.top > 64:
        dragon_rect.y -= VELOCITY
    if keys[pygame.K_DOWN] and dragon_rect.bottom < WINDOW_HEIGHT:
        dragon_rect.y += VELOCITY

    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()