import gym, numpy as np, random
from gym import error, spaces, utils
from gym.utils import seeding
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent

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
		self.player1Wins = 0
		self.player2Wins = 0
		self.state = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
		self.turns = 0
		self.done = 0
		self.validMove = True
		self.draws = 0

	def init(self, player1, player2):
		self.player1 = player1
		self.player2 = player2

	# Check if each column or row is occupied and has the same mark
	def checkRowsAndCols(self):
		stateObj = {'win': False, 'winner': "None"}
		for i in range(3):
			if (self.state[i][0] != " " and self.state[i][0] == self.state[i][1] and self.state[i][1] == self.state[i][2]):
				if (self.state[i][0] == "O" or self.state[0][i] == "O"):
					stateObj['winner'] = self.player1.name if (self.player1.mark == "O") else self.player2.name
					stateObj['win']  = True
				else:
					stateObj['winner'] =  self.player1.name if (self.player1.mark == "X") else self.player2.name
					stateObj['win'] = True
			elif(self.state[0][i] != " " and self.state[0][i] == self.state[1][i] and self.state[1][i] ==self.state[2][i]):
				if (self.state[0][i] == "O"):
					stateObj['winner'] = self.player1.name if (self.player1.mark == "O") else self.player2.name
					stateObj['win'] = True
				else:
					stateObj['winner'] = self.player1.name if (self.player1.mark == "X") else self.player2.name
					stateObj['win'] = True

		return stateObj

	# Check if minor or major diagonal is occupied and has the same mark
	def checkDiagonals(self):
		stateObj = {'win': False, 'winner': "None"}
		if (self.state[0][0] != " " and self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]):
			if (self.state[0][0] == "O"):
				stateObj['winner']  = self.player1.name if (self.player1.mark == "O") else self.player2.name
				stateObj['win'] = True
			else:
				stateObj['winner']  = self.player1.name if (self.player2.mark == "X") else self.player2.name
				stateObj['win'] = True
		elif (self.state[0][2] != " " and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]):
			if (self.state[0][2] == "O"):
				stateObj['winner']  = self.player1.name if (self.player1.mark == "O") else self.player2.name
				stateObj['win'] = True
			else:
				stateObj['winner']  = self.player1.name if (self.player1.mark == "X") else self.player2.name
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
			if (mark == self.player1.mark and type(self.player1) == TicTacToeAgent):
				self.punishBotForInvalidMove(self.player1, -0.5)
			elif (mark == self.player2.mark and type(self.player2) == TicTacToeAgent):
				self.punishBotForInvalidMove(self.player2, -0.5)

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

			if (checkState['winner'] == self.player1.name):
				print(self.player1.name + " wins.", sep="", end="\n")
				if (type(self.player1) == TicTacToeAgent):
					self.rewardBot(self.player1, 1)

				if (type(self.player2) == TicTacToeAgent):
					self.rewardBot(self.player2, -1)

				self.player1Wins += 1
			else:
				print(self.player2.name + " wins.", sep="", end="\n")
				if (type(self.player2) == TicTacToeAgent):
					self.rewardBot(self.player2, 1)

				if (type(self.player1) == TicTacToeAgent):
					self.rewardBot(self.player1, -1)

				self.player2Wins += 1

		# If the game's outcome is draw
		elif (checkState['win'] == False and self.done == 1):
			self.draws += 1
			if (type(self.player1) == TicTacToeAgent):
				self.rewardBot(self.player1, 0.5)

			if (type(self.player2) == TicTacToeAgent):
				self.rewardBot(self.player2, 0.5)

			print("DRAW! No one wins!")

		stateObj['state'] = self.state
		stateObj['done'] = self.done
		stateObj['winner'] = checkState['winner']
		stateObj['validMove'] = self.validMove

		return stateObj

	def punishBotForInvalidMove(self, player, reward):
		# Last move made by player
		last_state_key, last_move = player.state_order.pop()
		# Zero matrix
		player.q_states[last_state_key] = np.zeros((3, 3))
		# Punishing the player's invalid mod
		player.q_states[last_state_key].itemset(last_move, reward)

	# Rewarding or Punishing the bot
	def rewardBot(self, player, reward):
		# Last move made by bot
		last_state_key, last_move = player.state_order.pop()

		# Zero matrix
		player.q_states[last_state_key] = np.zeros((3, 3))
		# Rewarding or punishing the state
		player.q_states[last_state_key].itemset(last_move, reward)

		# Going through the rest of the moves that the bot has made
		while (player.state_order):
			# Move made by bot
			state_key, move = player.state_order.pop()

			# Reducing reward
			reward *= player.discount_factor

			# Calculating temporal difference
			old_state = player.q_states.get(state_key, np.zeros((3, 3)))
			temporal_difference = player.learning_rate * ((reward * player.q_states[last_state_key]) - old_state)

			# State was encountered before so we increase the reward
			if (state_key in player.q_states):
				reward += temporal_difference.item(last_move)
				player.q_states[state_key].itemset(move, reward)

			# State was not encountered before so we set the reward to a new one
			else:
				# Assign a new key to the array of states
				player.q_states[state_key] = np.zeros((3,3))
				reward = temporal_difference.item(last_move)
				player.q_states[state_key].itemset(move, reward)

			# Last state key and move are now the previous state key and move (as we pop moves out of the state_order array)
			last_state_key = state_key
			last_move = move


	#Reset the board and counters
	def reset(self):
		# Randomize the player who goes first
		self.turn = self.player1.mark if (random.randint(0, 1) == 0) else self.player2.mark
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

	# Play Tic Tac Toe game for a specified amount
	def play(self):
		for i in range(1,1000):
			print("Game #" + str(i) + "\n")
			self.reset()

			while (True):
				stateObj = None
				if(self.turn == self.player1.name):
					print(self.player1.name + "'s Turn\n-------------")
					action = self.player1.action(self.state)
					print(self.player1.name + " selects " + str(action))
					stateObj = self.step(action, self.player1.mark)
					self.turn = self.player2.name
					print(stateObj)
					self.render()

					while (type(self.player1) == TicTacToeAgent and stateObj['validMove'] != True):
						print(self.player1.name + "'s Turn\n-------------")
						action = self.player1.action(self.state)
						print(self.player1.name + " selects " + str(action))
						stateObj = self.step(action, self.player1.mark)
						print(stateObj)
						self.render()

				else:
					print(self.player2.name + "'s Turn\n-------------")
					action = self.player2.action(self.state)
					print(self.player2.name + " selects " + str(action))
					stateObj = self.step(action, self.player2.mark)
					self.turn = self.player1.name
					print(stateObj)
					self.render()

					while(type(self.player2) == TicTacToeAgent and stateObj['validMove'] != True):
						print(self.player2.name + "'s Turn\n-------------")
						action = self.player2.action(self.state)
						print(self.player2.name + " selects " + str(action))
						stateObj = self.step(action, self.player2.mark)
						print(stateObj)
						self.render()

				if (stateObj['done'] == 1):
					print("Game #" + str(i) + " done!\n------------------------------------------------------------------------------------------------------\n")
					break

		print(self.player1.name + " Wins (" + self.player1.mark + "): " + str(self.player1Wins) + "\n"
			  + self.player2.name + " Wins (" + self.player2.mark + "): " + str(self.player2Wins) + "\n"
			  + "Draws: " + str(self.draws))


		# print()
		#
		# for state in sorted (self.cpu.q_states):
		# 	print(state)
		# 	print(np.array(self.cpu.q_states[state]).ravel())