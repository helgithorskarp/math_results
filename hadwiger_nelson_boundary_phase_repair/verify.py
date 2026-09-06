"""Quadratic-tower boundary audit; imports no producer or parent code."""
from fractions import Fraction as Q
from itertools import combinations,product
from pathlib import Path
import argparse,copy,hashlib,json

def need(ok,msg):
 if not ok:raise ValueError(msg)
def kadd(a,b):return a[0]+b[0],a[1]+b[1]
def kmul(a,b):return a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def scale(a,b):return tuple(b*x for x in a)
def mul(a,b):
 # Real elements are A+eta B, A,B in Q(sqrt3), eta^2=2 sqrt3.
 A,B=a[:2],a[2:];C,D=b[:2],b[2:]
 return kadd(kmul(A,C),kmul((Q(0),Q(2)),kmul(B,D)))+kadd(kmul(A,D),kmul(B,C))
def sub(a,b):return add(a,neg(b))
ZERO=(Q(0),)*4;ONE=(Q(1),Q(0),Q(0),Q(0));SQRT3=(Q(0),Q(1),Q(0),Q(0));ETA=(Q(0),Q(0),Q(1),Q(0))
def ca(a,b):return add(a[0],b[0]),add(a[1],b[1])
def cn(a):return neg(a[0]),neg(a[1])
def cs(a,b):return ca(a,cn(b))
def cm(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def norm(a,b):
 x,y=cs(a,b);return add(mul(x,x),mul(y,y))
O=(ONE,ZERO);Z=(ZERO,ZERO);OMEGA=(scale(ONE,Q(1,2)),scale(SQRT3,Q(1,2)));U=[O]
for _ in range(5):U.append(cm(U[-1],OMEGA))
def coeff(a):return a[0],a[2],a[1]/2,a[3]/2
def key(z):return coeff(z[0]),coeff(z[1])
def encode(z):return [[[x.numerator,x.denominator] for x in coeff(a)] for a in z]
def decode(z):
 need(isinstance(z,list) and len(z)==2,'point shape');out=[]
 for axis in z:
  need(isinstance(axis,list) and len(axis)==4,'axis shape');values=[]
  for pair in axis:
   need(isinstance(pair,list) and len(pair)==2 and all(type(v)is int for v in pair) and pair[1]>0,'rational shape')
   x=Q(*pair);need([x.numerator,x.denominator]==pair,'reduced rational');values.append(x)
  a,b,c,d=values;out.append((a,2*c,b,2*d))
 return tuple(out)
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(raw(x)).hexdigest()
from functools import lru_cache
@lru_cache(None)
def sign(a):
 """Exact sign by rational isolating intervals for positive sqrt(3), eta."""
 if a==ZERO:return 0
 # Both nested square roots are isolated by rational dyadic bisection.
 s0,s1=Q(1),Q(2);e0,e1=Q(1),Q(2)
 def times(x,y):
  z=[a*b for a in x for b in y];return min(z),max(z)
 def by(c,x):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])
 while True:
  terms=[(a[0],a[0]),by(a[1],(s0,s1)),by(a[2],(e0,e1)),by(a[3],times((s0,s1),(e0,e1)))]
  lo,hi=sum(x[0] for x in terms),sum(x[1] for x in terms)
  if lo>0:return 1
  if hi<0:return -1
  sm=(s0+s1)/2
  if sm*sm<3:s0=sm
  else:s1=sm
  em=(e0+e1)/2
  if em**4<12:e0=em
  else:e1=em

def dot(v,w):return add(mul(v[0],w[0]),mul(v[1],w[1]))
def wedge(v,w):return sub(mul(v[0],w[1]),mul(v[1],w[0]))
@lru_cache(None)
def rot(v,k):return cm(v,U[k])
@lru_cache(None)
def sq(v):return dot(v,v)
@lru_cache(None)
def same_root(v,s,w,t):
 """Test substitution into both chord equations using dot products.

 For d=det(v,w), a=|w|^2-v.w, the first branch satisfies
 s*d*sqrt((4-|v|^2)/|v|^2)=a. The reverse equation fixes t.
 This uses neither coordinate root extraction nor the producer's Cramer test.
 """
 q,r=sq(v),sq(w);p=dot(v,w);d=wedge(v,w)
 if d==ZERO:return v==w and s==t
 a,b=sub(r,p),sub(q,p)
 if mul(mul(a,a),q)!=mul(mul(d,d),sub(scale(ONE,4),q)):return False
 sd=sign(d)
 return sign(a)==s*sd and sign(b)==-t*sd

