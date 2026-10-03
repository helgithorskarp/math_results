"""Exact two-intersection producer for fourteen literal closed-band masks."""
from pathlib import Path
from math import gcd, lcm
from time import monotonic
import argparse, json, sys

import geometry as C
from poly import clean
F = C.F
ZERO = []
ONE = [F(1)]
TWO_R = [F(2), F(1)]


def zclean(a):
    a = [clean(x) for x in a]
    while a and not a[-1]:
        a.pop()
    return a


def za(a, b):
    return zclean([C.add(a[i] if i < len(a) else [], b[i] if i < len(b) else [])
                   for i in range(max(len(a), len(b)))])


def zn(a):
    return [C.neg(x) for x in a]


def zm(a, b):
    if not a or not b:
        return []
    out = [[] for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = C.add(out[i+j], C.mul(x, y))
    return zclean(out)


def zs(a, p):
    return zclean([C.mul(x, p) for x in a])


def va(a, b):
    return [za(x, y) for x, y in zip(a, b)]


def vs(a, p):
    return [zs(x, p) for x in a]


def vzs(a, z):
    return [zm(x, z) for x in a]


def cross(a, b):
    return [za(zm(a[(i+1)%3], b[(i+2)%3]),
               zn(zm(a[(i+2)%3], b[(i+1)%3]))) for i in range(3)]


def J(a):
    s = []
    for x in a:
        s = za(s, x)
    return [za(zs(x, TWO_R), zn(zs(s, C.R))) for x in a]


def inner(a, b):
    out = []
    for i in range(3):
        for j in range(3):
            out = za(out, zs(zm(a[i], b[j]), C.D if i == j else C.R))
    return out


def primitive(p):
    p = clean(p)
    if not p:
        return []
    den = lcm(*(x.denominator for x in p))
    vals = [int(x*den) for x in p]
    d = gcd(*vals)
    if vals[-1] < 0:
        d = -d
    return [F(x//d) for x in vals]


def first_reduce(a, V, S):
    """V^k*a(z)=p0+p1*z modulo V*z^2=S, retaining both signs."""
    if not a:
        return [], []
    k = (len(a)-1)//2
    vp = [ONE]
    sp = [ONE]
    for _ in range(k):
        vp.append(C.mul(vp[-1], V))
        sp.append(C.mul(sp[-1], S))
    out = [[], []]
    for i, x in enumerate(a):
        out[i%2] = C.add(out[i%2], C.mul(x, C.mul(vp[k-i//2], sp[i//2])))
    return out


def stripped(p, factors):
    p = primitive(p)
    divisions = []
    for name, f in factors:
        C.need(C.sign(f) in (-1, 1), 'recorded factor whole closed nonzero '+name)
        count = 0
        while p and len(p) >= len(f):
            q, rem = C.divide(p, f)
            if rem:
                break
            p = primitive(q)
            count += 1
        if count:
            divisions.append([name, count])
    return p, divisions


def gcd_primitive(a, b):
    a, b = primitive(a), primitive(b)
    while b:
        _, rem = C.divide(a, b)
        a, b = b, primitive(rem)
    return primitive(a)


def case(i, output=None):
    started = monotonic()
    def status(stage, **kw):
        pass  # Operational timings belong to private execution receipts.
    parent = C.parent()
    row = parent['geometric_maps'][i]
    bp = C.reconstruct(parent['all_shapes'][row['shape']])
    anchor = next(a for a in (6, 7, 9) if sum(ax == a for ax, _ in row['cross']) == 2)
    u, v = [b for a, b in row['cross'] if a == anchor]
    root = 11 if anchor == 9 else 0
    remote = next(b for a, b in row['cross'] if a == root)
    third = 11 if anchor == 6 else 5
    g = C.inner(bp[u], bp[v])
    L = C.add(C.D, g)
    E = C.add(C.D, C.neg(g))
    S = C.add(C.mul(C.D, L), C.neg(C.mul([F(2)], C.mul(C.R, C.R))))
    V = C.mul(TWO_R, E)
    C.need(all(C.sign(x) == 1 for x in (L, E, S, V)), 'first anchor full closed positive factors')
    n0 = C.vecscale(C.R, C.vecadd(bp[u], bp[v]))
    n1 = [x[0] if x else [] for x in J(cross([[p] for p in bp[u]], [[p] for p in bp[v]]))]
    C.need(C.inner(n1, n1) == C.mul(V, L), 'first normal square')
    N = [zclean([x, y]) for x, y in zip(n0, n1)]
    e = [[p] if p else [] for p in bp[remote]]
    h = inner(N, e)
    ell = za([C.mul(C.D, L)], h)
    sz = za(zs(ell, C.D), [C.neg(C.mul([F(2)], C.mul(C.mul(C.R, C.R), L)))])
    vz = zs(za([C.mul(C.D, L)], zn(h)), TWO_R)
    M = [vs(va(N, vs(e, L)), C.R), J(cross(N, e))]
    T = zs(ell, C.mul([F(2)], L))
    anchor_num = [vs(vzs(N, ell), [F(2)]), [[], [], []]]
    root_num = [vs(a, C.mul([F(2)], L)) for a in M]
    unused = [[a, b] for a, b in row['cross'] if a not in (anchor, root)]
    C.need(len(unused) == 3, 'all three unused contacts')
    factors = [('r', C.R), ('D', C.D), ('1-r', [F(1), F(-1)]),
               ('2+r', TWO_R), ('L', L), ('E', E), ('V', V), ('S', S)]
    status('first and second intersections', anchor=anchor, pair=[u, v], root=root, remote=remote)
    branches = []
    for sigma in (-1, 1):
        third_num = []
        for w in range(2):
            base = va(vzs(N, ell) if w == 0 else [[], [], []], vs(M[w], L))
            third_num.append(va(vs(base, C.R), vs(J(cross(N, M[w])), [F(sigma)])))
        points = {anchor: anchor_num, root: root_num, third: third_num}
        missing = next(a for a in (0, 5, 11) if a not in points)
        points[missing] = [va(vs(va(root_num[w], third_num[w]), C.R),
                              vs(anchor_num[w], [F(-1)])) for w in range(2)]
        for leaf, x, y, opposite in ((6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0)):
            if leaf not in points:
                points[leaf] = [va(vs(va(points[x][w], points[y][w]), C.R),
                                   vs(points[opposite][w], [F(-1)])) for w in range(2)]
        equations = []
        for a, b in unused:
            bvec = [[p] if p else [] for p in bp[b]]
            A = za(inner(points[a][0], bvec), zn(zs(T, C.R)))
            B = inner(points[a][1], bvec)
            normw = za(zm(vz, zm(A, A)), zn(zm(sz, zm(B, B))))
            q0, q1 = first_reduce(normw, V, S)
            normz = C.add(C.mul(V, C.mul(q0, q0)), C.neg(C.mul(S, C.mul(q1, q1))))
            final, divisions = stripped(normz, factors)
            equations.append({'contact': [a, b], 'polynomial': C.enc(final),
                              'removed_factors': divisions,
                              'raw_degree': len(normz)-1,
                              'raw_polynomial_digest': C.digest(C.enc(normz))})
            status('unused contact norm', sigma=sigma, contact=[a, b],
                   raw_degree=len(normz)-1, reduced_degree=len(final)-1,
                   coefficient_bits=max((x.numerator.bit_length() for x in final), default=0))
        C.need(any(e['polynomial'] for e in equations), 'some necessary equation is nonzero')
        result = None
        for eq in equations:
            pp = [F(x) for x in eq['polynomial']]
            result = pp if result is None else gcd_primitive(result, pp)
        status('common primitive gcd', sigma=sigma, gcd=C.enc(result), degree=len(result)-1)
        closed_gcd = C.strip(result)
        bs = C.bernstein(closed_gcd, C.LO, C.HI)
        branches.append({'sigma': sigma, 'equations': equations, 'gcd': C.enc(result),
                         'closed_sign_gcd': C.enc(closed_gcd),
                         'whole_closed_Bernstein': C.enc(bs),
                         'whole_closed_nonzero': all(x > 0 for x in bs) or all(x < 0 for x in bs)})
        C.need(branches[-1]['whole_closed_nonzero'], 'strict whole closed gcd signs')
    record = {'actual_agent':'six-tammes-1','role':'researcher',
              'status':'author-checked exact necessary-equation record; independent review pending',
              'map':i,'shape':row['shape'],'anchor':anchor,'pair':[u,v],
              'root':root,'remote':remote,'branches':branches,'whole_branches_complete':len(branches)==2}
    C.need(record['whole_branches_complete'], 'every orientation complete')
    if output is not None:
        Path(output).parent.mkdir(parents=True,exist_ok=True)
        Path(output).write_text(C.canonical(record))
    return record

MASKS=[36,43,44,45,61,62,64,66,67,68,70,71,73,74]
PREVIOUS_SHA='84667b20ec5ff4b77ace9b878dca03bc5ab7d44c4bbed53cc41766b3b22a5022'


def load_certificate(record=None):
    p=C.parent();raw=Path(__file__).with_name('PREVIOUS.json').read_bytes()
    C.need(C.sha256(raw).hexdigest()==PREVIOUS_SHA, 'entire immutable10093 residual')
    previous=json.loads(raw)
    C.need(previous['remaining_strict_maps']==MASKS and previous['remaining_closed_maps']==[8]+MASKS,
           'whole previous15closed14strict input cover')
    C.need(all(i in p['strict_improvement_maps'] for i in MASKS), 'whole parent list membership')
    if record is None:record=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    expected={'actual_agent':'six-tammes-1','role':'researcher','format':'b7-eight-placement-v1',
        'cosine_closed_band':['7/13','3/5'],'r_closed_band':['7/10','3/4'],
        'excluded_maps':MASKS,'extra_contacts_allowed':True,'formalization':False,
        'independent_mathematical_review':False,'literal_masks_have_15_distinct_unit_vectors':True,
        'noncontact_packing_or_face_premises_required_for_literal_masks':False,
        'original_parent_sha256':C.PARENT_SHA,'previous_10093_certificate_sha256':PREVIOUS_SHA,
        'physical_corollary':'Under ALL9972/9813/10038/10068/10093 hypotheses and case cover: closed residual[8], strict residual[]. No global optimizer occurrence or unrestricted bound.',
        'remaining_closed_maps':[8],'remaining_strict_maps':[]}
    C.need(C.canonical({k:v for k,v in record.items() if k!='cases'})==C.canonical(expected),'entire typed scope/closed endpoints/physical corollary')
    C.need(C.canonical([row['map'] for row in record['cases']])==C.canonical(MASKS), 'every whole case, ordered exactly once')
    return record


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--maps',type=int,nargs='+',required=True,
                        help='One documented complete batch; union of all three batches is all14 masks.')
    parser.add_argument('--certificate',default=str(Path(__file__).with_name('CERTIFICATE.json')))
    parser.add_argument('--emit-dir')
    args=parser.parse_args();certificate=load_certificate(json.loads(Path(args.certificate).read_text()))
    C.need(len(args.maps)==len(set(args.maps)) and all(i in MASKS for i in args.maps), 'literal nonduplicate batch')
    expected={row['map']:row for row in certificate['cases']}
    for i in args.maps:
        result=case(i)
        C.need(C.canonical(result)==C.canonical(expected[i]),'entire freshly rebuilt case equality')
        if args.emit_dir:
            target=Path(args.emit_dir);target.mkdir(parents=True,exist_ok=True)
            (target/('placement'+str(i)+'.json')).write_text(C.canonical(result))
    print(C.canonical({'actual_agent':'six-tammes-1','role':'researcher','status':'complete stated batch',
                       'maps':args.maps,'all_full_case_records_equal':True,
                       'whole14_requires_all_three_documented_batches':True}).strip())
