import pygame
import random
pygame.init()

FPS = 60

WIDTH, HEIGHT = 1500, 750

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_VEL = 10
PLAYER_JUMP = 20
PLAYER_WIDTH = 25
PLAYER_HEIGHT = 30

ENEMY_VEL = 5
ENEMY_HEIGHT = 30
ENEMY_WIDTH = 50

GRAVITY = 5
GRAVITY_REINORCEMENT = 15

pygame.display.set_caption("Running game")

clock = pygame.time.Clock()

running = True

player = pygame.Rect(0, HEIGHT - 50 , PLAYER_HEIGHT, PLAYER_WIDTH)

ground = HEIGHT - 35

class enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.create()

    def create(self):
        self.rect = pygame.Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def draw(self):
        pygame.draw.rect(WINDOW, (255, 0, 0),(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT))
    
    def move(self):
        self.x -= ENEMY_VEL
        self.rect.x -= ENEMY_VEL
    
    def hit(self, other):
        if pygame.Rect.colliderect(self.rect, other) == True:
            return True
        
class ground_enemy(enemy):
    def __init__(self, x):
        self.y = ground
        self.x = x
        self.create()


def create_enemies(enemies):
    yes = random.randint(0, 90)
    if yes == 1:
        enemy_x = random.randint(WIDTH, WIDTH + 60)
        enemy_y = random.randint(int(ground - HEIGHT/4), ground)
        enemy_to_add = enemy(enemy_x, enemy_y)
        enemies.append(enemy_to_add)

    if yes == 2:
        enemy_x = random.randint(WIDTH, WIDTH + 60)
        enemy_to_add = ground_enemy(enemy_x)
        enemies.append(enemy_to_add)
                

def draw(player,enemies):
    pygame.draw.rect(WINDOW, (0, 0, 0), (player.x, player.y, player.height, player.width))
    for enemy_to_draw in enemies:
        enemy_to_draw.draw()


def player_movement(keys_pressed, player):

    if keys_pressed[pygame.K_a] and player.x - PLAYER_VEL >= 0:
        player.x -= PLAYER_VEL

    if keys_pressed[pygame.K_d] and player.x + PLAYER_VEL <= WIDTH - 30:
        player.x += PLAYER_VEL

    if keys_pressed[pygame.K_s] and player.y < ground:
       if player.y + GRAVITY_REINORCEMENT > ground:
           player.y = ground
       else: player.y += GRAVITY_REINORCEMENT
 
    if player.y < ground:
       if player.y + GRAVITY > ground:
           player.y = ground
       else: player.y += GRAVITY


def enemy_movement(enemies):
    for enemy_to_move in enemies:
        enemy_to_move.move()
        if enemy_to_move.x < 0:
            enemies.remove(enemy_to_move)

def is_something_hit(player, enemies):
    for enemy_that_hit in enemies:
        if enemy_that_hit.hit(player) == True:
            return True
        for enemy_that_got_hit in enemies:
            if enemy_that_got_hit != enemy_that_hit:
                if enemy_that_hit.hit(enemy_that_got_hit):
                    enemies.remove(enemy_that_got_hit)

enemies = []

while running:

    clock.tick(FPS)
    WINDOW.fill((255, 255, 255))

    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.y - 10 * PLAYER_VEL > HEIGHT - HEIGHT/3 or event.key == pygame.K_w and player.y - 10 * PLAYER_VEL > HEIGHT - HEIGHT/3:
                 
                 if keys_pressed[pygame.K_d]:
                    if player.y == ground:
                        for i in range (0,20):
                            if i < 10:
                                player.y -= PLAYER_JUMP
                            if player.x < WIDTH - 30:
                                player.x += PLAYER_VEL - 5

                            done = is_something_hit(player, enemies)
                            if done == True:
                                running = False

                            draw(player, enemies)

                 elif keys_pressed[pygame.K_a]:
                    if player.y == ground:
                        for i in range (0,20):
                            if i < 10:
                                player.y -= PLAYER_JUMP
                            if player.x > 0:
                                player.x -= PLAYER_VEL - 5

                            done = is_something_hit(player, enemies)
                            if done == True:
                                running = False

                            draw(player, enemies)

                 else: 
                     if player.y == ground:
                         for i in range (0,20):
                             if i < 10:
                                 player.y -= PLAYER_JUMP
                             done = is_something_hit(player, enemies)
                             if done == True:
                                running = False
                             draw(player, enemies)


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:

                if keys_pressed[pygame.K_d]:
                    for i in range (0,10):
                        player.x += PLAYER_VEL
                        draw(player, enemies)
                        if player.x >= WIDTH - 30:
                            break

                if keys_pressed[pygame.K_a]:
                    for i in range(0,10):
                        player.x -= PLAYER_VEL
                        draw(player, enemies)
                        if player.x <= 0:
                                break
                        

    create_enemies(enemies)
    enemy_movement(enemies)
    player_movement(keys_pressed, player)
    done = is_something_hit(player, enemies)
    if done == True:
        running = False
    draw(player, enemies) 
    pygame.display.flip()