def reconstruct():
 zeta=U[2];u=(scale(SQRT3,Q(1,2)),scale(ONE,Q(-1,2)))
 y=cm(u,(scale(sub(ONE,SQRT3),Q(1,2)),scale(ETA,Q(1,2))))
 z=cm(u,(scale(sub(ONE,SQRT3),Q(1,2)),scale(ETA,Q(-1,2))))
 D=[Z,U[4],cs(cn(O),y),ca(cn(zeta),z)]
 need(len(set(D))==4 and norm(D[0],D[1])==norm(D[2],D[3])==ONE,'paired distinct centres')
 mixed={cn(O),cn(zeta),cn(y),cs(U[4],y),z,ca(U[4],z)}
 need(len(mixed)==6,'six distinct mixed points')
 # Completeness: each of the four distinct centre pairs has precisely the
 # two distinct named points certified by unit norms; two circles have <=2.
 for a in range(2):
  for b in range(2,4):
   roots=[p for p in mixed if norm(p,D[a])==norm(p,D[b])==ONE]
   need(len(roots)==2,'complete cross-circle intersections')
 S=[set(),set()]
 for g in range(2):
  seed=[cs(D[2*g+1],D[2*g])]
  seed.extend(cs(p,D[h]) for p in mixed for h in (2*g,2*g+1) if norm(p,D[h])==ONE)
  S[g]={cm(v,r) for v in seed for r in U}
 V=sorted({ca(d,v) for h,d in enumerate(D) for v in S[h//2]},key=key)
 E=[(i,j) for i,j in combinations(range(len(V)),2) if norm(V[i],V[j])==ONE]
 ci=[V.index(d) for d in D];owners=[{h for h,d in enumerate(D) if norm(p,d)==ONE} for p in V]
 need(all(owners),'owned kernel points')
 need(all(cs(p,D[h]) in S[h//2] for p,own in zip(V,owners) for h in own if p not in D),'all owner directions in kernel sets')
 return D,S,V,E,ci,owners

def make_boundary(D,V,ci,owners):
 rows=[];stats={'candidate_circle_pairs':0,'empty_circle_pairs':0,'two_root_circle_pairs':0,'internal_root_incidences':0}
 for i,x in enumerate(V):
  if i in ci:continue
  groups={h//2 for h in owners[i]}
  for h,b in enumerate(D):
   if h//2 in groups:continue
   stats['candidate_circle_pairs']+=1
   v=cs(x,b);q=sq(v);need(sign(q)>0,'positive squared displacement')
   cls=sign(sub(scale(ONE,4),q));need(cls!=0,'no boundary tangencies for this instance')
   if cls<0:stats['empty_circle_pairs']+=1;continue
   stats['two_root_circle_pairs']+=1
   # Subtracting the two squared circle equations gives 2 v.w = q.
   inside=[]
   for point in V:
    w=cs(point,b)
    if sq(w)==ONE and scale(dot(v,w),2)==q:
     s=sign(wedge(v,w));need(s in (-1,1),'internal branch nonzero')
     inside.append(s)
   need(len(inside)==len(set(inside)),'one root per branch')
   stats['internal_root_incidences']+=len(inside)
   for s in (-1,1):
    if s not in inside:rows.append((i,h,s,v))
 return rows,stats

class Union:
 def __init__(self,n):self.p=list(range(n))
 def root(self,i):
  while self.p[i]!=i:i=self.p[i]
  return i
 def join(self,i,j):self.p[self.root(i)]=self.root(j)

def root_controls():
 # The chord for v=1 has roots omega and conjugate(omega).
 # Its 120-degree rotated chord shares precisely the first of these.
 v=O;w=U[2]
 cases=[(v,1,v,1,True),(v,1,v,-1,False),
        (v,1,cn(v),1,False),(v,1,w,-1,True),
        (v,-1,w,1,False),(w,-1,v,1,True)]
 for a,s,b,t,want in cases:need(same_root(a,s,b,t)==want,'hand-checkable chord control')
 return len(cases)

def audit(data,context=None):
 need(set(data)=={'schema','field','kernel_colour','boundary_direction_bits','point_sha256','edge_sha256','full_support_four_colourable','target_found'},'certificate keys')
 need(data['schema']==1 and type(data['schema'])is int and data['field']=='eta^4=12, eta>0','schema')
 need(data['full_support_four_colourable']is True and data['target_found']is False,'scope flags')
 if context is None:
  context=reconstruct();context=(*context,make_boundary(context[0],context[2],context[4],context[5]))
 D,S,V,E,ci,owners,(rows,stats)=context
 need(data['point_sha256']==digest(list(map(encode,V))) and data['edge_sha256']==digest(E),'exact graph hashes')
 c=data['kernel_colour'];need(type(c)is str and len(c)==len(V) and set(c)<={'0','1','2','3'},'kernel colour domain');col=list(map(int,c))
 need([col[i] for i in ci]==[2,3,0,1],'centre pins')
 need(all(col[i]!=col[j] for i,j in E),'kernel colour inequalities')
 cert=data['boundary_direction_bits'];need(type(cert)is list and len(cert)==len(rows),'complete boundary row count')
 for r,(i,h,s,v) in zip(cert,rows):
  need(type(r)is list and len(r)==4 and all(type(x)is int for x in r),'boundary row shape')
  need(r[:3]==[i,h,s] and r[3] in (0,1),'ordered boundary labels and bits')
  need(col[i]!=2*(h//2)+(r[3]^(h%2)),'external edge colour inequality')
 # Check ALL possible rotation equalities; no omitted class identification
 # can escape this audit. Bit values are phases at the actual directions.
 union=Union(len(rows));rotation_tests=0;equalities=0;parities=[0,0]
 for a,(i,h,s,v) in enumerate(rows):
  for b in range(a):
   j,k,t,w=rows[b]
   if h//2!=k//2:continue
   matches=[]
   for turn in range(6):
    rotation_tests+=1
    if same_root(v,s,rot(w,turn),t):matches.append(turn)
   need(len(matches)<=1,'unique sixth-root rotation')
   if matches:
    turn=matches[0];equalities+=1;parities[turn%2]+=1
    need(cert[a][3]^cert[b][3]==turn%2,'boundary orbit phase consistency')
    union.join(a,b)
 pinned={union.root(a) for a,(i,h,s,v) in enumerate(rows) if col[i]//2==h//2}
 counts=[len({union.root(i) for i,(_,h,_,_) in enumerate(rows) if h//2==g}) for g in (0,1)]
 violations=[i for i,c in enumerate(col) if i not in ci and (owners[i]<={0,1} and c>=2 or owners[i]<={2,3} and c<2)]
 out=dict(stats)
 out.update({'status':'PASS','vertices':len(V),'edges':len(E),'point_pair_norms':len(V)*(len(V)-1)//2,'direction_sizes':list(map(len,S)),'boundary_root_incidences':len(rows),'residual_orbits':counts,'pinned_residual_orbits':len(pinned),'free_residual_orbits':sum(counts)-len(pinned),'hand_checkable_root_controls':root_controls(),'boundary_rotation_tests':rotation_tests,'boundary_orbit_equalities':equalities,'equality_parities':parities,'kernel_colour_outside_old_lists':len(violations),'centre_indices':ci,'point_sha256':data['point_sha256'],'edge_sha256':data['edge_sha256'],'full_infinite_support_four_colourable':True,'native_solver_calls':0,'floating_point_operations':0,'target_found':False})
 return out,context

def controls(data,context):
 cases=[]
 def case(label,edit):
  x=copy.deepcopy(data);edit(x);cases.append((label,x))
 case('omitted boundary root',lambda x:x['boundary_direction_bits'].pop())
 case('duplicated boundary root',lambda x:x['boundary_direction_bits'].append(x['boundary_direction_bits'][0]))
 case('wrong root sign',lambda x:x['boundary_direction_bits'][0].__setitem__(2,0))
 case('nonbinary phase',lambda x:x['boundary_direction_bits'][0].__setitem__(3,2))
 case('noninteger phase',lambda x:x['boundary_direction_bits'][0].__setitem__(3,True))
 case('kernel monochromatic',lambda x:x.__setitem__('kernel_colour','0'*74))
 case('wrong graph hash',lambda x:x.__setitem__('point_sha256','0'*64))
 case('wrong embedding',lambda x:x.__setitem__('field','eta^4=12, eta<0'))
 # Select meaningful local mutations dynamically: one violates an external
 # edge, another an orbit equality while preserving all external edges.
 col=list(map(int,data['kernel_colour']));rows=context[-1][0]
 edge_index=next(a for a,(i,h,s,v) in enumerate(rows) if col[i]//2==h//2)
 case('external monochromatic edge',lambda x:x['boundary_direction_bits'][edge_index].__setitem__(3,1-x['boundary_direction_bits'][edge_index][3]))
 # Find two phase-linked boundary roots not each independently pinned by the
 # kernel colouring; flipping one must be rejected by the orbit audit.
 parity_index=None
 for a,(i,h,s,v) in enumerate(rows):
  if col[i]//2==h//2:continue
  if any(b!=a and k//2==h//2 and any(same_root(v,s,rot(w,tau),t) for tau in range(6)) for b,(j,k,t,w) in enumerate(rows)):
   parity_index=a;break
 need(parity_index is not None,'phase-only malformed control exists')
 case('inconsistent orbit with valid boundary edges',lambda x:x['boundary_direction_bits'][parity_index].__setitem__(3,1-x['boundary_direction_bits'][parity_index][3]))
 for label,x in cases:
  try:audit(x,context)
  except (ValueError,TypeError,IndexError,KeyError):continue
  raise ValueError('Malformed certificate accepted: '+label)
 return [label for label,x in cases]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
 p=Path(__file__).parent;blob=(p/'certificate.json').read_bytes();data=json.loads(blob);need(raw(data)==blob,'canonical certificate')
 report,context=audit(data);report['malformed_certificate_rejections']=controls(data,context);report['certificate_bytes']=len(blob);report['certificate_sha256']=hashlib.sha256(blob).hexdigest()
 if (p/'expected.json').exists():need(json.loads((p/'expected.json').read_text())==report,'expected report')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
