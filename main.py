import pygame
from pygame import mixer
from models import Player, Bullet, Enemy, HealthBar, GameOver
import random


# method to generate enemies
def gen_enemies(num: int) -> list:
    res = []
    locs = [i for i in range(0, 600, 20)]
    for _ in range(num):
        x = random.choice(locs)

        y_offset = random.randint(-100, 100)
        y = 20 + y_offset

        res.append(Enemy(x, y))
    
    return res

# set game state 1 for game, 0 menus, -1 game over
GAME_STATE = 1
# main game
SIZE = W, H = (700, 940)

pygame.init()

# load text
font = pygame.font.Font('freesansbold.ttf', 32)

# keep track of score 
score = 0

# load sounds
mixer.init()

mixer.Channel(0).play(pygame.mixer.Sound('background.mp3'))

def play_shot():
    pygame.mixer.music.load("shot.wav")
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('shot.wav'))

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# objects
player = Player()
bullets = []
enemies = gen_enemies(5)
health_bar = HealthBar()

running = True
count = 0
while running:

    # check game state
    if count == 60:
        enemies.extend(gen_enemies(5))
        count = 0
    
    main_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_shot()
                bullets.append(Bullet(player.get_pos()))

    player.get_keys()

    screen.fill((255, 255, 255))

    # draw entities
    player.draw(screen)
    
    for i, bullet in enumerate(bullets):
        bullet.move()
        bullet.draw(screen)

        # check for collisions
        bullet.set_hitbox()
        b_box = bullet.hitbox
        
        for j, enemy in enumerate(enemies):

            enemy.set_hitbox()
            e_box = enemy.hitbox

            if b_box.colliderect(e_box):
                # bullet hits enemy
                enemies.pop(j)
                # increment score
                score += 1
    
    player.set_hitbox()
    player_box = player.hitbox
    
    for index, enemy in enumerate(enemies):
        #  check if enemy has hit player
        enemy.set_hitbox()
        e_box = enemy.hitbox

        if player_box.colliderect(e_box):
            damage = enemy.get_damage()
            player.damage(damage)
            health_bar.remove()
        elif enemy.get_pos()[1] > H:
            # check to see if enemy has passed the player
            damage = enemy.get_damage()
            player.damage(damage)
            enemies.pop(index)
            health_bar.remove()

        enemy.move()
        enemy.draw(screen)

    health_bar.draw(screen)

    text = font.render(f"Score = {score}", True, (255, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (120, 25)
    screen.blit(text, textRect)

    count += 1

    print(player.get_health())

    if player.get_health() < 0:

        screen.fill((255, 255, 255))

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Game Over!", True, (255, 0, 0), (0, 255, 0))
        textRect = text.get_rect()
        textRect.center = (350, 490)
        screen.blit(text, textRect)


    pygame.display.update()
    clock.tick(60)