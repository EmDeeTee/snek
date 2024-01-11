import pygame
from random import randint
from sys import exit
from enum import Enum
from time import sleep

pygame.init()
pygame.font.init()

CELL_SIZE = 40
CELL_COUNT = 20
window = pygame.display.set_mode((CELL_COUNT * CELL_SIZE, CELL_COUNT * CELL_SIZE))
pygame.display.set_caption("Snek 2: Electric Boogaloo")
font = pygame.font.Font(pygame.font.get_default_font(), 36)

MOVE_SPEED = 10
isRunning = True
cock = pygame.time.Clock()
SCREEN_UPDATE_EVENT = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE_EVENT, 150)

class MapCoord2D:
    def __init__(self, xx, yy):
        self.xx: int = xx
        self.yy: int = yy

    def __iadd__(self, other):
        if isinstance(other, MapCoord2D):
            self.xx += other.xx
            self.yy += other.yy
        
        return self
    def __add__(self, other):
        if isinstance(other, MapCoord2D):
            return MapCoord2D(self.xx + other.xx, self.yy + other.yy)
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, MapCoord2D):
            return (self.xx, self.yy) == (other.xx, other.yy)
        raise TypeError("pizdiec")
        return False
    
    def x(self, offset = 0) -> int:
        return (self.xx + offset) * CELL_SIZE
    def y(self, offset = 0) -> int:
        return (self.yy + offset) * CELL_SIZE


class Snek:
    def __init__(self):
        self.snekBody = [MapCoord2D(6,10),MapCoord2D(7,10), MapCoord2D(8,10)]
        self.direction = MapCoord2D(-1,0)

    def draw(self):
        for index, block in enumerate(self.snekBody):
            color = (100,40,40)
            if index == 0:
                color = (100,140,40)
            r = pygame.rect.Rect(block.x(), block.y(), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, color, r)

    def move(self):
        c = self.snekBody[:-1]
        c.insert(0, c[0] + game.snek.direction)  # type: ignore
        self.snekBody = c

    def head(self) -> MapCoord2D:
        return self.snekBody[0]

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        #self.pos = MapCoord2D(self.x, self.y)
        self.pos : MapCoord2D = None # type: ignore
    
    def draw(self):
        r = pygame.rect.Rect(self.pos.x(), self.pos.y(), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, (200,40,40), r)

    def place(self):
        x = randint(1, CELL_COUNT-1)
        y = randint(1, CELL_COUNT-1)
        self.pos = MapCoord2D(x, y)

class Game:
    def __init__(self):
        self.snek = Snek()
        self.food = Food()
        self.food.place()
        self.points = 0
        self.isPaused = False

    def update(self):
        self.snek.move()
        # TODO: Collision detection for all walls and snake
        if not 0 <= self.snek.head().xx < CELL_COUNT:
            self.game_over()
        if self.food.pos == self.snek.head():
            self.food.place()
            self.snek.snekBody.append(MapCoord2D(self.snek.snekBody[-1].x(1) ,self.snek.snekBody[-1].y(1)))
            self.points += 1
        window.fill((100,101,100))
        game.draw()
        pygame.display.update()

    def draw(self):
        self.food.draw()
        self.snek.draw()

        font_surface = font.render(f"{game.points}", False, (0, 0, 0))
        window.blit(font_surface, (10,10))

    def game_over(self):
        font_surface = font.render("Life is over", False, (0, 0, 0))
        window.blit(font_surface, (0,0))
        pygame.display.flip()
        print("Life is over")
        self.isPaused = True

game = Game()

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == SCREEN_UPDATE_EVENT:
            if not game.isPaused:
                game.update()
        if event.type == pygame.KEYUP:
            # TODO: Make it, so you can't reverse direction
            if event.key == pygame.K_UP: game.snek.direction = MapCoord2D(0,-1)
            if event.key == pygame.K_DOWN: game.snek.direction = MapCoord2D(0,1)
            if event.key == pygame.K_LEFT: game.snek.direction = MapCoord2D(-1,0)
            if event.key == pygame.K_RIGHT: game.snek.direction = MapCoord2D(1,0)
    cock.tick(60)

