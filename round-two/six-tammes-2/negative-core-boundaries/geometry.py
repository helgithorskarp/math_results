"""Regenerate all four exact geometric boundary resultants in Q(t)[q].

Actual author six-tammes-2, researcher. Requires SymPy1.14.0. No numerical
roots or imported geometric coefficient tables are used in this producer.
"""
from pathlib import Path
from itertools import permutations
import json,time,argparse
import sympy as sp
from sympy.polys.rings import ring
HERE=Path(__file__).resolve().parent

def derive():
    started=time.monotonic();t=sp.Symbol('t');K=sp.QQ.frac_field(t);R,q=ring('q',K)
    T=K.from_sympy(t);zero,one=R.zero,R.one
    def g(a):return R.ground_new(K.convert(a))
    H=[[one if i==j else g(T) for j in range(3)] for i in range(3)]
    HI=[[g((1/(1-T) if i==j else 0)-T/((1-T)*(1+2*T))) for j in range(3)] for i in range(3)]
    D=(1-T)**2*(1+2*T);r=2*T/(1+T);k=T*(9*T*T-2*T-3)/(1+T)**2
    def dot(a,b):return sum((a[i]*H[i][j]*b[j] for i in range(3) for j in range(3)),zero)
    def mv(A,x):return [sum((a*b for a,b in zip(row,x)),zero) for row in A]
    def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    def det(A):
        ans=zero
        for p in permutations(range(len(A))):
            term=g((-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p))))
            for i,j in enumerate(p):term*=A[i][j]
            ans+=term
        return ans
    def require(ok,message):
        if not ok:raise ValueError(message)
    def encode(a):
        n,d=sp.fraction(K.to_sympy(a))
        nl=list(reversed(sp.Poly(n,t,domain=sp.QQ).all_coeffs()));dl=list(reversed(sp.Poly(d,t,domain=sp.QQ).all_coeffs()))
        scale=sp.ilcm(*[c.q for c in nl+dl])
        return {'n':[int(c*scale) for c in nl],'d':[int(c*scale) for c in dl]}
    def polynomial(a):return [encode(a.get((i,),K.zero)) for i in range(a.degree()+1)]
    B={i:[one if j==s else zero for j in range(3)] for s,i in enumerate((1,2,4))}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4),(3,1,4,2)):
        B[n]=[g(r)*(a+b)-c for a,b,c in zip(B[i],B[j],B[o])]
    require(dot(B[3],B[3])==one,'B3 unit')
    require(dot(B[3],B[1])==g(T) and dot(B[3],B[4])==g(T),'B3 common contact neighbor')
    require(dot(B[12],B[1])==g(T),'B1 shared neighbor of B3,B12')
    lambda_=dot(B[3],B[12]).get((0,),K.zero)
    Wother=[g(2*T/(1+lambda_))*(a+b)-c for a,b,c in zip(B[3],B[12],B[1])]
    require(dot(Wother,Wother)==one,'other boundary W unit')
    require(dot(Wother,B[3])==g(T) and dot(Wother,B[12])==g(T),'both boundary contacts')
    d=mv(HI,cross(B[8],B[2]));L=g(D)+q*q
    un=[g(T)*a*L+(g(D)-q*q)*(b-g(T)*a)+g(2*D)*q*c for a,b,c in zip(B[8],B[2],d)]
    require(dot(un,un)==L*L,'U circle unit')
    require(dot(un,B[8])==g(T)*L,'U retained cross contact')
    def parts(part):
        c,rows=part
        return {'constant':str(c),'factors':[{
            'coefficients':[int(a) for a in reversed(sp.Poly(f,t).all_coeffs())],
            'multiplicity':int(m),
            'roots_on_I':int(sp.Poly(f,t).count_roots(sp.Rational(14,25),sp.Rational(593,1000)))
        } for f,m in rows]}
    def pair(E,P):
        require(E.degree()==2 and P.degree()==4,'literal quadratic/quartic degrees')
        res=P.resultant(E);require(res!=K.zero,'nonzero necessary boundary resultant')
        n,den=sp.fraction(K.to_sympy(res))
        return {'E':polynomial(E),'P':polynomial(P),'resultant':encode(res),
                'numerator_factors':parts(sp.factor_list(n,t)),
                'denominator_factors':parts(sp.factor_list(den,t))}
    critical={'format':1,'domain':['14/25','593/1000'],'coefficient_domain':'Q(t)[q]',
              'lambda':encode(lambda_),'boundary_W':{},'resultants':{}}
    for name,W in [('B1',B[1]),('other',Wother)]:
        E=dot(un,W)-g(k)*L
        vectors=(un,B[10],W);rhs=(g(k)*L,g(T),g(k))
        G=[[dot(a,b) for b in vectors] for a in vectors]
        P=det([row+[rhs[i]] for i,row in enumerate(G)]+[list(rhs)+[one]])
        critical['boundary_W'][name]=[encode(a.get((0,),K.zero)) for a in W]
        critical['resultants'][name]=pair(E,P)
    den=(2*r-1)*(r+1);l0=(2*r*k+1-r)/den
    require((r+k)/den==T,'reflected anchor cross products')
    G3=[[one if i==j else g(k) for j in range(3)] for i in range(3)]
    def inner3(x,y):return sum((x[i]*G3[i][j]*y[j] for i in range(3) for j in range(3)),zero)
    A0=[g(a/den) for a in (r,r,1-r)]
    A5=[g(a/den) for a in (1-r,r,r)]
    Ue,We,Ve=[[one if i==j else zero for i in range(3)] for j in range(3)]
    for a in (A0,A5):require(inner3(a,a)==one,'unit reconstructed anchors')
    require(inner3(A0,A5)==g(T) and inner3(A0,We)==g(T) and inner3(A5,We)==g(T),
            'common-neighbor reflection hypotheses')
    require(inner3(A0,Ue)==g(T) and inner3(A5,Ve)==g(T), 'retained anchor contacts')
    require(inner3(A0,Ve)==g(l0) and inner3(A5,Ue)==g(l0),'opposite anchor products')
    Z=[g(r)*(a+b)-c for a,b,c in zip(A5,We,A0)]
    require(inner3(Z,Z)==one and inner3(Z,We)==g(T) and inner3(Z,A5)==g(T),
            'other lower-boundary common neighbor')
    choices={'A0':(T,l0),'other':(r*(l0+k)-T,r*(T+k)-l0)}
    lower={'format':1,'domain':['14/25','593/1000'],'coefficient_domain':'Q(t)[q]',
           'selector_pair':[5,12],'l0':encode(l0),'boundary_products':{},'resultants':{}}
    for name,(uz,vz) in choices.items():
        target=A0 if name=='A0' else Z
        require(inner3(Ue,target)==g(uz) and inner3(Ve,target)==g(vz),'both lower-boundary products')
        E=dot(un,B[12])-g(uz)*L
        vectors=(un,B[10],B[12]);rhs=(g(k)*L,g(T),g(vz))
        G=[[dot(a,b) for b in vectors] for a in vectors]
        P=det([row+[rhs[i]] for i,row in enumerate(G)]+[list(rhs)+[one]])
        lower['boundary_products'][name]={'U_B12':encode(uz),'V_B12':encode(vz)}
        lower['resultants'][name]=pair(E,P)
    # Verify the generic critical-vertex identity coefficient by coefficient.
    a,b,c=sp.symbols('a b c');rr=2*t/(1+t)
    determinant=1-t*t-a*a-b*b+2*t*a*b
    adjugate_sum=3-a*a-b*b-t*t+2*a*b-2*t+2*(t-1)*(a+b)
    numerator=t*t*adjugate_sum-determinant
    norm_equation=(1-t*t)*(a*a+b*b+c*c)-2*t*(1-t)*(a*b+a*c+b*c)-(1-t)**2*(1+2*t)
    identity=sp.cancel(numerator-(1-t*t)*(c-t)*(rr*(a+b)-c-t)-norm_equation)
    require(sp.Poly(identity,a,b,c,t).is_zero,'critical identity modulo the unit norm equation')
    return {'format':1,'authoring_agent':'six-tammes-2','role':'researcher','critical':critical,'lower':lower}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--generate',type=Path);args=parser.parse_args()
    start=time.monotonic();data=derive()
    if args.generate:args.generate.write_text(json.dumps(data,sort_keys=True)+'\n')
    else:
        expected=json.loads((HERE/'certificate.json').read_text())
        if data!=expected:raise ValueError('regenerated complete geometric certificate differs')
    print(json.dumps({'status':'GEOMETRY_REDERIVED','quadratic_quartic_resultants':4,
                      'norm_identity':True,'generated':bool(args.generate)} ,sort_keys=True))
