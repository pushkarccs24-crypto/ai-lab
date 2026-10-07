import heapq

# Goal state
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


# Calculate Manhattan Distance
def manhattan_distance(state):
    distance = 0

    for i in range(9):

        if state[i] == 0:
            continue

        current_row = i // 3
        current_col = i % 3

        goal_index = GOAL.index(state[i])

        goal_row = goal_index // 3
        goal_col = goal_index % 3

        distance += abs(current_row - goal_row)
        distance += abs(current_col - goal_col)

    return distance


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

    # Priority Queue
    # (f, g, state, path)
    pq = []

    h = manhattan_distance(start)

    heapq.heappush(
        pq,
        (h, 0, start, [])
    )

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

            print("\nSolution Path:")

            print("\nInitial State")
            print_puzzle(start)

            current_g = 0

            for move, next_state in path:

                current_g += 1

                h = manhattan_distance(next_state)
                f = current_g + h

                print("\nMove:", move)
                print("g(n) =", current_g)
                print("h(n) =", h)
                print("f(n) =", f)

                print_puzzle(next_state)

            return

        # Expand current state
        for move, next_state in get_neighbors(state):

            if next_state not in visited:

                new_g = g + 1
                new_h = manhattan_distance(next_state)
                new_f = new_g + new_h

                heapq.heappush(
                    pq,
                    (
                        new_f,
                        new_g,
                        next_state,
                        path + [(move, next_state)]
                    )
                )

    print("No solution found.")


# Main program
print("8-Puzzle using A* Search")
print("Heuristic: Manhattan Distance")

print("\nEnter the initial state")
print("Use 0 for blank space.")

start = []

for i in range(9):
    value = int(input("Enter value " + str(i + 1) + ": "))
    start.append(value)

start = tuple(start)

print("\nInitial State:")
print_puzzle(start)

a_star(start)
