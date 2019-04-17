# Code inspired by apoddar573 at https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa and https://github.com/apoddar573/Tic-Tac-Toe-Gym_Environment/tree/master/gym-tictac4/gym_tictac4
import gym
import gym_tictactoe

def main():
    env = gym.make('tictactoe-v0')
    env.play()


if __name__ == '__main__':
    main()
