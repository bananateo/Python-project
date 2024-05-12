import pygame
pygame.init()

FPS = 60

WIDTH, HEIGHT = 1500, 750

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_VEL = 10
PLAYER_JUMP = 20

GRAVITY = 6
GRAVITY_REINORCEMENT = 5

pygame.display.set_caption("Running game")

clock = pygame.time.Clock()

running = True

player = pygame.Rect(0, HEIGHT - 50 , 30, 25)

ground = HEIGHT - 40

def draw(player):
    pygame.draw.rect(WINDOW, (0, 0, 0), (player.x, player.y, player.height, player.width))

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
    
while running:

    clock.tick(FPS)
    WINDOW.fill((255, 255, 255))

    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.y - 10 * PLAYER_VEL > HEIGHT - HEIGHT/3 or event.key == pygame.K_w and player.y - 10 * PLAYER_VEL > HEIGHT - HEIGHT/3:
                 if player.y == ground:
                    for i in range (0,10):
                        player.y -= PLAYER_JUMP
                        draw(player)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                if keys_pressed[pygame.K_d]:
                    for i in range (0,10):
                        player.x += PLAYER_VEL
                        draw(player)
                        if player.x >= WIDTH - 30:
                            break
                if keys_pressed[pygame.K_a]:
                    for i in range(0,10):
                        player.x -= PLAYER_VEL
                        draw(player)
                        if player.x <= 0:
                                break
    
    draw(player) 
    pygame.display.flip()
    player_movement(keys_pressed, player)