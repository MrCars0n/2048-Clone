import pygame
import random
import square

pygame.init()
pygame.display.set_caption('2048')
pygame.display.set_icon(pygame.image.load('2048.png'))

# Setting colors
ColorBorder = (187, 173, 160)
ColorDarkText = (119, 110, 101)
ColorLightText = (249, 246, 242)
ColorEmptySq = (204, 191, 180)
ColorBackground = (250, 248, 239)

# IMPORTANT - Almost all other values based on these numbers.
#  Number of squares in grid, and size of squares
w, s = 4, 60
h, border, topSpace = w, 6, (s * 1.25) + (s / 6)
score, best = 0, 0

windowWidth, windowHeight = s * 1.25 * w, s * 1.25 * h + topSpace
window = pygame.display.set_mode((windowWidth, windowHeight))

regText = pygame.font.SysFont("ClearSans-Bold.ttf", int(s * 0.7))
subText = pygame.font.SysFont("ClearSans-Bold.ttf", int(s * 25 / 60))

GAME_DELAY = 250
lastPlace, lastMove = GAME_DELAY, GAME_DELAY
place, sound1 = False, True

# Generate grid and first square
grid = [[square.Square(0, s) for x in range(w)] for y in range(h)]
grid[random.randint(0, 3)][random.randint(0, 3)].setNumber(2)


def resetHasCombined():
    # Enable all the spaces on the board to combinations
    for row in range(h):
        for col in range(w):
            grid[row][col].setHasCombined(False)


def isFilled():
    for row in range(h):
        for col in range(w):
            # If an empty square is found, return False
            if grid[row][col].getNumber() == 0:
                return False
    return True


def gameOver():
    for row in range(h):
        for col in range(w):
            # If an empty square is found, return False
            if grid[row][col].getNumber() == 0:
                return False

            # If the loop is not on the last row or column
            elif row < h - 1 and col < w - 1:
                # If the current selected square can merge with the one in the next row, return False
                if grid[row][col].getNumber() == grid[row + 1][col].getNumber():
                    return False

                # If the current selected square can merge with the one in the next column, return False
                elif grid[row][col].getNumber() == grid[row][col + 1].getNumber():
                    return False
    return True


def placeNew():
    global w, h

    # Pick a random x and y coordinate
    if not isFilled():
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        while grid[x][y].getNumber() != 0:
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
        grid[x][y].setNumber(2)

    resetHasCombined()


# Reset grid
def reset():
    global grid, score
    grid = [[square.Square(0, s) for x in range(w)] for y in range(h)]
    score = 0


# Used for font generation
def textObjects(text, font, twoAndFour=True):
    if (text == "2" or text == "4") and twoAndFour:
        tempColor = ColorDarkText
    else:
        tempColor = ColorLightText

    textSurface = font.render(text, True, tempColor)
    return textSurface, textSurface.get_rect()


def moveSquare(r, c, rInc=0, cInc=0):
    global score
    # If the current space being moved is not empty
    if grid[r][c].getNumber() != 0:
        # If the space being moved to is empty
        if grid[r + rInc][c + cInc].getNumber() == 0:
            # Replace the new space number with the old space number
            grid[r + rInc][c + cInc].setNumber(grid[r][c].getNumber())

            # Set the old space value to zero
            grid[r][c].setNumber(0)

        # If the old space and new space are equal AND the new space has not already combined
        elif grid[r + rInc][c + cInc].getNumber() == grid[r][c].getNumber() and not grid[r + rInc][
            c + cInc].getHasCombined():
            # Double the value of the new space
            grid[r + rInc][c + cInc].setNumber(grid[r][c].getNumber() * 2)

            # Increment score
            score += grid[r][c].getNumber() * 2

            # Mark the new space as already having been combined
            grid[r + rInc][c + cInc].setHasCombined(True)

            # Set the old space value to zero
            grid[r][c].setNumber(0)


def moveDown(r, c):
    if r < h - 1:
        moveSquare(r, c, 1, 0)


def moveUp(r, c):
    if r > 0:
        moveSquare(r, c, -1, 0)


def moveLeft(r, c):
    if c > 0:
        moveSquare(r, c, 0, -1)


def moveRight(r, c):
    if c < w - 1:
        moveSquare(r, c, 0, 1)


def playSound():
    global sound1
    swipe1 = pygame.mixer.Sound("swipe1.wav")
    swipe2 = pygame.mixer.Sound("swipe2.wav")

    # Switch between sound 1 and 2
    if not gameOver():
        if sound1:
            swipe1.play()
            sound1 = False
        else:
            swipe2.play()
            sound1 = True


def keyCheck():
    global lastMove, GAME_DELAY
    keys = pygame.key.get_pressed()

    # Create buffer time between current and previous move
    if pygame.time.get_ticks() - lastMove > GAME_DELAY:

        # When down arrow is pressed
        if keys[pygame.K_DOWN]:
            # Repeat for the number of rows there are to ensure all squares go to bottom
            for x in range(h):
                # Decrement for loop to have bottom squares combined first
                for row in range(h - 1, -1, -1):
                    for col in range(w):
                        moveDown(row, col)
            placeNew()
            playSound()
            # Mark current time as last move
            lastMove = pygame.time.get_ticks()
            return

        # Repeat code for up arrow
        if keys[pygame.K_UP]:
            for x in range(h):
                for row in range(h):
                    for col in range(w):
                        moveUp(row, col)
            placeNew()
            playSound()
            lastMove = pygame.time.get_ticks()
            return

        # Repeat code for left arrow
        if keys[pygame.K_LEFT]:
            for x in range(h):
                for row in range(h):
                    for col in range(w - 1, -1, -1):
                        moveLeft(row, col)
            placeNew()
            playSound()
            lastMove = pygame.time.get_ticks()
            return

        # Repeat code for right arrow
        if keys[pygame.K_RIGHT]:
            for x in range(h):
                for row in range(h):
                    for col in range(w):
                        moveRight(row, col)
            placeNew()
            playSound()
            lastMove = pygame.time.get_ticks()
            return


