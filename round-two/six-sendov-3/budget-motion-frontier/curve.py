"""Exact moment/cost identities, same-author corroboration, standard library.

The ordinary compactness, constraint-manifold and actual-family arguments
are in PROOF.md. These finite maps do not formalize those arguments.
"""
from pathlib import Path
import json
from arithmetic import (F, N0, N1, NW, na, ns, nm, np, ni, nc, need,
                        constant, variable, add, scale, multiply, power,
                        derivative, substitute, encoded, identity, margin,
                        canonical, sha256)


def ef(x):
    return [str(q) for q in x]


def cf(a, b=0, d=0, c=None):
    return na(ns(N1, F(a)), ns(c, F(b)), ns(np(c, 2), F(d)))


def real_form(x, c):
    d=4*x[1]; b=-2*x[4]; a=x[0]-d/2
    need(x==cf(a,b,d,c),'whole real cubic normal form')
    return [str(a),str(b),str(d)]


def plus(*ps):
    n=max((len(p) for p in ps),default=0)
    return [na(*(p[j] if j<len(p) else N0 for p in ps)) for j in range(n)]


def times(p,q):
    out=[N0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]=na(out[i+j],nm(a,b))
    return out


def scaled(p,a):
    return [nm(x,a) for x in p]


def value(p,z):
    out=N0
    for a in reversed(p):out=na(nm(out,ns(N1,F(z))),a)
    return out


def pd(p):
    return [ns(p[j],j) for j in range(1,len(p))]


def equality(rows,name,lhs,rhs):
    n=max(len(lhs),len(rhs));left=lhs+[N0]*(n-len(lhs));right=rhs+[N0]*(n-len(rhs))
    need(left==right,'entire field polynomial '+name)
    rows.append({'name':name,'all_coefficients':[ef(a) for a in left],
                 'nonzero_residual_coefficients':0})


