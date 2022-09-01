# import pygame module in this program
import pygame
import random

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)

# assigning values to X and Y variable
X = 400
Y = 400

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Show Text')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

# create a text surface object,
# on which text is drawn on it.
leftText = font.render('<-', True, blue)
rightText = font.render('->', True, blue)
gameOverText = font.render('Game Over :(', True, red)

# create a rectangular object for the
# text surface object
leftTextRect = leftText.get_rect()
rightTextRect = rightText.get_rect()
gameOverTextRect = gameOverText.get_rect()

# set the center of the rectangular object.
leftTextRect.center = (X // 2, Y // 2)
rightTextRect.center = (X // 2, Y / 2)

# completely fill the surface object
# with white color
display_surface.fill(white)

isLeft = random.choice([0, 1]) == 0
isGameOver = False
canPressNewKey = False
score = 0

# useful methods
def refresh():
    display_surface.fill(white)

def showLeft():
    display_surface.blit(leftText, leftTextRect)

def showRight():
    display_surface.blit(rightText, rightTextRect)

def showGameOver():
    display_surface.blit(gameOverText, gameOverTextRect)

def showScore():
    scoreText = font.render("Score: " + str(score), True, green)
    scoreTextRect = scoreText.get_rect()
    display_surface.blit(scoreText, scoreTextRect)

# infinite loop
while True:
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.

    refresh()
    if isGameOver:
        showGameOver()
    else:
        showScore()
        if (isLeft):
            showLeft()
        else:
            showRight()


    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
            if canPressNewKey:
                if event.key == pygame.K_LEFT and isLeft:
                    num = random.choice([0, 1])
                    isLeft = num == 0
                    score = score + 1

                elif event.key == pygame.K_RIGHT and not isLeft:
                    num = random.choice([0, 1])
                    isLeft = num == 0
                    score = score + 1

                else:
                    isGameOver = True

            canPressNewKey = False

        else :
            canPressNewKey = True

        # Draws the surface object to the screen.
        pygame.display.update()