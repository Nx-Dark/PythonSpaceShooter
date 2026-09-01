import pygame, sys, math, os, random

#pygame init stuff
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 540
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
lastTime = float(pygame.time.get_ticks()) * 0.001
curTime = 0.0

#image surface
player_surf = pygame.image.load(os.path.join("res", "images", "player.png")).convert_alpha()
player_rect = player_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_dir = pygame.Vector2()
player_vel = 300.0

star_surf = pygame.image.load(os.path.join("res", "images", "star.png")).convert_alpha()
star_positions = [(random.randint(10, 900), random.randint(10, 500)) for _ in range(20)]

meteor_surf = pygame.image.load(os.path.join("res", "images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(os.path.join("res", "images", "laser.png")).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

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

        # elif event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

    #polling input events
    keys = pygame.key.get_pressed()
    recent_keys = pygame.key.get_just_pressed()

    #update

    #player movement update
    player_dir.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    player_dir.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

    player_dir = player_dir.normalize() if player_dir else player_dir

    if recent_keys[pygame.K_SPACE]:
        print("FIRE LASER")

    player_rect.center += player_dir * player_vel * dt

    #drawing/rendering
    screen.fill(color="darkgray")  # clearing the screen

    # drawing the star surface
    for pos in star_positions:
        screen.blit(star_surf, pos)

    #drawing the meteor
    screen.blit(meteor_surf, meteor_rect)

    #drawing the laster
    screen.blit(laser_surf, laser_rect)

    # drawing the player surface
    screen.blit(player_surf, player_rect)

    #updating the frame
    pygame.display.flip()

#exit
pygame.quit()
sys.exit(0)
