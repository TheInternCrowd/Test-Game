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
        #Comment out Kazim and surface.blitz if you want to remove 8-Bit Kazim
        player_outline = (117, 148, 56)
        kazim = pygame.image.load("8-Bit_Kazim.png")
        kazim = pygame.transform.scale(kazim, (GRID_SIZE, GRID_SIZE))
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        #pygame.draw.rect(surface, self.color, r)
        #pygame.draw.rect(surface, player_outline, r, 1)
        surface.blit(kazim, r)
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


CAR_NUM = 2
CAR_MOVE_DELAY_SECONDS = .25

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

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Game:
    def __int__(self):
        self.player = Player()
        self.player.__int__()
        self.cars = [Car() for i in range(CAR_NUM)]
        for i in range(CAR_NUM):
            self.cars[i].__int__(self.car_space(i))

        # Init the game
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.drawGrid()

        # Font for the game text
        self.font = pygame.font.SysFont("monospace", 16)

        # Track the current score
        self.score = 0

        self.start_time = 0

    def drawGrid(self):
        for x in range(0, int(GRID_WIDTH)):
            for y in range(0, int(GRID_HEIGHT)):
                if x == 1 or x == 4 or x == 7:
                    tile_color = (212, 227, 236)

                else:
                    tile_color = (204, 204, 204)

                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.surface, tile_color, r)

    def run_game_frame(self, direction):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if keyboard.is_pressed("q"):
            sys.exit()

        if self.player.alive:
            self.clock.tick(FRAME_RATE)
            ticks = pygame.time.get_ticks()
            if ticks - self.start_time > (CAR_MOVE_DELAY_SECONDS * 1000):
                self.start_time = ticks
                for car in self.cars:
                    car.move()
                    if car.get_position() == self.player.get_position():
                        self.player.alive = False
                    else:
                        if car.position[1] > SCREEN_HEIGHT:
                            car.reset_position()
                            self.score += 1

            self.player.move(direction)
            self.drawGrid()

            self.player.draw(self.surface)

            for car in self.cars:
                car.draw(self.surface)

            self.screen.blit(self.surface, (0, 0))
            text = self.font.render("Score {0}".format(self.score), 1, (0, 0, 0))
            self.screen.blit(text, (5, 10))
            pygame.display.update()

        else:
            # If a car hits the player then end the game
            self.game_over()

    def game_over(self):
        # Text for the game being over and asking user to play again
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        play_again_text = self.font.render("Press Space to play again!", True, (255, 255, 255))

        # Update screen with new text
        pygame.display.update(self.screen.blit(game_over_text, (200, 200)))
        pygame.display.update(self.screen.blit(play_again_text, (125, 225)))

        # If space is pressed then it will restart the game
        if keyboard.is_pressed(" "):
            self.__int__()

    def car_space(self, index):
        return 4 * index;


# Initialize the game
game = Game()
game.__int__()

while True:
    # Determine the keystroke
    key = ""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key = "LEFT"
            elif event.key == pygame.K_RIGHT:
                key = "RIGHT"
        else:
            key = "CENTER"
    # Run the game for one frame
    game.run_game_frame(key)