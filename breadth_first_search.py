# Python code to display the way from the root  
# node to the final destination node for 8 puzzle  
# algorithm

# Importing the numpy for method  
import sys
import numpy as np

# node  structure 
class Node:
	def __init__(self, state, parent, action):
		self.state = state
        # This will store the parent node to the  
        # current node 
		self.parent = parent
		self.action = action


class StackFrontier:
	def __init__(self):
		self.frontier = []

	def add(self, node):
		self.frontier.append(node)

	def has_state(self, state):
		return any((node.state[0] == state[0]).all() for node in self.frontier)
	
	def empty(self):
		return len(self.frontier) == 0
	
	def remove(self):
		if self.empty():
			raise Exception("Empty Stack")
		else:
			node = self.frontier[-1]
			self.frontier = self.frontier[:-1]
			return node


class QueueFrontier(StackFrontier):
	def remove(self):
		if self.empty():
			raise Exception("Empty Queue")
		else:
			node = self.frontier[0]
			self.frontier = self.frontier[1:]
			return node


class PuzzleDfs:
	def __init__(self, start, startIndex, goal, goalIndex):
		self.start = [start, startIndex]
		self.goal = [goal, goalIndex] 
		self.solution = None

	def neighbors(self, state):
		mat, (row, col) = state
		results = []
		
		if row > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row - 1][col]
			mat1[row - 1][col] = 0
			results.append(('up', [mat1, (row - 1, col)]))
		if col > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col - 1]
			mat1[row][col - 1] = 0
			results.append(('left', [mat1, (row, col - 1)]))
		if row < 2:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row + 1][col]
			mat1[row + 1][col] = 0
			results.append(('down', [mat1, (row + 1, col)]))
		if col < 2:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col + 1]
			mat1[row][col + 1] = 0
			results.append(('right', [mat1, (row, col + 1)]))

		return results
    
# func to print the results
	def print(self):
		solution = self.solution if self.solution is not None else None
		print("Initial:\n", self.start[0], "\n")
		print("Final :\n",  self.goal[0], "\n")
		print("\n Explored: ", self.num_explored, "\n")
		for action, cell in zip(solution[0], solution[1]):
			print("Movement: ", action, "\n", cell[0], "\n")
		print("Final attained!!")

	def lacks_state(self, state):
		for st in self.explored:
			if (st[0] == state[0]).all():
				return False
		return True
	
	def solve(self):
		self.num_explored = 0

		start = Node(state=self.start, parent=None, action=None)
		frontier = QueueFrontier()
		frontier.add(start)

		self.explored = [] 

		while True:
			if frontier.empty():
				raise Exception("No Frontier")

			node = frontier.remove()
			self.num_explored += 1

			if (node.state[0] == self.goal[0]).all():
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions,  cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not frontier.has_state(state) and self.lacks_state(state):
					child = Node(state=state, parent=node, action=action)
					frontier.add(child)

# Main Code   
# start form  
# Value 0 is taken here as an empty space  
start = np.array([[1,2,3], [8,0,4], [5, 6, 7]])

# Goal form that can be solved  
# Value 0 is an empty space  
goal = np.array([[2, 8, 1], [0, 4, 3], [5, 6, 7]])


startIndex = (1, 1)
goalIndex = (1, 0)

# Method call for solving the puzzle  
s = PuzzleDfs(start, startIndex, goal, goalIndex)
s.solve()
s.print()
