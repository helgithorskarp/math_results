"""Exact signed zero-height roll and normalized torque certificate.

Python3.11+ stdlib. Fixed checked witnesses; no floating proof decisions.
Complete continuous scope and trust boundary: zero_height_wedge_proof.md.
"""
import sys,json,itertools,argparse,time,resource,hashlib
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).parent
if not __debug__:raise RuntimeError("verification requires assertions; do not use python -O")
from verify import Q5,ZERO,vec,vertices,dot,cross,sub,add,mul,convex_hull_2d
from adaptive_area_certificate import parse
from closed_cell7_certificate import grid_upper,area_maximum,gap_less,chord_less,COERCIVITY
P=json.loads((ROOT/"expected_global_area.json").read_text());V=vertices();N=[vec(map(parse,x["ray"])) for x in P["corner_areas"]];M=N[9];M2=dot(M,M);QMIN=parse(P["global_minimum_area_squared"]);BODY=F(23,10)
def root_upper(q,cap=F(20)):
 if q==ZERO:return F(0)
 return grid_upper(lambda x:Q5(x*x)>q,cap)
def signed_root_lower(raw):
 if raw==ZERO:return F(0)
 up=root_upper(raw*raw/M2)
 return up-F(1,10**6) if raw.sign()>0 else -up
def convex_zero_point(i,j,t):
 assert i!=j and 0<=i<62 and 0<=j<62
 assert t.sign()>0 and (1-t).sign()>0
 w=add(mul(t,V[i]),mul(1-t,V[j]));assert dot(M,w)==ZERO
 return w

def reference():
 e1=vec((-M[1],M[0],0));e2=cross(M,e1);assert dot(e1,M)==dot(e2,M)==dot(e1,e2)==ZERO
 mapping={}
 for v in V:mapping.setdefault((dot(v,e1),dot(v,e2)),[]).append(v)
 hull=[mapping[q][0] for q in convex_hull_2d(mapping)]
 probes=[]
 for x,y in zip(hull,hull[1:]+hull[:1]):
  mu=cross(sub(y,x),M);H=dot(mu,x);assert H.sign()>0 and all(dot(mu,v)<=H for v in V)
  probes.append({"mu":mu,"H":H,"norm_upper":root_upper(dot(mu,mu)),"edge":[V.index(x),V.index(y)]})
 assert len(probes)==16
 zero=[]
 for i,j in [(43,57),(53,57),(59,61),(55,58),(34,36),(17,20)]:
  hi,hj=dot(M,V[i]),dot(M,V[j]);t=-hj/(hi-hj);assert t.sign()>0 and (1-t).sign()>0
  w=convex_zero_point(i,j,t)
  zero.append((w,{"indices":[i,j],"weight":str(t)}));zero.append((mul(-1,w),{"negative_of":[i,j],"weight":str(t)}))
 points=[(v,{"vertex":i}) for i,v in enumerate(V)]+zero
 assert len({w for w,rec in zero})==12 and all(dot(v,v)<Q5(BODY*BODY) for v,rec in points)
 data=[]
 for pi,p in enumerate(probes):
  row=[]
  for wi,(w,rec) in enumerate(points):
   h=dot(M,w);hu=root_upper(h*h/M2);raw=dot(M,cross(w,p["mu"]));d=dot(p["mu"],w)
   assert -p["H"]<=d<=p["H"]
   row.append({"point":wi,"d":d,"source_height_upper":hu,"tau":{sg:signed_root_lower(sg*raw) for sg in [-1,1]}})
  data.append(row)
 return probes,points,data
PROBES,POINTS,DATA=reference()
mu45=PROBES[3]["mu"];tW=-dot(mu45,N[8])/dot(mu45,sub(N[10],N[8]));W=add(N[8],mul(tW,sub(N[10],N[8])))
assert tW.sign()>0 and (1-tW).sign()>0 and dot(mu45,W)==ZERO
def triangle(scale):return [M,add(M,mul(scale,sub(W,M))),add(M,mul(scale,sub(N[10],M)))]
def linear_envelopes(tri):
 rows=[]
 for probe in PROBES:
  mu,H=probe["mu"],probe["H"];ratios=[dot(mu,u)/dot(M,u) for u in tri];assert all(dot(M,u).sign()>0 for u in tri)
  lo=min(ZERO,*ratios);hi=max(ZERO,*ratios);vals=[(-dot(M,v)*x-(H-dot(mu,v)),j,s) for j,v in enumerate(V) for s,x in enumerate([lo,hi])]
  L=max(ZERO,*(v for v,j,s in vals));assert all(v<=L for v,j,s in vals)
  rows.append({"lo":lo,"hi":hi,"L":L,"active":[[j,s] for v,j,s in vals if v==L]})
 return rows
