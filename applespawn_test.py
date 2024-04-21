import random
import math
import pygame

xSize = 20
ySize = 20

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH+20, HEIGHT+20))


class AppleSpawnTest:
    def __init__(self, x, y):
        self.num = 0

        self.x = x
        self.y = y

        self.xSize = xSize
        self.ySize = ySize

    def draw(self):
        if self.num == 0:
            self.colour = (255, 0, 0)
        else:
            self.colour = (0, 0, 0)

        self.image = pygame.Surface((self.xSize, self.ySize))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        screen.blit(self.image, (self.x, self.y))

def getCandidate():
    xCandidate = xSize * random.randint(0, math.floor(WIDTH / xSize - 1)) + 10
    yCandidate = ySize * random.randint(0, math.floor(HEIGHT / ySize - 1)) + 10

    return xCandidate, yCandidate

for _ in range(100000):
    apple = AppleSpawnTest(*getCandidate())
    apple.draw()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()





