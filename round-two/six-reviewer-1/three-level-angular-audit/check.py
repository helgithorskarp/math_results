#!/usr/bin/env python3
"""Independent complete three-level angular audit; standard library, no research imports."""
from fractions import Fraction as F
import argparse,hashlib,json,pathlib
checks=[]
def need(v,label):
 if not v:raise ValueError(label)
 checks.append(label)
def rejects(fn,label):
 try:fn()
 except ValueError:return label
 raise ValueError("undetected mathematical damage: "+label)
def trim(p):
 p=list(p)
 while len(p)>1 and p[-1]==0:p.pop()
 return p or [F(0)]
def add(a,b):
 out=[F(0)]*max(len(a),len(b))
 for j,v in enumerate(a):out[j]+=v
 for j,v in enumerate(b):out[j]+=v
 return trim(out)
def scale(p,c):return trim([v*c for v in p])
def mul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for j,x in enumerate(a):
  for k,y in enumerate(b):out[j+k]+=x*y
 return trim(out)
def div(a,b):
 if b==[0]:raise ValueError('polynomial division by zero')
 r=trim(a);q=[F(0)]*max(1,len(r)-len(b)+1)
 while len(r)>=len(b) and r!=[0]:
  j=len(r)-len(b);v=r[-1]/b[-1];q[j]+=v;r=add(r,[F(0)]*j+scale(b,-v))
 return trim(q),r
def gcd(a,b):
 while b!=[0]:a,b=b,div(a,b)[1]
 return scale(a,1/a[-1])
def derivative(p):return trim([j*v for j,v in enumerate(p)][1:])
def peval(p,x):
 s=F(0)
 for a in reversed(p):s=s*x+a
 return s
class R:
 def __init__(self,n=0,d=1):
  if isinstance(n,R):self.n,self.d=n.n,n.d;return
  n=trim(list(map(F,n)) if isinstance(n,(list,tuple)) else [F(n)])
  d=trim(list(map(F,d)) if isinstance(d,(list,tuple)) else [F(d)])
  if d==[0]:raise ValueError('rational function division by zero')
  g=gcd(n,d);n=div(n,g)[0];d=div(d,g)[0];self.n=scale(n,1/d[-1]);self.d=scale(d,1/d[-1])
 def __add__(self,x):
  if not isinstance(x,(R,int,F,str,list,tuple)):return NotImplemented
  x=R(x);return R(add(mul(self.n,x.d),mul(x.n,self.d)),mul(self.d,x.d))
 __radd__=__add__
 def __neg__(self):return R(scale(self.n,-1),self.d)
 def __sub__(self,x):
  if not isinstance(x,(R,int,F,str,list,tuple)):return NotImplemented
  return self+-R(x)
 def __rsub__(self,x):return R(x)+-self
 def __mul__(self,x):
  if not isinstance(x,(R,int,F,str,list,tuple)):return NotImplemented
  x=R(x);return R(mul(self.n,x.n),mul(self.d,x.d))
 __rmul__=__mul__
 def __truediv__(self,x):
  if not isinstance(x,(R,int,F,str,list,tuple)):return NotImplemented
  x=R(x);return R(mul(self.n,x.d),mul(self.d,x.n))
 def __rtruediv__(self,x):return R(x)/self
 def __pow__(self,n):
  if n<0:return (1/self)**(-n)
  r=R(1)
  for _ in range(n):r*=self
  return r
 def __eq__(self,x):x=R(x);return self.n==x.n and self.d==x.d
 def diff(self):return R(add(mul(derivative(self.n),self.d),scale(mul(self.n,derivative(self.d)),-1)),mul(self.d,self.d))
 def at(self,t):return peval(self.n,t)/peval(self.d,t)
 def encoded(self):return {'numerator':list(map(str,self.n)),'denominator':list(map(str,self.d))}
 def infinity(self):
  if len(self.n)>len(self.d):raise ValueError('unbounded projective limit')
  return self.n[-1]/self.d[-1] if len(self.n)==len(self.d) else F(0)
