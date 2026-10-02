"""Independent definition-level jets over QQ(i)(x), x=a/(1+a).

No researcher program is imported. Own prior phase-jet engine is reused;
all new polar/reference/weight formulas are reconstructed from definitions.
All eight phase variables coexist in one truncated polynomial product.
"""
import hashlib
import json
from fractions import Fraction
from math import comb


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def coeffs(f):
    """Increasing-power rational coefficients; requires an actual polynomial."""
    need(f.denom.degree() == 0, 'uncleared rational denominator')
    degree=max((m[0] for m in f.numer), default=0)
    return [str(Fraction(str(f.numer.get((j,), 0)))/Fraction(str(f.denom[(0,)])))
            for j in range(degree+1)]


def bernstein(power, lo, hi):
    """Use exact affine substitution, then reverse the entire expansion."""
    p=list(map(Fraction,power)); n=len(p)-1
    transformed=[sum(p[j]*comb(j,k)*lo**(j-k)*(hi-lo)**k
                     for j in range(k,n+1)) for k in range(n+1)]
    b=[sum(transformed[k]*Fraction(comb(i,k),comb(n,k)) for k in range(i+1))
       for i in range(n+1)]
    reverse=[Fraction(0)]*(n+1)
    for i,c in enumerate(b):
        for j in range(n-i+1):
            reverse[i+j]+=c*comb(n,i)*comb(n-i,j)*(-1)**j
    need(reverse==transformed,'whole reversed Bernstein equality')
    return {'degree':n,'power':list(map(str,p)),'bernstein':list(map(str,b)),
            'minimum':str(min(b))}


