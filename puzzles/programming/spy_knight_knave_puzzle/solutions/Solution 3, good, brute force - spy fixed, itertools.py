import itertools

# Define the roles and people
roles = ['knight', 'knave', 'spy']
people = ['A', 'B', 'C']

# Define the statements
def A_says(roles):
    return roles['C'] == 'knave'

def B_says(roles):
    return roles['A'] == 'knight'

def C_says(roles):
    # The spy can choose to lie or tell the truth independently
    return True

statements = {
    'A': A_says,
    'B': B_says,
    'C': C_says,
}

# Initialize a counter for solutions found
solutions_found = 0

# Iterate over all permutations of roles
for idx, perm in enumerate(itertools.permutations(roles), 1):
    assigned_roles = dict(zip(people, perm))  # Assign roles to people
    
    # Print the current permutation of roles
    print(f"\nPermutation {idx}:")
    for person, role in assigned_roles.items():
        print(f"{person} is the {role}")
    
    # Check statements for each person
    print("Statements:")
    for person in people:
        statement_result = statements[person](assigned_roles)
        print(f"  {person} says: {statement_result}")
    
    # Check if all statements are true according to the assigned roles
    if all(statements[person](assigned_roles) for person in people):
        print("\nSolution found:")
        for person, role in assigned_roles.items():
            print(f"{person} is the {role}")
        
        # Increment the counter for solutions found
        solutions_found += 1
        
        # Continue checking other permutations if desired (or break here)
        continue  # Continue to next permutation

print(f"\nTotal solutions found: {solutions_found}")

Or:

def solve_puzzle():                                                                                                                                                                                              
      identities = ["knight", "knave", "spy"]                                                                                                                                                                      
      statements = {                                                                                                                                                                                               
          "A": lambda a, b, c: c == "knave" or (c == "spy" and b == "knave"),                                                                                                                                      
          "B": lambda a, b, c: a == "knight" or (a == "knave" and c == "knave"),                                                                                                                                   
          "C": lambda a, b, c: c == "spy" or (c == "knave" and b == "spy")                                                                                                                                         
      }                                                                                                                                                                                                            
                                                                                                                                                                                                                   
      for a, b, c in itertools.product(identities, identities, identities):                                                                                                                                        
          if a == "knight" and statements["A"](a, b, c) and statements["B"](a, b, c) and statements["C"](a, b, c):                                                                                                 
              return {"A": a, "B": b, "C": c}                                                                                                                                                                      
                                                                                                                                                                                                                   
      return None                                                                                                                                                                                                  
                                                                                                                                                                                                                   
  import itertools                                                                                                                                                                                                 
                                                                                                                                                                                                                   
  solution = solve_puzzle()                                                                                                                                                                                        
  if solution:                                                                                                                                                                                                     
      print("A is the", solution["A"])                                                                                                                                                                             
      print("B is the", solution["B"])                                                                                                                                                                             
      print("C is the", solution["C"])                                                                                                                                                                             
  else:                                                                                                                                                                                                            
      print("No solution found")