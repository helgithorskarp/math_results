"""Check the colouring theorem, exact source contacts, and positive auxiliary data."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
from exact import (HERE, F, ONE, ZERO, add, sub, scale, mul, conj, norm, points,
                   differences, directions, residue, quotient_directions,
                   quotient_colour, require)

def word(s, n, k):
    require(isinstance(s,str) and len(s) == n and all(c in '01234'[:k] for c in s),
            'invalid colour word')
    return tuple(map(int,s))

def auxiliary(A):
    cert = json.loads((HERE/'auxiliary_certificate.json').read_text())
    ids = cert['source_indices']
    require(len(ids) == 114 and ids == sorted(set(ids))
            and all(isinstance(i,int) and 0 <= i < len(A) for i in ids),
            'auxiliary source indices')
    P = [A[i] for i in ids]
    E1,E43 = [],[]
    for a,b in combinations(range(114),2):
        n = norm(sub(P[a],P[b]))
        if n == ONE:
            E1.append((a,b))
        elif n == scale(ONE,F(4,3)):
            E43.append((a,b))
    edges = sorted(E1+E43)
    five = word(cert['five_colouring'],114,5)
    require(all(five[a] != five[b] for a,b in edges), 'auxiliary 5-colouring')
    require(len(cert['deletion_four_colourings']) == 114, 'missing deletion')
    for v,s in enumerate(cert['deletion_four_colourings']):
        c = word(s,114,4)
        require(all(c[a] != c[b] for a,b in edges if v not in (a,b)),
                'auxiliary deletion '+str(v))
    clauses = [[4*v+c+1 for c in range(4)] for v in range(114)]
    clauses += [[-4*a-c-1,-4*b-c-1] for a,b in edges for c in range(4)]
    clauses += [[1]]  # Global colour permutation can always colour vertex 0 by 0.
    cnf = 'p cnf 456 '+str(len(clauses))+'\n'
    cnf += ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
    return P,cnf,{'vertices':114,'unit_edges':len(E1),'distance_4_over_3_edges':len(E43),
                  'edges':len(edges),'checked_deletions':114,
                  'four_colour_cnf_sha256':sha256(cnf.encode()).hexdigest()}

def run(emit=None, audit=None):
    # The quotient check proves the universal colouring rule, independently of
    # every Parts coordinate or auxiliary SAT query.
    Q = quotient_directions()
    labels = list(product(range(4),repeat=4))
    require(len(Q) == 15, 'quotient direction count')
    edges = set()
    for z in labels:
        for d in Q:
            w = tuple((x+y)%4 for x,y in zip(z,d))
            require(quotient_colour(z) != quotient_colour(w), 'quotient colour failure')
            edges.add(tuple(sorted((z,w))))
    witness = json.loads((HERE/'quotient_certificate.json').read_text())
    require(witness['modulus'] == 4 and set(map(tuple,witness['directions'])) == Q,
            'quotient witness directions')
    require(witness['colours'] == ''.join(str(quotient_colour(z)) for z in labels),
            'Boolean formula / SAT witness mismatch')
    require(len(edges) == witness['edges'] == 1920, 'quotient edges')
    A = points()
    for p in A:
        residue(p)
    pairs = differences(A)
    dirs = directions(pairs)
    kinds = Counter()
    full_edges = 0
    for d,r in dirs:
        kinds['horizontal' if d == ZERO else 'vertical' if r == ZERO
              else 'diagonal' if d == r else 'mixed'] += 1
        require(residue(d)+residue(r) in Q, 'direction escapes quotient')
        full_edges += len(pairs[d])*len(pairs[r])
    P,cnf,aux = auxiliary(A)
    pp = differences(P)
    core_edges = sum(len(pp.get(d,()))*len(pp.get(r,())) for d,r in dirs)
    # A mixed physical contact outside the obstruction's residue set.
    alpha = (F(0),F(0),F(1),F(0))
    d,r = scale(alpha,F(1,15)),scale(alpha,F(3,5))
    # (1-u)d+u r = -sqrt(13)/5 + 2*alpha/5.
    x,y = scale(add(scale(d,3),scale(r,5)),F(1,8)),scale(mul(alpha,sub(r,d)),F(1,8))
    require(x == scale(alpha,F(2,5)) and y == scale(ONE,F(-1,5)),
            'explicit mixed contact coordinates')
    require(add(norm(x),scale(norm(y),13)) == ONE, 'mixed contact norm')
    require(add(mul(x,conj(y)),mul(conj(x),y)) == ZERO, 'mixed real cross term')
    omega = scale(sub(alpha,ONE),F(1,2))
    require(norm(omega) == ONE, 'escape rotation norm')
    escaped = residue(mul(omega,d))+residue(mul(omega,r))
    require(escaped == (2,1,2,1) and escaped not in Q, 'mixed residue escape')
    require(all(quotient_colour(z) == quotient_colour(tuple((a+b)%4 for a,b in zip(z,escaped)))
                for z in labels), 'mixed contact must break this colouring at all residues')
    ds = sorted(pairs)
    integer_ds = [tuple(x*12 for x in d) for d in ds]
    require(all(x.denominator == 1 for d in integer_ds for x in d), 'denominator 12')
    expected = {(ds.index(d),ds.index(r)) for d,r in dirs}
    expected |= {(ds.index(scale(d,-1)),ds.index(scale(r,-1))) for d,r in dirs}
    if audit is not None:
        rows = [tuple(map(int,l.split())) for l in Path(audit).read_text().splitlines()]
        require(len(rows) == len(set(rows)) and set(rows) == expected,
                'direct polynomial audit differs entrywise')
    if emit is not None:
        target = Path(emit)
        target.mkdir(parents=True,exist_ok=True)
        (target/'augmented114.cnf').write_text(cnf)
        (target/'differences.txt').write_text(str(len(ds))+'\n'+''.join(
            ' '.join(str(int(x)) for x in d)+'\n' for d in integer_ds))
    return {'quotient_vertices':256,'quotient_edges':1920,'quotient_directions':15,
            'source_vertices':374,'source_differences':len(ds),
            'physical_weighted_vertices':374**2,'physical_unit_edges':full_edges,
            'directions_up_to_sign':len(dirs),'direction_types':dict(kinds),
            'auxiliary':aux,'weighted_auxiliary_vertices':114**2,
            'weighted_auxiliary_unit_edges':core_edges,
            'mixed_escape_residue':list(escaped),
            'record_improvement':False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit',help='write reproducible solver/audit inputs outside the repository')
    parser.add_argument('--audit',help='check direct_contacts.cpp output entrywise')
    args = parser.parse_args()
    print(json.dumps(run(args.emit,args.audit),indent=2,sort_keys=True))
