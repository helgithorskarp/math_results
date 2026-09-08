"""Finish an exhaustive sieve by exact radical norms on every survivor."""
from pathlib import Path
import json,struct,sys,time,hashlib
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve();sys.path.insert(0,str(P))
from audit_source import norm,require
start=time.monotonic();source=json.loads((P/'exact_points.json').read_text());pts=source['points'];den=source['denominator'];n=len(pts)
control=json.loads((P/'sieve_controls.json').read_text());require(control['verified'],'sieve validation prerequisite')
run=json.loads((P/'full_sieve.json').read_text());require(run['vertices']==n and run['pairs']==n*(n-1)//2,'all pairs covered')
raw=(P/'full_sieve.bin').read_bytes();require(len(raw)==8*run['survivors'],'survivor byte count');pairs=list(struct.iter_unpack('<II',raw))
require(pairs==sorted(set(pairs)),'canonical pair census');require(all(0<=u<v<n for u,v in pairs),'pair labels')
actual=[];false=[];want=(den*den,)+(0,)*7
for u,v in pairs:
 d=tuple(x-y for x,y in zip(pts[u],pts[v]));d=min(d,tuple(-x for x in d))
 if norm(d)==want:actual.append([u,v])
 else:false.append({'pair':[u,v],'norm_coefficients':norm(d)})
expected=json.loads((P/'exact_edges.json').read_text());require(actual==expected,'strict edge census equals supplied edges')
(P/'sieve_false_positives.json').write_text(json.dumps(false,indent=2)+'\n')
out={'verified':True,'vertices':n,'all_pairs_examined':run['pairs'],'modular_survivors':len(pairs),'char_zero_unit_pairs':len(actual),'modular_false_positives':len(false),'distinct_exact_norms_evaluated':norm.cache_info().currsize,'full_strict_graph_equals_author_graph':True,'arithmetic':'necessary evaluation in Z[sqrt2,sqrt3,sqrt5,1/96] modulo 1000000009; every surviving pair tested in characteristic zero','integer_overflow_bound':2*(1000000009-1)**2,'CXX_scan_seconds':run['elapsed_seconds'],'exact_finish_seconds':time.monotonic()-start,'survivor_file_sha256':hashlib.sha256(raw).hexdigest(),'edges_sha256':hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest(),'new_vertices':0,'new_colour_queries':0,'chromatic_lower_bound_reproved':False}
(P/'strict_census.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
