"""Exact closed deltoidal receiver regions, per-contact affine torque hulls.

Python3.11+, stdlib only. One complete piece per invocation. No heuristic is a
certificate. All possible facets and all seven simplex strata are covered.
"""
import sys,json,hashlib,itertools,argparse,time,resource
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).parent
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
from verify import Q5,ZERO,vec,vertices,dot,cross,sub,add,mul
from adaptive_area_certificate import parse
from normalized_cap_certificate import CONTACTS,ORIGIN_STRESS
from global_area_certificate import root_gap_greater
from closed_cell7_certificate import grid_upper,area_maximum,gap_less,chord_less,split,COERCIVITY
from directional_area_certificate import padd,pscale,pmul,psub,psquare,pdot,pcross,pvsub,peval
from orientation_certificate import EXPONENTS,cofactor_coefficients,area_twice

FACES=[f for n in (3,2,1) for f in itertools.combinations(range(3),n)]
UNITS=[tuple(int(i==j) for i in range(3)) for j in range(3)]
P=json.loads((ROOT/'expected_global_area.json').read_text())
V=vertices();N=[vec(map(parse,x['ray'])) for x in P['corner_areas']];M=N[9]
QMIN=parse(P['global_minimum_area_squared']);TOP=parse(P['minimal_shadow_max_radius_squared'])
def ray(i,t):return add(M,mul(t,sub(N[i],M)))
MACROS=[(4,'near3',[M,ray(3,F(1,8)),ray(4,F(1,4))]),
        (4,'near7',[M,ray(4,F(1,4)),N[7]]),
        (9,'near8',[M,N[8],ray(10,F(1,6))])]
PIECES=[(4,'near3','',MACROS[0][2])]+[(4,'near7',str(i),p) for i,p in enumerate(split(MACROS[1][2]))]+[(9,'near8','',MACROS[2][2])]
def restrict(p,face):return {e:v for e,v in p.items() if all(e[i]==0 for i in range(3) if i not in face)}
def strict_sign(p,face):
 vals=restrict(p,face).values();signs={x.sign() for x in vals}
 return next(iter(signs)) if len(signs)==1 else 0
def classify(n,gaps,distance,face):
 pos=next((i for i,p in enumerate(gaps) if strict_sign(p,face)==1),None)
 neg=next((i for i,p in enumerate(gaps) if strict_sign(p,face)==-1),None)
 if pos is not None and neg is not None:return 'opposite',(pos,neg)
 if all(not restrict(p,face) for p in n):return 'degenerate',()
 if all(x.sign()>=0 for x in restrict(distance,face).values()):return 'distance',()
 return 'unresolved',()
def serialize(p):return [[list(e),str(v)] for e,v in sorted(p.items())]
def phase(cell,tri):
 C=vec(map(parse,P['cell_certificates'][cell]['area_vector']))
 q,arec=area_maximum(C,tri);e=grid_upper(lambda x:gap_less(q,QMIN,x),F(1,10))
 d=max(grid_upper(lambda x:chord_less(M,u,x),F(1,20)) for u in tri)
 a=COERCIVITY*e;E0=F(29,100)*(a+d)+F(23,20)*(a*a+d*d)
 E=F(29,100)*a+F(141,200)*d+F(23,20)*(a*a+d*d);b=2*E;X2=(a+d)**2+b*b
 assert d<=F(1,20) and a<=F(1,10) and b<=F(1,5)
 product=(1-d*d/4)*(1-a*a/4)*(1-b*b/4)
 assert product>F(99,100)**2 and F(99,100)-a*d/4>0
 assert E0<F(1,25);root_gap_greater(TOP,Q5(5),E0)
 beta=F(1003,1000)
 assert X2<=F(1,4)**2 and beta*beta*(1-X2/4)>1
 theta=grid_upper(lambda x:Q5(x*x)>Q5(beta*beta*X2),F(1,4))
 return theta,{'area':arec,'area_excess_upper':str(e),'receiver_chord_upper':str(d),
  'source_chord_upper':str(a),'radial_error_upper':str(E0),'old1_28gate_passes':E0<=F(1,28),
  'radial_positive_branch_left':str(TOP-Q5(5)-E0*E0),
  'radial_squared_margin':str((TOP-Q5(5)-E0*E0)**2-20*E0*E0),
  'roll_chord_upper':str(b),'composition_squared_upper':str(X2),
  'quaternion_product_margin':str(product-F(99,100)**2),
  'dynamic_angle_derivative_margin':str(beta*beta*(1-X2/4)-1),'full_angle_upper':str(theta)}