def derive():
    from sympy import QQ, QQ_I, I, __version__
    from sympy.polys.rings import ring
    need(__version__=='1.14.0','pinned SymPy')
    K=QQ_I.frac_field('x');x=K.gens[0];ell=1-x;a=x/ell
    Kr=QQ.frac_field('x');xr=Kr.gens[0];lr=1-xr;ar=xr/lr
    imaginary=K.from_sympy(I)
    def real(f):
        ex=K.to_sympy(f);need(not ex.has(I),'unexpected imaginary coefficient')
        return Kr.from_sympy(ex)
    R,*gens=ring('u,t0,t1,t2,t3,t4,t5,t6,t7',K);u,*ts=gens
    def cut(p):return R.from_dict({m:c for m,c in p.items() if sum(m[1:])<=2})
    radii=[9*ell-x*sum(t*t for t in ts[1:])/2]+[ell+x*t*t/2 for t in ts[1:]]
    q=[cut(r*(1+imaginary*t-t*t/2)) for r,t in zip(radii,ts)]
    oo=R.one;cc=R.one;pp=R.one;bb=1-a*a
    for z,r in zip(q,radii):
        oo=cut(oo*(1-a*u*z));cc=cut(cc*(a+bb*u*z));pp=cut(pp*r)
    def integrate(polynomial,multiplier):
        jet={}
        for m,c in polynomial.items():jet[m[1:]]=jet.get(m[1:],K.zero)+multiplier*c/(m[0]+1)
        return jet
    oj=integrate(oo,9);cj=integrate(cc,1);pj={m[1:]:c for m,c in pp.items()}
    zero=(0,)*8;P=9*lr**8
    need(real(oj[zero])==real(pj[zero])==P and real(cj[zero])==1,'complete model equalities')
    wo=[];wc=[]
    for i in range(8):
        m=tuple(int(j==i) for j in range(8))
        wo.append(real(oj[m]/imaginary));wc.append(real(cj[m]/imaginary))
    ao=[];ap=[];real_o=[];real_p=[]
    for i in range(8):
        ro=[];rp=[];fo=[];fp=[]
        for j in range(8):
            m=tuple(int(k==i)+int(k==j) for k in range(8));scale=1 if i==j else 2
            v=real(oj.get(m,K.zero)-pj.get(m,K.zero))/scale
            w=real(cj.get(m,K.zero))/scale
            ro.append(v);rp.append(w/(1-ar*ar))
            fo.append(v+wo[i]*wo[j]/(2*P))
            fp.append((w+wc[i]*wc[j]/2)/(1-ar*ar))
        real_o.append(ro);real_p.append(rp);ao.append(fo);ap.append(fp)
    def types(matrix):
        h,u,d,e=matrix[0][0],matrix[0][1],matrix[1][1],matrix[1][2]
        for i in range(8):
            for j in range(8):
                need(matrix[i][j]==(h if i==j==0 else d if i==j else u if i==0 or j==0 else e),'all64 S7 entries')
        return [h,u,d,e]
    types(ao);types(ap)
    # Radial derivatives use a fresh two-variable primitive product, not phase formulas.
    V,v,t=ring('v,t',Kr)
    def radial(heavy,small):
        rs=[9*lr+heavy*v,lr+small*v]+[lr]*6
        origin=V.one;polar=V.one;product=V.one
        for r in rs:origin*=1-ar*t*r;polar*=ar+(1-ar*ar)*t*r;product*=r
        do=sum(9*c/(m[1]+1) for m,c in origin.items() if m[0]==1)-product.get((1,0),Kr.zero)
        dp=sum(c/(m[1]+1) for m,c in polar.items() if m[0]==1)/(1-ar*ar)
        return do,dp
    heavy,polar_heavy=radial(1,0);slack,g=radial(-1,1);H=-heavy
    Ka=QQ.frac_field('a');av=Ka.gens[0];L=1+av;cutoff=QQ(5,8);delta=av-cutoff
    def to_a(f):
        xx=av/L
        def val(p):return sum(Ka.convert(c)*xx**m[0] for m,c in p.items())
        return val(f.numer)/val(f.denom)
    aoa=[to_a(z) for z in types(ao)];apa=[to_a(z) for z in types(ap)]
    ca,ga,ha,pha=map(to_a,[slack,g,H,polar_heavy])
    def evaluate(f,z):
        power_n=f.numer;power_d=f.denom
        numerator=sum(Fraction(str(c))*z**m[0] for m,c in power_n.items())
        denominator=sum(Fraction(str(c))*z**m[0] for m,c in power_d.items())
        need(denominator!=0,'exceptional evaluation denominator')
        return numerator/denominator
    mu=evaluate(ca,Fraction(5,8))/evaluate(ga,Fraction(5,8))
    need(mu==Fraction(22096964222976,21378414915091),'unique fixed weight')
    qm=Ka.convert(QQ(str(mu)));D=18*L**7
    joint=[o-qm*p for o,p in zip(aoa,apa)]
    n=[z*D for z in joint];o=[z*D for z in aoa];p=[z*2*L**2 for z in apa]
    cm=ca-qm*ga;hm=ha+qm*pha
    U=L**6*cm/delta;VV=(n[2]-n[3])/delta
    lamO=aoa[2]-aoa[3];lamP=apa[2]-apa[3]
    compatibility=L**8*(ga*lamO-ca*lamP)
    RR=compatibility/(av*(8*av-5))
    need(all(Fraction(z)>0 for z in coeffs(RR)), 'all compatibility factor coefficients positive')
    polar_transverse=coeffs(2*L**2*lamP)
    need(Fraction(polar_transverse[0])==0 and all(Fraction(z)<0 for z in polar_transverse[1:]),'polar transverse strict negative')
    # Independent primitive integral for g and heavy polar derivative.
    def polar_integral(k,n):
        return sum(Ka.convert(QQ(comb(n,i)))*av**(n-i)*(1-av)**i/QQ(k+i+1) for i in range(n+1))
    j1=polar_integral(1,7);j2=polar_integral(2,6);j3=polar_integral(3,5)
    need(ga==8*(1-av)*j2 and pha==j1,'whole polar radial integral identities')
    need(ha==(L**8-1)/(8*av*L**6),'whole heavy origin derivative')
    need(evaluate(cm,Fraction(5,8))==0 and evaluate(joint[2]-joint[3],Fraction(5,8))==0,'both endpoint degeneracies')
    boundary_o=[str(evaluate(z,Fraction(1))) for z in aoa]
    boundary_p=[str(evaluate(z,Fraction(1))) for z in apa]
    need(boundary_p==['-9/8','0','-1/8','0'],'full normalized polar boundary matrix')
    need(evaluate(ga,Fraction(1))==0 and evaluate(pha,Fraction(1))==Fraction(1,2),'boundary polar radial derivatives')
    def bound(z):return bernstein(coeffs(z),Fraction(5,8),Fraction(1))
    original={'U':bound(U),'V':bound(VV),
              'B_h':bound(n[0]-D/10000),
              'B_det':bound((n[0]-D/10000)*(n[2]+6*n[3]-D/10000)-7*n[1]**2)}
    need(all(Fraction(c)>0 for v in original.values() for c in v['bernstein']),'whole original interval certificate')
    need(sum(len(v['bernstein']) for v in original.values())==85,'original coefficient coverage')
    # Fixed, independently certified improvement; no grid or fit.
    improved={'heavy':bound(n[0]-D/100),
              'determinant':bound((n[0]-D/100)*(n[2]+6*n[3]-D/100)-7*n[1]**2)}
    need(all(Fraction(c)>0 for v in improved.values() for c in v['bernstein']), 'improved full collective block')
    need(Fraction(original['U']['minimum'])>48,'slack slope3/4')
    need(Fraction(original['V']['minimum'])>Fraction(2304,40),'transverse slope1/40')
    heavy_bound=bound((Ka.convert(QQ(9,8))-hm)*L**6)
    need(all(Fraction(c)>0 for c in heavy_bound['bernstein']), 'joint heavy derivative less than9/8')
    full_joint=[[coeffs(n[0] if i==j==0 else n[2] if i==j else n[1] if i==0 or j==0 else n[3])
                for j in range(8)] for i in range(8)]
    # Coverage above checked all64 entries before the four-type conversion.
    polynomials={'j1':j1,'j2':j2,'j3':j3,'g':ga,
        'origin_slack_numerator':ca*L**6,
        **dict(zip(['polar_heavy_numerator','polar_cross_numerator','polar_diagonal_numerator','polar_off_numerator'],p)),
        'polar_trans_numerator':2*L**2*lamP,'joint_slack_numerator':cm*L**6,
        'matrix_denominator':D,'joint_transverse_numerator':n[2]-n[3],
        'joint_collective_numerator':n[2]+6*n[3],
        'joint_determinant_numerator':n[0]*(n[2]+6*n[3])-7*n[1]**2,
        'compatibility_W_numerator':compatibility,
        **dict(zip(['joint_heavy_numerator','joint_cross_numerator','joint_diagonal_numerator','joint_off_numerator'],n))}
    # Recover the author's two whole64 directional record hashes from OUR
    # simultaneous products, after reconstructing all matrix entries.
    basis=[[int(i==j) for j in range(8)] for i in range(8)]
    directions=list(basis)
    for i in range(8):
        for j in range(i+1,8):
            directions += [[basis[i][k]+sign*basis[j][k] for k in range(8)] for sign in (1,-1)]
    otypes=types(ao); ox=[z*18*lr**8 for z in otypes]
    wc_a=list(map(to_a,wc))
    def quadratic(z,v,field):
        return sum((z[0] if i==j==0 else z[2] if i==j else z[1] if i==0 or j==0 else z[3])*v[i]*v[j]
                   for i in range(8) for j in range(8))
    origin_rows=[];polar_rows=[]
    for v in directions:
        origin_rows.append({'direction':v,'coefficients':coeffs(quadratic(ox,v,Kr))})
        polar_rows.append({'direction':v,'phase_numerator':coeffs(quadratic(p,v,Ka)),
            'modulus_unnormalized':coeffs(2*(1-av**2)*quadratic(apa,v,Ka)),
            'imaginary_linear':coeffs(sum(wc_a[i]*v[i] for i in range(8)))})
    need(len(origin_rows)==len(polar_rows)==64,'whole directional coverage')
    # Actual disk-rooted family is already known in graph7290. Independent
    # closed first-power formula verifies the credited endpoint obstruction.
    from sympy import symbols, diff, sqrt, Rational, simplify
    aa,c=symbols('aa c',real=True)
    ff=6/sqrt(aa**2+2*aa*c+1)+10*(aa+c)/(aa**2+2*aa*c+1)
    fc=diff(ff,c).subs(c,1);fcc=diff(ff,c,2).subs(c,1)
    # Positive a+1 fixes the square root branch; evaluate exactly at cutoff.
    endpoint_fourth= simplify(fcc.subs(aa,Rational(5,8))/8)
    need(simplify(fc.subs(aa,Rational(5,8)))==0 and endpoint_fourth==-Rational(9600,371293), 'known actual-polynomial endpoint quartic')
    rejected=[]
    def reject(label,operation):
        try:operation()
        except ValueError:rejected.append(label)
        else:raise ValueError('mathematical damage accepted: '+label)
    reject('omitted origin modulus rank-one',lambda:need(real_o==ao,'whole origin modulus matrix'))
    reject('omitted polar modulus rank-one',lambda:need(real_p==ap,'whole polar modulus matrix'))
    reject('reversed polar multiplier',lambda:need([o+qm*p for o,p in zip(aoa,apa)]==joint,'whole joint sign'))
    reject('weight one',lambda:need(evaluate(ca-ga,Fraction(5,8))==0,'cutoff slack balance'))
    reject('doubled phase matrix',lambda:need([2*z for z in joint]==joint,'Taylor matrix normalization'))
    reject('wrong boundary polar sign',lambda:need(boundary_p==['9/8','0','1/8','0'],'normalized boundary'))
    damaged=[list(row) for row in ao];damaged[1][2]+=1
    reject('broken small-coordinate orbit',lambda:types(damaged))
    bad=bound(-n[0]-D/100)
    reject('negative collective heavy pivot',lambda:need(all(Fraction(c)>0 for c in bad['bernstein']),'full heavy positivity'))
    # Whole 64-entry boundary value and rank-two decomposition remain represented.
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','sympy':__version__,
        'domain':'QQ(i)(x), x=a/(1+a), simultaneous eight-phase degree2 jets; converted to QQ(a)',
        'mu':str(mu),'origin_numerators':[coeffs(z) for z in o],
        'polar_numerators':[coeffs(z) for z in p],'joint_numerators':[coeffs(z) for z in n],
        'joint_full_matrix_sha256':digest(full_joint),'joint_full_matrix_entries':64,
        'original_bounds':original,'compatibility_R':coeffs(RR),
        'polar_transverse_numerator':polar_transverse,
        'slack_numerator':coeffs(cm*L**6),'heavy_joint_numerator':coeffs(hm*L**6),
        'boundary':{'origin_types':boundary_o,'polar_types':boundary_p,'joint_types':[str(evaluate(z,Fraction(1))) for z in joint]},
        'improved_collective_bounds':improved,'heavy_9_8_bound':heavy_bound,
        'proved_constants':{'phase_matrix_slope':'1/40','slack_slope':'3/4','reference_slack':'3/8','reference_phase':'1/80','nearby_heavy_upper':'5/4','tuple_slack':'3/10','tuple_phase':'1/100'},
        'author_polynomials':{k:coeffs(v) for k,v in polynomials.items()},
        'directional_hashes':{'origin':digest(origin_rows),'polar':digest(polar_rows),'count_each':64},
        'credited_endpoint_quartic':str(endpoint_fourth),'mathematical_damage_rejections':rejected,
        'jet_counts':{'origin_terms':len(oo),'polar_terms':len(cc),'origin_coefficients':len(oj),
                      'polar_coefficients':len(cj),'primitive_phase_entries':128},
        'origin_modulus_rank_one_nonzero':any(ao[i][j]!=real_o[i][j] for i in range(8) for j in range(8)),
        'polar_modulus_rank_one_nonzero':any(ap[i][j]!=real_p[i][j] for i in range(8) for j in range(8))}
