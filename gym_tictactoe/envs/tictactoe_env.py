import gym, random, numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

class PlayerAgent:
	def __init__(self, mark):
		self.mark = mark

	@property
	def mark(self):
		return self.__mark

	@mark.setter
	def mark(self, mark):
		self.__mark = mark

	# Random move from player
	def action(self, state):
		numbers = []
		array = np.array(state).ravel()
		for i in range(0, 9):
			if (array[i] == ' '):
				numbers.append(i)
		move = random.sample(numbers, 1)[0]
		return move

class TicTacToeAgent:
	def __init__(self, mark):
		self.learning_rate = 0.5
		self.discount_factor = 0.01
		self.exploration_rate = 0.33
		self.mark = mark

		self.state_order = []

	@property
	def mark(self):
		return self.__mark

	@mark.setter
	def mark(self, mark):
		self.__mark = mark

	# Random move from bot
	def action(self, state):
		numbers = []
		array = np.array(state).ravel()
		for i in range(0, 9):
			if (array[i] == ' '):
				numbers.append(i)

		move = random.sample(numbers, 1)[0]
		return move

	# Transcode the state matrix into a string
	def serializeState(self, state):
		string = ""
		for row in range(0, len(self.state)):
			for col in range(0, len(self.state[row])):
				if(state[row][col] == 'O'):
					string += '1'
				elif(state[row][col] == 'X'):
					string += '2'
				else:
					string += '0'

		return string