def finite_piece(index):
 started=time.monotonic();cell,name,path,tri=PIECES[index];assert area_twice(tri).sign()!=0
 theta,phase_rec=phase(cell,tri);rho=theta+F(1,50)
 support_count=0;T=[];scalings=[];values=[]
 for aa,bb,j in CONTACTS:
  edge=sub(V[bb],V[aa]);muv=[cross(edge,u) for u in tri]
  for mu in muv:
   for v in V:assert dot(mu,sub(V[j],v)).sign()>=0;support_count+=1
  K2=max(dot(V[j],V[j])*dot(mu,mu)/4 for mu in muv)
  B=grid_upper(lambda x:Q5(x*x)>K2,F(3));scalings.append(str(B))
  G=[mul(1/B,cross(V[j],mu)) for mu in muv];values.append(G)
  T.append([{UNITS[s]:G[s][k] for s in range(3) if G[s][k]!=ZERO} for k in range(3)])
 weights=cofactor_coefficients([values[j] for j in ORIGIN_STRESS],-1)
 assert all(x.sign()>0 for row in weights for x in row),'origin stress not positive'
 wp=[dict(zip(EXPONENTS,row)) for row in weights]
 assert all(sum_polys([pmul(wp[j],T[ORIGIN_STRESS[j]][k]) for j in range(4)])=={} for k in range(3))
 sumlam={e:Q5(1) for e in UNITS};sumlam2=psquare(sumlam)
 counts={'opposite':0,'distance':0,'degenerate':0,'unresolved':0};records=[];coeff=hashlib.sha256();audits=0
 audits_lam=[tuple(F(i==j) for i in range(3)) for j in range(3)]+[(F(1,2),F(1,3),F(1,6))]
 direct=[[vec(sum((lam[s]*G[s][k] for s in range(3)),ZERO) for k in range(3)) for G in values] for lam in audits_lam]
 for ids in itertools.combinations(range(12),3):
  a,b,c=[T[j] for j in ids];normal=pcross(pvsub(b,a),pvsub(c,a));h=pdot(normal,a)
  gaps=[psub(pdot(normal,t),h) for t in T]
  distance=psub(psquare(h),pscale(pmul(pdot(normal,normal),sumlam2),rho*rho))
  for p in [*normal,h,*gaps,distance]:coeff.update(json.dumps(serialize(p),separators=(',',':')).encode())
  for lam,actual in zip(audits_lam,direct):
   a0,b0,c0=[actual[j] for j in ids];n0=cross(sub(b0,a0),sub(c0,a0));h0=dot(n0,a0)
   assert vec(peval(p,lam) for p in normal)==n0 and peval(h,lam)==h0
   assert all(peval(p,lam)==dot(n0,t)-h0 for p,t in zip(gaps,actual))
   assert peval(distance,lam)==h0*h0-rho*rho*dot(n0,n0);audits+=15
  groups={};dm=gm=um=0
  for i,f in enumerate(FACES):
   kind,witness=classify(normal,gaps,distance,f);counts[kind]+=1
   if kind=='distance':dm|=1<<i
   elif kind=='degenerate':gm|=1<<i
   elif kind=='unresolved':um|=1<<i
   else:groups[witness]=groups.get(witness,0)|(1<<i)
  assert dm|gm|um|sum(groups.values())==127
  records.append({'triple':list(ids),'distance_face_mask':dm,'degenerate_face_mask':gm,'unresolved_face_mask':um,
                  'opposite_gap_witnesses':[[mask,*w] for w,mask in sorted(groups.items())]})
 assert len(records)==220 and sum(counts.values())==1540
 refinements=[];refhash=hashlib.sha256();refnodes=0;refaudits=0
 target_rho=rho if counts['unresolved']==0 else theta+F(1,100)
 for rec in records:
  if rec['unresolved_face_mask']:
   certificate=refine_triple(values,tuple(rec['triple']),target_rho,tri,refhash)
   refinements.append(certificate);refnodes+=certificate['nodes'];refaudits+=certificate['arithmetic_audits']
 assert all(r['terminal_unresolved_strata']==0 for r in refinements)
 result={'agent':'six-rupert-1','role':'researcher','status':'complete exact finite hypotheses',
  'global_Rupert_property':'OPEN','piece_index':index,'cell':cell,'macro':name,'path':path,
  'rays':[list(map(str,u)) for u in tri],'phase':phase_rec,'normalized_torque_ball_lower':str(target_rho),'base_distance_test_radius':str(rho),
  'strict_normalized_remainder_margin':str(target_rho-theta),'fixed_support_denominators':scalings,
  'actual_weak_support_comparisons':support_count,'positive_origin_stress':[1,3,8,10],
  'positive_cubic_origin_coefficients':40,'identically_zero_balance_coordinates':3,
  'all220potential_facets':220,'all7simplex_strata':list(map(list,FACES)),
  'all1540facet_strata':1540,'base_classifications':counts,'base_arithmetic_audits':audits,
  'base_coefficient_sha256':coeff.hexdigest(),'base_case_record_sha256':digest(records),
  'refinements':refinements,'refinement_coefficient_sha256':refhash.hexdigest(),
  'additional_refinement_nodes':refnodes,'additional_arithmetic_audits':refaudits,
  'terminal_unresolved_strata':0}
 return result

