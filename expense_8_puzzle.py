from imports import *


nodes_expanded = 0
nodes_generated = 0
output_path = "dump.txt"

class state:
    def __init__(self,array_2d, parent = None, move = "", moved_number = 0, current_cost=0):


        self.parent = parent
        #stores parent state to the current state


        self.array_2d = array_2d
        #stores the matrix (locations of the numbers) for current state


        self.blank = find_blank(self)
        #stores the location of the blank in current state

        if(parent == None):
            self.level = 0
            self.cost = 0
        else:
            self.level = parent.level+1
            self.cost = parent.cost + int(moved_number)
        
        self.move = move
        if(moved_number != 0):
            self.moved_number = moved_number

        #stores which level the state is on (starting with 0 for parent node)

#using Manhattan Distance as the second heuristic
def h2(current_state, goal_state):
    cost = 0
    expected_positions = dict()
    for i in range(len(goal_state.array_2d)):
        for j in range(len(goal_state.array_2d[i])):
            expected_positions[goal_state.array_2d[i][j]] = [i,j]
    for i in range(len(current_state.array_2d)):
        for j in range(len(current_state.array_2d[i])):
            if(current_state.array_2d[i][j] != 0):
                expected = expected_positions[current_state.array_2d[i][j]]
                cost = cost + abs(i - expected[0]) + abs(j - expected[1])
    return cost


#function to find the position of 0 in the current state
def find_blank(current_state):
    for i in range(len(current_state.array_2d)):
        for j in range(len(current_state.array_2d[i])):
            if current_state.array_2d[i][j] == 0:
                return (i,j)
            

#function used to take input from command line
def take_input():
    args = sys.argv
    length = len(args)
    if length < 3:
        print("incorret input format!")
        sys.exit(1)
    method = "star"
    dump_flag = False
    file1 = args[1]
    file2 = args[2]

    if(length > 3):
        if(args[3].lower() == "true"):
            dump_flag = True
        elif(args[3].lower() == "false"):
            dump_flag = False
        else:
            method = args[3]

    if(length > 4):
        if(args[4].lower() == "true"):
            dump_flag = True

    return file1, file2, method, dump_flag

#Function to convert the input file into a 2D array
def convert_to_array(name):
    array_2D = []
    try:
        with open(name,'r') as file:
            for line in file:
                if(line == "END OF FILE"):
                    break
                row = list(map(int, line.strip().split()))
                array_2D.append(row)

            return array_2D
    except FileNotFoundError:
        return "File Does Not Exist in folder"
    except Exception as e:
        return f"an error occured!: \n {e}"
    
#Function to move the 0 and generate new nodes
def move_blank(current_state, direction):
    x, y = current_state.blank
    number_movement = ""
    if direction == "up":
        x -= 1
        number_movement = "down"
    elif direction == "down":
        x += 1
        number_movement = "up"
    elif direction == "left":
        y -= 1
        number_movement = "right"
    elif direction == "right":
        y += 1
        number_movement = "left"
    if 0 <= x < 3 and 0 <= y < 3:
        new_array = [row[:] for row in current_state.array_2d]
        moved = new_array[x][y]
        new_array[current_state.blank[0]][current_state.blank[1]], new_array[x][y] = new_array[x][y], new_array[current_state.blank[0]][current_state.blank[1]]
        new_state = state(new_array, current_state, move = number_movement, moved_number = moved)
        new_state.blank = (x, y)
        return new_state
    return None

#function to show the path of the changes made to states
def find_path(current_state):
    path = []
    while current_state:
        path.append(current_state)
        current_state = current_state.parent
    return path[::-1]

def print_path(solution):
    path = find_path(solution)
    for i in range(1, len(path)):
        move = path[i].move
        moved = path[i].moved_number
        print(f"Move {moved} {move}")
        for row in path[i].array_2d:
            print("\t",row)
        print()

def print_solution_to_file(solution, stats):
    print("\n\nNodes Popped:", stats['nodes_popped'], file=open(output_path,'a'))
    print("Nodes Expanded:", stats['nodes_expanded'], file=open(output_path,'a'))
    print("Nodes Generated:", stats['nodes_generated'], file=open(output_path,'a'))
    print("Max Fringe Size:", stats['max_fringe_size'], file=open(output_path,'a'))
    print(f"Solution Found at depth {stats['solution_depth']} with cost of ", solution.cost, file=open(output_path,'a'))

def print_solution(solution, stats):
    print("\n \nSteps:")
    path = find_path(solution)
    previous_state = path[0]

    if len(path) > 1:
        for i in range(1, len(path)):
            move = path[i].move
            moved = path[i].moved_number
            print(f" \t Move {moved} {move}")
    else:
        print("No moves needed (initial state is the goal state).")
    print("\n\nNodes Popped:", stats['nodes_popped'])
    print("Nodes Expanded:", stats['nodes_expanded'])
    print("Nodes Generated:", stats['nodes_generated'])
    print("Max Fringe Size:", stats['max_fringe_size'])
    print(f"Solution Found at depth {stats['solution_depth']} with cost of ", solution.cost)

def print_fringe(fringe):
    print("\nFringe:\n\t", file=open(output_path,'a'))
    for i in fringe:
        print(i.array_2d,end=" , ",file=open(output_path,'a') )

def print_priority_fringe(fringe):
    print("\nFringe:\n\t", file=open(output_path,'a'))
    for a,b,c in fringe:
            print(c.array_2d,end=" , ",file=open(output_path,'a') )

#Driver Function
def find_solution(method,flag):
    solution_state = None
    if (method == "dfs"):
        solution_state,stats = dfs.dfs(start_state, goal_state,flag)
    elif (method == "bfs"):
        solution_state,stats = bfs.bfs(start_state, goal_state,flag)
    elif (method == "dls"):
        limit = int(input("Enter the limit for the dls method: "))
        solution_state,stats = dls.dls(start_state,goal_state,flag,limit)
    elif (method == "ids"):
        limit = 0
        while(not solution_state):
            limit += 1
            solution_state,stats = dls.dls(start_state,goal_state,flag,limit)
    elif (method == "greedy"):
        solution_state, stats = greedy.greedy_search(start_state, goal_state,flag)
    elif (method == "ucs"):
        solution_state, stats = ucs.ucs_search(start_state, goal_state,flag)
    elif (method == "star"):
        solution_state, stats = star.a_star_search(start_state, goal_state,flag)
    else:
        print("Wrong Choice!")
    
    if solution_state:
        if dump_flag:
            print_path(solution_state)
            print_solution_to_file(solution_state,stats)
        print_solution(solution_state,stats)
        if (method == "ids"):
            print("found with limit set to : ",limit )
    else:
        print("No solution exists.")
    
#Main Funtion
if __name__ == "__main__":
    open(output_path, 'w').close()
    start_file,goal_file,method,dump_flag = take_input()

    start_array = convert_to_array(start_file)
    goal_array = convert_to_array(goal_file)

    start_state = state(start_array)
    goal_state = state(goal_array)
    
    if(dump_flag == True):
        print("Command Line Arguments: ",start_file,goal_file,method,dump_flag, file = open(output_path,'a'))
        print("\nmethod selected : ",method, file=open(output_path,'a'))
    find_solution(method,dump_flag)