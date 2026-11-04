def is_variable(expr):
    """Returns True if the expression is a variable (starts with '?')."""
    return isinstance(expr, str) and expr.startswith('?')

def is_constant(expr):
    """Returns True if the expression is an atomic constant (not a variable and not a list)."""
    return isinstance(expr, (str, int, float)) and not expr.startswith('?')

def occurs_in(var, expr):
    """Checks if a variable occurs inside a given expression (Occurs Check)."""
    if expr == var:
        return True
    if isinstance(expr, list):
        return any(occurs_in(var, arg) for arg in expr)
    return False

def apply_substitution(subst, expr):
    """Applies a substitution set (list of dicts or pairs) to an expression."""
    if not subst:
        return expr
    
    # If the expression is a variable, look it up in the substitution mapping
    if is_variable(expr):
        for s_var, s_val in subst:
            if expr == s_var:
                return apply_substitution(subst, s_val)
        return expr
    
    # If it's a compound expression, apply substitution recursively to all arguments
    if isinstance(expr, list):
        return [expr[0]] + [apply_substitution(subst, arg) for arg in expr[1:]]
    
    return expr

def unify(psi1, psi2):
    # Step 1: If Psi1 or Psi2 is a variable or constant
    if is_variable(psi1) or is_constant(psi1) or is_variable(psi2) or is_constant(psi2):
        # a) If identical, return NIL (represented as an empty list [])
        if psi1 == psi2:
            return []
        
        # b) Else if Psi1 is a variable
        elif is_variable(psi1):
            # a. if Psi1 occurs in Psi2, return FAILURE
            if occurs_in(psi1, psi2):
                return "FAILURE"
            # b. Else return {(Psi2 / Psi1)}
            else:
                return [(psi1, psi2)]
        
        # c) Else if Psi2 is a variable
        elif is_variable(psi2):
            # a. If Psi2 occurs in Psi1, return FAILURE
            if occurs_in(psi2, psi1):
                return "FAILURE"
            # b. Else return {(Psi1 / Psi2)}
            else:
                return [(psi2, psi1)]
        
        # d) Else return FAILURE
        else:
            return "FAILURE"
            
    # Step 2: If the initial Predicate symbol in Psi1 and Psi2 are not the same
    if psi1[0] != psi2[0]:
        return "FAILURE"
        
    # Step 3: If Psi1 and Psi2 have a different number of arguments
    if len(psi1) != len(psi2):
        return "FAILURE"
        
    # Step 4: Set Substitution set (SUBST) to NIL
    subst = []
    
    # Step 5: For i = 1 to the number of elements (arguments) in Psi1
    # Note: index 0 is the predicate symbol, so we loop through the arguments from index 1 onwards
    psi1_args = psi1[1:]
    psi2_args = psi2[1:]
    
    for i in range(len(psi1_args)):
        # a) Call Unify function with the ith element of Psi1 and ith element of Psi2
        s = unify(psi1_args[i], psi2_args[i])
        
        # b) If S = failure then returns Failure
        if s == "FAILURE":
            return "FAILURE"
            
        # c) If S != NIL then do
        if s != []:
            # a. Apply S to the remainder of both argument lists
            psi1_args = [apply_substitution(s, arg) for arg in psi1_args]
            psi2_args = [apply_substitution(s, arg) for arg in psi2_args]
            
            # b. SUBST = APPEND(S, SUBST)
            subst = s + subst
            
    # Step 6: Return SUBST
    return subst

# --- Execution Example ---
if __name__ == "__main__":
    # Example 1: Unifying Knows(John, ?x) and Knows(John, Jane)
    expr1 = ["Knows", "John", "?x"]
    expr2 = ["Knows", "John", "Jane"]
    
    print("Expression 1:", expr1)
    print("Expression 2:", expr2)
    result = unify(expr1, expr2)
    print("Substitution Result:", result)
    print("-" * 40)
    
    # Example 2: Failed Unification due to Occurs Check -> ?x and F(?x)
    expr3 = ["P", "?x"]
    expr4 = ["P", ["F", "?x"]]
    
    print("Expression 3:", expr3)
    print("Expression 4:", expr4)
    result2 = unify(expr3, expr4)
    print("Substitution Result:", result2)
