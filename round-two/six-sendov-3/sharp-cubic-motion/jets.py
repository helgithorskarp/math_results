"""All nine cubic original-root motions, exact finite proof corroboration.

Actual six-sendov-3 / researcher. Same-author arithmetic.py is unchanged
from9671/10006/10036. Reviewed8619/8684 rates and10028 actual open repair
region are ordinary proof premises, not executable imports. No sampling.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from arithmetic import F, N0, N1, NW, na, ns, nm, np, ni, nc, need, canonical, sha256

NV = 3  # V=Im(S)/t^3, B=Im(P2)/t^3, J3=sum(h^3)
ORDER = 3
ZERO = (0,) * NV
F0, F1, FI = (N0, N0), (N1, N0), (N0, N1)


def fa(*xs):
    return na(*(x[0] for x in xs)), na(*(x[1] for x in xs))


def fs(x, q):
    return ns(x[0], q), ns(x[1], q)


def fm(x, y):
    return na(nm(x[0], y[0]), ns(nm(x[1], y[1]), -1)), na(nm(x[0], y[1]), nm(x[1], y[0]))


def fc(x):
    return nc(x[0]), ns(nc(x[1]), -1)


def fr(q):
    return q, N0


def fq(q):
    return ns(N1, F(q)), N0


def fp(x, n):
    out = F1
    for _ in range(n):
        out = fm(out, x)
    return out


def pc(x):
    return {} if x == F0 else {ZERO: x}


def pv(i):
    e = list(ZERO); e[i] = 1
    return {tuple(e): F1}


def pa(*ps):
    out = {}
    for p in ps:
        for e, z in p.items():
            out[e] = fa(out.get(e, F0), z)
    return {e: z for e, z in out.items() if z != F0}


def ps(p, q):
    return {e: fs(z, q) for e, z in p.items() if fs(z, q) != F0}


def pm(p, q):
    out = {}
    for e, z in p.items():
        for d, u in q.items():
            power = tuple(a+b for a, b in zip(e, d))
            out[power] = fa(out.get(power, F0), fm(z, u))
    return {e: z for e, z in out.items() if z != F0}


def pp(p, n):
    out = pc(F1)
    for _ in range(n):
        out = pm(out, p)
    return out


def substitute(p, images):
    out = {}
    for e, z in p.items():
        term = pc(z)
        for i, power in enumerate(e):
            term = pm(term, pp(images.get(i, pv(i)), power))
        out = pa(out, term)
    return out


def sa(*ss):
    out = {}
    for s in ss:
        for k, p in s.items():
            out[k] = pa(out.get(k, {}), p)
    return {k: p for k, p in out.items() if p}


def ss(s, q):
    return {k: ps(p, q) for k, p in s.items() if ps(p, q)}


def sm(s, u):
    out = {}
    for k, p in s.items():
        for j, q in u.items():
            if k+j <= ORDER:
                out[k+j] = pa(out.get(k+j, {}), pm(p, q))
    return {k: p for k, p in out.items() if p}


def sp(s, n):
    out = {0: pc(F1)}
    for _ in range(n):
        out = sm(out, s)
    return out


def zeval(poly, z):
    out = {}
    for coefficient in reversed(poly):
        out = sa(sm(out, z), coefficient)
    return out


def ef(z):
    return [[str(q) for q in side] for side in z]


def ep(p):
    return [[list(e), ef(z)] for e, z in sorted(p.items())]


def es(s):
    return [[k, ep(p)] for k, p in sorted(s.items())]


def build(damage=None):
    c = ns(na(np(NW, 4), np(NW, 5)), F(-1, 2))
    if damage == 'wrong_cosine_embedding':
        c = ns(c, -1)
    c2 = nm(c, c)
    need(na(ns(nm(c2, c), 8), ns(c, -6), ns(N1, -1)) == N0,
         'entire physical cosine polynomial')
    y = ns(ni(na(N1, c)), F(1, 3)); x = na(ns(N1, F(2, 3)), ns(y, -1))
    H, U0 = ns(y, 14), ns(x, -8)
    k = ns(na(N1, ns(c, 2)), F(-7, 18))
    V, B, J = (pv(i) for i in range(NV))
    powers = [{}, {2: pc(fr(U0)), 3: pm(pc(FI), V)},
              {2: pc(fr(ns(H, -1))), 3: pm(pc(FI), B)},
              {3: ps(pm(pc(FI), J), -1)}] + [{} for _ in range(5)]
    # All eight Newton identities, weighted through t^3. Higher moment
    # terms are zero ONLY in this finite jet, as justified in PROOF.md.
    elementary = [{0: pc(F1)}]
    for m in range(1, 9):
        total = sa(*(ss(sm(elementary[m-r], powers[r]), (-1)**(r-1))
                     for r in range(1, m+1)))
        elementary.append(ss(total, F(1, m)))
    derivative = [ss(elementary[8-z], 9*(-1)**(8-z)) for z in range(9)]
    primitive = [{}] + [ss(derivative[z-1], F(1, z)) for z in range(1, 10)]
    anchor = {0: pc(F1), 2: pc(fq(-1))}
    primitive[0] = ss(zeval(primitive, anchor), -1)
    if damage == 'wrong_anchor':
        primitive[0] = sa(primitive[0], {2: pc(F1)})
    # Independently stated generic polynomial jet, complete 10 z-columns.
    direct = [{0: pc(fq(-1)), 2: pc(fr(na(ns(N1, 9), ns(x, -9), ns(y, -9)))),
               3: pa(ps(pm(pc(FI), V), F(9, 8)),
                     ps(pm(pc(FI), B), F(9, 14)), ps(pm(pc(FI), J), F(-1, 2)))}]
    direct += [{} for _ in range(9)]
    direct[9] = {0: pc(F1)}
    direct[8] = {2: pc(fr(ns(x, 9))), 3: ps(pm(pc(FI), V), F(-9, 8))}
    direct[7] = {2: pc(fr(ns(y, 9))), 3: ps(pm(pc(FI), B), F(-9, 14))}
    direct[6] = {3: ps(pm(pc(FI), J), F(1, 2))}
    need(primitive == direct, 'entire Newton and anchored generic cubic jet')
    closure = {0: pm(J, pc(fr(ns(k, F(8, 7))))),
               1: pm(J, pc(fr(ns(k, 2))))}
    if damage == 'wrong_sine_closure':
        closure[0] = pm(J, pc(fr(k)))
    closed = [{order: substitute(p, closure) for order, p in z.items()}
              for z in primitive]
    roots, table = [], []
    for label in range(8 if damage == 'missing_ninth_root' else 9):
        w = np(NW, label); wi = np(w, 8); wi2 = np(w, 7)
        L = na(ns(w, F(-1, 3)), ns(x, -1), ns(nm(y, wi), -1))
        T = na(nm(na(ns(N1, 3), ns(c, 4)), w),
               ns(nm(na(N1, ns(c, 2)), na(N1, wi)), -1), ns(wi2, -1))
        W = (N0, ns(T, F(1, 18)))
        if damage == 'wrong_cubic_harmonic' and label == 7:
            W = fa(W, F1)
        Z = {0: pc(fr(w)), 2: pc(fr(L)), 3: pm(J, pc(W))}
        need(not zeval(closed, Z), 'entire original cubic substitution '+str(label))
        Q = fm(W, W if damage == 'wrong_norm_conjugation' else fc(W))
        need(Q[1] == N0 and nc(Q[0]) == Q[0], 'whole real cubic norm '+str(label))
        # Explicit full normal forms, including zero and paired labels.
        forms = [(0,0,0), (F(13,324),F(13,162),F(4,81)),
                 (F(4,81),F(25,162),F(10,81)), (F(1,36),F(1,9),F(1,9)),
                 (F(4,81),F(8,81),F(4,81))]
        form = tuple(F(a) for a in forms[min(label, 9-label)])
        target = na(ns(N1, form[0]), ns(c, form[1]), ns(c2, form[2]))
        need(Q == fr(target), 'entire nine-label squared coefficient table '+str(label))
        roots.append(Z)
        table.append({'label': label, 'omega': ef(fr(w)), 'L': ef(fr(L)), 'W': ef(W),
                      'squared_norm': ef(Q), 'real_cubic_normal_form': [str(a) for a in form]})
    need([r['label'] for r in table] == list(range(9)), 'all nine original labels')
    Qmax = na(ns(N1,F(4,81)),ns(c,F(25,162)),ns(c2,F(10,81)))
    if damage == 'cube_is_maximum':
        Qmax = na(ns(N1,F(1,36)),ns(c,F(1,9)),ns(c2,F(1,9)))
    gaps = []
    for row in table:
        gap = na(Qmax, ns(tuple(F(q) for q in row['squared_norm'][0]), -1))
        # Every gap has a nonnegative-coefficient polynomial in c>0.
        e = 4*gap[1]; b = -2*gap[4]; a = gap[0]-e/2
        need(gap == na(ns(N1,a),ns(c,b),ns(c2,e)), 'whole gap conversion')
        need(a >= 0 and b >= 0 and e >= 0, 'all coefficient gap signs '+str(row['label']))
        need((gap == N0) == (row['label'] in (2,7)), 'only labels2/7 maximize')
        gaps.append({'label':row['label'],'gap_real_cubic':[str(a),str(b),str(e)],
                     'zero':gap == N0})
    cases = []
    for r in range(1, 7 if damage == 'missing_skewness_case' else 8):
        balance_ratio = F(-r,8-r)
        norm_factor = F(r)+(8-r)*balance_ratio**2
        cubic_factor = F(r)+(8-r)*balance_ratio**3
        ratio = cubic_factor**2/norm_factor**3
        need(ratio == F((8-2*r)**2,8*r*(8-r)), 'whole stationary skewness '+str(r))
        need(ratio <= F(9,14), 'stationary sharp skewness bound')
        cases.append({'count':r,'complement':8-r,'squared_skewness':str(ratio),
                      'gap':str(F(9,14)-ratio)})
    need([r['count'] for r in cases] == list(range(1,8)), 'all seven skewness count cases')
    A2 = ns(nm(np(H,3),Qmax),F(9,14))
    proposed = ns(nm(np(H,3),na(ns(N1,8),ns(c,25),ns(c2,20))),F(1,252))
    if damage == 'wrong_sharp_constant':
        proposed = ns(proposed,F(14,9))
    need(A2 == proposed, 'entire universal sharp constant squared')
    rho = ns(na(c,ns(N1,-5)),F(1,3)); ell = na(k,rho)
    alpha = na(ns(N1,F(-527,360)),ns(c,F(41,90)),ns(c2,F(13,90)))
    tau = ns(nm(ell,ell),F(1,2))
    Bstar = na(ns(N1,F(2311,108)),ns(c,F(4934,27)),ns(c2,F(-1976,9)))
    K1 = na(Bstar,ns(nm(alpha,nm(H,H)),F(-1,2)))
    KE = na(K1,nm(nm(H,H),na(ns(alpha,F(43,56)),ns(tau,F(9,14)))))
    Kinf = na(ns(N1,F(6653,324)),ns(c,F(23915,486)),ns(c2,F(-15839,243)))
    if damage == 'wrong_repair_infimum':
        Kinf = na(Kinf,N1)
    need(KE == Kinf, 'whole reviewed open-repair infimum equals1+7 least profile cost')
    lam = ns(na(N1,c),12)
    need(nm(H,lam) == ns(N1,56), 'whole actual repair normalization')
    need(ns(np(H,3),F(9,14)) == nm(ns(N1,336**2),ni(np(lam,3))),
         'whole actual repair profile saturates sharp skewness')
    # Physical embedding isolation, exact rational signs only.
    lo,hi=F(15,16),F(47,50)
    cubic=lambda t:8*t**3-6*t-1
    need(cubic(lo)<0<cubic(hi) and 24*lo*lo-6>0,'physical root isolation')
    for _ in range(24):
        mid=(lo+hi)/2
        if cubic(mid)<0:lo=mid
        else:hi=mid
    def bounds(z):
        e=4*z[1];b=-2*z[4];a=z[0]-e/2
        need(z==na(ns(N1,a),ns(c,b),ns(c2,e)),'whole physical normal form')
        return a+min(b*lo,b*hi)+min(e*lo*lo,e*hi*hi),a+max(b*lo,b*hi)+max(e*lo*lo,e*hi*hi)
    kel,keu=bounds(KE);need(kel>9 and keu<10,'physical9<K_E<10')
    return {'agent':'six-sendov-3','role':'researcher','variables':['V','B','J3'],
            'order':ORDER,'arithmetic':'rational Gaussian ninth-cyclotomic, unchanged same-author kernel',
            'whole_generic_primitive':[es(z) for z in primitive],
            'whole_closed_primitive':[es(z) for z in closed],
            'all_nine_closed_root_jets':[es(z) for z in roots], 'all_nine_harmonics':table,
            'all_nine_maximum_gaps':gaps,'all_seven_skewness_cases':cases,
            'sharp_constant_squared':ef(fr(A2)), 'least_extreme_profile_cost':ef(fr(KE)),
            'actual_repair_normalization':{'H':ef(fr(H)),'lambda':ef(fr(lam)),
                                          'J3_numerator':'336','J3_squared_normalized':'9/14'},
            'physical_cosine_bracket':[str(lo),str(hi)],
            'extreme_cost_bounds':[str(kel),str(keu)],
            'ordinary_analytic_bridges_unformalized':True,'independent_review':False}


def compare_baseline(path, record):
    raw=Path(path).read_bytes()
    need(sha256(raw).hexdigest()=='09fce50546b5836a6c11b959f9e762c1594bb981e12141a9a9aa29dd7b871d20',
         'entire prior10036 fixture source pin')
    import json
    baseline=json.loads(raw)
    need(len(baseline['all_nine_closed_root_jets'])==9,'prior all-nine baseline coverage')
    compared=[]
    for label,old in enumerate(baseline['all_nine_closed_root_jets']):
        cubic=next((p for order,p in old if order==3),[])
        W=record['all_nine_harmonics'][label]['W']
        expected=[] if all(F(q)==0 for side in W for q in side) else [[[1,0,0,0,0,0,0],W]]
        need(cubic==expected,'entire prior10036 cubic baseline '+str(label))
        compared.append({'label':label,'entire_cubic_map_equal':True})
    return {'prior_source_commit':'8890cc2f467f71934ea3b816e7c6bc6670893885',
            'prior_record_sha256':'3b32c4caf3d8e70a7f0564c6dcdb0c0031fef4638baab48b9bee351a3bce8087',
            'fixture_bytes':len(raw),'comparison_scope':'ALL nine cubic maps only; not the whole older theorem',
            'same_author_not_independent':True,'all_nine':compared}
