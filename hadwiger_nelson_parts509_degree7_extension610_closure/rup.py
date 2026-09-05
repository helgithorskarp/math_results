"""Small addition-only reverse-unit-propagation checker; no SAT library."""


def conflict_by_units(formula, assumptions):
    true=set(assumptions)
    if any(-literal in true for literal in true):
        return True
    while True:
        changed=False
        for clause in formula:
            if any(literal in true for literal in clause):
                continue
            remaining={literal for literal in clause if -literal not in true}
            if not remaining:
                return True
            if len(remaining)==1:
                true.update(remaining)
                changed=True
        if not changed:
            return False


def is_rup(formula, clause):
    return conflict_by_units(formula, [-literal for literal in clause])


def check(formula, proof):
    if not proof or proof[-1]:
        raise ValueError('proof must end with the empty clause')
    active=[list(row) for row in formula]
    for i,clause in enumerate(proof):
        if not is_rup(active,clause):
            raise ValueError(f'addition {i+1} is not RUP')
        active.append(clause)
    return len(proof)


def parse_clause(line, variables):
    tokens=list(map(int,line.split()))
    if not tokens or tokens[-1]!=0 or any(v==0 or abs(v)>variables for v in tokens[:-1]):
        raise ValueError('invalid clause')
    return tokens[:-1]


def parse_dimacs(data):
    lines=data.decode('ascii').splitlines()
    kind,format_,variables,count=lines[0].split()
    if (kind,format_)!=('p','cnf'):
        raise ValueError('invalid header')
    variables,count=int(variables),int(count)
    rows=[parse_clause(line,variables) for line in lines[1:]]
    if len(rows)!=count:
        raise ValueError('clause count differs')
    return variables,rows