MAX_FACET_DEPTH=8
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def split_values(G):
 a,b,c=G;ab=mul(F(1,2),add(a,b));bc=mul(F(1,2),add(b,c));ca=mul(F(1,2),add(c,a))
 return [[a,ab,ca],[ab,b,bc],[ca,bc,c],[ab,bc,ca]]
def facet_polynomials(values,ids,rho):
 T=[[{UNITS[s]:G[s][k] for s in range(3) if G[s][k]!=ZERO} for k in range(3)] for G in values]
 a,b,c=[T[j] for j in ids];n=pcross(pvsub(b,a),pvsub(c,a));h=pdot(n,a)
 gaps=[psub(pdot(n,t),h) for t in T];sumlam={e:Q5(1) for e in UNITS}
 distance=psub(psquare(h),pscale(pmul(pdot(n,n),psquare(sumlam)),rho*rho))
 return n,h,gaps,distance
def validate_closed_paths(tri,paths):
 assert paths and len(paths)==len(set(paths)) and all(len(p)<=MAX_FACET_DEPTH and set(p)<=set('0123') for p in paths)
 wanted=set(paths);seen=[]
 def visit(path,t):
  if path in wanted:seen.append(path);return
  assert len(path)<MAX_FACET_DEPTH and any(p.startswith(path) for p in wanted)
  for i,child in enumerate(split(t)):visit(path+str(i),child)
 visit('',tri);assert set(seen)==wanted
 assert sum((F(1,4)**len(p) for p in paths),F(0))==1
def refine_triple(values,ids,rho,tri,coeff):
 pending=[('',values)];paths=[];nodes=0;audits=0
 counts={k:0 for k in ['opposite','distance','degenerate','unresolved']};leaf_counts={k:0 for k in counts}
 case_records=[];lam=(F(1,2),F(1,3),F(1,6))
 while pending:
  path,val=pending.pop();n,h,gaps,distance=facet_polynomials(val,ids,rho);nodes+=1
  coeff.update(json.dumps([list(ids),path],separators=(',',':')).encode())
  for poly in [*n,h,*gaps,distance]:coeff.update(json.dumps(serialize(poly),separators=(',',':')).encode())
  actual=[vec(sum((lam[s]*G[s][k] for s in range(3)),ZERO) for k in range(3)) for G in val]
  a,b,c=[actual[j] for j in ids];direct_n=cross(sub(b,a),sub(c,a));direct_h=dot(direct_n,a)
  assert vec(peval(poly,lam) for poly in n)==direct_n and peval(h,lam)==direct_h
  assert all(peval(poly,lam)==dot(direct_n,t)-direct_h for poly,t in zip(gaps,actual))
  assert peval(distance,lam)==direct_h*direct_h-rho*rho*dot(direct_n,direct_n);audits+=15
  row=[classify(n,gaps,distance,f) for f in FACES]
  for kind,_ in row:counts[kind]+=1
  case_records.append([path,[[kind,list(witness)] for kind,witness in row]])
  if all(kind!='unresolved' for kind,_ in row):
   paths.append(path)
   for kind,_ in row:leaf_counts[kind]+=1
  else:
   assert len(path)<MAX_FACET_DEPTH,('incomplete finite facet cover',ids,path)
   children=[split_values(G) for G in val]
   pending.extend((path+str(i),[c[i] for c in children]) for i in reversed(range(4)))
 validate_closed_paths(tri,paths);assert leaf_counts['unresolved']==0
 return {'triple':list(ids),'nodes':nodes,'closed_leaf_paths':paths,'max_leaf_depth':max(map(len,paths)),
  'all_node_classifications':counts,'all_leaf_classifications':leaf_counts,
  'all7faces_checked_on_each_closed_leaf':True,'arithmetic_audits':audits,
  'terminal_unresolved_strata':0,'case_record_sha256':digest(case_records)}

