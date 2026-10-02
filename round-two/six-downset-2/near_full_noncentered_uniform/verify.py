"""Independent exact controls for the ordinary proof; stdlib only.

No finite cohort is promoted to unbounded coverage. No assertions or solver.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import argparse,hashlib,json
import affine,certificate as c
from model import parameters,physical,quadratic,require

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def evaluate(n,B):
    aa,l,u,mu=c.tests(n);a,F=physical(n,B);b,H=physical(n,B,True)
    require(a==b==aa,'Test layer order')
    return quadratic(H,u)+mu*quadratic(F,l)

def affine_controls(n):
    pairs=[p for p in affine.supported_pairs(n) if p[0]>=2]
    free,recover=affine.rref(n);require(pairs==free,'Independent RREF coordinates')
    N,s,h=parameters(n);base=[Q(s-1) if a+b==n else Q(0) for a,b in pairs]
    B=affine.direct(n,base);require(B==recover(base),'Independent base completion')
    anchor=evaluate(n,B);require(anchor==c.identity_rhs(n,B),'Full-face anchor identity')
    coeffs=[]
    for i,p in enumerate(pairs):
        values=base.copy();values[i]+=1;T=affine.direct(n,values)
        require(T==recover(values),'Independent direction completion')
        z=evaluate(n,T);rhs=c.identity_rhs(n,T)
        require(z==rhs,'Full-face exact directional identity')
        coeffs.append([list(p),str(z-anchor)])
    # A mixed signed vector checks the assembled affine identity as well.
    values=[v+Q((-1)**i*(i+1),13) for i,v in enumerate(base)]
    T=affine.direct(n,values);require(T==recover(values),'Independent signed completion')
    require(evaluate(n,T)==c.identity_rhs(n,T),'Signed full-face identity')
    return {'n':n,'directions':len(pairs),'coefficients_sha256':digest(coeffs),
            'complement_directions':sum(a+b==n for a,b in pairs),
            'two_set_cancellations':sum(a==2 for a,b in pairs),
            'positive_proper_classes':len(c.weights(n))}

def scalar_controls(n):
    rec=c.constant(n);v,mu,f,k=c.profile(n);s=rec['s'];h=rec['h'];q=rec['q']
    m2=sum(Q(comb(n,a)*(2*a-n)**2,4) for a in range(n+1))
    m4=sum(Q(comb(n,a)*(2*a-n)**4,16) for a in range(n+1))
    require(m2==Q(n*2**n,4) and m4==Q((3*n*n-2*n)*2**n,16),'Literal binomial moments')
    full=sum(comb(n,a)*(Q(5,4)-Q((2*a-n)**2,4*n))**2 for a in range(n+1))
    require(full==c.moment_bound(n),'Full square moment expansion')
    require(rec['bulk_norm2']<=full,'Clipping/discarding reduces squared norm')
    bound= n*h+q*(8*h-10*s)+(n-1)*full+mu*(4*s-4)
    require(bound==c.tail_bound(n),'Closed tail bound equality')
    eta_at_root2=rec['eta']+Q(4*q*(n-1)**2,h)
    require(eta_at_root2<=bound,'Optimized endpoint root and clipped moment')
    if n>=12:
        require(s>12*n*n,'Tail base and induction consequence, finite control')
        require(c.tail_bound(n)<0 and rec['eta']<0,'Negative tail scalar control')
    if n==11:
        require(rec['bulk_norm2']==Q(4533,2),'Endpoint exact norm')
        require(rec['eta']==-Q(1535,93),'Endpoint exact negative constant')
        require(eta_at_root2==5,'Root2 negative control: fails endpoint exclusion')
    if n==16:
        require(rec['positive_mass_floor']>Q(1,64),'Improves credited9365 fixed-order floor')
    if n in (6,7,8,10):
        require(rec['eta']>0,'Compatible small-order controls are not exclusions')
    weights=c.weights(n);count=sum(c.pair_count(n,a,b) for a,b in weights)
    low=sum(comb(n,a)*2**(n-a) for a in range(3))
    both=sum(comb(n,a)*comb(n-a,b) for a in range(3) for b in range(3))
    complements=2**n-2*(1+n+q)
    require(2*count==3**n-2*low+both-complements,
            'Independent ternary-assignment original pair count')
    return {**{key:str(value) if type(value) is Q else value for key,value in rec.items()},
            'tail_bound':str(bound),'eta_root2':str(eta_at_root2),
            'proper_unordered_pairs':count,'weights':len(weights),
            'minimum_weight':str(min(weights.values())) if weights else None,
            'maximum_weight':str(max(weights.values())) if weights else None,
            'profile_sha256':digest({str(a):str(v[a]) for a in v})}

def literal_control(n):
    N,s,h=parameters(n);pairs=[p for p in affine.supported_pairs(n) if p[0]>=2]
    values=[Q(s-1) if a+b==n else Q((-1)**(a+b),17) for a,b in pairs]
    B=affine.direct(n,values)
    masks=[a for a in range(1,2**n) if a.bit_count()<=n-2];m=len(masks)
    sizes=[a.bit_count() for a in masks]
    C=[[Q(s*int(i==j)-1)+(B[sizes[i]][sizes[j]] if not (a&b) else 0)
        for j,b in enumerate(masks)] for i,a in enumerate(masks)]
    require(m+1==N,'Actual domain includes empty and omits n+1 high sets')
    sums=[sum(row) for row in C]
    empty=[1-v for v in sums];loop=1+sum(sums)
    L=[[loop]+empty]+[[empty[i]]+[v+1 for v in row] for i,row in enumerate(C)]
    require(all(sum(row)==N for row in L),'Actual full rows')
    require(all(L[i+1][i+1]==s for i in range(m)),'Original nonempty diagonals')
    require(all(L[i+1][j+1]==0 for i,a in enumerate(masks) for j,b in enumerate(masks)
                if i!=j and (a&b)),'All intersecting original pairs')
    for p in range(n):
        star=[int(bool(a&(1<<p))) for a in masks]
        require(sum(star)==s,'Actual star size')
        require(all(sum(v*z for v,z in zip(row,star))==0 for row in C),'Actual C star kernels')
    aa,l,u,mu=c.tests(n);lv=[l[a-1] for a in sizes];uv=[u[a-1] for a in sizes]
    U=[[Q(N*int(i==j))-L[i+1][j+1] for j in range(m)] for i in range(m)]
    direct=quadratic(U,uv)+mu*quadratic(C,lv)
    require(direct==evaluate(n,B)==c.identity_rhs(n,B),'Literal original scalar identity')
    # Invalid empty-loop convention is rejected by the independent full row test.
    require(sum(empty)!=N,'Setting the actual empty loop to zero fails row normalization')
    return {'n':n,'original_order':N,'checked_original_entries':N*N,
            'identity':str(direct),'table_sha256':digest([[str(v) for v in row] for row in B]),
            'scope':'Affine identity/support/rows/stars only; no PSD feasibility claim'}

def noninvariant_control():
    n=12;N,s,h=parameters(n);aa,l,u,mu=c.tests(n);rho=c.weights(n)
    def mask(points):
        return sum(1<<p for p in points)
    left={mask([0,1,2]):1,mask([3,4,5]):1,mask([0,1]):-1,mask([2,3,4,5]):-1}
    right={mask([6,7,8]):1,mask([9,10,11]):1,mask([6,7]):-1,mask([8,9,10,11]):-1}
    for trade in (left,right):
        require(sum(trade.values())==0,'Trade has zero mean')
        require(all(sum(v for a,v in trade.items() if a&(1<<p))==0 for p in range(n)),
                'Trade annihilates each actual point star')
    score=lambda trade,vec:sum(z*vec[a.bit_count()-1] for a,z in trade.items())
    direct=2*mu*score(left,l)*score(right,l)-2*score(left,u)*score(right,u)
    rhs=Q(0);positions=0;omitted=0
    for a,x in left.items():
        for b,y in right.items():
            require(not a&b and a!=b,'Every changed original pair is allowed')
            positions+=2;ka,kb=sorted((a.bit_count(),b.bit_count()))
            if ka>=3 and ka+kb<n:
                rhs+=2*mu*rho[ka,kb]*x*y;omitted+=1
    require(rhs==direct!=0,'Noninvariant mixed-cardinality original identity')
    return {'n':n,'changed_ordered_positions':positions,'omitted_unordered_pairs':omitted,
            'exact_scalar_change':str(direct),'all_actual_stars_and_rows_preserved':True,
            'scope':'Signed affine trade; no PSD/cap feasibility claim'}

def tail_polynomial_controls():
    # These expansions support the written all-n induction, never replace it.
    for t in (0,1,2,7):
        n=12+t
        require(12*n*n-23*n-13==12*t*t+265*t+1439,'Exponential induction polynomial')
        require(5*n*n-45*n-3==5*t*t+75*t+177,'Linear coefficient dominance')
        require(23*n*n-22*n+24==23*t*t+530*t+3072,'Cubic remainder dominance')
    return {'tail_start':12,'base_s':2036,'base_quadratic':1728,
            'induction_coefficients':[1439,265,12],
            'linear_dominance_coefficients':[177,75,5],
            'remainder_dominance_coefficients':[3072,530,23],
            'all_coefficients_positive':True}

def run():
    orders=(6,7,8,10,11,12,16,20)
    return {'agent':'six-downset-2','role':'researcher',
            'proof_status':'Ordinary all-n author proof, unformalized and independently unreviewed',
            'theorem_domain':'All real original capped H, near cube, every integer n>=11',
            'affine_controls':[affine_controls(n) for n in orders],
            'scalar_controls':[scalar_controls(n) for n in orders],
            'literal_controls':[literal_control(n) for n in (6,8)],
            'noninvariant_control':noninvariant_control(),'tail_controls':tail_polynomial_controls(),
            'no_finite_enumeration_substituted_for_unbounded_proof':True,
            'no_solver_or_floating_point_input':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',type=Path);a=p.parse_args()
    result=run();raw=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        require(a.check.read_bytes()==raw.encode(),'Complete frozen record mismatch')
        print(json.dumps({'ok':True,'record_sha256':hashlib.sha256(raw.encode()).hexdigest(),
                          'affine_directions':sum(r['directions'] for r in result['affine_controls']),
                          'literal_original_entries':sum(r['checked_original_entries'] for r in result['literal_controls']),
                          'uniform_exclusion_starts':11,'tail_start':12,'no_centering':True}))
    else:
        print(raw,end='')
