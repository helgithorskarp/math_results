"""Local primitive-block sharpening of the proved fibre completion budget.

six-covering-3, researcher. N=B*p^2, gcd(B,p)=1, p prime, T=B/rad(B),
b|T, Q=b*p^2 (or Q=b*p, lifted). A Q-periodic weight is constant on
each primitive block t mod T at a fixed z mod p^2. Every other actual
resource has proper B-part. On a primitive block of size rad(B), its
weighted footprint has proper period: a missing prime exponent gives
invariance under B/ell, hence under rad(B)/ell in the block index.
The primitive-period sign lemma applies separately on every block.

If at most one top class among B,Bp,N is active in a block, the other
footprints alone meet that block's demand. Only blocks containing two
or more top classes need a charge. Their exact maximum is at most

K(w) = max_{r,s,t} [2 U_r(t) + c(r,s) w_s(t)],
 U_r(t)=sum_{z=r mod p} w_z(t), c=1 if s=r mod p, and c=2 otherwise.

To see this, compare the block labels of the B and Bp classes. Equal
labels give two times their coset weight, plus one (inside the coset)
or two (outside) copies of the single-fibre weight at the same label.
Different labels give no useful charge except a possible pair in the
single N fibre, at most 2 max_t w_s(t), which the displayed maximum
dominates. Nonnegativity proves K<=J<=2M_bp+2M_Q.

This is a necessary covering-completion budget, not a literal bound
for the union of three classes. No earlier finite exclusion is assumed.
The elementary primitive-period method is classical; no priority claim.
"""
from collections import defaultdict
from itertools import product
from math import gcd, isqrt
from random import Random


def radical(B):
    if type(B) is not int or B<2:
        raise ValueError('B must be at least two')
    n, answer, ell = B, 1, 2
    while ell*ell<=n:
        if n%ell==0:
            answer *= ell
            while n%ell==0:
                n //= ell
        ell += 1
    if n>1:
        answer *= n
    return answer


def is_prime(n):
    return type(n) is int and n>=2 and all(n%d for d in range(2,isqrt(n)+1))


