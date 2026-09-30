"""Exact area-sublevel source cover and enlarged deltoidal receiver wedge.

Python3.11+ standard library. Fixed closed-cover witnesses, exact Q(sqrt5)
comparisons, full signed C2 roll cover and all1540 torque strata.
See area_sublevel_wedge_proof.md for continuous scope and trust boundary.
"""
import sys,json,hashlib,itertools,argparse,time,resource,copy
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).parent
if not __debug__:
 raise RuntimeError('verification requires assertions; do not use python -O')
from verify import Q5,ZERO,vec,vertices,dot,cross,sub,add,mul
from adaptive_area_certificate import parse
from closed_cell7_certificate import grid_upper,area_maximum,gap_less,chord_less,split
from orientation_certificate import EXPONENTS,cofactor_coefficients,area_twice,determinant
from directional_area_certificate import pmul,psub,psquare,pscale,pdot,pcross,pvsub,peval
from normalized_receiver_piece_certificate import FACES,UNITS,serialize,classify,digest,sum_polys
from normalized_cap_certificate import CONTACTS,ORIGIN_STRESS
import zero_height_wedge_certificate as parent
from zero_height_wedge_certificate import (P,V,N,M,M2,QMIN,BODY,PROBES,POINTS,DATA,
 root_upper,triangle,linear_envelopes,REMOTE_COVER,validate_roll_cover,W,tW)
TRI=triangle(F(2,5))
SOURCE_CHORD=F(2,25)
SOURCE_MAX_DEPTH=5
PARENT_CHECKER_SHA256='2968d516344a836745bb4f8a6e1875c5db31874f3670362909a322c90397a708'
PARENT_FIXTURE_SHA256='fc17167e8ec8deb80d20712c9e70ea4ee96b09ad1d08ff4c14db086cf785051c'

def source_roots():
 roots=[]
 for ci,c in enumerate(P['cell_certificates']):
  C=vec(map(parse,c['area_vector']));poly=[N[i] for i in c['corner_indices']]
  area=area_twice(poly);assert area.sign()>0
  fans=[[poly[0],poly[j],poly[j+1]] for j in range(1,len(poly)-1)]
  assert sum((area_twice(tri) for tri in fans),ZERO)==area
  assert all(area_twice(tri).sign()>0 for tri in fans)
  roots.extend((ci,j,C,tri) for j,tri in enumerate(fans))
 assert len(P['cell_certificates'])==12 and len(roots)==16
 return roots

def cap_margin(u,a):
 c=1-a*a/2;assert c>0
 mu=dot(M,u);assert mu.sign()>0
 return mu*mu-c*c*M2*dot(u,u)

def area_margin(C,u,T):
 cu=dot(C,u);assert cu.sign()>0 and T>0
 return cu*cu-T*T*dot(u,u)

