#!/usr/bin/env python3
"""Reuse the published overlap census to document the inner-gadget selection.

This reads certified metadata, not a new exhaustive geometry enumeration.
The selected geometry is rebuilt independently by verify.py and controls.py.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import lzma,json
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'hadwiger_nelson_nonmono159_overlap10'
def checked(name,pin):
 raw=(OLD/name).read_bytes()
 if sha256(raw).hexdigest()!=pin:raise ValueError('catalogue input mismatch')
 return lzma.decompress(raw).decode().splitlines()
def main():
 transforms=[]
 for line in checked('overlap_transforms.txt.xz','96a88e026cda4892404feac63f0e2ee85f3e05785ba2bf6ff0671e593d9a779d'):
  if not line.startswith('placement='):continue
  r=dict(z.split('=') for z in line.split(';'))
  t=tuple(int(r[k]) for k in ('reflected','denominator'))+tuple(tuple(map(int,r[k].split(','))) for k in ('c','s','tx','ty'))
  transforms.append((t,int(r['placement'])))
 transforms.sort();rows=[]
 for line in checked('colorings.txt.xz','449dbf4640fef549897c4dd14aa5c8a5463571881b448b673d7e30a38abf75ad'):
  if not line.startswith('graph='):continue
  r=dict(z.split('=') for z in line.split(';'));i=int(r['graph']);n=int(r['order']);m=int(r['edges'])
  if i!=len(rows) or n!=318-transforms[i][1] or r['status']!='SAT' or len(r['colors'])!=n:raise ValueError('inconsistent catalogue metadata')
  rows.append((i,n,m))
 if len(rows)!=len(transforms) or len(rows)!=30013:raise ValueError('incomplete catalogue')
 eligible=[r for r in rows if r[1]<=294];maximum=max(m for _,_,m in eligible);best=[r for r in eligible if r[2]==maximum]
 chosen=16347;t,k=transforms[chosen]
 if t!=(1,1,(1,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(5,0,0,0,0,1,0,0),(0,5,0,0,-1,0,0,0)) or k!=25:raise ValueError('wrong selected isometry')
 import verify as M
 A=M.F.read_points(159);image=[(a+5,b+1,5-c,-1-d) for a,b,c,d in A];B=list(dict.fromkeys(A+image));idx={b:i for i,b in enumerate(B)}
 ea=set(M.F.edges(A,12));ei={tuple(sorted((idx[image[i]],idx[image[j]]))) for i,j in ea};eb=set(M.F.edges(B,12))
 print(json.dumps({'catalogue_entries':len(rows),'eligible_entries':len(eligible),'eligible_distinct_orthogonal_parts':len({transforms[i][0][:4] for i,n,m in eligible}),'largest_recorded_edge_count':maximum,'maximizers':best,'selected_graph_index':chosen,'selected_overlap':k,'selected_vertices':len(B),'selected_strict_edges':len(eb),'shared_inherited_edges':len(ea&ei),'new_inner_cross_edges':len(eb-(ea|ei)),'selection_reuses_durable_census':True},indent=2))
if __name__=='__main__':main()
