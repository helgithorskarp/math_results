"""Independent literal original-coordinate compression and projector audit.
No author imports, companion matrices, quotient gradients or root solver.
"""
from fractions import Fraction as Q
import hashlib
import json


def need(test, label):
    if not test:
        raise ValueError(label)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def mat(n, f):
    return [[Q(f(i, j)) for j in range(n)] for i in range(n)]


def add(a, b, k=1):
    return [[x + k*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, k):
    return [[k*x for x in ar] for ar in a]


def mul(a, b):
    return [[sum((x*y for x, y in zip(ar, bc)), Q(0)) for bc in zip(*b)] for ar in a]


def mv(a, v):
    return [sum((x*y for x, y in zip(ar, v)), Q(0)) for ar in a]


def dot(v, w):
    return sum((x*y for x, y in zip(v, w)), Q(0))


def tr(a):
    return sum((a[i][i] for i in range(len(a))), Q(0))


def compression(u):
    n = len(u)
    p = mat(n, lambda i, j: int(i == j)-Q(1, n))
    h = mul(mul(p, mat(n, lambda i, j: u[i] if i == j else 0)), p)
    return p, h


def projector(p, h, nodes, lam, omit_p=False):
    n = len(p)
    result = mat(n, lambda i, j: int(i == j)) if omit_p else p
    for other in nodes:
        if other != lam:
            result = mul(result, scale(add(h, p, -other), 1/(lam-other)))
    return result


def check_projectors(p, h, nodes, projectors):
    n = len(p)
    z = mat(n, lambda i, j: 0)
    total = z
    for lam, pi in zip(nodes, projectors):
        need(pi == list(map(list, zip(*pi))), 'projector symmetry')
        need(mul(pi, pi) == pi, 'projector idempotence')
        need(mul(p, pi) == pi, 'ambient constant removed')
        need(mul(h, pi) == scale(pi, lam), 'literal eigenvalue identity')
        need(tr(pi).denominator == 1 and tr(pi) > 0, 'whole positive integer rank')
        total = add(total, pi)
    need(total == p, 'full e-perp coverage')
    for i, pi in enumerate(projectors):
        for pj in projectors[:i]:
            need(mul(pi, pj) == z, 'whole eigenspace orthogonality')


def cluster_dm(u, v, dh, nodes, ps, j, sign=1):
    lam, pi = nodes[j], ps[j]
    piu = mv(pi, u)
    ans = 2*dot(v, piu)
    for k, (other, pk) in enumerate(zip(nodes, ps)):
        if k != j:
            ans += sign*2*dot(mv(pk, u), mv(dh, piu))/(lam-other)
    return ans


def audit_case(name, u, nodes, v):
    u, nodes, v = list(map(Q, u)), list(map(Q, nodes)), list(map(Q, v))
    n = len(u)
    need(len(v) == n and sum(u) == sum(v) == 0, 'balanced dimensions')
    need(u == sorted(u) and nodes == sorted(set(nodes)), 'ordered inputs')
    p, h = compression(u)
    _, dh = compression(v)
    ps = [projector(p, h, nodes, lam) for lam in nodes]
    check_projectors(p, h, nodes, ps)
    masses = [dot(u, mv(pi, u)) for pi in ps]
    need(all(m >= 0 for m in masses), 'nonnegative full masses')
    energy = dot(u, u)
    fourth = sum(x**4 for x in u)
    eta = sum(m*m for m in masses)
    d = fourth-energy*energy/n
    need(sum(masses) == energy, 'total mass equals centered energy')
    need(sum(lam*lam*m for lam, m in zip(nodes, masses)) == d, 'entire compression second moment')
    dms = [cluster_dm(u, v, dh, nodes, ps, j) for j in range(len(nodes))]
    need(sum(dms) == 2*dot(u, v), 'entire moving mass sum')
    labels = []
    for a, b in zip(u, u[1:]):
        if a == b:
            labels.append([str(a), '0'])
        else:
            inside = [j for j, lam in enumerate(nodes) if a < lam < b]
            need(len(inside) == 1, 'one literal active critical per positive gap')
            j = inside[0]
            labels.append([str(nodes[j]), str(masses[j])])
    need(sum(Q(m)**2 for _, m in labels) == eta, 'labels retain whole eta')
    rows = []
    for j, (lam, pi, mass, dm) in enumerate(zip(nodes, ps, masses, dms)):
        rank = tr(pi)
        vel = None
        if lam in u:
            need(mass == dm == 0, 'original-level full cluster mass vanishes')
            need(rank == u.count(lam)-1, 'original-level entire multiplicity')
        else:
            need(rank == 1, 'active whole projector rank one')
            r = [1/(x-lam) for x in u]
            s = dot(r, r)
            need(sum(r) == 0, 'actual original logarithmic equation')
            need(mass == n*n/s, 'matrix mass versus reciprocal mass')
            omega = [x*x/s for x in r]
            vel = sum(w*x for w, x in zip(omega, v))
            need(vel == tr(mul(pi, dh)), 'actual simple eigenvalue velocity')
            cov = sum(w*x*y for w, x, y in zip(omega, r, v))-sum(w*x for w, x in zip(omega, r))*vel
            need(dm == 2*mass*cov, 'matrix projector derivative versus covariance')
            vr = sum(w*x*x for w, x in zip(omega, r))-sum(w*x for w, x in zip(omega, r))**2
            vv = sum(w*x*x for w, x in zip(omega, v))-vel*vel
            need(cov*cov <= vr*vv, 'exact covariance Cauchy control')
            need(vr <= s/2, 'exact gap-free reciprocal variance control')
            need(vv <= max(abs(x) for x in v)**2, 'exact motion variance control')
            need(dm*dm <= 2*n*n*mass*max(abs(x) for x in v)**2, 'squared mass derivative bound')
        rows.append({'lambda':str(lam), 'rank':int(rank), 'mass':str(mass), 'cluster_mass_derivative':str(dm), 'simple_lambda_derivative':None if vel is None else str(vel), 'full_projector_sha256':digest([[str(x) for x in ar] for ar in pi])})
    if energy == 0:
        need(ps == [p] and masses == [0], 'all-original collision and ambient zero distinction')
    return {'name':name, 'n':n, 'originals':list(map(str,u)), 'motion':list(map(str,v)), 'energy':str(energy), 'D':str(d), 'eta':str(eta), 'eta_derivative':str(2*dot(masses,dms)), 'ordered_labels':labels, 'whole_eigenspaces':rows}


def cases():
    out = []
    for n, k in [(2,1),(3,2),(4,1),(4,2),(5,2),(8,1),(8,3),(8,4),(11,5),(12,6)]:
        a, b = -(n-k), k
        u = [a]*k+[b]*(n-k)
        nodes = sorted(([a] if k > 1 else [])+[a+b]+([b] if n-k > 1 else []))
        v = list(range(n)); v = [Q(x)-Q(n-1,2) for x in v]
        out.append(audit_case('two-level-%s-%s'%(n,k),u,nodes,v))
    out.append(audit_case('four-distinct',[-7,-1,1,7],[-5,0,5],[-3,1,0,2]))
    out.append(audit_case('double-originals',[-7,-7,-1,-1,1,1,7,7],[-7,-5,-1,0,1,5,7],[-4,3,-2,1,0,1,2,-1]))
    out.append(audit_case('all-original-zero',[0]*8,[0],[-7,-5,-3,-1,1,3,5,7]))
    return out


def scalar_record():
    t, k = Q(24531,1000), Q(47,2)
    d0 = (t-16)**2/(56*t*t)
    b02 = Q(1,4)-2/t
    old = (t-k)*d0/162
    new = (t-k)*d0/106
    lim = Q(1,48000)
    margins = {
        'b0_upper_positive_square':Q(33,80)**2-b02,
        'sqrt2_upper_positive_square':Q(99,70)**2-2,
        'L_upper_strict_106':106-(4*k*Q(33,80)+(24+k)*Q(99,70)),
        'new_radius_minus_1_over_48000':new-lim,
        'old_radius_minus_1_over_73000':old-Q(1,73000),
        'small_D_gamma_square_margin':Q(11,100)**2-Q(7,8)*Q(69,5000),
        'sign_count_error_margin':Q(1,16)-Q(138,2209),
        'large_D_branch_margin':Q(69,5000)-Q(1,224),
        'original_L24_square_margin':68**2-2*48**2,
        'original_L23p5_square_margin':68**2-2*Q(95,2)**2,
        'sign_coordinate_square_margin':Q(3,200)-Q(3,25)**2,
        'uniform_magnitude_lower_square':Q(1,8)-Q(7,20)**2}
    need(all(value > 0 for value in margins.values()), 'entire positive rational margin list')
    need(d0 == Q(72777961,33699117816), 'exact variance threshold')
    need(new == Q(75034077791,3572106488496000), 'new exact tube')
    need(new/old == Q(81,53), 'entire radius improvement ratio')
    need(b02 == Q(16531,98124), 'exact coordinate bound at variance floor')
    need(4*k*Q(33,80)+(24+k)*Q(99,70) == Q(29667,280), 'retained coordinate Lipschitz cap')
    return {'T':str(t),'kappa':str(k),'D_floor':str(d0),'b0_squared':str(b02),'L_rational_upper':str(Q(29667,280)),'L_integer_upper':106,'original_radius':str(old),'new_radius':str(new),'radius_improvement':str(new/old),'positive_margins':{name:str(value) for name,value in margins.items()}}


def sharp_polynomial():
    # Independent coefficient expansion of the cleared reciprocal equation;
    # variable exponents are (n,delta,s). No author polynomial is an input.
    def plus(a,b):
        z = dict(a)
        for e,c in b.items(): z[e]=z.get(e,Q(0))+c
        return {e:c for e,c in z.items() if c}
    def times(a,b):
        z = {}
        for e,c in a.items():
            for f,d in b.items():
                g=tuple(x+y for x,y in zip(e,f));z[g]=z.get(g,Q(0))+c*d
        return {e:c for e,c in z.items() if c}
    n={(1,0,0):Q(1)};de={(0,1,0):Q(1)};s={(0,0,1):Q(1)}
    neg=lambda a:{e:-c for e,c in a.items()}
    two={(0,0,0):Q(2)}
    cleared=plus(times(times(two,de),plus(n,neg(de))),times(plus(n,neg(two)),plus(times(s,s),neg(times(de,de)))))
    quadratic=plus(plus(times(n,times(de,de)),neg(times(times(two,n),de))),neg(times(plus(n,neg(two)),times(s,s))))
    need(plus(cleared,quadratic)=={},'general-n whole sharp-family polynomial')
    return {'variables':['n','delta','s'],'cleared_logarithmic_numerator':[[list(e),str(c)] for e,c in sorted(cleared.items())],'sharp_quadratic':[[list(e),str(c)] for e,c in sorted(quadratic.items())],'entire_identity_zero':True}


def symmetric_projection():
    u = list(map(Q,[-8,-4,-3,-2,1,3,5,8]))
    v = [(a-b)/2 for a,b in zip(u,reversed(u))]
    need(sum(u)==sum(v)==0 and v==sorted(v), 'literal balanced ordered projection')
    ainf=max(abs(a+b) for a,b in zip(u,reversed(u)))/2
    need(max(abs(a-b) for a,b in zip(u,v))==ainf,'exact bottleneck projection distance')
    need(dot(v,v)<=dot(u,u),'nonexpansive Euclidean projection')
    need(max(map(abs,v))<=max(map(abs,u)),'nonexpansive coordinate bound')
    need(dot(u,u)==dot(v,v)+dot([a-b for a,b in zip(u,v)],[a-b for a,b in zip(u,v)]),'orthogonal decomposition')
    return {'originals':list(map(str,u)),'projection':list(map(str,v)),'Ainf':str(ainf),'original_energy':str(dot(u,u)),'projection_energy':str(dot(v,v))}


def translation_control():
    u=list(map(Q,[-7,-1,1,7])); nodes=list(map(Q,[-5,0,5])); alpha=Q(9,7)
    p,h=compression(u); shifted=[x+alpha for x in u];p1,h1=compression(shifted)
    need(p1==p and h1==add(h,p,alpha),'literal translation of restricted compression')
    ps=[projector(p,h,nodes,lam) for lam in nodes]
    shifted_nodes=[lam+alpha for lam in nodes]
    ps1=[projector(p,h1,shifted_nodes,lam) for lam in shifted_nodes]
    need(ps1==ps,'entire projectors translation invariant')
    masses=[dot(u,mv(pi,u)) for pi in ps]
    need(masses==[dot(shifted,mv(pi,shifted)) for pi in ps1],'whole projected masses translation invariant')
    difference=list(map(Q,[-3,1,0,2])); mid=(max(difference)+min(difference))/2
    distance=(max(difference)-min(difference))/2
    need(max(abs(x-mid) for x in difference)==distance,'optimal scalar shift distance')
    return {'originals':list(map(str,u)),'translation':str(alpha),'shifted_nodes':list(map(str,shifted_nodes)),'invariant_masses':list(map(str,masses)),'balanced_difference':list(map(str,difference)),'optimal_constant_shift':str(mid),'translation_quotient_distance':str(distance),'balanced_max_distance':str(max(map(abs,difference)))}


def negative_controls():
    rejected=[]
    def reject(name,call):
        try: call()
        except (ValueError,ZeroDivisionError): rejected.append(name); return
        raise ValueError('accepted damaged mathematics: '+name)
    u=list(map(Q,[-7,-1,1,7]));v=list(map(Q,[-3,1,0,2]));nodes=list(map(Q,[-5,0,5]))
    p,h=compression(u);_,dh=compression(v);ps=[projector(p,h,nodes,l) for l in nodes]
    identity=mat(4,lambda i,j:int(i==j))
    damaged=list(ps); damaged[1]=projector(identity,h,nodes,Q(0),True)
    reject('unremoved-ambient-zero',lambda:check_projectors(p,h,nodes,damaged))
    reject('uncompressed-original-diagonal',lambda:check_projectors(p,mat(4,lambda i,j:u[i] if i==j else 0),nodes,ps))
    reject('missing-entire-critical-space',lambda:check_projectors(p,h,nodes[:-1],ps[:-1]))
    j=0;r=[1/(x-nodes[j]) for x in u];s=dot(r,r);mass=dot(u,mv(ps[j],u));om=[x*x/s for x in r];vel=dot(om,v);cov=sum(w*x*y for w,x,y in zip(om,r,v))-dot(om,r)*vel
    reject('linear-instead-of-squared-n-mass',lambda:need(mass==len(u)/s,'damaged mass'))
    reject('wrong-projector-derivative-sign',lambda:need(cluster_dm(u,v,dh,nodes,ps,j,-1)==2*mass*cov,'damaged derivative sign'))
    reject('missing-covariance-factor-two',lambda:need(cluster_dm(u,v,dh,nodes,ps,j)==mass*cov,'damaged covariance factor'))
    reject('reversed-critical-gap-label',lambda:audit_case('bad',u,[-5,0,6],v))
    reject('unbalanced-motion',lambda:audit_case('bad',u,nodes,[0,0,0,1]))
    reject('lost-original-multiplicity',lambda:audit_case('bad',[-1,-1,2],[1],[-1,0,1]))
    reject('zero-eigenspace-as-ambient-I',lambda:check_projectors(*compression([0]*8),[Q(0)],[mat(8,lambda i,j:int(i==j))]))
    reject('false-stronger-tube-denominator',lambda:need(105>Q(29667,280),'invalid integer upper bound'))
    return rejected


def record():
    return {'schema':'six-reviewer-1-mass-continuity-independent-v1','literal_original_matrix_cases':cases(),'sharp_family_entire_polynomial':sharp_polynomial(),'symmetric_projection':symmetric_projection(),'translation_quotient_control':translation_control(),'tube_refinement_exact_margins':scalar_record(),'mathematical_damage_rejections':negative_controls()}


def same(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
