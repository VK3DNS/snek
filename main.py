# Import necessary modules
from arcadify import arcadify
import pygame
import random
import math
from mutagen import mp3

# Load and set up sound files
deathsoundlen = mp3.MP3("pacman.mp3")
deathsoundlength = deathsoundlen.info.length
pygame.init()
deathSound = pygame.mixer.Sound("pacman.mp3")
deathSound.set_volume(0.05)
hitmarkerSound = pygame.mixer.Sound("hitmarker.mp3")
hitmarkerSound.set_volume(0.1)

# Set up display parameters
WIDTH, HEIGHT = 1000, 1000
xSize = 20
ySize = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snek")
window_icon = pygame.image.load("snake.png")
pygame.display.set_icon(window_icon)
pygame.mouse.set_visible(False)

# Set up score and apple parameters
scoresize = 3
applenumsize = 2

# Function to display score
def score(score):
    arc.render(score, WIDTH/50, HEIGHT/50, "blue", scoresize)

# Initialize Arcadify
arc = arcadify.Arcadify(screen, pygame)

# Class for main menu
class mainMenu:
    def __init__(self):
        # Initialize menu parameters
        self.menu = True
        self.titlestr = "Snek"
        self.startstr = "Press enter or space to start"
        self.titlesize = 7
        self.startsize = 1
        self.colour = (0, 255, 0)
        self.image = pygame.Surface((xSize, ySize))
        self.image.fill(self.colour)
        self.apple = pygame.Surface((xSize, ySize))
        self.apple.fill((255, 0, 0))
        self.applepos = 5
        self.coords = []
        # Generate coordinates for menu display
        for i in range(-2,math.ceil(self.titlesize*8*len(self.titlestr)/xSize)+1):
            self.coords.append((WIDTH / 2 - len(self.titlestr) * 4 * self.titlesize + i * xSize, HEIGHT / 2 - 3 * 20 - self.titlesize * 8))
        for i in range(-5, 4)[::-1]:
            self.coords.append((WIDTH / 2 - len(self.titlestr) * 4 * self.titlesize + (math.ceil(self.titlesize*8*len(self.titlestr)/xSize)+1) * xSize, HEIGHT / 2 - 3 * 20 - self.titlesize * 8 - (i-3) * 20))
        for i in range(-2, math.ceil(self.titlesize * 8 * len(self.titlestr) / xSize) + 1)[::-1]:
            self.coords.append((WIDTH / 2 - len(self.titlestr) * 4 * self.titlesize + i * xSize, HEIGHT / 2 + 3 * 20 - self.titlesize * 8 + 2 * 20))
        for i in range(-5, 4):
            self.coords.append((WIDTH / 2 - len(self.titlestr) * 4 * self.titlesize + -3 * xSize, HEIGHT / 2 - 3 * 20 - self.titlesize * 8 - (i-3) * 20))
        self.snekanimationhead = 0
        self.snekanimationlength = 12
        self.snekanimationsegments = []

    # Function to draw snake segment
    def drawsneksegment(self):
        for coord in self.coords:
            screen.blit(self.image, (coord[0], coord[1]))

    # Function to display menu
    def display(self):
        ticks = 0
        maxticks = 60
        while self.menu:
            screen.fill((255, 255, 255))
            screen.blit(self.apple, self.coords[self.applepos])
            self.snekanimationsegments.append([0, self.snekanimationhead])
            if ticks > maxticks:
                ticks = 0
                for segment in self.snekanimationsegments:
                    segment[0] += 1
                    if len(self.snekanimationsegments) > self.snekanimationlength:
                        self.snekanimationsegments.remove(segment)
                self.snekanimationhead += 1
                if self.applepos == self.snekanimationhead:
                    hitmarkerSound.play()
                    self.applepos += random.randint(1, len(self.coords) - self.snekanimationlength - 4)
                    if self.applepos > len(self.coords) - 1:
                        self.applepos -= len(self.coords) - 1
            ticks += 1
            if self.snekanimationhead > len(self.coords) - 1:
                self.snekanimationhead = 0
            for segment in self.snekanimationsegments:
                screen.blit(self.image, (self.coords[segment[1]], self.coords[segment[1]]))
            arc.render(self.titlestr, WIDTH/2 - len(self.titlestr)*4*self.titlesize, HEIGHT/2 - 7*8, "blue", 7)
            arc.render(self.startstr, WIDTH/2 - len(self.startstr)*4*self.startsize, HEIGHT/2, "blue", 1)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        self.menu = False
        return not self.menu

