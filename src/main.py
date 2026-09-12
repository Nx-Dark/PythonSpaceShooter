import pygame
import os
import sys
import random

#OOP stuff
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.original_img = pygame.image.load(os.path.join("res", "images", "player.png")).convert_alpha()
        self.image = self.original_img
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.dir = pygame.Vector2()
        self.vel = 350.0

        #laser cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.laser_cooldown_duration = 100

        self.target_angle = 0.0
        self.angle = 0.0

        #masks
        self.mask = pygame.mask.from_surface(self.image)

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

        self.target_angle = -(self.dir.x * 30.0)

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_time()

        #rotation
        self.angle = pygame.math.lerp(self.angle, self.target_angle, 10 * dt)
        self.image = pygame.transform.rotozoom(self.original_img, self.angle, 1)

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
        self.original_img = surf
        self.image = self.original_img
        self.rect = self.image.get_frect(center=pos)

        self.speed = random.randint(400, 500)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)

        self.rotation_speed = random.randint(40, 80)
        self.angle = 0.0

    def update(self, dt: float):
        self.rect.center += self.direction * self.speed * dt

        self.angle += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_img, self.angle, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

        if self.rect.top > WINDOW_HEIGHT + 10:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt: float):

        self.frame_index += 20 * dt
        self.image = self.frames[(int(self.frame_index) % len(self.frames))]
        if self.frame_index >= len(self.frames):
            self.kill()

def collision():
    global running

    if pygame.sprite.spritecollide(player, meteor_sprites, False):
        if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
            running = False

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, False):
            if pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask):
                AnimatedExplosion(explosion_surfs, laser.rect.midtop, all_sprites)
                explosion_sound.play()
                laser.kill()

def display_score():
    cur_time = pygame.time.get_ticks() // 100
    text_surf = font.render(f"{cur_time}", True, "#f0f0f0")
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, "#dfdfdf", text_rect.inflate(20, 16).move(0, -7), 4, 10)


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
explosion_surfs = [pygame.image.load(os.path.join("res", "images", "explosion", f"{i}.png")) for i in range(21)]
font = pygame.font.Font(os.path.join("res", "images", "Oxanium-Bold.ttf"), 30)

laser_sound = pygame.mixer.Sound(os.path.join("res", "audio", "laser.wav"))
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(os.path.join("res", "audio", "explosion.wav"))
explosion_sound.set_volume(0.1)
game_music = pygame.mixer.Sound(os.path.join("res", "audio", "game_music.wav"))
game_music.set_volume(0.05)
game_music.play(loops=-1)

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
    screen.fill(color="#3a2e3f")  # clearing the screen

    all_sprites.draw(screen)

    display_score()

    #updating the frame
    pygame.display.flip()

#exit
pygame.quit()
sys.exit(0)