running = True
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False

    surface = pygame.display.get_surface()

    # Set background color
    window.fill(ColorBackground)

    # Generate grid
    gridLength = w * (s + border)
    gridHeight = h * (s + border)
    centerBuffer = (windowWidth - gridLength) / 2 + (s / 25)

    # Generate background for grid
    pygame.draw.rect(window, ColorBorder, (
        centerBuffer - (border * 1.5), (s / 4.5) + topSpace, gridLength + (border * 2), gridHeight + (border * 2)),
                     width=0,
                     border_radius=3)

    # Generate 2048 Logo
    logo = square.Square(2048, s * 1.25)
    logoSquare = pygame.Rect(centerBuffer - border, topSpace - logo.getWidth(), logo.getWidth(), logo.getWidth())
    pygame.draw.rect(window, logo.getColor(), logoSquare, width=0, border_radius=3)

    # Generate Score and Best
    bestSquare = pygame.Rect(windowWidth - centerBuffer + border - (s * 1.25),
                             (topSpace - (s * 1.25)), (s * 1.25),
                             (s * 1.25))
    pygame.draw.rect(window, ColorBorder, bestSquare, width=0, border_radius=3)

    scoreSquare = pygame.Rect(windowWidth - centerBuffer + border - ((s * 1.25) * 2) - border,
                              (topSpace - (s * 1.25)), (s * 1.25),
                              (s * 1.25))
    pygame.draw.rect(window, ColorBorder, scoreSquare, width=0, border_radius=3)

    # Generate grid
    rect = [[0 for x in range(w)] for y in range(h)]
    for row in range(h):
        for col in range(w):
            # Add rectangle to array
            rect[row][col] = pygame.Rect(col * (s + border) + centerBuffer,
                                         row * (s + border) + border + (s / 4) + topSpace, s, s)
            # Create border for empty squares
            pygame.draw.rect(window, grid[row][col].getColor(), rect[row][col], width=0, border_radius=3)

    # Generate text on each grid square
    for row in range(h):
        for col in range(w):
            if grid[row][col].getNumber() > 0:
                textSurf, textRect = textObjects(str(grid[row][col].getNumber()), regText)
            else:
                textSurf, textRect = textObjects("", regText)
            textRect.center = (rect[row][col].x + s / 2, rect[row][col].y + s / 2)
            window.blit(textSurf, textRect)

    # Generate 2048 Logo text
    textSurf, textRect = textObjects(str(logo.getNumber()), regText)
    textRect.center = (logoSquare.x + s * 1.25 / 2, logoSquare.y + s * 1.25 / 2)
    window.blit(textSurf, textRect)

    # Generate Score text
    textSurf, textRect = textObjects("SCORE", subText)
    textRect.center = (scoreSquare.x + s * 1.25 / 2, scoreSquare.y + s * 1.25 / 4)
    window.blit(textSurf, textRect)

    textSurf, textRect = textObjects(str(score), regText, False)
    textRect.center = (scoreSquare.x + s * 1.25 / 2, scoreSquare.y + s * 1.25 / 1.5)
    window.blit(textSurf, textRect)

    # Generate Best text
    textSurf, textRect = textObjects("BEST", subText)
    textRect.center = (bestSquare.x + s * 1.25 / 2, bestSquare.y + s * 1.25 / 4)
    window.blit(textSurf, textRect)

    textSurf, textRect = textObjects(str(best), regText, False)
    textRect.center = (bestSquare.x + s * 1.25 / 2, bestSquare.y + s * 1.25 / 1.5)
    window.blit(textSurf, textRect)

    # Generate Restart button
    # Create rectangle for button
    restartSquare = pygame.Rect((windowWidth / 2) - (s * 2.5) / 2,
                                (windowHeight / 2) - ((s * 0.75) / 2) + (topSpace / 2), (s * 2.5),
                                (s * 0.75))
    if gameOver():
        # Change color if mouse hovers over
        if not restartSquare.collidepoint(pygame.mouse.get_pos()):
            tempColor = ColorEmptySq
        else:
            tempColor = ColorBorder

        # Generate rectangles, one border and other filled
        pygame.draw.rect(window, tempColor, restartSquare, border_radius=3)
        pygame.draw.rect(window, ColorBorder, restartSquare, width=border, border_radius=3)

        textSurf, textRect = textObjects("RESTART", regText, False)
        textRect.center = (restartSquare.x + s * 2.5 / 2, restartSquare.y + s * 0.8 / 2)
        window.blit(textSurf, textRect)

    # Check for keystrokes
    keyCheck()

    # Restart game when restart button pressed
    if event.type == pygame.MOUSEBUTTONUP and restartSquare.collidepoint(pygame.mouse.get_pos()):
        reset()
        placeNew()

    # High score set
    if score > best:
        best = score

    pygame.display.flip()
