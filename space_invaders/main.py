import pygame
import random

pygame.init()

X = 1200
Y = 700
display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Space Invaders")

FPS = 60
clock = pygame.time.Clock()


class Game:
    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        self.round_number = 1
        self.score = 0
        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group

        self.new_round_sound = pygame.mixer.Sound("assets/new_round.wav")
        self.breach_sound = pygame.mixer.Sound("assets/breach.wav")
        self.alien_hit_sound = pygame.mixer.Sound("assets/alien_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound("assets/player_hit.wav")

        self.font = pygame.font.Font("assets/Facon.ttf", 32)

    def update(self):
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()

    def draw(self):
        white = (255, 255, 255)

        score_text = self.font.render(f"Score: {self.score}", True, white)
        score_rect = score_text.get_rect()
        score_rect.centerx = X // 2
        score_rect.top = 10

        round_text = self.font.render(f"Round: {self.round_number}", True, white)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, white)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (X - 20, 10)

        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, white, (0, 50), (X, 50), 4)
        pygame.draw.line(display_surface, white, (0, Y - 100), (X, Y - 100), 4)

    def shift_aliens(self):
        shift = False
        for alien in self.alien_group.sprites():
            if alien.rect.left <= 0 or alien.rect.right >= X:
                shift = True

        if shift:
            breach = False
            for alien in self.alien_group.sprites():
                alien.rect.y += 10 * self.round_number
                alien.direction = -alien.direction
                alien.rect.x += alien.direction * alien.velocity

                if alien.rect.bottom >= Y - 100:
                    breach = True

            if breach:
                self.breach_sound.play()
                self.player.lives -= 1
                self.check_game_status("Aliens breached the line!", "Press enter to continue")

    def check_collisions(self):
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, True):
            self.alien_hit_sound.play()
            self.score += 100
        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.player_hit_sound.play()
            self.player.lives -= 1
            self.check_game_status("You have been hit", "Press enter to continue")

    def check_round_completion(self):
        if not self.alien_group:
            self.round_number += 1
            self.score += 1000 * self.round_number
            self.start_new_round()

    def start_new_round(self):
        for i in range(11):
            for j in range(5):
                alien = Alien(64 + i * 64, 64 + j * 64, self.round_number, self.alien_bullet_group)
                self.alien_group.add(alien)

        self.new_round_sound.play()
        self.pause_game(f"Space invaders round{self.round_number}", "Press enter to begin")

    def check_game_status(self, main_text, sub_text):
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()

        if self.player.lives <= 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)

    def pause_game(self, main_text, sub_text):
        global running
        white = (255, 255, 255)
        black = (0, 0, 0)

        main_text = self.font.render(main_text, True, white)
        main_rect = main_text.get_rect()
        main_rect.center = (X // 2, Y // 2)

        sub_text = self.font.render(sub_text, True, white)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (X // 2, Y // 2 + main_rect.height)

        display_surface.fill(black)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)

        pygame.display.update()
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_pause = False
                if event.type == pygame.QUIT:
                    running = False
                    is_pause = False

    def reset_game(self):
        self.pause_game(f"Final Score: {self.score}", "Press enter to play again")
        self.score = 0
        self.round_number = 1
        self.player.lives = 5
        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.start_new_round()



class Player(pygame.sprite.Sprite):

    def __init__(self, bullet_group):
        super().__init__()
        self.bullet_group = bullet_group
        self.image = pygame.image.load("assets/player_ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = X // 2
        self.rect.bottom = Y
        self.lives = 5
        self.velocity = 8
        self.shoot_sound = pygame.mixer.Sound("assets/player_fire.wav")

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.left < X - self.rect.width:
            self.rect.x += self.velocity

    def fire(self):
        if len(self.bullet_group) < 2:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        self.rect.centerx = X // 2


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, bullet_group):
        super().__init__()
        self.image = pygame.image.load("assets/alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.startingx = x
        self.startingy = y

        self.direction = 1
        self.velocity = velocity
        self.bullet_group = bullet_group
        self.shoot_sound = pygame.mixer.Sound("assets/alien_fire.wav")

    def update(self):
        self.rect.x += self.velocity * self.direction

        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            self.fire()
            self.shoot_sound.play()

    def fire(self):
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        self.rect.topleft = (self.startingx, self.startingy)
        self.direction = 1


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.image.load("assets/green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        self.rect.y -= self.velocity

        if self.rect.bottom < 0:
            self.kill()


class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.image.load("assets/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        self.rect.y += self.velocity

        if self.rect.bottom > Y:
            self.kill()


player_bullet_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

player_group = pygame.sprite.Group()
player = Player(player_bullet_group)
player_group.add(player)

alien_group = pygame.sprite.Group()

game = Game(player, alien_group, player_bullet_group, alien_bullet_group)

game.start_new_round()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    display_surface.fill((0, 0, 0))

    player_group.update()
    player_group.draw(display_surface)

    alien_group.update()
    alien_group.draw(display_surface)

    player_bullet_group.update()
    player_bullet_group.draw(display_surface)

    alien_bullet_group.update()
    alien_bullet_group.draw(display_surface)

    game.update()
    game.draw()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
