#!/usr/bin/env python3
"""Independent geometry, positive witnesses, and exact refutation-CNF audit.

This command does NOT by itself assert a lower chromatic bound. See reproduce.py
for the separately checked UNSAT proof. Generated CNFs stay in --work.
"""
from pathlib import Path
from hashlib import sha256
import argparse,json,time
import radical_check as R
HERE=Path(__file__).resolve().parent

def digest(obj):return sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()
def colour(ee,word,n,k):
 R.require(isinstance(word,str) and len(word)==n and all(c in '0123456'[:k] for c in word),'colour domain')
 R.require(all(word[a]!=word[b] for a,b in ee),'monochromatic edge')
def subset_edges(ee,vs):
 ix={v:i for i,v in enumerate(vs)}
 return [(ix[a],ix[b]) for a,b in ee if a in ix and b in ix]
def verify(work,certificate):
 t=time.monotonic();c=json.loads(certificate.read_text());work.mkdir(parents=True,exist_ok=True)
 pts=R.generate(True);ee=R.edges(pts);colour(ee,c['radius_two_five_word'],len(pts),5)
 text,tri=R.encode(len(pts),ee);(work/'radius_two.cnf').write_text(text)
 vs=c['selected_radius_two_ids'];R.require(vs==sorted(set(vs)) and all(type(v)==int and 0<=v<len(pts) for v in vs),'selected point IDs')
 se=subset_edges(ee,vs);colour(se,''.join(c['radius_two_five_word'][v] for v in vs),len(vs),5)
 selected_text,selected_tri=R.encode(len(vs),se);(work/'selected.cnf').write_text(selected_text)
 fixed=set(c['radius_two_fixed_482']);R.require(len(fixed)==482 and fixed<=set(range(len(pts))),'482-point base')
 adj=[set() for _ in pts]
 for a,b in ee:adj[a].add(b);adj[b].add(a)
 pool=sorted(fixed|{v for v in range(len(pts)) if len(adj[v]&fixed)>=2});pe=subset_edges(ee,pool)
 colour(pe,c['radius_two_two_neighbor_pool_word'],len(pool),4)
 full=R.generate(False);fe=R.edges(full);colour(fe,c['untruncated_five_word'],len(full),5)
 R.require(set(pts)<=set(full),'lower-bound subgraph containment')
 base=c['untruncated_fixed_503'];R.require(base==sorted(set(base)) and len(base)==503 and all(0<=v<len(full) for v in base),'503-point base')
 R.require(sorted(c['record_map'].values())==base,'record map target')
 R.require(sorted(map(int,c['record_map']))+[]==sorted(set(range(509))-set(c['missing_original_indices'])),'record map source')
 small=c['subrecord_control']['vertices'];R.require(small==sorted(set(small)) and set(base)<=set(small) and len(small)<=508,'sub-record control')
 sce=subset_edges(fe,small);colour(sce,c['subrecord_control']['word'],len(small),4)
 # Definition-level geometry and certificate corruption controls.
 R.require(R.unit((96,0,0,0,0,0,0,0)) and not R.unit((0,)*8),'unit/zero controls')
 bad=(40,0,-8,0,40,0,-8,0)
 R.require(R.norm_compact(bad)[0]==9216 and not R.unit(bad),'irrational norm control')
 damaged=list(c['radius_two_five_word']);a,b=ee[0];damaged[a]=damaged[b]
 try:colour(ee,''.join(damaged),len(pts),5)
 except ValueError:pass
 else:raise ValueError('corrupt colour accepted')
 result={'status':'EXACT GEOMETRY, FIVE-COLOUR UPPER BOUNDS AND CNFS VERIFIED; RUN PROOF CHECK FOR LOWER BOUNDS',
  'radius_two':{'vertices':len(pts),'edges':len(ee),'points_sha256':digest(pts),'edges_sha256':digest(ee),'triangle':list(tri),'cnf_sha256':sha256(text.encode()).hexdigest()},
  'selected':{'vertices':len(vs),'edges':len(se),'ids_sha256':digest(vs),'triangle':list(selected_tri),'cnf_sha256':sha256(selected_text.encode()).hexdigest()},
  'untruncated':{'vertices':len(full),'edges':len(fe),'points_sha256':digest(full),'edges_sha256':digest(fe)},
  'two_neighbor_pool':{'vertices':len(pool),'edges':len(pe),'four_colourable':True},
  'subrecord_control':{'vertices':len(small),'edges':len(sce),'four_colourable':True},
  'physical_pairs_checked':len(pts)*(len(pts)-1)//2+len(full)*(len(full)-1)//2,
  'seconds':time.monotonic()-t}
 (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--check-expected',action='store_true');a=p.parse_args()
 result=verify(a.work,a.certificate)
 if a.check_expected:
  expected=json.loads((HERE/'EXPECTED.json').read_text());R.require({k:v for k,v in result.items() if k!='seconds'}==expected,'expected output mismatch')
 print(json.dumps(result,indent=2))
