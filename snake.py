import keyboard
import pygame
import sys
import random
import keyword


class Snake:
    def __int__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (65, 82, 31)
        self.alive = True

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        curr = self.get_head_position()
        x, y = self.direction
        new = (((curr[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (curr[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.alive = False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            snake_outline = (117, 148, 56)
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, snake_outline, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class Food:
    def __int__(self):
        self.position = (0, 0)
        self.color = (164, 3, 31)
        self.randomize_position([(0, 0)])

    def randomize_position(self, snakePositions):
        possibleLocations = [x for x in GRID_LOCATIONS if x not in snakePositions]
        self.position = random.choice(possibleLocations)

    def draw(self, surface):
        #Uncomment apple and surface.blit to display picture of an apple instead of rectangle
        food_outline = (80, 2, 15)
        #apple = pygame.image.load("apple2.jfif")
        #apple = pygame.transform.scale(apple,(GRID_SIZE, GRID_SIZE))
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        #surface.blit(apple, r)
        pygame.draw.rect(surface, food_outline, r, 2)


def game_over(surface, snake):

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    myfont = pygame.font.SysFont("monospace", 16)

    #Text for the game being over and asking user to play again
    game_over_text = myfont.render("GAME OVER", True, (255, 255, 255))
    play_again_text = myfont.render("Press Space to play again!", True, (255, 255, 255))

    #Update screen with new text
    pygame.display.update(screen.blit(game_over_text, (200, 200)))
    pygame.display.update(screen.blit(play_again_text, (125, 225)))

    #If space is pressed then it will restart the game
    if keyboard.is_pressed(" "):
        play_game()

#Move entire game to one function
def play_game():
    #Init the game
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    #Set snake
    snake = Snake()
    snake.__int__()
    food = Food()
    food.__int__()

    #Font for the game text
    myfont = pygame.font.SysFont("monospace", 16)

    #Track the score
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if snake.alive:
            clock.tick(5)
            snake.handle_keys()
            drawGrid(surface)
            snake.move()
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                food.randomize_position(snake.positions)

            snake.draw(surface)
            food.draw(surface)
            screen.blit(surface, (0, 0))
            text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
            screen.blit(text, (5, 10))
            pygame.display.update()

        else:
            #If snake eats itself then initiate game_over screen
            game_over(surface, snake)


def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                tile_color = (212, 227, 236)
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, tile_color, r)
            else:
                tile_color = (204, 204, 204)
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, tile_color, rr)


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRID_SIZE
GRID_HEIGHT = SCREEN_WIDTH / GRID_SIZE

GRID_LOCATIONS = []
for x in range(int(GRID_HEIGHT)):
    for y in range(int(GRID_WIDTH)):
        GRID_LOCATIONS.insert(0, (float(x * GRID_SIZE), float(x * GRID_SIZE)))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
game_running = True


def main():
    #Function to start the Snake Game
    play_game()


main()
