# Code inspired by ...
# apoddar573 at https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa and https://github.com/apoddar573/Tic-Tac-Toe-Gym_Environment/
# giladariel at https://towardsdatascience.com/reinforcement-learning-and-deep-reinforcement-learning-with-tic-tac-toe-588d09c41dda and https://github.com/giladariel/TicTacToe_RL/
# AmreshVenugopal at https://github.com/AmreshVenugopal/tic_tac_toe

import gym
import gym_tictactoe

def main():
    env = gym.make('tictactoe-v0')
    env.play()

    #env.train()


if __name__ == '__main__':
    main()
