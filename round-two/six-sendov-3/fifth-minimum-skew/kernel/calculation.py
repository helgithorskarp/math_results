"""Whole tenth forcing and mixed fifth cost, reconstructed from literal slots.

Six-sendov-3 / researcher; ordinary unformalized author mathematics.
No peer program, expected fixture, private path or sampled parameter is used.
"""
import family as j
from arithmetic import F, need, canonical
from hashlib import sha256
s=j.s
def no_ninth():
    A, B, K = j.closed_parts()
    return s.pa(A, {(9,0):s.gs(s.G1,-1)}), s.pa(B, {(9,0):s.gs(s.G1,-1)}), K

def physical_variances(parts,order):
    A,B,K=parts
    anchor={(0,0):s.G1,(2,0):s.gs(s.G1,-1)}
    da,db=s.pa(anchor,s.ps(A,-1)),s.pa(anchor,s.ps(B,-1))
    conjugate=lambda p:{key:s.gc(z) for key,z in p.items()}
    va=s.pm(da,conjugate(da),order)
    vb=s.pa(s.pm(db,conjugate(db),order),
            {(e+2,k):s.gm(s.gf(s.ns(s.H,F(1,2))),g)
             for (e,k),g in s.pm(K,conjugate(K),order).items() if e+2<=order})
    cross={key:s.real(g) for key,g in s.pm(db,conjugate(K),order).items()}
    x2={(e+2,k):s.gm(s.gf(s.ns(s.H,2)),g)
        for (e,k),g in s.pp(cross,2,order).items() if e+2<=order}
    return va,vb,x2

def direct_first(parts, order, damage=None):
    """Physical all-eight scalar through epsilon11, derived afresh.

    V-1 starts at epsilon2; X^2 starts at epsilon8.  The two split
    distances are V+/-X, so their sum has the positive 3/4 X^2 V^-5/2
    correction.  Fifth inverse-square-root power is now essential.
    """
    need(order in (10,11), 'tenth/eleventh physical scalar truncation domain')
    va,vb,x2=physical_variances(parts,order)
    def inverse_square_root(v):
        h=s.pa(v,{(0,0):s.gs(s.G1,-1)})
        need(not h or min(e for e,k in h)>=2,'whole V minus one valuation')
        fifth=F(0) if damage=='omit_fifth_binomial' else F(-63,256)
        return s.pa({(0,0):s.G1},s.ps(h,F(-1,2)),s.ps(s.pp(h,2,order),F(3,8)),
                    s.ps(s.pp(h,3,order),F(-5,16)),s.ps(s.pp(h,4,order),F(35,128)),
                    s.ps(s.pp(h,5,order),fifth))
    need(not x2 or min(e for e,k in x2)>=8,'whole physical pair X squared valuation')
    h=s.pa(vb,{(0,0):s.gs(s.G1,-1)})
    linear=F(0) if damage=='omit_pair_variance' else F(-5,2)
    correction=s.ps(s.pm(x2,s.pa({(0,0):s.G1},s.ps(h,linear)),order),F(3,4))
    total=s.pa(s.ps(inverse_square_root(va),6),s.ps(inverse_square_root(vb),2),correction)
    need(all(k==0 for e,k in total),'physical scalar has no original variable')
    return [total.get((e,0),s.G0) for e in range(order+1)]

def scalar_recursion(parts,order,ids):
    """Separate positive-branch equations, without binomial coefficients.

    R=(VB^2-X^2)^(-1/2); pair S satisfies
    S^2=2 VB R^2+2R with S(0)=2.  All retained equations checked.
    """
    va,vb,x2=physical_variances(parts,order)
    vec=lambda p:[p.get((e,0),s.G0) for e in range(order+1)]
    va,vb,x2=vec(va),vec(vb),vec(x2)
    target=[s.G1]+[s.G0]*order
    def inverse_sqrt(v,name):
        need(v[0]==s.G1,'physical scalar constant unit variance '+name)
        u=[s.G1]+[s.G0]*order
        for e in range(1,order+1):
            u[e]=s.gs(s.sm(v,s.sm(u,u,e),e)[e],F(-1,2))
        s.eq(ids,'WHOLE positive reciprocal-square-root equation '+name,
             s.sm(v,s.sm(u,u,order),order),target)
        return u
    small=inverse_sqrt(va,'six repeated critical slots')
    determinant=[s.ga(a,s.gs(b,-1)) for a,b in zip(s.sm(vb,vb,order),x2)]
    R=inverse_sqrt(determinant,'split-pair distance product')
    q=[s.gs(s.ga(a,b),2) for a,b in zip(s.sm(vb,s.sm(R,R,order),order),R)]
    pair=[s.gs(s.G1,2)]+[s.G0]*order
    for e in range(1,order+1):
        pair[e]=s.gs(s.ga(q[e],s.gs(s.sm(pair,pair,e)[e],-1)),F(1,4))
    s.eq(ids,'WHOLE positive split-pair sum equation',s.sm(pair,pair,order),q)
    return [s.ga(s.gs(a,6),b) for a,b in zip(small,pair)]