t=R([0,1])
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),0) for j in range(len(b[0]))] for i in range(len(a))]
def solve(a,b):
 n=len(b);r=[list(a[j])+[b[j]] for j in range(n)]
 for j in range(n):
  q=next(i for i in range(j,n) if r[i][j]!=0);r[j],r[q]=r[q],r[j];pivot=r[j][j];r[j]=[x/pivot for x in r[j]]
  for i in range(n):
   if i!=j:
    c=r[i][j];r[i]=[x-c*y for x,y in zip(r[i],r[j])]
 return [r[j][-1] for j in range(n)]
def sturm(p):
 seq=[trim(p),derivative(p)]
 while seq[-1]!=[0]:
  rem=div(seq[-2],seq[-1])[1]
  if rem==[0]:break
  seq.append(scale(rem,-1/abs(rem[-1])))
 return seq
def variations(seq,x):
 signs=[]
 for p in seq:
  if x=='-inf':v=p[-1]*(-1)**(len(p)-1)
  elif x=='+inf':v=p[-1]
  else:v=peval(p,x)
  if v:signs.append(1 if v>0 else -1)
 return sum(a!=b for a,b in zip(signs,signs[1:]))
def imul(a,b):
 z=[x*y for x in a for y in b];return min(z),max(z)
def ipoly(p,I):
 r=(F(0),F(0))
 for c in reversed(p):r=imul(r,I);r=(r[0]+c,r[1]+c)
 return r
def interval(r,I):
 a,b=ipoly(r.n,I),ipoly(r.d,I)
 if b[0]<=0<=b[1]:raise ValueError('interval denominator contains zero')
 return imul(a,tuple(sorted((1/b[0],1/b[1]))))
# Active quotient: z^2-T*z+B=0, coefficient arithmetic in Q(t).
class A:
 def __init__(self,T,B,a=0,b=0):self.T,self.B,self.a,self.b=T,B,R(a),R(b)
 def coerce(self,x):return x if isinstance(x,A) else A(self.T,self.B,x)
 def __add__(self,x):x=self.coerce(x);return A(self.T,self.B,self.a+x.a,self.b+x.b)
 __radd__=__add__
 def __neg__(self):return A(self.T,self.B,-self.a,-self.b)
 def __sub__(self,x):return self+-self.coerce(x)
 def __rsub__(self,x):return self.coerce(x)+-self
 def __mul__(self,x):
  x=self.coerce(x);return A(self.T,self.B,self.a*x.a-self.B*self.b*x.b,self.a*x.b+self.b*x.a+self.T*self.b*x.b)
 __rmul__=__mul__
 def inverse(self):
  norm=self.a*self.a+self.T*self.a*self.b+self.B*self.b*self.b
  return A(self.T,self.B,(self.a+self.T*self.b)/norm,-self.b/norm)
 def __truediv__(self,x):return self*self.coerce(x).inverse()
 def __rtruediv__(self,x):return self.coerce(x)*self.inverse()
 def __pow__(self,n):
  r=self.coerce(1)
  for _ in range(n):r*=self
  return r
 def trace(self):return 2*self.a+self.T*self.b

def block_ratio(m,n,k):
 levels=[t,R(1),-(m*t+n)/k];sizes=[m,n,k]
 G=[[F(1,m)+F(1,k),F(1,k)],[F(1,k),F(1,n)+F(1,k)]]
 B=[[levels[0]/m+levels[2]/k,levels[2]/k],[levels[2]/k,levels[1]/n+levels[2]/k]]
 Gi=[[F(m*(n+k),8),-F(m*n,8)],[-F(m*n,8),F(n*(m+k),8)]]
 mat=mm(Gi,B);b=[m*t,R(n)];Gb=[sum(G[i][j]*b[j] for j in range(2)) for i in range(2)]
 N=sum(Gb[j]*b[j] for j in range(2));S3=sum(s*v**3 for s,v in zip(sizes,levels));S4=sum(s*v**4 for s,v in zip(sizes,levels))
 T=mat[0][0]+mat[1][1];det=mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
 need(mm(Gi,G)==[[1,0],[0,1]],'complete block Gram inverse '+str(sizes));need(mm(G,mat)==[list(v) for v in zip(*mm(G,mat))],'complete block selfadjointness '+str(sizes))
 need(T==sum(levels),'full compression trace '+str(sizes));need(sum(s*v for s,v in zip(sizes,levels))==0,'balanced full chart '+str(sizes))
 need(N==sum(s*v*v for s,v in zip(sizes,levels)),'compression norm '+str(sizes))
 M1=sum(Gb[i]*mat[i][j]*b[j] for i in range(2) for j in range(2));need(M1==S3,'full compression first coupling moment '+str(sizes))
 gram=[[R(2),T],[T,T*T-2*det]];coeff=solve(gram,[N,M1]);eta=coeff[0]*N+coeff[1]*M1
 delta=S4-N*N/8;C=(N*N-eta)/delta
 need(mm(mat,mat)==[[T*mat[i][j]-(det if i==j else 0) for j in range(2)] for i in range(2)],'full compression closure '+str(sizes))
 return C,N,S3,S4,eta,T,det

