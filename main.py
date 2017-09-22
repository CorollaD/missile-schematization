import sys
import pygame

import utils
from colony import Colony
from graph import g_graph

pygame.init()
pygame.display.set_caption('Missile Schematization')
screen=pygame.display.set_mode([1000,650])
screen.fill(utils.get_color('WHITE'))
empty = pygame.Surface((1000, 650))
empty.fill(utils.get_color('WHITE'))

colony = Colony()

# draw map
# graph.draw(screen)
# pygame.display.flip()

ants = pygame.sprite.Group()
ants.add(colony.ants)

global_time = 0.
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    global_time += 0.01
    print('{:.2f}'.format(global_time))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

    # update
    screen.fill(utils.get_color('WHITE'))
    g_graph.draw(screen)
    ants.update()
    for ant in ants:
        screen.blit(ant.surf, ant.rect)
    pygame.display.flip()
