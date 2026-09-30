#!/usr/bin/env python3
"""six-reviewer-2 independent global RID gap audit, Python stdlib.
Only pinned previous reviewer code/data are used; no target imports/fixtures.
All720rank permutations replace the researcher's angular sorting algorithm.
New840-strata torque proof uses earlier reviewer integer homogeneous code.
Written continuous interpretation and explicit inherited inputs: REVIEW.md.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path

PINS={
 'winning_audit':'1ce270a559c9b86582ff7bae580763490a10468d6cd5367a70927c7f269ac456',
 'winning_expected':'f1ff37922401ce54d6c5ef965acda3bb81d8f0142e1be014abd527a14db4e791',
 'threshold_audit':'f12b78980722260e5a6b8d777ec008d1de7e5c8c4ceae6a18a652ec42e541763',
 'contact_audit':'b34c68fe16041e379d5d24ac52953fd8af8cfa23b65f8f77cba6c063c1ad4a05',
 'beta_expected':'d9814ba3f397cf05387b0727a003e7fe6bf4cf0eedf329077073ef1f8e37168b'}
def require(c,msg='independent global gap audit failed'):
 if not c:raise ValueError(msg)
def pin(p,key):require(hashlib.sha256(p.read_bytes()).hexdigest()==PINS[key],key+' differs')
def load(winning,threshold,contact,beta):
 for d,key in [(winning,'winning'),(threshold,'threshold'),(contact,'contact')]:pin(d/'audit.py',key+'_audit')
 pin(winning/'expected.json','winning_expected');pin(beta/'expected.json','beta_expected')
 spec=importlib.util.spec_from_file_location('previous_contact_review2',contact/'audit.py')
 c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
 g,k,old=c.load_geometry(threshold,winning)
 return c,g,k,old,json.loads((beta/'expected.json').read_text())
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def encoded(g,v):return [g.enc(x) for x in v]
def phi_decode(g,v):
 return tuple((F(a)+F(b)/2,F(b)/2) for a,b in v)
def ray(g,w):
 a=next((x for x in w if x!=g.ZERO),None);require(a is not None,'zero ray')
 if g.sign(a)<0:a=g.neg(a)
 return g.scaled(w,g.div(g.ONE,a))

def rank_cones(g,V,B):
 N=g.dot(B,B);c0sq=(F(1,3),0)
 active=sorted(v for v in V if g.sign(g.dot(v,B))>0 and
               g.div(g.mul(g.dot(v,B),g.dot(v,B)),N)==c0sq)
 require(len(active)==6,'complete six positive originals')
 P=[g.project(v,B) for v in active]
 require(all(g.sum_field(p[j] for p in P)==g.ZERO for j in range(3)),'mean tangent balance')
 require(any(g.cross(g.vs(P[j],P[0]),g.vs(P[l],P[0]))!=(g.ZERO,)*3 for j,l in combinations(range(1,6),2)),'tangent affine rank below two')
 candidates=[]
 for p,q in combinations(P,2):
  w=g.cross(g.vs(p,q),B);candidates += [ray(g,w),ray(g,g.vc(w,-1))]
 rays=sorted(set(candidates));require(len(candidates)==30 and len(rays)==18,'complete wall ray counts')
 require(all(ray(g,g.vc(w,-1)) in rays for w in rays),'missing antipodal wall')
 rows=[];full=[];isolated=set();counts=Counter();gap_values=[];comparisons=0
 for order in permutations(range(6)):
  constraints=[g.vs(P[b],P[a]) for a,b in zip(order,order[1:])]
  surviving=[]
  for j,w in enumerate(rays):
   signs=[g.sign(g.dot(v,w)) for v in constraints];comparisons+=5
   if min(signs)>=0:surviving.append(j)
  require(len(surviving)<=2,'unexpected nonpointed or unsplit order cone')
  counts[len(surviving)]+=1
  rows.append([list(order),surviving])
  if not surviving:continue
  for j in surviving:
   w=rays[j];gap=g.dot(g.vs(P[order[2]],P[order[0]]),w)
   require(g.sign(gap)>0,'third and first tie')
   gap_values.append(g.div(g.mul(gap,gap),g.dot(w,w)))
  if len(surviving)==1:isolated.add(surviving[0]);continue
  u,v=(rays[j] for j in surviving);w=g.va(u,v)
  require(g.cross(u,v)!=(g.ZERO,)*3 and all(g.sign(g.dot(t,w))>0 for t in constraints),'rank cone lacks strict interior')
  full.append({'boundary_ray_indices':surviving,'all_six_original_ranks':list(order)})
 require(len(full)==18 and len({tuple(z['boundary_ray_indices']) for z in full})==18,'full order cones not complete or unique')
 require(set(j for z in full for j in z['boundary_ray_indices'])==set(range(18)) and
         Counter(j for z in full for j in z['boundary_ray_indices'])==Counter({j:2 for j in range(18)}),'closed boundary coverage')
 sharp=g.minimum(gap_values);claimed=g.div(g.sub((60,0),g.sc(g.PH,12)),(19,0))
 require(sharp==claimed and g.sign(g.sub(sharp,(1,0)))>0,'sharp third-height gap differs')
 others=[v for v in V if v not in active and g.vc(v,-1) not in active]
 heights=[g.div(g.mul(g.dot(v,B),g.dot(v,B)),N) for v in others]
 require(len(others)==48 and g.minimum(heights)==(F(5,3),0),'complete nonactive original height spectrum')
 return {'all_original_positive_active_vertices':[encoded(g,v) for v in active],
         'all_actual_tangents':[encoded(g,p) for p in P],
         'full_directed_wall_rays':[encoded(g,w) for w in rays],
         'all_rank_permutations':720,'all_rank_wall_sign_comparisons':comparisons,
         'permutation_feasible_ray_count_histogram':dict(counts),'all_nonempty_two_dimensional_rank_cones':full,
         'full720permutation_record_sha256':digest(rows),
         'sharp_squared_third_minus_first_gap':g.enc(sharp),
         'all48nonactive_heights_squared':[g.enc(h) for h in heights],
         'continuous_coverage':'Every order cone is pointed; extreme rays must be among the complete pair walls. The720permutations exhaust all orders, including boundary-only orders.'},active,P

def circles(g,V,beta,refs):
 result=[]
 for n in refs:
  allp=[g.project(v,n) for v in V]
  R2=(11,4);rsq=g.sub(R2,beta)
  P=sorted(set(p for p in allp if g.dot(p,p)==rsq));require(len(P)==8,'complete circle')
  pre=[]
  for p in P:
   vv=[v for v in V if g.project(v,n)==p];require(len(vv)==1,'unique original circle preimage')
   v=vv[0];require(g.div(g.mul(g.dot(v,n),g.dot(v,n)),g.dot(n,n))==beta,'source axial height')
   pre.append(encoded(g,v))
  pairs=[]
  for i,j in combinations(range(8),2):
   w=g.vs(P[i],P[j]);pairs.append(([i,j],g.dot(w,w)))
  sharp=g.minimum([x for pair,x in pairs])
  require(sharp==g.div(g.add((40,0),g.sc(g.PH,32)),(29,0)) and g.sign(g.sub(sharp,(1,0)))>0,'complete source separation')
  result.append({'reference_ray':encoded(g,n),'all8original_preimages':pre,
                 'all8original_circle_points':[encoded(g,p) for p in P],
                 'all28squared_pair_distances':[[p,g.enc(d)] for p,d in pairs],
                 'minimum_squared_pair_distance':g.enc(sharp)})
 return result

def triangle(g,k,q):
 A,B,D,old=k.chart()
 s=g.div(g.sub(g.sub(g.PH,g.ONE),(q,0)),g.PH)
 t=g.div(g.sub(g.sub(g.PH,g.ONE),(q,0)),g.sub(g.PH,g.ONE))
 require(g.sign(s)>0 and g.sign(g.sub(g.ONE,s))>0 and g.sign(t)>0 and g.sign(g.sub(g.ONE,t))>0,'invalid cut intercept')
 U=(B,g.va(B,g.scaled(g.vs(A,B),s)),g.va(B,g.scaled(g.vs(D,B),t)))
 cut=((-1,0),(2,1),(-1,0))
 require(g.dot(cut,U[1])==g.dot(cut,U[2])==(q,0) and g.sign(g.sub(g.dot(cut,B),(q,0)))>0,'exact original cut')
 for u in U:
  require(g.sign(g.sub((F(27,25)**2,0),g.dot(u,u)))>0,'chart norm upper')
  require(g.sign(g.sub((F(27,500)**2,0),g.dot(g.vs(u,B),g.vs(u,B))))>0,'chart drift upper')
 return U

def c3_identity(g,V,B,probes):
 N=g.dot(B,B)
 skew=((g.ZERO,g.neg(B[2]),B[1]),(B[2],g.ZERO,g.neg(B[0])),(g.neg(B[1]),B[0],g.ZERO))
 P=tuple(tuple(g.sub(g.identity()[i][j],g.div(g.mul(B[i],B[j]),N)) for j in range(3)) for i in range(3))
 C=tuple(tuple(g.add(g.add(g.sc(g.identity()[i][j],F(-1,2)),g.sc(g.div(g.mul(B[i],B[j]),N),F(3,2))),g.mul(g.sc(g.PH,F(1,2)),skew[i][j])) for j in range(3)) for i in range(3))
 g.proper(C);require(g.mm(C,g.mm(C,C))==g.identity() and {g.act(C,v) for v in V}==set(V),'actual proper C3')
 for v,e in probes:
  vv=[v,g.act(C,v),g.act(g.mm(C,C),v)];ee=[e,g.act(C,e),g.act(g.mm(C,C),e)]
  pp=[g.project(a,B) for a in vv];mm=[g.cross(a,B) for a in ee]
  require(len({g.dot(a,B) for a in vv})==1 and all(g.sum_field(m[j] for m in mm)==g.ZERO for j in range(3)),'source first-order average fails')
  M=tuple(tuple(g.sum_field(g.mul(p[i],m[j]) for p,m in zip(pp,mm)) for j in range(3)) for i in range(3))
  trace=g.sum_field(M[i][i] for i in range(3))
  require(all(g.add(M[i][j],M[j][i])==g.mul(trace,P[i][j]) for i in range(3) for j in range(3)),'C3 symmetric second moment not scalar')
 return {'actual_proper_order3_body_rotation_verified':True,'all10probe_orbit_first_order_cancellations':True,'all10probe_orbit_second_moment_identities':True}

def torque(g,k,c,V,U,probes):
 A,B,D,_=k.chart()
 points=[g.cross(v,g.cross(e,B)) for v,e in probes]
 planes,dist,sides=c.hull_planes(points)
 require(len(planes)==15 and dist==g.sub((2,0),g.PH),'fresh exact center torque hull')
 require(g.sign(g.sub(g.sub(g.PH,g.ONE),(F(3,5),0)))>0 and F(3,5)-9*F(27,500)==F(57,500)>0,'uniform expanded origin interiority')
 supports=0
 for v,e in probes:
  require(v in V and g.dot(e,e)==(4,0) and (g.va(v,e) in V or g.vs(v,e) in V),'actual original endpoint/edge')
  for u in U:
   m=g.cross(e,u)
   for w in V:require(g.sign(g.dot(m,g.vs(v,w)))>=0,'original support on expanded corner');supports+=1
 L=math.lcm(*(F(x).denominator for u in U for a in u for x in a))
 chart=[tuple(tuple(int(x*L) for x in a) for a in u) for u in U];scale=4*L
 units=[tuple(int(i==j) for i in range(3)) for j in range(3)]
 polys=[]
 for v,e in probes:
  vi=tuple(tuple(int(x*2) for x in a) for a in v);ei=tuple(tuple(int(x*2) for x in a) for a in e)
  ts=[g.cross(vi,g.cross(ei,u)) for u in chart]
  polys.append(tuple({units[j]:ts[j][i] for j in range(3) if ts[j][i]!=g.ZERO} for i in range(3)))
 S={x:g.ONE for x in units};S2=k.pmul(S,S)
 faces=[f for n in (3,2,1) for f in combinations(range(3),n)]
 require(len(faces)==7,'complete simplex faces')
 counts=Counter();stream=hashlib.sha256();records=[];nodechecks=0
 for triple in combinations(range(10),3):
  a,b,z=(polys[i] for i in triple)
  normal=k.pcross(k.psub(b,a),k.psub(z,a));H=k.pdot(normal,a)
  gaps=[k.padd(k.pdot(normal,p),k.pscale(H,-1)) for p in polys]
  NS=k.pmul(k.pdot(normal,normal),S2)
  P=k.padd(k.pscale(k.pmul(H,H),4),k.pscale(NS,-scale**2))
  require(all(sum(e)==6 for e in P),'wrong homogeneous distance degree')
  stream.update(json.dumps([triple,[[list(e),g.enc(v)] for e,v in sorted(P.items())]],separators=(',',':')).encode()+b'\n')
  cases=[]
  for face in faces:
   signs=[k.psign(p,face) for p in gaps]
   if 1 in signs and -1 in signs:kind='opposite';witness=[signs.index(1),signs.index(-1)]
   elif all(not k.restriction(x,face) for x in normal):kind='degenerate';witness=[]
   elif k.nonneg(P,face):kind='distance';witness=[]
   else:raise ValueError('uncovered expanded torque stratum')
   counts[kind]+=1;cases.append([list(face),kind,witness])
  records.append({'triple':list(triple),'all7relative_face_cases':cases})
  for lam in [(1,0,0),(0,1,0),(0,0,1),(1,2,3)]:
   T=[tuple(k.peval(p,lam) for p in t) for t in polys]
   x,y,z=(T[i] for i in triple);n=g.cross(g.vs(y,x),g.vs(z,x));h=g.dot(n,x)
   require(tuple(k.peval(p,lam) for p in normal)==n and k.peval(H,lam)==h,'direct normal/height identity')
   for j,p in enumerate(gaps):require(k.peval(p,lam)==g.sub(g.dot(n,T[j]),h),'direct gap identity');nodechecks+=1
   require(k.peval(P,lam)==g.sub(g.sc(g.mul(h,h),4),g.sc(g.dot(n,n),scale**2*sum(lam)**2)),'direct distance homogenization');nodechecks+=2
 require(counts==Counter({'opposite':726,'distance':114}) and len(records)==120,'complete840strata classifications')
 return {'triangle':[encoded(g,u) for u in U],'fresh_center_hull_facets':15,'sharp_center_squared_inradius':g.enc(dist),
         'uniform_origin_interior_ball_lower':'57/500','original_corner_support_comparisons':supports,
         'integer_chart_scale':L,'integer_torque_scale':scale,'all_torque_triples':120,'all_relative_faces':7,
         'all840strata_counts':dict(counts),'all840case_record_sha256':digest(records),
         'distance_polynomial_integer_sqrt5_stream_sha256':stream.hexdigest(),
         'direct_exact_arithmetic_node_comparisons':nodechecks,'raw_uniform_torque_ball_radius':'1/2'}

def bounds(g,beta,epsilon,q,distance,band):
 require(epsilon>0 and q>0 and band>0,'invalid theorem parameters')
 a=F(25,27)*epsilon;eta=F(23,50)*a+F(9,4)*a*a;L=epsilon+9*eta;d=F(1,24)
 E=(F(13,15)*d+F(3,2)*d*d+F(17,16)*d*d)/(1-d*d/4)
 radial=(F(577,1000)*F(199,200)-F(23,50))/F(9,2)
 tests={
  'all_source_receiver_heights_strictly_above_q':g.sign(g.sub(g.sub(beta,(epsilon,0)),(q*q,0)))>0,
  'complete_lower_region_barrier':g.sign(g.sub(g.sub(beta,(epsilon,0)),(F(1,7),0)))>0,
  'height_lower_exceeds9over20':g.sign(g.sub(g.sub(beta,(epsilon,0)),(F(9,20)**2,0)))>0,
  'winning_sine_bound':0<(F(289,500)-q)/3<F(1,20),
  'winning_acute_cosine':F(399,400)>F(199,200)**2,
  'winning_chord_multiplier':F(101,100)**2*F(399,400)>1,
  'winning_source_receiver_chord':F(101,300)*(F(289,500)-q)<d,
  'source_reference_radius_upper':g.sign(g.sub((F(9,2)**2,0),(11,4)))>0,
  'c0_upper':F(1,3)<F(289,500)**2,
  'c0_lower':F(577,1000)**2<F(1,3),
  'beta_upper':g.sign(g.sub((F(23,50)**2,0),beta))>0,
  'sqrt2_upper3over2':2<F(3,2)**2,
  'threshold_coercivity_constant':F(3,2)/F(9,5)*F(10,9)==F(25,27),
  'source_threshold_small_angle':0<a<F(1,10),
  'source_transport_small':eta<F(1,1000),
  'beta_circle_radius_above4':g.sign(g.sub(g.sub((11,4),beta),(16,0)))>0,
  'receiver_candidate_height_below1over2':g.sign(g.sub((F(1,4),0),g.add(beta,(9*eta,0))))>0,
  'receiver_height_excess_below_rank_gap':F(10,9)*L<F(1,40),
  'support_choice_distance':distance>0 and L<distance**2,
  'source_separation_injective':1-2*eta>2*distance,
  'original_nonactive_separation':F(5,4)**2<F(5,3) and F(5,4)-F(9,2)*d==F(17,16),
  'winning_receiver_tangent_separation':radial>F(1,40),
  'balanced_roll_gate':E==F(267,6580) and E<F(77,1000),
  'proper_full_angle':F(101,100)**2*((2*d)**2+E*E)<F(47,500)**2,
  'torque_taylor_margin':F(1,2)-F(9,2)*F(27,25)*F(47,500)==F(1079,25000)>F(1,25),
  'nonwinning_chord_band_inside_existing_cap':F(25,27)*band<F(1,480),
  'cutoff_inside_new_nonwinning_band':epsilon<=band}
 for name,ok in tests.items():require(ok,name)
 return {'global_squared_height_slack':str(epsilon),'global_squared_diameter_slack':str(4*epsilon),
         'winning_height_cut':str(q),'threshold_source_chord_upper':str(a),'original_source_transport_upper':str(eta),
         'support_choice_squared_distance_upper':str(L),'candidate_height_excess_upper':str(F(10,9)*L),
         'reference_circle_points':8,'candidate_receiving_originals_upper':4,
         'support_choice_distance_upper':str(distance),'source_pair_distance_lower':str(2*distance),
         'winning_receiver_tangent_norm_lower':str(radial),'remote_roll_chord_upper':str(E),
         'full_proper_angle_upper':'47/500','torque_taylor_margin':'1079/25000',
         'nonwinning_band_slack':str(band),'nonwinning_band_chord_upper':str(F(25,27)*band),
         'all_exact_guards':tests}

def controls(g,beta):
 failures=[
  lambda:bounds(g,beta,F(1,440),F(909,2000),F(1,8),F(1,440)),
  lambda:bounds(g,beta,F(1,445),F(57,125),F(1,8),F(1,445)),
  lambda:bounds(g,beta,F(1,450),F(909,2000),F(1,20),F(1,450)),
  lambda:bounds(g,beta,F(0),F(909,2000),F(1,8),F(1,450)),
  lambda:bounds(g,beta,F(1,445),F(909,2000),F(1,8),F(1,450)),
  lambda:ray(g,(g.ZERO,)*3),
  lambda:g.proper(tuple(tuple(g.neg(x) for x in row) for row in g.identity()))]
 for f in failures:
  try:f()
  except ValueError:pass
  else:raise ValueError('unsupported malformed control accepted')
 return len(failures)

def main():
 root=Path(__file__).resolve().parent.parent
 p=argparse.ArgumentParser(description=__doc__)
 for arg,d in [('winning','rhombicosidodecahedron_winning_receiver_review2'),('threshold','rhombicosidodecahedron_threshold_receiver_review2'),('contact','rhombicosidodecahedron_contact_collar_review2'),('beta','rhombicosidodecahedron_beta_cap_review2')]:p.add_argument('--'+arg+'-review',type=Path,default=root/d)
 p.add_argument('--output',type=Path);a=p.parse_args()
 c,g,k,old,previous=load(a.winning_review,a.threshold_review,a.contact_review,a.beta_review)
 V=[g.vc(v,F(1,2)) for v in k.original_vertices()]
 require(len(set(V))==60 and all(g.dot(v,v)==(11,4) and g.vc(v,-1) in V for v in V),'original edge-two centrally symmetric body')
 beta=g.div(g.sub((19,0),g.sc(g.PH,8)),(29,0))
 require(previous['complete_inherited_projective_regions']==436 and previous['winning_regions']==10 and previous['threshold_regions']==60 and previous['remaining_regions']==366 and previous['remaining_maximum_squared']=='1/7','previous complete global region barrier')
 require(previous['proved_refined_transport_and_band']['closed_unit_normal_chord_cap']=='1/480','previous full all-source cap hypothesis')
 B=k.chart()[1];rank,active,P=rank_cones(g,V,B)
 require(g.sign(g.sub(g.div(g.sub((60,0),g.sc(g.PH,12)),(19,0)),(F(29,20)**2,0)))>0,'stronger rational rank margin')
 radial=(F(577,1000)*F(199,200)-F(23,50))/F(9,2)
 require(F(29,20)*radial>F(11,300),'stronger original third-height bound')
 refs=((g.ZERO,g.ONE,g.sc(g.add(g.ONE,g.PH),-3)),(g.ZERO,g.ONE,g.div(g.sub(g.sc(g.PH,3),g.ONE),(11,0))))
 circle=circles(g,V,beta,refs)
 disks=[g.active_tangents(V,n,beta)[0] for n in refs]
 require(all(x==g.div(g.add((39,0),g.sc(g.PH,37)),(29,0)) and g.sign(g.sub(x,(F(9,5)**2,0)))>0 for x in disks),'sharp threshold tangent disks')
 hexagon,_=k.boundary_geometry([g.vc(v,2) for v in V])
 probes=[(phi_decode(g,x['vertex']),phi_decode(g,x['edge'])) for x in old['torque_continuum']['selected_probes_phi_basis']]
 require(len(probes)==len(set(probes))==10,'previous original probe witnesses')
 identities=c3_identity(g,V,B,probes)
 U0=triangle(g,k,F(57,125));U1=triangle(g,k,F(909,2000))
 full=torque(g,k,c,V,U1,probes)
 result={'agent':'six-reviewer-2','role':'independent mathematical reviewer',
  'target_python_modules_or_target_fixtures_used':False,'arithmetic':'Q(sqrt5) exact Fraction pairs and integer homogeneous polynomials',
  'pinned_previous_reviewer_dependencies':PINS,'complete_global436region_classification_rerun':False,
  'previous_full_beta_cap1over480_replayed':False,
  'fresh_full720rank_order_audit':rank,'fresh_both_full_original_source_circle_audits':circle,
  'fresh_sharp_threshold_tangent_disk_squares':[g.enc(x) for x in disks],'fresh_winning_active_hexagon':hexagon,
  'fresh_actual_C3_average_identities':identities,
  'fresh_inherited_full_remote_roll_endpoint_gates':k.phase_gates(),
  'old_receiver_triangle':[encoded(g,u) for u in U0],
  'fresh_expanded_full840strata_torque_proof':full,
  'confirmed_original_global1over1200':bounds(g,beta,F(1,1200),F(57,125),F(1,10),F(1,450)),
  'confirmed_expanded_global1over450':bounds(g,beta,F(1,450),F(909,2000),F(1,8),F(1,450)),
  'proved_global_refinement1over445':bounds(g,beta,F(1,445),F(909,2000),F(1,8),F(1,445)),
  'proved_third_original_height_gap_lower':'11/300',
  'malformed_controls_rejected':controls(g,beta),
  'global_non_rupert_proved':False,'continuous_bridges_formalized':False,
  'continuous_interpretation':'Written in REVIEW.md: pointed order-cone completeness, prior C3 support envelope/proper frames, all-facets/simplex lemma, original transport/injection.'}
 text=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(text)
 else:print(text,end='')
if __name__=='__main__':main()