# Class for snake head
class Head:
    def __init__(self, x, y, dir, xSize, ySize, startLength=10):
        # Initialize head parameters
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize
        self.dir = dir
        self.startLength = startLength
        self.length = startLength
        self.colour = (0, 255, 0)

    # Function to move head
    def move(self, bodylist, applelist, initialApples):
        keepRunning = True
        # Move head based on direction
        if self.dir == "up":
            self.y -= self.ySize
        elif self.dir == "down":
            self.y += self.ySize
        elif self.dir == "left":
            self.x -= self.xSize
        elif self.dir == "right":
            self.x += self.xSize
        # Wrap around if head reaches edge of screen
        if self.x < 0:
            self.x = WIDTH - self.xSize
        elif self.x > WIDTH - self.xSize:
            self.x = 0
        elif self.y < 0:
            self.y = HEIGHT - self.ySize
        elif self.y > HEIGHT - self.ySize:
            self.y = 0
        # Add apples if necessary
        while len(applelist) < math.floor(self.length / 5) + 1:
            conditions = False
            while not conditions:
                xCandidate, yCandidate = self.getCandidate()
                conditions = True
                for segment in bodylist:
                    if xCandidate == segment.x and yCandidate == segment.y:
                        conditions = False
                        print("touching snek")
                for apple in applelist:
                    if xCandidate == apple.x and yCandidate == apple.y:
                        conditions = False
                        print("touching apple")
                if self.x - self.xSize * 5 <= xCandidate <= self.x + self.xSize * 5 and self.y - self.ySize * 5 <= yCandidate <= self.y + self.ySize * 5:
                    conditions = False
                    print("too close")
                if initialApples:
                    if xCandidate >= WIDTH/2 and yCandidate == math.floor((HEIGHT/2 - ySize/2)/10)*10:
                        conditions = False
                        print("out of bounds")
            applelist.append(Apple(xCandidate, yCandidate, len(applelist), self.xSize, self.ySize))
        for apple in applelist:
            apple.draw()
        apple = self.detectApple()
        if apple is not None:
            if not apple:
                keepRunning = False
        bodyCollision = self.spawn_body(bodylist)
        if keepRunning:
            keepRunning = bodyCollision
        return keepRunning

    # Function to get candidate position for apple
    def getCandidate(self):
        xCandidate = self.xSize*random.randint(0, math.floor(WIDTH/self.xSize - 1))
        yCandidate = self.ySize*random.randint(math.ceil(0+8*scoresize/20+1), math.floor(HEIGHT/self.ySize - 1))
        return xCandidate, yCandidate

    # Function to spawn body segment
    def spawn_body(self, bodylist):
        bodylist.append(Body(self.x, self.y, self.xSize, self.ySize, self.colour))
        if len(bodylist) > self.length:
            del bodylist[0]
        toReturn = True
        for segment in bodylist:
            if segment != bodylist[-1]:
                segment.draw()
                if self.x == segment.x and self.y == segment.y:
                    toReturn = False
            else:
                segment.draw()
        return toReturn

    # Function to detect apple
    def detectApple(self):
        for apple in applelist:
            if self.x == apple.x and self.y == apple.y:
                if apple.num == 0:
                    applelist.remove(apple)
                    self.length += 1
                    for apple in applelist:
                        apple.num -= 1
                        hitmarkerSound.play()
                    return True
                return False
        return None

