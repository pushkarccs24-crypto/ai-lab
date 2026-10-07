import heapq

# Goal state
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

# Possible movements of blank tile
MOVES = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}


# Calculate number of misplaced tiles
def misplaced_tiles(state):
    count = 0

    for i in range(9):
        if state[i] != 0 and state[i] != GOAL[i]:
            count += 1

    return count


# Generate neighboring states
def get_neighbors(state):
    neighbors = []

    zero = state.index(0)
    row = zero // 3
    col = zero % 3

    # Up
    if row > 0:
        new_state = list(state)
        new_state[zero], new_state[zero - 3] = \
            new_state[zero - 3], new_state[zero]
        neighbors.append(("Up", tuple(new_state)))

    # Down
    if row < 2:
        new_state = list(state)
        new_state[zero], new_state[zero + 3] = \
            new_state[zero + 3], new_state[zero]
        neighbors.append(("Down", tuple(new_state)))

    # Left
    if col > 0:
        new_state = list(state)
        new_state[zero], new_state[zero - 1] = \
            new_state[zero - 1], new_state[zero]
        neighbors.append(("Left", tuple(new_state)))

    # Right
    if col < 2:
        new_state = list(state)
        new_state[zero], new_state[zero + 1] = \
            new_state[zero + 1], new_state[zero]
        neighbors.append(("Right", tuple(new_state)))

    return neighbors


# Print puzzle
def print_puzzle(state):
    print("-------------")
    for i in range(0, 9, 3):
        print("|", state[i], state[i + 1], state[i + 2], "|")
    print("-------------")


# A* Search
def a_star(start):
    # Priority queue contains:
    # (f, g, state, path)
    pq = []

    h = misplaced_tiles(start)
    heapq.heappush(pq, (h, 0, start, []))

    visited = set()

    while pq:
        f, g, state, path = heapq.heappop(pq)

        if state in visited:
            continue

        visited.add(state)

        # Goal test
        if state == GOAL:
            print("\nSolution Found!")
            print("Total Depth:", g)
            print("Total Cost:", f)

            print("\nSolution Path:")

            current = start
            print("\nInitial State")
            print_puzzle(current)

            for move, next_state in path:
                print("\nMove:", move)

                h = misplaced_tiles(next_state)
                new_g = path.index((move, next_state)) + 1
                new_f = new_g + h

                print("g(n) =", new_g)
                print("h(n) =", h)
                print("f(n) =", new_f)

                print_puzzle(next_state)

            return

        # Expand node
        for move, next_state in get_neighbors(state):

            if next_state not in visited:

                new_g = g + 1
                new_h = misplaced_tiles(next_state)
                new_f = new_g + new_h

                heapq.heappush(
                    pq,
                    (new_f, new_g, next_state,
                     path + [(move, next_state)])
                )

    print("No solution found.")


# Main program
print("8-Puzzle using A* Search")
print("Heuristic: Number of Misplaced Tiles")

print("\nEnter the initial state")
print("Use 0 for blank space.")

start = []

for i in range(9):
    value = int(input("Enter value " + str(i + 1) + ": "))
    start.append(value)

start = tuple(start)

print("\nInitial State:")
print_puzzle(start)
