import random
import math

# Calculate number of attacking queen pairs
def heuristic(state):
    conflicts = 0

    for i in range(8):
        for j in range(i + 1, 8):
            # Same row or same diagonal
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1

    return conflicts


# Generate a neighboring state
def get_neighbor(state):
    neighbor = state.copy()

    col = random.randint(0, 7)
    new_row = random.randint(0, 7)

    while new_row == neighbor[col]:
        new_row = random.randint(0, 7)

    neighbor[col] = new_row

    return neighbor


# Simulated Annealing algorithm
def simulated_annealing():

    for restart in range(100):

        # Initial random state
        current = [random.randint(0, 7) for _ in range(8)]

        T = 10.0
        alpha = 0.995
        max_steps = 20000

        for step in range(max_steps):

            # Check goal state
            current_h = heuristic(current)

            if current_h == 0:
                return current, step, restart + 1

            # Generate next state
            next_state = get_neighbor(current)
            next_h = heuristic(next_state)

            # Calculate change in energy
            delta = next_h - current_h

            # Accept better state
            if delta < 0:
                current = next_state

            # Sometimes accept worse state
            else:
                probability = math.exp(-delta / T)

                if random.random() < probability:
                    current = next_state

            # Reduce temperature
            T = T * alpha

            if T < 0.0001:
                break

    return None, 0, 100


# Main program
solution, steps, restarts = simulated_annealing()

if solution is not None:
    print("Solution Found!")
    print("Queen positions:", solution)
    print("Heuristic value:", heuristic(solution))
    print("Steps:", steps)
    print("Restarts:", restarts)

    print("\nChessboard:")

    for row in range(8):
        for col in range(8):
            if solution[col] == row:
                print(" Q ", end="")
            else:
                print(" . ", end="")
        print()

else:
    print("Solution not found.")

