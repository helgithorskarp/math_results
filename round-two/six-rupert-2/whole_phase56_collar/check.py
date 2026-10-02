#!/usr/bin/env python3
"""Complete exact J74 whole-phase56 receiving-cell local rigidity certificate.

No solver, NumPy, private journal or old full-source forest is imported.
The entire ordinary mathematical bridge is in PROOF.md. This is a local
collar result, not a complete source or global Rupert classification.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,copy,hashlib,importlib.util,json,sys
HERE=Path(__file__).resolve().parent

def require(ok,message):
 if not ok:raise ValueError(message)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def enc(x):return [str(x.a),str(x.b)]
def decode(x):
 require(isinstance(x,list) and len(x)==2 and all(isinstance(v,str) for v in x),'literal ordered-field coefficient')
 return Q(F(x[0]),F(x[1]))

pins=json.loads((HERE/'DEPENDENCIES.json').read_text());base=(HERE/pins['relative_directory']).resolve()
require(set(pins['sha256'])=={'model.py','q5.py'},'exact two-source prerequisites')
for name,h in pins['sha256'].items():require(hashlib.sha256((base/name).read_bytes()).hexdigest()==h,'before-import original source fingerprint: '+name)
require('q5' not in sys.modules,'unexpected preloaded arithmetic')
sys.path.insert(0,str(base));import q5 as a
Q=a.Q;require(Path(a.__file__).resolve()==base/'q5.py','verified inherited ordered-field source')
spec=importlib.util.spec_from_file_location('j74_phase56_original_model',base/'model.py');model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
import algebra as p
require(Path(p.__file__).resolve()==HERE/'algebra.py','intended literal polynomial source')
V=model.VERTICES;Z=(Q(),)*3;I=tuple(tuple(Q(int(i==j)) for j in range(3)) for i in range(3))
def act(A,v):return tuple(a.dot(row,v) for row in A)
def mm(A,B):return tuple(tuple(a.dot(row,col) for col in zip(*B)) for row in A)
def transpose(A):return tuple(zip(*A))
def proper(A):require(mm(A,transpose(A))==I and a.dot(A[0],a.cross(A[1],A[2]))==1,'actual proper source rotation')
def matrices():
 s=Q(0,1);aa=(s-1)/4;bb=(s+1)/4;cc=Q(F(1,2))
 H=((Q(-1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(1)))
 Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
 A=((bb,aa,cc),(-aa,-cc,bb),(cc,-bb,-aa));B=((-aa,-cc,-bb),(cc,-bb,aa),(-bb,-aa,cc))
 return [H,mm(A,H),mm(B,H),B,A,I],H,Mx
POSES,H,MX=matrices()
def raw(v):return (v[0],Q(1),-v[1])
def value(w,v):return w[0]+w[1]*v[0]+w[2]*v[1]
def normalize(w):
 t=next((x for x in w if x!=0),None)
 return None if t is None else tuple(x/(t if t>0 else -t) for x in w)
def clip(poly,w):
 out=[]
 for v,u in zip(poly,poly[1:]+poly[:1]):
  fv,fu=value(w,v),value(w,u)
  if fv>=0:out.append(v)
  if fv<0<fu or fu<0<fv:
   t=fv/(fv-fu);out.append(tuple(x+t*(y-x) for x,y in zip(v,u)))
 result=[]
 for v in out:
  if not result or v!=result[-1]:result.append(v)
 if len(result)>1 and result[0]==result[-1]:result.pop()
 return result

def certificate(data=None):
 if data is None:data=json.loads((HERE/'certificate.json').read_text())
 require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','literal author/schema')
 require(data['named_solid']=='original unit-edge J74 metabigyrate rhombicosidodecahedron' and data['receiving_world_raw']=='(x,1,-y)','actual original named problem/frame')
 require(data['original_cycle']==[16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,56,20],'entire actual phase56 receiving cycle')
 require(len(data['closed_triangle'])==3 and all(len(v)==2 for v in data['closed_triangle']),'three whole closed receiving corners')
 tri=[tuple(map(decode,v)) for v in data['closed_triangle']]
 s=Q(0,1);require(tri==[((s-1)/2,3-s),((5-s)/6,(5*s-7)/6),((s-1)/2,(9*s-19)/2)],'exact whole named phase56 cell triangle')
 edges=list(zip(data['original_cycle'],data['original_cycle'][1:]+data['original_cycle'][:1]))
 require(len(data['bases'])==6 and [(b['axis'],b['sign']) for b in data['bases']]==list(product(range(3),(-1,1))),'six distinct signed physical torque targets')
 for b in data['bases']:
  rows=b['literal_original_contacts'];require(len(rows)==5,'five actual physical columns')
  for row in rows:require(isinstance(row,list) and len(row)==3 and all(type(k) is int for k in row) and tuple(row[:2]) in edges and row[2] in row[:2],'literal persistent endpoint contact of original true support')
  require(type(b['strict_normalized_mass_upper']) is int and b['strict_normalized_mass_upper']>0,'literal positive mass bound')
 require(decode(data['C'])==Q(F(21,20)) and decode(data['closed_physical_Cayley_radius'])==Q(F(1,21)) and data['axis_mass_bounds']==[10,11,12] and decode(data['absorption_squared'])==Q(F(73,80)),'advertised fresh nonlinear constants')
 return data,tri,edges

def geometry_record(data=None):
 data,tri,edges=certificate(data);original,caps,gyrated,built,axes=model.cupola_construction()
 require(len(V)==len(set(V))==60 and built==set(V) and len(original)==60 and len(caps)==2 and all(len(c)==5 for c in caps),'exact original sixty-vertex two-cupola identification')
 R2=(11+4*Q(0,1))/4;require(all(a.dot(v,v)==R2 for v in V),'all original common-radius vertices')
 require(all(a.add(V[i],V[j])==Z for i,j in ((0,7),(1,6),(2,5))) and a.dot(V[0],a.cross(V[1],V[2]))!=0,'actual independent antipodal pairs, original body origin interior')
 require({act(H,v) for v in V}==set(V) and {act(MX,v) for v in V}==set(V),'actual full-body H and Mx permutations')
 for g in POSES:proper(g)
 images=[tuple(act(g,v) for v in V) for g in POSES]
 preimages=[[next(k for k,pv in enumerate(ps) if pv==V[v]) for v in data['original_cycle']] for ps in images]
 constraints={}
 for i,j in edges:
  E=a.sub(V[j],V[i])
  for k,v in enumerate(V):
   w=a.cross(a.sub(V[i],v),E);w=normalize((w[1],w[0],-w[2]))
   if w is not None:constraints.setdefault(w,[]).append([i,j,k])
 poly=[(Q(-1),Q(-1)),(Q(1),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1))]
 for w in constraints:poly=clip(poly,w)
 require(poly==tri,'all defining original support halfspaces give the entire closed triangle')
 square=[(Q(1),Q(1),Q()),(Q(1),Q(-1),Q()),(Q(1),Q(),Q(1)),(Q(1),Q(),Q(-1))]
 side_lines=[]
 for v,u in zip(tri,tri[1:]+tri[:1]):
  active=[w for w in list(constraints)+square if value(w,v)==0 and value(w,u)==0]
  require(bool(active),'each actual polygon side is a defining support/frame halfspace')
  side_lines.append([enc(z) for z in active[0]])
 require(all(-1<x<1 and 0<y<1 for x,y in tri),'whole triangle lies strictly in proper Sy maximal face, raw rz never zero')
 heights=[];ratios=[];receiver_gaps=[];source_gaps=[]
 for v in tri:
  r=raw(v)
  for i,j in edges:
   m=a.cross(a.sub(V[j],V[i]),r);h=a.dot(m,V[i]);require(h>0,'strict whole-cell corner support height')
   heights.append(h);ratios.append(R2*a.dot(m,m)/(h*h));require(ratios[-1]<(2*decode(data['C'])-1)*(2*decode(data['C'])-1),'fresh normalized whole-cell quadratic bound')
   for pv in V:require(h-a.dot(m,pv)>=0,'every original receiving support at each closed corner');receiver_gaps.append(h-a.dot(m,pv))
   for ps in images:
    for pv in ps:require(h-a.dot(m,pv)>=0,'every original source support at each closed corner');source_gaps.append(h-a.dot(m,pv))
 centroid=tuple(sum((v[k] for v in tri),Q())/3 for k in range(2));strict_centroid=0
 for i,j in edges:
  m=a.cross(a.sub(V[j],V[i]),raw(centroid));h=a.dot(m,V[i])
  for k,pv in enumerate(V):
   if k not in (i,j):require(h-a.dot(m,pv)>0,'actual seventeen-corner phase interior');strict_centroid+=1
 # Complete possible collisions g_i=C_n(g_j), with exact reflection axes.
 collisions=[]
 for gi,g in enumerate(POSES):
  for hi,h in enumerate(POSES):
   Fm=mm(mm(g,MX),transpose(h))
   if Fm!=transpose(Fm) or sum((Fm[k][k] for k in range(3)),Q())!=1:
    collisions.append([gi,hi,'not a plane reflection']);continue
   axis=next(tuple(I[i][k]-Fm[i][k] for i in range(3)) for k in range(3) if any(I[i][k]!=Fm[i][k] for i in range(3)))
   require(Fm==tuple(tuple(I[i][k]-2*axis[i]*axis[k]/a.dot(axis,axis) for k in range(3)) for i in range(3)),'literal collision reflection axis')
   if axis[1]==0:collisions.append([gi,hi,'axis outside raw ry=1 chart']);continue
   v=(axis[0]/axis[1],-axis[2]/axis[1]);bad=next((w for w in list(constraints)+square if value(w,v)<0),None)
   require(bad is not None,'no base/companion collision anywhere on the entire closed cell')
   collisions.append([gi,hi,'outside cell',[enc(z) for z in v],[enc(z) for z in bad],enc(value(bad,v))])
 require(len(set(POSES))==6,'six distinct original base poses')
 fixture_comparisons=0
 for v in tri+[centroid]:
  r=raw(v);r2=a.dot(r,r);Mn=tuple(tuple(I[i][k]-2*r[i]*r[k]/r2 for k in range(3)) for i in range(3));P=tuple(tuple(I[i][k]-r[i]*r[k]/r2 for k in range(3)) for i in range(3))
  require(mm(P,Mn)==P and mm(Mn,Mn)==I,'literal original projection/reflection action fixtures')
  for g in POSES:
   Cg=mm(mm(Mn,g),MX);proper(Cg)
   require({act(P,act(Cg,pv)) for pv in V}=={act(P,act(g,pv)) for pv in V},'whole sixty-point source projection action fixture');fixture_comparisons+=60
 control=data['old_stencil_countercontrol'];require(control['axis']==1 and control['sign']==-1 and control['receiver_vertex']==0,'old physical countercontrol signed target')
 r=raw(tri[0]);columns=[]
 for i,j,k in control['literal_original_contacts']:
  require((i,j) in edges and k in (i,j),'old stencil still genuine endpoint contact')
  m=a.cross(a.sub(V[j],V[i]),r);columns.append(tuple(a.cross(V[k],m))+tuple(m[:2]))
 B=tuple(zip(*columns));target=(Q(),Q(-1),Q(),Q(),Q());weights=act(p.inverse(B),target)
 require(act(B,weights)==target and weights[0]==decode(control['first_raw_weight']) and weights[0]<0,'actual exact old-stencil failure, not cone nonexistence')
 return {'agent':'six-rupert-2','role':'researcher','certificate_sha256':digest(data),'closed_world_raw_vertices':[[enc(z) for z in raw(v)] for v in tri],
  'true_gap_halfspaces':len(constraints),'all_closed_receiving_support_comparisons':len(receiver_gaps),'all_six_closed_source_support_comparisons':len(source_gaps),
  'strict_centroid_offendpoint_gaps':strict_centroid,'all_six_exact_spatial_corner_preimages':preimages,'actual_defining_side_lines':side_lines,
  'minimum_strict_support_height':enc(min(heights)),'maximum_corner_R2_norm_N2':enc(max(ratios)),'all_51_fresh_quadratic_bounds':True,
  'all_36_base_companion_collision_cases':collisions,'whole_original_branches_distinct':12,'source_projection_action_fixture_comparisons':fixture_comparisons,
  'old_stencil_first_negative_raw_weight':enc(weights[0]),'old_stencil_failure_not_nonexistence':True}

def dual_record(index,data=None):
 data,tri,edges=certificate(data);require(type(index) is int and 0<=index<6,'signed physical dual index');d=data['bases'][index];contacts=d['literal_original_contacts'];corners=[];height_corners=[];normal_z=[]
 for v in tri:
  normals=[a.cross(a.sub(V[j],V[i]),raw(v)) for i,j,k in contacts]
  corners.append(tuple(zip(*(tuple(a.cross(V[k],m))+tuple(m[:2]) for m,(i,j,k) in zip(normals,contacts)))))
  height_corners.append([a.dot(m,V[k]) for m,(i,j,k) in zip(normals,contacts)]);normal_z.append([m[2] for m in normals])
 M=[[p.linear([B[r][k] for B in corners]) for k in range(5)] for r in range(5)]
 hs=[p.linear([h[k] for h in height_corners]) for k in range(5)];mz=[p.linear([m[k] for m in normal_z]) for k in range(5)]
 D=p.det(M);target=tuple(Q(d['sign']*int(k==d['axis'])) for k in range(5));Ns=[]
 for k in range(5):
  A=[[({p.ZERO:target[r]} if target[r]!=0 else {}) if i==k else M[r][i] for i in range(5)] for r in range(5)];Ns.append(p.det(A))
 for r in range(5):
  lhs={}
  for k in range(5):lhs=p.add(lhs,p.mul(M[r][k],Ns[k]))
  require(lhs==p.scale(D,target[r]),'entire literal homogeneous torque/two-force polynomial identity')
 force_z={}
 for k in range(5):force_z=p.add(force_z,p.mul(mz[k],Ns[k]))
 require(force_z=={},'entire literal third spatial force polynomial identity')
 midpoint=(Q(F(1,3)),)*3;require(p.value(D,midpoint)!=0,'nonzero point physical contact determinant')
 orientation=1 if p.value(D,midpoint)>0 else -1;D=p.scale(D,orientation);Ns=[p.scale(N,orientation) for N in Ns]
 dc=p.controls(D,5);nc=[p.controls(N,4) for N in Ns];require(min(z for e,z in dc)>0,'all21 whole closed triangle determinant controls strict')
 require(min(z for cs in nc for e,z in cs)>=0,'all75 whole closed triangle cofactors nonnegative, closed grazing ties retained')
 mass={}
 for N,h in zip(Ns,hs):mass=p.add(mass,p.mul(N,h))
 bound=d['strict_normalized_mass_upper'];bc=p.controls(p.add(p.scale(D,bound),p.scale(mass,-1)),5);require(min(z for e,z in bc)>0,'all21 normalized whole triangle mass upper controls strict')
 fixtures=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)),midpoint,(Q(F(1,2)),Q(F(1,2)),Q()),(Q(),Q(F(1,2)),Q(F(1,2)))]
 for t in fixtures:
  B=tuple(tuple(sum((t[v]*corners[v][r][k] for v in range(3)),Q()) for k in range(5)) for r in range(5));dd=p.directdet(B)
  require(p.value(D,t)==orientation*dd,'direct Gaussian determinant/Cramer expansion comparison')
  weights=act(p.inverse(B),target);require(tuple(p.value(N,t)/p.value(D,t) for N in Ns)==weights,'full literal independent exact inverse/Cramer comparison')
 controls=[[[list(e),enc(z)] for e,z in cs] for cs in [dc,*nc,bc]]
 return {'agent':'six-rupert-2','role':'researcher','certificate_sha256':digest(data),'signed_basis_index':index,'axis':d['axis'],'sign':d['sign'],
  'literal_original_contacts':contacts,'strict_normalized_mass_upper':bound,'every_117_control_signs_checked':True,'all_six_literal_spatial_polynomial_identities':True,
  'control_stream_sha256':digest(controls),'minimum_determinant_control':enc(min(z for e,z in dc)),'minimum_cofactor_control':enc(min(z for cs in nc for e,z in cs)),
  'minimum_strict_mass_bound_control':enc(min(z for e,z in bc)),'zero_cofactor_controls':[[k,list(e)] for k,cs in enumerate(nc) for e,z in cs if z==0],
  'direct_determinant_and_inverse_fixtures':len(fixtures)}

def semantics(data,records):
 rejected=[]
 def reject(label,fn):
  try:fn()
  except (ValueError,ZeroDivisionError,StopIteration):rejected.append(label);return
  raise ValueError('semantic damage accepted: '+label)
 bad=copy.deepcopy(data);bad['original_cycle'].remove(56);reject('omitted actual receiving edge',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['closed_triangle'][0][0]=['0','0'];reject('changed closed cell corner',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['bases'][0]['literal_original_contacts'][0][2]=15;reject('nonendpoint or nongenuine persistent contact',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['bases'][1]['strict_normalized_mass_upper']=9;reject('unproved smaller whole normalized mass',lambda:dual_record(1,bad))
 bad=copy.deepcopy(data);bad['C']=['1','0'];reject('unproved smaller quadratic constant',lambda:certificate(bad))
 A=POSES[4];reject('right folding by a partial shadow pose as body symmetry',lambda:require({act(A,v) for v in V}==set(V),'A is not a full-body symmetry'))
 reject('silently discarded closed zero-cofactor boundary',lambda:require(records[4]['minimum_cofactor_control']!=['0','0'],'negative-z dual retains genuine closed zero weights'))
 bad=copy.deepcopy(data);bad['closed_physical_Cayley_radius']=['1/20','0'];reject('larger unproved advertised Cayley radius',lambda:certificate(bad))
 return {'agent':'six-rupert-2','role':'researcher','semantic_damages_rejected':rejected}

def complete_record(data=None):
 data,tri,edges=certificate(data);geometry=geometry_record(data);duals=[dual_record(i,data) for i in range(6)];semantic=semantics(data,duals)
 masses=[max(d['strict_normalized_mass_upper'] for d in duals if d['axis']==k) for k in range(3)]
 require(masses==data['axis_mass_bounds'],'all actual signed masses required for three-coordinate closure')
 absorption=decode(data['C'])*decode(data['C'])*sum((Q(v*v) for v in masses),Q())*decode(data['closed_physical_Cayley_radius'])*decode(data['closed_physical_Cayley_radius'])
 require(absorption==decode(data['absorption_squared']) and absorption<1,'strict uniform CLOSED nonlinear absorption')
 return {'agent':'six-rupert-2','role':'researcher','scope':'whole actual J74 phase56 closed triangle geometry and uniform local1/21 collar only; far source and global Rupert OPEN',
  'certificate_sha256':digest(data),'geometry':geometry,'all_six_duals':duals,'semantics':semantic,'all_702_control_signs_checked':True,
  'literal_spatial_polynomial_equations':36,'closed_physical_Cayley_radius':'1/21','equivalent_trace_lower_gate':'661/221','C':'21/20','axis_mass_bounds':masses,'absorption_squared':enc(absorption),
  'global_J74_Rupert_status':'OPEN','all_source_classification_claimed':False,'old_full_source_forests_used':False,'ordinary_unformalized_author_check':True,'independent_review_claimed':False}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true',help='omit only fixed expected record comparison; every proof check remains');args=parser.parse_args()
 result=complete_record()
 if not args.emit:require(result==json.loads((HERE/'expected.json').read_text()),'complete exact expected mathematical record')
 print(json.dumps(result,indent=2))
