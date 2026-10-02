#!/usr/bin/env python3
"""Exact bounded checks for all source fits across a true J74 receiver seam.

Standard library only. Full local proof and every contiguous source chunk are
required. A profile, a numerical forest proposal or journal assembly alone is
not a proof. Explicit exceptions retain every gate under optimized execution.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,copy,hashlib,importlib.util,json,sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('j74_cross_forms',HERE/'forms.py')
j=importlib.util.module_from_spec(spec);sys.modules[spec.name]=j;spec.loader.exec_module(j)
c,a,Q,l=j.c,j.a,j.Q,j.l
CHUNK_SIZE=512
def digest(x):return hashlib.sha256(c.canonical(x)).hexdigest()
def certificate(data=None):
 if data is None:data=json.loads((HERE/'certificate.json').read_text())
 c.require(set(data)=={'schema','agent','role','scope','algorithm_source_commit','geometry_source_commit',
  'parent_pose_certificate_canonical_sha256','raw_center','raw_halfwidth','local_Cayley_gate',
  'point_hole_gate','physical_rotation_bases','leaves'},'entire compact certificate schema')
 c.require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','actual certificate author and schema')
 c.require(data['algorithm_source_commit']==l.DEPENDENCIES['algorithm_source_commit'] and data['geometry_source_commit']==l.DEPENDENCIES['geometry_source_commit'],'pinned exact source provenance')
 parent=json.loads((c.HERE/'certificate.json').read_text())
 c.require(data['parent_pose_certificate_canonical_sha256']==digest(parent),'whole pinned parent pose/contact certificate')
 c.require(data['raw_center']==[['2315/1798','-453/1798'],['2211/1798','205/1798'],['-1','0']]
  and data['raw_halfwidth']==['1/1000','0'] and data['local_Cayley_gate']==['1/30','0'] and data['point_hole_gate']==['1/33','0'],
  'literal entire receiver box and derived local/source-hole gates')
 return data,c.validate_partition(data['leaves'])
def local_record():
 data,charts=certificate();math=l.preflight(data)
 return {'agent':'six-rupert-2','role':'researcher','kind':'whole closed phase-crossing box conditional local bridge',
  'certificate_canonical_sha256':digest(data),'whole_local_mathematical_record_sha256':digest(math),
  'raw_center':math['raw_center'],'raw_halfwidth':math['raw_halfwidth'],
  'common_actual_original_edges':[[i,j] for i,j in math['common_actual_original_edges']],
  'fifteen_common_receiver_corner_comparisons':math['fifteen_common_receiver_corner_comparisons'],
  'full_piecewise_receiver_comparisons':math['full_piecewise_receiver_comparisons'],
  'full_piecewise_source_comparisons':math['full_piecewise_source_comparisons'],
  'raw_closed_phase_polygon_vertices':[x['raw_closed_polygon_vertices'] for x in math['receiving_closed_phase_regions']],
  'actual_true_closed_phase_cycles':[x['original_cycle'] for x in math['receiving_closed_phase_regions']],
  'raw_signed_rotation_families':len(math['raw_families']),
  'uniform_coordinate_contact_mass_bounds':math['uniform_coordinate_contact_mass_bounds'],
  'uniform_common_contact_quadratic_constant':math['uniform_common_contact_quadratic_constant'],
  'closed_local_Cayley_Euclidean_gate':math['closed_local_Cayley_Euclidean_gate'],
  'squared_local_absorption_bound':math['squared_local_absorption_bound'],
  'point_reference_hole_Cayley_gate':math['point_reference_hole_Cayley_gate'],
  'proper_distinct_equal_shadow_branches':len(math['proper_point_pose_rows']),
  'closed_chart_leaf_counts':charts}
def chunk_record(index,profile=None,data=None):
 data,charts=certificate(data);leaves=data['leaves'];n=(len(leaves)+CHUNK_SIZE-1)//CHUNK_SIZE
 c.require(type(index) is int and index in range(n),'actual bounded source chunk index')
 start=index*CHUNK_SIZE;end=min(start+CHUNK_SIZE,len(leaves))
 if profile is not None:
  c.require(type(profile) is int and 0<profile<=end-start,'bounded partial source profile');end=start+profile
 forms=j.Forms();stream=hashlib.sha256();counts={'C':0,'H':0};minimum={};checks=0
 for number,leaf in enumerate(leaves[start:end],start):
  values=forms.exact_leaf_coefficients(leaf)
  c.require(min(values)>0,'strict exact whole receiver/source sign at actual source leaf'+str(number))
  counts[leaf[3]]+=1;checks+=len(values);minimum[leaf[3]]=min(minimum.get(leaf[3],values[0]),min(values))
  stream.update(c.canonical([leaf,[c.enc(x) for x in values]]));stream.update(b'\n')
 return {'agent':'six-rupert-2','role':'researcher','scope':'bounded exact source chunk; local bridge and every other chunk remain required',
  'certificate_canonical_sha256':digest(data),'chunk_index':index,'chunk_size':CHUNK_SIZE,'required_chunks':n,
  'leaf_start_inclusive':start,'leaf_end_exclusive':end,'verified_leaf_count':end-start,
  'profile_partial':profile is not None and end<min(start+CHUNK_SIZE,len(leaves)),
  'verified_leaf_kinds':counts,'strict_joint_Bernstein_coefficient_count':checks,
  'minimum_exact_Bernstein_coefficients':{k:c.enc(v) for k,v in minimum.items()},
  'complete_chunk_coefficient_stream_sha256':stream.hexdigest(),'unique_exact_cut_forms':len(forms.cache),
  'closed_chart_leaf_counts':charts,'source_quaternion_charts':4,'actual_common_stresses':len(forms.circuits),
  'exact_receiver_polynomial_force_component_identities':len(forms.circuits)*6*3}
def assemble(local,chunks):
 data,charts=certificate();leaves=data['leaves'];n=(len(leaves)+CHUNK_SIZE-1)//CHUNK_SIZE
 c.require(len(chunks)==n and local['certificate_canonical_sha256']==digest(data),'entire local bridge and all source chunks required')
 end=0;counts={'C':0,'H':0};checks=0
 for index,rec in enumerate(chunks):
  c.require(rec['chunk_index']==index and rec['leaf_start_inclusive']==end and not rec['profile_partial'],'ordered source ranges without missing or partial job')
  c.require(rec['certificate_canonical_sha256']==digest(data),'actual complete forest fingerprint')
  wanted=min(end+CHUNK_SIZE,len(leaves));c.require(rec['leaf_end_exclusive']==wanted and rec['verified_leaf_count']==wanted-end,'whole contiguous actual source range')
  end=wanted;checks+=rec['strict_joint_Bernstein_coefficient_count']
  for kind in counts:counts[kind]+=rec['verified_leaf_kinds'][kind]
 c.require(end==len(leaves) and counts=={k:sum(x[3]==k for x in leaves) for k in counts},'whole four-chart source cover')
 c.require(checks==243*counts['C']+27*counts['H'],'entire advertised exact coefficient inventory')
 return {'agent':'six-rupert-2','role':'researcher','scope':'all-source closed-fit rigidity on an entire J74 receiving box across a true support phase wall; global J74 OPEN',
  'certificate_canonical_sha256':digest(data),'verified_source_leaves':len(leaves),'verified_leaf_kinds':counts,
  'strict_exact_joint_Bernstein_coefficient_count':checks,'closed_chart_leaf_counts':charts,'required_completed_source_chunks':n,
  'whole_local_mathematical_record_sha256':local['whole_local_mathematical_record_sha256'],
  'ordered_complete_chunk_records_sha256':digest(chunks),'coefficient_stream_hashes_in_chunk_order':[x['complete_chunk_coefficient_stream_sha256'] for x in chunks],
  'raw_receiving_center':data['raw_center'],'raw_receiving_halfwidth':data['raw_halfwidth'],
  'actual_equal_shadow_motions':12,'source_entry_hypothesis':False,'arbitrary_original_translation_retained':True,
  'all_scales_at_least_one':True,'includes_all_halfturns':True,'closed_actual_receiver_phase_seam_retained':True,
  'necessary_common_supports_only':15,'common_stresses':108,'local_verification_and_all_chunks_required':True}
def audits():
 count=0
 for chart in range(4):
  for depth,code in ((0,0),(7,91)):
   lo,hi=c.box(depth,code);W=j.j.quaternion_moments(chart,lo,hi)
   for i in range(4):
    for k in range(i,4):
     B=[[Q() for _ in range(4)] for _ in range(4)];B[i][k]=Q(1);B[k][i]=Q(1)
     x=c.coefficients(B,chart,lo,hi);y=j.j.moment_coefficients(B,W)
     c.require(x==y,'two exact source conversion algorithms on the entire symmetric matrix basis');count+=len(x)
 e=Q(F(1,1000));basis=((1,-2,1),(0,2,-2),(0,0,1));other=0
 for monomial in range(6):
  components=[[[Q() for _ in range(4)] for _ in range(4)] for _ in range(6)];components[monomial][0][0]=Q(1)
  controls=[B[0][0] for B in j.j.receiver_controls(components,e)];expanded=[[Q() for _ in range(3)] for _ in range(3)]
  for (i,k),v in zip(product(range(3),repeat=2),controls):
   for x in range(3):
    for y in range(3):expanded[x][y]+=v*basis[i][x]*basis[k][y]
  wanted=[[Q() for _ in range(3)] for _ in range(3)]
  if monomial==0:wanted[0][0]=Q(1)
  elif monomial==1:wanted[0][0]=-e;wanted[1][0]=2*e
  elif monomial==2:wanted[0][0]=-e;wanted[0][1]=2*e
  elif monomial==3:wanted[0][0]=e*e;wanted[1][0]=-4*e*e;wanted[2][0]=4*e*e
  elif monomial==4:wanted[0][0]=e*e;wanted[1][0]=-2*e*e;wanted[0][1]=-2*e*e;wanted[1][1]=4*e*e
  else:wanted[0][0]=e*e;wanted[0][1]=-4*e*e;wanted[0][2]=4*e*e
  c.require(expanded==wanted,'all receiver Bernstein powers re-expand exactly');other+=9
 return {'quaternion_basis_coefficient_equalities':count,'receiver_ordinary_coefficient_equalities':other}
def damages():
 data,charts=certificate();passed=[]
 def reject(label,fn):
  try:fn()
  except (ValueError,StopIteration,ZeroDivisionError):passed.append(label)
  else:raise ValueError('damaged mathematical control accepted: '+label)
 bad=copy.deepcopy(data);bad['leaves'].pop(0);reject('missing entire closed source leaf',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['leaves']=[x for x in bad['leaves'] if x[0]!=3];reject('omitted original halfturn component chart',lambda:certificate(bad))
 leaf=next(x[:] for x in data['leaves'] if x[3]=='C');leaf[5:]=[0]*len(leaf[5:])
 reject('wrong original source labels in force cut',lambda:c.require(min(j.Forms().exact_leaf_coefficients(leaf))>0,'wrong source gap'))
 bad=copy.deepcopy(data);x=bad['physical_rotation_bases'][0]['literal_original_contacts'][0];x[2]=next(i for i in range(60) if i not in x[:2])
 reject('noncontact source point in physical basis',lambda:l.preflight(bad))
 bad=copy.deepcopy(data);bad['raw_halfwidth']=['1/500','0'];reject('enlarged receiver box without proof',lambda:certificate(bad))
 bad=copy.deepcopy(data);bad['local_Cayley_gate']=['1/15','0'];reject('unsupported nonlinear local collar',lambda:certificate(bad))
 def wrong_phase():
  raw=tuple(c.field(x) for x in data['raw_center']);r=a.add(raw,(-Q(F(1,1000)),Q(F(1,1000)),Q()))
  m=a.cross(a.sub(c.V[56],c.V[48]),r);h=a.dot(m,c.V[48])
  c.require(all(a.dot(m,v)<=h for v in c.V),'false fixed17corner old support beyond wall')
 reject('discarding the actual receiving phase change',wrong_phase)
 def missing_companion():
  raw=tuple(c.field(x) for x in data['raw_center']);Mn=tuple(tuple(c.IDENTITY[i][k]-2*raw[i]*raw[k]/a.dot(raw,raw) for k in range(3)) for i in range(3))
  Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
  base=[c.matrix(x['proper_matrix_rows']) for x in json.loads((c.HERE/'certificate.json').read_text())['poses']]
  companion=c.matmul(c.matmul(Mn,base[0]),Mx);c.proper(companion)
  c.require(companion in base,'false omission of real proper companion equality branch')
 reject('omitting real proper reflection companions',missing_companion)
 return {'semantic_damaged_controls_rejected':passed,'algebra_audits':audits()}
def main():
 parser=argparse.ArgumentParser();mode=parser.add_mutually_exclusive_group()
 mode.add_argument('--local',action='store_true');mode.add_argument('--controls',action='store_true');mode.add_argument('--chunk',type=int);mode.add_argument('--assemble',type=Path)
 parser.add_argument('--profile',type=int);parser.add_argument('--emit',action='store_true');args=parser.parse_args()
 c.require(args.profile is None or args.chunk is not None,'profile only selects part of one source chunk')
 if args.local:record=local_record()
 elif args.controls:record=damages()
 elif args.chunk is not None:record=chunk_record(args.chunk,args.profile)
 elif args.assemble is not None:
  data,_=certificate();n=(len(data['leaves'])+CHUNK_SIZE-1)//CHUNK_SIZE
  record=assemble(json.loads((args.assemble/'local.json').read_text()),[json.loads((args.assemble/f'chunk-{i:02d}.json').read_text()) for i in range(n)])
 else:raise ValueError('choose --local, --controls, --chunk or --assemble; all are required for the whole proof')
 if not args.emit and args.profile is None:
  expected=json.loads((HERE/'expected.json').read_text())
  key='local' if args.local else 'controls' if args.controls else 'chunks' if args.chunk is not None else 'complete_aggregate'
  wanted=expected[key][args.chunk] if args.chunk is not None else expected[key]
  c.require(record==wanted,'entire mathematical record differs from frozen expected')
 print(json.dumps(record,sort_keys=True,indent=2))
if __name__=='__main__':main()