def weight_hypothesis(B,b,p,Q):
    if (type(b) is not int or b<1 or not is_prime(p) or gcd(B,p)!=1
            or (B//radical(B))%b or Q not in (b*p,b*p*p)):
        raise ValueError('Primitive block weight hypothesis fails')


def hypothesis(B,b,p,Q,resources):
    weight_hypothesis(B,b,p,Q)
    N = B*p*p
    if N%Q:
        raise ValueError('Primitive block hypothesis fails')
    if len(resources)!=len(set(resources)) or any(type(n) is not int or n<1 or N%n for n in resources):
        raise ValueError('Invalid actual resources')
    if not {B,B*p,N}<=set(resources):
        raise ValueError('Three top resources required')
    return True


def exact_K(B,b,p,Q,vector):
    if len(vector)!=Q or any(type(w) is not int or w<0 for w in vector):
        raise ValueError('Invalid literal weight')
    weight_hypothesis(B,b,p,Q)
    inverse = pow(b,-1,p*p)
    W = [[vector[(t+b*((s-t)*inverse%(p*p)))%Q] for t in range(b)]
         for s in range(p*p)]
    U = [[sum(W[z][t] for z in range(r,p*p,p)) for t in range(b)]
         for r in range(p)]
    best, witness = -1, None
    for r in range(p):
        for s in range(p*p):
            c = 1 if s%p==r else 2
            for t in range(b):
                value = 2*U[r][t]+c*W[s][t]
                if value>best:
                    best, witness = value, (r,s,t)
    return best, witness


def literal_adjusted(B,b,p,Q,vector,classes):
    """Definition-level progression sum and useful primitive-block mass."""
    N, T = B*p*p, B//radical(B)
    resources = tuple(n for n,a in classes)
    hypothesis(B,b,p,Q,resources)
    if len(vector)!=Q or any(type(w) is not int or w<0 for w in vector):
        raise ValueError('Invalid literal weight')
    if any(type(a) is not int or not 0<=a<n for n,a in classes):
        raise ValueError('Invalid actual phase')
    top = tuple((n,a) for n,a in classes if n%B==0)
    other = tuple((n,a) for n,a in classes if n%B)
    active = defaultdict(int)
    for n,a in top:
        for z in range(a%(n//B),p*p,n//B):
            active[z,a%T] += 1
    other_mass = sum(vector[x%Q] for n,a in other for x in range(a,N,n))
    useful_top = sum(vector[x%Q] for n,a in top for x in range(a,N,n)
                     if active[x%(p*p),a%T]>=2)
    return sum(vector)*(N//Q), other_mass, useful_top


def covers(N,classes):
    return all(any(x%n==a for n,a in classes) for x in range(N))


def exact_J(b,p,Q,vector):
    """Earlier whole-fibre comparison budget, formula stated in proof.md."""
    inverse = pow(b,-1,p*p)
    W = [[vector[(t+b*((z-t)*inverse%(p*p)))%Q] for t in range(b)] for z in range(p*p)]
    U = [[sum(W[z][t] for z in range(r,p*p,p)) for t in range(b)] for r in range(p)]
    A = [max(row) for row in U]
    point = [max(row) for row in W]
    return max(2*A[r]+point[z] if z%p==r else
               A[r]+point[z]+max(a+c for a,c in zip(U[r],W[z]))
               for r in range(p) for z in range(p*p))


def controls():
    out = {'agent':'six-covering-3','role':'researcher'}
    blocks, footprints = 0, 0
    for B in (4,8,9,12,18,24,36):
        R, T = radical(B), B//radical(B)
        primes = tuple(ell for ell in range(2,R+1) if R%ell==0 and is_prime(ell))
        for q in range(T):
            blocks += 1
            for m in range(1,B):
                if B%m:
                    continue
                for a in range(m):
                    values = [int((q+T*j)%m==a) for j in range(R)]
                    if not any(all(values[j]==values[(j+R//ell)%R] for j in range(R))
                               for ell in primes):
                        raise RuntimeError('Proper resource loses proper local period')
                    footprints += 1
    out.update(primitive_blocks=blocks,proper_period_footprints=footprints)
    rng, checked = Random(803), 0
    examples = [(4,2,3,{2:0,3:0,4:1,6:1,12:11}),
                (12,2,5,{2:0,3:0,4:1,6:1,12:11})]
    for B,b,p,original in examples:
        N = B*p*p
        classes = tuple(sorted(original.items()))+tuple(
            (n,1%n) for n in (B,B*p,N) if n not in original)
        if not covers(N,classes):
            raise RuntimeError('Positive cover control invalid')
        for Q in (b*p,b*p*p):
            vectors = ([list(v) for v in product(range(2),repeat=Q)]
                       if Q<=6 else [[rng.randrange(8) for x in range(Q)] for i in range(32)])
            for vector in vectors:
                if not any(vector):
                    continue
                demand, other, useful = literal_adjusted(B,b,p,Q,vector,classes)
                K,witness = exact_K(B,b,p,Q,vector)
                J = exact_J(b,p,Q,vector)
                if useful>K or other+useful<demand or K>J:
                    raise RuntimeError('Genuine-cover budget check fails')
                checked += 1
    out['positive_cover_weight_checks'] = checked
    # Explicit asymmetric vector: old J separates maxima at different t.
    B,b,p,Q = 12,2,5,50
    vector = [0]*Q
    inv = pow(b,-1,25)
    for z in range(0,25,5):
        vector[(0+b*((z-0)*inv%25))%Q] = 2
    vector[(1+b*((1-1)*inv%25))%Q] = 8
    K,witness = exact_K(B,b,p,Q,vector)
    J = exact_J(b,p,Q,vector)
    if not K<J:
        raise RuntimeError('Strict-gain fixture is not strict')
    out['strict_gain_fixture'] = {'B':B,'b':b,'p':p,'Q':Q,'K':K,'J':J,'witness':witness}
    # Exhaust every raw top phase tuple independently of the K maximizer.
    B,b,p,N = 4,2,3,36
    phase_checks = 0
    for Q in (6,18):
        for i in range(3):
            vector = [rng.randrange(5) for x in range(Q)]
            largest = -1
            for a,c,e in product(range(B),range(B*p),range(N)):
                classes = ((B,a),(B*p,c),(N,e))
                demand,other,useful = literal_adjusted(B,b,p,Q,vector,classes)
                if other:
                    raise RuntimeError('Top-only fixture has other mass')
                largest = max(largest,useful)
                phase_checks += 1
            K,witness = exact_K(B,b,p,Q,vector)
            if K!=largest:
                raise RuntimeError('Literal complete top-phase maximum differs')
    out['complete_top_phase_tuples'] = phase_checks
    vector = [1]*6
    classes = ((4,0),(12,1),(36,2))
    union = sum(any(x%n==a for n,a in classes) for x in range(N))
    K,witness = exact_K(B,b,p,6,vector)
    if (union,K)!=(13,8):
        raise RuntimeError('Literal union distinction fixture differs')
    out['literal_union_is_not_completion_budget'] = {'union':union,'K':K}
    rejects = 0
    for args in ((12,2,6,72),(12,0,5,50),(12,12,5,300),(12,2,3,18)):
        try:
            weight_hypothesis(*args)
        except ValueError:
            rejects += 1
        else:
            raise RuntimeError('Invalid block/cofactor input accepted')
    out['necessary_hypothesis_rejections'] = rejects
    return out


if __name__=='__main__':
    from pathlib import Path
    from time import monotonic
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    start=monotonic()
    data=controls()
    # JSON canonicalizes tuple witnesses before comparison.
    data=json.loads(json.dumps(data))
    expected=Path(__file__).with_name('controls_expected.json')
    if args.write:expected.write_text(json.dumps(data,indent=2)+'\n')
    elif data!=json.loads(expected.read_text()):raise RuntimeError('Controls manifest differs')
    print('615 local-period footprints,159 genuine-cover weights and10368 full top-phase tuples passed.')
    print('Strict comparison fixture: K=24<J=28; literal union13 differs from completion budget8.')
    print('Elapsed seconds:',monotonic()-start)
