"""six-reviewer-3: independent global rank audit; credited owned9550 kernel.
Integer determinants use rational Gaussian elimination, modular polynomials
use symmetric-node Lagrange interpolation. No producer imports/fixtures.
"""
import json,hashlib
from fractions import Fraction as F
from math import gcd,lcm
from polys import Poly,cast,symbol,need
from pencil import audit as pencil
from certificates import trim,add,mul,scale,divrem,egcd

def load(record):
 terms={}
 for key,v in record.items():
  need(len(v)==2 and F(v[1])==0,'real polynomial coefficient')
  m=[]
  if key!='1':
   for x in key.split('*'):
    name,_,n=x.partition('^');m.append((name,int(n) if n else 1))
  terms[tuple(sorted(m))]=(F(v[0]),F(0))
 return Poly(terms)
def deg(p,name):return max((dict(k).get(name,0) for k in p.terms),default=-1)
def exactdiv(p,d):
 # Coefficient-wise division as univariates in x; no symbolic CAS.
 groups={}
 for k,v in p.terms.items():
  m=dict(k);n=m.pop('x',0);key=tuple(sorted(m.items()));a=groups.setdefault(key,[])
  while len(a)<=n:a.append(F(0))
  a[n]+=v[0]
 b=[d.coefficient('x',j).terms.get((),(F(0),F(0)))[0] for j in range(deg(d,'x')+1)]
 out={}
 for key,a in groups.items():
  q,rem=divrem(a,b);need(not rem,'entire exact x-factor division')
  for j,c in enumerate(q):
   if c:out[tuple(sorted(key+((('x',j),) if j else ())))]=(c,F(0))
 result=Poly(out);need(result*d==p,'entire divided product');return result

def integers(p):
 need(all(v[1]==0 and v[0].denominator==1 for v in p.terms.values()),'integer polynomial')
 return p

def cleared(w,V,d,e,s_power):
 out=cast(0)
 for j in range(e+1):out+=w.coefficient('E',j)*(-V)**j*d**(e-j)
 need(deg(w,'E')==e,'correct whole E degree')
 out=out.substitute({'B':symbol('q')*symbol('s')}).divide_monomial({'s':s_power})
 terms={}
 for k,v in out.terms.items():
  m=dict(k);n=m.pop('s',0);need(n%2==0,'whole even s exponents');m['x']=m.get('x',0)+n//2
  terms[tuple(sorted((a,b) for a,b in m.items() if b))]=v
 return Poly(terms)

def rcoeff(p):return [p.coefficient('r',j) for j in range(deg(p,'r')+1)]
def evalx(p,x,mod=None):
 value=F(0)
 for k,v in p.terms.items():
  need(all(name=='x' for name,_ in k),'univariate x evaluation');value+=v[0]*x**dict(k).get('x',0)
 if mod is None:need(value.denominator==1,'integer evaluation');return int(value)
 return (value.numerator*pow(value.denominator,-1,mod))%mod

def sylvester(p,q,x,mod=None):
 a=list(reversed([evalx(v,x,mod) for v in rcoeff(p)]));b=list(reversed([evalx(v,x,mod) for v in rcoeff(q)]));m,n=len(a)-1,len(b)-1
 return [[0]*j+a+[0]*(n-1-j) for j in range(n)]+[[0]*j+b+[0]*(m-1-j) for j in range(m)]

def detQQ(matrix):
 a=[[F(v) for v in row] for row in matrix];answer=F(1);n=len(a)
 for j in range(n):
  pivot=next((i for i in range(j,n) if a[i][j]),None)
  if pivot is None:return 0
  if pivot!=j:a[pivot],a[j]=a[j],a[pivot];answer=-answer
  z=a[j][j];answer*=z
  for i in range(j+1,n):
   t=a[i][j]/z
   for k in range(j+1,n):a[i][k]-=t*a[j][k]
   a[i][j]=0
 need(answer.denominator==1,'integer rational determinant');return int(answer)

def detmod(matrix,p):
 a=[[v%p for v in row] for row in matrix];answer=1;n=len(a)
 for j in range(n):
  pivot=next((i for i in range(j,n) if a[i][j]),None)
  if pivot is None:return 0
  if pivot!=j:a[pivot],a[j]=a[j],a[pivot];answer=-answer
  z=a[j][j];answer=answer*z%p
  for i in range(j+1,n):
   t=a[i][j]*pow(z,-1,p)%p
   for k in range(j+1,n):a[i][k]=(a[i][k]-t*a[j][k])%p
   a[i][j]=0
 return answer%p

def mtrim(a,p):return trim([int(x)%p for x in a])
def madd(a,b,p):return mtrim(add(a,b),p)
def mmul(a,b,p):return mtrim(mul(a,b),p)
def mscale(a,c,p):return mtrim(scale(a,c),p)
def mdiv(a,b,p):
 a=mtrim(a,p);b=mtrim(b,p);need(bool(b),'modular nonzero divisor');q=[0]*max(0,len(a)-len(b)+1)
 while a and len(a)>=len(b):
  k=len(a)-len(b);z=a[-1]*pow(b[-1],-1,p)%p;q[k]=z
  for j,v in enumerate(b):a[k+j]=(a[k+j]-z*v)%p
  a=mtrim(a,p)
 return mtrim(q,p),a

