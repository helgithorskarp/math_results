"""Fresh companion trace/remainder and Laurent quotient reconstruction.

No producer imports or expected input. Written defining mathematics exposed.
Coefficient domain is unlocalized QQ[B,E,F,G,J,p0,p1,p2,p3,p4,p5,C].
"""
import sys,pathlib,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
from fractions import Fraction as Fr
R,B,E,F,G,J,p0,p1,p2,p3,p4,p5,C=ring('B,E,F,G,J,p0,p1,p2,p3,p4,p5,C',QQ)
x=[B,E,F,G,J,p0,p1,p2,p3,p4,p5,C];A=R(QQ(-3,8));zero=R.zero;one=R.one

def need(ok,why):
    if not ok:raise ValueError(why)

def add(a,b):return [(a[i] if i<len(a) else zero)+(b[i] if i<len(b) else zero) for i in range(max(len(a),len(b)))]
def scale(a,c):return [z*c for z in a]
def mul(a,b):
    out=[zero]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):out[i+j]+=u*v
    return out

def deriv(a):return [a[i]*i for i in range(1,len(a))]
h=[J,G,F,E,B,A,zero,one];p=[p0,p1,p2,p3,p4,p5]

def companion(v):return [-h[0]*v[6]]+[v[i-1]-h[i]*v[6] for i in range(1,7)]
columns=[[one if i==j else zero for i in range(7)] for j in range(7)]
trace=[];power=[]
for k in range(13):
    trace.append(sum((columns[i][i] for i in range(7)),zero));power.append(list(columns[0]));columns=[companion(v) for v in columns]

def rho(a):
    need(len(a)<=len(power),'complete companion powers')
    return [sum((c*power[k][i] for k,c in enumerate(a)),zero) for i in range(7)]

def T(a):
    need(len(a)<=7,'normal representative before adjoint')
    out=[zero]*6
    for k,c in enumerate(a):
        if k:
            for j in range(k):out[k-1-j]+=c*trace[j]
            out[k-1]-=k*c
    return out
# Quotient extraction at infinity, separate from any polynomial long division.
f=[zero,8*J,4*G,R(QQ(8,3))*F,2*E,R(QQ(8,5))*B,R(QQ(4,3))*A,zero,one]
numerator=add(scale(f,8),mul(p,deriv(h)))
rev=[h[7-i] for i in range(8)];inv=[one]
for i in range(1,5):inv.append(-sum((rev[j]*inv[i-j] for j in range(1,min(i,7)+1)),zero))
Q=[sum((numerator[7+k+j]*inv[j] for j in range(5-k) if 7+k+j<len(numerator)),zero) for k in range(5)]
remainder=add(numerator,scale(mul(Q,h),-one));need(all(c==0 for c in remainder[7:]),'whole Laurent quotient upper cancellation')
O=add(add(mul(p,deriv(deriv(h))),mul(add(deriv(p),scale(Q,-one)),deriv(h))),mul(add([R(64)],scale(deriv(Q),-one)),h))
r2=rho(mul(p,p));rq=rho(mul(p,add(Q,scale(deriv(p),-one))))
K=add(add(scale(p,-16),scale(T(T(r2)),R(QQ(-1,4)))),scale(T(rq),R(QQ(1,4))))
O+= [zero]*max(0,11-len(O));K+=[zero]*max(0,7-len(K));need(all(c==0 for c in O[6:]),'ALL higher ODE rows vanish')
phi=O[:6]+add(K,[R(4),zero,-4*C,zero,zero,zero,zero]);need(len(phi)==13 and phi[-1]==0,'all thirteen canonical rows including zero')

def subst(poly,pairs):
    out=zero
    for powers,c in poly.items():
        term=R(c)
        for i,e in enumerate(powers):
            if e:term*=pairs.get(i,x[i])**e
        out+=term
    return out

