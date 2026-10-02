"""Independent free-entry dual audit; all computations are over Q.

No import of an author's constructor, decoder, verifier or fixture.
The polynomial kernel is this reviewer's previously published source.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb
from pathlib import Path
import signal

from algebra import vars, zero


def require(ok, message):
    if not ok:
        raise ValueError(message)


def symbolic():
    n, s, r, V, S, mu = vars(6)
    h = s + n - 1
    q = n * (n - 1) / 2
    G = 2 * s - 2 - 2 * q
    A = n + q * (2 + r) + V
    a2 = n * (n + 1) * (s + n) / 2 - n * (n - 1)**2 - n**2
    a2_bulk = a2 - n - 4 * q - q * (n - 2)**2
    w_sum = n**2 * G / 2 - a2_bulk - n * V + S
    au = n + 4 * q + n * V / 2 + (n - 2) * q * r
    # Kernel defect (a-2u)^T C a, on a completely free B=supported edges.
    defect_constant = s * (a2 - 2 * au) - n * s * (n * s - 2 * A)
    direct_constant = h * (n + q * (4 + r**2) + S)
    direct_constant += mu * (s * (G + 4 * q) - (G + 2 * q)**2)
    eta = n * h + q * (h * (4 + r**2) - s * (2 + 4 * r))
    eta += (n - 1) * S + mu * (4 * s - 4)
    zero(direct_constant - eta + s * (mu * G - w_sum)
         - defect_constant, "universal free-entry constant")
    # Completion of the r quadratic, without a rational-function package.
    zero((h * r**2 - 4 * s * r + 4 * h - 2 * s) * h
         - ((h * r - 2 * s)**2 + (8 * h - 10 * s) * h
            - 4 * (n - 1)**2), "root square completion")
    c = Q(5, 4)
    mu0 = (n / 2 - c)**2
    # Multiply by n to remove the only denominator in the moment bound.
    eta_bound_times_n = n * (n * h + q * (8 * h - 10 * s)
                            + mu0 * (4 * s - 4))
    eta_bound_times_n += (n - 1) * (s + n) * (9 * n - 1) / 4
    remainder = 4 * n**3 - 23 * n**2 / 4 + 11 * n / 2 - 6
    claimed_times_n = -s * (3 * n**2 - 15 * n - 1) / 4 + n * remainder
    zero(eta_bound_times_n - claimed_times_n, "unbounded tail polynomial")
    t = vars(1)[0]
    for raw, claimed in [
        (12 * n**2 - 23 * n - 13, 12 * t**2 + 265 * t + 1439),
        (5 * n**2 - 45 * n - 3, 5 * t**2 + 75 * t + 177),
        (23 * n**2 - 22 * n + 24, 23 * t**2 + 530 * t + 3072),
    ]:
        shifted = raw.sub([12 + t, 0, 0, 0, 0, 0])
        zero(shifted - claimed, "tail positive polynomial")
        require(all(x > 0 for x in claimed.d.values()), "tail sign")
    require(2**11 - 12 > 12 * 12**2, "induction base")
    return {"free_entry_constant": "zero", "root_square_completion": "zero",
            "tail_identity": "zero", "positive_tail_polynomials": 3,
            "induction_base": [2036, 1728]}


def profile(n, c=Q(5, 4)):
    require(type(n) is int and n >= 6, "order domain")
    require(type(c) is Q and 0 < c < 3, "profile domain")
    s = 2**(n-1) - n
    h = 2**(n-1) - 1
    r = Q(2*s, h)
    mu = (Q(n, 2) - c)**2
    v = {a: max(Q(0), c-Q((2*a-n)**2, 4*n)) for a in range(3, n-2)}
    f = {a: Q(a)-v[a] for a in v}
    S = sum((comb(n, a)*x*x for a, x in v.items()), Q(0))
    eta = n*h + comb(n, 2)*(h*(4+r*r)-s*(2+4*r))
    eta += (n-1)*S + mu*(4*s-4)
    return s, h, r, mu, v, f, S, eta


def tests(n, r, v, a):
    if a <= 2:
        return Q(0), Q(a)
    if a == n-2:
        return Q(2), r
    return Q(1), v[a]


def layer_checks(n, c=Q(5, 4)):
    s, h, r, mu, v, f, S, eta = profile(n, c)
    pair_types = proper_types = 0
    for a in range(1, n-1):
        for b in range(a, min(n-a, n-2)+1):
            la, ua = tests(n, r, v, a)
            lb, ub = tests(n, r, v, b)
            direct = 2*(mu*la*lb-ua*ub)
            kernel = 2*a*b-2*(ua*b+ub*a)
            rhs = Q(0)
            if 3 <= a <= n-3 and 3 <= b <= n-3:
                rhs = 2*(mu-f[a]*f[b])
                if a+b < n:
                    require(0 < rhs < 2*mu, "proper coefficient sign")
                    proper_types += 1
            require(direct == rhs+kernel, "free individual edge coefficient")
            pair_types += 1
    deficits = [mu-f[a]*f[n-a] for a in v]
    require(all(x >= 0 for x in deficits), "complement coefficient")
    require(all(f[a] > 0 for a in f), "positive f")
    require(all(f[a+1] > f[a] for a in range(3, n-3)), "strict monotonic f")
    d2 = sum((comb(n,a)*Q((2*a-n)**2,4) for a in range(n+1)),Q(0))
    d4 = sum((comb(n,a)*Q((2*a-n)**4,16) for a in range(n+1)),Q(0))
    require(d2 == 2**n*Q(n,4), "second moment")
    require(d4 == 2**n*Q(3*n*n-2*n,16), "fourth moment")
    rho_max = 1-f[3]**2/mu if n >= 7 else None
    if n >= 11 and c == Q(5,4):
        require(eta < 0, "endpoint/tail sample")
        moment_bound = (s+n)*Q(9*n-1,4*n)
        require(S <= moment_bound, "clipped square bound")
        require(0 < rho_max < 1, "largest proper weight")
        for a in f:
            for b in f:
                if a+b < n:
                    require(1-f[a]*f[b]/mu <= rho_max, "uniform mass coefficient")
    return {"n":n,"c":str(c),"pair_types":pair_types,
            "proper_types":proper_types,"S":str(S),"eta":str(eta),
            "min_complement_multiplier":str(min(deficits)),
            "rho_max":str(rho_max),
            "weighted_floor":str(-eta/(2*h*mu)),
            "positive_mass_floor":str(-eta/(2*h*mu*rho_max)) if rho_max else None}


def literal(n):
    """Literal original affine H, credited complement-family formula8106.

    It is deliberately not a capped control; its empty upper form is negative.
    Also evaluate the free-entry identity on a damaged, nonkernel matrix.
    """
    s,h,r,mu,v,f,S,eta = profile(n)
    full = (1<<n)-1
    masks = [a for a in range(1, full+1) if a.bit_count() <= n-2]
    size = [a.bit_count() for a in masks]
    m = len(masks)
    B = [[Q(0) for _ in masks] for _ in masks]
    for i,a in enumerate(masks):
        for j in range(i+1,m):
            b = masks[j]
            if a & b:
                continue
            if size[i] == size[j] == 1:
                z = Q(s-(2**(n-2)-2))
            elif min(size[i],size[j]) == 1:
                z = Q(1)
            elif a|b == full:
                z = Q(s-1)
            else:
                z = Q(0)
            B[i][j] = B[j][i] = z
    C = [[s*int(i==j)-1+B[i][j] for j in range(m)] for i in range(m)]
    rows = [sum(row) for row in C]
    L = [[Q(1+sum(rows))]+[1-z for z in rows]]
    L += [[1-rows[i]]+[C[i][j]+1 for j in range(m)] for i in range(m)]
    N = m+1
    require(N == 2**n-n-1, "literal vertices")
    orig = [0]+masks
    stars = [[int(a & (1<<k) != 0) for a in orig] for k in range(n)]
    for i,a in enumerate(orig):
        require(sum(L[i]) == N, "actual original row")
        for j,b in enumerate(orig):
            require(L[i][j] == L[j][i], "actual symmetry")
            if a & b:
                require(L[i][j] == s*int(i==j), "actual support")
        for x in stars:
            require(sum(L[i][j]*x[j] for j in range(N)) == s, "individual star")
    ell = [tests(n,r,v,a)[0] for a in size]
    uu = [tests(n,r,v,a)[1] for a in size]
    aa = [Q(a) for a in size]
    def identity(matrix):
        core = [[s*int(i==j)-1+matrix[i][j] for j in range(m)] for i in range(m)]
        def form(x,y):
            return sum((x[i]*sum(core[i][j]*y[j] for j in range(m))
                        for i in range(m)),Q(0))
        direct = N*sum(x*x for x in uu)-sum(uu)**2-form(uu,uu)+mu*form(ell,ell)
        defect = form([aa[i]-2*uu[i] for i in range(m)],aa)
        rhs = eta
        for i,a in enumerate(masks):
            if 3 <= size[i] <= n-3:
                j = masks.index(full^a)
                rhs -= (mu-f[size[i]]*f[n-size[i]])*(s-matrix[i][j])
        proper = Q(0)
        for i,a in enumerate(masks):
            for j in range(i+1,m):
                b = masks[j]
                if not(a&b) and a|b != full and min(size[i],size[j])>=3:
                    proper += (mu-f[size[i]]*f[size[j]])*matrix[i][j]
        rhs += 2*proper
        require(direct == rhs+defect, "literal entire original dual identity")
        return direct,rhs,defect
    clean = identity(B)
    require(clean[2] == 0, "clean cardinality kernel")
    # Perturb a disjoint singleton edge. The omitted kernel defect must matter.
    i,j = masks.index(1),masks.index(2)
    B[i][j] += Q(1,7)
    B[j][i] += Q(1,7)
    damaged = identity(B)
    require(damaged[2] != 0 and damaged[0] != damaged[1], "missing kernel rejected")
    require(L[0][0] > N, "uncapped empty control")
    return {"n":n,"vertices":N,"all_original_positions":N*N,
            "point_star_equations":n*N,"actual_empty_L":str(L[0][0]),
            "upper_empty_energy":str(N-L[0][0]),
            "clean_identity":list(map(str,clean)),
            "damaged_kernel_identity":list(map(str,damaged))}


def trade(n=11,c=Q(5,4)):
    s,h,r,mu,v,f,S,eta = profile(n,c)
    def side(offset):
        base = sum(1<<(offset+i) for i in range(3))
        p,z = 1<<(offset+3),1<<(offset+4)
        return {base|p:1,base|z:1,base:-1,base|p|z:-1}
    x,y = side(0),side(5)
    for z in [x,y]:
        require(sum(z.values()) == 0, "trade row relation")
        for k in range(n):
            require(sum(w for a,w in z.items() if a&(1<<k)) == 0,
                    "trade individual star relation")
    edges = [(a,b,xx*yy) for a,xx in x.items() for b,yy in y.items()]
    require(len(edges)==16 and all(not(a&b) and a|b < (1<<n)-1
                                   and min(a.bit_count(),b.bit_count())>=3
                                   for a,b,w in edges), "trade original support")
    du = sum(w*v[a.bit_count()] for a,w in x.items())
    direct = -2*du*du
    weighted = sum((Q(w,h)*(1-f[a.bit_count()]*f[b.bit_count()]/mu)
                    for a,b,w in edges),Q(0))
    require(du == Q(2,n), "trade curvature")
    require(direct == 2*h*mu*weighted != 0, "noninvariant functional")
    require(direct == Q(-8,n*n), "trade exact change")
    return {"n":n,"c":str(c),"unordered_positions":16,"ordered_positions":32,
            "row_and_all_stars_preserved":True,"Phi_change":str(direct),
            "weighted_M_change":str(weighted),
            "edges":[[a,b,w] for a,b,w in edges]}


def record():
    results = [layer_checks(n) for n in [6,8,10,11,12,16,20,32,64]]
    improved = layer_checks(11,Q(9,8))
    require(improved['eta'] == '-707831/1488', "new endpoint eta")
    require(improved['positive_mass_floor'] == '7786141/441099000', "new endpoint mass")
    original = next(z for z in results if z['n']==11)
    require(Q(improved['positive_mass_floor']) > 39*Q(original['weighted_floor']),
            "endpoint improvement exceeds39")
    return {"agent":"six-reviewer-1","role":"independent mathematical reviewer",
            "method":"free-entry coefficient dual with explicit cardinality-kernel defect",
            "symbolic":symbolic(),"layer_records":results,
            "literal_original_controls":[literal(6),literal(8)],
            "noninvariant_trades":[trade(),trade(c=Q(9,8))],
            "endpoint_refinement":improved}


def main():
    signal.alarm(45)
    p=argparse.ArgumentParser()
    p.add_argument('--check',type=Path)
    args=p.parse_args()
    data=record()
    output=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if args.check:
        expected=args.check.read_text()
        require(expected==output,"entire typed canonical fixture mismatch")
    print(output,end='')


if __name__=='__main__':
    main()
