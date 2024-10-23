import expense_8_puzzle as puzzle
import heapq

counter = 0
def ucs_search(start_state, goal_state,flag):
    fringe = []
    global counter
    heapq.heappush(fringe, (0,counter, start_state))
    closed = set()
    closed.add(tuple(map(tuple, start_state.array_2d)))

    nodes_popped = 0
    max_fringe_size = 0

    while fringe:
        current_cost, _ ,current_state = heapq.heappop(fringe)
        nodes_popped += 1

        if current_state.array_2d == goal_state.array_2d:
            return current_state, {
                'nodes_popped': nodes_popped,
                'nodes_generated': puzzle.nodes_generated,
                'max_fringe_size': max_fringe_size,
                'nodes_expanded': puzzle.nodes_expanded,
                'nodes_popped': nodes_popped,
                'solution_depth': current_state.level
            }

        # Expand the node
        count_nodes_generated = 0
        if(flag == True):
            print("\nGenerating Successors to : ",current_state.array_2d, file=open(puzzle.output_path,'a'))
        for direction in ["up", "down", "left", "right"]:
            new_state = puzzle.move_blank(current_state, direction)
            if new_state:
                puzzle.nodes_expanded += 1
                if (tuple(map(tuple, new_state.array_2d)) not in closed):
                    new_cost = current_cost + new_state.cost  # moved_number is the cost of the tile moved
                    heapq.heappush(fringe, (new_cost, counter,  new_state))
                    counter += 1
                    closed.add(tuple(map(tuple, new_state.array_2d)))
                    puzzle.nodes_generated += 1
                    max_fringe_size = max(max_fringe_size, len(fringe))

        if(flag == True):
            print("\n",count_nodes_generated," Successors generated", file=open(puzzle.output_path,'a'))
            puzzle.print_priority_fringe(fringe)
            print("\n Closed: \t",closed,file=open(puzzle.output_path,'a'))

    return None, None #No solution found