def projected(pairs):return [subst(c,pairs) for c in phi]
quartic=projected({10:zero});cubic=projected({10:zero,9:zero});quadratic=projected({10:zero,9:zero,8:zero});even=projected({10:zero,9:zero,8:zero,6:zero})
qfull=projected({10:zero,8:zero,7:4+2*A*p4/3,6:4*B*p4/5})
evenB=[subst(c,{0:zero}) for c in even];evenBF=[subst(c,{0:zero,2:zero}) for c in even]
need(cubic[10]==R(QQ(3,2))*p3**2,'whole cubic K4')
need(quadratic[8]+4*C==2*p2*(p2-4),'whole quadratic K2')
need(quadratic[7]==R(QQ(3,4))*p1*(5*p2-8),'whole quadratic K1')
need(even[4]==-3*(5*p2-8)*B and evenB[2]==-5*(3*p2-8)*F and evenBF[0]==-7*(p2-8)*J,'all nonresonant odd rows')
need(quartic[11]==R(QQ(7,4))*p3*p4,'whole quartic K5')
need(qfull[7]+p4*qfull[4]/20==R(QQ(3,5))*p4*B*(A*p4-6),'undivided exceptional factor')
starD=R(QQ(3,8))-8*E;starP0=R(QQ(8,7))*starD-R(QQ(1,2))
need(subst(qfull[5],{9:R(-16)})==42*(p0-starP0),'whole exceptional O5')
need(subst(qfull[8]+4*C,{9:R(-16)})==48*p0-8,'whole exceptional K2')
drop=[]
for row,qrow in zip(phi,quartic):
    d=(row-qrow).exquo(p5) if row!=qrow else zero
    need(row-qrow==p5*d,'every full p5 difference quotient');drop.append(d)
# Finite nilpotent inverse of the resonance operator; no backward recurrence.
diag=[R(QQ(1,8*(i-6))) for i in range(6)]
H=[[zero]*6 for _ in range(6)]
for i in range(4):H[i][i+2]=-diag[i]*p0*(i+2)
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(6)),zero) for j in range(6)] for i in range(6)]
H2=mm(H,H);H3=mm(H2,H);need(all(c==0 for row in H3 for c in row),'complete nilpotent tail')
inverse=[[( (one if i==j else zero)+H[i][j]+H2[i][j])*diag[j] for j in range(6)] for i in range(6)]
operator=[[zero]*6 for _ in range(6)]
for i in range(6):
    operator[i][i]=R(8*(i-6))
    if i+2<6:operator[i][i+2]=p0*(i+2)
need(mm(operator,inverse)==[[one if i==j else zero for j in range(6)] for i in range(6)],'whole six-by-six exact resonance inverse')
invnorm=sum((abs(c) for row in inverse for z in row for c in z.values()),QQ.zero)
need(invnorm<1 and max((sum(e) for row in inverse for z in row for e in z),default=0)<=2,'proved coefficient-one-norm inverse floor M squared')
g=scale(deriv(h),R(QQ(1,7)))
cube=[(p0/8)**3,zero,3*(p0/8)**2,zero,3*p0/8,zero,one]
def ode(a):return add(mul([p0,zero,R(8)],deriv(a)),scale([zero]+a,-48))
need(all(c==0 for c in ode(cube)),'cube satisfies entire resonance ODE')
resonance=projected({10:zero,9:zero,8:zero,6:zero,7:R(8)})
need(resonance[:6]==scale(ode(g)[:6],7),'actual full-heptic resonance ODE')
diff=add(g,scale(cube,-one));need(diff[6]==0,'monic difference degree five')
rr=ode(diff)
need(all(c==0 for c in rr[7:]),'residual degree at most six; constant row retained')
need([sum((operator[i][j]*diff[j] for j in range(6)),zero) for i in range(6)]==rr[1:7],'inverse addresses full actual difference')

def degree(z):return max((sum(e) for e in z),default=0)
def gradnorm(z):return sum((abs(c)*sum(e) for e,c in z.items()),QQ.zero)
need(max(map(degree,phi))<=4 and max(map(gradnorm,phi))<10000,'complete raw segment gradient')
need(max(map(degree,qfull))<=4 and max(map(gradnorm,qfull))<10000,'complete projected segment gradient')

def record(z):return [[list(e),str(Fr(c.numerator,c.denominator))] for e,c in sorted(z.items())]
maps=dict(trace=trace,Q=Q,rho_p2=r2,rho_mixed=rq,O=O,K=K,Phi=phi,quartic=quartic,cubic=cubic,quadratic=quadratic,even=even,even_B=evenB,even_BF=evenBF,projected_quartic=qfull,p5_differences=drop,resonance=rr)
out=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',variables=[str(z) for z in x],domain='unlocalized QQ, A=-3/8',method='companion traces/power remainders; Laurent inverse quotient; nilpotent exact resonance inverse',maps={name:[record(z) for z in array] for name,array in maps.items()},resonance_inverse=[[record(z) for z in row] for row in inverse],resonance_inverse_total_abs_coefficient=str(invnorm),resonance_inverse_degree=2,full_raw_degree=max(map(degree,phi)),full_raw_gradient=str(max(map(gradnorm,phi))),full_projected_degree=max(map(degree,qfull)),full_projected_gradient=str(max(map(gradnorm,qfull))),full_raw_nonzero_terms=sum(len(z) for z in phi),higher_ODE_rows_all_zero=True,complete13rows=True)
print(json.dumps(out,sort_keys=True,separators=(',',':')))
