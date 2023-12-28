import torch
import numpy as np
from game_ai import SnakeGameAI, Direction, Point, BLOCK_SIZE
from collections import deque
from game_ai.model import Linear_QNet, QTrainer
import game_ai.utils as utils

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 # learning rate

class Agent:

    def __init__(self):
        self.count_games = 0
        self.epsilon = 0 # randomnes
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]

        #points arround the head
        point_r = Point(head.x - BLOCK_SIZE, head.y)
        point_l = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y  - BLOCK_SIZE)
        point_d = Point(head.x - BLOCK_SIZE, head.y  + BLOCK_SIZE)

        danger_straight = False
        danger_left = False
        danger_right = False

        dir_l = False
        dir_r = False
        dir_u = False
        dir_d = False

        if game.direction == Direction.RIGHT:
            dir_r = True
            danger_straight = game.collision(point_r)
            danger_left = game.collision(point_d)
            danger_right = game.collision(point_u)
        
        elif game.direction == Direction.LEFT:
            dir_l = True
            danger_straight = game.collision(point_l)
            danger_left = game.collision(point_u)
            danger_right = game.collision(point_d)
        
        elif game.direction == Direction.UP:
            dir_u = True
            danger_straight = game.collision(point_u)
            danger_left = game.collision(point_l)
            danger_right = game.collision(point_d)

        if game.direction == Direction.DOWN:
            dir_d = True
            danger_straight = game.collision(point_d)
            danger_left = game.collision(point_r)
            danger_right = game.collision(point_l)

        state = [
                danger_straight,
                danger_left,
                danger_right,
                dir_l,
                dir_r,
                dir_u,
                dir_d,
                game.food.x < game.head.x,
                game.food.x > game.head.x,
                game.food.y < game.head.y,
                game.food.y > game.head.y,
                ]
        
        state = [0 if s is None else s for s in state]
        
        return np.array(state, dtype = int)

    def get_action(self, state):
        self.epsilon = (80 - self.count_games)/100
        final_move = [0,0,0]

        if np.random.random() < self.epsilon:
            move = np.random.randint(0,3) 
            final_move[move] = 1
        else:
            state0= torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            idx = torch.argmax(prediction).item()
            final_move[idx] = 1

    def store(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def train_long_memory(self, state, action, reward, next_state, done):
        if len(self.memory) > BATCH_SIZE:
            sample = np.random.choice(self.memory, BATCH_SIZE)
        else:
            sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

def train():
    scores = []
    mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # train short memory
        agent.store(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.count_games += 1

            if score > record:
                record = score
                agent.model.save()
            
            print('Game', agent.count_games, 'Score', score, 'Record', record)

            scores.append(score)
            total_score += score
            mean_score = total_score / agent.count_games
            mean_scores.append(mean_score)

            utils.plot(scores, mean_scores)

if __name__ == '__main__':
    train()