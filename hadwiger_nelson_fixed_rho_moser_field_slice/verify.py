"""Rebuild the entire exact K phase census and directly audit every unit graph."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from math import lcm
import argparse,hashlib,json,subprocess
import model as m
HERE=Path(__file__).resolve().parent
def need(b,s):
 if not b:raise ValueError(s)
def canon(x):return json.dumps(x,separators=(',',':'),sort_keys=True).encode()
def flatmul(a,b):
 # Independent bit-mask multiplication for the real field, followed by i sqrt3.
 z=[0]*8
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   t=x*y;bits=i&j
   for k,p in enumerate([5,33,-3]):
    if bits>>k&1:t*=p
   z[i^j]+=t
 return tuple(z)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--audit-binary',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);args=ap.parse_args();args.work.mkdir(parents=True,exist_ok=True)
 data=json.loads((HERE/'certificate.json').read_text());den,M,B,addresses,generic,lines,phases,stats=m.inventory()
 need(len(set(M))==7 and len(B)==49 and len(addresses)==343,'source point counts')
 keys=sorted(phases);phasehash=hashlib.sha256(canon([m.encode(v)for v in keys])).hexdigest()
 need(phasehash==data['phase_sha256'],'phase identity/order')
 need(len(data['word_indices'])==len(keys),'case count')
 words=data['words'];need(all(len(w)==343 and set(w)<=set('0123')for w in words),'word alphabet')
 g=words[data['generic_word']];need(all(g[a]!=g[b]for a,b in generic),'generic colouring')
 base_edges=[(i,j)for i,j in combinations(range(7),2)if m.norm(m.sub(M[i],M[j]))==(den*den,0,0,0)]
 need(len(base_edges)==11 and all(any(c[a]==c[b]for a,b in base_edges)for c in product(range(3),repeat=7)),'Moser lower bound')
 geometry_file=args.work/'direct-geometry.txt';point_counts={};edge_counts={};expanded_checks=0
 generic_set=set(generic)
 with geometry_file.open('w')as out:
  out.write(str(len(keys))+'\n')
  for v,wi in zip(keys,data['word_indices']):
   need(type(wi)is int and 0<=wi<len(words),'word pointer');w=words[wi];r=phases[v];E0=sorted(generic_set|r['edges'])
   need(all(w[a]!=w[b]for a,b in E0),'event word');need(all(w[a]==w[b]for a,b in r['collisions']),'collision word')
   labels,E=m.merged_graph(343,E0,r['collisions']);n=1+max(labels)
   point_counts[n]=point_counts.get(n,0)+1;edge_counts[len(E)]=edge_counts.get(len(E),0)+1;expanded_checks+=len(E0)
   # Construct coordinates independently using flat basis products, not m.mul.
   vd=lcm(*(x.denominator for x in v));vn=tuple(int(x*vd)for x in v);D=den*vd
   points=[tuple(x*vd+y for x,y in zip(a,flatmul(vn,b)))for a,b in addresses]
   need(len(set(points))==n,'direct distinct points')
   out.write(f'343 {D} {n} {len(E)}\n')
   for p,c in zip(points,w):out.write(' '.join(map(str,p))+' '+c+'\n')
   for a,b in E:out.write(f'{a} {b}\n')
 with geometry_file.open('r')as inp:
  run=subprocess.run([str(args.audit_binary.resolve())],stdin=inp,capture_output=True,text=True)
 need(run.returncode==0,'direct audit failed: '+run.stderr)
 audit=json.loads(run.stdout);need(audit['cases']==len(keys),'audit case coverage')
 result=stats|{'status':'COMPLETE_FIXED_RHO_K_SLICE_FOUR_CHROMATIC','phase_sha256':phasehash,'colour_words':len(words),'expanded_unit_incidences_checked':expanded_checks,'physical_point_histogram':point_counts,'physical_edges_min':min(edge_counts),'physical_edges_max':max(edge_counts),'collision_merged':True,'generic_phase_coloured':True,'exact_direct_audit':audit,'record_candidate':False,'full_independent_two_phase_family_closed':False,'outside_K_phases_closed':False,'old_a8_reopened':False}
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