def verify_source_cover(T,a=SOURCE_CHORD,certificate=None):
 """Check fixed witnesses, independently of the exploratory split policy.

 A prefix-free full tree covers each original closed fan triangle.
 Reconstruct each supplied leaf directly from its base4 path and check
 all three original geometric corner inequalities. Incomplete trees fail.
 """
 assert T>0 and 0<a<F(1,5)
 if certificate is None:
  certificate=json.loads((ROOT/'expected_area_sublevel_wedge.json').read_text())['source_cover_witnesses']
 roots=source_roots();assert len(certificate)==len(roots)
 records=[];nodes=0;depth=0;counts={'cap':0,'above_area':0}
 for root,rec in zip(roots,certificate):
  ci,j,C,tri=root
  assert set(rec)=={'cell','fan_triangle','leaves'}
  assert rec['cell']==ci and rec['fan_triangle']==j
  leaves=rec['leaves'];assert leaves
  assert all(isinstance(r,list) and len(r)==2 and isinstance(r[0],str) and r[1] in counts for r in leaves)
  paths=[r[0] for r in leaves]
  assert len(paths)==len(set(paths))
  assert all(len(p)<=SOURCE_MAX_DEPTH and set(p)<=set('0123') for p in paths)
  wanted=set(paths);seen=[]
  def cover(path):
   nonlocal nodes
   nodes+=1
   if path in wanted:seen.append(path);return
   assert len(path)<SOURCE_MAX_DEPTH and any(p.startswith(path) for p in wanted)
   for digit in '0123':cover(path+digit)
  cover('');assert set(seen)==wanted
  assert sum((F(1,4)**len(p) for p in paths),F(0))==1
  for path,kind in leaves:
   patch=tri
   for digit in path:patch=split(patch)[int(digit)]
   assert area_twice(patch)==area_twice(tri)*F(1,4)**len(path)
   cm=[cap_margin(u,a) for u in patch];am=[area_margin(C,u,T) for u in patch]
   assert all(x.sign()>0 for x in (cm if kind=='cap' else am)),('false source leaf',ci,j,path,kind)
   records.append({'cell':ci,'fan_triangle':j,'path':path,'kind':kind,
    'rays':[list(map(str,u)) for u in patch],
    'cap_corner_squared_margins':list(map(str,cm)),
    'area_corner_squared_margins':list(map(str,am))})
   counts[kind]+=1;depth=max(depth,len(path))
 return {'agent':'six-rupert-1','role':'researcher',
  'status':'complete exact finite closed source cover; written unformalized continuous proof',
  'global_Rupert_property':'OPEN','area_upper':str(T),'source_chord_upper':str(a),
  'source_cells':12,'closed_fan_triangles':16,'visited_nodes':nodes,
  'leaf_count':sum(counts.values()),'leaf_classes':counts,'maximum_depth':depth,
  'leaf_record_sha256':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest()}

def source_enclosure(tri=TRI,*,a=SOURCE_CHORD,T=None,certificate=None):
 C=vec(map(parse,P['cell_certificates'][9]['area_vector']))
 q,area=area_maximum(C,tri)
 if T is None:T=root_upper(q)
 assert T>0 and Q5(T*T)>q
 return verify_source_cover(T,a,certificate),q,area

