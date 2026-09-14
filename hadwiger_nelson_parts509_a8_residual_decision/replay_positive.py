"""Regenerate/check a literal positive witness for every baseline killing cut."""
from pathlib import Path
import json,importlib.util,time,hashlib,os,argparse
HERE=Path(__file__).resolve().parent;repo=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args();W=args.work;W.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('a8',repo/'hadwiger_nelson_parts509_shape8_transfer/search.py');a8=importlib.util.module_from_spec(spec);spec.loader.exec_module(a8)
start=time.monotonic();den,pts,verts,U,E=a8.load_geometry(repo);us=set(U)
words=[r['witness_colouring_L'] for r in json.loads((repo/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())['classes']]
o=a8.Oracle(U,E,words);seed,hashes=a8.seed_clauses(repo,U);known={};hints={}
for row in json.loads((repo/'hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json').read_text())['sets']:
 known[tuple(row['D'])]={'D':row['D'],'p':row['p'],'c':row['c']}
for row in json.loads((repo/'hadwiger_nelson_parts509_s_replacement_budget/certificate.json').read_text())['killing_sets']:
 D=tuple(row['D']);raw=row['colouring_U_minus_D'];a8.need(len(raw)==303-len(D),'S-only compact word length');cc=dict(zip([v for v in U if v not in D],raw));c=''.join(cc.get(v,'.') for v in U);known[D]={'D':list(D),'p':row['class_index'],'c':c}
for row in json.loads((repo/'hadwiger_nelson_parts509_pool_cover_shrink01/colourings.json').read_text()):known[tuple(row['D'])]={'D':row['D'],'l':row['l'],'c':row['c']}
for shape in [6,7]:
 d=repo/f'hadwiger_nelson_parts509_pool_shape{shape}_verified';ps=json.loads((d/'interface_hints.json').read_text());lines=(d/'killing_clauses.cnf').read_text().splitlines()[1:]
 a8.need(len(lines)==len(ps),'hint rows')
 for line,p in zip(lines,ps):
  q=list(map(int,line.split()));D=tuple(U[v-1] for v in q[:-1]);hints.setdefault(D,p)
rows=json.loads((HERE/'baseline_cuts.json').read_text())
for row in rows:known[tuple(row['D'])]={k:row[k] for k in ['D','p','c']}
Dlist=seed+[tuple(r['D']) for r in rows];checked=0;generated=0
out=W/'seed-colourings.jsonl';t=time.monotonic()
with out.open('w') as f:
 for D in Dlist:
  D=tuple(D);row=known.get(D)
  if row is None:
   a8.need(D in hints,'missing published hint');a,c=o.solve(us-set(D),hints[D],200000)
   a8.need(a is True,'positive source replay unresolved '+str(D));row={'D':list(D),'p':hints[D],'c':c};generated+=1
  if 'p' in row:o.check(us-set(D),row['p'],row['c'])
  else:
   l=row['l'];c=row['c'];a8.need(len(l)==374 and set(l)<=set('0123'),'literal L word');a8.need(len(c)==303 and set(c)<=set('.0123') and {v for v,x in zip(U,c) if x=='.'}==set(D),'literal pool word')
   col=dict(enumerate(l));col.update({v:x for v,x in zip(U,c) if x!='.'});a8.need(all(col[a]!=col[b] for a,b in E if a in col and b in col),'literal complete edge colouring')
  f.write(json.dumps(row,separators=(',',':'))+'\n');checked+=1
  if checked%1000==0:
   f.flush();a8.save(W/'seed-progress.json',{'checked':checked,'generated':generated,'total':len(Dlist),'elapsed_seconds':time.monotonic()-start});print(checked,generated,time.monotonic()-start,flush=True)
 f.flush();os.fsync(f.fileno())
for s in o.solvers:s.delete()
r={'status':'ALL_BASELINE_KILLING_WORDS_CHECKED','count':checked,'generated':generated,'seconds':time.monotonic()-start,'sha256':a8.sha(out),'bytes':out.stat().st_size,'source_hashes':hashes,'points':len(verts),'unit_edges':len(E),'denominator':den}
a8.save(W/'seed-validation.json',r);print(json.dumps(r),flush=True)
