#!/usr/bin/env python3
"""Reconstruct the exact open residual and verify every available positive cut."""
from pathlib import Path
import argparse,importlib.util,json,hashlib
import reduction
HERE=Path(__file__).resolve().parent;REPO=HERE.parent

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def check_positive(row,U,E,words):
 D=row['D'];ds=set(D);c=row['c'];reduction.require(D==sorted(ds) and ds<=set(U),'cut labels')
 reduction.require(len(c)==303 and set(c)<=set('.0123') and {v for v,t in zip(U,c) if t=='.'}==ds,'pool word domain')
 if 'l' in row:l=row['l']
 else:
  p=row['p'];reduction.require(type(p)is int and 0<=p<20,'class index');l=words[p]
 reduction.require(len(l)==374 and set(l)<=set('0123'),'source word')
 col=dict(enumerate(l));col.update({v:t for v,t in zip(U,c) if t!='.'})
 reduction.require(all(col[a]!=col[b] for a,b in E if a in col and b in col),'positive word fails a physical edge')
 return len(col)

def check_selection(X,U,E,points,cuts):
 xs=set(X);S=set(U[:135]);Q=set(U[135:]);vs=set(range(374))|xs
 reduction.require(X==sorted(xs) and xs<=set(U),'selection labels')
 reduction.require(len(xs&S)==126 and len(xs&Q)==8 and len({points[v] for v in vs})==508,'exact a8 point budget')
 reduction.require(all(xs&set(D) for D in cuts),'separator does not meet earlier cuts')
 adj={v:set() for v in vs}
 for a,b in E:
  if a in vs and b in vs:adj[a].add(b);adj[b].add(a)
 reduction.require(all(len(adj[q])>=4 for q in xs&Q),'separator degree condition')
 return sum(a in vs and b in vs for a,b in E)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--positive-cache',type=Path);args=ap.parse_args();args.work.mkdir(parents=True,exist_ok=True)
 accepted=module('accepted_a8_geometry',REPO/'hadwiger_nelson_parts509_shape8_transfer/verify.py')
 den,points,vertices,U,E,words,pins=accepted.inputs();seed,hashes=accepted.old_constraints(U)
 reduction.require(hashes==json.loads((REPO/'hadwiger_nelson_parts509_shape8_transfer/seed_hashes.json').read_text()),'pinned old cut families')
 cuts=sorted(seed,key=lambda D:(len(D),D));rows=json.loads((HERE/'baseline_cuts.json').read_text());edges=[]
 for row in rows:
  check_positive(row,U,E,words);edges.append(check_selection(row['excluded_X'],U,E,points,cuts));reduction.require(not set(row['D'])&set(row['excluded_X']),'strict historical cut separator');cuts.append(row['D'])
 reduction.require(len(cuts)==17269 and len({tuple(D) for D in cuts})==17269,'frozen baseline cut count')
 cached=0
 if args.positive_cache:
  seen=set()
  with args.positive_cache.open() as f:
   for line in f:
    row=json.loads(line);D=tuple(row['D']);reduction.require(D not in seen,'duplicate cached cut');check_positive(row,U,E,words);seen.add(D)
  reduction.require(seen=={tuple(D) for D in cuts},'incomplete positive cache');cached=len(seen)
 nv,clauses,index,adj,meanings=reduction.build(U,E,cuts);cnf=args.work/'residual.cnf';cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
 result={'status':'RESIDUAL_REDUCTION_AND_ALL_POSITIVE_CUTS_VERIFIED' if cached else 'RESIDUAL_REDUCTION_VERIFIED_OLD_CUT_THEOREMS_IMPORTED','physical_points':len(vertices),'physical_edges':len(E),'denominator':den,'selection_points':508,'baseline_cut_count':len(cuts),'detached_cut_sizes':[len(r['D']) for r in rows],'historical_separating_support_edges':edges,'all_positive_words_checked':cached,'cnf_variables':nv,'cnf_clauses':len(clauses),'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),'strict_shrink_beyond_three_cut_baseline':False,'global_closure_claimed':False,'record_candidate':False}
 print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