def phase(tri):
 C=vec(map(parse,P["cell_certificates"][9]["area_vector"]));q,arec=area_maximum(C,tri);e=grid_upper(lambda x:gap_less(q,QMIN,x),F(1));a=COERCIVITY*e
 d=max(grid_upper(lambda x:chord_less(M,u,x),F(9,100)) for u in tri)
 assert a<=F(1,5) and d<=F(1,20)
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
 return theta,{"area":arec,"area_excess_upper":str(e),"receiver_chord_upper":str(d),"source_chord_upper":str(a),"whole_receiver_signed_envelopes":[{k:([*v] if isinstance(v,list) else str(v)) for k,v in row.items()} for row in env],"near_zero_gates":gates,"remote_interval_count":len(remote),"remote_cover":remote,"remote_distinct_witnesses_per_sign":chosen,"roll_chord_upper":str(r),"composition_squared_upper":str(X2),"quaternion_product_margin":str(product-F(99,100)**2),"angle_derivative_factor":str(beta),"angle_derivative_margin":str(beta*beta*(1-X2/4)-1),"full_angle_upper":str(theta)}

REMOTE_COVER=((-1, '1/10', '109/640', 3, 45), (-1, '109/640', '181/640', 7, 4), (-1, '181/640', '13/40', 7, 65), (-1, '13/40', '167/320', 6, 4), (-1, '167/320', '343/640', 7, 67), (-1, '343/640', '11/20', 5, 4), (-1, '11/20', '221/320', 0, 45), (-1, '221/320', '577/640', 4, 4), (-1, '577/640', '1', 4, 65), (1, '1/10', '109/640', 4, 45), (1, '109/640', '181/640', 0, 57), (1, '181/640', '13/40', 0, 62), (1, '13/40', '167/320', 1, 57), (1, '167/320', '343/640', 0, 73), (1, '343/640', '11/20', 2, 57), (1, '11/20', '221/320', 7, 45), (1, '221/320', '577/640', 3, 57), (1, '577/640', '1', 3, 62))
def validate_roll_cover(rows,b):
 assert rows and len(rows)==9 and len({r[0] for r in rows})==1 and rows[0][0] in [-1,1]
 assert F(rows[0][1])==b and F(rows[-1][2])==1
 for r in rows:
  assert len(r)==5 and F(r[1])<F(r[2]) and 0<=r[3]<16 and 0<=r[4]<74
 for a,c in zip(rows,rows[1:]):assert F(a[2])==F(c[1])
