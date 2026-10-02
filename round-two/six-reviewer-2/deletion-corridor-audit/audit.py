"""Independent exact polynomial and original-coordinate audit of9478.

Visible defining proof credited; new target programs/oracles not consulted.
Original affine/linear primitives reused unchanged from own9488 source.
Unbounded completeness is the written root/sign/Pell proof, not sampling.
"""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
import signal,json
from affine import parameters,matrices,table,repair,pair,quad
from linear import need,digest,canonical,mv

def alarm(*unused):raise TimeoutError('fixed60s mathematical phase guard; incomplete is not exclusion')
signal.signal(signal.SIGALRM,alarm)
signal.alarm(60)

# Sparse bivariate polynomial arithmetic; no symbolic package or evaluations.
def poly(v):return {(0,0):F(v)} if v else {}
def add(*terms):
 out={}
 for term in terms:
  for key,val in term.items():out[key]=out.get(key,F(0))+val
 return {key:val for key,val in out.items()if val}
def mul(a,b):
 out={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():out[i+k,j+l]=out.get((i+k,j+l),F(0))+v*w
 return {key:val for key,val in out.items()if val}
def scale(a,c):return mul(a,poly(c))
def power(a,n):
 out=poly(1)
 for unused in range(n):out=mul(out,a)
 return out
def evalp(a,x,y):return sum(v*x**i*y**j for(i,j),v in a.items())
def serial(a):return [[i,j,str(v)]for(i,j),v in sorted(a.items())]
def eq(a,b,why):need(a==b,why);return {'identity':why,'lhs':serial(a),'rhs':serial(b)}
x={(1,0):F(1)};y={(0,1):F(1)}
def e(q,k):return scale(add(power(q,2),mul(add(poly(13),scale(k,-6)),q),scale(power(k,2),2),scale(k,-10),poly(14)),F(1,2))
def b0(q,k):return scale(add(power(q,2),mul(add(poly(7),scale(k,-6)),q),scale(power(k,2),2),scale(k,-12),poly(8)),F(1,2))
def db(k):return add(scale(power(k,2),28),scale(k,-36),poly(17))
def pellreduce(a):
 out={}
 # Replace every p² by7u²+1 using exact polynomial division.
 for (i,j),v in a.items():
  powerpoly=power(add(scale(power(y,2),7),poly(1)),i//2)
  term=mul({(i%2,j):v},powerpoly);out=add(out,term)
 return out

def algebra():
 rec=[]
 rec.append(eq(add(scale(e(add(x,poly(-6)),y),2),scale(add(scale(y,19),poly(-18),scale(x,-3)),-2)),scale(b0(x,y),2),'root substitution before monotonicity'))
 rec.append(eq(add(e(x,y),scale(b0(x,y),-1)),add(scale(x,3),y,poly(3)),'e minus strict tail polynomial'))
 rec.append(eq(e(y,y),scale(add(scale(power(y,2),-3),scale(y,3),poly(14)),F(1,2)),'e at left domain endpoint'))
 rec.append(eq(b0(y,y),scale(mul(add(y,poly(-1)),add(scale(y,3),poly(8))),F(-1,2)),'strict B0 endpoint branch'))
 rec.append(eq(add(power(add(scale(y,6),poly(7)),2),scale(db(y),-1)),add(scale(power(y,2),8),scale(y,120),poly(32)),'rB below6k'))
 rec.append(eq(add(db(y),scale(power(add(scale(y,5),poly(-2)),2),-1)),mul(add(scale(y,3),poly(-13)),add(y,poly(-1))),'square comparison all k>=5'))
 lossnum=add(scale(mul(power(y,2),add(scale(y,6),poly(1))),16),scale(mul(power(add(y,poly(-1)),2),add(scale(y,6),poly(7))),16),scale(mul(mul(add(scale(y,6),poly(7)),add(scale(y,6),poly(1))),add(scale(y,5),poly(-9))),-1))
 rec.append(eq(lossnum,add(scale(power(y,3),12),scale(power(y,2),20),scale(y,269),poly(175)),'positive loss cubic'))
 p,u=x,y;k=add(u,poly(1));q=add(scale(u,3),p,poly(-5));DB=db(k)
 rec.append(eq(pellreduce(add(DB,scale(power(add(scale(p,2),poly(1)),2),-1))),scale(add(scale(u,5),poly(1),scale(p,-1)),4),'Pell lower root bracket'))
 rec.append(eq(pellreduce(add(power(add(scale(p,2),poly(3)),2),scale(DB,-1))),scale(add(scale(p,3),scale(u,-5),poly(1)),4),'Pell upper root bracket'))
 rec.append(eq(pellreduce(scale(e(q,k),2)),add(scale(u,15),scale(p,-3),poly(-3)),'Pell original e identity'))
 pn=add(scale(p,8),scale(u,21));un=add(scale(p,3),scale(u,8))
 rec.append(eq(add(power(pn,2),scale(power(un,2),-7)),add(power(p,2),scale(power(u,2),-7)),'Pell recurrence preserves norm'))
 cubic=add(scale(power(y,3),15),scale(power(y,2),-395),scale(y,-384),poly(-64))
 shifted=add(scale(power(add(y,poly(48)),3),15),scale(power(add(y,poly(48)),2),-395),scale(add(y,poly(48)),-384),poly(-64))
 need(all(v>0 for v in shifted.values()),'Pell lower-bound positive coefficients afteru48')
 rec.append({'identity':'50u² times the rational Q lower bound','polynomial':serial(cubic),'shift_u48':serial(shifted),'minimum_u':48})
 rad_e=add(scale(power(y,2),28),scale(y,-116),poly(113))
 # All coefficients in k=3+v, except the positive constant, prove positivity.
 rad_shift=add(scale(power(add(y,poly(3)),2),28),scale(add(y,poly(3)),-116),poly(113))
 need(all(v>0 for v in rad_shift.values()),'e discriminant positive on k>=3')
 rec.append({'identity':'e-root discriminant positive','polynomial':serial(rad_e),'shift_k3':serial(rad_shift)})
 return rec

def scalar(q,k):
 need(type(q)is int and type(k)is int and q>=max(4,k) and k>=3,'full unbounded scalar domain')
 P=parameters(q,k);gap=P['gap'];d=P['d'];ww=P['ww'];a=P['a0'];h=P['h']
 direct=P['e']-a*a/(q*gap)-k*(q-k)*ww*ww/(q*gap)-4*q*(k-1)**2/d
 need(direct==P['Q0']and gap>0 and d>0 and P['D4']>0 and P['c4']>0,'original scalar variance identity and positive denominators')
 B0=F(q*q+(7-6*k)*q+2*k*k-12*k+8,2);DB=28*k*k-36*k+17
 b=(6*k-7+isqrt(DB))//2
 return P,B0,b

def baseline():
 q,k=5,3;S,Z,C,D,R,U=matrices(q,k);non=S[1:];N=len(S)
 Y=[ [F(1)]*len(non),[F((A&7)==1 and(A&~7).bit_count()==1 and bool(A&Z))for A in non], [F((A&7)==1 and(A&~7).bit_count()==1 and not(A&Z))for A in non], [F(A&7 in [2,4,3,5]and(A&~7).bit_count()==1)for A in non] ]
 P,B,b=scalar(q,k)
 GU=[[pair(U,u,v)for v in Y]for u in Y];GD=[[pair(D,u,v)for v in Y]for u in Y];GR=[[pair(R,u,v)for v in Y]for u in Y];GC=[[pair(C,u,v)for v in Y]for u in Y]
 gap=P['gap'];az=P['az'];aw=P['aw'];d=P['d'];h=P['h']
 expected=[[P['e'],k*az,(q-k)*aw,4*q*(1-k)],[k*az,k*gap,0,0],[(q-k)*aw,0,(q-k)*gap,0],[4*q*(1-k),0,0,4*q*d]]
 need(GU==expected,'actual weighted four-vector upper Gram')
 need(GD==[[P['S'],k*h,(q-k)*h,4*q*h],[k*h,0,0,0],[(q-k)*h,0,0,0],[4*q*h,0,0,0]],'actual weighted perturbation Gram')
 need(not any(v for row in GR for v in row),'all repair Gram entries vanish')
 w=[a-F(29,155)*b-F(97,310)*c+F(10,77)*d for a,b,c,d in zip(*Y)]
 z=[F(1-int(bool(A&2))-int(bool(A&4))+int((A&7).bit_count()>=2))for A in non]
 need(not any(mv(C,z))and not any(mv(R,z)),'whole lower C0 and repair kernels')
 need(quad(D,z)==F(159,10)>0,'whole original lower orientation')
 need(quad(U,w)==F(-322737,23870)and quad(D,w)==F(939346,59675)>0 and quad(R,w)==0,'whole real parameter-independent cap obstruction')
 # Independent binary census and physical transports to every labeled deletion.
 allbase=[A for A in range(1<<8)if A.bit_count()<=2 or(A.bit_count()==3 and(A&7).bit_count()>=2 and not(A&7==6 and A&Z))]
 need(S==allbase and len(S)==50,'binary family including actual empty member')
 QQ=table(q,0);QQ1=table(q,1);transports=[];checked=0
 for chosen in combinations(range(3,8),k):
  rest=[j for j in range(3,8)if j not in chosen];perm=list(range(3))+list(chosen)+rest;ZZ=sum(1<<j for j in chosen)
  def tr(A):return sum(1<<perm[j]for j in range(8)if A>>j&1)
  actual=[A for A in range(1<<8)if A.bit_count()<=2 or(A.bit_count()==3 and(A&7).bit_count()>=2 and not(A&7==6 and A&ZZ))]
  need(sorted(tr(A)for A in S)==actual,'complete physical transported family')
  for i,A0 in enumerate(non):
   A=tr(A0);at=((A&7).bit_count(),(A&~7).bit_count())
   for j,B0 in enumerate(non):
    B=tr(B0);bt=((B&7).bit_count(),(B&~7).bit_count());key=tuple(sorted((at,bt)))
    c=F(3*q+3)if A==B else F(-1)if A&B else QQ[key]-1
    delta=F(0)if A==B or A&B else QQ1[key]-QQ[key];r=repair(A,B);upper=F(N*(A==B)-1)-c
    need([c,delta,r,upper]==[C[i][j],D[i][j],R[i][j],U[i][j]],'all four original transported entries');checked+=4
  transports.append({'Z_bits':ZZ,'family_sha256':digest(actual)})
 return {'q':q,'k':k,'N':N,'nonempty':len(non),'family':S,'original_matrix_positions':4*len(non)**2,'matrix_sha256':digest([C,D,R,U]),'Grams':{'C0':GC,'Delta':GD,'repair':GR,'U0':GU},'lower_z_delta':quad(D,z),'upper_w':{'U0':quad(U,w),'Delta':quad(D,w),'repair':quad(R,w)},'all_labeled_deletions':transports,'transported_original_entries':checked},(C,D,R,U,Y,z,w)

def pell():
 out=[];p,u=8,3
 for n in range(1,9):
  need(p*p-7*u*u==1,'exact Pell norm')
  k=u+1;q=3*u+p-5;P,B,b=scalar(q,k)
  need(b==3*u+p and q==b-5,'exact leftmost corridor order')
  need((2*p+1)**2<28*k*k-36*k+17<(2*p+3)**2,'exact irrational-root floor bracket')
  need(P['e']==F(15*u-3*p-3,2)and B<0,'Pell original e and failed positive-tail criterion')
  if n>=2:
   need(u>=48 and p>F(5,2)*u and p<=F(8,3)*u and q>=5*u,'Pell all-order rational brackets')
   need(P['gap']>=F(q*q,2)and P['d']>=F(q*q,2)and P['a0']<2*(u+2)*q and 0<P['ww']<4,'original Schur loss bounds')
   lb=F(3*u-79,10)-F(192,25*u)-F(32,25*u*u)
   need(P['Q0']>lb>0,'positive Q lower bound at every Pell calibration')
   orders=[]
   for qq in range(q,b+1):
    X,BB,bb=scalar(qq,k)
    need(X['e']>=P['e']and X['Q0']>lb>0 and BB<0,'all six actual scalar corridor orders')
    kap=min(F(1),X['Q0']/(4*(X['D4']+X['c4'])))
    Q=X['Q0']-kap*X['D4']-kap*kap*X['c4'];need(Q>=3*X['Q0']/4>0,'positive parameter passes scalar Schur test')
    orders.append({'q':qq,'B0':BB,'Q0':X['Q0'],'scalar_positive_kappa':kap,'Q_at_kappa':Q})
   need(len(orders)==6,'six integers survive these two criteria')
   out.append({'n':n,'p':p,'u':u,'k':k,'q_min':q,'b':b,'e_at_q_min':P['e'],'rigorous_lower_bound':lb,'six_orders':orders})
  else:need(P['Q0']<0,'first Pell pair excluded; cannot include n1')
  p,u=8*p+21*u,3*p+8*u
 return {'range':'all n>=2 by written proof; n2..8 calibration only','recurrence_initial':[8,3],'calibrations':out}

def controls(finite):
 C,D,R,U,Y,z,w=finite;rejected=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,ZeroDivisionError):rejected.append(name);return
  raise ValueError('semantic damage accepted: '+name)
 damaged=[row[:]for row in C];damaged[0][0]+=1
 reject('changed original lower diagonal',lambda:need(not any(mv(damaged,z)),'physical lower kernel'))
 reject('reversed lower perturbation orientation',lambda:need(quad([[-v for v in row]for row in D],z)>0,'lower positive'))
 damagedR=[row[:]for row in R];damagedR[0][0]+=1
 reject('repair dependence in upper dual',lambda:need(quad(damagedR,w)==0,'all-real t independence'))
 damagedY=[v[:]for v in Y];damagedY[1][next(i for i,v in enumerate(Y[1])if v)]=0
 reject('unweighted deletion-pair coordinate',lambda:need(quad(U,damagedY[1])==3*31,'full weighted Gram'))
 reject('wrong root substitution coefficient',lambda:eq(add(scale(e(add(x,poly(-6)),y),2),scale(add(scale(y,19),poly(-18),scale(x,-3)),-2)),add(scale(b0(x,y),2),scale(y,2)),'root identity'))
 reject('non-strict square tail endpoint',lambda:need(scalar(40,8)[1]>0,'B0 strict'))
 reject('corridor off by one',lambda:need((6*49-7+isqrt(28*49*49-36*49+17))//2==270,'correct exact floor'))
 reject('Pell first pair incorrectly included',lambda:need(scalar(12,4)[0]['Q0']>0,'n1 not in theorem'))
 reject('damaged Pell recurrence',lambda:need((8*127+20*48)**2-7*(3*127+8*48)**2==1,'Pell invariant'))
 reject('reversed Schur parameter sign',lambda:need(scalar(266,49)[0]['D4']<0,'decreasing necessary condition'))
 reject('wrong positive loss cubic',lambda:eq(add(scale(power(y,3),12),scale(power(y,2),20),scale(y,269),poly(175)),add(scale(power(y,3),12),scale(power(y,2),20),scale(y,268),poly(175)),'exact cubic'))
 reject('missing empty set in full family',lambda:need(49==50,'N includes empty'))
 return rejected

def main():
 alg=algebra();base,finite=baseline();samples=[]
 for k in [3,4,5,8,49,128,1000]:
  DB=28*k*k-36*k+17;b=(6*k-7+isqrt(DB))//2
  need(2*b-(6*k-7)>=0 and(2*b-(6*k-7))**2<=DB and(2*(b+1)-(6*k-7))**2>DB,'exact floor root branch')
  P,B,unused=scalar(b,k);PP,BP,unused=scalar(b+1,k)
  need(B<=0 and BP>0,'strict tail cutoff calibration')
  samples.append({'k':k,'DB':DB,'b':b,'B0_at_b':B,'B0_at_b_plus1':BP})
 need(scalar(4,3)[0]['e']==-1,'sole q4 endpoint')
 L4=F(128,31)+F(72,25);need(L4-7==F(7,775)>0,'k4 strict rational margin')
 record={'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','scope':'ordinary all-k root/sign proof plus original q5/k3 dual;9195 infinite constructive theorem imported; proved Pell criterion-width sharpness, not full feasibility','algebra':alg,'baseline':base,'strict_tail_calibrations':samples,'k4_margin':L4-7,'Pell':pell(),'semantic_rejections':controls(finite)}
 print(json.dumps(canonical(record),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
