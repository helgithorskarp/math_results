"""Different same-author algorithm: sparse integers, reverse tree, modular gcd.

Imports neither the primary producer nor its dense arithmetic kernel.
All complete raw polynomials and masks are compared, never just counts.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm, comb, isqrt
from hashlib import sha256
from time import monotonic
import argparse, json

R = {(1, 0): 1}
D = {(0, 0): 2, (1, 0): -1}
ONE = {(0, 0): 1}
TWO = {(0, 0): 2}
MU = {(0, 0): 2, (1, 0): 1}
LO, HI = F(7, 10), F(3, 4)
PRIME = 65521
if any(PRIME % d == 0 for d in range(2, isqrt(PRIME)+1)):
    raise ValueError('Modular gcd requires a proved prime modulus')
PARENT_SHA = 'a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def canon(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':'))+'\n'


def plus(a, b):
    out = dict(a)
    for k, x in b.items():
        out[k] = out.get(k, 0)+x
        if not out[k]:
            del out[k]
    return out


def minus(a):
    return {k: -x for k, x in a.items()}


def times(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, h), y in b.items():
            key = i+k, j+h
            out[key] = out.get(key, 0)+x*y
    return {k: x for k, x in out.items() if x}


def power(a, n):
    out = ONE
    for _ in range(n):
        out = times(out, a)
    return out


def vplus(a, b):
    return [plus(x, y) for x, y in zip(a, b)]


def vscale(a, p):
    return [times(x, p) for x in a]


def dot(a, b):
    diagonal, sa, sb = {}, {}, {}
    for x, y in zip(a, b):
        diagonal = plus(diagonal, times(x, y))
        sa, sb = plus(sa, x), plus(sb, y)
    return plus(times({(0, 0): 2, (1, 0): -2}, diagonal), times(R, times(sa, sb)))


def exterior(a, b):
    return [plus(times(a[(i+1)%3], b[(i+2)%3]),
                 minus(times(a[(i+2)%3], b[(i+1)%3]))) for i in range(3)]


def dual(a):
    total = {}
    for x in a:
        total = plus(total, x)
    return [plus(times(MU, x), minus(times(R, total))) for x in a]


def reverse_B(triangles):
    remaining = {tuple(sorted(t)) for t in triangles}
    root = (1, 2, 4)
    require(len(remaining) == 7 and root in remaining, 'entire seven-triangle literal B mask')
    notes = []
    while len(remaining) > 1:
        candidates = []
        for t in sorted(remaining, reverse=True):
            if t == root:
                continue
            neighbors = [s for s in remaining if s != t and len(set(t)&set(s)) == 2]
            if len(neighbors) == 1:
                parent = neighbors[0]
                fresh = next(iter(set(t)-set(parent)))
                if all(fresh not in s for s in remaining if s != t):
                    edge = sorted(set(t)&set(parent))
                    old = next(iter(set(parent)-set(t)))
                    candidates.append((t, fresh, edge, old))
        require(bool(candidates), 'reverse leaf elimination, no unidentified shared vertex')
        t, fresh, edge, old = candidates[0]
        remaining.remove(t)
        notes.append((fresh, edge, old))
    points = {k: [ONE if i == j else {} for i in range(3)] for j, k in enumerate(root)}
    for fresh, edge, old in reversed(notes):
        require(fresh not in points and all(k in points for k in edge+[old]), 'reverse insertion available')
        points[fresh] = vplus(vscale(vplus(points[edge[0]], points[edge[1]]), R),
                             vscale(points[old], {(0, 0): -1}))
    require(len(points) == 9 and all(dot(x, x) == D for x in points.values()), 'all nine B unit polynomial identities')
    for t in triangles:
        for i, j in combinations(t, 2):
            require(dot(points[i], points[j]) == R, 'all required B edges')
    return points


def vector(p):
    require(all(j == 0 for i, j in p), 'univariate result')
    out = [0]*(max((i for i, j in p), default=-1)+1)
    for (i, j), x in p.items():
        out[i] = x
    return out


def poly(vals):
    return {(i, 0): x for i, x in enumerate(vals) if x}


def primitive(a):
    if not a:
        return {}
    require(all(j == 0 for i, j in a), 'single-variable primitive')
    den = lcm(*(F(x).denominator for x in a.values()))
    ns = {k: int(x*den) for k, x in a.items()}
    d = gcd(*ns.values())
    if ns[max(ns)] < 0:
        d = -d
    return {k: x//d for k, x in ns.items()}


def divide(a, b):
    require(bool(b), 'nonzero polynomial divisor')
    a = {k: F(x) for k, x in a.items()}
    b = {k: F(x) for k, x in b.items()}
    q = {}
    db, lb = max(b), b[max(b)]
    while a and max(a) >= db:
        da = max(a)
        shift, scale = da[0]-db[0], a[da]/lb
        q[(shift, 0)] = q.get((shift, 0), 0)+scale
        a = plus(a, {(i+shift, j): -scale*x for (i, j), x in b.items()})
    return q, a


def remove(a, factors):
    a = primitive(a)
    removed = []
    for name, f in factors:
        centered_cover(f)
        n = 0
        while a and max(a) >= max(f):
            q, rem = divide(a, f)
            if rem:
                break
            a, n = primitive(q), n+1
        if n:
            removed.append([name, n])
    return a, removed


def centered_cover(p, low=LO, high=HI, depth=0):
    """Closed centered-Taylor bound, a different sign algorithm."""
    p = vector(p)
    require(bool(p), 'zero polynomial cannot have a strict sign')
    mid, radius = (low+high)/2, (high-low)/2
    degree = len(p)-1
    shifted = [sum(F(p[j])*comb(j, k)*mid**(j-k) for j in range(k, degree+1))
               for k in range(degree+1)]
    error = sum(abs(x)*radius**i for i, x in enumerate(shifted) if i)
    if abs(shifted[0]) > error:
        sign = 1 if shifted[0] > 0 else -1
        return [{'closed_cell': [str(low), str(high)], 'sign': sign,
                 'absolute_center': str(abs(shifted[0])), 'error': str(error)}]
    require(depth < 12, 'closed sign coverage incomplete; no exclusion')
    left = centered_cover(poly(p), low, mid, depth+1)
    right = centered_cover(poly(p), mid, high, depth+1)
    require(all(t['sign'] == left[0]['sign'] for t in left+right), 'changing sign retained')
    return left+right


def first_norm(U, V, S):
    k = max((j for i, j in U), default=0)//2
    a, b = {}, {}
    for (i, j), x in U.items():
        term = times({(i, 0): x}, times(power(V, k-j//2), power(S, j//2)))
        if j % 2:
            b = plus(b, term)
        else:
            a = plus(a, term)
    return plus(times(V, times(a, a)), minus(times(S, times(b, b))))


def trim(a):
    while a and not a[-1]:
        a.pop()
    return a


def modular_rem(a, b):
    a, b = trim([int(x)%PRIME for x in a]), trim([int(x)%PRIME for x in b])
    require(bool(b), 'modular nonzero divisor')
    inv = pow(b[-1], -1, PRIME)
    while len(a) >= len(b):
        shift, scalar = len(a)-len(b), a[-1]*inv % PRIME
        for i, x in enumerate(b):
            a[i+shift] = (a[i+shift]-scalar*x) % PRIME
        trim(a)
    return a


def modular_gcd(a, b):
    a, b = trim(list(a)), trim(list(b))
    while b:
        a, b = b, modular_rem(a, b)
    if not a:
        return []
    inv = pow(a[-1], -1, PRIME)
    return [x*inv % PRIME for x in a]


def check_gcd(equations, candidate):
    require(bool(candidate), 'common gcd nonzero')
    cofactor_gcd = []
    leads = []
    for f in equations:
        q, rem = divide(f, candidate)
        require(not rem, 'candidate divides whole exact norm equation')
        if not q:
            continue
        q = primitive(q)
        values = vector(q)
        require(values[-1] % PRIME != 0, 'modular specialization preserves degree')
        leads.append(values[-1] % PRIME)
        cofactor_gcd = modular_gcd(cofactor_gcd, [x%PRIME for x in values])
    require(cofactor_gcd == [1], 'cofactors coprime over Q by Gauss and degree preservation')
    return {'prime': PRIME, 'cofactor_leading_residues': leads, 'cofactor_modular_gcd': [1]}


def check_Bernstein_identity(stored, coefficients):
    values = [F(x) for x in coefficients]
    degree = len(vector(stored))-1
    require(len(values) == degree+1, 'whole Bernstein coefficient count')
    require(all(x > 0 for x in values) or all(x < 0 for x in values), 'strict Bernstein sign includes both closed endpoints')
    left = {(1, 0): F(1), (0, 0): -LO}
    right = {(0, 0): HI, (1, 0): F(-1)}
    expansion = {}
    for i, value in enumerate(values):
        weight = {(0, 0): value*comb(degree, i)/(HI-LO)**degree}
        expansion = plus(expansion, times(weight, times(power(left, i), power(right, degree-i))))
    require(expansion == stored, 'whole Bernstein basis polynomial identity')


def audit(i, record):
    started = monotonic()
    parent_bytes = Path(__file__).with_name('PARENT.json').read_bytes()
    require(sha256(parent_bytes).hexdigest() == PARENT_SHA, 'whole frozen parent byte binding')
    p = json.loads(parent_bytes)
    row = p['geometric_maps'][i]
    bp = reverse_B(p['all_shapes'][row['shape']])
    counts = {a: [b for x, b in row['cross'] if x == a] for a in (6, 7, 9)}
    anchors = [a for a in counts if len(counts[a]) == 2]
    require(len(anchors) == 1, 'exactly one two-contact leaf in the full row')
    anchor = anchors[0]
    u, v = counts[anchor]
    root = 11 if anchor == 9 else 0
    remotes = [b for a, b in row['cross'] if a == root]
    require(len(remotes) == 1, 'chosen adjacent root has exactly one literal B contact')
    remote = remotes[0]
    third = 11 if anchor == 6 else 5
    for field, value in [('map', i), ('shape', row['shape']), ('anchor', anchor),
                         ('pair', [u, v]), ('root', root), ('remote', remote)]:
        require(record[field] == value, 'complete literal row binding '+field)
    require(record['whole_branches_complete'] and [b['sigma'] for b in record['branches']] == [-1, 1], 'both triangle orientations retained')
    g = dot(bp[u], bp[v])
    L, E = plus(D, g), plus(D, minus(g))
    S = plus(times(D, L), minus(times(TWO, times(R, R))))
    V = times(MU, E)
    for f in (L, E, S, V):
        cells = centered_cover(f)
        require(cells[0]['sign'] == 1, 'first sphere factors strictly positive on entire closed band')
    N0, N1 = vscale(vplus(bp[u], bp[v]), R), dual(exterior(bp[u], bp[v]))
    require(dot(N1, bp[u]) == {} and dot(N1, bp[v]) == {}, 'first normal orthogonal')
    require(dot(N1, N1) == times(V, L), 'first normal exact square')
    Z = {(0, 1): 1}
    N = vplus(N0, vscale(N1, Z))
    h = dot(N, bp[remote])
    ell = plus(times(D, L), h)
    vz = times(MU, plus(times(D, L), minus(h)))
    sz = plus(times(D, ell), minus(times(TWO, times(times(R, R), L))))
    M = [vscale(vplus(N, vscale(bp[remote], L)), R), dual(exterior(N, bp[remote]))]
    T = times(TWO, times(L, ell))
    an = [vscale(N, times(TWO, ell)), [{}, {}, {}]]
    xn = [vscale(x, times(TWO, L)) for x in M]
    unused = [[a, b] for a, b in row['cross'] if a not in (anchor, root)]
    require(len(unused) == 3, 'complete remaining contacts')
    factors = [('r', R), ('D', D), ('1-r', {(0, 0): 1, (1, 0): -1}),
               ('2+r', MU), ('L', L), ('E', E), ('V', V), ('S', S)]
    extra = [('r', R), ('D', D), ('1-r', {(0, 0): 1, (1, 0): -1}),
             ('1+r', {(0, 0): 1, (1, 0): 1}), ('2+r', MU),
             ('2r-1', {(0, 0): -1, (1, 0): 2}), ('1+2r', {(0, 0): 1, (1, 0): 2})]
    results = []
    for branch in record['branches']:
        sigma = branch['sigma']
        y = []
        for w in range(2):
            base = vplus(vscale(N, ell) if w == 0 else [{}, {}, {}], vscale(M[w], L))
            y.append(vplus(vscale(base, R), vscale(dual(exterior(N, M[w])), {(0, 0): sigma})))
        points = {anchor: an, root: xn, third: y}
        missing = next(k for k in (0, 5, 11) if k not in points)
        points[missing] = [vplus(vscale(vplus(xn[w], y[w]), R), vscale(an[w], {(0, 0): -1})) for w in range(2)]
        for leaf, x, y, opposite in ((6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0)):
            if leaf not in points:
                points[leaf] = [vplus(vscale(vplus(points[x][w], points[y][w]), R),
                                     vscale(points[opposite][w], {(0, 0): -1})) for w in range(2)]
        require([e['contact'] for e in branch['equations']] == unused, 'all three full unused contacts retained')
        equations = []
        for (a, b), eq in zip(unused, branch['equations']):
            e0 = plus(dot(points[a][0], bp[b]), minus(times(R, T)))
            e1 = dot(points[a][1], bp[b])
            U = plus(times(vz, times(e0, e0)), minus(times(sz, times(e1, e1))))
            raw = first_norm(U, V, S)
            strings = [str(x) for x in vector(raw)]
            require(len(strings)-1 == eq['raw_degree'] and sha256(canon(strings).encode()).hexdigest() == eq['raw_polynomial_digest'], 'complete original raw polynomial identity')
            final, removed = remove(raw, factors)
            require([str(x) for x in vector(final)] == eq['polynomial'] and removed == eq['removed_factors'], 'complete reduced polynomial and factor multiplicities')
            equations.append(final)
        candidate = poly([int(x) for x in branch['gcd']])
        modular = check_gcd(equations, candidate)
        closed, removed = remove(candidate, extra)
        # Producer strip preserves content sign; candidate leading is positive,
        # whereas its final quotient may have either leading sign.
        stored = poly([int(x) for x in branch['closed_sign_gcd']])
        require(primitive(stored) == closed, 'whole sign polynomial up to a nonzero constant')
        check_Bernstein_identity(stored, branch['whole_closed_Bernstein'])
        cells = centered_cover(closed)
        require(branch['whole_closed_nonzero'], 'producer did not claim a complete closed sign cover')
        results.append({'sigma': sigma, 'modular_gcd_certificate': modular,
                        'centered_Taylor_closed_cover': cells, 'extra_removed_factors': removed})
    out = {'actual_agent': 'six-tammes-1', 'role': 'researcher', 'map': i,
           'status': 'same-author different algorithm corroboration; no independent mathematical review',
           'all_raw_equations_identical': True, 'all_branches_retained': True,
           'whole_closed_nonzero_gcds': True, 'branches': results,
           'wall_seconds': monotonic()-started}
    out.pop('wall_seconds')  # Operational measurements are outside exact mathematical records.
    return out


MASKS=[36,43,44,45,61,62,64,66,67,68,70,71,73,74]
PREVIOUS_SHA='84667b20ec5ff4b77ace9b878dca03bc5ab7d44c4bbed53cc41766b3b22a5022'


def load_certificate(record=None):
    raw=Path(__file__).with_name('PARENT.json').read_bytes()
    require(sha256(raw).hexdigest()==PARENT_SHA,'whole original9972 input')
    parent=json.loads(raw)
    raw=Path(__file__).with_name('PREVIOUS.json').read_bytes()
    require(sha256(raw).hexdigest()==PREVIOUS_SHA,'whole original10093 residual input')
    previous=json.loads(raw)
    require(previous['remaining_closed_maps']==[8]+MASKS and previous['remaining_strict_maps']==MASKS,
            'all previous necessary cases retained')
    require(all(i in parent['strict_improvement_maps'] for i in MASKS),'all parent strict-map memberships')
    if record is None:record=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    expected={'actual_agent':'six-tammes-1','role':'researcher','format':'b7-eight-placement-v1',
        'cosine_closed_band':['7/13','3/5'],'r_closed_band':['7/10','3/4'],
        'excluded_maps':MASKS,'extra_contacts_allowed':True,'formalization':False,
        'independent_mathematical_review':False,'literal_masks_have_15_distinct_unit_vectors':True,
        'noncontact_packing_or_face_premises_required_for_literal_masks':False,
        'original_parent_sha256':PARENT_SHA,'previous_10093_certificate_sha256':PREVIOUS_SHA,
        'physical_corollary':'Under ALL9972/9813/10038/10068/10093 hypotheses and case cover: closed residual[8], strict residual[]. No global optimizer occurrence or unrestricted bound.',
        'remaining_closed_maps':[8],'remaining_strict_maps':[]}
    require(canon({k:v for k,v in record.items() if k!='cases'})==canon(expected),'whole scope and closed-domain metadata')
    require(canon([row['map'] for row in record['cases']])==canon(MASKS),'entire14 cases with no omissions/duplicates')
    return record


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',default=str(Path(__file__).with_name('CERTIFICATE.json')))
    parser.add_argument('--expected',default=str(Path(__file__).with_name('ALTERNATE.json')))
    parser.add_argument('--emit')
    args=parser.parse_args();certificate=load_certificate(json.loads(Path(args.certificate).read_text()))
    result=[audit(row['map'],row) for row in certificate['cases']]
    require(canon(result)==canon(json.loads(Path(args.expected).read_text())), 'all alternate mathematical records')
    if args.emit:Path(args.emit).write_text(canon(result))
    print(canon({'actual_agent':'six-tammes-1','role':'researcher','status':'complete all14 alternate checks',
                'whole_raw_and_reduced_equations_checked':84,'whole_sign_branches':28,
                'closed_Taylor_cells':sum(len(b['centered_Taylor_closed_cover']) for r in result for b in r['branches']),
                'all_whole_alternate_records_equal':True,'independent_mathematical_review':False}).strip())
