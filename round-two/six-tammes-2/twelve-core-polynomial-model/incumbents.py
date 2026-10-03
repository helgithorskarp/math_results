"""Exact specialization controls, separate from generic polynomial reduction.

Only vectors, alternate_last and the distinguished root are used from INPUT.
Other archived metadata, including Gram permutations, are not proof premises.
"""
from fractions import Fraction as Q
from itertools import combinations
import field as f
from model import CORE,CONTACTS,PAIRS,make,stereographic,constraints
from polynomials import cross,dot
from schema import require

class F:
    def __init__(self,x=0):self.v=x if isinstance(x,tuple) else f.scalar(Q(x))
    @staticmethod
    def cv(x):return x if isinstance(x,F) else F(x)
    def __add__(self,x):return F(f.add(self.v,F.cv(x).v))
    __radd__=__add__
    def __neg__(self):return F(f.scale(self.v,-1))
    def __sub__(self,x):return self+-F.cv(x)
    def __rsub__(self,x):return F.cv(x)+-self
    def __mul__(self,x):return F(f.mul(self.v,F.cv(x).v))
    __rmul__=__mul__
    def __truediv__(self,x):return F(f.mul(self.v,f.inverse(F.cv(x).v)))
    def __rtruediv__(self,x):return F.cv(x)/self
    def __pow__(self,n):
        require(type(n)is int and n>=0,'nonnegative exact exponent')
        y=F(1);x=self
        while n:
            if n&1:y=y*x
            n//=2
            if n:x=x*x
        return y
    def __eq__(self,x):return self.v==F.cv(x).v
    def sign(self):return f.sign(self.v)

def determinant(M):
    return sum((M[0][j]*cross(M[1],M[2])[j] for j in range(3)),F())
def solve(M,rhs):
    d=determinant(M)
    out=[determinant([[rhs[i] if j==k else M[i][j] for j in range(3)] for i in range(3)])/d for k in range(3)]
    require(all(sum((M[i][j]*out[j] for j in range(3)),F())==rhs[i] for i in range(3)),'exact Cramer solve')
    return out
def rowH(v,t):return [(1-t)*x+t*sum(v,F()) for x in v]
def encode_added(x,t):
    anchor=dot(x,[F(1),F(),F()],t);d=1-anchor
    require(d.sign()>0 and (d-(1-t)).sign()>=0,'pole avoided by actual anchor packing')
    u,v=x[1]/d,x[2]/d
    T,A,R=stereographic(t,u,v)
    require(A.sign()>0 and all(T[i]/A==x[i] for i in range(3)),'exact stereographic inversion')
    require((10-u*u-v*v).sign()>0,'proved disk bound at incumbent')
    require(all((Q(16,5)-h).sign()>0 and (Q(16,5)+h).sign()>0 for h in (u,v)),'closed chart box contains incumbent')
    return T,A,(u,v)