def sum_polys(polys):
 ans={}
 for p in polys:ans=padd(ans,p)
 return ans

from stable_certificate import orbit
from orientation_certificate import determinant
from closed_cell7_certificate import closed_cover,inside,area_controls
def weak_inside(u,poly):
 sign=area_twice(poly).sign();assert sign!=0
 return all((cross(sub(b,a),sub(u,a))[2]*sign).sign()>=0 for a,b in zip(poly,poly[1:]+poly[:1]))

def receiver_geometry():
 for cell,_,tri in MACROS:
  poly=[N[j] for j in P['cell_certificates'][cell]['corner_indices']]
  assert all(weak_inside(u,poly) for u in tri)
 quad=[M,ray(3,F(1,8)),ray(4,F(1,4)),N[7]]
 assert all(cross(sub(quad[(i+1)%4],quad[i]),sub(quad[(i+2)%4],quad[(i+1)%4]))[2].sign()>0 for i in range(4))
 assert area_twice(quad)==sum((area_twice(t) for _,_,t in MACROS[:2]),ZERO)
 assert cross(sub(quad[2],quad[0]),sub(quad[1],quad[0]))[2].sign()*cross(sub(quad[2],quad[0]),sub(quad[3],quad[0]))[2].sign()<0
 leaves,splits=closed_cover(MACROS[1][2],['0','1','2','3'])
 assert splits==[''] and [t for _,t in leaves]==[x[3] for x in PIECES[1:5]]
 tri=PIECES[2][3];u=vec(sum((v[k] for v in tri),ZERO)/3 for k in range(3));assert inside(u,tri)
 poly=[N[j] for j in P['cell_certificates'][4]['corner_indices']];sign=area_twice(poly).sign()
 assert all((cross(sub(b,a),sub(u,a))[2]*sign).sign()>0 for a,b in zip(poly,poly[1:]+poly[:1]))
 axes=sorted(orbit(M));assert len(axes)==30
 d=F(1,50);c=1-d*d/2
 margins=[c*c*dot(u,u)*dot(v,v)-dot(u,v)**2 for v in axes]
 assert all(x.sign()>0 for x in margins)
 images=sorted(orbit(u));assert len(images)==60
 a,b,c=M,N[7],N[8];det=determinant(a,b,c);assert det.sign()!=0
 coords=[]
 for v in images:
  w=(determinant(v,b,c)/det,determinant(a,v,c)/det,determinant(a,b,v)/det)
  assert not(all(x.sign()>=0 for x in w) or all(x.sign()<=0 for x in w));coords.append(list(map(str,w)))
 return {'macro_regions':[{'cell':cell,'name':name,'rays':[list(map(str,u)) for u in tri]} for cell,name,tri in MACROS],
  'closed_cell4_convex_quadrilateral_rays':[list(map(str,u)) for u in quad],
  'closed_midpoint_cover_paths':['0','1','2','3'],'exact_child_area_ratio':'1/4',
  'new_receiver_witness':{'ray':list(map(str,u)),'strict_inside_cell':4,'strict_inside_piece':2,
   'distance_from_all60_directed_minimum_centers_lower':'1/50','all30_projective_axis_comparisons':30,
   'cap_separation_margin_sha256':digest(list(map(str,margins))),
   'complete_projective_reflection_orbit':60,'images_in_old_closed_cell7_cone':0,
   'all_projective_cone_coordinates_sha256':digest(coords)}}


