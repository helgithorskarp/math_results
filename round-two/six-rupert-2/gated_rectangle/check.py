#!/usr/bin/env python3
"""Every source chunk plus the local and coordinate bridge are required."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,copy,hashlib,importlib.util,json,sys
import forms as j
HERE=Path(__file__).resolve().parent;c,a,Q=j.c,j.a,j.Q
CHUNK_SIZE=128
def digest(x):return hashlib.sha256(c.canonical(x)).hexdigest()
def independent_box(depth,code):
 lo=[];hi=[]
 for axis in range(3):
  bits=[(code>>(depth-level-1))&1 for level in range(axis,depth,3)];integer=0
  for bit in bits:integer=2*integer+bit
  width=F(2,2**len(bits));lo.append(F(-1)+integer*width);hi.append(F(-1)+(integer+1)*width)
 return lo,hi
def certificate(data=None):
 if data is None:data=json.loads((HERE/'certificate.json').read_text())
 c.require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','actual certificate author and schema')
 c.require(data['source_M']==['15/4','0'] and data['receiver_halfwidth']==['1/1000','0'],'literal complete source/receiver domains')
 c.require(data['receiver_center']==[['2315/1798','-453/1798'],['2211/1798','205/1798'],['-1','0']],'actual entire old phase-crossing box')
 c.require(data['canonical_original_hole_indices']==[1,8,7],'three literal original point-reference holes')
 leaves=data['leaves'];cursor=F();nodes=set();counts={'C':0,'G':0,'H':0}
 for leaf in leaves:
  c.require(type(leaf) is list and len(leaf)>=4,'complete actual leaf schema')
  depth,code,kind=leaf[:3];c.require(type(depth) is int and type(code) is int and 0<=depth<=28 and 0<=code<2**depth,'actual finite closed source cube')
  start=F(code,2**depth);end=F(code+1,2**depth)
  c.require(start==cursor,'complete sorted prefix cover without gaps or overlaps');cursor=end
  c.require(c.box(depth,code)==independent_box(depth,code),'independent dyadic source box decoder')
  c.require(kind in counts,'physical cut, canonical gauge reject or one of three equality holes');counts[kind]+=1
  if kind=='G':c.require(len(leaf)==4 and type(leaf[3]) is int and leaf[3] in (0,1),'two exact closed gauges')
  elif kind=='H':c.require(len(leaf)==4 and leaf[3] in (1,8,7),'three actual canonical equality reference indices')
  else:c.require(len(leaf) in (6,7) and type(leaf[3]) is int and 0<=leaf[3]<108 and all(type(k) is int and 0<=k<60 for k in leaf[4:]),'actual original two- or three-support physical cut labels')
  for level in range(depth):nodes.add((level,code>>(depth-level)))
 c.require(cursor==1,'the entire closed source cube is covered')
 for depth,code in nodes:
  lo,hi=independent_box(depth,code);left=independent_box(depth+1,2*code);right=independent_box(depth+1,2*code+1);axis=depth%3;mid=(lo[axis]+hi[axis])/2
  c.require(left[0]==lo and right[1]==hi and left[1][axis]==mid==right[0][axis],'actual closed midpoint source split')
  c.require(all(left[1][i]==hi[i] and right[0][i]==lo[i] for i in range(3) if i!=axis),'every unsplit coordinate retained')
 return data,{'closed_source_roots':1,'closed_source_leaves':len(leaves),'closed_midpoint_nodes':len(nodes),'leaf_kinds':counts,'maximum_depth':max(x[0] for x in leaves),'exact_required_signs':243*counts['C']+81*counts['G']+27*counts['H']}
def local_record():
 data,partition=certificate();olddata=json.loads((j.old.HERE/'certificate.json').read_text());mathematics=j.old.l.preflight(olddata)
 f=j.Forms();c.require([c.enc(x) for x in f.raw]==data['receiver_center'],'same exact entire receiving box')
 return {'agent':'six-rupert-2','role':'researcher','scope':'fresh whole original local collar and both receiver phases, no replay of old source forest','certificate_canonical_sha256':digest(data),'whole_local_mathematical_record':mathematics,'whole_local_mathematical_record_sha256':digest(mathematics),'source_hole_indices':f.original_hole_indices,'point_hole_Cayley_gate':'1/33','moving_closed_local_Cayley_gate':'1/30','partition':partition,'old_source_exclusion_used_as_premise':False}
def audit_gauges(f):
 evaluations=0
 sources=[(0,0,0)]+[tuple(sign*int(i==axis) for i in range(3)) for axis in range(3) for sign in (-1,1)]+[tuple(int(i in pair) for i in range(3)) for pair in ((0,1),(0,2),(1,2))]
 e=f.eta
 for which in range(2):
  components=j.gauge_components(f.raw,which)
  for ddx,ddy in product((-e,Q(),e),repeat=2):
   X,Y=f.raw[0]+ddx,f.raw[1]+ddy;powers=(Q(1),ddx,ddy,ddx*ddx,ddx*ddy,ddy*ddy)
   A=[[sum((powers[k]*components[k][i][m] for k in range(6)),Q()) for m in range(4)] for i in range(4)]
   for U,V,w in sources:
    z=(Q(1),Q(U),Q(V),Q(w));actual=sum((z[i]*A[i][m]*z[m] for i in range(4) for m in range(4)),Q())
    wanted=(X+w-j.M*Y*V)*(X+w-j.M*Y*V)-X*X-Y*Y-1 if which==0 else (1-X*w+j.M*Y*U)*(1-X*w+j.M*Y*U)-X*X-Y*Y-1
    c.require(actual==wanted,'literal closed scalar gauge polynomial and matrix differ');evaluations+=1
 return evaluations
def audit_physical_forms(f,data):
 # Literal spatial evaluations do not use matrix congruence or Bernstein conversion.
 leaves=[leaf for leaf in data['leaves'] if leaf[2]=='C'];chosen=[leaves[i] for i in (0,len(leaves)//2,-1)];records=[]
 for leaf in chosen:
  ci,ks=leaf[3],leaf[4:];rows,_=f.original.circuits[ci]
  components=f.original.component_forms(ci,ks)
  for dx,dy,U,V,w in ((Q(),Q(),Q(),Q(),Q()),(-f.eta,f.eta,Q(F(1,2)),Q(F(-1,3)),Q(F(1,4))),(f.eta,-f.eta,Q(-1),Q(1),Q(-1))):
   raw=a.add(f.raw,(dx,dy,Q()));z=(Q(1),U,V,w);qw=c.act(j.B,z);norm=sum((t*t for t in qw),Q())
   # R_hom is independently evaluated from its explicit ordinary quaternion formula.
   h,x,y,zz=qw
   Rh=((h*h+x*x-y*y-zz*zz,2*(x*y-h*zz),2*(x*zz+h*y)),(2*(x*y+h*zz),h*h-x*x+y*y-zz*zz,2*(y*zz-h*x)),(2*(x*zz-h*y),2*(y*zz+h*x),h*h-x*x-y*y+zz*zz))
   beta=f.original.beta[ci];actual=Q()
   for k,row in enumerate(rows):
    m=a.cross(f.original.E[row],raw);height=a.dot(m,c.V[f.original.edges[row][0]]);weight=beta[0][k]+dx*beta[1][k]+dy*beta[2][k]
    actual+=weight*(a.dot(m,c.act(Rh,c.V[ks[k]]))-height*norm)
   powers=(Q(1),dx,dy,dx*dx,dx*dy,dy*dy)
   D=[[sum((p*component[i][t] for p,component in zip(powers,components)),Q()) for t in range(4)] for i in range(4)];A=j.congruence(D)
   wanted=sum((z[i]*A[i][t]*z[t] for i in range(4) for t in range(4)),Q())
   c.require(actual==wanted,'literal original spatial source/support/force evaluation differs');records.append([leaf,[c.enc(v) for v in (dx,dy,U,V,w)],c.enc(actual)])
 return {'literal_original_spatial_cut_evaluations':len(records),'complete_spatial_fixture_records_sha256':digest(records)}
def bridge_record():
 data,partition=certificate();f=j.Forms()
 # The fixed named source modules are pinned before any import.
 sys.path.insert(0,str(HERE.parent/'three_cube_cover'))
 spec=importlib.util.spec_from_file_location('j74_prior_cover_audit',HERE.parent/'three_cube_cover/check.py');cov=importlib.util.module_from_spec(spec);sys.modules[spec.name]=cov;spec.loader.exec_module(cov)
 import poly
 c.require(Path(poly.__file__).resolve()==HERE.parent/'three_cube_cover/poly.py','actual pinned polynomial identity module')
 cov.validate_frames();hp=cov.permutation(cov.H);mp=cov.permutation(cov.MX);identities,evaluations=cov.audit_actions()
 from poly import Poly,qmul,rotation_homogeneous,mm,scaled
 x,y,U,V,w=[Poly.variable(i,n=5) for i in range(5)];L=F(7,4);M=F(15,4)
 ua=(x+y*w-M*V)*F(4,7);va=(y-x*w+M*U)*F(4,7)
 qg=(Poly(1,n=5),L*va-y+x*w,x+y*w-L*ua,w);qr=(Poly(1,n=5),M*U,M*V,w)
 c.require(qg==qr,'all four universal source decoder components')
 c.require(L*ua==x+y*w-M*V and L*va==y-x*w+M*U and (M-2)*(M-2)-3==F(1,16),'both closed gauge inverses and cube containments')
 # Pure rational universal physical Sy lift, independent of golden-field cuts.
 symbolic_B=((1,M,0,0),(-1,M,0,0),(0,0,M,1),(0,0,-M,1));parameter=(Poly(1,n=5),U,V,w)
 qw=tuple(sum((b*p for b,p in zip(row,parameter)),Poly(0,n=5)) for row in symbolic_B)
 c.require(qmul((1,-1,0,0),qr)==qw,'literal proper Sy quaternion lift')
 c.require(rotation_homogeneous(qw)==scaled(mm(cov.FRAMES[1][1],rotation_homogeneous(qr)),2),'all nine universal physical source rotation entries')
 e=f.eta;face_checks=0
 for dx,dy in product((-e,e),repeat=2):
  X,Y=f.raw[0]+dx,f.raw[1]+dy
  c.require(Y-X>0 and Y+X>0 and Y-1>0,'whole closed original box chooses Sy strictly');face_checks+=3
 qnorm=F(2)+2*M*M;c.require(qnorm==F(241,8),'sharp whole outer rectangle relative quaternion norm')
 # Independently compare moment and direct power conversion on actual forms.
 coefficient_equalities=0
 for depth,code in ((0,0),(7,91),(26,0)):
  W=f.moments(depth,code);lo,hi=c.box(depth,code)
  for A in list(f.holes.values())+[f.gauges[0][0],f.gauges[1][8]]:
   first=j.old.j.moment_coefficients(A,W);second=c.coefficients(A,0,lo,hi)
   c.require(first==second,'two source Bernstein conversion algorithms');coefficient_equalities+=len(first)
 gauge_evaluations=audit_gauges(f)
 physical_audit=audit_physical_forms(f,data)
 # An ACTUAL physical identity fit is outside this canonical rectangle gate.
 # A gauge reject is therefore conditional on the source canonicalization.
 U=Q(F(4,15));z=(Q(1),U,Q(),Q());qworld=c.act(j.B,z)
 c.require(cov.matrix_rotation(qworld)==c.IDENTITY,'physical identity source countercontrol')
 g=(1+f.raw[1])*(1+f.raw[1])-a.dot(f.raw,f.raw);c.require(g>0,'identity fit is genuinely outside the closed canonical gauge')
 return {'agent':'six-rupert-2','role':'researcher','scope':'global degree-preserving rectangle and actual closed original box bridge, independent of old global source classification','certificate_canonical_sha256':digest(data),'partition':partition,'actual_full_body_permutations':[hp,mp],'proper_receiving_frames':3,'universal_quaternion_identity_groups':identities,'independent_numeric_polynomial_evaluations':evaluations,'universal_decoder_component_identities':4,'universal_gate_inverse_identities':2,'universal_Sy_quaternion_lift_components':4,'universal_Sy_rotation_matrix_entries':9,'literal_gauge_polynomial_evaluations':gauge_evaluations,'independent_source_coefficient_equalities':coefficient_equalities,'literal_original_spatial_cut_audit':physical_audit,'strict_receiver_face_corner_checks':face_checks,'source_M':'15/4','sharp_outer_relative_quaternion_norm_squared':'241/8','unit_relative_scalar_squared_lower_bound':'8/241','outer_source_Cayley_volume_ratio':'225/49','identity_physical_fit_outside_canonical_gate':True,'gauge_cut_is_NOT_an_unconditional_physical_nonfit':True,'physical_controls_per_leaf':243,'gauge_controls_per_leaf':81,'hole_controls_per_leaf':27}
def chunk_record(index,data=None,limit=None):
 data,partition=certificate(data);leaves=data['leaves'];n=(len(leaves)+CHUNK_SIZE-1)//CHUNK_SIZE
 c.require(type(index) is int and index in range(n),'actual complete source chunk index')
 start=index*CHUNK_SIZE;end=min(start+CHUNK_SIZE,len(leaves))
 if limit is not None:c.require(type(limit) is int and 0<limit<=end-start,'bounded partial profile');end=start+limit
 f=j.Forms();stream=hashlib.sha256();kinds={'C':0,'G':0,'H':0};minimum={};signs=0
 for number,leaf in enumerate(leaves[start:end],start):
  values=f.coefficients(leaf);c.require(min(values)>0,'strict exact complete receiving/source coefficient at leaf'+str(number))
  kinds[leaf[2]]+=1;signs+=len(values);minimum[leaf[2]]=min(minimum.get(leaf[2],values[0]),min(values));stream.update(c.canonical([leaf,[c.enc(x) for x in values]]));stream.update(b'\n')
 return {'agent':'six-rupert-2','role':'researcher','scope':'every source chunk plus local/coordinate bridges required','certificate_canonical_sha256':digest(data),'chunk_index':index,'chunk_size':CHUNK_SIZE,'required_chunks':n,'leaf_start_inclusive':start,'leaf_end_exclusive':end,'verified_leaf_count':end-start,'partial_profile':limit is not None and end<min(start+CHUNK_SIZE,len(leaves)),'leaf_kinds':kinds,'strict_exact_controls':signs,'minimum_exact_coefficients':{k:c.enc(v) for k,v in minimum.items()},'complete_coefficient_stream_sha256':stream.hexdigest(),'unique_physical_cuts':len(f.cache),'partition':partition}
def controls_record():
 data,_=certificate();f=j.Forms();rejected=[]
 def reject(label,fn):
  try:fn()
  except (ValueError,StopIteration):rejected.append(label);return
  raise ValueError('semantic damage not rejected: '+label)
 bad=copy.deepcopy(data);bad['leaves'].pop(0);reject('missing closed source leaf',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['leaves'][0][1]+=1;reject('wrong source prefix address',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['source_M']=['7/4','0'];reject('shrunk independent source rectangle without coverage',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['canonical_original_hole_indices']=[1,8];reject('omitted third physical equality branch',lambda:certificate(bad))
 reject('unconditional physical exclusion from a canonical gauge',lambda:c.require((1+f.raw[1])*(1+f.raw[1])<=a.dot(f.raw,f.raw),'false unconditional gauge premise'))
 reject('noncanonical old point hole',lambda:f.coefficients([0,0,'H',next(i for i in range(12) if i not in f.holes)]))
 # Immutable inherited matrices need an explicit altered copy.
 damaged=copy.deepcopy(f);A=[list(row) for row in damaged.gauges[0][0]];A[0][0]+=Q(1);damaged.gauges[0][0]=A
 reject('wrong advertised scalar gauge matrix',lambda:c.require(damaged.gauges==[j.old.j.receiver_controls(j.gauge_components(f.raw,i),f.eta) for i in range(2)],'wrong literal gauge'))
 zero=copy.deepcopy(f);zero.gauges[0]=[[[Q() for _ in range(4)] for _ in range(4)] for _ in range(9)]
 reject('closed gauge boundary excluded by a nonstrict sign',lambda:c.require(min(zero.coefficients([0,0,'G',0]))>0,'zero closed gauge boundary'))
 return {'agent':'six-rupert-2','role':'researcher','semantic_damages_rejected':rejected}
def assemble(journal):
 data,part=certificate();n=(len(data['leaves'])+CHUNK_SIZE-1)//CHUNK_SIZE;local=json.loads((journal/'local.json').read_text());bridge=json.loads((journal/'bridge.json').read_text());controls=json.loads((journal/'controls.json').read_text());chunks=[json.loads((journal/f'chunk-{i:02d}.json').read_text()) for i in range(n)]
 for r in (local,bridge,*chunks):c.require(r['certificate_canonical_sha256']==digest(data) and r['partition']==part and r['agent']=='six-rupert-2' and r['role']=='researcher','all original compact certificate records required')
 c.require(local['old_source_exclusion_used_as_premise'] is False and local['source_hole_indices']==[1,8,7] and local['point_hole_Cayley_gate']=='1/33' and local['moving_closed_local_Cayley_gate']=='1/30','whole correct local bridge required')
 c.require(bridge['source_M']=='15/4' and bridge['proper_receiving_frames']==3 and bridge['gauge_cut_is_NOT_an_unconditional_physical_nonfit'] is True,'whole correct actual coordinate bridge required')
 c.require(controls['agent']=='six-rupert-2' and controls['role']=='researcher' and len(controls['semantic_damages_rejected'])==8 and len(set(controls['semantic_damages_rejected']))==8,'eight distinct semantic controls required')
 end=0;signs=0;kinds={'C':0,'G':0,'H':0}
 for i,r in enumerate(chunks):
  c.require(r['chunk_index']==i and r['chunk_size']==CHUNK_SIZE and r['required_chunks']==n and r['leaf_start_inclusive']==end and not r['partial_profile'],'every whole contiguous source chunk required');wanted=min(end+CHUNK_SIZE,len(data['leaves']))
  c.require(r['leaf_end_exclusive']==wanted and r['verified_leaf_count']==wanted-end,'all advertised source leaves required');end=wanted;signs+=r['strict_exact_controls']
  for k in kinds:kinds[k]+=r['leaf_kinds'][k]
 c.require(end==len(data['leaves']) and kinds==part['leaf_kinds'] and signs==part['exact_required_signs'],'entire closed gated source cover required')
 return {'agent':'six-rupert-2','role':'researcher','scope':'complete all-source closed-fit rigidity on the prior closed phase-crossing box, via a new degree-preserving canonical gated source cover; global J74 OPEN','certificate_canonical_sha256':digest(data),'partition':part,'required_completed_chunks':n,'whole_local_record_sha256':digest(local),'whole_coordinate_bridge_sha256':digest(bridge),'whole_semantic_control_record_sha256':digest(controls),'ordered_complete_chunk_records_sha256':digest(chunks),'ordered_coefficient_stream_hashes':[r['complete_coefficient_stream_sha256'] for r in chunks],'original_translation_and_scale_preserved':True,'source_entry_premise':False,'old_full_source_exclusion_is_not_a_premise':True,'partial_shadow_right_quotient':False}
def main():
 p=argparse.ArgumentParser();mode=p.add_mutually_exclusive_group(required=True);mode.add_argument('--local',action='store_true');mode.add_argument('--bridge',action='store_true');mode.add_argument('--controls',action='store_true');mode.add_argument('--chunk',type=int);mode.add_argument('--assemble',type=Path);p.add_argument('--profile',type=int);p.add_argument('--emit',action='store_true');x=p.parse_args()
 c.require(x.profile is None or x.chunk is not None,'partial profiling requires an explicit source chunk')
 if x.local:record=local_record();key='local'
 elif x.bridge:record=bridge_record();key='bridge'
 elif x.controls:record=controls_record();key='controls'
 elif x.chunk is not None:record=chunk_record(x.chunk,limit=x.profile);key='chunks'
 else:record=assemble(x.assemble);key='complete_aggregate'
 record=json.loads(c.canonical(record))
 if not x.emit and x.profile is None:
  expected=json.loads((HERE/'expected.json').read_text());wanted=expected[key][x.chunk] if key=='chunks' else expected[key];c.require(record==wanted,'complete exact record differs from frozen expectations')
 print(json.dumps(record,sort_keys=True,indent=2))
if __name__=='__main__':main()
