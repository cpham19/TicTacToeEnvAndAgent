# Code inspired by ...
# apoddar573 at https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa and https://github.com/apoddar573/Tic-Tac-Toe-Gym_Environment/
# giladariel at https://towardsdatascience.com/reinforcement-learning-and-deep-reinforcement-learning-with-tic-tac-toe-588d09c41dda and https://github.com/giladariel/TicTacToe_RL/
# AmreshVenugopal at https://github.com/AmreshVenugopal/tic_tac_toe

import gym
import gym_tictactoe
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent

def main():

    player = PlayerAgent('Player 1', 'O')
    cpu = TicTacToeAgent('Bot 1', 'X')
    env = gym.make('tictactoe-v0')
    env.init(player, cpu)
    env.train(30000)
    cpu.exploration_rate = 0.00
    env.play(30000)

    # cpu3 = TicTacToeAgent('Bot 3', 'O')
    # cpu4 = TicTacToeAgent('Bot 4', 'X')
    # env2 = gym.make('tictactoe-v0')
    # env2.init(cpu3, cpu4)
    # env2.play()


if __name__ == '__main__':
    main()
