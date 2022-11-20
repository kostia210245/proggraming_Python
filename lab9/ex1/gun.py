import math
from random import choice
import pygame
from pygame.draw import *
from random import randint as rnd

pygame.init()

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
g = 1
WIDTH = 800
HEIGHT = 600
clock = pygame.time.Clock()
targets = []
points = 0
timer = 90
f1 = pygame.font.Font(None, 60)


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=550):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.bouns = 0
        self.live = 0
        self.g = 1

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        vy = self.vy - self.g
        self.vy = vy
        if (self.y + self.r - self.vy + g > 600):
            vy = -0.8 * self.vy
            self.vy = vy
            self.vx = 0.8 * self.vx
            self.bouns += 1
        if (self.bouns == 12):
            self.vy = 0
            self.vx = 0
            self.g = 0
            self.live += 1
        if (self.x + self.r + self.vx >= 800):
            self.vx = -0.8 * self.vx
        if (self.x - self.r + self.vx <= 0):
            self.vx = -0.8 * self.vx

    def draw(self):
        """Рисует шары"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        x = self.x
        y = self.y
        r = self.r
        x0 = obj.x
        y0 = obj.y
        r0 = obj.r
        if ((x0 - x) ** 2 + (y0 - y) ** 2 <= (r0 + r) ** 2):
            return True
            hit()
        else:
            return False


class LINE:
    def __init__(self, screen: pygame.Surface, x=40, y=520, x2=20, y2=550):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.x2 = x2
        self.y = y
        self.y2 = y2
        self.vx = 0
        self.vy = 0
        self.color = RED
        self.live = 0
        self.g = 1

    def moveL(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.x2 += self.vx
        self.y2 -= self.vy

    def drawL(self):
        """Рисует лазер"""
        pygame.draw.line(self.screen, self.color, (self.x2, self.y2), (self.x, self.y), 4)

    def hittestL(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        x = self.x
        y = self.y
        x2 = self.x2
        y2 = self.y2
        x0 = obj.x
        y0 = obj.y
        r0 = obj.r
        if ((x0 - x) ** 2 + (y0 - y) ** 2 <= r0 ** 2):
            return True
            hit()
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450
        self.l = 25
        self.x1 = 20

    def fire2_start(self, event):
        """Начало натяжения"""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, linesL
        bullet += 1
        new_ball = Ball(self.screen, x=self.x1)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def fire3_end(self, event):
        """Стрельба после отжатия лазером"""
        global linesL
        new_line = LINE(self.screen)
        lenght = 40
        new_line.x = lenght * math.cos(self.an) + self.x1
        new_line.y = lenght * math.sin(self.an) + 550
        new_line.x2 = self.x1
        new_line.vx = self.f2_power * math.cos(self.an)
        new_line.vy = - self.f2_power * math.sin(self.an)
        linesL.append(new_line)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""

        if (event.pos[0] == self.x1):
            self.an = math.atan((event.pos[1] - 550) / (event.pos[0] + 0.1 - self.x1))
        else:
            self.an = math.atan((event.pos[1] - 550) / (event.pos[0] - self.x1))
        if (event.pos[0] - self.x1) < 0:
            self.an += math.pi

    def draw(self):
        """Рисует пушку танка"""
        self.x = self.l * math.cos(self.an)
        self.y = self.l * math.sin(self.an)

        if self.f2_on:
            self.color = GREEN
        else:
            self.color = GREY
        line(self.screen, self.color, (self.x1, 550), (self.x + self.x1, 550 + self.y), 10)
        rect(self.screen, (0,150,0), (self.x1 - 20, 550, 60, 20))

    def power_up(self):
        """Сила натяжение"""
        if self.f2_on:
            if self.f2_power < 100:
                self.l = self.l + 1
                self.f2_power += 1
            self.color = RED
        else:
            self.l = 25
            self.color = GREY

    def move(self, keys):
        """Движение танка"""
        if keys[pygame.K_d]:
            self.vx = 5
        elif keys[pygame.K_a]:
            self.vx = -5
        else:
            self.vx = 0
        self.x1 += self.vx


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target()
        self.screen = screen

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(100, 700)
        y = self.y = rnd(300, 530)
        r = self.r = rnd(15, 65)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        color = self.color = GAME_COLORS[rnd(0, 5)]
        self.live = 1

    def hit(self):
        """Попадание шарика в цель."""
        global points
        points += 1
        print(points)

    def update_position(self):
        """Обновление позиции"""
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        if (self.x + self.r >= 800):
            self.vx = -self.vx
        if (self.x - self.r < 0):
            self.vx = -self.vx
        if (self.y - self.r < 0):
            self.vy = -self.vy
        if (self.y + self.r > 600):
            self.vy = -self.vy

    def draw(self):
        """ Рисует новый таргет"""
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r + 1)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class Target2:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target2()
        self.screen = screen

    def new_target2(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(100, 700)
        y = self.y = rnd(300, 530)
        r = self.r = rnd(15, 65)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        self.vr = 3
        color = self.color = GAME_COLORS[rnd(0, 5)]
        self.live = 1

    def update_position2(self):
        """Обновление позиции"""
        global ticker
        x = 20 * math.cos(0.2 * ticker)
        y = 20 * math.sin(0.2 * ticker)
        self.x += x
        self.y += y
        self.r = self.r + self.vr
        if self.r >= 80:
            self.vr = -self.vr
        if self.r <= 0:
            self.vr = - self.vr
        if (self.x + self.r + self.vr >= 800):
            self.vx = -self.vx
        if (self.x + self.r + self.vr < 0):
            self.vx = -self.vx
        if (self.y - self.r - self.vr < 15):
            self.vy = -self.vy
        if (self.y + self.r - self.vr > 600):
            self.vy = -self.vy

    def hit(self):
        """Попадание шарика в цель."""
        global points
        points += 1
        print(points)

    def draw2(self):
        """ Рисует новый таргет"""
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r + 1)
        pygame.draw.circle(self.screen, (0, 100, 244), (self.x, self.y), self.r)


def ScoreText():
    """Вывод текста на экран"""
    screen.fill(RED)
    screen.fill(BLACK)
    score = f1.render(str(points), 5, (0, 0, 0), (180, 0, 0))
    scoreTEXT = f1.render("Ваш счет - ", 5, (0, 0, 0), (180, 0, 0))
    screen.blit(score, (500, 200))
    screen.blit(scoreTEXT, (250, 200))


def DeathUslovie():
    """Условие смерти таргетов"""
    for b in balls:
        b.move()
        for i in range(len(targets)):
            if b.hittest(targets[i]) and targets[i].live:
                targets[i].live = 0
                targets[i].hit()
        for i in range(len(targets2)):
            if b.hittest(targets2[i]) and targets2[i].live:
                targets2[i].live = 0
                targets2[i].hit()
    for i in linesL:
        i.moveL()
        for j in range(len(targets)):
            if i.hittestL(targets[j]) and targets[j].live:
                targets[j].live = 0
                targets[j].hit()
            for j in range(len(targets2)):
                if i.hittestL(targets2[j]) and targets2[j].live:
                    targets2[j].live = 0
                    targets2[j].hit()


def ThreeballsAlive():
    """Условие того чтобы таргеты исчезали и не появлялись только после ликвидаци всех таргетов на экране"""
    global timer, alive, balls, cantshot
    for i in range(len(targets)):
        if targets[i].live == 1:
            alive = 1
    for i in range(len(targets2)):
        if targets2[i].live == 1:
            alive = 1
    if not (alive):
        balls = []
        timer -= 1
        cantshot = 0
        gun.f2_on = 0
        ScoreText()
        if timer == 0:
            for i in range(len(targets)):
                targets[i].new_target()
            for i in range(len(targets2)):
                targets2[i].new_target2()
            timer = 120
            cantshot = 1


def AllTargetsUpdatePos():
    """Обновление позиции все таргетов в масиве"""
    for i in range(len(targets)):
        if targets[i].live == 1:
            targets[i].draw()
            targets[i].update_position()
    for i in range(len(targets2)):
        if targets2[i].live == 1:
            targets2[i].draw2()
            targets2[i].update_position2()


def BulletsLive():
    """ Время жизни пуль"""
    for b in balls:
        b.draw()
        if b.live >= 120:
            balls.remove(b)
    for l in linesL:
        l.drawL()
        if l.live >= 120:
            linesL.remove(l)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
targets = []
targets2 = []
balls = []
linesL = []
for i in range(1):
    targets2.append(Target2())
for i in range(2):
    targets.append(Target())

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False
cantshot = 1
RightLeft = 0
ticker = 0

while not finished:
    ticker += 1
    screen.fill(WHITE)
    gun.draw()
    AllTargetsUpdatePos()
    BulletsLive()
    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and cantshot == 1:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and cantshot == 1:
            if event.button == 1:
                gun.fire2_end(event)
            elif event.button == 3:
                gun.fire3_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    keys = pygame.key.get_pressed()
    gun.move(keys)
    alive = 0
    DeathUslovie()
    ThreeballsAlive()
    pygame.display.update()
    gun.power_up()

pygame.quit()
