import pygame
import random


class Monster(pygame.sprite.Sprite):
    """"""

    def __init__(self, color, velocity):
        super().__init__()
        self.color = color
        self.velocity = velocity
        self.image = pygame.image.load("assets/" + self.color + "_monster.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(10, 550), random.randint(64, 500))
        self.x_direction = 1 if random.random() < 0.5 else -1
        self.y_direction = 1 if random.random() < 0.5 else -1

    def update(self):
        if self.x_direction == 1:
            self.rect.x += 1
        elif self.x_direction == -1:
            self.rect.x -= 1
        if self.y_direction == 1:
            self.rect.y += 1
        elif self.y_direction == -1:
            self.rect.y -= 1

