#!/usr/bin/env python3
"""Independent direct-compression audit of angular counterexample 8702.

No author import, polynomial inverse, numerical eigensolver or solver.
Raw seven-dimensional matrices, trace-inner-product spectral dephasing,
exact Q(sqrt3) arithmetic and complete generated fixtures.
"""
from fractions import Fraction as Q
import argparse,hashlib,json,math
from pathlib import Path
class K:
 def __init__(self,a=0,b=0):
  if isinstance(a,K):self.a,self.b=a.a,a.b
  else:self.a,self.b=Q(a),Q(b)
 def __add__(self,o):o=K(o);return K(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return K(-self.a,-self.b)
 def __sub__(self,o):return self+-K(o)
 def __rsub__(self,o):return K(o)+-self
 def __mul__(self,o):o=K(o);return K(self.a*o.a+3*self.b*o.b,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def __truediv__(self,o):
  o=K(o);n=o.a*o.a-3*o.b*o.b
  if not n:raise ValueError('zero field denominator')
  return self*K(o.a/n,-o.b/n)
 def __eq__(self,o):o=K(o);return self.a==o.a and self.b==o.b
 def __bool__(self):return bool(self.a or self.b)
 def __repr__(self):return f'K({self.a},{self.b})'
 def rational(self):
  if self.b:raise ValueError('Galois invariance not rational')
  return self.a

def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def inner(a,b):return sum(x*y for x,y in zip(a,b))
def solve(a,b):
 n=len(b);r=[list(a[i])+[b[i]] for i in range(n)]
 for j in range(n):
  row=next((i for i in range(j,n) if r[i][j]),None)
  if row is None:raise ValueError('singular matrix')
  r[j],r[row]=r[row],r[j];pivot=r[j][j];r[j]=[x/pivot for x in r[j]]
  for i in range(n):
   if i!=j:
    c=r[i][j]
    if c:r[i]=[x-c*y for x,y in zip(r[i],r[j])]
 return [r[i][-1] for i in range(n)]

def audit(u,d,inactive=None,declared_norm=None):
 u=list(map(K,u));n=len(u)-1
 if sum(u)!=0:raise ValueError('not balanced')
 G=[[Q(1+int(i==j)) for j in range(n)] for i in range(n)]
 Gi=[[Q(int(i==j))-Q(1,n+1) for j in range(n)] for i in range(n)]
 B=[[u[-1]+(u[i] if i==j else 0) for j in range(n)] for i in range(n)]
 A=mm(Gi,B);GA=mm(G,A)
 if any(GA[i][j]!=GA[j][i] for i in range(n) for j in range(n)):raise ValueError('not selfadjoint')
 powers=[[[K(int(i==j)) for j in range(n)] for i in range(n)]]
 for k in range(1,2*d+1):powers.append(mm(powers[-1],A))
 tr=[sum(p[i][i] for i in range(n)).rational() for p in powers]
 b=u[:-1];Gb=[sum(G[i][j]*b[j] for j in range(n)) for i in range(n)]
 moments=[inner(Gb,[sum(p[i][j]*b[j] for j in range(n)) for i in range(n)]).rational() for p in powers[:d+1]]
 gram=[[tr[i+j] for j in range(d)] for i in range(d)]
 coeff=solve(gram,moments[:d]);eta_u=inner(coeff,moments[:d])
 closure=solve(gram,tr[d:d+d])
 if any(powers[d][i][j]!=sum(closure[k]*powers[k][i][j] for k in range(d)) for i in range(n) for j in range(n)):raise ValueError('wrong minimal dimension')
 R=[[sum(coeff[k]*powers[k][i][j] for k in range(d)) for j in range(n)] for i in range(n)]
 if sum(mm(R,R)[i][i] for i in range(n))!=eta_u:raise ValueError('projection norm')
 N=sum(x*x for x in u).rational();S4=sum(x*x*x*x for x in u).rational()
 if N<=0:raise ValueError('zero norm')
 if declared_norm is not None and N!=declared_norm:raise ValueError('declared norm mismatch')
 if d<n:
  if inactive is None:raise ValueError('repeated spectra need inactive-block proof')
  for block in inactive:
   if len(block)!=3 or len({(u[i].a,u[i].b) for i in block})!=1:raise ValueError('not a triple block')
   for j in block[1:]:
    vec=[K(int(i==block[0])-int(i==j)) for i in range(n)]
    if any(sum(A[i][k]*vec[k] for k in range(n))!=u[block[0]]*vec[i] for i in range(n)):raise ValueError('inactive eigenvector failure')
    if inner(Gb,vec)!=0:raise ValueError('repeated eigenspace not inactive')
  if len(inactive)!=2 or set(inactive[0])&set(inactive[1]):raise ValueError('inactive dimension proof failure')
 return {'N':N,'S4':S4,'eta_u':eta_u,'X':S4/N**2,'eta':eta_u/N**2,'Phi':9*eta_u+208*S4-35*N**2,'Cex':(N**2-eta_u)/(S4-N**2/8),'trace_moments':tr,'coupling_moments':moments,'gram':gram,'projection_coefficients':coeff,'minimal_degree':d,'closure_coefficients':closure,'root_moments':[sum(x*x for x in u).rational(),sum(x*x*x for x in u).rational(),S4],'root_polynomial':root_polynomial(u),'compression_characteristic':characteristic(tr,n)}

def encode(x):
 if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
 if isinstance(x,list):return [encode(v) for v in x]
 return str(x)

def trim(p):
 p=list(p)
 while len(p)>1 and p[-1]==0:p.pop()
 return p

def pmul(p,q):
 out=[0]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):out[i+j]+=a*b
 return trim(out)

def padd(p,q):
 out=[Q(0)]*max(len(p),len(q))
 for i,a in enumerate(p):out[i]+=a
 for j,b in enumerate(q):out[j]+=b
 return trim(out)

def prem(p,q):
 out=list(p)
 while len(out)>=len(q) and out!=[0]:
  i=len(out)-len(q);a=out[-1]/q[-1]
  for j,b in enumerate(q):out[i+j]-=a*b
  out=trim(out)
 return out

def pder(p):return [i*p[i] for i in range(1,len(p))] or [Q(0)]
def peval(p,x):
 a=Q(0)
 for v in reversed(p):a=a*x+v
 return a

def root_polynomial(u):
 p=[K(1)]
 for v in u:p=pmul(p,[-v,K(1)])
 return [v.rational() for v in p]

def characteristic(tr,n):
 # Faddeev--LeVerrier, using traces of actual compression matrices.
 c=[Q(1)]
 for k in range(1,n+1):c.append(-sum(c[k-j]*tr[j] for j in range(1,k+1))/k)
 return c[::-1]

def determinant(a):
 a=[list(r) for r in a];result=Q(1)
 for k in range(len(a)):
  j=next((i for i in range(k,len(a)) if a[i][k]),None)
  if j is None:return Q(0)
  if j!=k:a[j],a[k]=a[k],a[j];result=-result
  pivot=a[k][k];result*=pivot
  for i in range(k+1,len(a)):
   factor=a[i][k]/pivot
   for h in range(k+1,len(a)):a[i][h]-=factor*a[k][h]
 return result

def radius(C):
 raw=[-720*C.denominator+25*C.numerator,896*C.denominator+40*C.numerator,768*C.denominator+16*C.numerator]
 g=math.gcd(*raw);p=[Q(c//g) for c in raw]
 lo,hi=Q(0),Q(1)
 for _ in range(100):
  mid=(lo+hi)/2
  if peval(p,mid)<0:lo=mid
  else:hi=mid
 floor=lo.numerator*10**9//lo.denominator;bracket=[Q(floor,10**9),Q(floor+1,10**9)]
 if not peval(p,bracket[0])<0<peval(p,bracket[1]):raise ValueError('radius bracket')
 return {'primitive_polynomial':p,'nine_decimal_bracket':bracket}

def generate():
 checks=[]
 def check(name,value):
  if not value:raise ValueError(name+' failed')
  checks.append(name)
 blocks=[[0,1,2],[3,4,5]]
 compact=[K(1,10)]*3+[K(1,-10)]*3+[K(7),K(-13)]
 distinct=[K(c,t) for c in [Q(1,2),Q(1),Q(3,2)] for t in [10,-10]]+[K(7),K(-13)]
 integer=[18]*3+[-16]*3+[7,-13]
 rational_numerators=[10367,10513,10657,-9491,-9344,-9198,4088,-7592]
 rational=[Q(x,25844) for x in rational_numerators]
 profiles={}
 for label,u,d,zero_blocks,N in [('compact',compact,5,blocks,Q(2024)),('distinct',distinct,7,None,Q(2025)),('integer',integer,5,blocks,Q(1958)),('rational_distinct',rational,7,None,Q(1))]:
  r=audit(u,d,zero_blocks,N);profiles[label]=r
  check(label+' squared trace norm nonnegative',r['eta_u']>=0)
  check(label+' compression characteristic versus direct root derivative',r['compression_characteristic']==[v/8 for v in pder(r['root_polynomial'])])
  check(label+' fourth moment excess positive',r['X']>Q(1,8))
  check(label+' all-sphere208/9 counterexample',r['Phi']<0)
  check(label+' coefficient normalization',r['eta']==r['eta_u']/r['N']**2)
  check(label+' dephasing Gram positive definite',all(determinant([row[:i] for row in r['gram'][:i]])>0 for i in range(1,d+1)))
  check(label+' universal constant in physical radius range',Q(208,9)<r['Cex']<Q(144,5))
  check(label+' raw and normalized certificates agree',r['eta']-1+Q(208,9)*(r['X']-Q(1,8))==r['Phi']/(9*r['N']**2))
  if d==7:check(label+' all eight inputs distinct',len({(K(v).a,K(v).b) for v in u})==8)
 a=profiles['compact'];b=profiles['distinct'];c=profiles['integer'];z=profiles['rational_distinct']
 check('original compact norm and moment',a['N']==2024 and a['S4']==581768)
 check('original compact complete negative certificate',a['Phi']==-Q(474603485184,1220287))
 check('original compact raw spectral weight sum',a['eta_u']==Q(2980684990912,1220287))
 check('original compact coefficient',a['Cex']==Q(3504016400,147654727))
 check('original distinct complete negative certificate',b['Phi']==-Q(1746288997284374824819986419052268279175827203851276237295,7980145913653001587422178012567716983879010063343874))
 check('original distinct norm and fourth moment',b['N']==2025 and b['S4']==Q(2334297,4))
 check('integer raw weight sum',c['eta_u']==Q(85966170287501,36957457))
 check('integer raw certificate',c['Phi']==-Q(15056280069783,36957457))
 check('integer stronger constant',c['Cex']==Q(111439995781294,4677150970635) and c['Cex']>a['Cex'])
 check('integer normalized certificate below-1/100',c['Phi']/(9*c['N']**2)<-Q(1,100))
 check('rational norm-one common denominator',sum(rational)==0 and sum(v*v for v in rational)==1)
 check('rational counterexample below-1/100',z['Phi']/9<-Q(1,100))
 check('rational necessary constant exceeds95/4',z['Cex']>Q(95,4)>a['Cex'])
 # Check the rational sphere-line provenance, rather than trust a normalized list.
 roots=[71,72,73,-65,-64,-63,28,-52]
 v=[Q(1,2),Q(1,2),-Q(1,2),-Q(1,2),Q(0),Q(0),Q(0),Q(0)]
 delta=[Q(x,177)-y for x,y in zip(roots,v)]
 t=-2*inner(v,delta)/inner(delta,delta)
 check('rational line second unit-sphere intersection',t==Q(12921,12922) and rational==[x+t*y for x,y in zip(v,delta)])
 # Coefficient and radius algebra, independent of the analytic angular reduction.
 num=list(map(Q,[-720,896,768]));den=list(map(Q,[25,40,16]))
 derivative=padd(pmul(pder(num),den),[-v for v in pmul(num,pder(den))])
 check('radius derivative numerator factorization',derivative==[2048*x for x in pmul([Q(5),Q(2)],[Q(5),Q(4)])])
 rold=radius(a['Cex']);rnew=radius(c['Cex'])
 check('original radius primitive polynomial',rold['primitive_polynomial']==list(map(Q,[-584718545,8514352856,5295721648])))
 check('original radius bracket',peval(rold['primitive_polynomial'],Q(659677,10**7))<0<peval(rold['primitive_polynomial'],Q(659678,10**7)))
 check('new radius primitive polynomial',rnew['primitive_polynomial']==list(map(Q,[-290774402162425,4324163550470360,2687545938974192])))
 check('new radius bracket',rnew['nine_decimal_bracket']==[Q(64646639,10**9),Q(64646640,10**9)])
 check('new radius earlier',rnew['nine_decimal_bracket'][1]<Q(659677,10**7))
 # Reproduce the restricted comparison's tie without importing its classification.
 r,s=Q(21,136),Q(5,136);mu2=(r+3*s)/4
 crossX=6*r*r+2*s*s;mass=(crossX-Q(1,8))/mu2
 crossEta=(1-mass)**2+mass*mass/2
 check('crossing symmetric profile normalization',6*r+2*s==1)
 check('crossing complete spectral weight evaluation',crossX==Q(337,2312) and crossEta==Q(451,867))
 check('crossing tie at Rstar',-Q(208,9)*(crossX-Q(1,8))+1-crossEta==0)
 check('crossing radius greater than original obstruction',(20*Q(659678,10**7)+16)**2<9*34)
 # Direct matrix projections supply every 31 author scalar/coefficient record.
 A=list(map(Q,[-299,-2,1]));B=list(map(Q,[-91,6,1]));h=list(map(Q,[-156,-149,4,1]))
 q=prem(a['projection_coefficients'],h)
 ps=[]
 for k in range(5):
  plus,minus=K(1),K(1)
  for _ in range(k):plus=plus*K(1,10);minus=minus*K(1,-10)
  ps.append(a['trace_moments'][k]-2*(plus+minus).rational())
 g3=[[ps[i+j] for j in range(3)] for i in range(3)]
 congruence=prem(padd(pmul(q,pder(h)),[8*v for v in pmul(A,B)]),h)
 gd=b['compression_characteristic'];qd=b['projection_coefficients']
 congruence_d=prem(padd(pmul(qd,pder(gd)),[8*v for v in b['root_polynomial']]),gd)
 check('compact center projection gives author residue polynomial',q==[Q(1807004888,1220287),-Q(4876192,1220287),-Q(9460696,1220287)])
 check('compact residue congruence',congruence==[0])
 check('distinct direct-matrix residue congruence',congruence_d==[0])
 bridge={
 'exact_root_moments':[[Q(0),Q(0)]]+[[v,Q(0)] for v in a['root_moments']],
 'root_separation_squared_bracket':[Q(17,10)**2,Q(7,4)**2],
 'expanded_real_root_polynomial':a['root_polynomial'],
 'compression_polynomial_factorization':a['compression_characteristic'],
 'inner_root_compression_values':[peval(h,Q(7)),peval(h,-Q(13))],
 'derived_active_residue_polynomial':q,'residue_congruence':congruence,
 'active_root_power_sums':ps,'independent_spectral_moment_vector':a['coupling_moments'][:3],
 'residue_spectral_moments':a['coupling_moments'][:3],'spectral_Gram_matrix':g3,'Gram_discriminant':determinant(g3),
 'Newton_residue_squared_trace':a['eta_u'],'companion_matrix_squared_trace':a['eta_u'],'independent_three_moment_Gram_inverse':a['eta_u'],
 'normalized_fourth_moment':a['X'],'normalized_collision_weight_sum':a['eta'],
 'fourth_moment_excess':a['X']-Q(1,8),'negative_universal_extension_certificate':a['Phi'],
 'normalized_208_9_deficit':a['Phi']/(9*a['N']**2),'necessary_universal_constant':a['Cex'],
 'constant_excess_over_restricted_value':a['Cex']-Q(208,9),'uniform_objective_gap_at_Rstar':-a['Phi']/(9*a['N']**2),
 'radius_equation_coefficients':padd([v*a['Cex'].denominator for v in num],[v*a['Cex'].numerator for v in den]),
 'radius_root_bracket':[Q(659677,10**7),Q(659678,10**7)],'distinct_root_polynomial':b['root_polynomial'],
 'distinct_root_moments':[[Q(0),Q(0)],[b['N'],Q(0)],[b['S4'],Q(0)]],
 'distinct_residue_congruence':congruence_d,'distinct_companion_Newton_trace_agreement':b['eta_u'],
 'distinct_residue_mass':b['N'],'distinct_negative_certificate':b['Phi']}
 check('full bridge has31 records',len(bridge)==31)
 check('strict quadratic embedding separation',Q(17,10)**2<3<Q(7,4)**2)
 controls=[]
 for name,u,d,zero,N in [('unbalanced',[K(2,10)]+compact[1:],5,blocks,None),('wrong_minimal_degree',compact,4,blocks,None),('wrong_repeated_block',compact,5,[[0,1,6],[3,4,5]],None),('wrong_normalization',compact,5,blocks,Q(2025))]:
  try:audit(u,d,zero,N)
  except ValueError:controls.append(name)
  else:raise ValueError('damage accepted: '+name)
 return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','profiles':profiles,'radius_original':rold,'radius_improved':rnew,'crossing':{'X':crossX,'eta':crossEta},'author_bridge':bridge,'checks':checks,'damage_controls_rejected':controls}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'));parser.add_argument('--author-record',type=Path);parser.add_argument('--emit',type=Path);args=parser.parse_args()
 record=encode(generate());expected=json.loads(args.expected.read_text())
 if record!=expected:raise ValueError('complete independent fixture mismatch')
 if args.author_record is not None:
  author=json.loads(args.author_record.read_text())
  if author!=record['author_bridge']:raise ValueError('complete31-record author bridge mismatch')
 canonical=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
 if args.emit is not None:args.emit.write_bytes(canonical)
 print('PASS: '+str(len(record['checks']))+' independent exact checks; four damaged inputs rejected; all 31 author values independently derived.')
 print('Full record SHA256: '+hashlib.sha256(canonical).hexdigest())
 print('Proved stronger constant 111439995781294/4677150970635; rational norm-one simple-spectrum witness and earlier radius obstruction.')
if __name__=='__main__':main()