def check_incumbents(data,s):
    t=F(f.T);lo,hi=map(Q,data['root_bracket'])
    require(Q(14,25)<lo<hi<Q(593,1000) and lo==f.LO and hi==f.HI and f.F==tuple(map(Q,s['root_quintic_for_controls'])),'exact control root convention in the full target band')
    require(f.evaluate(f.F,lo)<0<f.evaluate(f.F,hi) and f.interval(tuple(i*f.F[i] for i in range(1,6)))[0]>0,'isolated real root')
    V=[[F(f.readpoly(p)) for p in row] for row in data['vectors']]
    require(all(dot(x,x,t)==1 for x in V),'all reference vectors exactly unit')
    require(all((t-dot(V[i],V[j],t)).sign()>=0 for i,j in combinations(range(15),2)),'all original 105 reference comparisons')
    M=[[V[k][j] for k in (1,2,4)] for j in range(3)]
    require(determinant(M)==-1,'exact old/new anchor orientation')
    require(all(dot([M[k][i] for k in range(3)],[M[k][j] for k in range(3)],t)==(1 if i==j else t) for i in range(3) for j in range(3)),'isometric anchor change')
    B=[solve(M,v) for v in V]
    z=F(tuple(map(Q,s['exact_z0_coefficients'])))
    D=(1-t)**2*(1+2*t);q=-D*determinant([B[9],B[7],B[10]])
    require(q.sign()>0,'positive original radical orientation')
    C=1+D*z*z;w=(1+t)**2*C*q;m=make(t,z,w);Y=m['points'];O=m['Omega']
    require(O.sign()>0 and m['E'].sign()>0 and (6-w).sign()>0 and w.sign()>0,'cleared denominator and bounded positive root')
    require(w*w==m['root_squared'],'exact scaled radical equation')
    require((1-(1-t)**2*z*z).sign()>=0 and (2*m['G']-(1+t)**4*C*C).sign()>0,'both full-frame model predicates at incumbent')
    require((z+Q(5,2)).sign()>0 and (Q(5,2)-z).sign()>0,'finite core chart box')
    Oinv=1/O
    require(all(Y[i][j]*Oinv==B[i][j] for i in CORE for j in range(3)),'all twelve homogeneous coordinates decode to reference')
    require(all(dot(B[i],B[j],t)==t for i,j in CONTACTS),'all twenty literal reference contacts')
    qpoint=solve([rowH(V[i],t) for i in (8,9,11)],[t]*3)
    alternate=[F(f.readpoly(p)) for p in data['alternate_last']]
    require(dot(qpoint,qpoint,t)==1 and dot(alternate,alternate,t)==1,'both alternative fixtures exactly unit')
    units={'p3':B[3],'p13':B[13],'q':solve(M,qpoint),'p14':B[14],'c14':solve(M,alternate)}
    charts={name:encode_added(x,t) for name,x in units.items()}
    core_gaps=[t*O*O-dot(Y[i],Y[j],t) for i,j in PAIRS]
    require(all(x.sign()>=0 for x in core_gaps),'all thirty-three reference core polynomial inequalities')
    rows=[]
    for aname in ('p13','q'):
        for bname in ('p14','c14'):
            names=('p3',aname,bname);encoded=[charts[n] for n in names]
            gaps=list(core_gaps)
            for T,A,uv in encoded:
                require(dot(T,T,t)==A*A,'encoded unit identity at incumbent')
                for i in CORE:gaps.append(t*A*O-dot(T,Y[i],t))
            for j,k in combinations(range(3),2):
                T,A,_=encoded[j];U,Bden,_=encoded[k];gaps.append(t*A*Bden-dot(T,U,t))
            system=constraints(t,z,w,[row[2] for row in encoded])
            require([x for name,x in system['packing']]==gaps,'complete polynomial generator agrees with direct cleared comparisons')
            require(len(system['equalities'])==1 and all(x==0 for name,x in system['equalities']),'all generated equalities at incumbent')
            require(len(system['strict'])==2 and all(x.sign()>0 for name,x in system['strict']),'all generated strict predicates at incumbent')
            require(len(system['weak_domain'])==19 and all(x.sign()>=0 for name,x in system['weak_domain']),'all generated closed domain predicates at incumbent')
            improved=constraints(t,z,w,[row[2] for row in encoded],strict_improvement=True)
            require(improved['equalities']==system['equalities'] and improved['weak_domain']==system['weak_domain'] and improved['packing']==system['packing'] and improved['strict'][:-1]==system['strict'],'only exact strict improvement is appended')
            require(improved['strict'][-1][0]=='strict-improvement' and improved['strict'][-1][1]==0,'all incumbents fail strict improvement at exact equality, not bracket truncation')
            signs=[x.sign() for name,x in system['packing']]
            require(len(signs)==72 and all(x>=0 for x in signs),'all seventy-two polynomial packing inequalities in actual completion')
            rows.append({'added_points':list(names),'packing_inequalities_actually_checked':72,'closed_domain_inequalities_actually_checked':19,'strict_domain_inequalities_actually_checked':2,'radical_equalities_actually_checked':1,'all_generated_polynomials_actually_checked':94,'exact_strict_improvement_equality_control_checked':True,'zero_gaps':signs.count(0),'strict_gaps':signs.count(1),'decoded_added_units':3,'all_six_chart_bounds_strict':True})
    return {'exact_reference_core_points':12,'original_reference_comparisons':105,'reference_to_polynomial_coordinates':36,'alternative_units':2,'positive_completions_actually_checked':4,'packing_comparisons_in_four_completions':288,'all_generated_polynomials_in_four_completions':376,'cases':rows}