def megcd(a,b,p):
 a=mtrim(a,p);b=mtrim(b,p);u,v,uu,vv=[1],[],[],[1]
 while b:
  q,r=mdiv(a,b,p);a,b=b,r;u,uu=uu,madd(u,mscale(mmul(q,uu,p),-1,p),p);v,vv=vv,madd(v,mscale(mmul(q,vv,p),-1,p),p)
 need(len(a)==1,'whole modular coprimality');u=mscale(u,pow(a[0],-1,p),p);v=mscale(v,pow(a[0],-1,p),p)
 return u,v

def meval(a,x,p):
 y=0
 for c in reversed(a):y=(y*x+c)%p
 return y

def lagrange(nodes,values,p):
 # Full cardinal-product interpolation, independent of forward differences.
 prod=[1]
 for x in nodes:prod=mmul(prod,[-x,1],p)
 answer=[]
 for x,y in zip(nodes,values):
  basis,rem=mdiv(prod,[-x,1],p);need(not rem,'cardinal basis quotient');den=meval(basis,x,p);need(den!=0,'distinct field nodes')
  answer=madd(answer,mscale(basis,y*pow(den,-1,p),p),p)
 need(all(meval(answer,x,p)==y for x,y in zip(nodes,values)),'all Lagrange values');return answer

def newtonQQ(values):
 a=[F(v) for v in values];answer=[];basis=[F(1)]
 for n in range(len(values)):
  answer=add(answer,scale(basis,a[0]));a=[a[i+1]-a[i] for i in range(len(a)-1)]
  basis=scale(mul(basis,[-F(n),F(1)]),F(1,n+1))
 need(all(v.denominator==1 for v in answer),'entire integer determinant coefficients')
 return [int(v) for v in answer]