class TicTacToe(gym.Env):
	metadata = {'render.modes': ['human']}

	"""
	Description:
		Tic Tac Toe is a simple game that you win by having the same marks on a row, column, or diagonal

    Observation: 
        Type: Discrete (9)
        Num		Observation
		0		First square in the first row is marked/unmarked
		1		Second square in the first row is marked/unmarked
		2		Third square in the first row is marked/unmarked
		3		First square in the second row is marked/unmarked
		4		Second square in the second row is marked/unmarked
		5		Third square in the second row is marked/unmarked
		6		First square in the third row is marked/unmarked
		7		Second square in the third row is marked/unmarked
		8		Third square in the third row is marked/unmarked
        
    Actions:
        Type: Discrete(9)
        Num	Action
        0	Mark the first square in the first row
        1	Mark the second square in the first row
        2	Mark the third square in the first row
        3	Mark the first square in the second row
        4	Mark the second square in the second row
        5	Mark the third square in the second row
        6	Mark the first square in the third row
        7	Mark the second square in the third row
        8	Mark the third square in the third row

    Reward:
        Reward is 100 for every step taken, including the termination step
        
    Starting State:
        The gameboard is empty.
        
    Episode Termination:
        The game is completed when someone wins by having three marks on a row, column, or diagonal or when the game reaches a draw by depleting the number of turns (9)
    """


	def __init__(self):
		self.games = 100
		self.playerWins = 0
		self.draws = 0
		self.cpuWins = 0
		self.reset()

	# Check if each column or row is occupied and has the same mark
	def checkRowsAndCols(self):
		stateObj = {'win': False, 'winner': "None"}
		for i in range(3):
			if (self.state[i][0] != " " and self.state[i][0] == self.state[i][1] and self.state[i][1] == self.state[i][2]):
				if (self.state[i][0] == "O" or self.state[0][i] == "O"):
					stateObj['winner'] = "Player" if (self.player.mark == "O") else "CPU"
					stateObj['win']  = True
				else:
					stateObj['winner'] =  "Player" if (self.player.mark == "X") else "CPU"
					stateObj['win'] = True
			elif(self.state[0][i] != " " and self.state[0][i] == self.state[1][i] and self.state[1][i] ==self.state[2][i]):
				if (self.state[0][i] == "O"):
					stateObj['winner'] = "Player" if (self.player.mark == "O") else "CPU"
					stateObj['win'] = True
				else:
					stateObj['winner'] = "Player" if (self.player.mark == "X") else "CPU"
					stateObj['win'] = True

		return stateObj

	# Check if minor or major diagonal is occupied and has the same mark
	def checkDiagonals(self):
		stateObj = {'win': False, 'winner': "None"}
		if (self.state[0][0] != " " and self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]):
			if (self.state[0][0] == "O"):
				stateObj['winner']  = "Player" if (self.player.mark == "O") else "CPU"
				stateObj['win'] = True
			else:
				stateObj['winner']  = "Player" if (self.player.mark == "X") else "CPU"
				stateObj['win'] = True
		elif (self.state[0][2] != " " and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]):
			if (self.state[0][2] == "O"):
				stateObj['winner']  = "Player" if (self.player.mark == "O") else "CPU"
				stateObj['win'] = True
			else:
				stateObj['winner']  = "Player" if (self.player.mark == "X") else "CPU"
				stateObj['win'] = True

		return stateObj

	# Check the game if someone won, if the game reaches a draw, or game is still going on
	def check(self):
		stateObj = {'win': False, 'winner': "None"}
		if (self.turns < 5):
			return stateObj

		outcome = self.checkDiagonals()
		if(outcome['win'] == True):
			return outcome

		outcome = self.checkRowsAndCols()
		if (outcome['win'] == True):
			return outcome

		return stateObj

	#  Change the state after every action made by player or computer
	def step(self, target, mark):
		stateObj = {}

		if self.state[int(target/3)][target%3] != " ":
			print("Invalid Step")
			return [self.state, self.reward, self.done, self.add]
		else:
			self.state[int(target/3)][target%3] = mark

			self.turns += 1
			if(self.turns == 9):
				self.done = 1;

		checkState = self.check()

		# If Someone wins
		if(checkState['win'] == True):
			self.games += 1
			self.done = 1;

			if (checkState['winner'] == "Player"):
				print("Player wins.", sep="", end="\n")
				self.add[0] = 1;
				self.reward = -100
				self.playerWins += 1
			else:
				print("CPU wins.", sep="", end="\n")
				self.add[1] = 1;
				self.reward = 100
				self.cpuWins += 1

		# If the game's outcome is draw
		elif (checkState['win'] == False and self.done == 1):
			self.draws += 1
			print("DRAW! No one wins!")

		stateObj['state'] = self.state
		stateObj['reward'] = self.reward
		stateObj['done'] = self.done
		stateObj['add'] = self.add

		return stateObj

	# Reset the board and counters
	def reset(self):
		# Randomize the player who goes first
		self.turn = 'Player' if (random.randint(0, 1) == 0) else 'CPU'
		self.state = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
		self.turns = 0
		self.done = 0
		self.add = [0, 0]
		self.reward = 0

		return self.state

	# Print the Tic Tac Toe board
	def render(self):
		for row in range(3):
			for col in range(3):
				if (col != 2):
					print(self.state[row][col], end=" | ")
				else:
					print(self.state[row][col], end=" ")
			if (row != 2):
				print('\n---------')
		print("\n")

	# Play Tic Tac Toe game for a specified amount
	def play(self):
		self.player = PlayerAgent('O')
		self.cpu = TicTacToeAgent('X')

		for i in range(1, 101):
			print("Game #" + str(i) + "\n")
			self.reset()

			while (True):
				stateObj = None
				if(self.turn == "Player"):
					action = self.player.action(self.state)
					mark = self.player.mark
					stateObj = self.step(action, mark)
					self.turn = 'CPU'
				else:
					action = self.cpu.action(self.state)
					mark = self.cpu.mark
					stateObj = self.step(action, mark)
					self.turn = 'Player'

				print(stateObj)
				self.render()

				if (stateObj['done'] == 1):
					print("Game #" + str(i) + " done!\n------------------------------------------------------------------------------------------------------\n")
					break

		print("Player Wins (" + self.player.mark + "): " + str(self.playerWins) +
			  " | CPU Wins (" + self.cpu.mark + "): " + str(self.cpuWins) +
			  " | Draws: " + str(self.draws))