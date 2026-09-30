def print_board(state):
    """Helper function to print the 1D state array as a 3x3 grid layout."""
    for i in range(0, 9, 3):
        # Displays the 0 tile as an empty space ' ' for realistic puzzle visuals
        row = [str(tile) if tile != 0 else ' ' for tile in state[i:i+3]]
        print("  " + " ".join(row))
    print("---------")

def solve_8_puzzle_dfs(start_state, goal_state):
    """Solves the 8-puzzle using a Depth-First Search strategy."""
    stack = [(start_state, [])]
    visited = {start_state}
    
    def get_neighbors(state):
        neighbors = []
        idx = state.index(0)
        row, col = idx // 3, idx % 3
        moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]
        
        for dr, dc, action in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_layout = list(state)
                new_layout[idx], new_layout[new_idx] = new_layout[new_idx], new_layout[idx]
                neighbors.append((tuple(new_layout), action))
        return neighbors

    while stack:
        current_state, path = stack.pop()
        if current_state == goal_state:
            return path
            
        for neighbor_state, action in get_neighbors(current_state):
            if neighbor_state not in visited:
                visited.add(neighbor_state)
                stack.append((neighbor_state, path + [action]))
    return None

def simulate_solution(start_state, goal_state, path):
    """Simulates and prints each incremental state step-by-step alongside the Goal State."""
    print("=============================")
    print("TARGET GOAL STATE:")
    print_board(goal_state)
    print("STARTING INTIAL STATE:")
    print_board(start_state)
    print("=============================\n")
    
    if path is None:
        print("No valid solution sequence exists.")
        return
        
    current_state = list(start_state)
    for step_num, action in enumerate(path, 1):
        idx = current_state.index(0)
        row, col = idx // 3, idx % 3
        
        if action == 'Up': target_idx = (row - 1) * 3 + col
        elif action == 'Down': target_idx = (row + 1) * 3 + col
        elif action == 'Left': target_idx = row * 3 + (col - 1)
        elif action == 'Right': target_idx = row * 3 + (col + 1)
        
        # Swap empty tile with target sliding tile
        current_state[idx], current_state[target_idx] = current_state[target_idx], current_state[idx]
        
        print(f"Step {step_num}: Slide Tile '{action}'")
        print_board(current_state)
        
    print("Goal Reached Successfully!")

# --- Define Your Configurations Here ---
initial_board = (1, 2, 3, 
                 4, 0, 5, 
                 7, 8, 6)

goal_board = (1, 2, 3, 
              4, 5, 6, 
              7, 8, 0)

# Run DFS calculation
solution_moves = solve_8_puzzle_dfs(initial_board, goal_board)

# Output visual simulation steps
simulate_solution(initial_board, goal_board, solution_moves)