def audit():
 base=pencil();need(hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest()=='7afaf2e4aac5b52080b03d7e133eeb8f77f295ad8703f90c3406820916468f9c','complete owned matrix audit pinned');matrix=[[load(v) for v in row] for row in base['whole_matrix']];B,E,r,s,x=[symbol(k) for k in ('B','E','r','s','x')]
 A,L,C=map(list,zip(*matrix));w=[-F(1,192),0,0,F(7,384)*s,F(7,96)]
 alpha=sum((z*y for z,y in zip(w,A)),cast(0));beta=sum((z*y for z,y in zip(w,L)),cast(0));a=[z-y*alpha for z,y in zip(A,C)];b=[z-y*beta for z,y in zip(L,C)]
 checks={}
 def eq(name,left,right):need(left==right,name);checks[name]=cast(left).record()
 eq('global whole constant unit',sum((z*y for z,y in zip(w,C)),cast(0)),1)
 d=21120*(49*s*s+2);V=924672*B*r*s-848736*B*s**3+302976*B*s+3849440*r*r*s*s+219520*r*r-4602080*r*s**4+2603440*r*s*s+146880*r+1286250*s**6-1694385*s**4+403500*s*s+22860
 eq('whole E numerator',-3360*b[3],d*E+V)
 U=[matrix[0][j]-14*matrix[4][j] for j in range(3)];eq('whole reference C',U[2],-48*(7*s*s+4))
 wedges=[U[2]*matrix[i][j]-C[i]*U[j] for i,j in [(0,1),(1,1),(2,1),(0,0)]]
 cc=[cleared(z,V,d,e,pow_s) for z,e,pow_s in zip(wedges,[1,1,1,2],[1,0,1,0])]
 f=integers(exactdiv(cc[0]*F(3,64),7*x+4));g=integers(exactdiv(cc[1]*F(-105,16),7*x+4));f2=integers(exactdiv(cc[2]*F(315,8),7*x+4));A0=integers(cc[3]*F(63,8))
 need([len(z.terms) for z in [f,g,f2,A0]]==[16,23,28,66],'four complete term counts')
 h=f2-6*g;need(deg(f,'q')==deg(h,'q')==1,'both full affine q pivots')
 a1,b1=f.coefficient('q',1),f.coefficient('q',0);a2,b2=h.coefficient('q',1),h.coefficient('q',0)
 eq('stated whole first slope',a1,96*(4238080*r*r-10322760*r*x+2868096*r+3315879*x*x-3689028*x+479952))
 def clear(G,Fp):
  need(deg(G,'q')==2,'full quadratic degree');aa,bb=Fp.coefficient('q',1),Fp.coefficient('q',0);G0,G1,G2=[G.coefficient('q',j) for j in range(3)];z=G2*bb*bb-G1*aa*bb+G0*aa*aa
  eq('whole syzygy '+str(len(checks)),aa*aa*G-z,Fp*(aa*G2*symbol('q')+aa*G1-bb*G2));return z
 P5=integers(exactdiv((a1*b2-a2*b1)/17740800,49*x+2));P7=integers(exactdiv(clear(g,f)/-35481600,49*x+2));bh=integers(clear(g,h)/6209280000);bA=integers(clear(A0,f)/1561190400)
 need([(deg(z,'r'),deg(z,'x'),len(z.terms)) for z in [P5,P7,bh,bA]]==[(5,5,21),(7,7,36),(9,10,65),(9,11,75)],'four full elimination degrees and terms')
 # s=0 independently derived whole matrix identities, rational units.
 Epivot=-(10976*r*r+7344*r+1143)/2112;sl={'s':0,'E':Epivot}
 Q2=[2727,16296,24080];H2=[1875,7280,5488];P3=[157599,1459368,4606896,4934272];T5=[57863160,900559539,5524855776,16747763040,25150852608,15003349760]
 rp=lambda arr:sum((cast(v)*r**j for j,v in enumerate(arr)),cast(0))
 eq('s0 B-nonzero first necessary equation',b[0].substitute(sl),-F(8,45)*B*rp(Q2));eq('s0 B-nonzero second necessary equation',a[3].substitute(sl),-F(3,34496)*B*rp(H2))
 eq('s0 B-zero first necessary equation',b[1].substitute({**sl,'B':0}),-rp(P3)/9504);eq('s0 B-zero second necessary equation',a[0].substitute({**sl,'B':0}),F(7,60217344)*rp(T5))
 zero_units=[]
 for pp,qq in [(Q2,H2),(P3,T5)]:
  u,v=egcd(pp,qq);need(add(mul(u,pp),mul(v,qq))==[1],'s0 entire rational Bezout');zero_units.append({'P':pp,'Q':qq,'U':list(map(str,u)),'V':list(map(str,v))})
 # All85 rational-Gaussian determinant values; derive complete integer
 # polynomial, and derive P20 without reading any producer P20 coefficients.
 need(deg(P5,'r')==5 and deg(P7,'r')==7 and max(deg(z,'x') for z in rcoeff(P5)+rcoeff(P7))<=7,'fixed12by12 degree84 bound')
 values=[detQQ(sylvester(P5,P7,j)) for j in range(85)];res=newtonQQ(values);need(len(res)==36,'whole resultant degree35')
 need(all(sum(c*j**k for k,c in enumerate(res))==values[j] for j in range(85)),'all full integer polynomial values')
 S5=[1878249696897024,137517513338916480,-949012690531122084,-47045003408526384373,-516919826627115107546,4665265033450726317767]
 c=54398595580319162820682667735046723239077132589821466561740800
 divisor=[0]*5+scale(mul(S5,S5),c);P20,rem=divrem([F(z) for z in res],[F(z) for z in divisor]);need(not rem and len(P20)==21 and all(z.denominator==1 for z in P20),'entire derived degree20 integer factor');P20=[int(z) for z in P20]
 need(mul(divisor,P20)==res,'full characteristic-zero factorization')
 need(P20[0]==-5447729122472491706796885548483935511329357824 and P20[-1]==1682406513386732369627639529362524119993790686195129083280000000,'stated factor endpoints')
 mods=[]
 for target,factor,bound,degree,lead in [(bh,S5,140,50,225),(bA,P20,154,55,146)]:
  need(all(257%d for d in range(2,17)) and bound<257 and deg(P5,'r')+deg(target,'r')==14 and 14*max(deg(z,'x') for z in rcoeff(P5)+rcoeff(target))<=bound,'prime257/distinct-node whole determinant bound')
  nodes=list(range(-bound//2,bound//2+1));need(len(nodes)==bound+1,'complete symmetric node census')
  val=[detmod(sylvester(P5,target,n,257),257) for n in nodes];poly=lagrange(nodes,val,257);need(len(poly)==degree+1 and poly[-1]==lead,'full modular resultant degree/lead');need(factor[-1]%257!=0,'Gauss leading degree preserved')
  u,v=megcd(factor,poly,257);need(madd(mmul(u,factor,257),mmul(v,poly,257),257)==[1],'whole modular unit')
  mods.append({'bound':bound,'nodes':nodes,'values':val,'entire_determinant':poly,'integer_factor':factor,'U':u,'V':v,'whole_unit':[1]})
 return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','owned_matrix_regeneration_sha256':hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'whole_matrix':[[z.record() for z in row] for row in matrix],'whole_checks':checks,'four_cleared':{k:z.record() for k,z in zip(['f','g','f2','A0'],[f,g,f2,A0])},'elimination':{k:z.record() for k,z in zip(['P5','P7','bh','bA'],[P5,P7,bh,bA])},'s0_rational_units':zero_units,'integer_determinant_values':values,'entire_integer_resultant':res,'S5':S5,'derived_P20':P20,'constant_c':c,'full_modular_units':mods,'scope':'real rank>=2; complex rank>=2 whenever (49s^2+2)(7s^2+4)!=0; s=0 included; exact four exceptional s values retained'}

if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,separators=(',',':')))