def phase(tri=TRI):
 source,q,arec=source_enclosure(tri);e=grid_upper(lambda x:gap_less(q,QMIN,x),F(1));a=SOURCE_CHORD
 d=max(grid_upper(lambda x:chord_less(M,u,x),F(9,100)) for u in tri)
 assert a<=F(1,5) and d<=F(3,40)
 env=linear_envelopes(tri);gates=[];remote=[];chosen=[];b=F(1,10)
 for sg,pi in [(-1,3),(1,4)]:
  near=DATA[pi][45];probe=PROBES[pi];assert dot(M,V[45])==ZERO and near["d"]==probe["H"] and near["tau"][sg]>0
  assert env[pi]["L"]==ZERO
  E=env[pi]["L"]+probe["norm_upper"]*(near["source_height_upper"]*a+BODY/2*(a*a+d*d));H=probe["H"];tau=near["tau"][sg]
  quad=lambda x:(2*H+E)*x*x-2*tau*x+E
  assert quad(b).sign()<0 and quad(F(0)).sign()>=0
  xup=grid_upper(lambda x:quad(x).sign()<0,b);gates.append({"sign":sg,"probe":pi,"point":45,"error_upper":str(E),"tau_lower":str(tau),"b":str(b),"q_b":str(quad(b)),"small_root_upper":str(xup),"q_upper":str(quad(xup)),"q_predecessor":str(quad(xup-F(1,10**6))),"epsilon":str(2*xup)})
  selected=[r for r in REMOTE_COVER if r[0]==sg];validate_roll_cover(selected,b)
  for sign,los,his,pj,wi in selected:
   lo,hi=F(los),F(his);p=PROBES[pj];row=DATA[pj][wi];H=p["H"];dd=row["d"];tau=row["tau"][sg]
   E=env[pj]["L"]+p["norm_upper"]*(row["source_height_upper"]*a+BODY/2*(a*a+d*d))
   coef=[dd-H-E,Q5(2*tau),-dd-H-E];exact=[coef[0]+coef[1]*x+coef[2]*x*x for x in [lo,hi]]
   assert all(x.sign()>0 for x in exact) and coef[2].sign()<=0
   remote.append({"sign":sg,"interval":[los,his],"probe":pj,"point":wi,"source_point":POINTS[wi][1],
                  "coefficients":list(map(str,coef)),"strict_endpoint_margins":list(map(str,exact))})
  chosen.append((sg,len(set((r["probe"],r["point"]) for r in remote if r["sign"]==sg))))
 r=max(F(g["epsilon"]) for g in gates);product=(1-a*a/4)*(1-d*d/4)*(1-r*r/4);X2=(a+d)**2+r*r
 assert r<=F(1,5) and product>F(99,100)**2 and F(99,100)-a*d/4>0 and X2<=F(1,3)**2
 beta=next(F(j,1000) for j in range(1001,1020) if F(j,1000)**2*(1-X2/4)>1)
 theta=grid_upper(lambda x:Q5(x*x)>Q5(beta*beta*X2),F(1,3))
 return theta,{"area":arec,"source_cover":source,"area_excess_upper":str(e),"receiver_chord_upper":str(d),"source_chord_upper":str(a),"whole_receiver_signed_envelopes":[{k:([*v] if isinstance(v,list) else str(v)) for k,v in row.items()} for row in env],"near_zero_gates":gates,"remote_interval_count":len(remote),"remote_cover":remote,"remote_distinct_witnesses_per_sign":chosen,"roll_chord_upper":str(r),"composition_squared_upper":str(X2),"quaternion_product_margin":str(product-F(99,100)**2),"angle_derivative_factor":str(beta),"angle_derivative_margin":str(beta*beta*(1-X2/4)-1),"full_angle_upper":str(theta)}

def hull_certificate():
 tri=TRI;assert area_twice(tri).sign()!=0
 theta,phase_rec=phase(tri);rho=theta+F(1,50)
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
 assert counts["unresolved"]==0,"incomplete facet certificate is not an exclusion"
 target_rho=rho
 result={'agent':'six-rupert-1','role':'researcher','status':'complete exact finite hypotheses',
  'global_Rupert_property':'OPEN','receiver':'closed2/5area_sublevel_wedge','cell':9,
  'rays':[list(map(str,u)) for u in tri],'phase':phase_rec,'normalized_torque_ball_lower':str(target_rho),'base_distance_test_radius':str(rho),
  'strict_normalized_remainder_margin':str(target_rho-theta),'fixed_support_denominators':scalings,
  'actual_weak_support_comparisons':support_count,'positive_origin_stress':[1,3,8,10],
  'positive_cubic_origin_coefficients':40,'identically_zero_balance_coordinates':3,
  'all220potential_facets':220,'all7simplex_strata':list(map(list,FACES)),
  'all1540facet_strata':1540,'base_classifications':counts,'base_arithmetic_audits':audits,
  'base_coefficient_sha256':coeff.hexdigest(),'base_case_record_sha256':digest(records),
  'adaptive_refinement_needed':False,
  'terminal_unresolved_strata':0}
 return result