def negative_controls():
 rejected=[]
 def reject(name,fn):
  try:fn()
  except AssertionError:rejected.append(name)
  else:raise AssertionError('malformed control accepted: '+name)
 reject('missing closed midpoint child',lambda:validate_closed_paths(PIECES[0][3],['0','1','2']))
 reject('prefix-overlapping closed cover',lambda:validate_closed_paths(PIECES[0][3],['','0']))
 reject('duplicate closed cover leaf',lambda:validate_closed_paths(PIECES[0][3],['','']))
 tri=PIECES[0][3];aa,bb,j=CONTACTS[0]
 def reversed_support():
  mu=cross(sub(V[aa],V[bb]),tri[0]);assert all(dot(mu,sub(V[j],v)).sign()>=0 for v in V)
 reject('reversed original support',reversed_support)
 vals=[]
 for aa,bb,j in CONTACTS:
  edge=sub(V[bb],V[aa]);vals.append([cross(V[j],cross(edge,u)) for u in tri])
 reject('repeated origin stress point',lambda:cofactor_coefficients([vals[j] for j in (1,3,3,10)],-1))
 def false_facet_distance():
  points=[G[0] for G in vals]
  for ids in itertools.combinations(range(12),3):
   a,b,c=[points[j] for j in ids];n=cross(sub(b,a),sub(c,a))
   if dot(n,n)==ZERO:continue
   h=dot(n,a);gaps=[dot(n,x)-h for x in points]
   if all(x.sign()>=0 for x in gaps) or all(x.sign()<=0 for x in gaps):
    assert h*h>=Q5(10000)*dot(n,n);return
  raise RuntimeError('no actual facet in false-distance control')
 reject('false actual facet ball100',false_facet_distance)
 left=TOP-Q5(5)-F(1,20)**2
 def false_radial_gap():
  assert left.sign()>0 and (left*left-20*F(1,20)**2).sign()>0
 reject('false radial gap1/20',false_radial_gap)
 def false_angle_derivative():assert F(1)*(1-F(1,10)**2/4)>1
 reject('false unit angle derivative',false_angle_derivative)
 area_controls()
 C=vec(map(parse,P['cell_certificates'][4]['area_vector']));q,rec=area_maximum(C,tri)
 assert rec['active_strata']==['edge1']
 assert q>max(dot(C,u)**2/dot(u,u) for u in tri)
 return rejected
def prerequisites():
 from normalized_cap_certificate import check as check_cap
 actual=check_cap(self_test=True);expected=json.loads((ROOT/'expected_normalized_cap.json').read_text())
 assert json.loads(json.dumps(actual))==expected
 assert parse(P['receiver_halfturn_Frobenius_separation_squared'])>Q5(8*F(1,20)**2)
 return {'agent':'six-rupert-1','role':'researcher','full_normalized_cap_prerequisite_matched':True,
  'parent_expected_sha256':hashlib.sha256((ROOT/'expected_normalized_cap.json').read_bytes()).hexdigest(),
  'receiver_geometry':receiver_geometry(),'malformed_controls_rejected':negative_controls()}
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);choice=ap.add_mutually_exclusive_group(required=True)
 choice.add_argument('--piece',type=int,choices=range(6));choice.add_argument('--prerequisites',action='store_true')
 args=ap.parse_args();started=time.monotonic();fixture=json.loads((ROOT/'expected_normalized_receiver_pieces.json').read_text())
 if args.prerequisites:actual=prerequisites();expected=fixture['prerequisites'];label='prerequisites'
 else:actual=finite_piece(args.piece);expected=fixture['pieces'][args.piece];label='piece'+str(args.piece)
 assert json.loads(json.dumps(actual))==expected,'complete expected-field mismatch'
 print(json.dumps({'checked':label,'all_expected_fields_match':True,'elapsed_seconds':time.monotonic()-started,
  'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'global_Rupert_property':'OPEN'},indent=2))
