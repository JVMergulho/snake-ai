import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)

Point = namedtuple('Point', ['x','y'])

speed = 10
BLOCK_SIZE = 20

# Default colors
WHITE = (255,255,255)
BG_COLOR = (32, 52, 49)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
RED = (255,0,0)
GRID_COLOR = (18,29,13)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.game_step = 0

    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def _make_grid(self):
        for x in range(1, self.w + 1, BLOCK_SIZE):
            pygame.draw.line(self.display, GRID_COLOR, (1,x), (self.w, x), 2)
            pygame.draw.line(self.display, GRID_COLOR, (x, 1), (x, self.w), 2)

    def _update_ui(self):
        self.display.fill(BG_COLOR)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x + 2, point.y + 2, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x + 6, point.y + 6, BLOCK_SIZE - 8, BLOCK_SIZE - 8))
        
        pygame.draw.ellipse(self.display, RED, pygame.Rect(self.food.x + 4, self.food.y + 4, BLOCK_SIZE - 3 , BLOCK_SIZE - 3))

        self._make_grid()

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()
    
    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if action[0] == 1:
            direction = clock_wise[idx]
        elif action[1] == 1: # right turn
            next_idx = (idx + 1) % 4
            direction = clock_wise[next_idx]
        else: # left turn
            next_idx = (idx - 1) % 4
            direction = clock_wise[next_idx]

        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y)
    
    def _collision(self, point=None):
        if point is None:
            point = self.head
        if point.x > self.w - BLOCK_SIZE or point.x < 0 or point.y > self.h - BLOCK_SIZE or point.y < 0:
            return True
        
        if point in self.snake[1:]:
            return True

    def step(self):
        global speed
        self.game_step += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    if speed >= 10:
                        speed = speed - 5
                if event.key == pygame.K_2:
                    speed = speed + 5

        # 2. move
        self._move(action) #update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self._collision() or self.game_step > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(speed)
        # 6. return game over and score
        return reward, game_over, self.score