def receiver_geometry():
 from stable_certificate import orbit
 cell=[M,N[8],N[10]];sign=area_twice(cell).sign();assert sign!=0
 assert TRI==[M,add(M,mul(F(2,5),sub(W,M))),add(M,mul(F(2,5),sub(N[10],M)))]
 def weak_inside(u,tri):
  sg=area_twice(tri).sign();assert sg!=0
  return all((cross(sub(b,a),sub(u,a))[2]*sg).sign()>=0 for a,b in zip(tri,tri[1:]+tri[:1]))
 assert all(weak_inside(u,cell) for u in TRI)
 previous=triangle(F(3,10));assert all(weak_inside(u,TRI) for u in previous)
 assert area_twice(TRI)==F(16,9)*area_twice(previous)
 weights=[F(1,10),F(1,15),F(5,6)];assert sum(weights)==1 and min(weights)>0
 witness=vec(sum((weights[j]*TRI[j][k] for j in range(3)),ZERO) for k in range(3))
 sg=area_twice(TRI).sign()
 assert all((cross(sub(b,a),sub(witness,a))[2]*sg).sign()>0 for a,b in zip(TRI,TRI[1:]+TRI[:1]))
 old=[[M,add(M,mul(F(1,8),sub(N[3],M))),add(M,mul(F(1,4),sub(N[4],M)))],
  [M,add(M,mul(F(1,4),sub(N[4],M))),N[7]],
  [M,N[7],N[8]],[M,N[8],add(M,mul(F(1,6),sub(N[10],M)))],previous]
 images=orbit(witness);assert len(images)==60
 for u in images:
  for a,b,c in old:
   det=determinant(a,b,c);assert det.sign()!=0
   co=[determinant(u,b,c)/det,determinant(a,u,c)/det,determinant(a,b,u)/det]
   assert not(all(x.sign()>=0 for x in co) or all(x.sign()<=0 for x in co))
 centers=orbit(M);assert len(centers)==30
 cosine=1-F(1,50)**2/2
 for v in centers:assert dot(witness,v)**2<cosine*cosine*dot(witness,witness)*dot(v,v)
 return {'closed_triangle_rays':[list(map(str,u)) for u in TRI],
  'contains_entire_previous3_10_triangle':True,'unit_z_chart_area_ratio_over_previous_triangle':'16/9',
  'spherical_area_ratio_claimed':False,'new_witness':list(map(str,witness)),
  'witness_barycentric_weights':list(map(str,weights)),
  'projective_witness_body_orbit':60,'old_triangular_cones_checked_per_image':5,
  'witness_images_in_old_closed_receiver_regions':0,'minimum_projective_axes_checked':30,
  'witness_chord_from_every_signed_minimum_center_lower':'1/50 > 1/64'}

def proper_fold_audit():
 phi=Q5(F(1,2),F(1,2));r=vec((-phi,-phi*phi,1));r2=dot(r,r)
 assert r2.sign()>0 and dot(r,M)==ZERO
 def H(v):return sub(v,mul(2*dot(r,v)/r2,r))
 cols=[H(vec(int(i==j) for i in range(3))) for j in range(3)]
 assert all(dot(cols[i],cols[j])==Q5(int(i==j)) for i in range(3) for j in range(3))
 assert determinant(*cols)==Q5(-1) and H(M)==M
 assert {H(v) for v in V}==set(V)
 return {'actual_improper_body_reflection_normal':list(map(str,r)),
  'determinant':'-1','fixes_minimum_ray':True,'original_vertices_permuted':62,
  'proper_gauge_bridge':'if a chamber fold is improper, compose on the left with this reflection fixing m'}