TRI=triangle(F(3,10))
from normalized_cap_certificate import CONTACTS,ORIGIN_STRESS
from orientation_certificate import EXPONENTS,cofactor_coefficients,area_twice,determinant
from directional_area_certificate import pmul,psub,psquare,pscale,pdot,pcross,pvsub,peval
from normalized_receiver_piece_certificate import FACES,UNITS,serialize,classify,digest,sum_polys

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
  'global_Rupert_property':'OPEN','receiver':'closed3/10zero_height_wedge','cell':9,
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
 sign=area_twice([M,N[8],N[10]]).sign();assert sign!=0
 assert dot(PROBES[3]['mu'],W)==ZERO
 assert TRI==[M,add(M,mul(F(3,10),sub(W,M))),add(M,mul(F(3,10),sub(N[10],M)))]
 assert area_twice(TRI).sign()!=0
 for u in TRI:
  assert u[2]==Q5(1)
  assert all((cross(sub(b,a),sub(u,a))[2]*sign).sign()>=0
             for a,b in zip([M,N[8],N[10]],[N[8],N[10],M]))
 # A strict new witness must escape every body/antipodal image of the
 # preceding regions, not just their representatives in this chamber.
 weights=[F(1,10),F(1,15),F(5,6)];assert sum(weights)==1 and min(weights)>0
 witness=vec(sum((weights[j]*TRI[j][k] for j in range(3)),ZERO) for k in range(3))
 s=area_twice(TRI).sign()
 assert all((cross(sub(b,a),sub(witness,a))[2]*s).sign()>0
            for a,b in zip(TRI,TRI[1:]+TRI[:1]))
 old=[[M,add(M,mul(F(1,8),sub(N[3],M))),add(M,mul(F(1,4),sub(N[4],M)))],
      [M,add(M,mul(F(1,4),sub(N[4],M))),N[7]],
      [M,N[7],N[8]],[M,N[8],add(M,mul(F(1,6),sub(N[10],M)))]]
 images=orbit(witness);assert len(images)==60
 for u in images:
  for a,b,c in old:
   det=determinant(a,b,c);assert det.sign()!=0
   co=[determinant(u,b,c)/det,determinant(a,u,c)/det,determinant(a,b,u)/det]
   assert not (all(x.sign()>=0 for x in co) or all(x.sign()<=0 for x in co))
 centers=orbit(M);assert len(centers)==30
 cosine=1-F(1,50)**2/2
 for v in centers:
  assert dot(witness,v)**2<cosine*cosine*dot(witness,witness)*dot(v,v)
 return {'closed_triangle_rays':[list(map(str,u)) for u in TRI],
         'signed_cone_cut_W':list(map(str,W)),'W_N10_weight':str(tW),
         'N10_intercept_over_previous_D9':'9/5; this is an intercept ratio, not an area ratio',
         'new_witness':list(map(str,witness)),'witness_barycentric_weights':list(map(str,weights)),
         'projective_witness_body_orbit':60,'old_triangular_cones_checked_per_image':4,
         'witness_images_in_old_closed_receiver_regions':0,'minimum_projective_axes_checked':30,
         'witness_chord_from_every_signed_minimum_center_lower':'1/50 > 1/64'}

def rodrigues_audits():
 base=vec((0,0,1));mu=vec((2,-3,0));identities=0
 for e in map(vec,[(1,0,0),(F(3,5),F(4,5),0)]):
  axis=cross(base,e);assert dot(e,e)==dot(axis,axis)==Q5(1)
  for t in [F(-1,4),F(0),F(1,4)]:
   c=(1-t*t)/(1+t*t);ss=2*t/(1+t*t);delta2=2*(1-c)
   def rotation(w,sgn=1):return add(add(mul(c,w),mul((1-c)*dot(axis,w),axis)),mul(sgn*ss,cross(axis,w)))
   normal=add(mul(c,base),mul(ss,e));assert rotation(base)==normal
   columns=[rotation(vec(int(i==j) for i in range(3))) for j in range(3)]
   assert all(dot(columns[i],columns[j])==Q5(int(i==j)) for i in range(3) for j in range(3))
   assert determinant(*columns)==Q5(1)
   for h in [-5,0,5]:
    w=vec((7,11,h));actual=dot(mu,rotation(w,-1))
    expected=dot(mu,w)-dot(w,base)*dot(mu,normal)-delta2/2*dot(mu,e)*dot(w,e)
    assert actual==expected
    moved=sub(rotation(w,-1),w);tangent=vec((moved[0],moved[1],0))
    assert tangent==mul(-ss*h-delta2/2*dot(w,e),e)
    identities+=2
 return {'proper_rotation_matrices_audited':6,'signed_receiving_and_source_vector_identities':identities,
         'axes':2,'signed_angles_including_zero':3,'signed_heights_including_zero':3}

