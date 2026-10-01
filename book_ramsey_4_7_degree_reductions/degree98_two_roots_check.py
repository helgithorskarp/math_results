"""Exact necessary-defect exclusion for the 98-edge (2,20,0) histogram.
Standalone standard-library program; no predecessor imports.
Actual author: six-books-1, role researcher, 2026-10-01.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from math import gcd, isqrt
from pathlib import Path
from random import Random
import json

N=22
HISTOGRAMS=((2,20,0),)
DEGREES=[8]*2+[9]*20

def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def determinant(matrix):
    a = [row[:] for row in matrix]
    n, previous, sign = len(a), 1, 1
    require(n and all(len(row) == n for row in a), "nonsquare determinant")
    for k in range(n - 1):
        row = next((i for i in range(k, n) if a[i][k]), None)
        if row is None:
            return 0
        if row != k:
            a[row], a[k] = a[k], a[row]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                require(numerator % previous == 0, "inexact Bareiss division")
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def integer_rank(matrix):
    """Exact rational rank using integer row operations and gcd reduction."""
    a = [row[:] for row in matrix]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][column]
        for i in range(rank + 1, len(a)):
            v = a[i][column]
            if not v:
                continue
            a[i] = [p * x - v * y for x, y in zip(a[i], a[rank])]
            divisor = 0
            for value in a[i]:
                divisor = gcd(divisor, value)
            if divisor:
                a[i] = [x // divisor for x in a[i]]
        rank += 1
    return rank


def forced_matrix(degrees, f):
    y = [10 - d for d in degrees]
    return [[25 * (i == j) + 24 - 4 * (y[i] + y[j])
             - 4 * (degrees[i] == 9) * (i == j) - 4 * f[i][j]
             for j in range(N)] for i in range(N)]


def signed_graphs(degrees):
    remaining = list(degrees)
    red = [set() for _ in degrees]
    while any(remaining):
        order = sorted((i for i, value in enumerate(remaining) if value), key=lambda i: (-remaining[i], i))
        i = order[0]
        demand = remaining[i]
        require(demand < len(order), "nongraphical control histogram")
        remaining[i] = 0
        for j in order[1:demand + 1]:
            red[i].add(j)
            red[j].add(i)
            remaining[j] -= 1
    pairs = list(combinations(range(N), 2))
    for seed in range(24):
        r = [row.copy() for row in red]
        rng = Random(9847 + seed)
        for _ in range(80):
            edges = [(i, j) for i, j in pairs if j in r[i]]
            (a, b), (c, d) = rng.sample(edges, 2)
            if len({a, b, c, d}) < 4 or c in r[a] or d in r[b]:
                continue
            for i, j in ((a, b), (c, d)):
                r[i].remove(j)
                r[j].remove(i)
            for i, j in ((a, c), (b, d)):
                r[i].add(j)
                r[j].add(i)
        require(list(map(len, r)) == degrees, "signed control degrees changed")
        yield sum(1 << bit for bit, (i, j) in enumerate(pairs) if j in r[i]), r


def controls():
    require(determinant([[0, 1], [2, 3]]) == -2 and determinant([[1, 2], [2, 4]]) == 0, "determinant controls")
    require(integer_rank([[0, 1], [2, 3]]) == 2 and integer_rank([[1, 2], [2, 4]]) == 1, "rank controls")
    fixture = Path(__file__).with_name("baseline21.rows").read_text().split()
    require(len(fixture) == 21 and all(len(row) == 21 and set(row) <= {"0", "1"} for row in fixture), "bad baseline")
    red = [{j for j, value in enumerate(row) if value == "1"} for row in fixture]
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    require(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21)) for i in range(21)), "baseline symmetry")
    hist = Counter(map(len, red))
    maxima = [max(len(rows[i] & rows[j]) for i, j in combinations(range(21), 2) if j in rows[i]) for rows in (red, blue)]
    require(hist == {8: 4, 9: 16, 10: 1} and maxima == [3, 6], "known baseline mismatch")
    signed = []
    for histogram in HISTOGRAMS:
        degrees = [d for d, count in zip((8, 9, 10), histogram) for _ in range(count)]
        masks = []
        for mask, r in signed_graphs(degrees):
            b = [set(range(N)) - r[i] - {i} for i in range(N)]
            f = [[0] * N for _ in range(N)]
            for i, j in combinations(range(N), 2):
                f[i][j] = f[j][i] = 3 - len(r[i] & r[j]) if j in r[i] else 6 - len(b[i] & b[j])
            h = forced_matrix(degrees, f)
            k = [[2 * (j in r[i]) + (2 * degrees[i] - 17) * (i == j) for j in range(N)] for i in range(N)]
            for i in range(N):
                require(sum(f[i]) == sum(degrees) - 294 + 38 * degrees[i] - degrees[i] ** 2
                        - 2 * sum(degrees[j] for j in r[i]), "literal incident identity")
                require((sum(f[i]) - degrees[i] % 2) % 2 == 0, "signed parity")
                for j in range(N):
                    require(sum(k[i][t] * k[t][j] for t in range(N)) == h[i][j], "literal square identity")
            require(sum(map(sum, f)) == 28 + histogram[1], "signed total surplus")
            masks.append(mask)
        require(len(set(masks)) == 24, "duplicate signed controls")
        signed.append({"histogram": list(histogram), "red_masks": masks, "graphs": 24,
                       "incident_identity_checks": 528, "square_identity_entries": 11616})
    return {"determinant_controls": [-2, 0], "rank_controls": [2, 1],
            "baseline21_red_edges": sum(map(len, red)) // 2,
            "baseline21_degree_histogram": [hist[d] for d in (8, 9, 10)],
            "baseline21_max_pages": maxima, "signed": signed}


def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def transposed(a): return list(map(list,zip(*a)))

def apply(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]

def cross_domain():
    rows=[r for r in product(range(3),repeat=4) if sum(r)==2]
    require(len(rows)==10,"two-unit row coverage")
    def fill(prefix,remaining):
        if len(prefix)==4:
            if remaining==[0]*4:yield prefix
            return
        for row in rows:
            if all(row[j]<=remaining[j] for j in range(4)):
                yield from fill(prefix+[list(row)],[remaining[j]-row[j] for j in range(4)])
    yield from fill([],[2]*4)

def full_defect(m):
    f=[[0]*N for _ in range(N)]
    def edge(i,j,w=1):f[i][j]=f[j][i]=w
    for i,j in combinations(range(2,5),2):edge(i,j)
    for center in range(3):
        for j in range(13+3*center,16+3*center):edge(2+center,j)
    for i,j in [(5,6),(7,8),(9,10),(11,12)]:edge(i,j)
    for i in range(4):
        for j in range(4):edge(5+i,9+j,m[i][j])
    return f

def orbit_key(m):
    matching={frozenset((0,1)),frozenset((2,3))}
    group=[p for p in permutations(range(4)) if {frozenset((p[0],p[1])),frozenset((p[2],p[3]))}==matching]
    require(len(group)==8,"matching symmetry group")
    return min(tuple(m[p[i]][q[j]] for i in range(4) for j in range(4)) for p in group for q in group)

def lattice_certificate():
    columns=[]
    for first in (13,16,19):
        for offset in (0,1):
            v=[0]*N;v[first+offset]=1;v[first+2]=-1;columns.append(v)
    b=transposed(columns)
    gram=multiply(transposed(b),b)
    require(gram==[[2 if i==j else 1 if i//2==j//2 else 0 for j in range(6)] for i in range(6)],"leaf lattice Gram")
    require(determinant(gram)==27 and integer_rank(b)==6,"primitive leaf basis")
    # The two free coordinates in each leaf triple are an integral left inverse.
    selectors=[13,14,16,17,19,20]
    require([b[i] for i in selectors]==[[int(i==j) for j in range(6)] for i in range(6)],"integral lattice coordinate inverse")
    # Rational self-adjoint roots exist on this Gram plane: integrality matters.
    s=[[Fraction(0),Fraction(5,2)],[Fraction(2),Fraction(-1)]]
    g=[[2,1],[1,2]];s2=multiply(s,s)
    require(multiply(transposed(s),g)==multiply(g,s),"rational lattice positive control")
    require(all(s2[i][j]+s[i][j]==5*(i==j) for i in range(2) for j in range(2)),"rational quadratic control")
    require(sum(s[i][i] for i in range(2))==-1 and s[0][1].denominator==2,"rational odd trace is permitted")
    # For any integral self-adjoint S, the three paired diagonal entries agree mod2.
    require(all(gram[2*k][2*k+1]%2==1 and gram[2*k][2*k]%2==gram[2*k+1][2*k+1]%2==0 for k in range(3)),"trace parity blocks")
    return {'basis_columns':columns,'gram':gram,'gram_determinant':27,
            'coordinate_selectors':selectors,'rank':6,'eigenvalue':21,
            'adjacency_polynomial':[1,1,-5],'discriminant':21,
            'characteristic_polynomial_power':3,'forced_trace':-3,
            'integral_self_adjoint_trace_parity':0,
            'rational_2plane_control':[['0','5/2'],['2','-1']]}

def check_structural_identities(f,h):
    one=[1]*N;u=[int(i<2) for i in range(N)]
    v=[1,-1]+[0]*20
    hvec=[1]*2+[2]*3+[1]*8+[0]*9
    w=[0]*5+[1]*4+[-1]*4+[0]*9
    p=[0]*2+[3]*3+[2]*8+[1]*9
    require(apply(f,one)==[one[i]-3*u[i]+2*hvec[i] for i in range(N)],"F row identity")
    require(apply(f,u)==[0]*N,"zero root defect rows")
    require(apply(f,hvec)==[2*one[i]-3*u[i]+hvec[i] for i in range(N)],"F cyclic identity")
    require(apply(f,p)==[3*x for x in p] and apply(f,w)==[-x for x in w],"positive-vector and contrast identities")
    q=[[9,0,6],[-1,0,5],[0,1,0]]
    diagonal=[[1,0,0],[-2,-1,-2],[0,0,1]]
    k=[[2*q[i][j]+diagonal[i][j] for j in range(3)] for i in range(3)]
    basis=transposed([one,u,hvec])
    require(multiply(h,basis)==multiply(basis,multiply(k,k)),"forced cyclic square")
    require(apply(h,v)==[25*x for x in v] and apply(h,w)==[25*x for x in w],"root contrast square")

def build(with_matrices=False):
    certificate=lattice_certificate();b=transposed(certificate['basis_columns'])
    records=[];corpus={};groups={};squares=[]
    for m in cross_domain():
        flat=[x for row in m for x in row]
        f=full_defect(m);h=forced_matrix(DEGREES,f)
        check_structural_identities(f,h)
        value=determinant(h);require(value>0,"nonpositive forced determinant")
        root=isqrt(value);square=root*root==value
        records.append([flat,value,root,sha256(encode(f)).hexdigest(),sha256(encode(h)).hexdigest(),square])
        key=orbit_key(m)
        if key not in groups:groups[key]={'flat_M':list(key),'labeled_count':0,'detH':value,'square':square}
        require(groups[key]['detH']==value,"orbit determinant differs")
        groups[key]['labeled_count']+=1
        if square:
            shifted=[[h[i][j]-21*(i==j) for j in range(N)] for i in range(N)]
            rank=integer_rank(shifted)
            require(rank==16 and multiply(h,b)==[[21*x for x in row] for row in b],"entire21 eigenspace bridge")
            squares.append({'flat_M':flat,'rank_H_minus21I':rank})
        if with_matrices:corpus[','.join(map(str,flat))]={'F':f,'H':h}
    require(len(records)==282 and len(squares)==18 and len(groups)==16,"complete cross census")
    require(sum(r['labeled_count'] for r in groups.values())==282,"orbit coverage")
    out={'agent':'six-books-1','role':'researcher','version':1,'histogram':[2,20,0],
         'record_fields':['flat_M','det_H','floor_sqrt','F_sha256','H_sha256','square'],
         'row_compositions':10,'labeled_forms':282,'positive_nonsquares':264,'square_forms':18,
         'normal_form_orbits':16,'orbits':[groups[k] for k in sorted(groups)],
         'lattice_certificate':certificate,'square_ranks':squares,'controls':controls(),'records':records}
    return out,corpus

def write_compact(path,data):
    fields=[]
    for key,value in data.items():
        if key=='records':text='[\n'+',\n'.join('    '+json.dumps(row,separators=(',',':')) for row in value)+'\n  ]'
        else:text=json.dumps(value,indent=2)
        fields.append('  '+json.dumps(key)+': '+text)
    path.write_text('{\n'+',\n'.join(fields)+'\n}\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('degree98_two_roots_expected.json'))
    parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--matrices',type=Path)
    args=parser.parse_args()
    result,corpus=build(args.matrices is not None)
    if args.write_expected:write_compact(args.expected,result)
    else:require(result==json.loads(args.expected.read_text()),"expected certificate mismatch")
    if args.matrices:args.matrices.write_text(json.dumps(corpus,separators=(',',':'))+'\n')
    print(json.dumps({'complete':True,'forms':282,'nonsquares':264,'square_cases':18,
                      'square_orbits':3,'full_kernel_rank':6,'integer_trace_obstruction':True,
                      'adjacency_survivors':0,'matrix_records_written':bool(args.matrices)}))

if __name__=='__main__':main()
