import pygame
import sys

#initialize pygame
pygame.init()

#set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Game")

#define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#Player settings
player_pos = [width // 2, height // 2]
player_size = 50
player_speed = 5

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K.DOWN] and player_pos[1] < height - player_size:
        player_pos[1] += player_speed

    #fill the background
    screen.fill(WHITE)

    #draw the player
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    #update the display
    pygame.display.flip()
