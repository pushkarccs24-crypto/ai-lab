def print_board(state):
    for i in range(0, 9, 3):
        print(" " + " ".join(str(t) if t != 0 else " " for t in state[i:i+3]))
    print(" -----")

def get_neighbors(state):
    neighbors = []
    idx = state.index(0)
    r, c = idx // 3, idx % 3
    moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]
    for dr, dc, action in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_idx = nr * 3 + nc
            new_layout = list(state)
            new_layout[idx], new_layout[new_idx] = new_layout[new_idx], new_layout[idx]
            neighbors.append((tuple(new_layout), action))
    return neighbors

def dls(state, goal, limit, path, visited):
    # Print the current state being evaluated (just like regular DFS logs)
    print(f" DFS Node Check (Path Length {len(path)}):")
    print_board(state)

    if state == goal:
        return path
    if len(path) >= limit:
        return None

    for neighbor, action in get_neighbors(state):
        if neighbor not in visited:
            visited.add(neighbor)
            result = dls(neighbor, goal, limit, path + [action], visited)
            if result is not None:
                return result
            visited.remove(neighbor) # Backtrack
    return None

def run_ids(start, goal):
    print("Goal State:")
    print_board(goal)
    print("=======================")

    for limit in range(5):
        print(f"\n--- Starting New Iteration (Depth Limit = {limit}) ---")
        visited = {start}
        solution = dls(start, goal, limit, [], visited)
        if solution:
            print(f"Goal Found! Path: {solution}")
            return
            
initial = (1, 2, 3, 4, 0, 5, 7, 8, 6)
goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
run_ids(initial, goal)
