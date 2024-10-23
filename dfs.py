import sys
from collections import deque
import expense_8_puzzle as puzzle

def dfs(start_state, goal_state,flag):
    global nodes_expanded
    global nodes_generated
    fringe = [start_state]
    closed = set()
    closed.add(tuple(map(tuple, start_state.array_2d)))

    max_depth = 0
    nodes_popped = 0
    max_fringe_size = 0
    while fringe:
        current_state = fringe.pop()
        nodes_popped += 1
        max_fringe_size = max(max_fringe_size, len(fringe))

        if current_state.array_2d == goal_state.array_2d:
            return current_state, {
                'nodes_popped': nodes_popped,
                'nodes_generated': puzzle.nodes_generated,
                'nodes_expanded': puzzle.nodes_expanded,
                'max_fringe_size': max_fringe_size,
                'solution_depth': current_state.level,
            }
        count_nodes_generated = 0
        if(flag == True):
            print("\nGenerating Successors to : ",current_state.array_2d, file=open(puzzle.output_path,'a'))
        for direction in ["up", "down", "left", "right"]:
                new_state= puzzle.move_blank(current_state, direction)
                if(new_state):
                    puzzle.nodes_generated += 1
                    count_nodes_generated += 1
                    if tuple(map(tuple, new_state.array_2d)) not in closed:
                        closed.add(tuple(map(tuple, new_state.array_2d)))
                        fringe.append(new_state)
                        puzzle.nodes_expanded += 1
                        max_depth = max(max_depth, new_state.level)
        if(flag == True):
            print("\n",count_nodes_generated," Successors generated", file=open(puzzle.output_path,'a'))
            puzzle.print_fringe(fringe)
            print("\n Closed: \t",closed,file=open(puzzle.output_path,'a'))

    return None, None  # No solution found