def splitting(N,S3,S4,T,B,r):
 z=A(T,B,0,1);hp=2*z-T
 rho=(N*z+S3-N*T)/hp
 anum=r*(z-T)+r*r-N/8
 # Laurent coefficient of resolvent's epsilon2 term:
 # 2(1+[(z-T)r+r2-N/8]/h)^2/(z-r).
 knum=2*anum**2;kp=4*anum*(hp+r)
 rho2=kp/((z-r)*hp**2)-knum/((z-r)**2*hp**2)-2*knum/((z-r)*hp**3)
 eta2=(2*rho*rho2).trace();eta=(rho*rho).trace();delta=S4-N*N/8
 return ((4*N-eta2)*delta-(N*N-eta)*(12*r*r-N/2))/delta**2

def uniform_basis():
 ones=[F(1)]*8;s=ones[:4]+[-F(1)]*4
 P=[[F(int(i==j))-F(1,8) for j in range(8)] for i in range(8)]
 def diagonal(v):return [[v[i] if i==j else F(0) for j in range(8)] for i in range(8)]
 def mv(a,v):return [sum(a[i][j]*v[j] for j in range(8)) for i in range(8)]
 H0=mm(mm(P,diagonal(s)),P)
 need(mv(H0,s)==[0]*8,'uniform central eigenvector')
 basis=[[F(int(i==start)-int(i==j)) for i in range(8)] for start in [0,4] for j in range(start+1,start+4)]
 for j,v in enumerate(basis):
  need(sum(v)==0 and sum(a*b for a,b in zip(s,v))==0,'uniform complete tangent basis'+str(j))
  DH=mm(mm(P,diagonal(v)),P)
  need(mv(DH,s)==mv(H0,v),'uniform eigenvector differential'+str(j))
  need(sum(s[i]*mv(DH,s)[i] for i in range(8))==0,'uniform central eigenvalue differential'+str(j))
  need(mv(H0,v)==[a*b for a,b in zip(s,v)],'uniform cluster action'+str(j))
 G=[[sum(x*y for x,y in zip(v,w)) for w in basis] for v in basis]
 leakage=[[4*x for x in row] for row in G]
 need(leakage==[[F((8 if i==j else 4) if i//3==j//3 else 0) for j in range(6)] for i in range(6)],'uniform full six-dimensional leakage quadratic form')
 return {'dimension':6,'gram':[[str(x) for x in row] for row in G],'leakage_gram':[[str(x) for x in row] for row in leakage],'ratio_leading_constant':'16'}

def integer_matrix():
 u=list(map(F,[-64]*4+[75]*3+[31]));n=7
 G=[[F(1+int(i==j)) for j in range(n)] for i in range(n)]
 Gi=[[F(int(i==j))-F(1,8) for j in range(n)] for i in range(n)]
 B=[[u[-1]+(u[i] if i==j else 0) for j in range(n)] for i in range(n)]
 mat=mm(Gi,B);powers=[[[F(int(i==j)) for j in range(n)] for i in range(n)]]
 for k in range(1,9):powers.append(mm(powers[-1],mat))
 traces=[sum(a[j][j] for j in range(n)) for a in powers]
 b=u[:7];Gb=[sum(G[i][j]*b[j] for j in range(n)) for i in range(n)]
 moments=[sum(Gb[i]*a[i][j]*b[j] for i in range(n) for j in range(n)) for a in powers[:5]]
 gram=[[traces[i+j] for j in range(4)] for i in range(4)]
 co=solve(gram,moments[:4]);closure=solve(gram,traces[4:8])
 need(powers[4]==[[sum(closure[k]*powers[k][i][j] for k in range(4)) for j in range(n)] for i in range(n)],'benchmark complete four-dimensional polynomial algebra')
 need(peval(co,-64)==0 and peval(co,75)==0,'benchmark all repeated spectral masses vanish')
 for block in [range(4),range(4,7)]:
  for j in list(block)[1:]:
   v=[F(int(i==block.start)-int(i==j)) for i in range(7)]
   need([sum(mat[i][h]*v[h] for h in range(7)) for i in range(7)]==[u[block.start]*x for x in v] and sum(Gb[i]*v[i] for i in range(7))==0,'benchmark original repeated-block eigenspace'+str(j))
 eta=sum(co[i]*moments[i] for i in range(4));N=sum(v*v for v in u);S4=sum(v**4 for v in u);X=S4/N**2;e=eta/N**2;C=(1-e)/(X-F(1,8));defect=e-1+24*(X-F(1,8))
 need(N==34220 and S4==162954260,'literal benchmark original moments')
 need(eta==F(63435273160,83),'literal benchmark full-compression spectral square')
 need(X==F(8147713,58550420) and e==F(1585881829,2429842430),'literal benchmark normalized invariants')
 need(C==F(27899524,1137183)>F(49,2),'literal benchmark constant above49/2')
 need(defect==-F(18365743,2429842430)<0,'literal benchmark disproves coefficient24')
 return {'norm':str(N),'fourth_moment':str(S4),'eta_raw':str(eta),'X':str(X),'eta':str(e),'C':str(C),'defect24':str(defect),'trace_moments':list(map(str,traces)),'coupling_moments':list(map(str,moments)),'minimal_polynomial_closure':list(map(str,closure)),'dephasing_coefficients':list(map(str,co))}

def generate():
 ratios={};parts=[(4,3,1),(4,2,2),(5,2,1),(3,3,2),(6,1,1)]
 for p in parts:ratios[p]=block_ratio(*p)
 expected={
 (4,3,1):8*(t-1)**2*(5*t+3)**2/((15*t*t+24*t+10)*(35*t*t+38*t+11)),
 (4,2,2):8*(t-1)**2*(3*t+1)**2/((3*t*t+4*t+2)*(9*t*t+2*t+1)),
 (5,2,1):20*(t-1)**2*(3*t+1)**2*(5*t+3)**2/((21*t*t+22*t+6)*R([27,260,1010,1700,1035])),
 (3,3,2):6*(t-1)**2*(3*t+5)**2*(5*t+3)**2/((5*t*t+8*t+5)*(5*t*t+14*t+13)*(13*t*t+14*t+5)),
 (6,1,1):4*(t-1)**2*(3*t+1)**2*(7*t+1)**2/((28*t*t+18*t+3)*R([1,12,118,492,721]))}
 allparts=[]
 for m in range(1,9):
  for n in range(1,m+1):
   k=8-m-n
   if 1<=k<=n:allparts.append((m,n,k))
 need(set(allparts)==set(parts),'complete multiplicity partition coverage')
 record={};rootcounts={}
 for p,values in ratios.items():
  C=values[0];ds=sturm(C.d);need(variations(ds,'-inf')==variations(ds,'+inf') and peval(C.d,0)>0,'all-real denominator strictly positive '+str(p));need(C==expected[p],'generic matrix-derived ratio '+str(p));record[str(p)]=C.encoded()
  gap=16-C
  if p not in [(4,3,1),(4,2,2)]:
   seq=sturm(gap.n);v=[variations(seq,x) for x in ['-inf','+inf']];need(v[0]==v[1] and peval(gap.n,0)>0,'all-real strict16 '+str(p));rootcounts[str(p)]=v
  elif p==(4,2,2):need(gap==24*(t+1)**2*(15*t*t+2*t+1)/((3*t*t+4*t+2)*(9*t*t+2*t+1)),'422 exact upper16 square')
  record[str(p)]['infinity']=str(C.infinity())
 C,N,S3,S4,eta,T,B=ratios[(4,3,1)];Q=[F(x) for x in [746,4737,11175,11695,4575]];d=(15*t*t+24*t+10)*(35*t*t+38*t+11)
 need(C.diff()==16*(t-1)*(5*t+3)*R(Q)/(d*d),'all-parameter stationary factorization')
 seq=sturm(Q);need(variations(seq,'-inf')-variations(seq,'+inf')==2,'exact two real stationary roots')
 Ia=(F(-853410556973738,10**15),F(-853410556973736,10**15));Ib=(F(-443370119245,10**12),F(-443370119244,10**12))
 for name,I in [('alpha',Ia),('beta',Ib)]:need(variations(seq,I[0])-variations(seq,I[1])==1,'isolated '+name)
 need(C.at(1)==0 and C.at(F(-3,5))==0 and C.infinity()==F(8,21),'all remaining stationary/projective values')
 beta=interval(C,Ib);need(4<beta[0]<=beta[1]<5,'beta below sharp value')
 for _ in range(40):
  mid=sum(Ia)/2
  if peval(Q,mid)>0:Ia=(mid,Ia[1])
  else:Ia=(Ia[0],mid)
 need(peval(Q,Ia[0])>0>peval(Q,Ia[1]),'refined alpha exact sign bracket')
 val=interval(C,Ia);need(F('24.53389668')<val[0]<=val[1]<F('24.53389670'),'sharp constant rational enclosure')
 cp=[F(x) for x in [587202560,-103317504,-7974720,-50108,20667]]
 rf=R(0)
 for a in reversed(cp):rf=rf*C+a
 need(div(rf.n,Q)[1]==[0],'independent constant quartic divisibility')
 cpseq=sturm(cp);need(variations(cpseq,F('24.53389668'))-variations(cpseq,F('24.53389670'))==1,'constant quartic unique real root in enclosure')
 L4=splitting(N,S3,S4,T,B,t);L3=splitting(N,S3,S4,T,B,R(1))
 pred4=4*R([12684,103380,366599,751299,993954,872170,470475,117375])/(3*(t+1)*d*d)
 pred3=4*R([42424,326238,1074965,2064611,2726970,2646100,1685625,496875])/(9*(t+1)*d*d)
 need(L4==pred4,'independent full-resolvent fourfold splitting')
 need(L3==pred3,'independent full-resolvent threefold splitting')
 Fpp=16*(t-1)*(5*t+3)*R(derivative(Q))/(d*d) # exact at alpha, where Q=0
 b4=-N*L4/2;b3=-N*L3/2;b0=-N*N*Fpp/192
 curvature={label:{'rational_function':r.encoded(),'enclosure':list(map(str,interval(r,Ia)))} for label,r in [('fourfold',b4),('threefold',b3),('block_constant',b0)]}
 for label,lo,hi in [('fourfold','340.462200','340.462201'),('threefold','891.770149','891.770150'),('block_constant','354.625092','354.625093')]:
  I=tuple(map(F,curvature[label]['enclosure']));need(F(lo)<I[0]<I[1]<F(hi),'normalized-sphere curvature '+label)
 need(interval(b4,Ia)[1]<min(interval(b3,Ia)[0],interval(b0,Ia)[0]),'fourfold is uniquely least stable tangent type')
 need(interval(-L4,Ia)[0]>0 and interval(-L3,Ia)[0]>0 and interval(-Fpp,Ia)[0]>0,'all tangent blocks strictly stable')
 # Sharp local-transition boundary and differentiability obstruction at uniform.
 need(C.diff().at(-1)==64,'nonzero uniform chart derivative64')
 gap_uniform=(S4-N*N/8)/(N*N)*(C-16)
 for order in range(3):
  expr=gap_uniform
  for _ in range(order):expr=expr.diff()
  need(expr.at(-1)==0,'uniform Jminus16 vanishes order'+str(order))
 need(gap_uniform.diff().diff().diff().at(-1)/6==48,'uniform transition cubic coefficient48')
 record['stationary_factor']=C.diff().encoded();record['fourfold_splitting']=L4.encoded();record['threefold_splitting']=L3.encoded()
 # Complete uniform tangent basis and direct seven-dimensional benchmark.
 uniform=uniform_basis();integer=integer_matrix()
 badQ=Q[:];badQ[0]+=1;badseq=sturm(badQ)
 damages=[rejects(lambda:need(C+1==expected[(4,3,1)],'damaged complete ratio'),'generic ratio coefficient'),rejects(lambda:need(variations(badseq,F(-853410556973738,10**15))-variations(badseq,F(-853410556973736,10**15))==1,'damaged isolated quartic'),'stationary polynomial coefficient'),rejects(lambda:need(-L4==pred4,'damaged splitting sign'),'transverse curvature sign'),rejects(lambda:need(F(integer['norm'])==34221,'damaged benchmark norm'),'raw matrix normalization'),rejects(lambda:need(interval(-L4/2,Ia)[0]>340,'normalized sphere metric omitted'),'sphere metric factor'),rejects(lambda:need(C.diff().at(-1)==0,'false differentiable-uniform certificate'),'uniform smoothness claim')]
 return {'damage_controls':damages,'uniform_tangent':uniform,'integer_benchmark':integer,'uniform_nondifferentiability_chart_derivative':'64','uniform_Jminus16_cubic_coefficient':'48','agent':'six-reviewer-1','role':'independent mathematical reviewer','checks':list(checks),'ratios':record,'sextic_sturm_variations':rootcounts,'alpha_enclosure':list(map(str,Ia)),'sharp_constant_enclosure':list(map(str,val)),'beta_value_enclosure':list(map(str,beta)),'local_normalized_curvatures':curvature}
def author_bridge(r,author):
 a=author['records'];count=0
 def eq(x,y,label):
  nonlocal count
  if x!=y:raise ValueError('author data bridge: '+label)
  count+=1
 for p in [(4,3,1),(4,2,2),(5,2,1),(3,3,2),(6,1,1)]:
  key=str(p);v=r['ratios'][key];eq({n:v[n] for n in ['numerator','denominator']},a[key+' universal ratio identity'],key+' full ratio')
  eq(v['infinity'],a[key+' infinite chart limit'],key+' projective infinity')
 eq(r['ratios']['stationary_factor'],a['stationary factor identity'],'full derivative')
 for field,label in [('fourfold_splitting','fourfold block splitting identity'),('threefold_splitting','threefold block splitting identity')]:eq(r['ratios'][field],a[label],label)
 b=r['integer_benchmark'];eq([b['norm'],b['fourth_moment']],a['integer witness moments'],'raw moments');eq(b['eta_raw'],a['integer witness unnormalized eta'],'raw spectral square');eq([b['X'],b['eta']],a['integer witness normalized X and eta'],'normalized invariants');eq(b['C'],a['integer witness ratio'],'benchmark ratio');eq(b['defect24'],a['integer witness defect24'],'benchmark negative defect')
 eq(r['uniform_tangent']['leakage_gram'],a['uniform full tangent leakage quadratic form'],'entire uniform six-dimensional Gram');eq(r['uniform_tangent']['ratio_leading_constant'],a['uniform ratio leading constant'],'uniform quotient16')
 return count

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--fixture',type=pathlib.Path,default=pathlib.Path(__file__).with_name('expected.json'))
 parser.add_argument('--author',type=pathlib.Path)
 parser.add_argument('--write',action='store_true',help='development only: regenerate the independent full fixture')
 args=parser.parse_args()
 expected=None if args.write else json.loads(args.fixture.read_text())
 r=generate();text=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if args.write:args.fixture.write_text(text)
 elif r!=expected:raise ValueError('complete independent record differs from fixture')
 print(f"PASS: {len(r['checks'])} independent exact checks; {len(r['damage_controls'])} mathematical damages rejected.")
 print('Complete record SHA256: '+hashlib.sha256(text.encode()).hexdigest())
 print('Least local quadratic cost in (340.462200,340.462201); coefficient340 valid in an existential collar.')
 print('Uniform transition is locally maximal exactly for R<-16; R=-16 cubic saddle; quotient not differentiable at uniform.')
 if args.author:print(str(author_bridge(r,json.loads(args.author.read_text())))+' complete author records independently matched.')
if __name__=='__main__':main()
