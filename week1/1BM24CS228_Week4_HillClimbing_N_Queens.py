def calculate_cost(state):
    cost = 0
    n = len(state)

   
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                cost += 1
    return cost


def hill_climbing(initial_state):
    current = initial_state[:]
    step = 1

    while True:
        current_cost = calculate_cost(current)

        print("\n" + "=" * 50)
        print(f"STEP {step}")
        print("Current State :", current)
        print("Current Cost  :", current_cost)
        print("\nAll Possible Swaps:")

        neighbors = []
        n = len(current)

        
        for i in range(n):
            for j in range(i + 1, n):
                neighbor = current[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                cost = calculate_cost(neighbor)
                neighbors.append((cost, i, j, neighbor))

                print(f"Swap (x{i}, x{j}) -> {neighbor}   Cost = {cost}")

        
        best = min(neighbors, key=lambda x: (x[0], x[1], x[2]))
        best_cost, i, j, best_state = best

        print("\nSelected Swap :", f"(x{i}, x{j})")
        print("Next State    :", best_state)
        print("Next Cost     :", best_cost)

        if best_cost >= current_cost:
            print("\nNo better neighbor found.")
            print("Hill Climbing Terminated.")
            break

        current = best_state
        step += 1

        if best_cost == 0:
            print("\nGOAL STATE REACHED!")
            print("Final State :", current)
            break


initial_state = [3, 1, 2, 0]
hill_climbing(initial_state)