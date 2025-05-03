import pygame
import sys
import graphics
import logic
import resourcegame

pygame.init()

WIDTH, HEIGHT = 500, 500
BACKGROUND_COLOR = (255, 255, 255)
player_coord = [0, 0]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")

clock = pygame.time.Clock()
running = True

logic.init_coord(resourcegame.coords)

while running:
    if resourcegame.Finish == True:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                logic.move_left(player_coord, resourcegame.coords, screen)
            elif event.key == pygame.K_RIGHT:
                logic.move_right(player_coord, resourcegame.coords, screen)
            elif event.key == pygame.K_UP:
                logic.move_up(player_coord, resourcegame.coords, screen)
            elif event.key == pygame.K_DOWN:
                logic.move_down(player_coord, resourcegame.coords, screen)
            elif event.key == pygame.K_F1:
                print(resourcegame.coords)
            print(player_coord)        
    screen.fill(BACKGROUND_COLOR)
    graphics.draw_labirint(screen, player_coord[0], player_coord[1], resourcegame.coords)
    graphics.draw_player(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()