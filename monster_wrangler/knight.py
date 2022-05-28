import pygame
import constants


class Knight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (constants.X//2 - self.rect.width//2, constants.arena_bottom + 10)
        self.warps = 3
        self.lives = 4

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.rect.top > constants.arena_top + 2:
            self.rect.y -= constants.VELOCITY
        if keys[pygame.K_DOWN] and self.rect.bottom < constants.arena_bottom - 2:
            self.rect.y += constants.VELOCITY
        if keys[pygame.K_LEFT] and self.rect.left > 2:
            self.rect.x -= constants.VELOCITY
        if keys[pygame.K_RIGHT] and self.rect.right < constants.X - 2:
            self.rect.x += constants.VELOCITY

    def reset(self):
        self.rect.topleft = (constants.X // 2 - self.rect.width // 2, constants.arena_bottom + 10)
