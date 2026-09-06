"""Independent quadratic-tower audit; imports no producer or parent code."""
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
def formula_ok(clauses,bits):return all(any(bits[v]==b for v,b in c) for c in clauses)
def lift_controls():
 forms=[(2,[[(0,a),(1,b)] for a,b in product((0,1),repeat=2)]),(3,[[(0,a),(1+a,b)] for a,b in product((0,1),repeat=2)])]
 out=[]
 for n,F in forms:
  lifted=[]
  for ((v,p),(w,q)) in F:lifted.extend([[(v,p),(n+w,q)],[(w,q),(n+v,p)]])
  models=sum(formula_ok(lifted,bits) for bits in product((0,1),repeat=2*n));need(models==0,'lift obstruction')
  restored=[]
  for i in range(4):
   c=lifted[:2*i]+lifted[2*i+2:];restored.append(sum(formula_ok(c,bits) for bits in product((0,1),repeat=2*n)))
  need(all(restored),'paired clause deletion restoration')
  out.append({'base_variables':n,'lift_assignments':1<<(2*n),'lift_models':models,'paired_clause_deletion_model_counts':restored})
 return out

def audit(data):
 need(data.get('schema')==1 and data.get('field_polynomial')=='T^4-12' and data.get('embedding')=='eta positive','schema and field')
 need(data.get('target_found')is False and data.get('full_support_colouring_claimed')is False,'scope flag')
 need(mul(mul(ETA,ETA),mul(ETA,ETA))==scale(ONE,12),'quartic relation')
 zeta=U[2];a1=U[4];u=(scale(SQRT3,Q(1,2)),scale(ONE,Q(-1,2)))
 y=cm(u,(scale(sub(ONE,SQRT3),Q(1,2)),scale(ETA,Q(1,2))))
 z=cm(u,(scale(sub(ONE,SQRT3),Q(1,2)),scale(ETA,Q(-1,2))))
 params={k:decode(data['parameters'][k]) for k in ['u','y','z']}
 need(params=={'u':u,'y':y,'z':z},'exact parameter')
 need(all(norm(v,Z)==ONE for v in [u,y,z]),'unit parameters')
 reps=[O,y,z];orbit_exclusions=0
 for v,w in combinations(reps,2):
  for root in U:need(v!=cm(w,root),'distinct orbit');orbit_exclusions+=1
 D=list(map(decode,data['centres']));want=[Z,a1,cs(cn(O),y),ca(cn(zeta),z)]
 need(D==want and len(set(D))==4,'centre construction')
 need(norm(D[0],D[1])==ONE and norm(D[2],D[3])==ONE and cs(D[3],D[2])==u,'unit segment')
 # Strictly 0<q<4 follows from the two supplied distinct unit roots.
 cross=((0,2),(0,3),(1,2),(1,3));I=[];qrows=[];root_checks=0
 need(len(data['intersections'])==4,'four cross slots')
 for (a,b),row in zip(cross,data['intersections']):
  roots=list(map(decode,row));need(len(roots)==2 and len(set(roots))==2,'two distinct roots')
  need(roots==sorted(roots,key=key),'root order')
  for point in roots:need(norm(point,D[a])==norm(point,D[b])==ONE,'root on both circles');root_checks+=2
  q=norm(D[a],D[b]);need(q not in [scale(ONE,j) for j in (0,1,3,4)],'regular distances')
  qrows.append([[x.numerator,x.denominator] for x in coeff(q)]);I.append(roots)
 need(data['cross_squared_distances']==qrows,'distance encoding')
 # This also checks the explicit formula q+=(1+sqrt3+eta)/2, q-=(1+sqrt3-eta)/2.
 qplus=scale(add(add(ONE,SQRT3),ETA),Q(1,2));qminus=scale(sub(add(ONE,SQRT3),ETA),Q(1,2))
 need([norm(D[a],D[b]) for a,b in cross]==[qplus,qplus,qminus,qminus],'distance formula')
 def phase_info(v):
  found=[(j,k) for j,rep in enumerate(reps) for k,root in enumerate(U) if cm(rep,root)==v]
  need(len(found)==1,'unique phase label');return found[0]
 expected_clauses=[[[0,0],[1,0]],[[0,1],[2,0]],[[0,0],[1,1]],[[0,1],[2,1]]]
 need(data['coupled_clauses']==expected_clauses,'three-variable forcing pattern')
 need(len(data['independent_phase_clauses'])==8,'eight incidence clauses')
 for c in data['independent_phase_clauses']:
  need(isinstance(c,list) and len(c)==2 and c==sorted(c),'independent clause shape')
  for lit in c:need(isinstance(lit,list) and len(lit)==2 and all(type(x)is int for x in lit) and 0<=lit[0]<6 and lit[1] in (0,1),'literal domain')
  need(c[0][0]<3 and c[1][0]>=3,'A/B variables')
 root_truth=0;coupled_truth=0
 for bits in product((0,1),repeat=6):
  for slot,((a,b),roots) in enumerate(zip(cross,I)):
   for r,x in enumerate(roots):
    v,k=phase_info(cs(x,D[a]));w,l=phase_info(cs(x,D[b]))
    ca_value=(bits[v]+a+k)%2;cb_value=2+(bits[3+w]+b-2+l)%2
    eligible=(ca_value!=b-2 or cb_value!=2+a)
    need(eligible==formula_ok([data['independent_phase_clauses'][2*slot+r]],bits),'independent clause geometry');root_truth+=1
    if all(bits[3+i]==1-bits[i] for i in range(3)):
     need(eligible==formula_ok([expected_clauses[slot]],bits),'coupled clause geometry');coupled_truth+=1
 need(not any(formula_ok(data['independent_phase_clauses'],bits) for bits in product((0,1),repeat=6)),'independent phase impossibility')
 need(not any(formula_ok(expected_clauses,bits) for bits in product((0,1),repeat=3)),'coupled phase impossibility')
 mixed=set(x for row in I for x in row);need(len(mixed)==data['mixed_points']==6,'six mixed points')
 # Named six-point formula checked independently against all certified roots.
 named={cn(O),cn(zeta),cn(y),cs(a1,y),z,ca(a1,z)};need(mixed==named,'named mixed points')
 S=[set(),set()]
 for g in range(2):
  seeds=[cs(D[2*g+1],D[2*g])]
  for x in mixed:
   for h in (2*g,2*g+1):
    if norm(x,D[h])==ONE:seeds.append(cs(x,D[h]))
  for seed in seeds:S[g].update(cm(seed,root) for root in U)
 V=sorted({ca(d,direction) for h,d in enumerate(D) for direction in S[h//2]},key=key)
 E=[(a,b) for a,b in combinations(range(len(V)),2) if norm(V[a],V[b])==ONE]
 need(data['direction_sizes']==list(map(len,S)),'direction counts');need(data['vertices']==len(V) and data['edges']==len(E),'graph counts')
 need(data['point_sha256']==digest(list(map(encode,V))) and data['edge_sha256']==digest(E),'graph hashes')
 idx={v:i for i,v in enumerate(V)};ci=[idx[d] for d in D];need(ci==data['centre_indices'],'centre labels')
 own=[{i for i,d in enumerate(D) if norm(v,d)==ONE} for v in V];need(all(own),'all points owned')
 lists=[1<<(2,3,0,1)[ci.index(i)] if i in ci else 3 if o<={0,1} else 12 if o<={2,3} else 15 for i,o in enumerate(own)]
 need(data['kernel_lists']==''.join(format(m,'x') for m in lists),'kernel lists')
 path=data['list_obstruction_path'];need(path==list(map(idx.__getitem__,[cn(O),zeta,cn(a1),O,cn(zeta)])),'fixed even path')
 need(len(set(path))==5 and all(tuple(sorted((a,b))) in E for a,b in zip(path,path[1:])),'four unit path edges')
 need(all(lists[i]==3 and own[i]=={0} for i in path[1:-1]),'path interior lists')
 forced=[]
 for v in (path[0],path[-1]):
  mask=lists[v]
  for h in own[v]:mask &= ~(1<<(2,3,0,1)[h])
  colours=[c for c in range(4) if mask>>c&1];need(len(colours)==1,'one forced endpoint');forced.append(colours[0])
 need(forced==data['path_forced_colours']==[1,0] and (len(path)-1)%2==0,'opposite pins on even binary path')
 colour=data['colouring'];need(isinstance(colour,str) and len(colour)==len(V) and set(colour)<={'0','1','2','3'},'colour domain');col=list(map(int,colour))
 need([col[i] for i in ci]==[2,3,0,1],'distinct centre pins')
 need(all(col[a]!=col[b] for a,b in E),'proper unrestricted colouring')
 violations=[i for i,c in enumerate(col) if not lists[i]>>c&1];need(violations,'positive colouring must leave the old lists')
 return {'status':'PASS','vertices':len(V),'edges':len(E),'point_pair_norms':len(V)*(len(V)-1)//2,'mixed_points':len(mixed),'direction_sizes':list(map(len,S)),'orbit_exclusion_checks':orbit_exclusions,'root_unit_distance_checks':root_checks,'independent_root_truth_checks':root_truth,'coupled_root_truth_checks':coupled_truth,'coupled_phase_models':0,'independent_phase_models':0,'list_obstruction_path_edges':len(path)-1,'path_forced_colours':forced,'proper_colour_edge_checks':len(E),'positive_colouring_outside_list_vertices':len(violations),'point_sha256':data['point_sha256'],'edge_sha256':data['edge_sha256'],'abstract_lift_controls':lift_controls(),'full_support_colourability':'not established','native_solver_calls':0,'target_found':False}

def controls(data):
 cases=[]
 x=copy.deepcopy(data);x['intersections'][0].pop();cases.append(x)
 x=copy.deepcopy(data);x['parameters']['y'][0][0][0]+=1;cases.append(x)
 x=copy.deepcopy(data);x['coupled_clauses'][0][0][1]^=1;cases.append(x)
 x=copy.deepcopy(data);x['independent_phase_clauses'][0][0][1]^=1;cases.append(x)
 x=copy.deepcopy(data);x['list_obstruction_path'].pop();cases.append(x)
 x=copy.deepcopy(data);x['kernel_lists']='f'*x['vertices'];cases.append(x)
 x=copy.deepcopy(data);x['colouring']='0'*x['vertices'];cases.append(x)
 x=copy.deepcopy(data);x['point_sha256']='0'*64;cases.append(x)
 x=copy.deepcopy(data);x['full_support_colouring_claimed']=True;cases.append(x)
 for x in cases:
  try:audit(x)
  except (ValueError,TypeError,IndexError,KeyError):continue
  raise ValueError('Malformed certificate accepted')
 return len(cases)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
 p=Path(__file__).parent;blob=(p/'certificate.json').read_bytes();data=json.loads(blob);need(raw(data)==blob,'canonical certificate')
 report=audit(data);report['malformed_certificate_rejections']=controls(data);report['certificate_bytes']=len(blob);report['certificate_sha256']=hashlib.sha256(blob).hexdigest()
 if (p/'expected.json').exists():need(json.loads((p/'expected.json').read_text())==report,'expected report')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