def malformed_controls():
 rejected=[]
 def reject(name,fn):
  try:fn()
  except AssertionError:rejected.append(name)
  else:raise AssertionError('malformed control accepted: '+name)
 minus=[r for r in REMOTE_COVER if r[0]==-1]
 reject('missing closed roll interval',lambda:validate_roll_cover(minus[:-1],F(1,10)))
 bad=list(minus);r=list(bad[1]);r[1]=str(F(r[1])+F(1,1000));bad[1]=tuple(r)
 reject('gap in closed roll cover',lambda:validate_roll_cover(bad,F(1,10)))
 bad2=list(minus);r=list(bad2[1]);r[1]=str(F(r[1])-F(1,1000));bad2[1]=tuple(r)
 reject('overlapping intervals substituted for exact roll partition',lambda:validate_roll_cover(bad2,F(1,10)))
 reject('false zero axial height of original V57',lambda:require(dot(M,V[57])==ZERO))
 env=linear_envelopes(TRI)
 reject('false zero one-sided envelope on reference facet0',lambda:require(env[0]['L']==ZERO))
 outside=linear_envelopes([M,N[8],TRI[2]])
 reject('outside the receiving zero-height sign cone',lambda:require(outside[3]['L']==ZERO))
 reject('reversed actual reference support',lambda:require(all(dot(mul(-1,PROBES[3]['mu']),sub(V[45],v)).sign()>=0 for v in V)))
 reject('undersized reference normal norm',lambda:require(dot(PROBES[3]['mu'],PROBES[3]['mu'])<Q5(1)))
 theta,rec=phase(TRI);a=F(rec['source_chord_upper']);d=F(rec['receiver_chord_upper'])
 reject('clamping necessary source chord to1/10',lambda:require(a<=F(1,10)))
 reject('zero falsely chosen above the inverse small root',lambda:require(parse(rec['near_zero_gates'][0]['error_upper']).sign()<0))
 reject('unit angle derivative factor',lambda:require(1-F(rec['composition_squared_upper'])/4>1))
 # A non-convex value cannot be accepted as an original convex witness.
 reject('nonpositive convex source weight',lambda:convex_zero_point(43,57,Q5(-1)))
 return rejected

def require(value):assert value

def prerequisites():
 from normalized_receiver_piece_certificate import prerequisites as previous_prerequisites
 actual=previous_prerequisites()
 expected=json.loads((ROOT/'expected_normalized_receiver_pieces.json').read_text())['prerequisites']
 assert json.loads(json.dumps(actual))==expected
 assert dot(M,V[45])==ZERO and dot(V[45],V[45])==Q5(5)
 for pi in [3,4]:
  p=PROBES[pi];assert dot(p['mu'],V[45])==p['H']
 pins=['verify.py','orientation_certificate.py','stable_certificate.py','global_area_certificate.py',
       'adaptive_area_certificate.py','directional_area_certificate.py','closed_cell7_certificate.py',
       'normalized_cap_certificate.py','normalized_receiver_piece_certificate.py',
       'expected_global_area.json','expected_adaptive_area.json','expected_directional_area.json',
       'expected_closed_cell7.json','expected_normalized_cap.json','expected_normalized_receiver_pieces.json']
 return {'agent':'six-rupert-1','role':'researcher','status':'exact finite prerequisites; unformalized continuous proof',
         'global_Rupert_property':'OPEN','previous_prerequisites_every_field_matched':True,
         'old_six_receiver_pieces_replayed':False,'parent_source_and_fixture_sha256':
          {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in pins},
         'reference_shadow_facets':16,'actual_original_reference_support_comparisons':992,
         'reference_probe_edges':[p['edge'] for p in PROBES],
         'original_vertices':62,'additional_checked_zero_height_convex_source_points':12,
         'zero_height_original_V45':list(map(str,V[45])),'V45_norm_squared':'5',
         'receiver_geometry':receiver_geometry(),'rodrigues_audits':rodrigues_audits(),
         'malformed_controls_rejected':malformed_controls()}

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);choice=ap.add_mutually_exclusive_group(required=True)
 choice.add_argument('--prerequisites',action='store_true');choice.add_argument('--hull',action='store_true')
 args=ap.parse_args();started=time.monotonic();fixture=json.loads((ROOT/'expected_zero_height_wedge.json').read_text())
 name='prerequisites' if args.prerequisites else 'hull';actual=prerequisites() if args.prerequisites else hull_certificate()
 assert json.loads(json.dumps(actual))==fixture[name],'complete expected-field mismatch'
 print(json.dumps({'checked':name,'all_expected_fields_match':True,'elapsed_seconds':time.monotonic()-started,
  'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'global_Rupert_property':'OPEN'},indent=2))