# Class for body segment
class Body:
    def __init__(self, x, y, xSize, ySize, colour):
        # Initialize body segment parameters
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize
        self.colour = colour
        self.image = pygame.Surface((self.xSize, self.ySize))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    # Function to draw body segment
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Class for apple
class Apple:
    def __init__(self, x, y, num, xSize, ySize):
        # Initialize apple parameters
        self.num = num
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize

    # Function to draw apple
    def draw(self):
        applenum_colour = "blue" if self.num == 0 else "yellow"
        if self.num == 0:
            self.colour = (255, 0, 0)
        else:
            self.colour = (0, 0, 0)
        displaynum = self.num + 1 if self.num + 1 <=9 else "-"
        self.image = pygame.Surface((self.xSize, self.ySize))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        screen.blit(self.image, (self.x, self.y))
        arc.render(displaynum, self.x + self.xSize/2 - applenumsize*4, self.y + self.ySize/2 - applenumsize*4, applenum_colour, applenumsize)

# Function to initialize game
def init():
    head = Head(math.floor((WIDTH/2 - xSize/2)/xSize)*xSize, math.floor((HEIGHT/2 - ySize/2)/ySize)*ySize, "right", xSize, ySize)
    bodylist = []
    applelist = []
    initialApples = True
    running = True
    return head, bodylist, applelist, initialApples, running

# Initialize game
head, bodylist, applelist, initialApples, running = init()

# Main game loop
while True:
    menu = mainMenu()
    running = menu.display()
    if running:
        head, bodylist, applelist, initialApples, running = init()
    while running:
        abort = False
        screen.fill((255, 255, 255))
        score(f"Score: {head.length - head.startLength}")
        rotated = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not rotated:
                    if head.dir != "down":
                        head.dir = "up"
                        rotated = True
                elif event.key == pygame.K_DOWN and not rotated:
                    if head.dir != "up":
                        head.dir = "down"
                        rotated = True
                elif event.key == pygame.K_LEFT and not rotated:
                    if head.dir != "right":
                        head.dir = "left"
                        rotated = True
                elif event.key == pygame.K_RIGHT and not rotated:
                    if head.dir != "left":
                        head.dir = "right"
                        rotated = True
                elif event.key == pygame.K_ESCAPE:
                    abort = True
                elif event.key == pygame.K_SPACE:
                    head, bodylist, applelist, initialApples, running = init()

        running = head.move(bodylist, applelist, initialApples)
        pygame.display.flip()
        screen.fill((0, 0, 0))
        pygame.time.delay(100)

        # Death sequence
        if not running or abort:

            print("death")
            screen.fill((255, 255, 255))
            score(f"Score: {head.length - head.startLength}")
            for apple in applelist:
                apple.draw()
            pygame.display.flip()

            pygame.time.delay(100)

            screen.fill((255, 255, 255))
            score(f"Score: {head.length - head.startLength}")
            for apple in applelist:
                apple.draw()
            for segment in bodylist:
                segment.draw()
            pygame.display.flip()

            pygame.time.delay(100)

            screen.fill((255, 255, 255))
            score(f"Score: {head.length - head.startLength}")
            for apple in applelist:
                apple.draw()
            pygame.display.flip()

            pygame.time.delay(100)

            screen.fill((255, 255, 255))
            score(f"Score: {head.length - head.startLength}")

            for apple in applelist:
                apple.draw()
            for segment in bodylist:
                segment.draw()
            pygame.display.flip()

            deathSound.play()
            bodylen = len(bodylist)
            for segment in bodylist:
                screen.fill((255, 255, 255))
                score(f"Score: {head.length - head.startLength}")
                pygame.time.delay(math.floor(deathsoundlength*1000/bodylen))
                bodylist = bodylist[0:-1]
                for segment in bodylist:
                    segment.draw()
                for apple in applelist:
                    apple.draw()
                pygame.display.flip()
            if abort:
                pygame.quit()
