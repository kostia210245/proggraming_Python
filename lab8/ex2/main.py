import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 700))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
coordinates = []
f1 = pygame.font.Font(None, 36)
global point, x ,y ,r, speed, typeR, text1
point = 0
nomer = -1
N=-1
def click(event):
    '''Определяет попадание курсором в объект'''
    global coordinates, typeR, N
    x0 = event.pos[0]
    y0 = event.pos[1]
    l = len(coordinates)
    for i in range(l):
        x1 = coordinates[i][0]
        y1 = coordinates[i][1]
        r1 = coordinates[i][2]
        if (r1 * r1 >= (x0-x1) * (x0-x1) + (y0-y1) * (y0-y1)):
            N = i
            return True
    return False
def text():
    ''' добавляет очки'''
    global point, x, y, r, typeR, text1
    if N!=-1:

        if coordinates[N][6] == 1:
           point = point + 1
        elif coordinates[N][6] == 2:
           point = point + 5
    print(point)
def SCORE():
    ''' выводит очки'''
    text1 = f1.render(str(point), 5, (180, 0, 0))
    screen.blit(text1, (100, 100))

def new_ball():
    '''рисует новый объект '''
    global x, y, r, color, speedx, speedy, coordinates, typeR

    r = randint(30, 50)
    typeR = randint(1,2)
    if typeR == 1:
        speedx = randint(-15, 15)
        speedy = randint(-15, 15)
        x = randint(100, 700)
        y = randint(100, 500)
    else:
        speedx = 10
        speedy = 10
        x = randint(100, 700)
        y = randint(150, 300)
    color = COLORS[randint(0, 5)]
    coordinates.append([x,y,r, speedx, speedy, color,typeR])


def update_position():
    ''' обновляет позицию объекта'''
    global coordinates, text1
    screen.fill(BLACK)
    for i in range(len(coordinates)):
        x = coordinates[i][0]
        r = coordinates[i][2]
        y = coordinates[i][1]
        if (coordinates[i][6] == 1):
            speedx = coordinates[i][3]
            speedy = coordinates[i][4]
            x = x + speedx
            coordinates[i][0] = x
            y = y + speedy
            coordinates[i][1] = y
            if (x + r >= 1200):
                speedx = -speedx
                coordinates[i][3] = speedx
            if (x - r <= 0):
                speedx = -speedx
                coordinates[i][3] = speedx
            if (y + r >= 700):
                speedy = -speedy
                coordinates[i][4] = speedy
            if (y - r <= 0):
                speedy = -speedy
                coordinates[i][4] = speedy
            circle(screen, coordinates[i][5], (x, y), r)
        else:
            speedx = coordinates[i][3]
            speedy = coordinates[i][4]
            x = x + 1.4*speedx
            coordinates[i][0] = x
            y = y + 1.4*speedy
            coordinates[i][1] = y
            if (x + r >= 1200):
                speedx = -speedx
                coordinates[i][3] = speedx
            if (x - r <= 0):
                speedx = -speedx
                coordinates[i][3] = speedx
            if (y + r >= 400):
                speedy = -speedy
                coordinates[i][4] = speedy
            if (y - r <=100):
                speedy = -speedy
                coordinates[i][4] = speedy
            rect(screen, coordinates[i][5], (x, y, r,r))
    pygame.display.update()

clock = pygame.time.Clock()
finished = False
new_ball()
new_ball()
pygame.display.update()

while not finished:
    N = -1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (click(event)):
                new_ball()
                text()
                coordinates.remove(coordinates[N])
    update_position()
    SCORE()
    pygame.display.update()
pygame.quit()