import itertools

# Define the roles and people
roles = ['knight', 'knave', 'spy']
people = ['A', 'B', 'C']

# Define the statements as functions that return True if the statement is true, given a set of roles
def A_says(roles_map):
    # A says: "C is a knave."
    return roles_map['C'] == 'knave'

def B_says(roles_map):
    # B says: "A is a knight."
    return roles_map['A'] == 'knight'

def C_says(roles_map):
    # C says: "I am the spy."
    return roles_map['C'] == 'spy'

statements = {
    'A': A_says,
    'B': B_says,
    'C': C_says,
}

solutions_found = 0
print("--- Checking all possible realities ---")

# Iterate over all unique permutations of roles for the people
for idx, perm in enumerate(itertools.permutations(roles), 1):
    # Create a dictionary mapping people to their assigned roles for this permutation
    assigned_roles = dict(zip(people, perm))
    
    print(f"\n#{idx} Checking permutation: A={perm[0]}, B={perm[1]}, C={perm[2]}")

    is_consistent = True
    # Check for consistency for each person
    for person in people:
        person_role = assigned_roles[person]
        statement_is_true = statements[person](assigned_roles)
        
        # Apply the rules of logic for each role
        if person_role == 'knight':
            if not statement_is_true:
                print(f"  - Inconsistent: Knight {person} made a false statement.")
                is_consistent = False
                break
        elif person_role == 'knave':
            if statement_is_true:
                print(f"  - Inconsistent: Knave {person} made a true statement.")
                is_consistent = False
                break
        elif person_role == 'spy':
            # The spy's statement can be true or false, so it never breaks consistency.
            print(f"  - Consistent: Spy {person}'s statement is ignored.")
            pass
            
    if is_consistent:
        solutions_found += 1
        print("  >>> This permutation is a valid solution.")
        # Storing the solution to print at the end
        solution = assigned_roles

print("\n--- Verification Complete ---")
if solutions_found == 1:
    print("A single solution was found:")
    for person, role in solution.items():
        print(f"  {person} is the {role}")
elif solutions_found > 1:
    print(f"Error: {solutions_found} solutions were found. The puzzle is ambiguous.")
else:
    print("No solutions found.")