def build(damage=None):
    rows=[];field_rows=[];bounds=[]
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2))
    if damage=='wrong_cosine_embedding':c=ns(c,-1)
    need(na(ns(np(c,3),8),ns(c,-6),ns(N1,-1))==N0,'physical cosine cubic')
    need(c[4]==F(-1,2) and c[5]==F(-1,2),'physical large cosine embedding')
    lo=F(15,16);hi=F(47,50)
    f=lambda q:8*q**3-6*q-1
    margin(bounds,'cosine bracket left',-f(lo));margin(bounds,'cosine bracket right',f(hi))
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1));H=ns(y,14)
    U0=ns(x,-8);C=na(ns(N1,F(8,3)),y)
    k=ns(na(N1,ns(c,2)),F(-7,18));rho=ns(na(c,ns(N1,-5)),F(1,3))
    alpha=cf(F(-527,360),F(41,90),F(13,90),c)
    tau=ns(np(na(k,rho),2),F(1,2))
    need(tau==cf(F(1369,648),F(74,81),F(8,81),c),'derived whole tau')
    Bstar=cf(F(2311,108),F(4934,27),F(-1976,9),c)
    K1=na(Bstar,ns(nm(alpha,np(H,2)),F(-1,2)))
    KE=cf(F(6653,324),F(23915,486),F(-15839,243),c)
    kappa=na(tau,ns(alpha,F(10,27)))
    need(kappa==cf(F(3053,1944),F(263,243),F(37,243),c),'whole near-minimum coefficient')
    positive=na(ns(alpha,30),ns(tau,54))
    need(positive==cf(F(421,6),63,F(29,3),c),'whole positive endpoint derivative factor')
    ap=lambda q:F(-527,360)+F(41,90)*q+F(13,90)*q*q
    tp=lambda q:F(1369,648)+F(74,81)*q+F(8,81)*q*q
    ep=lambda q:F(6653,324)+F(23915,486)*q-F(15839,243)*q*q
    margin(bounds,'alpha greater than minus one',ap(lo),-1)
    margin(bounds,'alpha negative',-ap(hi))
    margin(bounds,'tau greater than three',tp(lo),3)
    margin(bounds,'endpoint polynomial decreasing',2*F(15839,243)*lo-F(23915,486))
    margin(bounds,'K_E lower',ep(hi),9);margin(bounds,'K_E upper',10,ep(lo))

    hh,m,z,a,b=[variable(j) for j in (0,1,3,4,5)]
    rr=add(scale(hh,F(1,2)),scale(power(m,2),-12))
    # Direct expansion of six m's and the pair -3m +/- r. Odd r terms cancel.
    def raw_moment(n):
        out=scale(power(m,n),5 if damage=='wrong_middle_count' else 6)
        from math import comb
        for j in range(0,n+1,2):
            out=add(out,scale(multiply(power(scale(m,-3),n-j),power(rr,j//2)),2*comb(n,j)))
        return out
    identity(rows,'all eight balance',raw_moment(1),constant(0))
    identity(rows,'all eight norm',raw_moment(2),hh)
    cubic=add(scale(power(m,3),168),scale(multiply(hh,m),-8 if damage=='wrong_candidate_cubic' else -9))
    quartic=add(scale(power(hh,2),F(1,2)),scale(multiply(hh,power(m,2)),30),
                scale(power(m,4),-839 if damage=='wrong_candidate_quartic' else -840))
    identity(rows,'whole candidate cubic',raw_moment(3),cubic)
    identity(rows,'whole candidate quartic',raw_moment(4),quartic)
    # Normalization H=1, m^2=z, done coefficient by coefficient, no square-root rounding.
    def even_normalized(p):
        out={}
        for ex,q in p.items():
            need(ex[1]%2==0 and not any(ex[j] for j in range(2,len(ex))),
                 'homogeneous even normalization')
            out=add(out,scale(power(z,ex[1]//2),q))
        return out
    g2=even_normalized(power(cubic,2));v4=even_normalized(quartic)
    direct_g2=multiply(z,power(add(constant(9),scale(z,-168)),2))
    identity(rows,'whole normalized cubic squared',g2,direct_g2)
    identity(rows,'whole normalized quartic',v4,add(constant(F(1,2)),scale(z,30),scale(power(z,2),-840)))
    identity(rows,'cubic level strictly increasing factor',derivative(g2,3),
             scale(multiply(add(constant(1),scale(z,-56)),add(constant(1),scale(z,F(-56,3)))),81))
    pearson=add(v4,scale(g2,-1),constant(F(-1,8)))
    factor=multiply(power(add(constant(1),scale(z,-56)),2),add(constant(F(3,8)),scale(z,9 if damage=='wrong_pearson_factor' else -9)))
    identity(rows,'whole singular two-value Pearson defect',pearson,factor)
    upper=add(constant(F(1,2)),scale(g2,F(5,12)),scale(v4,-1))
    identity(rows,'whole classical upper-bound improvement',upper,
             scale(multiply(z,power(add(constant(1),scale(z,-56)),2)),F(15,4)))
    # Constraint Jacobian at the three ordered values -a,0,b; exact determinant.
    columns=[[constant(1),scale(v,2),scale(power(v,2),3)] for v in (scale(a,-1),constant(0),b)]
    from itertools import permutations
    det=constant(0)
    for perm in permutations(range(3)):
        inversions=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        term=constant((-1)**inversions)
        for j in range(3):term=multiply(term,columns[j][perm[j]])
        det=add(det,term)
    identity(rows,'whole rank-three constraint minor',det,scale(multiply(multiply(a,b),add(a,b)),6))
    u=variable(6)
    lagrange_cubic=scale(multiply(multiply(add(u,a),u),add(u,scale(b,-1))),4)
    lagrange_hessian=derivative(lagrange_cubic,6)
    outer_sign=-1 if damage=='wrong_outer_hessian_sign' else 1
    identity(rows,'repeated lower value Hessian direction',
             scale(substitute(lagrange_hessian,6,scale(a,-1)),2),
             scale(multiply(a,add(a,b)),8*outer_sign))
    identity(rows,'repeated upper value Hessian direction',
             scale(substitute(lagrange_hessian,6,b),2),
             scale(multiply(b,add(a,b)),8))
    counts=[{'ordered_multiplicities':[i,j,8-i-j],'outer_repeat_excluded':i>1 or 8-i-j>1}
            for i in range(1,7) for j in range(1,8-i)]
    if damage=='missing_count_case':counts.pop()
    need(len(counts)==21,'all ordered three-value multiplicities')
    need([r['ordered_multiplicities'] for r in counts if not r['outer_repeat_excluded']]==[[1,6,1]],'only six middle multiplicities remain')
    two=[]
    expected=[F(9,14),F(1,6),F(1,30),F(0),F(1,30),F(1,6),F(9,14)]
    for n in range(1,8):
        norm=n*(8-n)**2+(8-n)*n*n
        third=n*(8-n)**3-(8-n)*n**3
        fourth=n*(8-n)**4+(8-n)*n**4
        need(n*(8-n)+(8-n)*(-n)==0,'direct two-value balance')
        skew=F(third*third,norm**3);four=F(fourth,norm**2)
        need(skew==expected[n-1] and four==F(1,8)+skew,'entire two-value moments')
        two.append({'first_count':n,'second_count':8-n,'cubic_squared_over_H_cubed':str(skew),
                    'quartic_over_H_squared':str(four),'pearson_equality':True})
    endpoint=F(1,56)
    identity(rows,'endpoint maximum cubic squared',substitute(g2,3,constant(endpoint)),constant(F(9,14)))
    identity(rows,'endpoint quartic',substitute(v4,3,constant(endpoint)),constant(F(43,56)))
    A=na(ns(alpha,30),ns(tau,81));B=na(ns(alpha,-840),ns(tau,-3024));DD=ns(tau,28224)
    P=[N0,A,B,DD]
    q4=[ns(N1,F(1,2)),ns(N1,30),ns(N1,-840)]
    s2=[N0,ns(N1,81),ns(N1,-3024),ns(N1,28224)]
    cost=plus([K1],scaled(q4,nm(alpha,np(H,2))),scaled(s2,nm(tau,np(H,2))))
    equality(field_rows,'whole candidate least-profile cost',cost,plus([Bstar],scaled(P,np(H,2))))
    factor2=[A,ns(tau,-1511 if damage=='wrong_cost_monotonicity' else -1512)]
    equality(field_rows,'entire monotone cost derivative',pd(P),times([N1,ns(N1,-56)],factor2))
    equality(field_rows,'endpoint cost', [na(Bstar,nm(np(H,2),value(P,endpoint)))],
             [na(KE,N1) if damage=='wrong_cost_endpoint' else KE])
    gap=plus([value(P,endpoint)],scaled(P,ns(N1,-1)))
    equality(field_rows,'whole endpoint quadratic cost gap',gap,
             times(times([ns(N1,endpoint),ns(N1,-1)],[ns(N1,endpoint),ns(N1,-1)]),
                   [na(ns(alpha,840),ns(tau,2016)),ns(tau,-28224)]))
    equality(field_rows,'near-minimum derivative', [A], [ns(kappa,81)])
    profile_cost=[[[0,0,0,0,0,0,0],[ef(K1),ef(N0)]],
                  [[0,1,0,0,0,0,0],[ef(alpha),ef(N0)]],
                  [[2,0,0,0,0,0,0],[ef(nm(tau,ni(H))),ef(N0)]]]
    harmonics=[]
    expected_forms=[(0,0,0),(F(13,324),F(13,162),F(4,81)),
                    (F(4,81),F(25,162),F(10,81)),(F(1,36),F(1,9),F(1,9)),
                    (F(4,81),F(8,81),F(4,81))]
    for j in range(8 if damage=='missing_ninth_harmonic' else 9):
        w=np(NW,j);wi=np(w,8)
        T=na(nm(na(ns(N1,3),ns(c,4)),w),
             ns(nm(na(N1,ns(c,2)),na(N1,wi)),-1),ns(np(wi,2),-1))
        WW=ns(T,F(1,18));norm=nm(WW,nc(WW))
        need(norm==cf(*expected_forms[min(j,9-j)],c),'complete prior harmonic norm '+str(j))
        harmonics.append({'label':j,'W':[ef(N0),ef(WW)],'squared_norm':[ef(norm),ef(N0)],
                          'real_cubic_normal_form':real_form(norm,c)})
    need(len(harmonics)==9,'all nine harmonics')
    q2=cf(F(4,81),F(25,162),F(10,81),c)
    return {'agent':'six-sendov-3','role':'researcher','schema':1,
            'arithmetic':'exact rational and ninth-cyclotomic; standard library; same author',
            'constants':{name:ef(v) for name,v in [('c',c),('y',y),('x',x),('H',H),('U0',U0),('C',C),
                ('alpha',alpha),('tau',tau),('Bstar',Bstar),('KE',KE),('kappa',kappa),('endpoint_positive_factor',positive),('q_squared',q2)]},
            'ordinary_analytic_bridges_unformalized':True,'independent_review':False,
            'rational_polynomial_identities':rows,'rational_sign_bounds':bounds,
            'all_ordered_three_value_counts':counts,'all_two_value_cases':two,
            'candidate_cubic_squared':encoded(g2),'candidate_quartic':encoded(v4),
            'cost_curve_coefficients':[ef(v) for v in P],
            'field_polynomial_identities':field_rows,
            'all_nine_harmonics':harmonics,'whole_prior_least_profile_cost':profile_cost,
            'closed_z_interval':['0','1/56'],
            'attainment_gap_lower_bound':{'coefficient':ef(ns(nm(np(H,2),positive),28)),
                'exponent_of_profile_gap':2,'profile_gap':'eta^(1/4)','cost_error':'O(eta) after division by eta^2'}}


def compare_baselines(root,record):
    deps=json.loads((Path(__file__).parent/'dependencies.json').read_text())['files']
    out=[]
    for directory,key in [('sharp-cubic-motion','all_nine_harmonics'),('uniform-leading-profiles','whole_profile_cost')]:
        path=Path(root)/'round-two/six-sendov-3'/directory/'EXPECTED.json'
        row=next(r for r in deps if r['path'].endswith(directory+'/EXPECTED.json'))
        raw=path.read_bytes();need(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],'whole baseline source pin '+directory)
        old=json.loads(raw)
        if directory=='sharp-cubic-motion':
            need(len(old[key])==9,'all baseline nine labels')
            for j,now in enumerate(record[key]):
                need(all(old[key][j][field]==now[field] for field in ('label','W','squared_norm','real_cubic_normal_form')),
                     'every field of baseline harmonic '+str(j))
        else:need(old[key]==record['whole_prior_least_profile_cost'],'entire baseline least-profile cost')
        out.append({'source_commit':row['source_commit'],'path':row['path'],'whole_file_sha256':row['sha256'],
                    'comparison':'all9 complete cubic coefficient/norm maps' if directory=='sharp-cubic-motion' else 'entire least-profile cost polynomial',
                    'same_author_not_independent':True,'prior_theorem_replay':False})
    return out
