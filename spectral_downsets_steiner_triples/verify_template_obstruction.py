"""Exact corroboration of TEMPLATE_OBSTRUCTION.md; Python 3.11+, stdlib.

Universal coverage is the written proof. These four designs validate the
actual seven-parameter equations and explicit negative quadratic witnesses.
Author: six-downset-2, researcher. Assertions must remain enabled.
"""
import argparse
import copy
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

from certificates import affine_sts9, check_sts, cyclic_sts13
from verify import check_definition, matrix_hash, rejects, relabel

NAMES = ['a','b','u','c','h1','h2','t']


def entry(a,b,s,U):
    coefficients = [0]*7
    if not a or not b:
        return 1,coefficients
    if a == b:
        return s,coefficients
    if a&b:
        return 0,coefficients
    k,l = sorted((a.bit_count(),b.bit_count()))
    if (k,l) == (1,1):
        coefficients[0] = 1
    elif (k,l) == (1,2):
        coefficients[1] = 1
        coefficients[2] = -int(a|b in U)
    elif (k,l) == (2,2):
        coefficients[3] = 1
    elif (k,l) == (1,3):
        coefficients[4] = 1
    elif (k,l) == (2,3):
        coefficients[5] = 1
    elif (k,l) == (3,3):
        coefficients[6] = 1
    else:
        raise AssertionError('unsupported set size')
    return 0,coefficients


def solve(equations):
    pivots = {}
    for values in equations:
        row = list(map(F,values))
        for c,p in sorted(pivots.items()):
            f = row[c]
            row = [a-f*b for a,b in zip(row,p)]
        nonzero = [c for c in range(7) if row[c]]
        if not nonzero:
            assert not row[7], 'inconsistent affine equations'
            continue
        c = nonzero[0]
        f = row[c]
        pivots[c] = [x/f for x in row]
    assert set(pivots) == set(range(7)), 'weights not uniquely forced'
    result = [F(0)]*7
    for c,p in sorted(pivots.items(),reverse=True):
        result[c] = p[7]-sum(p[j]*result[j] for j in range(c+1,7))
    assert all(sum(F(a)*x for a,x in zip(row[:7],result)) == row[7]
               for row in equations)
    return result


def regular(U,v,m):
    assert 6*len(U) == m*v*(v-1) and all(t.bit_count() == 3 for t in U)
    assert all(0 < t < 1<<v for t in U)
    for i,j in itertools.combinations(range(v),2):
        pair = (1<<i)|(1<<j)
        assert sum(t&pair == pair for t in U) == m


def check_case(U,v,m):
    regular(U,v,m)
    D = sorted({0} | {1<<i for i in range(v)} |
               {sum(1<<i for i in pair) for pair in itertools.combinations(range(v),2)} |
               U, key=lambda a:(a.bit_count(),a))
    assert m*(v-1)%2 == 0 and m*v*(v-1)%6 == 0
    N,s = 1+v+v*(v-1)//2+m*v*(v-1)//6, v+m*(v-1)//2
    assert len(D) == N
    supports = [(range(N),N)] + [([j for j,a in enumerate(D) if a>>i&1],s)
                                for i in range(v)]
    assert all(len(support) == s for support,rhs in supports[1:])
    equations = set()
    for a in D:
        for support,target in supports:
            row = [0]*7
            rhs = target
            for j in support:
                constant,cs = entry(a,D[j],s,U)
                rhs -= constant
                row = [x+y for x,y in zip(row,cs)]
            equations.add(tuple(row+[rhs]))
    weights = solve(sorted(equations))
    h2 = F(v*(v-5)*3+2*m*(v-1)*(v-3),3*(v-3)*(v-4))
    h1 = F(2*v,v-3)-F(m*(v-1),6)
    c = 2*((v-1)*s+1-N-F(m*(v-3)*(v-4),3)*h2)/((v-2)*(v-3))
    b = s-(v-3)*c-F(m*(v-5),2)*h2
    a = F(m*(v-3)*(6-m*(v-1)),36)
    expected = [a,b,h2,c,h1,h2,F(0)]
    assert weights == expected
    Q = []
    for a in D:
        row = []
        for b in D:
            constant,cs = entry(a,b,s,U)
            row.append(F(constant)+sum(x*y for x,y in zip(cs,weights)))
        Q.append(row)
    check_definition(D,s,Q,psd=False)
    indices = [j for j,a in enumerate(D) if a.bit_count() == 1]
    witness = sum(Q[i][j] for i in indices for j in indices)
    assert witness == v*(F(s)+(v-1)*weights[0]) < 0
    return D,s,Q, {'v':v,'m':m,'N':N,'s':s,'affine_rank':7,
                   'weights':dict(zip(NAMES,map(str,weights))),
                   'singleton_constant_eigenvalue':str(F(s)+(v-1)*weights[0]),
                   'singleton_ones_quadratic_form':str(witness),
                   'matrix_sha256':matrix_hash(Q)}


def run():
    here = Path(__file__).parent
    two = json.loads((here/'two9_certificates.json').read_text())
    four = json.loads((here/'four9_certificates.json').read_text())
    first = set(affine_sts9())
    U2 = set(two['first_blocks'])|set(two['cases'][0]['second_blocks'])
    U4 = set().union(*map(set,four['cases'][0]['layers']))
    U6 = {sum(1<<i for i in t) for t in itertools.combinations(range(9),3)}-first
    output = []
    first13 = cyclic_sts13()
    # Literal checked point permutation; discovery is not a proof input.
    p13 = [8, 4, 5, 9, 7, 12, 11, 2, 6, 1, 10, 0, 3]
    assert sorted(p13) == list(range(13))
    second13 = [relabel(a,p13) for a in first13]
    check_sts(13,first13)
    check_sts(13,second13)
    assert not set(first13)&set(second13)
    U13 = set(first13)|set(second13)
    for v,m,U in [(9,2,U2),(9,4,U4),(9,6,U6),(13,2,U13)]:
        D,s,Q,record = check_case(U,v,m)
        output.append(record)
    bad = copy.deepcopy(Q)
    bad[0][1] += 1
    rejects(lambda:check_definition(D,s,bad,psd=False))
    malformed = set(U6)
    malformed.remove(min(malformed))
    rejects(lambda:regular(malformed,9,6))
    return {'arithmetic':'fractions.Fraction and integer set masks',
            'universal_scope':'Analytic obstruction for v>=9,2<=m<=v-3 when completing-point counts vary; in particular all simple 2-(v,3,2) and the even-degree9 cases. Finite checks corroborate four inputs.',
            'cases':output,'rejection_controls':2}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    result = run()
    path = Path(__file__).with_name('template_obstruction_expected.json')
    if args.check:
        assert result == json.loads(path.read_text()), 'expected-output mismatch'
    if args.write_expected:
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
