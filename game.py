import pygame
import random
import time
import os
from enum import Enum
from collections import namedtuple
from buttom import Buttom

pygame.init()
font = pygame.font.SysFont('arial', 25)

Point = namedtuple('Point', ['x','y'])

BLOCK_SIZE = 20
speed = 10
WHITE = (255,255,255)
BG_COLOR = (32, 60, 49)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
RED = (255,0,0)
GRAY = (128, 128, 128)
GRID_COLOR = (18,29,13)

score_sfx = pygame.mixer.Sound(os.path.join('assets', 'score.flac')) 
hit_sfx = pygame.mixer.Sound(os.path.join('assets', 'hit.wav')) 
theme_sfx = pygame.mixer.Sound(os.path.join('assets', 'theme.mp3')) 
score_sfx.set_volume(0.7)
theme_sfx.set_volume(0.5)
# game_over_sfx = pygame.mixer.Sound(os.path.join('assets', 'game_over.wav'))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self._reset()

    def _reset(self):
        self.direction = Direction.RIGHT
        self.pause = False

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]

        self.score = 0
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

    def _pause_menu(self):
        surface = pygame.Surface([self.w, self.h], pygame.SRCALPHA)
        pygame.draw.rect(surface, (*GRAY, 150), pygame.Rect(0, 0, self.w, self.h))
        self.display.blit(surface, (0,0))

        btn_resume = Buttom(self.display, 390, 200, 100, 50, (20, 80, 0))
        btn_resume.write('Resume', WHITE)

        btn_reset = Buttom(self.display, 150, 200, 100, 50, (20, 80, 0))
        btn_reset.write('Reset', WHITE)

        if btn_reset.draw():
            self._reset()
        
        if btn_resume.draw():
            self.pause = False

    def _update_ui(self):
        self.display.fill(BG_COLOR)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x + 2, point.y + 2, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x + 6, point.y + 6, BLOCK_SIZE - 8, BLOCK_SIZE - 8))
        
        pygame.draw.ellipse(self.display, RED, pygame.Rect(self.food.x + 4, self.food.y + 4, BLOCK_SIZE - 3 , BLOCK_SIZE - 3))

        self._make_grid()

        pause_text = font.render("Pause: press space", True, WHITE)
        self.display.blit(pause_text, [0,0])
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(score_text, [0,28])
        
        if self.pause:
            self._pause_menu()

        pygame.display.flip()
    
    def _move(self, direction):
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
    
    def _collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        
        if self.head in self.snake[1:]:
            return True
        
    def step(self):

        global speed
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

                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause

                if not self.pause:
                    if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN

        game_over = False

        if not self.pause:
            # 2. move
            self._move(self.direction) #update the head
            self.snake.insert(0, self.head)

            # 3. check if game over
            if self._collision():
                hit_sfx.play()
                game_over = True
                return game_over, self.score
            # 4. place new food or just move
            if self.head == self.food:
                self.score += 1
                score_sfx.play(maxtime=300)

                # increases speed for each 5 points scored
                if self.score % 5 == 0:
                    speed += 2
                self._place_food()
            else:
                self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(speed)
        # 6. return game over and score
        return game_over, self.score

if __name__ == '__main__':
    game = SnakeGame()

    theme_sfx.play(loops=-1)

    while True:
        game_over, score = game.step()

        if game_over:
            # play theme song forever
            hit_sfx.play()
            time.sleep(1)
            break

    print('Final score', score)
    
    pygame.quit()
