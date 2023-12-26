Project inspired by [Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake](https://www.youtube.com/watch?v=L8ypSXwyBds&t=17s)

State (11 boolean values)

[ 
    danger_straight, danger_right, danger_left
    direction_left, direction_right, direction_up, direction_down
    food_left,  food_right, food_up, food_down
]

Action (3 booleans)

[ straight, left, right ]

Model:
- 11 inputs
- 3 otputs

State -> Model -> Action

Deep Q Learning 

0. Initite Q value randomly                          
1. Choose action (model.predict(state) or random move)
2. Perform action
3. Meausre reward
4. Update Q value and train model. Return to step 1. 