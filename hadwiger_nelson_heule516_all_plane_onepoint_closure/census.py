from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
from math import comb
import json, importlib.util, hashlib, subprocess, time
import argparse
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--filter',type=Path,required=True)
a=ap.parse_args();OUT=a.work;OUT.mkdir(parents=True,exist_ok=True)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
geom=load('previous_exact_centres',REPO/'hadwiger_nelson_heule510_completion_frontier/census.py')
old=load('onepoint_input',REPO/'hadwiger_nelson_heule516_single_point_h632_closure/verify.py')
if (OUT/'centres.json').exists():raise ValueError('Use a fresh work directory; census already exists')
start=time.monotonic();source_path=REPO/'hadwiger_nelson_h516_degree4_surgeries/SOURCE.json'
if hashlib.sha256(source_path.read_bytes()).hexdigest()!='3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51':raise ValueError('Source hash')
source=json.loads(source_path.read_text());labels=source['labels'];H=[tuple(tuple(F(x,96) for x in axis) for axis in row) for row in source['coordinates']]
host,edges,_=old.exact_geometry();base,h560,inside=old.source_supports()
if labels!=sorted(base):raise ValueError('Source base identity')
rad=[1,3,5,15,11,33,55,165]
host_points=[tuple(tuple(F(a.get(r,0),96) for r in rad) for a in p) for p in host]
if [host_points[v] for v in labels]!=H:raise ValueError('Source coordinate identity')
if source['edges']!=[list(e) for e in edges if set(e)<=base]:raise ValueError('Source edge identity')
host_set=set(host_points);Hset=set(H)
raw='516 96\n'+''.join(' '.join(str(v) for axis in row for v in axis)+'\n' for row in source['coordinates'])
(OUT/'points.txt').write_text(raw)
r=subprocess.run([str(a.filter.resolve()),str(OUT/'points.txt'),str(OUT/'survivors.tsv')],capture_output=True,text=True,check=True);flt=json.loads(r.stdout)
if flt['triples']!=comb(516,3):raise ValueError('Triple count')
(OUT/'FILTER.json').write_text(json.dumps(flt,indent=2)+'\n')
pair_centres={};centres=[];centre_ids={};rejected=[];visited=0
for line in (OUT/'survivors.tsv').read_text().splitlines():
    triple=tuple(map(int,line.split()));i,j,k=triple;visited+=1
    if any(k in centres[c]['neighbors'] for c in pair_centres.get((i,j),[])):continue
    q=geom.circumcentre(H[i],H[j],H[k])
    if q is None or geom.dist(H[i],q)!=geom.ONE:rejected.append(list(triple));continue
    if q in centre_ids:raise ValueError('Unaccounted repeated centre')
    ns=geom.neighbours(q,H)
    if not set(triple)<=set(ns):raise ValueError('Centre radius')
    index=len(centres);centre_ids[q]=index;centres.append({'coordinates':geom.dump_point(q),'neighbors':ns,'witness':list(triple)})
    for pair in combinations(ns,2):pair_centres.setdefault(pair,[]).append(index)
    if index%250==0:print(json.dumps({'centres':len(centres),'visited':visited,'seconds':time.monotonic()-start}),flush=True)
centres.sort(key=lambda r:geom.parse_point(r['coordinates']))
(OUT/'centres.json').write_text(json.dumps(centres,separators=(',',':'))+'\n');(OUT/'rejected.json').write_text(json.dumps(rejected)+'\n')
if sum(comb(len(r['neighbors']),3) for r in centres)+len(rejected)!=visited:raise ValueError('Survivor accounting')
exterior=[{'centre_index':i,**r} for i,r in enumerate(centres) if len(r['neighbors'])>=4 and geom.parse_point(r['coordinates']) not in host_set]
(OUT/'exterior.json').write_text(json.dumps(exterior,separators=(',',':'))+'\n')
words=json.loads((REPO/'hadwiger_nelson_heule516_single_point_h632_closure/certificate.json').read_text())['deletion_rows']
col_by_removed={v:[] for v in labels};base_edges={tuple(e) for e in source['edges']};edgechecks=0
for row in words:
    v=row['removed'];order=[x for x in labels if x!=v];col=dict(zip(order,old.unpack(row['colours'],len(order))))
    for a,b in base_edges:
        if v not in (a,b):
            if col[a]==col[b]:raise ValueError('Invalid base deletion colouring')
            edgechecks+=1
    col_by_removed[v].append(col)
if not all(col_by_removed.values()):raise ValueError('Missing source deletion word')
coverage={};residual=[]
for row in exterior:
    ns=[labels[i] for i in row['neighbors']];covered=[]
    for v in labels:
        if any(len({col[u] for u in ns if u!=v})<4 for col in col_by_removed[v]):covered.append(v)
    coverage[str(row['centre_index'])]=covered
    if len(covered)<508:residual.append({'centre_index':row['centre_index'],'degree':len(ns),'coverage':len(covered),'uncovered':sorted(base-set(covered))})
(OUT/'COVERAGE.json').write_text(json.dumps(coverage,separators=(',',':'))+'\n');(OUT/'RESIDUAL.json').write_text(json.dumps(residual,indent=2)+'\n')
summary={'vertices':516,'base_edges':len(base_edges),'all_centres_degree_at_least_three':len(centres),'external_all_degree_histogram':dict(sorted(Counter(len(r['neighbors']) for r in centres if geom.parse_point(r['coordinates']) not in Hset).items())),'outside_H632_degree_at_least_four':len(exterior),'outside_H632_degree_histogram':dict(sorted(Counter(len(r['neighbors']) for r in exterior).items())),'coverage_histogram':dict(sorted(Counter(len(x) for x in coverage.values()).items())),'residual_points':len(residual),'worst_coverage':min(map(len,coverage.values())),'filter':flt,'modular_false_positives':len(rejected),'verified_base_deletion_edge_checks':edgechecks,'seconds':time.monotonic()-start,'new_solver_queries':0}
(OUT/'CENSUS.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps(summary,indent=2),flush=True)
