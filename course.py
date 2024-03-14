def load_dimacs(file_name):
    dimacs = []
    with open(file_name, 'r') as dimacsFile:
        for line in dimacsFile:
            if line[0] not in ('c', 'p'):
                p = line.split('0')[0].strip().split(' ')
                clause = []  
                for char in p:
                    clause.append(int(char))
                dimacs.append(clause) 
    return dimacs
        

def simple_sat_solve(clause_set):
    def backtrack(index, assignment):
        if index == len(clause_set):
            return True

        for literal in clause_set[index]:
            if literal in assignment:
                if assignment[literal]:
                    if backtrack(index + 1, assignment):
                        return True
            elif -literal not in assignment:
                assignment[literal] = True
                if backtrack(index + 1, assignment):
                    return True
                assignment[literal] = False
        return False

    partial_assignment = {}
    if backtrack(0, partial_assignment):
        satisfying_assign = []
        for literal, value in partial_assignment.items():
            if value:
                satisfying_assign.append(literal)
        return satisfying_assign
    

    else:
        return False
    
def branching_sat_solve(clause_set, partial_assignment=[]):
    if not clause_set:
        return partial_assignment



    all_literals = set()
    for clause in clause_set:
       for literal in clause:
          all_literals.add(abs(literal))

    assigned_literals = set()
    for literal in partial_assignment:
       assigned_literals.add(abs(literal))
    unassigned_vars = all_literals - assigned_literals

    if not unassigned_vars: 
        return False
    
    
    
    
    var = unassigned_vars.pop()  

    edited_clause = []
    for clause in clause_set:
      if var not in clause:
          edited_clause.append(clause)

    new_partial = partial_assignment + [var]
    true_asg = branching_sat_solve(edited_clause, new_partial)

    if true_asg: 
        return true_asg




    edited_clause_negate = []
    for clause in clause_set:
        if -var not in clause:
            edited_clause_negate.append(clause)

    new_partial_negate = partial_assignment + [-var]
    false_asg = branching_sat_solve(edited_clause_negate, new_partial_negate)
    if false_asg: 
        return false_asg


    return False

def unit_propagate(clause_set):
    def helper_unit_clause(clauses):
        for clause in clauses:
            if len(clause) == 1:
                return clause
        return None

    while True:
        unit_clause = helper_unit_clause(clause_set)
        if unit_clause is None:
            break



        literal = unit_clause[0]

        clause_edited = []
        for clause in clause_set:
            if unit_clause not in [clause]:
                clause_edited.append(clause)

        clause_no_neg = []
        for clause in clause_edited:
            if -literal not in clause:
                new_clause = clause - {-literal}
                clause_no_neg.append(new_clause)

        final_clause_set = []
        for clause in clause_no_neg:
            if clause:
                final_clause_set.append(clause)

        clause_set = final_clause_set


        
    return clause_set
