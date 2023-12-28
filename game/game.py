import pygame
import random
import time
import os
from enum import Enum
from utils import Point, Color, Size
from button import Button

pygame.init()
font = pygame.font.SysFont('arial', 25)

default_speed = 10

score_sfx = pygame.mixer.Sound(os.path.join('assets', 'score.flac')) 
hit_sfx = pygame.mixer.Sound(os.path.join('assets', 'hit.wav')) 
break_sfx = pygame.mixer.Sound(os.path.join('assets', 'break.wav')) 
score_sfx.set_volume(0.7)
# game_over_sfx = pygame.mixer.Sound(os.path.join('assets', 'game_over.wav'))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:

    def __init__(self, w=640, h=480, control = 1):

        pygame.mixer.music.stop()

        self.control = control
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        pygame.mixer.music.load(os.path.join('assets', 'theme.mp3'))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self._reset()

    def _reset(self):
        self.obstacles = []
        self.direction = Direction.RIGHT
        self.pause = False
        self.power_up = False
        self.color_score = Color.RED
        self.speed = default_speed

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - Size.BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*Size.BLOCK_SIZE), self.head.y)]

        self.score = 0
        self._place_food()
    
    def _place_food(self):
        while True:
            x = random.randint(0, (self.w - Size.BLOCK_SIZE)//Size.BLOCK_SIZE)*Size.BLOCK_SIZE
            y = random.randint(0, (self.h - Size.BLOCK_SIZE)//Size.BLOCK_SIZE)*Size.BLOCK_SIZE
            self.food = Point(x,y)
            if (not self.food in self.snake) and (not self.food in self.obstacles):
                break
        
        if random.randint(0, 10) == 1:
            self.color_score  = Color.YELLOW
        else:
            self.color_score = Color.RED

    def _make_grid(self):
        for x in range(1, self.w + 1, Size.BLOCK_SIZE):
            pygame.draw.line(self.display, Color.GRID_COLOR, (1,x), (self.w, x), 2)
            pygame.draw.line(self.display, Color.GRID_COLOR, (x, 1), (x, self.w), 2)

    def _pause_menu(self):
        surface = pygame.Surface([self.w, self.h], pygame.SRCALPHA)
        pygame.draw.rect(surface, (*Color.GRAY, 150), pygame.Rect(0, 0, self.w, self.h))
        self.display.blit(surface, (0,0))

        btn_resume = Button(self.display, 440, 200, 100, 50, Color.BTN_COLOR)
        btn_resume.write('Resume', Color.WHITE)

        btn_reset = Button(self.display, 200, 200, 100, 50, Color.BTN_COLOR)
        btn_reset.write('Reset', Color.WHITE)

        if btn_reset.draw():
            self._reset()
        
        if btn_resume.draw():
            self.pause = False

    def _update_ui(self):
        self.display.fill(Color.BG_COLOR)

        for point in self.snake:
            if self.power_up:
                pygame.draw.rect(self.display, Color.YELLOW, pygame.Rect(point.x + 2, point.y + 2, Size.BLOCK_SIZE - 2, Size.BLOCK_SIZE - 2))
            else:
                pygame.draw.rect(self.display, Color.BLUE1, pygame.Rect(point.x + 2, point.y + 2, Size.BLOCK_SIZE- 2, Size.BLOCK_SIZE- 2))
                pygame.draw.rect(self.display, Color.BLUE2, pygame.Rect(point.x + 6, point.y + 6, Size.BLOCK_SIZE - 8, Size.BLOCK_SIZE - 8))
        
        for point in self.obstacles:
            pygame.draw.rect(self.display, Color.GRAY, pygame.Rect(point.x+ 2, point.y+ 2, Size.BLOCK_SIZE - 2, Size.BLOCK_SIZE - 2))
        
        pygame.draw.ellipse(self.display, self.color_score, pygame.Rect(self.food.x + 4, self.food.y + 4, Size.BLOCK_SIZE - 3 , Size.BLOCK_SIZE - 3))

        self._make_grid()

        pause_text = font.render("Pause: press space", True, Color.WHITE)
        self.display.blit(pause_text, [0,0])
        score_text = font.render("Score: " + str(self.score), True, Color.WHITE)
        self.display.blit(score_text, [0,28])
        
        if self.pause:
            self._pause_menu()

        pygame.display.flip()
    
    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += Size.BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= Size.BLOCK_SIZE
        elif direction == Direction.UP:
            y -= Size.BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += Size.BLOCK_SIZE

        self.head = Point(x,y)

    def _make_obstacles(self):

        for obs in self.snake[1:]:
            self.obstacles.append(obs)

    def _collision(self):
        if self.head.x > self.w - Size.BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - Size.BLOCK_SIZE or self.head.y < 0:
            return True
        
        if (self.head in self.snake[1:]) or (self.head in self.obstacles and not self.power_up):
            return True
        
        # destroy obstacle
        if self.head in self.obstacles and self.power_up:
            self.obstacles.remove(self.head)
            break_sfx.play(maxtime=400)
        
        return False
        
    def step(self):

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    if self.speed >= 10:
                        self.speed = self.speed - 5
                if event.key == pygame.K_2:
                    self.speed = self.speed + 5

                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause

                if not self.pause:
                    if self.control == 1:
                        if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                            self.direction = Direction.LEFT
                        elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                            self.direction = Direction.RIGHT
                        elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                            self.direction = Direction.UP
                        elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                            self.direction = Direction.DOWN
                    else:
                        if event.key == pygame.K_a and self.direction != Direction.RIGHT:
                            self.direction = Direction.LEFT
                        elif event.key == pygame.K_d and self.direction != Direction.LEFT:
                            self.direction = Direction.RIGHT
                        elif event.key == pygame.K_w and self.direction != Direction.DOWN:
                            self.direction = Direction.UP
                        elif event.key == pygame.K_s and self.direction != Direction.UP:
                            self.direction = Direction.DOWN

        game_over = False

        if not self.pause:
            # 2. move
            self._move(self.direction) #update the head
            self.snake.insert(0, self.head)

            # 3. check if game over
            if self._collision():
                hit_sfx.play()
                time.sleep(1)
                game_over = True
                return game_over, self.score
            # 4. place new food or just move

            if self.head == self.food:
                self.score += 1
                score_sfx.play(maxtime=300)
                self._make_obstacles()

                self.power_up = (self.color_score == Color.YELLOW)

                self._place_food()

                # increases self.speed for each 5 points scored
                if self.score % 5 == 0:
                    self.speed += 2
            else:
                self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.speed)
        # 6. return game over and score
        return game_over, self.score 

def play_game(control = 1):
    game = SnakeGame(control = control)

    while True:
        game_over, score = game.step()

        if game_over:
            print('Final score', score)
            return score
