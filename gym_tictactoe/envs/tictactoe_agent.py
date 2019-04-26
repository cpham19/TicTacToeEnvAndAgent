import random, numpy as np

class PlayerAgent:
	def __init__(self, name, mark):
		self.name = name
		self.mark = mark

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

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
	def __init__(self, name, mark):
		super().__init__(name, mark)
		self.learning_rate = 0.5
		self.discount_factor = 0.01
		self.exploration_rate = 0.33

		self.q_states = {}
		self.state_order = []

		self.name = name
		self.mark = mark

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

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

		print("POSSIBLE MOVES")
		print(possible_moves)
		move = random.choice(possible_moves)
		self.state_order.append((state_key, move))
		return move