def cubes(parts,order):
    A,B,K=parts
    imag=lambda p:{key:s.real((g[1],s.ns(g[0],-1))) for key,g in p.items()}
    ya,yb,ki=imag(A),imag(B),imag(K)
    variance={(e+2,k):s.gm(s.gf(s.ns(s.H,F(1,2))),g)
              for (e,k),g in s.pp(ki,2,order).items() if e+2<=order}
    total=s.pa(s.ps(s.pp(ya,3,order),6),s.ps(s.pp(yb,3,order),2),s.ps(s.pm(yb,variance,order),6))
    return [total.get((e,0),s.G0) for e in range(order+1)]

def graded(p,roots,first,powers,order):
    need(order<32,'Kronecker base exceeds every t degree')
    rows=[(e,g) for e,row in enumerate(p) for g in row]
    rows += [(e,g) for row in roots for key in ('root','normals') for e,g in enumerate(row[key])]
    rows += list(enumerate(first))
    rows += [(e,g) for power in powers[1:] for (e,k),g in power.items()]
    for e,g in rows:
        for fieldpoly in g:
            for n in fieldpoly:
                need(type(n) is int and n>=0 and n%32<=e<=order,
                     'whole graded t degree bound and injective Kronecker domain')

def cosine_rows():
    rows=[]
    for label in range(9):
        w=s.np(s.WW,label);v=s.np(s.WW,(2*label)%9)
        Aj=s.na(s.N1,s.ns(s.na(w,s.nc(w)),F(-1,2)))
        Bj=s.na(s.N1,s.ns(s.na(v,s.nc(v)),F(-1,2)))
        rows.append((Aj,Bj))
    return rows

AB=cosine_rows()
def rational_interval(coefficients):
    lo,hi=F(15,16),F(47,50)
    cubic=lambda c:8*c**3-6*c-1
    need(cubic(lo)<0<cubic(hi) and 24*lo*lo-6>0,'whole physical cosine root bracket')
    for _ in range(48):
        mid=(lo+hi)/2
        if cubic(mid)<0:lo=mid
        else:hi=mid
    low,high=F(0),F(0)
    for a in reversed(coefficients):
        corners=(low*lo,low*hi,high*lo,high*hi)
        low,high=min(corners)+a,max(corners)+a
    return low,high,lo,hi

