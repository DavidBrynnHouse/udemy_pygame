import pygame
import random
import constants


class Monster(pygame.sprite.Sprite):

    def __init__(self, color, velocity):
        super().__init__()
        self.color = color
        self.velocity = velocity
        self.image = pygame.image.load("assets/" + self.color + "_monster.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(10, 550),
                             random.randint(constants.arena_top + 1,
                                            constants.arena_bottom - self.rect.height - 1))
        self.x_direction = 1 if random.random() < 0.5 else -1
        self.y_direction = 1 if random.random() < 0.5 else -1

    def update(self):
        self.update_x()
        self.update_y()

    def update_x(self):
        if self.x_direction == 1:
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity

        if self.rect.x >= constants.X - self.rect.width or self.rect.x <= 0:
            self.x_direction = -self.x_direction

    def update_y(self):
        if self.y_direction == 1:
            self.rect.y -= self.velocity
        else:
            self.rect.y += self.velocity

        if self.rect.y <= constants.arena_top or self.rect.y >= constants.arena_bottom - self.rect.height:
            self.y_direction = -self.y_direction
