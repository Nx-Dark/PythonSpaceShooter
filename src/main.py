from typing import Any

import pygame
import os
import sys
import random

#OOP stuff
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.image.load(os.path.join("res", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.dir = pygame.Vector2()
        self.vel = 350.0

        #laser cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.laser_cooldown_duration = 250

    def laser_time(self):
        if not self.can_shoot:
            cur_time = pygame.time.get_ticks()
            if cur_time - self.laser_shoot_time >= self.laser_cooldown_duration:
                self.can_shoot = True

    def update(self, dt: float):
        keys = pygame.key.get_pressed()

        self.dir.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.dir.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.dir = self.dir.normalize() if self.dir else self.dir
        self.rect.center += self.dir * self.vel * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_time()

class Star(pygame.sprite.Sprite):

    def __init__(self, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(10, WINDOW_WIDTH - 30), random.randint(10, WINDOW_HEIGHT - 20)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt: float):
        self.rect.centery -= 400 * dt

        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(center=pos)

        self.speed = random.randint(400, 500)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)

    def update(self, dt: float):
        self.rect.center += self.direction * self.speed * dt

        if self.rect.top > WINDOW_HEIGHT + 10:
            self.kill()

def collision():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collision_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collision_sprites:
            laser.kill()


#pygame init stuff
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1050, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
lastTime = float(pygame.time.get_ticks()) * 0.001
curTime = 0.0

#import
star_surf = pygame.image.load(os.path.join("res", "images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(os.path.join("res", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(os.path.join("res", "images", "laser.png")).convert_alpha()

#sprite group for all sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

#stars
for _ in range(20): Star(star_surf, all_sprites)

#player
player: Player = Player(all_sprites)

#custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

test_rect = pygame.FRect(0, 0, 300, 600)

#main loop
while running:
    #calculating deltaTime#########
    curTime = float(pygame.time.get_ticks()) * 0.001
    dt: float = (float(curTime) - float(lastTime))
    lastTime = curTime
    ###############################

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(30, WINDOW_WIDTH - 30), random.randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    #update
    all_sprites.update(dt)

    #collisions
    collision()

    #drawing/rendering
    screen.fill(color="darkgray")  # clearing the screen

    all_sprites.draw(screen)

    #updating the frame
    pygame.display.flip()

#exit
pygame.quit()
sys.exit(0)
