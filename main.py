import pygame
import random
import square

pygame.init()
pygame.display.set_caption('2048')
pygame.display.set_icon(pygame.image.load('2048.png'))

windowWidth, windowHeight = 300, 300
window = pygame.display.set_mode((windowWidth, windowHeight))

ColorBorder = (187, 173, 160)
ColorDarkText = (119, 110, 101)
ColorLightText = (249, 246, 242)
ColorEmptySq = (204, 192, 179)

smallText = pygame.font.SysFont("ClearSans-Bold.ttf", 42)
w, h, s, border = 4, 4, 60, 5
GAME_DELAY = 1000
lastPlace, lastMove = GAME_DELAY, GAME_DELAY
shake = False
tempShake, shakeCounter = 0, 0
#109 ticks

grid = [[square.Square(0, s) for x in range(w)] for y in range(h)]

def place():
    global lastPlace
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    #print(lastPlace - pygame.time.get_ticks())
    if pygame.time.get_ticks() - lastPlace > GAME_DELAY:
        lastPlace = pygame.time.get_ticks()
        while grid[x][y].getNumber() != 0:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        grid[x][y].setNumber(2)

def reset():
    grid = [[square.Square(0, s) for x in range(w)] for y in range(h)]

def textObjects(text, font):
    textSurface = font.render(text, True, ColorDarkText)
    return textSurface, textSurface.get_rect()

def moveDown(r, c):
    global lastMove
    if pygame.time.get_ticks() - lastMove > GAME_DELAY:
        if r < h - 1:
            if grid[r][c].getNumber() != 0:
                if grid[r+1][c].getNumber() == 0:
                    grid[r+1][c].setNumber(grid[r][c].getNumber())
                elif grid[r+1][c].getNumber() == grid[r][c].getNumber():
                    grid[r+1][c].setNumber(grid[r][c].getNumber() * 2)
                grid[r][c].setNumber(0)
    place()

def moveUp(r, c):
    global lastMove
    if pygame.time.get_ticks() - lastMove > GAME_DELAY:
        if r > 0:
                if grid[r][c].getNumber() != 0 and grid[r-1][c].getNumber() == 0:
                    grid[r-1][c].setNumber(grid[r][c].getNumber())
                    grid[r][c].setNumber(0)
    place()

def moveLeft(r, c):
    global lastMove, shake
    if pygame.time.get_ticks() - lastMove > GAME_DELAY:
        if c > 0:
                if grid[r][c].getNumber() != 0 and grid[r][c-1].getNumber() == 0:
                    grid[r][c-1].setNumber(grid[r][c].getNumber())
                    grid[r][c].setNumber(0)
                shake = True
                place()


def moveRight(r, c):
    global lastMove, shake
    if pygame.time.get_ticks() - lastMove > GAME_DELAY:
        if c < w - 1:
                if grid[r][c].getNumber() != 0 and grid[r][c+1].getNumber() == 0:
                    grid[r][c+1].setNumber(grid[r][c].getNumber())
                    grid[r][c].setNumber(0)
                shake = True
                place()

def leftShake():
    global tempShake, shakeCounter
    if int(pygame.time.get_ticks() / 200) % 2 == 0:
        if tempShake == int(s / 4):
            tempShake = 0
        else:
            tempShake = -int(s / 4)
        shakeCounter += 1
    else:
        tempShake = 0
        shakeCounter += 1

def rightShake():
    global tempShake, shakeCounter
    if int(pygame.time.get_ticks() / 200) % 2 == 0:
        if tempShake == int(s / 4):
            tempShake = 0
        else:
            tempShake = int(s / 4)
        shakeCounter += 1
    else:
        tempShake = 0
        shakeCounter += 1

place()

running = True
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False

    surface = pygame.display.get_surface()

    window.fill(ColorBorder)

    # Generate grid
    gridLength = w * (s + border)
    gridHeight = h * (s + border)
    centerBuffer = (windowWidth - gridLength) / 2
    rect = [[0 for x in range(w)] for y in range(h)]
    for row in range(h):
        for col in range(w):
            # Add rectangle to array
            if shake == True:
                rect[row][col] = pygame.Rect(col * (s + border) + centerBuffer + tempShake, row * (s + border) + border + (s / 4), s, s)
            else:
                rect[row][col] = pygame.Rect(col * (s + border) + centerBuffer, row * (s + border) + border + (s / 4), s, s)
            # Create border for empty squares
            pygame.draw.rect(window, grid[row][col].getColor(), rect[row][col], width=0)

    # Generate text on each square
    for row in range(h):
        for col in range(w):
            if grid[row][col].getNumber() > 0:
                textSurf, textRect = textObjects(str(grid[row][col].getNumber()), smallText)
            else:
                textSurf, textRect = textObjects("", smallText)
            textRect.center = (rect[row][col].x + s / 2, rect[row][col].y + s / 2)
            window.blit(textSurf, textRect)

    # Key Down
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        for row in range(h):
            for col in range(w):
                moveDown(row, col)

    if keys[pygame.K_UP]:
        for row in range(h):
            for col in range(w):
                moveUp(row, col)

    if keys[pygame.K_LEFT]:
        for row in range(h):
            for col in range(w):
                moveLeft(row, col)
    leftShake()

    if keys[pygame.K_RIGHT]:
        for row in range(h):
            for col in range(w):
                moveRight(row, col)
    rightShake()

    # Stop shaking
    if shakeCounter > 2:
        shake = False
        shakeCounter = 0

            #print(pygame.time.get_ticks())

    pygame.display.flip()
