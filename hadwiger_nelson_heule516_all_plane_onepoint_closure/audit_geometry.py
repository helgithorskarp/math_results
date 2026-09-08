from pathlib import Path
from itertools import combinations
from collections import Counter
from fractions import Fraction as F
from math import comb,lcm
import json,importlib.util,time,hashlib
import argparse
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
a=ap.parse_args();OUT=a.work;OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('independent_field_audit',REPO/'hadwiger_nelson_heule510_completion_frontier/audit.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
start=time.monotonic();sp=REPO/'hadwiger_nelson_h516_degree4_surgeries/SOURCE.json'
if hashlib.sha256(sp.read_bytes()).hexdigest()!='3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51':raise ValueError('Source hash')
s=json.loads(sp.read_text());V=s['labels'];H96=[tuple(tuple(a) for a in p) for p in s['coordinates']];H=[tuple(tuple(F(c,96) for c in a) for a in p) for p in H96]
if len(V)!=516 or len(set(H))!=516:raise ValueError('Source size')
lines=(OUT/'points.txt').read_text().splitlines()
if lines[0]!='516 96' or [list(map(int,x.split())) for x in lines[1:]]!=[[c for a in p for c in a] for p in H96]:raise ValueError('Filter coordinate stream')
edges=[[V[i],V[j]] for i,j in combinations(range(516),2) if m.distance(H96[i],H96[j])==(9216,0,0,0,0,0,0,0)]
if edges!=s['edges']:raise ValueError('Exact source edges')
# Reconstruct H632 membership by the original rational input tables.
old=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
old_labels=[v for v in sorted(map(int,old['coordinates'])) if '510' in old['provenance'][v]]
host=[m.parse(old['coordinates'][str(v)]) for v in old_labels]+[m.parse(r['coordinates']) for r in json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())]
if len(host)!=632 or len(set(host))!=632 or [host[v] for v in V]!=H:raise ValueError('H632 and base coordinate identity')
host_set=set(host);rows=json.loads((OUT/'centres.json').read_text());centres=[m.parse(r['coordinates']) for r in rows]
if centres!=sorted(set(centres)):raise ValueError('Centre canonical order')
scaled={96:H96};cover=set();exterior=[];degrees=Counter();denoms=Counter()
for i,(q,row) in enumerate(zip(centres,rows)):
    D=lcm(96,*(c.denominator for a in q for c in a));denoms[D]+=1
    if D not in scaled:scaled[D]=[m.integer_point(p,D) for p in H]
    qi=m.integer_point(q,D);unit=(D*D,0,0,0,0,0,0,0);ns=[j for j,p in enumerate(scaled[D]) if m.distance(qi,p)==unit]
    if ns!=row['neighbors'] or len(ns)<3:raise ValueError('Incorrect centre incidence '+str(i))
    if len(row['witness'])!=3 or row['witness']!=sorted(set(row['witness'])) or not set(row['witness'])<=set(ns):raise ValueError('Witness triple')
    for t in combinations(ns,3):
        if t in cover:raise ValueError('Repeated triple across distinct centres')
        cover.add(t)
    if len(ns)>=4 and q not in host_set:exterior.append({'centre_index':i,**row});degrees[len(ns)]+=1
    if i%400==0:print(json.dumps({'audited_centres':i+1,'seconds':time.monotonic()-start}),flush=True)
survivors=[tuple(map(int,line.split())) for line in (OUT/'survivors.tsv').read_text().splitlines()]
if survivors!=sorted(set(survivors)) or any(len(t)!=3 or not(0<=t[0]<t[1]<t[2]<516) for t in survivors):raise ValueError('Survivor domain')
if not cover<=set(survivors):raise ValueError('Real centre omitted from modular stream')
false=sorted(set(survivors)-cover)
for a,b,c in false:
    if m.exact_unit_triple(H96[a],H96[b],H96[c],96):raise ValueError('Unaccounted real unit-circle triple')
if [list(t) for t in false]!=json.loads((OUT/'rejected.json').read_text()):raise ValueError('Rejected stream')
if exterior!=json.loads((OUT/'exterior.json').read_text()):raise ValueError('Exterior set mismatch')
flt=json.loads((OUT/'FILTER.json').read_text())
if flt['vertices']!=516 or flt['triples']!=comb(516,3) or flt['second_survivors']!=len(survivors):raise ValueError('Filter count')
result={'status':'EXACT_WHOLE_PLANE_EXTERNAL_CENTRE_CENSUS_VERIFIED','base_vertices':516,'base_edges':len(edges),'all_base_pair_checks':comb(516,2),'all_base_triples_enumerated':flt['triples'],'all_centres':len(rows),'centre_base_pair_checks':len(rows)*516,'survivor_triples_compared_entrywise':len(survivors),'modular_false_positives':len(false),'external_degree_at_least_four_points':len(exterior),'external_degree_histogram':dict(sorted(degrees.items())),'coordinate_denominator_histogram':dict(sorted(denoms.items())),'exterior_sha256':hashlib.sha256((OUT/'exterior.json').read_bytes()).hexdigest(),'centres_sha256':hashlib.sha256((OUT/'centres.json').read_bytes()).hexdigest(),'survivors_sha256':hashlib.sha256((OUT/'survivors.tsv').read_bytes()).hexdigest(),'seconds':time.monotonic()-start,'trust':'Independent monomial exponent arithmetic and complete entrywise incidence/triple audit; native modular filter supplies exhaustive superset.'}
(OUT/'GEOMETRY_AUDIT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2),flush=True)
