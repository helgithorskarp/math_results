"""six-reviewer-1: independent Fraction/Gaussian matrix and reciprocal audit.
No author code, theorem executable, CAS, float, solver or external input.
Quadratic polarization is coefficient-complete; finite fixtures are controls.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import argparse, hashlib, json, signal, sys
signal.alarm(90)
class Error(Exception): pass
count=0
def require(ok,label):
    global count
    count+=1
    if not ok: raise Error(label)
class C:
    __slots__=('r','i')
    def __init__(self,r=0,i=0): self.r=F(r);self.i=F(i)
    def __add__(a,b):
        b=coerce(b);return C(a.r+b.r,a.i+b.i)
    __radd__=__add__
    def __neg__(a): return C(-a.r,-a.i)
    def __sub__(a,b): return a+-coerce(b)
    def __rsub__(a,b): return coerce(b)+-a
    def __mul__(a,b):
        b=coerce(b);return C(a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r)
    __rmul__=__mul__
    def __truediv__(a,b):
        b=coerce(b);n=b.r*b.r+b.i*b.i
        if not n: raise Error('zero Gaussian denominator')
        return C((a.r*b.r+a.i*b.i)/n,(a.i*b.r-a.r*b.i)/n)
    def __rtruediv__(a,b): return coerce(b)/a
    def __eq__(a,b):
        b=coerce(b);return a.r==b.r and a.i==b.i
    def conj(a): return C(a.r,-a.i)
    def n2(a): return a.r*a.r+a.i*a.i
    def __bool__(a): return bool(a.r or a.i)
def coerce(a): return a if isinstance(a,C) else C(a)
def eye(n): return [[C(i==j) for j in range(n)] for i in range(n)]
def mat(n,m=None): return [[C() for _ in range(m if m is not None else n)] for _ in range(n)]
def add(A,B): return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def scale(c,A): return [[c*a for a in r] for r in A]
def mul(A,B): return [[sum((a*b for a,b in zip(r,col)),C()) for col in zip(*B)] for r in A]
def star(A): return [[a.conj() for a in r] for r in zip(*A)]
def trace(A): return sum((A[i][i] for i in range(len(A))),C())
def norm2(A): return sum((a.n2() for r in A for a in r),F())
def diag(v): return [[coerce(v[i]) if i==j else C() for j in range(len(v))] for i in range(len(v))]
def outer(v): return [[a*b.conj() for b in v] for a in v]
def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,C): return [str(v.r),str(v.i)]
    if isinstance(v,list): return [encode(a) for a in v]
    if isinstance(v,tuple): return [encode(a) for a in v]
    if isinstance(v,dict): return {k:encode(a) for k,a in v.items()}
    return v
I=eye(8);H=[[C(F(1,8)) for _ in range(8)] for _ in range(8)];P=add(I,scale(-1,H));S=add(P,scale(3,H));Sinv=add(P,scale(F(1,3),H));J=scale(8,H)
def det_elim(A):
    A=[r[:] for r in A];out=C(1)
    for i in range(len(A)):
        piv=next((j for j in range(i,len(A)) if A[j][i]),None)
        if piv is None:return C()
        if piv!=i:A[i],A[piv]=A[piv],A[i];out=-out
        d=A[i][i];out=out*d
        for j in range(i+1,len(A)):
            f=A[j][i]/d
            for k in range(i+1,len(A)):A[j][k]=A[j][k]-f*A[i][k]
            A[j][i]=C()
    return out
def det_leib(A):
    out=C();n=len(A)
    for p in permutations(range(n)):
        inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));t=C((-1)**inv)
        for i in range(n):t=t*A[i][p[i]]
        out=out+t
    return out
def char_trace(A):
    # Faddeev--LeVerrier, independent of principal-minor/e_k encoding.
    B=eye(len(A));out=[C(1)]
    for k in range(1,len(A)+1):
        AB=mul(A,B);c=-trace(AB)/k;out.append(c);B=add(AB,scale(c,eye(len(A))))
    require(B==mat(len(A)),'Cayley-Hamilton final remainder')
    return out

def product_desc(u):
    out=[C(1)]
    for z in u:
        b=[C() for _ in range(len(out)+1)]
        for i,a in enumerate(out):b[i]=b[i]+a;b[i+1]=b[i+1]-a*z
        out=b
    return out

def poly_eval(p,q):
    t=C()
    for a in p:t=t*q+a
    return t

def polynomial_controls():
    out=[]
    vs=[[C() for _ in range(8)], [C(F(1,1000)) for _ in range(8)], [C(0,F(1,1000)) for _ in range(8)],
        [C(F((-1)**i,10000),F(i-3,20000)) for i in range(8)],
        [C(F(1,10000),F(1,20000)) for _ in range(4)]+[C(F(-1,20000),F(-1,30000)) for _ in range(4)],
        [C(0,F(1,2000)),C(0,F(-1,2000))]+[C() for _ in range(6)]]
    for ix,v in enumerate(vs):
        ell=F(1,2) if ix%2==0 else F(1);u=[ell+a for a in v];L=mul(mul(S,diag(u)),S);g=product_desc(u)
        expected=[(k+1)*a for k,a in enumerate(g)];ct=char_trace(L)
        require(ct==expected,'literal trace characteristic versus 9g-qgprime')
        require(ct[1]==-2*sum(u,C()),'first critical trace')
        # p(w)=w*product(1+u*w); reciprocal transformed derivative.
        asc=[C(1)]
        for z in u:
            b=[C() for _ in range(len(asc)+1)]
            for i,a in enumerate(asc):b[i]=b[i]+a;b[i+1]=b[i+1]+a*z
            asc=b
        pulled=[((-1)**k)*(k+1)*a for k,a in enumerate(asc)]
        require(pulled==ct,'full derivative reciprocal coefficient bridge')
        comm=add(mul(L,star(L)),scale(-1,mul(star(L),L)))
        if ix in (3,4,5):require(norm2(comm)>0,'heterogeneous complex nonnormal fixture')
        out.append(dict(index=ix,ell=ell,v=v,characteristic=ct,nonnormal_commutator_squared=norm2(comm)))
    return out

def quadratic_coeff(n,fun):
    e=[[F(i==j) for j in range(n)] for i in range(n)];diagc=[fun(a) for a in e];Q=[[F() for _ in range(n)] for _ in range(n)]
    require(fun([F()]*n)==0,'homogeneous quadratic constant')
    for i in range(n):Q[i][i]=diagc[i]
    for i,j in combinations(range(n),2):Q[i][j]=Q[j][i]=(fun([a+b for a,b in zip(e[i],e[j])])-diagc[i]-diagc[j])/2
    return Q

def quadratics():
    forms={}
    def build(v):return mul(mul(S,diag(v)),S)
    funcs={'imaginary':lambda y:norm2(build(y)), 'fixed_light':lambda y:norm2(mul(mul(P,build(y)),P)),
           'projected_perturbation':lambda xy:norm2(mul(P,build([C(xy[i],xy[8+i]) for i in range(8)])))}
    for name,fn in funcs.items():
        n=16 if name=='projected_perturbation' else 8;Q=quadratic_coeff(n,fn)
        for i in range(n):
            for j in range(n):
                target=(F(3*(i==j))+1 if name=='imaginary' else F(3,4)*(i==j)+F(1,64) if name=='fixed_light'
                        else (F(15,8)*(i==j)-F(1,8) if (i<8)==(j<8) else F()))
                require(Q[i][j]==target,'complete quadratic coefficient '+name)
        forms[name]=Q
    return forms

def heavy_control():
    ell=F(1,2);qh=9*ell;base=F(1)/(8*ell);z=C(base,F(1,100000));u=[C(qh)-1/z,C(qh)-1/z.conj()]+[C(ell)]*6;v=[a-ell for a in u];E=sum(a.n2() for a in v);M=sum(v,C());L=mul(mul(S,diag(u)),S)
    require(max(a.n2() for a in v)<=F(1,1000)**2,'designed heavy fixture epsilon')
    eta=[a/(qh-a) for a in u];require(sum(eta,C())==1,'exact heavy secular equation')
    r=[sum((S[i][j]*eta[j] for j in range(8)),C()) for i in range(8)];norm=sum(a.n2() for a in r)
    require([sum((L[i][j]*r[j] for j in range(8)),C()) for i in range(8)]==[qh*a for a in r],'right heavy eigenvector')
    Hp=scale(1/norm,outer(r));Pp=add(I,scale(-1,Hp));D=add(Pp,scale(-1,P));sine2=trace(mul(mul(Hp,P),Hp)).r
    require(star(Pp)==Pp and mul(Pp,Pp)==Pp and mul(Pp,[[a] for a in r])==[[C()] for _ in range(8)],'exact heavy orthogonal projector')
    require(mul(mul(D,D),D)==scale(sine2,D),'rank-two projection difference spectral identity')
    require(norm2(D)==2*sine2,'projection norm sine law')
    require(sine2<=F(15,8)*E/(49*ell**2),'sharper heavy-angle squared budget')
    K=scale(C(0,F(-1,2)),add(L,scale(-1,star(L))));require(K==mul(mul(S,diag([a.i for a in v])),S),'Hermitian imaginary part')
    delta=add(mul(mul(Pp,K),Pp),scale(-1,mul(mul(P,K),P)))
    require(norm2(delta)<=4*sine2*norm2(K),'moving projection Frobenius bound')
    R=C(qh)-9*ell-F(9,8)*M
    formula=-(C(qh)-9*ell)*M/(8*(qh-ell))+(qh/(qh-ell))*sum((a*a/(qh-b) for a,b in zip(v,u)),C())
    require(R==formula,'exact heavy quadratic remainder identity')
    require(R.n2()<=F(113,84)**2*E**2,'113/84 finite remainder control')
    chi=char_trace(L);require(poly_eval(chi,C(qh))==0,'literal heavy characteristic root')
    remainder=chi
    for _ in range(5):
        quotient=[remainder[0]]
        for a in remainder[1:-1]:quotient.append(a+ell*quotient[-1])
        require(remainder[-1]+ell*quotient[-1]==0,'fivefold colliding light root retained');remainder=quotient
    require(poly_eval(remainder,C(ell))!=0,'light collision has exactly multiplicity five')
    require(norm2(add(mul(L,star(L)),scale(-1,mul(star(L),L))))>0,'fivefold collision is nonnormal')
    return dict(ell=ell,u=u,E=E,M=M,heavy=qh,right_vector=r,heavy_projector=Hp,sine_squared=sine2,moving_error_squared=norm2(delta),remainder=R,characteristic=chi,quotient_after_five_colliding_lights=remainder)

def constants():
    # Each positive margin is the exact endpoint of an ordinary interval proof.
    a={
      'separation_4ell_minus_5eps':4*F(1,2)-5*F(1,1000),
      'qheavy_minus_uk_minus_three':8*F(1,2)-10*F(1,1000)-3,
      'heavy_vs_7ell':F(1,2)-9*F(1,1000),
      '113_over84_below2':2-F(113,84),
      'projection_sharp_squared':F(1,25)-F(15,8)/49,
      'combined_error_below_15_over4_squared':F(15,4)**2-F(660,49)-8*F(113,756)**2,
      'phase_51_over50':F(51,50)-F(2015,1996)**2,
      'original_phase_41_over40':F(41,40)-F(505,499)**2,
      'new_slack_10E':F(1,64)-10/(163200*F(13,8)**2),
      'original_slack_10E':F(1,64)-10/(164000*F(13,8)**2),
      'new_epsilon_squared':F(1,1000000)-F(3,8)/(163200*F(13,8)**2),
      'new_root_budget_to_energy':164000*F(639,640)**2-163200,
      'original_root_budget_to_energy':165000*F(639,640)**2-164000,
      'aggregate_older_maximum_budget':F(1,164000)-F(1,180000),
      'strengthened_energy_contains_original':F(1,163200)-F(1,164000),
      'strengthened_root_contains_original':F(1,164000)-F(1,165000),
      'sum_slack_below_17_over2':F(17,2)-F(113,84)-F(3500,499),
      'collective_slack_12_over5':F(12,5)-F(113,84)-F(403,400)**2/(2*(F(1,2)-F(1,1000))),
      'new_slack_12E_over5_entry':F(1,64)-F(12,5)/(163200*F(13,8)**2),
    }
    for k,v in a.items():require(v>0,'strict rational margin '+k)
    require(F(51,50)/163200==F(1,160000),'new exact phase entry')
    require(F(41,40)/164000==F(1,160000),'original exact phase entry')
    return a

def physical_controls():
    out=[]
    # Exact A=0 boundary configurations; d=2, gamma=3/8.
    for denominator in (2000,1868,1872):
        ell=F(1,2);u=[C(ell,F(1,denominator)),C(ell,F(-1,denominator))]+[C(ell)]*6;z=[1-1/a for a in u];E=sum((a-ell).n2() for a in u);B=sum((a+1).n2() for a in z);delta=max((a+1).n2() for a in z)
        require(all(a.n2()==1 for a in z),'original unit disk including all boundary roots')
        require(sum((a-ell).r for a in u)==0,'actual nonpositive trace A0')
        if denominator==2000:
            require(B<=F(4)*F(3,8)/165000 and delta>F(4)*F(3,8)/1200**2,'author strict maximum-domain witness')
            require(E<F(3,4)/1154736,'witness already inside prior baseline domain')
        elif denominator==1868:
            require(E>F(3,8)/(164000*4) and E<=F(3,8)/(163200*4),'new E-domain strict witness')
        else:
            require(B<=F(4)*F(3,8)/164000 and B>F(4)*F(3,8)/165000,'new B-domain strict witness')
        out.append(dict(denominator=denominator,u=u,z=z,E=E,B_original=B,maximum_original_shift_squared=delta))
    # Reciprocal feasibility identity holds coefficientwise as a polynomial in
    # a,x,y: (1-a*a)*|u|^2+2*a*Re(u)-1 = 2*x+(1-a*a)*(x*x+y*y).
    for a in (F(5,8),F(3,4),F(1)):
        ell=1/(1+a)
        for x,y in ((F(),F()),(F(),F(1,1000)),(F(-1,10000),F(1,1000)),(F(1,10000),F(-1,1000))):
            u=C(ell+x,y);v=C(x,y)
            excess=(1-a*a)*u.n2()+2*a*u.r-1
            require(excess==2*x+(1-a*a)*v.n2(),'closed reciprocal disk centered identity')
    return out

def communication_controls():
    out=[]
    for a in (F(5,8),F(3,4),F(1)):
        ell=1/(1+a);u=[C(ell+F(i+1,100000),F((-1)**i,200000)) for i in range(8)]
        z=[a-1/b for b in u];require(all(b.n2()<=1 for b in z),'communication fixture actual original disks')
        chi=[(k+1)*b for k,b in enumerate(product_desc(u))]
        O=9*sum((a**k*b/(k+1) for k,b in enumerate(chi)),C())
        Cp=sum((a**(8-k)*(1-a*a)**k*((-1)**k)*b/(k+1) for k,b in enumerate(chi)),C())
        prod_u=C(1);prod_z=C(1);polar=C(1)
        for b,c in zip(u,z):prod_u=prod_u*b;prod_z=prod_z*c;polar=polar*(1-a*c)/(a-c)
        require(O==9*prod_u*prod_z,'whole literal original-origin communication')
        require(Cp==polar,'whole literal original-polar communication')
        require(O.n2()<=(9*prod_u).n2(),'origin necessary modulus constraint')
        require(Cp.n2()>=1,'polar necessary modulus constraint')
        if a==1:require((-chi[1]).r>=8,'a1 direct original trace condition')
        out.append(dict(a=a,u=u,z=z,chi=chi,O=O,C_polar=Cp,product_critical=9*prod_u))
    return out

def reject_controls():
    out=[]
    checks=[('missing_heavy_scale',lambda:require(F(3,4)+F(8,64)+F(81*8,64)<=1,'heavy phase scale damaged')),
            ('lost_rank_one_frobenius',lambda:require(quadratic_coeff(8,lambda y:norm2(mul(mul(P,diag(y)),P)))[0][1]==0,'missing rankone term')),
            ('wrong_characteristic_multiplicity',lambda:require(char_trace(mul(mul(S,diag([F(1,2)]*8)),S))[1]==-F(1,2)*8,'wrong k factor')),
            ('false_Hermitian_assumption',lambda:require(mul(mul(S,diag([C(F(1,2),F(1,1000))]+[C(F(1,2))]*7)),S)==star(mul(mul(S,diag([C(F(1,2),F(1,1000))]+[C(F(1,2))]*7)),S)),'false Hermitian assumption')),
            ('overclaimed_phase_101_over100',lambda:require(F(101,100)>=F(2015,1996)**2,'overclaimed constant')),
            ('enlarged_root_without_shrink_cost',lambda:require(163200*F(639,640)**2>=163200,'lost inverse-distance cost')),
            ('marked_multiple_false_finite',lambda:require(C(1)-C(1),'marked multiple finite')),
            ('squared_norm_is_real',lambda:require(C(1,1)*C(1,1)==C(2),'lost complex conjugation'))]
    for label,fn in checks:
        try:fn()
        except Error:out.append(label)
        else:raise Error('damage accepted '+label)
    return out

def generate():
    require(mul(S,Sinv)==I and mul(S,S)==add(I,J),'matrix square and inverse')
    require(mul(P,H)==mat(8) and mul(P,P)==P and mul(H,H)==H,'complementary projections')
    minors=[]
    B=add(I,J)
    for mask in range(256):
        ix=[i for i in range(8) if mask>>i&1];sub=[[B[i][j] for j in ix] for i in ix];d=det_elim(sub);d2=det_leib(sub)
        require(d==d2==len(ix)+1,'every principal minor factor by two independent determinants')
        minors.append([mask,len(ix),d.r])
    record=dict(schema='six-reviewer-1-critical-phase-audit-v1',arithmetic='stdlib Fraction and own exact Gaussian pairs',projections={'P':P,'H':H,'S':S,'S_inverse':Sinv},principal_minors=minors,complete_quadratic_coefficients=quadratics(),polynomial_controls=polynomial_controls(),nonnormal_fivefold_collision=heavy_control(),strict_rational_margins=constants(),physical_witnesses=physical_controls(),actual_communication_controls=communication_controls(),semantic_damage_rejections=reject_controls())
    record['exact_predicates_including_controls']=count
    return encode(record)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--emit',action='store_true');ap.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'));args=ap.parse_args();r=generate();data=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if args.emit:sys.stdout.write(data);return
    try:loaded=json.loads(args.expected.read_text())
    except (OSError,ValueError) as e:raise Error('expected fixture unreadable') from e
    require(loaded==r,'entire regenerated fixture comparison')
    print(json.dumps({'status':'PASS','schema':r['schema'],'exact_predicates_including_controls':r['exact_predicates_including_controls'],'principal_minors':256,'quadratic_forms':3,'literal_polynomial_controls':6,'fivefold_light_collision_nonnormal':True,'strict_margins':len(r['strict_rational_margins']),'semantic_damages':len(r['semantic_damage_rejections']),'sha256':hashlib.sha256(data.encode()).hexdigest(),'expected_bytes':len(data.encode())},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Error as e:print('FAIL: '+str(e),file=sys.stderr);raise SystemExit(1)
