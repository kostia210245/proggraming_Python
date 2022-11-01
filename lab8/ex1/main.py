import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((50,50,50))
circle(screen, (255, 255, 0), (200, 175), 100)
circle(screen, (0, 0, 0), (200, 175), 100, 2)

circle(screen, (255, 0, 0), (150, 135), 20)
circle(screen, (0, 0, 0), (150, 135), 20, 1)
circle(screen, (0, 0, 0), (150, 135), 10)

circle(screen, (255, 0, 0), (250, 135), 15)
circle(screen, (0, 0, 0), (250, 135), 15, 1)
circle(screen, (0, 0, 0), (250, 135), 8)

rect(screen, (0, 0, 0), (150, 220, 100, 20), 0)


line(screen, (0, 0, 0), (100, 90), (180, 120), 10)
line(screen, (0, 0, 0), (300, 90), (220, 130), 10)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()