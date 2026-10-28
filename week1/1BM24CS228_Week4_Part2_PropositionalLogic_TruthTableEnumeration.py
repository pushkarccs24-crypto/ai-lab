
from itertools import product

def implies(a, b):
    return not a or b

def KB(P, Q, R):
    return (implies(Q, P) and
            implies(P, not Q) and
            (Q or R))

def TT_Entails(query):
    for P, Q, R in product([True, False], repeat=3):
        if KB(P, Q, R):
            if query == "R":
                result = R
            elif query == "R -> P":
                result = implies(R, P)
            elif query == "Q -> R":
                result = implies(Q, R)

            if not result:
                return False
    return True

print("P Q R | KB")
print("----------------")

for P, Q, R in product([True, False], repeat=3):
    print(P, Q, R, "|", KB(P, Q, R))

print("\nEntailment Results:")
print("KB entails R:", TT_Entails("R"))
print("KB entails R -> P:", TT_Entails("R -> P"))
print("KB entails Q -> R:", TT_Entails("Q -> R"))
