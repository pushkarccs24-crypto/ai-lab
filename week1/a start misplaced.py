import heapq

# The target configuration of the 8-puzzle board
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


def misplaced_tiles(state):
    """Calculate the number of misplaced tiles (Heuristic h(n))."""
    count = 0
    for i in range(9):
        # We don't count the blank tile (0) as misplaced
        if state[i] != 0 and state[i] != GOAL[i]:
            count += 1
    return count


def get_neighbors(state):
    """Generate all valid neighboring states from moving the blank tile (0)."""
    neighbors = []

    zero = state.index(0)
    row = zero // 3
    col = zero % 3

    # Up Movement
    if row > 0:
        new_state = list(state)
        new_state[zero], new_state[zero - 3] = new_state[zero - 3], new_state[zero]
        neighbors.append(("Up", tuple(new_state)))

    # Down Movement
    if row < 2:
        new_state = list(state)
        new_state[zero], new_state[zero + 3] = new_state[zero + 3], new_state[zero]
        neighbors.append(("Down", tuple(new_state)))

    # Left Movement
    if col > 0:
        new_state = list(state)
        new_state[zero], new_state[zero - 1] = new_state[zero - 1], new_state[zero]
        neighbors.append(("Left", tuple(new_state)))

    # Right Movement
    if col < 2:
        new_state = list(state)
        new_state[zero], new_state[zero + 1] = new_state[zero + 1], new_state[zero]
        neighbors.append(("Right", tuple(new_state)))

    return neighbors


def print_puzzle(state):
    """Print the puzzle state as a readable 3x3 grid layout."""
    print("-------------")
    for i in range(0, 9, 3):
        # Display 0 as a blank space for better visual readability
        display_row = [str(x) if x != 0 else " " for x in state[i:i+3]]
        print("|", " ".join(display_row), "|")
    print("-------------")


def is_solvable(state):
    """Verify if the puzzle can be mathematically solved using inversion counting."""
    flat_list = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    # An 8-puzzle is solvable only if the number of inversions is even
    return inversions % 2 == 0


def a_star(start):
    """Run A* Search from start state to target goal state."""
    if not is_solvable(start):
        print("\n[Error]: This puzzle configuration is mathematically unsolvable!")
        return None

    # Priority queue stores tuples format: (f_score, g_score, current_state, transition_path)
    pq = []
    
    initial_h = misplaced_tiles(start)
    # At start state, g_score is 0, so f_score = 0 + initial_h
    heapq.heappush(pq, (initial_h, 0, start, []))

    visited = set()

    while pq:
        f, g, state, path = heapq.heappop(pq)

        # Skip states we have already processed optimally
        if state in visited:
            continue

        visited.add(state)

        # Goal verification
        if state == GOAL:
            print(f"\n🎉 Solution Found in {g} moves!")
            return path

        # Expand neighboring movements
        for move, neighbor_state in get_neighbors(state):
            if neighbor_state not in visited:
                new_g = g + 1
                new_h = misplaced_tiles(neighbor_state)
                new_f = new_g + new_h
                
                # Append the directional move instruction to tracking list
                heapq.heappush(pq, (new_f, new_g, neighbor_state, path + [(move, neighbor_state)]))

    print("\nNo solution pathway discovered.")
    return None


# --- Execution Controller Block ---
if __name__ == "__main__":
    # Define an initial random board layout (Requires 4 moves to solve)
    initial_state = (1, 2, 3,
                     0, 4, 6,
                     7, 5, 8)
    
    print("Initial Starting Board State:")
    print_puzzle(initial_state)
    
    # Run the compiled A* engine
    solution_steps = a_star(initial_state)
    
    if solution_steps:
        print("\n--- Visualizing Step-by-Step Solution Path ---")
        current_board = initial_state
        
        for step_num, (direction, next_state) in enumerate(solution_steps, start=1):
            print(f"\nStep {step_num}: Slide Blank Tile '{direction}'")
            print_puzzle(next_state)

<FollowUp>
Would you like me to rewrite the puzzle evaluation to use **Manhattan Distance** instead of Misplaced Tiles to see how it drastically **reduces the number of checked nodes**?
