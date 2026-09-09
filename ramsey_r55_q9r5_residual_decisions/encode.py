"""Definition-level necessary residual formula for all q9,r5 tasks."""
from itertools import combinations
from pathlib import Path
import hashlib

CORE_SHA = '6a3da7f0687c392420f190db0643b5c5b7ecb1a3c5ed098c7d96200185a5f010'
PAIRS = tuple(combinations(range(23), 2))

def require(ok, message):
    if not ok:
        raise ValueError(message)

def catalogue(path):
    data = Path(path).read_bytes()
    require(hashlib.sha256(data).hexdigest() == CORE_SHA, 'catalogue hash')
    rows = data.splitlines()
    require(len(rows) == 362, 'catalogue cardinality')
    return rows

def core_edges(row):
    require(len(row) == 5 and row[0] == 70, 'graph6 header/length')
    bits = ''.join(f'{x-63:06b}' for x in row[1:])
    require(all(63 <= x <= 126 for x in row[1:]) and bits[21:] == '000', 'graph6 payload')
    return {(u+16,v+16): int(bits[i])
            for i,(u,v) in enumerate(( (u,v) for v in range(1,7) for u in range(v) ))}

def fixed_edges(row):
    fixed = core_edges(row)
    for b in range(4):
        fixed.update({(u,v):0 for u,v in combinations(range(4*b,4*b+4),2)})
    require(len(fixed) == 45, 'fixed edge count')
    return fixed

def formula(row):
    fixed = fixed_edges(row)
    variables = {e:i+1 for i,e in enumerate(e for e in PAIRS if e not in fixed)}
    clauses = []
    for k, forbidden in ((4,1),(5,0)):
        for vertices in combinations(range(23),k):
            edges = tuple(combinations(vertices,2))
            if any(e in fixed and fixed[e] != forbidden for e in edges):
                continue
            clause = [(1 if forbidden == 0 else -1)*variables[e] for e in edges if e not in fixed]
            clauses.append(clause)
    require(len(variables) == 208, 'variable count')
    return fixed, variables, clauses

def dimacs(clauses):
    return ('p cnf 208 '+str(len(clauses))+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()

def decode(row, model):
    fixed, variables, _ = formula(row)
    values = {abs(x):int(x>0) for x in model}
    require(all(v in values for v in variables.values()), 'incomplete model')
    word = sum((fixed[e] if e in fixed else values[variables[e]]) << i for i,e in enumerate(PAIRS))
    return f'{word:064x}'

def witness(row, word):
    require(isinstance(word,str) and len(word)==64 and all(c in '0123456789abcdef' for c in word), 'edge word format')
    value = int(word,16)
    require(value < 1 << 253, 'edge word padding')
    edges = {e: (value>>i)&1 for i,e in enumerate(PAIRS)}
    require(all(edges[e] == x for e,x in fixed_edges(row).items()), 'fixed edges')
    for k,forbidden in ((4,1),(5,0)):
        for vs in combinations(range(23),k):
            require(not all(edges[e] == forbidden for e in combinations(vs,2)), f'forbidden {forbidden}-K{k}: {vs}')
    return {'red_edges':value.bit_count(),'literal_four_sets':8855,'literal_five_sets':33649}
