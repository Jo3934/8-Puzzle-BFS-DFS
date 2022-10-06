""" 8 Puzzle BFS algorithmn in python """

#import libraries 
import numpy as np 
import os

#declare node class 
class Node:
    def __init__(self, node_no, data, parent, act, cost):
        self.data = data
        self.parent = parent
        self.act = act
        self.node_no = node_no
        self.cost = cost
#get_initial method        
def get_initial():
    print("Enter number between 0-9")
    initial_state = np.zeros(9)
    for i in range(9):
        states = int(input("Enter " + str(i + 1) + " number: "))
        if states < 0 or states > 8:
            print("Enter state between [0-8]")
            exit(0)
        else:
            initial_state[i] = np.array(states)
    return np.reshape(initial_state, (3, 3))
#method find_index
def find_ind(puzzle):
    i, j = np.where(puzzle == 0)
    i = int(i)
    j = int(j)
    return i, j

#method of movement in array left
def move_left(data):
    i, j = find_ind(data)
    if j == 0:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i, j - 1]
        temp_arr[i, j] = temp
        temp_arr[i, j - 1] = 0
        return temp_arr
#method of movement in array right   
def move_right(data):
    i, j = find_ind(data)
    if j == 2:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i, j + 1]
        temp_arr[i, j] = temp
        temp_arr[i, j + 1] = 0
        return temp_arr
#method of movement in array up
def move_up(data):
    i, j = find_ind(data)
    if i == 0:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i - 1, j]
        temp_arr[i, j] = temp
        temp_arr[i - 1, j] = 0
        return temp_arr
#method of movement in array down
def move_down(data):
    i, j = find_ind(data)
    if i == 2:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i + 1, j]
        temp_arr[i, j] = temp
        temp_arr[i + 1, j] = 0
        return temp_arr
#method of movement in array tile
def move_tile(action, data):
    if action == 'up':
        return move_up(data)
    if action == 'down':
        return move_down(data)
    if action == 'left':
        return move_left(data)
    if action == 'right':
        return move_right(data)
    else:
        return None
#method of printing states
def print_states(list_final): 
    print("printing final solution")
    for l in list_final:
        print("Move : " + str(l.act) + "\n" + "Result : " + "\n" + str(l.data) + "\t" + "node number:" + str(l.node_no))

#method to write the details in path
def write_path(path_formed): 
    if os.path.exists("Path_file.txt"):
        os.remove("Path_file.txt")

    f = open("Path_file.txt", "a")
    for node in path_formed:
        if node.parent is not None:
            f.write(str(node.node_no) + "\t" + str(node.parent.node_no) + "\t" + str(node.cost) + "\n")
    f.close()
#Method defining the explored nodes
def write_node_explored(explored): 
    if os.path.exists("Node.txt"):
        os.remove("Node.txt")

    f = open("Nodes.txt", "a")
    for element in explored:
        f.write('[')
        for i in range(len(element)):
            for j in range(len(element)):
                f.write(str(element[j][i]) + " ")
        f.write(']')
        f.write("\n")
    f.close()

def write_node_info(visited): 
    if os.path.exists("info.txt"):
        os.remove("info.txt")

    f = open("info.txt", "a")
    for n in visited:
        if n.parent is not None:
            f.write(str(n.node_no) + "\t" + str(n.parent.node_no) + "\t" + str(n.cost) + "\n")
    f.close()

def path(node):  
    p = []  # Empty list
    p.append(node)
    parent_node = node.parent
    while parent_node is not None:
        p.append(parent_node)
        parent_node = parent_node.parent
    return list(reversed(p))

def exploring_nodes(node):
    print(" Nodes Exploration")
    actions = ["down", "up", "left", "right"]
    goal_node = np.array([[2, 8, 1], [0, 4, 3], [5, 6, 7]])
    node_q = [node]
    final_nodes = []
    visited = []
    final_nodes.append(node_q[0].data.tolist())  
    #  writing data of nodes in seen
    node_counter = 0  # To define a unique ID to all the nodes formed
    while node_q:
        current_root = node_q.pop(0)  # Pop the element 0 from the list
        if current_root.data.tolist() == goal_node.tolist():
            print("Final attained")
            return current_root, final_nodes, visited

        for move in actions:
            temp_data = move_tile(move, current_root.data)
            if temp_data is not None:
                node_counter += 1
                child_node = Node(node_counter, np.array(temp_data), current_root, move, 0)  
                # Create a child node

                if child_node.data.tolist() not in final_nodes:  
                    # Add the child node data in final node list
                    node_q.append(child_node)
                    final_nodes.append(child_node.data.tolist())
                    visited.append(child_node)
                    if child_node.data.tolist() == goal_node.tolist():
                        print("Final attained")
                        return child_node, final_nodes, visited
    return None, None, None  
# return statement if the goal node is not reached

def check_input(l):
    array = np.reshape(l, 9)
    for i in range(9):
        counter_appear = 0
        f = array[i]
        for j in range(9):
            if f == array[j]:
                counter_appear += 1
        if counter_appear >= 2:
            print("invalid input")
            exit(0)

def check_solvable(g):
    arr = np.reshape(g, 9)
    counter_states = 0
    for i in range(9):
        if not arr[i] == 0:
            check_elem = arr[i]
            for x in range(i + 1, 9):
                if check_elem < arr[x] or arr[x] == 0:
                    continue
                else:
                    counter_states += 1
    if counter_states % 2 == 0:
        print("Solving 8 puzzle")
    else:
        print("Solving 8 puzzle failure")

#Main code
k = get_initial()

check_input(k)
check_solvable(k)

root = Node(0, k, None, None, 0)

# BFS implementation call
goal, s, v = exploring_nodes(root)

if goal is None and s is None and v is None:
    print("Goal State not reached")
else:
    # Print and write the final output
    print_states(path(goal))
    write_path(path(goal))
    write_node_explored(s)
    write_node_info(v)
