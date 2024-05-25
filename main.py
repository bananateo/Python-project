import pygame
import random

pygame.init()

FPS = 60

WIDTH, HEIGHT = 1500, 750

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
 
PLAYER_VEL = 10
PLAYER_JUMP = 20
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 55

SLASH_WIDTH = 20
SLASH_HEIGHT = 60

ENEMY_VEL = 5
ENEMY_HEIGHT = 60
ENEMY_WIDTH = 60
GROUND_ENEMY_WIDTH = 50
GROUND_ENEMY_HEIGHT = 50

GRAVITY = 5
GRAVITY_REINORCEMENT = 15
ADDED_GRAVITY = 0.6

JUMP_HEIGHT = 20
CUR_JUMP_VELOCITY = JUMP_HEIGHT

enemies = []
ground_enemies = []
enemies_survived = 0

jumping = False
double_jumping = False

background = pygame.image.load('images/background.jpg')
Background = pygame.transform.rotate(pygame.transform.scale(background, (WIDTH, HEIGHT)), 0)

RocketImg = pygame.image.load('images/enemy_rocket.png')
Rocket = pygame.transform.rotate(pygame.transform.scale(RocketImg, (ENEMY_WIDTH, ENEMY_HEIGHT)), 0)

Ground_enemyImg = pygame.image.load('images/ground_enemy.png')
Ground_enemy_image = pygame.transform.rotate(pygame.transform.scale(Ground_enemyImg, (GROUND_ENEMY_WIDTH, GROUND_ENEMY_HEIGHT)), 0)

SlashImg = pygame.image.load('images/slash.png')
slash_right = pygame.transform.rotate(pygame.transform.scale(SlashImg, (SLASH_HEIGHT, SLASH_WIDTH)), 45)
slash_down = pygame.transform.rotate(pygame.transform.scale(SlashImg, (SLASH_HEIGHT, SLASH_WIDTH)), 90)

Ninja_run = pygame.image.load('images/ninja_run1.png')
ninja_run = pygame.transform.rotate(pygame.transform.scale(Ninja_run, (PLAYER_HEIGHT, PLAYER_WIDTH)), 0)
Ninja_jump = pygame.image.load('images/ninja_jump.png')
ninja_jump = pygame.transform.rotate(pygame.transform.scale(Ninja_jump, (PLAYER_HEIGHT, PLAYER_WIDTH)), 0)



slash_counter = 10

font = pygame.font.Font('freesansbold.ttf', 16)

pygame.display.set_caption("A game about running")

clock = pygame.time.Clock()

running = True

ground = HEIGHT - 160

player = pygame.Rect(0, ground , PLAYER_HEIGHT, PLAYER_WIDTH)

class enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.create(ENEMY_WIDTH, ENEMY_HEIGHT)

    def create(self, width, height):
        self.rect = pygame.Rect(self.x, self.y, height, width)

    def draw(self):
        WINDOW.blit(Rocket, (self.x, self.y)) 
    
    def move(self):
        self.x -= ENEMY_VEL
        self.rect.x -= ENEMY_VEL
    
    def hit(self, other):
        if pygame.Rect.colliderect(self.rect, other) == True:
            return True
        


class ground_enemy(enemy):
    def __init__(self, x):
        self.y = ground - 5
        self.x = x
        self.create(GROUND_ENEMY_WIDTH, GROUND_ENEMY_HEIGHT)
    
    def draw(self):
        WINDOW.blit(Ground_enemy_image, (self.x, self.y))


def create_enemies(enemies, ground_enemies):
    yes = random.randint(0, 90)
    if yes == 1:
        enemy_x = random.randint(WIDTH, WIDTH + 60)
        enemy_y = random.randint(int(ground - HEIGHT/4), ground)
        enemy_to_add = enemy(enemy_x, enemy_y)
        enemies.append(enemy_to_add)

    if yes == 2:
        enemy_x = random.randint(WIDTH, WIDTH + 60)
        enemy_to_add = ground_enemy(enemy_x)
        ground_enemies.append(enemy_to_add)
                

def draw(player, enemies, ground_enemies):
    if player.y == ground:
        WINDOW.blit(ninja_run, (player.x, player.y))
    else:
        WINDOW.blit(ninja_jump, (player.x, player.y))
    for enemy_to_draw in enemies:
        enemy_to_draw.draw()
    
    for enemy_to_draw in ground_enemies:
        enemy_to_draw.draw()

