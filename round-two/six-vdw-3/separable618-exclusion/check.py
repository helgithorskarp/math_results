#!/usr/bin/env python3
"""Independent clause-set audit, endpoint AP reconstruction and literal controls."""
import argparse, hashlib, itertools, json, math
from pathlib import Path

def need(ok, message):
    if not ok: raise ValueError(message)

def label(q, x, y):
    x, y = sorted((x, y))
    need(0 <= x < y < q, 'Invalid pair')
    return x*(2*q-x-1)//2 + y-x

def parse(text):
    lines = [s.strip() for s in text.splitlines() if s.strip() and not s.startswith('c')]
    header = lines[0].split()
    need(len(header) == 4 and header[:2] == ['p', 'cnf'], 'Bad header')
    n, declared = map(int, header[2:]); rows = set()
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        need(len(values) > 1 and values[-1] == 0, 'Bad clause terminator')
        row = values[:-1]
        need(all(0 < abs(v) <= n for v in row), 'Bad literal')
        need(len(set(map(abs, row))) == len(row), 'Repeated or tautological literal')
        row = tuple(sorted(row, key=abs))
        need(row not in rows, 'Duplicate clause'); rows.add(row)
    need(len(rows) == declared, 'Clause count differs')
    return n, rows

def parameters(case):
    if case == 'no-five': return 4, 5
    if case == 'no-six': return 5, 6
    need(case == 'six', 'Unknown case'); return 6, None

def audit(text, q, case):
    need(q >= 7 and all(q % d for d in range(2, math.isqrt(q) + 1)), 'Prime audit domain')
    seed, forbidden = parameters(case); n, actual = parse(text)
    expected = {(-j,) for j in range(1, seed)}
    for x in range(1, q):
        for y in range(x+1, q):
            z = label(q, x, y)
            expected.update(((x,y,-z), (x,-y,z), (-x,y,z), (-x,-y,-z)))
    ladders = set()
    for first in range(q):
        for second in range(q):
            if first == second: continue
            d = second-first
            row = tuple(sorted(label(q,(first+j*d)%q,(first+(j+3)*d)%q) for j in range(4)))
            need(len(set(row)) == 4, 'Repeated ladder edge')
            ladders.add(row); expected.update((row,tuple(-v for v in row)))
    supports = set()
    if forbidden is not None:
        inverse = pow(forbidden-1, -1, q)
        for first, last in itertools.combinations(range(q), 2):
            d = (last-first)*inverse % q
            support = tuple(sorted((first+j*d)%q for j in range(forbidden)))
            need(len(set(support)) == forbidden, 'Repeated AP point')
            supports.add(support); expected.add(tuple(x for x in support if x))
    need(n == q*(q-1)//2 and actual == expected, 'Complete variable/clause coverage differs')
    return {'q':q, 'case':case, 'seed_length':seed, 'forbidden_AP_length':forbidden,
            'variables':n, 'clauses':len(actual), 'counter_variables':0, 'weight_cap':None,
            'directed_ladders':q*(q-1), 'distinct_ladders':len(ladders),
            'forbidden_AP_supports':len(supports),
            'cnf_sha256':hashlib.sha256(text.encode()).hexdigest()}

def full(u):
    q = len(u)
    return all(len({u[(x+j*d)%q]^u[(x+(j+3)*d)%q] for j in range(4)}) == 2
               for x in range(q) for d in range(1,q))

def avoids(u, k):
    q = len(u)
    return k is None or all(any(u[(x+j*d)%q] for j in range(k)) for x in range(q) for d in range(1,q))

def assignment(u):
    return {label(len(u),x,y):bool(u[x]^u[y]) for x in range(len(u)) for y in range(x+1,len(u))}

def satisfied(rows, values):
    return all(any(values[abs(v)] == (v>0) for v in row) for row in rows)

def small(text,q,case):
    need(q in (7,11,13), 'Bound full Boolean controls to7/11/13')
    audit(text,q,case); _, rows = parse(text); seed, forbidden = parameters(case)
    valid = accepted = normalizations = cyclic = 0; fixtures = []
    for tail in itertools.product((0,1), repeat=q-1):
        u = (0,)+tail; F = full(u); valid += F
        expected = F and not any(u[:seed]) and avoids(u,forbidden)
        need(satisfied(rows,assignment(u)) == expected, 'Complete literal branch semantics differ')
        accepted += expected
        if expected:
            word = [u[t%q]^int(t%6>=3) for t in range(6*q)]
            for start in range(6*q):
                for d in range(1,6*q):
                    need(len({word[(start+j*d)%(6*q)] for j in range(7)}) == 2, 'Literal cyclic positive control failed')
                    cyclic += 1
            fixtures.append(''.join(map(str,u)))
        if not F: continue
        for color in (0,1):
            colored = tuple(b^color for b in u)
            if not avoids(colored,forbidden): continue
            for first in range(q):
                for d in range(1,q):
                    if not all(u[(first+j*d)%q] == color for j in range(seed)): continue
                    pulled = tuple(u[(first+j*d)%q]^color for j in range(q))
                    need(pulled.count(0)==u.count(color) and satisfied(rows,assignment(pulled)), 'Lost affine/color normalization')
                    normalizations += 1
    return {'q':q, 'case':case, 'origin_normalized_words':1<<(q-1), 'full_F_words':valid,
            'accepted':accepted, 'all_eligible_normalizations':normalizations,
            'literal_positive_cyclic_APs':cyclic, 'fixtures':fixtures}

def controls(text,q,case):
    n, rows = parse(text); seed,_ = parameters(case)
    changes = [rows-{(-1,)}, (rows-{(-(seed-1),)})|{(seed-1,)}, rows-{min(rows)}]
    for damaged in changes:
        raw = f'p cnf {n} {len(damaged)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(damaged))
        try: audit(raw,q,case)
        except ValueError: pass
        else: raise ValueError('Damaged model accepted')
    try: audit(text.replace(f'p cnf {n} ',f'p cnf {n+1} ',1),q,case)
    except ValueError: pass
    else: raise ValueError('Wrong dimension accepted')
    return 4

def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('cnf',type=Path)
    p.add_argument('--q',type=int,default=103); p.add_argument('--case',choices=('no-five','no-six','six'),required=True)
    p.add_argument('--small',action='store_true'); p.add_argument('--controls',action='store_true'); a=p.parse_args()
    text=a.cnf.read_text(); result=small(text,a.q,a.case) if a.small else audit(text,a.q,a.case)
    if a.controls: result['model_corruptions_rejected']=controls(text,a.q,a.case)
    print(json.dumps(result,sort_keys=True))

if __name__ == '__main__': main()
