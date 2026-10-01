"""Independent D(16,14) exact audit. No author program is imported.

Run with CPython 3.12, SymPy 1.14.0, all numerical threads one.
Characteristic-polynomial coefficient signs replace author PSD elimination.
"""
import hashlib
import json
import math
from pathlib import Path

import sympy as sp

Q = sp.Rational
N, S, M, R = 65519, 32752, 65518, 14
FREE = [(a, b) for a in range(3, 15) for b in range(a, 15) if a+b <= 16]
COMPS = [(a, 16-a) for a in range(3, 9)]
ORDERS = [14, 14, 13, 11, 9, 7, 5, 3, 1]
MULTS = [1, 15, 104, 440, 1260, 2548, 3640, 3432, 1430]
END = Q(1, 22568)


def require(ok, label):
    if not ok:
        raise ValueError(label)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def bc(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


def matrix_values(a):
    return [[str(x) for x in row] for row in a.tolist()]


def complete(values):
    """Solve the original row/moment equations directly over Q (hence R)."""
    require(len(values) == 36, 'free-coordinate count')
    b = {(a, c): Q(0) for a in range(1, 15) for c in range(1, 15)}
    def put(a, c, v):
        b[a, c] = b[c, a] = Q(v)
    for (a, c), v in zip(FREE, values):
        put(a, c, v)
    for a in range(3, 15):
        q = 16-a
        s0 = sum(b[a, k]*bc(q, k) for k in range(3, 15))
        s1 = sum(b[a, k]*bc(q-1, k-1) for k in range(3, 15))
        put(2, a, (q*(S-s1)-(M-S-s0))/bc(q, 2))
        put(1, a, S-s1-(q-1)*b[2, a])
    s0 = sum(b[2, k]*bc(14, k) for k in range(3, 15))
    s1 = sum(b[2, k]*bc(13, k-1) for k in range(3, 15))
    put(2, 2, (14*(S-s1)-(M-S-s0))/bc(14, 2))
    put(1, 2, S-s1-13*b[2, 2])
    put(1, 1, S-14*b[1, 2]-sum(b[1, k]*bc(14, k-1) for k in range(3, 15)))
    return b


def equations(b):
    out = []
    for a in range(1, 15):
        out.append(sum(b[a, c]*bc(16-a, c) for c in range(1, 15))-(M-S))
        out.append(sum(b[a, c]*bc(15-a, c-1) for c in range(1, 15))-S)
    return out


def sector(b, j):
    layers = list(range(max(1, j), min(14, 16-j)+1))
    g = [bc(16-2*j, a-j) for a in layers]
    k = sp.Matrix([[S*int(a==c)-int(j==0)*bc(16, c)
                   +(-1)**j*b[a,c]*bc(16-a-j, c-j)
                   for c in layers] for a in layers])
    u = sp.eye(len(layers))*N-sp.Matrix([[int(j==0)*bc(16,c) for c in layers] for a in layers])-k
    gram = sp.diag(*g)
    require(gram*k == (gram*k).T and gram*u == (gram*u).T, 'metric self-adjointness')
    return layers, gram, k, u


def characteristic(a, g, nullity=None, strict=False):
    """All eigenvalues are real by positive-metric self-adjointness.

    det(zI+A) has nonnegative coefficients iff A has no negative eigenvalue
    in this real-rooted situation. It is positive at every positive z.
    The zero-root multiplicity is the trailing-zero count.
    """
    require(g*a == (g*a).T and all(g[i,i] > 0 for i in range(g.rows)), 'positive metric')
    z = sp.Symbol('z')
    cs = list((-a).charpoly(z).all_coeffs())
    require(cs[0] == 1 and all(c >= 0 for c in cs), 'negative characteristic coefficient')
    zeros = 0
    for c in reversed(cs):
        if c != 0:
            break
        zeros += 1
    require(zeros < len(cs), 'identically zero monic polynomial')
    if nullity is not None:
        require(zeros == nullity, 'kernel multiplicity')
    if strict:
        require(zeros == 0 and all(c > 0 for c in cs), 'strict positivity')
    return {'order':a.rows, 'nullity':zeros, 'positive_coefficients':sum(1 for c in cs if c>0),
            'coefficient_sha256':digest([str(c) for c in cs]),
            'matrix_sha256':digest(matrix_values(a))}, cs


def projection(layers, g, j):
    q = len(layers)
    if j == 0:
        v = sp.Matrix([[1, a] for a in layers])
    elif j == 1:
        v = sp.ones(q, 1)
    else:
        return sp.eye(q)
    return sp.eye(q)-v*(v.T*g*v).inv()*v.T*g


def literal_harmonics():
    """Literal sets and signed paired-point harmonics; no quotient formulas in sums."""
    sets = [(x, x.bit_count()) for x in range(1, 1<<16) if x.bit_count() <= 14]
    require(len(sets) == M, 'literal nonempty set count')
    require(all(sum(bool(x&(1<<i)) for x,a in sets)==S for i in range(16)), 'sixteen literal star sizes')
    require(sum(2<=a<=14 for x,a in sets)==65502, 'complement-closed middle size')
    results = []
    for j in range(9):
        pos = [(1<<(2*i), 1<<(2*i+1)) for i in range(j)]
        nonzero = []
        norms = [0]*17
        for x,a in sets:
            h = 1
            for p,q in pos:
                h *= int(bool(x&p))-int(bool(x&q))
                if not h:
                    break
            if h:
                nonzero.append((x,a,h))
                norms[a] += h*h
        lo,hi = max(1,j), min(14,16-j)
        require(all(norms[a] == (1<<j)*bc(16-2*j,a-j) for a in range(1,15)), 'literal harmonic norm')
        rows = []
        for a in range(lo,hi+1):
            x = sum(p for p,q in pos)
            extra = a-j
            x |= sum(1<<i for i in range(2*j,2*j+extra))
            representatives = [(x,1)]
            if j:
                representatives.append(((x ^ pos[0][0]) | pos[0][1], -1))
                if a >= j+1:
                    # Replace an outside singleton by the other point of first pair.
                    zero = (x ^ (1<<(2*j))) | pos[0][1]
                    representatives.append((zero,0))
                elif 2*j < 16:
                    zero = (x ^ pos[0][0]) | (1<<(2*j))
                    representatives.append((zero,0))
            for representative, h in representatives:
                counts = [0]*17
                for y,b,hy in nonzero:
                    if not representative & y:
                        counts[b] += hy
                require(all(counts[b] == h*((-1)**j)*bc(16-a-j,b-j) for b in range(lo,hi+1)), 'literal disjoint action')
                rows.append([a,h,counts[lo:hi+1]])
        results.append({'degree':j,'norms':norms[1:15],'rows':len(rows),
                        'action_sha256':digest(rows),'nonzero_sets':len(nonzero)})
    return results


def read_inputs(directory):
    directory = Path(directory)
    raw = [(directory/name).read_bytes() for name in ('seed.json','dual.json')]
    shas = [hashlib.sha256(x).hexdigest() for x in raw]
    require(shas == ['401068b8e2d435f9be2837c003e0f3e97849d327494f2d519e122adc646b5144',
                     'e1fd40f386c7c463ceb1474d74ab93e784e8366930c7858c62527d5cb52d79aa'], 'original input byte hashes')
    seed,dual = [json.loads(x) for x in raw]
    require(seed['n']==16 and seed['r']==14 and seed['N']==N and seed['s']==S, 'seed domain')
    require(seed['free_pairs']==[list(p) for p in FREE] and seed['repair_endpoint']==str(END), 'seed coordinates')
    require(dual['n']==16 and dual['r']==14 and dual['comp_pairs']==[list(p) for p in COMPS], 'dual domain')
    return seed,dual,shas


def derive(directory, pilot=False):
    require(sp.__version__ == '1.14.0', 'SymPy version')
    seed,dual,shas = read_inputs(directory)
    # The seed stores canonical rational values, not a numerical proposal.
    values = [Q(x) for x in seed['free_values']]
    require(all(isinstance(x, str) for x in seed['free_values']), 'exact seed rational strings')
    bseed = complete(values)
    require(equations(bseed) == [0]*28, 'seed original equations')
    if pilot:
        layers,g,k,u = sector(bseed,0)
        return characteristic(k,g,2)[0]
    affine = []
    base = complete([0]*36)
    require(equations(base)==[0]*28, 'affine zero original equations')
    for i in range(36):
        v=[Q(0)]*36;v[i]=1
        b=complete(v)
        require(equations(b)==[0]*28, 'affine basis original equations')
        require([b[a,c] for a,c in FREE] == v, 'free coordinates retained')
        affine.append(digest([str(b[a,c]-base[a,c]) for a in range(1,15) for c in range(a,15) if a+c<=16]))
    # 36 independent free coordinates; 27 uniquely solved touching layers1/2.
    require(len(FREE)==36 and sum(1 for a in range(1,15) for c in range(a,15) if a+c<=16)==63, 'affine dimension')
    ys = [sp.Matrix([[Q(x) for x in row] for row in matrix]) for matrix in dual['Y']]
    scales = [[math.isqrt(bc(16-2*j,a-j)) for a in range(1,15)] for j in (0,1)]
    require(scales == dual['scales'], 'dual normalization scales')
    require(sum(y.trace() for y in ys)==1, 'dual trace normalization')
    dual_positive=[]
    for y in ys:
        require(y==y.T, 'dual symmetry')
        certificate,_=characteristic(y-Q(1,1000000)*sp.eye(14), sp.eye(14),0,True)
        dual_positive.append(certificate)
    def pairing(b):
        total=Q(0)
        for j,y in enumerate(ys):
            _,g,_,u=sector(b,j)
            f=sp.diag(*[Q(1,x) for x in scales[j]])
            a=f*g*u*f
            require(a==a.T, 'dual necessity form symmetry')
            total += sum(y[p,q]*a[q,p] for p in range(14) for q in range(14))
        return total
    fv=[Q(S) if p in COMPS else Q(0) for p in FREE]
    restricted=complete(fv)
    constant=pairing(restricted)
    require(constant==Q(dual['dual_constant']) and constant < -Q(1,4), 'negative dual constant')
    coefficients=[]
    for i,p in enumerate(FREE):
        v=fv.copy();v[i]+=1
        coefficients.append(pairing(complete(v))-constant)
    require(all(coefficients[FREE.index(p)]==0 for p in COMPS), 'all six real deficits cancel')
    middle=[(p,c) for p,c in zip(FREE,coefficients) if p not in COMPS]
    l1=sum(abs(c) for p,c in middle)
    require(l1>0 and len(middle)==30, 'full-face nontrivial coupling coefficients')
    require(pairing(bseed)==constant+sum(c*x for c,x in zip(coefficients,values))>=0, 'seed coupling inequality')
    coupling={'constant':str(constant),'coefficients':[[*p,str(c)] for p,c in middle],
              'coefficient_l1':str(l1),'max_original_weight_floor':str(-constant/((N-S)*l1)),
              'seed_pairing':str(pairing(bseed))}
    blocks=[];lower_ratios=[];floors=[];empty_records=[]
    for t in (Q(0),END/2,END):
        b=bseed.copy()
        b[1,1]+=182*t;b[1,2]-=13*t;b[2,1]-=13*t;b[2,2]+=t
        # Trade kills all stars, but may remove centering.
        require(all(sum(b[a,c]*bc(15-a,c-1) for c in range(1,15))==S for a in range(1,15)), 'trade star equations')
        row=[S-M+sum(b[a,c]*bc(16-a,c) for c in range(1,15)) for a in range(1,15)]
        require(row==[1365*t,-91*t]+[0]*12,'original repaired core row sums')
        total=sum(bc(16,a)*row[a-1] for a in range(1,15))
        loop=1+total
        empty=[1-x for x in row]
        require(loop+sum(bc(16,a)*empty[a-1] for a in range(1,15))==N, 'actual empty-row sum')
        require(all(empty[a-1]+M+row[a-1]==N for a in range(1,15)), 'all actual nonempty row sums')
        require(sum(bc(15,a-1)*empty[a-1] for a in range(1,15))==S,'actual empty-star action')
        empty_records.append({'parameter':str(t),'L_empty_loop':str(loop),
                              'M_empty_loop':str((loop-S)/(N-S)),
                              'empty_layer_entries':[str(x) for x in empty],
                              'core_layer_row_sums':[str(x) for x in row]})
        rank=0; rows=[]
        for j in range(9):
            layers,g,k,u=sector(b,j)
            require(len(layers)==ORDERS[j], 'sector order')
            null = (2 if t==0 else 1) if j==0 else (1 if j==1 else 0)
            low,cs=characteristic(k,g,null)
            up,_=characteristic(u-(Q(1,4) if t==0 else Q(1,8))*sp.eye(len(layers)),g,0,True)
            # Verify the stated nullvectors independently of coefficient multiplicity.
            if j==0:
                require(k*sp.Matrix(layers)==sp.zeros(len(layers),1), 'cardinality star nullvector')
                if t==0:require(k*sp.ones(len(layers),1)==sp.zeros(len(layers),1), 'center nullvector')
            if j==1:require(k*sp.ones(len(layers),1)==sp.zeros(len(layers),1), 'point nullvector')
            rank+=(len(layers)-null)*MULTS[j]
            rows.append({'degree':j,'multiplicity':MULTS[j],'lower':low,'upper_floor':up,
                         'lower_form_sha256':digest(matrix_values(g*k)),
                         'upper_form_sha256':digest(matrix_values(g*(u-(Q(1,4) if t==0 else Q(1,8))*sp.eye(len(layers)))))})
            if t==0:
                p=projection(layers,g,j)
                require(p*p==p and g*p==(g*p).T, 'orthogonal projection')
                cert,_=characteristic(k-p,g,null)
                floors.append({'degree':j,**cert})
            if t==END:
                nonzero=cs[:len(cs)-null] if null else cs
                require(len(nonzero)>=2 and nonzero[-1]>0 and nonzero[-2]>0, 'endpoint positive spectrum')
                lower_ratios.append(nonzero[-1]/nonzero[-2])
        require(rank+1==(65502 if t==0 else 65503), 'full lower rank')
        blocks.append({'parameter':str(t),'full_lower_rank':rank+1,'full_upper_rank':65518,'sectors':rows})
    require(sum(a*d for a,d in zip(ORDERS,MULTS))==M, 'sector dimension coverage')
    # Harmonic lift spectrum uses G as the physical Euclidean metric. Product/
    # next coefficient = reciprocal trace of inverse on the positive spectrum.
    bits=max(1,(1/min(lower_ratios)).p.bit_length()-(1/min(lower_ratios)).q.bit_length()+1)
    while Q(1,2**bits)>min(lower_ratios):bits+=1
    lower_floor=Q(1,2**bits)
    require(all(x>=lower_floor for x in lower_ratios) and lower_floor<N, 'explicit endpoint lower coercivity')
    controls=literal_harmonics()
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','sympy':sp.__version__,
            'input_sha256':shas,'affine_equations':28,'affine_rank':27,'free_coordinates':36,
            'affine_basis_sha256':digest(affine),'dual_positive':dual_positive,
            'dual_y_sha256':[digest(matrix_values(y)) for y in ys],
            'dual_constant':str(constant),'complement_coefficients':['0']*6,
            'full_face_coupling':coupling,'blocks':blocks,'seed_projected_floor_one':floors,
            'endpoint_lower_floor':str(lower_floor),'endpoint_lower_floor_power_two':bits,
            'literal_harmonic_controls':controls,'actual_original_empty_rows':empty_records,
            'maximum_intersecting_size':S,
            'maximum_intersecting_families':16,'no_singleton_intersecting_ceiling':32751}
