import pygame
import constants
import random
from monster import Monster


class Game:

    def __init__(self, knight):
        self.target_image = None
        self.target_rect = None
        self.monster_group = None
        self.knight = knight
        self.target_color_list = []
        self.current_target_color = None
        self.score = 0
        self.current_round = 0

    def update(self):
        self.check_collisions()

    def check_collisions(self):
        collided_monster = pygame.sprite.spritecollideany(self.knight, self.monster_group)
        if collided_monster:
            if collided_monster.color == self.current_target_color:
                collided_monster.remove(self.monster_group)
                self.select_target_monster()
                self.score += 100
            else:
                self.knight.reset()
                self.knight.lives -= 1

    def select_target_monster(self):
        try:
            self.current_target_color = self.target_color_list.pop()
            print(self.target_color_list)
        except IndexError:
            self.knight.reset()
            self.spawn_monsters()
            self.select_target_monster()
        self.target_image = pygame.image.load("assets/" + self.current_target_color + "_monster.png")
        self.target_rect = self.target_image.get_rect()
        self.target_rect.topleft = (constants.X // 2 - self.target_rect.width // 2,
                                    constants.arena_top - self.target_rect.height)

    def spawn_monsters(self):
        monster_group = pygame.sprite.Group()

        for i in range(4):
            color = random.choice(list(constants.colors))
            self.target_color_list.append(color)
            monster = Monster(color, constants.VELOCITY)
            monster_group.add(monster)
        self.monster_group = monster_group