def bound_normals(roots):
    records=[];monomial_bounds={}
    for label in (3,4,5,6):
        g=roots[label]['normals'][10]
        need(g[1]==s.N0,'unaveraged actual tenth normal physically real')
        ratio=s.nm(g[0],s.ni(AB[label][0]))
        entries=[]
        for n,coefficient in sorted(ratio.items()):
            cs=list(map(F,s.field_real_form(s.fc,coefficient)))
            low,high,lo,hi=rational_interval(cs)
            bound=max(abs(low),abs(high));integer=-(-bound.numerator//bound.denominator)
            monomial_bounds[n]=max(monomial_bounds.get(n,0),integer)
            entries.append({'mu_power':n//32,'t_power':n%32,'whole_cubic':[str(a) for a in cs],
                            'lower':str(low),'upper':str(high),'integer_absolute_bound':integer})
        records.append({'label':label,'whole_q_over_A':entries})
    # In fact the two new mixed terms have negative physical coefficients
    # separately on every unaveraged row.  Nonnegative means need NO T cost.
    for row in records:
        need({(a['mu_power'],a['t_power']) for a in row['whole_q_over_A']}==
             {(0,0),(1,0),(2,0),(0,2),(1,2)},'entire tenth ratio monomial census')
        for entry in row['whole_q_over_A']:
            if entry['t_power']==2:
                need(F(entry['upper'])<0,'ALL4 new mixed tenth ratio coefficient strictly negative')
    return {'all4_unaveraged_ratio_rows':records,
            'cosine_bracket':[str(lo),str(hi)],
            'explicit_tau_MT':'1 + sum b_uv M^u T^v; for every M,T >= 0',
            'nonnegative_mean_improvement':'tau_M=8+13M+2M^2 for 0<=mu<=M and arbitrary t in each fixed compact set',
            'bound_terms':[{'mu_power':n//32,'t_power':n%32,'b':b}
                           for n,b in sorted(monomial_bounds.items())]}

def documentary_real_baseline(roots,first,ids):
    """Written complete polynomial coefficients of10288, credited validation.

    This published zero-skew derivative is PRIOR ART.  No reviewer program
    or EXPECTED is exposed; fresh current calculations are compared in full.
    """
    triples={
      3:[(F(-7293232089277697,69657034752),F(-5809710683424677,11609505792),F(1889762375330027,2902376448)),
         (F(486091517,279936),F(2310714253,279936),F(-751884343,69984)),(F(53,126),F(31,54),F(170,189))],
      4:[(F(-7549883884071265,17414258688),F(-70772795590721635,34828517376),F(15402534234898513,5804752896)),
         (F(-1068415519,279936),F(-2693216555,139968),F(3472962359,139968)),(F(2953,1134),F(6073,567),F(-6883,567))]}
    for label in (3,4,5,6):
        row=triples[3 if label in (3,6) else 4]
        expected={n:s.fcf(*coeffs) for n,coeffs in enumerate(row)}
        ratio=s.nm(roots[label]['normals'][10][0],s.ni(AB[label][0]))
        s.eq(ids,'WHOLE credited written10288 real ratio '+str(label),
             [j.projection(s.gf(ratio),'t0')],[s.gf(expected)])
    fc=[(F(46162779724939271,69657034752),F(36338752485008003,11609505792),F(-11846579474774765,2902376448)),
        (F(932974693,279936),F(6209560805,279936),F(-1933889279,69984)),(F(-809,54),F(-3545,54),F(166,3))]
    s.eq(ids,'WHOLE credited written10288 real fifth scalar',
         [j.projection(first[10],'t0')],[s.gf({n:s.fcf(*cs) for n,cs in enumerate(fc)})])

def unit_controls(parts,p,roots,first,ids,damage=None):
    changed=s.pa(parts[0],{(10,0):s.G1}),s.pa(parts[1],{(10,0):s.G1}),parts[2]
    if damage=='outward_tenth':
        changed=s.pa(parts[0],{(10,0):s.gs(s.G1,-1)}),s.pa(parts[1],{(10,0):s.gs(s.G1,-1)}),parts[2]
    newp=s.actual_polynomial(*changed,10,2)
    pn,powers=s.newton_polynomial(*changed,10,2)
    s.eq(ids,'WHOLE repaired literal versus all8 Newton primitive',
         [g for row in newp for g in row],[g for row in pn for g in row])
    newroots=s.roots_and_normals(newp,10,ids)
    column=[s.G0]*10;column[0]=s.gs(s.G1,9);column[8]=s.gs(s.G1,-9)
    for e in range(11):
        delta=[s.ga(a,s.gs(b,-1)) for a,b in zip(newp[e],p[e])]
        s.eq(ids,'WHOLE common tenth primitive column '+str(e),delta,column if e==10 else [s.G0]*10)
    for label,(row,newrow) in enumerate(zip(roots,newroots)):
        root_response=s.gf(s.na(s.N1,s.ns(s.np(s.WW,label),-1)))
        for key,target in (('root',root_response),('normals',s.gf(s.ns(AB[label][0],-1)))):
            delta=[s.ga(a,s.gs(b,-1)) for a,b in zip(newrow[key],row[key])]
            s.eq(ids,'ALL9 full tenth '+key+' unit response '+str(label),delta,[s.G0]*10+[target])
    newfirst=direct_first(changed,10)
    s.eq(ids,'WHOLE repaired independent physical scalar',newfirst,scalar_recursion(changed,10,ids))
    s.eq(ids,'WHOLE all8 common tenth objective unit response',
         [s.ga(a,s.gs(b,-1)) for a,b in zip(newfirst,first)],
         [s.G0]*10+[s.gs(s.G1,8)])
    graded(newp,newroots,newfirst,powers,10)
    # Each critical slot moves by epsilon10; l>=2 first interacts above10.
    _,oldpowers=s.newton_polynomial(*parts,10,2)
    for l in range(1,9):
        delta=[s.ga(powers[l].get((e,0),s.G0),s.gs(oldpowers[l].get((e,0),s.G0),-1))
               for e in range(11)]
        s.eq(ids,'ALL8 whole tenth moment unit response '+str(l),delta,
             [s.G0]*10+[s.gs(s.G1,8) if l==1 else s.G0])
    return {'whole_unit_parts':j.encoded_parts(changed),'whole_unit_primitive':[s.encoded_vector(row) for row in newp],
            'whole_unit_all9_originals':s.output_roots(newroots),'whole_unit_first':s.encoded_vector(newfirst),
            'whole_unit_moments':[s.encoded_vector([power.get((e,0),s.G0) for e in range(11)])
                                  for power in powers[1:]]}

def parity_and_endpoint(parts,first,cc,ids):
    # These are whole identities of the literal finite coefficient polynomials.
    # They imply exact conjugation parity, hence an eta-analytic scalar, rather
    # than only a finite claim that one odd Taylor coefficient vanishes.
    for name,p,extra_sign in zip(('A','B','K'),parts,(1,1,-1)):
        for (e,k),g in sorted(p.items()):
            s.eq(ids,'WHOLE literal conjugation parity '+name+'/'+str(e),
                 [s.gs(g,(-1)**e)],[s.gs(s.gc(g),extra_sign)])
            reflected=tuple({n:s.ar.ns(a,(-1)**(n%32)) for n,a in side.items()} for side in g)
            s.eq(ids,'WHOLE literal t reflection '+name+'/'+str(e),
                 [reflected],[s.gs(s.gc(g),extra_sign)])
    extended=direct_first(parts,11)
    s.eq(ids,'WHOLE eleventh independent positive-branch scalar',extended,scalar_recursion(parts,11,ids))
    s.eq(ids,'WHOLE eleventh scalar truncation unchanged',extended[:11],first)
    s.eq(ids,'WHOLE eleventh scalar coefficient zero',[extended[11]],[s.G0])
    U7=s.na(s.ns(s.gamma,2),s.ns(s.nm(s.H,s.k),F(3,7)))
    s.eq(ids,'WHOLE actual leading and third skew coefficients',cc[:8],
         [s.G0]*5+[s.gf(j.t),s.G0,s.gf(s.nm(U7,j.t))])
    P0=j.f(F(134807893,18289152),F(57634811,4064256),F(159762149,18289152))
    P1=j.f(F(241,1764),F(331,882),F(233,882))
    real_fifth=j.projection(first[10],'t0')[0]
    expected=s.na({32*n:v for n,v in real_fifth.items()},
                  s.nm(s.na(P0,s.nm(P1,j.mu)),s.np(j.t,2)))
    s.eq(ids,'WHOLE mixed fifth objective decomposition',[first[10]],[s.gf(expected)])
    def positive(name,p):
        need(set(p)=={0},'constant physical endpoint field '+name)
        cs=list(map(F,s.field_real_form(s.fc,p[0])))
        low,high,lo,hi=rational_interval(cs)
        need(low>0,'strict endpoint physical sign '+name)
        return {'name':name,'whole_cubic':[str(a) for a in cs],'lower':str(low),'upper':str(high)}
    ell2=s.ns(s.nm(s.H,s.nm(j.m.Gmean,s.ni(s.kappa))),-1)
    signs=[positive(name,p) for name,p in (
        ('H',s.H),('kappa',s.kappa),('minus_Gmean',s.ns(j.m.Gmean,-1)),
        ('mu_star_minus8',s.na(j.m.MUstar,s.ns(s.N1,-8))),
        ('16_minus_mu_star',s.na(s.ns(s.N1,16),s.ns(j.m.MUstar,-1))),
        ('ellmean_squared',ell2),('physical_fifth_t2',P0),('physical_fifth_mu_t2',P1))]
    def substitute_even(p):
        value=s.N0
        for n,coefficient in p.items():
            need(n%32%2==0,'central endpoint whole substitution even t')
            term=s.nm(s.const(coefficient),s.nm(s.np(j.m.MUstar,n//32),s.np(ell2,(n%32)//2)))
            value=s.na(value,term)
        return value
    J=s.na(substitute_even(first[10][0]),s.ns(s.N1,5824))
    Lambda=s.na(U7,s.nm(J,s.ni(s.ns(j.m.Gmean,2))))
    # tau16=728 is prior at t=0; the NEW mixed sign control permits it
    # for 0<=mu<=16 on every fixed compact t interval.
    baseline_D=s.na(s.const(s.fcf(F(-1554380464593574777,69657034752),
                       F(-1219260700409103133,11609505792),F(397722967460633563,2902376448))))
    fifth_mean=s.N0
    for n,v in real_fifth.items():fifth_mean=s.na(fifth_mean,s.nm(s.const(v),s.np(j.m.MUstar,n)))
    s.eq(ids,'WHOLE credited10288 central real fifth comparison',
         [s.gf(s.na(fifth_mean,s.ns(s.N1,5824)))],[s.gf(baseline_D)])
    Jinterval=rational_interval(list(map(F,s.field_real_form(s.fc,J[0]))))[:2]
    Linterval=rational_interval(list(map(F,s.field_real_form(s.fc,Lambda[0]))))[:2]
    need(F(7426)<Jinterval[0]<=Jinterval[1]<F(7427),'strict whole rational7426<J16<7427')
    need(F(-14)<Linterval[0]<=Linterval[1]<F(-13),'strict whole rational-14<Lambda16<-13')
    return {'whole_first_epsilon0to11':s.encoded_vector(extended),
            'whole_cubic_P0':s.rpoly(P0),'whole_cubic_P1':s.rpoly(P1),
            'whole_U7':s.rpoly(U7),'whole_ellmean_squared':s.rpoly(ell2),
            'whole_central_J16':s.rpoly(J),'whole_central_lambda_relative_correction':s.rpoly(Lambda),
            'central_J_rational_interval':[str(v) for v in Jinterval],
            'central_lambda_correction_interval':[str(v) for v in Linterval],
            'exact_signs':signs,'attained_central_lambda_expansion':'ellmean*(sqrteta+Lambda16*eta^(3/2)+O(eta^(5/2)))',
            'claim_scope':'actual central equality construction only; no arbitrary-competitor maximum or universal fourth lower/limit'}


def lower_controls(parts,p,roots,first,cc,ids,damage=None):
    """Whole lower coefficients, mixed columns and motion; no fixture input."""
    cost=s.na(j.m.Gstar,s.nm(j.m.L,j.mu),s.ns(s.np(j.mu,2),F(4,3)),
              s.nm(s.nm(s.kappa,s.ni(s.H)),s.np(j.t,2)))
    if damage=='wrong_cost_cross':cost=s.na(cost,s.nm(j.mu,j.t))
    target=[s.G0]*10
    for e,z in ((0,s.ns(s.N1,8)),(2,s.C['C']),(4,s.C['Bstar']),(6,s.Tstar),(8,cost)):
        target[e]=s.gf(z)
    s.eq(ids,'WHOLE coupled mixed lower FIRST epsilon0to9',first[:10],target)
    s.eq(ids,'WHOLE actual cubic lower coefficients',cc[:7],[s.G0]*5+[s.gf(j.t),s.G0])
    j.column_controls(parts,ids)
    signs,ideal,ell,oldell,bracket=j.signs_and_motion(roots,ids,
                            damage='wrong_motion_winner' if damage=='wrong_motion_winner' else None)
    # A displayed coefficient is checked against every unaveraged row.
    triples={3:((F(21588995,28449792),F(86382659,170698752),F(44717485,85349376)),
                 (F(83,8232),F(137,4116),F(109,4116))),
             4:((F(90414379,146313216),F(216408443,256048128),F(65443465,256048128)),
                 (F(391,24696),F(557,24696),F(41,12348)))}
    for label in (3,4,5,6):
        a,b=triples[3 if label in (3,6) else 4]
        q=roots[label]['normals'][10][0]
        expected=s.ns(s.nm(s.na(j.f(*a),s.nm(j.f(*b),j.mu)),s.np(j.t,2)),-1)
        zero={n:v for n,v in q.items() if n%32==0}
        s.eq(ids,'ALL4 displayed complete mixed tenth terms '+str(label),
             [s.gf(s.na(q,s.ns(zero,-1)))],[s.gf(expected)])
    # Exact leading normals individually, including the marked branch.
    n1=s.ns(j.f(2,4,-4),F(-1,3))
    n2=s.ns(s.np(s.na(s.ns(s.c,2),s.ns(s.N1,-1)),2),F(-1,3))
    for label,z in ((0,s.ns(s.N1,-1)),(1,n1),(8,n1),(2,n2),(7,n2)):
        s.eq(ids,'ALL5 written inactive leading normals '+str(label),
             [roots[label]['normals'][2]],[s.gf(z)])
    return signs

def build(stage='unit',damage=None):
    ids=[]
    need(stage in ('forcing','unit'),'defined exact calculation stage')
    parts=no_ninth()
    if damage in ('omit_seventh','omit_ninth_center','omit_ninth_scale'):
        A,B,K=j.closed_parts(damage)
        parts=s.pa(A,{(9,0):s.gs(s.G1,-1)}),s.pa(B,{(9,0):s.gs(s.G1,-1)}),K
    if damage=='keep_ninth':parts=j.closed_parts()
    order=10
    p=s.actual_polynomial(*parts,order,2)
    pn,powers=s.newton_polynomial(*parts,order,2)
    s.eq(ids,'WHOLE tenth literal versus all8 Newton primitive',
         [g for row in p for g in row],[g for row in pn for g in row])
    roots=s.roots_and_normals(p,order,ids,damage='missing_ninth_root' if damage=='missing_ninth' else None)
    first=direct_first(parts,order,damage);cc=cubes(parts,order)
    s.eq(ids,'WHOLE independent positive-branch physical scalar',first,scalar_recursion(parts,order,ids))
    lower_signs=lower_controls(parts,p,roots,first,cc,ids,damage)
    for label in (3,4,5,6):
        s.eq(ids,'ALL4 active lower half normals zero '+str(label),roots[label]['normals'][:10],[s.G0]*10)
    for a,b in ((3,6),(4,5)):
        s.eq(ids,'WHOLE reflected tenth forcing '+str(a)+'/'+str(b),
             [roots[a]['normals'][10]],[roots[b]['normals'][10]])
    for label in (3,4,5,6):
        need(roots[label]['normals'][10][1]==s.N0,'actual tenth forcing Gaussian first component')
        need(all(n%32%2==0 for n in roots[label]['normals'][10][0]),'actual tenth forcing even t')
    if damage=='reverse_skew_forcing':
        for label in (4,5):
            q=roots[label]['normals'][10][0]
            q[2]=s.ar.ns(q[2],-1)
    graded(p,roots,first,powers,order)
    bounds=bound_normals(roots)
    need(bounds['bound_terms']==[{'mu_power':0,'t_power':0,'b':7},{'mu_power':0,'t_power':2,'b':2},{'mu_power':1,'t_power':0,'b':13},{'mu_power':1,'t_power':2,'b':1},{'mu_power':2,'t_power':0,'b':2}], 'entire explicit repair integer bounds')
    documentary_real_baseline(roots,first,ids)
    anchor=[s.G1,s.G0,s.gs(s.G1,-1)]+[s.G0]*8
    s.eq(ids,'WHOLE marked original branch through tenth',roots[0]['root'],anchor)
    # The fifth scalar is calculated from physical distances, not from normals.
    need(first[10][1]==s.N0,'physical fifth scalar Gaussian first component')
    need(all(n%32%2==0 for n in first[10][0]),'physical fifth scalar even t')
    endpoint=parity_and_endpoint(parts,first,cc,ids)
    record={'agent':'six-sendov-3','role':'researcher','stage':stage,'order':order,
            'status':'whole exact author computation; analytic bridges unformalized; no independent review',
            'whole_parts':j.encoded_parts(parts),'whole_primitive':[s.encoded_vector(row) for row in p],
            'whole_all9_originals':s.output_roots(roots),
            'whole_all8_moments':[s.encoded_vector([power.get((e,0),s.G0) for e in range(order+1)]) for power in powers[1:]],
            'whole_first':s.encoded_vector(first),'whole_all8_cubes':s.encoded_vector(cc),
            'all4_q10':[{'label':label,'whole_real_polynomial':s.rpoly(roots[label]['normals'][10][0])} for label in (3,4,5,6)],
            'whole_fifth_scalar':s.rpoly(first[10][0]),'explicit_uniform_bound':bounds,
            'lower_positive_signs':lower_signs,
            'actual_central_endpoint_control':endpoint}
    if stage=='unit':record['full_unit_control']=unit_controls(parts,p,roots,first,ids,damage)
    record['whole_identity_count']=len(ids)
    record['whole_identity_digest']=sha256(canonical(ids)).hexdigest()
    return record
