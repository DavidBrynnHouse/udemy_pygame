import pygame
import random
from pygame import mixer

pygame.init()

mixer.init()
coin_sound = mixer.Sound('feed_the_dragon_assets/coin_sound.wav')
miss_sound = mixer.Sound('feed_the_dragon_assets/miss_sound.wav')
mixer.music.load('feed_the_dragon_assets/ftd_background_music.wav')
mixer.music.play()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hello, World!")
clock = pygame.time.Clock()

VELOCITY = 10
FPS = 60

score = 0
lives = 4
velocity_multiplier = 1

dragon_image = pygame.image.load('feed_the_dragon_assets/dragon_right.png')
dragon_rect = dragon_image.get_rect()
dragon_rect.topleft = (0, 64)

coin_image = pygame.image.load('feed_the_dragon_assets/coin.png')
coin_rect = coin_image.get_rect()
coin_rect.topleft = (WINDOW_WIDTH, random.randint(64, WINDOW_HEIGHT - 64))

font = pygame.font.Font('feed_the_dragon_assets/AttackGraffiti.ttf', 32)
scoreText = font.render(f'Score: {score}', True, green, blue)
scoreRect = scoreText.get_rect()
scoreRect.topleft = (10, 10)

livesText = font.render(f'Lives: {lives}', True, green, blue)
livesRect = livesText.get_rect()
livesRect.topleft = (WINDOW_WIDTH - livesRect.width, 10)

gameOverText = font.render(f'Game Over', True, green, blue)
gameOverRect = gameOverText.get_rect()
gameOverRect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continueText = font.render(f'Press any key to start over', True, green, blue)
continueRect = continueText.get_rect()
continueRect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + gameOverRect.height)

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
    
    coin_rect.x -= VELOCITY * velocity_multiplier
    
    if dragon_rect.colliderect(coin_rect):
        coin_rect.topleft = (WINDOW_WIDTH, random.randint(64, WINDOW_HEIGHT - 64))
        velocity_multiplier += .1
        score += 1
        mixer.Sound.play(coin_sound)
    
    if coin_rect.left <= 0:
        coin_rect.topleft = (WINDOW_WIDTH, random.randint(64, WINDOW_HEIGHT - 64))
        lives -= 1
        mixer.Sound.play(miss_sound)
        
    if lives == 0:
        isPaused = True
        while isPaused:
            gameOverText = font.render(f'Game Over', True, green, blue)
            continueText = font.render(f'Press any key to start over', True, green, blue)
            
            display_surface.blit(gameOverText, gameOverRect)
            display_surface.blit(continueText, continueRect)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isPaused = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    mixer.music.play()
                    isPaused = False
                    score = 0
                    lives = 4
                    velocity_multiplier = 1
                    coin_rect.topleft = (WINDOW_WIDTH, random.randint(64, WINDOW_HEIGHT - 64))
                    dragon_rect.topleft = (0, 64)
                    
        
    display_surface.fill((0,0,0))
    
    scoreText = font.render(f'Score: {score}', True, green, blue)
    livesText = font.render(f'Lives: {lives}', True, green, blue)
    
    
    display_surface.blit(scoreText, scoreRect)
    display_surface.blit(livesText, livesRect)
    
    pygame.draw.line(display_surface, (255, 255, 255), (0, 64), (WINDOW_WIDTH, 64), 5)
    
    display_surface.blit(dragon_image, dragon_rect)
    display_surface.blit(coin_image, coin_rect)
    
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()