def malformed_controls():
 rejected=[]
 def reject(name,fn):
  try:fn()
  except AssertionError:rejected.append(name)
  else:raise AssertionError('malformed control accepted: '+name)
 cert=json.loads((ROOT/'expected_area_sublevel_wedge.json').read_text())['source_cover_witnesses']
 source,q,area=source_enclosure();T=F(source['area_upper'])
 reject('missing original closed fan triangle',lambda:verify_source_cover(T,certificate=cert[:-1]))
 bad=copy.deepcopy(cert);bad[-1]=copy.deepcopy(bad[0])
 reject('duplicate fan triangle substituted for an original source region',lambda:verify_source_cover(T,certificate=bad))
 idx=next(i for i,r in enumerate(cert) if len(r['leaves'])>1)
 bad=copy.deepcopy(cert);bad[idx]['leaves'].pop()
 reject('missing closed source cover leaf',lambda:verify_source_cover(T,certificate=bad))
 bad=copy.deepcopy(cert);bad[idx]['leaves'].append(copy.deepcopy(bad[idx]['leaves'][0]))
 reject('duplicate source cover leaf',lambda:verify_source_cover(T,certificate=bad))
 bad=copy.deepcopy(cert);bad[idx]['leaves'].append(['','cap'])
 reject('ancestor overlaps supplied source leaves',lambda:verify_source_cover(T,certificate=bad))
 bad=copy.deepcopy(cert);bad[idx]['leaves'][0][0]='4'
 reject('invalid source path digit',lambda:verify_source_cover(T,certificate=bad))
 bad=copy.deepcopy(cert)
 ci=next(i for i,r in enumerate(bad) if r['cell']==7)
 assert bad[ci]['leaves']==[['','cap']]
 bad[ci]['leaves'][0][1]='above_area'
 reject('false above-area certificate at minimum-containing cell7',lambda:verify_source_cover(T,certificate=bad))
 reject('insufficient receiver area upper bound14',lambda:source_enclosure(T=F(14)))
 reject('unsupported smaller source chord7/100 with the same cover',lambda:verify_source_cover(T,F(7,100)))
 reject('zero source chord for a nontrivial area sublevel',lambda:verify_source_cover(T,F(0)))
 reject('false positive cap margin at distant chamber corner13',lambda:require(cap_margin(N[13],SOURCE_CHORD).sign()>0))
 return rejected

def require(value):assert value

def prerequisites():
 raw=(ROOT/'expected_zero_height_wedge.json').read_bytes()
 assert hashlib.sha256(raw).hexdigest()==PARENT_FIXTURE_SHA256
 assert hashlib.sha256((ROOT/'zero_height_wedge_certificate.py').read_bytes()).hexdigest()==PARENT_CHECKER_SHA256
 actual=parent.prerequisites()
 assert json.loads(json.dumps(actual))==json.loads(raw)['prerequisites']
 theta,phase_rec=phase()
 separation=Q5(F(106,29),F(-36,29));d=F(phase_rec['receiver_chord_upper'])
 assert (separation-Q5(8*d*d)).sign()>0
 return {'agent':'six-rupert-1','role':'researcher',
  'status':'complete exact finite prerequisites; written unformalized continuous proof',
  'global_Rupert_property':'OPEN','parent_signed_zero_height_prerequisite_every_field_matched':True,
  'parent3_10_torque_hull_replayed':False,'parent_checker_sha256':PARENT_CHECKER_SHA256,
  'parent_fixture_sha256':PARENT_FIXTURE_SHA256,'source_cover':phase_rec['source_cover'],
  'entire18interval_phase_replayed':True,'receiver_geometry':receiver_geometry(),
  'proper_fold_audit':proper_fold_audit(),'halfturn_body_separation_squared':str(separation),
  'receiver_halfturn_separation_margin':str(separation-8*d*d),
  'malformed_controls_rejected':malformed_controls()}

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);choice=ap.add_mutually_exclusive_group(required=True)
 choice.add_argument('--prerequisites',action='store_true');choice.add_argument('--hull',action='store_true')
 args=ap.parse_args();started=time.monotonic();fixture=json.loads((ROOT/'expected_area_sublevel_wedge.json').read_text())
 name='prerequisites' if args.prerequisites else 'hull'
 actual=prerequisites() if args.prerequisites else hull_certificate()
 assert json.loads(json.dumps(actual))==fixture[name],'complete expected-field mismatch'
 print(json.dumps({'checked':name,'all_expected_fields_match':True,'elapsed_seconds':time.monotonic()-started,
  'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'global_Rupert_property':'OPEN'},indent=2))
