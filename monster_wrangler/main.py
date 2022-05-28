import pygame
from knight import Knight
from game import Game
import constants

pygame.init()

display_surface = pygame.display.set_mode((constants.X, constants.Y))
arena_rect = pygame.Rect(1, constants.arena_top, constants.X - 2, constants.arena_bottom - constants.arena_top)

monster_colors = {'blue': (13, 180, 240), 'purple': (222, 37, 244), 'green': (55, 191, 70), 'yellow': (246, 158, 26)}
white = (255, 255, 255)
black = (0, 0, 0)

knight = Knight()

game = Game(knight)
game.spawn_monsters()
game.select_target_monster()

font = pygame.font.Font('assets/Abrushow.ttf', 32)
livesText = font.render(f'Lives: {knight.lives}', True, white, black)
livesRect = livesText.get_rect()
livesRect.topleft = (10, 10)

scoreText = font.render(f'Score: {game.score}', True, white, black)
scoreRect = scoreText.get_rect()
scoreRect.topright = (constants.X - scoreRect.width, 10)

warpsText = font.render(f'Lives: {knight.warps}', True, white, black)
warpsRect = warpsText.get_rect()
warpsRect.topleft = (10, 42)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            knight.reset()
            knight.warps -= 1

    border_color = monster_colors[game.current_target_color]

    display_surface.fill((0, 0, 0))
    pygame.draw.rect(display_surface, border_color, arena_rect, 2)

    livesText = font.render(f'Lives: {knight.lives}', True, white, black)
    display_surface.blit(livesText, livesRect)

    scoreText = font.render(f'Score: {game.score}', True, white, black)
    display_surface.blit(scoreText, scoreRect)

    warpsText = font.render(f'Warps: {knight.warps}', True, white, black)
    display_surface.blit(warpsText, warpsRect)

    display_surface.blit(game.target_image, game.target_rect)
    pygame.draw.rect(display_surface, border_color, game.target_rect, 2)

    knight.update()
    display_surface.blit(knight.image, knight.rect)

    game.monster_group.update()
    game.monster_group.draw(display_surface)

    game.update()

    pygame.display.update()
pygame.quit()
