# Rules:
# - Predicates look like: "Human(x)" or "~Human(x)"
# - Variables are single lowercase letters: "x", "y", "z"
# - Constants start with an uppercase letter: "Socrates", "Plato"

def is_var(x):
    return len(x) == 1 and x.islower()

def parse(literal):
    neg = literal.startswith("~")
    clean = literal[1:] if neg else literal
    pred, args = clean[:-1].split("(")
    return neg, pred, [a.strip() for a in args.split(",")]

def unify(lit1, lit2):
    neg1, pred1, args1 = parse(lit1)
    neg2, pred2, args2 = parse(lit2)
    
    # Must be opposite signs, same predicate, same number of arguments
    if neg1 == neg2 or pred1 != pred2 or len(args1) != len(args2):
        return None
        
    subs = {}
    for a, b in zip(args1, args2):
        a = subs.get(a, a)
        b = subs.get(b, b)
        if a == b:
            continue
        elif is_var(a):
            subs[a] = b
        elif is_var(b):
            subs[b] = a
        else:
            return None  # Two different constants cannot unify
    return subs

def substitute(clause, subs):
    new_clause = []
    for lit in clause:
        neg, pred, args = parse(lit)
        new_args = [subs.get(a, a) for a in args]
        prefix = "~" if neg else ""
        new_clause.append(f"{prefix}{pred}({','.join(new_args)})")
    return new_clause

def resolve(c1, c2):
    resolvents = []
    for l1 in c1:
        for l2 in c2:
            subs = unify(l1, l2)
            if subs is not None:
                rem1 = [l for l in c1 if l != l1]
                rem2 = [l for l in c2 if l != l2]
                combined = list(set(substitute(rem1 + rem2, subs)))
                resolvents.append(combined)
    return resolvents

def prove(kb, query):
    # Negate the query and add it to the knowledge base
    neg_query = query[1:] if query.startswith("~") else "~" + query
    clauses = kb + [[neg_query]]
    
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                for res in resolve(clauses[i], clauses[j]):
                    if res == []:  # Empty clause = Contradiction = Proven!
                        return True
                    if res not in clauses and res not in new_clauses:
                        new_clauses.append(res)
        if not new_clauses:
            return False
        clauses.extend(new_clauses)

# --- Example ---
kb = [
    ["~Human(x)", "Mortal(x)"],  # All humans are mortal
    ["Human(Socrates)"]          # Socrates is human
]

print("Is Socrates mortal?", prove(kb, "Mortal(Socrates)"))  # True
print("Is Plato mortal?", prove(kb, "Mortal(Plato)"))        # False
