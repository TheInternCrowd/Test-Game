import keyboard
import pygame
import sys
import random
import keyword


class Player:
    def __int__(self):
        self.position = ((SCREEN_WIDTH - GRID_SIZE) / 2, SCREEN_HEIGHT - GRID_SIZE)
        self.color = (20, 20, 200)
        self.alive = True

    def get_position(self):
        return self.position

    def move(self, dir):
        if dir is "LEFT":
            self.position = (COLUMN_LEFT_X, COLUMN_BOTTOM_Y)
        elif dir is "CENTER":
            self.position = (COLUMN_CENTER_X, COLUMN_BOTTOM_Y)
        elif dir is "RIGHT":
            self.position = (COLUMN_RIGHT_X, COLUMN_BOTTOM_Y)

    def draw(self, surface):
        player_outline = (117, 148, 56)
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, player_outline, r, 1)
        return

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.move("RIGHT")
            else:
                self.move("CENTER")


class Car:
    def __int__(self, spaces_back):
        self.position = (random.choice(COLUMN_X_CHOICES), COLUMN_TOP_Y - (spaces_back * GRID_SIZE))
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def draw(self, surface):
        car_outline = (80, 2, 15)
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, car_outline, r, 2)

    def move(self):
        self.position = (self.position[0], self.position[1] + GRID_SIZE)

    def reset_position(self):
        self.position = (random.choice(COLUMN_X_CHOICES), COLUMN_TOP_Y)
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def get_position(self):
        return self.position


def game_over():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    myfont = pygame.font.SysFont("monospace", 16)

    # Text for the game being over and asking user to play again
    game_over_text = myfont.render("GAME OVER", True, (255, 255, 255))
    play_again_text = myfont.render("Press Space to play again!", True, (255, 255, 255))

    # Update screen with new text
    pygame.display.update(screen.blit(game_over_text, (200, 200)))
    pygame.display.update(screen.blit(play_again_text, (125, 225)))

    # If space is pressed then it will restart the game
    if keyboard.is_pressed(" "):
        play_game()


def play_game():
    # Init the game
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    player = Player()
    player.__int__()

    cars = [Car() for i in range(CAR_NUM)]
    for i in range(CAR_NUM):
        cars[i].__int__(4*i)

    # Font for the game text
    myfont = pygame.font.SysFont("monospace", 16)

    # Track the score
    score = 0
    start_time = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if keyboard.is_pressed("q"):
            sys.exit()
        if player.alive:
            clock.tick(FRAME_RATE)
            ticks = pygame.time.get_ticks()
            if ticks - start_time > (SPAWN_DELAY_SECONDS * 1000):
                start_time = ticks

                for car in cars:
                    car.move()
                    if car.get_position() == player.get_position():
                        player.alive = False
                    else:
                        if car.position[1] > SCREEN_HEIGHT:
                            car.reset_position()
                            score = score + 1

            player.handle_keys()
            drawGrid(surface)

            player.draw(surface)

            for car in cars:
                car.draw(surface)

            screen.blit(surface, (0, 0))
            text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
            screen.blit(text, (5, 10))
            pygame.display.update()

        else:
            # If a car hits the player then end the game
            game_over()


def drawGrid(surface):
    for x in range(0, int(GRID_WIDTH)):
        for y in range(0, int(GRID_HEIGHT)):
            if x == 1 or x == 4 or x == 7:
                tile_color = (212, 227, 236)

            else:
                tile_color = (204, 204, 204)

            r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, tile_color, r)


SPAWN_DELAY_SECONDS = .25

GRID_SIZE = 60

SCREEN_WIDTH = GRID_SIZE * 9
SCREEN_HEIGHT = GRID_SIZE * 9

GRID_WIDTH = SCREEN_HEIGHT / GRID_SIZE
GRID_HEIGHT = SCREEN_WIDTH / GRID_SIZE

COLUMN_LEFT_X = GRID_SIZE
COLUMN_CENTER_X = (SCREEN_WIDTH - GRID_SIZE) / 2
COLUMN_RIGHT_X = SCREEN_WIDTH - (GRID_SIZE * 2)
COLUMN_X_CHOICES = [COLUMN_LEFT_X, COLUMN_CENTER_X, COLUMN_RIGHT_X]

COLUMN_BOTTOM_Y = SCREEN_HEIGHT - GRID_SIZE
COLUMN_TOP_Y = 0

FRAME_RATE = 5

CAR_NUM = 2

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
game_running = True

# Function to start the Snake Game
play_game()
