import heapq

# The target configuration of the 8-puzzle board
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

# Precomputed target coordinates (row, col) for each tile (0 to 8) to optimize speed
GOAL_COORDS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}


def manhattan_distance(state):
    """Calculate the sum of Manhattan distances of all tiles from their goal positions."""
    distance = 0
    for i in range(9):
        tile = state[i]
        # Skip the blank tile (0) when calculating distance
        if tile != 0:
            # Current coordinates
            current_row = i // 3
            current_col = i % 3
            
            # Target coordinates
            target_row, target_col = GOAL_COORDS[tile]
            
            # Add absolute horizontal and vertical differences
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance


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
    """Run A* Search using Manhattan Distance heuristic."""
    if not is_solvable(start):
        print("\n[Error]: This puzzle configuration is mathematically unsolvable!")
        return None

    # Priority queue stores tuples format: (f_score, g_score, current_state, transition_path)
    pq = []
    
    initial_h = manhattan_distance(start)
    heapq.heappush(pq, (initial_h, 0, start, []))

    visited = set()
    nodes_expanded = 0

    while pq:
        f, g, state, path = heapq.heappop(pq)

        if state in visited:
            continue

        visited.add(state)
        nodes_expanded += 1

        # Goal verification
        if state == GOAL:
            print(f"\n🎉 Solution Found in {g} moves!")
            print(f"Total states explored (nodes expanded): {nodes_expanded}")
            return path

        # Expand neighboring movements
        for move, neighbor_state in get_neighbors(state):
            if neighbor_state not in visited:
                new_g = g + 1
                new_h = manhattan_distance(neighbor_state)
                new_f = new_g + new_h
                
                heapq.heappush(pq, (new_f, new_g, neighbor_state, path + [(move, neighbor_state)]))

    print("\nNo solution pathway discovered.")
    return None


# --- Execution Controller Block ---
if __name__ == "__main__":
    # Define a significantly scrambled layout (Requires 14 moves to solve)
    initial_state = (4, 1, 3,
                     7, 2, 6,
                     5, 8, 0)
    
    print("Initial Starting Board State:")
    print_puzzle(initial_state)
    
    # Run the compiled A* engine
    solution_steps = a_star(initial_state)
    
    if solution_steps:
        print("\n--- Visualizing Step-by-Step Solution Path ---")
        for step_num, (direction, next_state) in enumerate(solution_steps, start=1):
            print(f"\nStep {step_num}: Slide Blank Tile '{direction}'")
            print_puzzle(next_state)
