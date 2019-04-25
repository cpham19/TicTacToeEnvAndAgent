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

class TicTacToeAgent(PlayerAgent):
	def __init__(self, mark):
		super().__init__(mark)
		self.learning_rate = 0.5
		self.discount_factor = 0.01
		self.exploration_rate = 0.33

		self.q_states = {}
		self.state_order = []

		self.mark = mark

	# Transcode the state matrix into a string (used for recording the state before making the winning move)
	def serializeState(self, state):
		string = ""
		for row in range(0, len(state)):
			for col in range(0, len(state[row])):
				if(state[row][col] == 'O'):
					string += '1'
				elif(state[row][col] == 'X'):
					string += '2'
				else:
					string += '0'

		return string

	# Determine the move for bot
	def action(self, state):
		# One dimensionl array of the current state of the game
		current_state = np.array(state).ravel()

		# State key for recording movements
		state_key = self.serializeState(state)

		# Determining if the bot explores or not
		exploration = np.random.random() < self.exploration_rate

		possible_moves = []

		# Checking if the board only has one move left
		for i in range(0, 9):
			if (current_state[i] == " "):
				possible_moves.append(i)

		if (len(possible_moves) == 1):
			move = possible_moves[0]
			self.state_order.append((state_key, move))
			return move


		possible_moves = []
		# For Exploiting: If the bot remembers the current state, it can make a calculated move
		if (not exploration and state_key in self.q_states):
			print("EXPLOITING")
			# Get the q values of the currnt state (these are the numbers that are constantly changing after rewarding and punishing the bot)
			state_values = self.q_states[state_key].ravel()
			print(state_values)

			max_reward = np.max(state_values)
			for i in range(0, 9):
				if (state_values[i] == max_reward):
					possible_moves.append(i)


		# For Exploring: Making a random move based on the current state
		else:
			print("EXPLORING")
			for i in range(0, 9):
				if (current_state[i] == ' '):
					possible_moves.append(i)

		move = random.choice(possible_moves)
		self.state_order.append((state_key, move))
		return move


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

		# Pointless if you and the bot knows how to make proper moves!!! (for example, prevent the player from pressing a square on a GUI or rerandomizing a random move from a bot if it's invalid)
		if self.state[int(target/3)][target%3] != " ":
			print("Invalid Step")
			self.validMove = False

		else:
			self.state[int(target/3)][target%3] = mark
			self.validMove = True
			self.turns += 1
			if(self.turns == 9):
				self.done = 1;

		checkState = self.check()

		# Reward Bot for winning/Punish Bot for losing
		if(checkState['win'] == True):
			self.done = 1;

			if (checkState['winner'] == "Player"):
				print("Player wins.", sep="", end="\n")
				self.rewardBot(-1)
				self.playerWins += 1
			else:
				print("CPU wins.", sep="", end="\n")
				self.rewardBot(1)
				self.cpuWins += 1

		# If the game's outcome is draw
		elif (checkState['win'] == False and self.done == 1):
			self.draws += 1
			self.rewardBot(0.5)
			print("DRAW! No one wins!")

		stateObj['state'] = self.state
		stateObj['done'] = self.done
		stateObj['winner'] = checkState['winner']
		stateObj['validMove'] = self.validMove

		return stateObj

	# Rewarding or Punishing the bot
	def rewardBot(self, reward):
		# Last move made by bot
		last_state_key, last_move = self.cpu.state_order.pop()

		# Zero matrix
		self.cpu.q_states[last_state_key] = np.zeros((3, 3))
		# Rewarding the state
		self.cpu.q_states[last_state_key].itemset(last_move, reward)

		# Going through the rest of the moves that the bot has made
		while (self.cpu.state_order):
			# Move made by bot
			state_key, move = self.cpu.state_order.pop()

			# Reducing reward
			reward *= self.cpu.discount_factor

			# Calculating temporal difference
			old_state = self.cpu.q_states.get(state_key, np.zeros((3, 3)))
			temporal_difference = self.cpu.learning_rate * ((reward * self.cpu.q_states[last_state_key]) - old_state)

			# State was encountered before so we increase the reward
			if (state_key in self.cpu.q_states):
				reward += temporal_difference.item(last_move)
				self.cpu.q_states[state_key].itemset(move, reward)

			# State was not encountered before so we set the reward to a new one
			else:
				# Assign a new key to the array of states
				self.cpu.q_states[state_key] = np.zeros((3,3))
				reward = temporal_difference.item(last_move)
				self.cpu.q_states[state_key].itemset(move, reward)

			# Last state key and move are now the previous state key and move (as we pop moves out of the state_order array)
			last_state_key = state_key
			last_move = move



	#Reset the board and counters
	def reset(self):
		# Randomize the player who goes first
		#self.turn = 'Player' if (random.randint(0, 1) == 0) else 'CPU'
		self.turn = 'CPU'
		self.state = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
		self.turns = 0
		self.done = 0
		self.validMove = True

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

	# Train the bot
	def train(self):
		self.player = PlayerAgent('O')
		self.cpu = TicTacToeAgent('X')

		for i in range(1,1000):
			print("Game #" + str(i) + "\n")
			self.reset()

			while (True):
				stateObj = None
				action = self.cpu.action(self.state)
				stateObj = self.step(action, self.cpu.mark)
				print(stateObj)
				self.render()

				if (stateObj['done'] == 1):
					print("Q_STATES\n--------")
					print(self.cpu.q_states)
					print("\n--------------------------------------------------------------------------------------")

					print("Game #" + str(i) + " done!\n------------------------------------------------------------------------------------------------------\n")
					break

	# Play Tic Tac Toe game for a specified amount
	def play(self):
		self.player = PlayerAgent('O')
		self.cpu = TicTacToeAgent('X')

		for i in range(1,10000):
			print("Game #" + str(i) + "\n")
			self.reset()

			while (True):
				stateObj = None
				if(self.turn == "Player"):
					print("Player's Turn\n-------------")
					action = self.player.action(self.state)
					print("Player selects " + str(action))
					stateObj = self.step(action, self.player.mark)
					self.turn = 'CPU'
					print(stateObj)
					self.render()

				else:
					print("CPU's Turn\n-------------")
					action = self.cpu.action(self.state)
					print("CPU selects " + str(action))
					stateObj = self.step(action, self.cpu.mark)
					print(stateObj)
					self.render()

					while(stateObj['validMove'] != True):
						print("CPU's Turn\n-------------")
						action = self.cpu.action(self.state)
						print("CPU selects " + str(action))
						stateObj = self.step(action, self.cpu.mark)
						print(stateObj)
						self.render()

					self.turn = 'Player'

				if (stateObj['done'] == 1):
					print("Game #" + str(i) + " done!\n------------------------------------------------------------------------------------------------------\n")
					break

		print("Player Wins (" + self.player.mark + "): " + str(self.playerWins) +
			  " | CPU Wins (" + self.cpu.mark + "): " + str(self.cpuWins) +
			  " | Draws: " + str(self.draws))