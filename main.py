import pygame
pygame.init()
WIDTH, HEIGHT = 1500, 750

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_VEL = 10

pygame.display.set_caption("Running game")

player = pygame.Rect(0, 0, 60, 60)

clock = pygame.time.Clock()

running = True

player = pygame.Rect(50, 50, 200, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        WINDOW.fill((255, 255, 255))

        player.draw(WINDOW)
        player.handle_keys()
        pygame.display.update()

        clock.tick(40)