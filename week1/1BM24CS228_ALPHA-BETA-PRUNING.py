def alpha_beta(depth, node, maximizing, values, alpha, beta):
    if depth == 0:
        return values[node]

    if maximizing:
        best = float('-inf')

        for i in range(2):
            val = alpha_beta(depth - 1, node * 2 + i,
                             False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:
        best = float('inf')

        for i in range(2):
            val = alpha_beta(depth - 1, node * 2 + i,
                             True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best


# Dynamic input
depth = int(input("Enter depth of tree: "))

n = 2 ** depth
values = []

print("Enter leaf node values:")
for i in range(n):
    values.append(int(input()))

result = alpha_beta(depth, 0, True, values,
                    float('-inf'), float('inf'))

print("Optimal value:", result)