def player_hit(key_tapped, player, enemies, ground_enemies):
    
    if key_tapped == pygame.K_RIGHT:

        slash = pygame.Rect(player.x + PLAYER_WIDTH, player.y, SLASH_HEIGHT, SLASH_WIDTH)
        WINDOW.blit(slash_right, (slash.x, slash.y))
        for enemy_to_be_hit in enemies:
            if pygame.Rect.colliderect(slash, enemy_to_be_hit.rect) is True:
                enemies.remove(enemy_to_be_hit)
                return 1
            
        for enemy_to_be_hit in ground_enemies:
            if pygame.Rect.colliderect(slash, enemy_to_be_hit.rect) is True:
                ground_enemies.remove(enemy_to_be_hit)
                return 1
                
    if key_tapped == pygame.K_DOWN:

        slash = pygame.Rect(player.x + PLAYER_WIDTH // 2, player.y + PLAYER_HEIGHT, SLASH_WIDTH, SLASH_HEIGHT)
        WINDOW.blit(slash_down, (slash.x, slash.y))
        for enemy_to_be_hit in enemies:
            if pygame.Rect.colliderect(enemy_to_be_hit.rect, slash) is True:
                enemies.remove(enemy_to_be_hit)
                return 2
            
        for enemy_to_be_hit in ground_enemies:
            if pygame.Rect.colliderect(enemy_to_be_hit.rect, slash) is True:
                ground_enemies.remove(enemy_to_be_hit)
                return 2
    return 0


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


def enemy_movement(enemies, ground_enemies):
    for enemy_to_move in enemies:
        enemy_to_move.move()
        if enemy_to_move.x < 0:
            enemies.remove(enemy_to_move)
            return 1
    for enemy_to_move in ground_enemies:
        enemy_to_move.move()
        if enemy_to_move.x < 0:
            ground_enemies.remove(enemy_to_move)
            return 1

def is_something_hit(player, enemies, ground_enemies):
    for enemy_that_hit in enemies:
        if enemy_that_hit.hit(player) == True:
            return True
        for enemy_that_got_hit in enemies:
            if enemy_that_got_hit != enemy_that_hit:
                if enemy_that_hit.hit(enemy_that_got_hit):
                    enemies.remove(enemy_that_got_hit)

    for enemy_that_hit in ground_enemies:
        if enemy_that_hit.hit(player) == True:
            return True
        for enemy_that_got_hit in enemies:
            if enemy_that_got_hit != enemy_that_hit:
                if enemy_that_hit.hit(enemy_that_got_hit):
                    enemies.remove(enemy_that_got_hit)

    for enemy_that_hit in ground_enemies:
        for enemy_that_got_hit in ground_enemies:
            if enemy_that_got_hit != enemy_that_hit:
                if enemy_that_hit.hit(enemy_that_got_hit):
                    ground_enemies.remove(enemy_that_got_hit)

while running:

    WINDOW.blit(Background, (0, 0))
    text1 = font.render(f'Slashes left:{slash_counter}', True, (0, 0, 0))
    textRect1 = text1.get_rect()
    textRect1.center = (0 + textRect1.width / 2, textRect1.height / 2)

    text2 = font.render(f'Enemies survived:{enemies_survived}', True, (0, 0, 0))
    textRect2 = text2.get_rect()
    textRect2.center = (WIDTH - textRect2.width / 2, textRect2.height / 2)

    clock.tick(FPS)

    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            
            if slash_counter > 0:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                    result_from_slash = player_hit(event.key, player, enemies, ground_enemies)
                    if result_from_slash == 1:
                        enemies_survived += 1
                        
                    if result_from_slash == 2:
                        enemies_survived += 1
                        double_jumping = 1
                    slash_counter -= 1

            if event.key == pygame.K_SPACE:
                 
                jumping = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:

                if keys_pressed[pygame.K_d]:
                    for i in range (0,10):
                        player.x += PLAYER_VEL
                        draw(player, enemies, ground_enemies)
                        if player.x >= WIDTH - 30:
                            break

                if keys_pressed[pygame.K_a]:
                    for i in range(0,10):
                        player.x -= PLAYER_VEL
                        draw(player, enemies, ground_enemies)
                        if player.x <= 0:
                                break
                        

    WINDOW.blit(text1, textRect1)
    WINDOW.blit(text2, textRect2)


    if double_jumping:
            if jumping == True:
                jumping = False
                CUR_JUMP_VELOCITY = JUMP_HEIGHT
            if player.y - CUR_JUMP_VELOCITY > ground:
                double_jumping = False
                CUR_JUMP_VELOCITY = JUMP_HEIGHT
            if player.y - GRAVITY_REINORCEMENT > ground:
                double_jumping = False
            player.y -= CUR_JUMP_VELOCITY
            CUR_JUMP_VELOCITY -= ADDED_GRAVITY
            if CUR_JUMP_VELOCITY < -JUMP_HEIGHT:
                double_jumping = False
                CUR_JUMP_VELOCITY = JUMP_HEIGHT

    if jumping:
        if player.y - CUR_JUMP_VELOCITY > ground:
            jumping = False
            CUR_JUMP_VELOCITY = JUMP_HEIGHT
        if player.y - GRAVITY_REINORCEMENT > ground:
            jumping = False
        player.y -= CUR_JUMP_VELOCITY
        CUR_JUMP_VELOCITY -= ADDED_GRAVITY
        if CUR_JUMP_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            CUR_JUMP_VELOCITY = JUMP_HEIGHT


    if len(enemies) + len(ground_enemies) < 11:
        create_enemies(enemies, ground_enemies)
    if enemy_movement(enemies, ground_enemies) == 1:
        enemies_survived += 1

    player_movement(keys_pressed, player)
    done = is_something_hit(player, enemies, ground_enemies)

    if done == True:
        running = False
        
    draw(player, enemies, ground_enemies) 
    pygame.display.flip()
    print(f"Enemies survived:{enemies_survived}")