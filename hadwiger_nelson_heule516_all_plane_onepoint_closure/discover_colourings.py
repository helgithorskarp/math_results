from pathlib import Path
from collections import Counter
from itertools import combinations
import json, base64, time, importlib.util
from pysat.solvers import Glucose42
import argparse
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
a=ap.parse_args();OUT=a.work;OUT.mkdir(parents=True,exist_ok=True)
if (OUT/'new_deletion_rows.json').exists():raise ValueError('Colour discovery already present; no implicit rerun')
G=json.loads((REPO/'hadwiger_nelson_h516_degree4_surgeries/SOURCE.json').read_text());V=G['labels'];ix={v:i for i,v in enumerate(V)};n=len(V);E=[tuple(e) for e in G['edges']]
points=json.loads((OUT/'exterior.json').read_text());point_ids=[r['centre_index'] for r in points];neigh={r['centre_index']:[V[i] for i in r['neighbors']] for r in points}
cov={int(k):set(v) for k,v in json.loads((OUT/'COVERAGE.json').read_text()).items()};newwords=[];tried=set();log=[]
X=lambda v,c:4*ix[v]+c+1;Q=lambda c:4*n+c+1
ACT=lambda v:4*(n+1)+ix[v]+1
SEL={qid:4*(n+1)+n+i+1 for i,qid in enumerate(point_ids)}
clauses=[[X(v,c) for c in range(4)] for v in V]+[[Q(c) for c in range(4)]]
for u,v in E:
    for c in range(4):clauses.append([-ACT(u),-ACT(v),-X(u,c),-X(v,c)])
for q in point_ids:
    for u in neigh[q]:
        for c in range(4):clauses.append([-SEL[q],-ACT(u),-Q(c),-X(u,c)])
adj={v:set() for v in V}
for u,v in E:adj[u].add(v);adj[v].add(u)
tri=next((u,v,w) for u in V for v,w in combinations(sorted(x for x in adj[u] if x>u),2) if w in adj[v])
clauses += [[X(v,c)] for c,v in enumerate(tri)]
start=time.monotonic();solver=Glucose42(bootstrap_with=clauses);stats={};last_report=start

def save(status):
    (OUT/'new_deletion_rows.json').write_text(json.dumps(newwords,separators=(',',':'))+'\n')
    (OUT/'COVERAGE_FINAL.json').write_text(json.dumps({str(q):sorted(c) for q,c in cov.items()},separators=(',',':'))+'\n')
    (OUT/'QUERY_LOG.json').write_text(json.dumps(log,indent=2)+'\n')
    result={'status':status,'queries':len(log),'answers':dict(Counter(r['answer'] for r in log)),'new_deletion_rows':len(newwords),'residual_points':sum(len(c)<508 for c in cov.values()),'minimum_coverage':min(map(len,cov.values())),'coverage_histogram':dict(sorted(Counter(len(c) for c in cov.values()).items())),'seconds':time.monotonic()-start,'conflicts_per_query':200000,'source_triangle':list(tri),'solver':'Glucose42','source_variables':4*(n+1)+n+len(points),'source_clauses':len(clauses)}
    (OUT/'COLOUR_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result

while any(len(c)<508 for c in cov.values()):
    residual=[q for q in point_ids if len(cov[q])<508]
    choices=[q for q in residual if any(v not in cov[q] and (q,v) not in tried for v in V)]
    if not choices:print(json.dumps(save('EXHAUSTED_DISTINCT_EXTENSION_PAIRS_WITH_RESIDUAL'),sort_keys=True),flush=True);break
    q=min(choices,key=lambda q:(len(cov[q]),-len(neigh[q]),q))
    potential=[v for v in V if v not in cov[q] and (q,v) not in tried]
    v=max(potential,key=lambda v:(sum(v not in cov[t] for t in residual),v in neigh[q],-v))
    tried.add((q,v));before=solver.accum_stats();t=time.monotonic();solver.conf_budget(200000)
    ans=solver.solve_limited(assumptions=[ACT(u) if u!=v else -ACT(u) for u in V]+[SEL[q]])
    elapsed=time.monotonic()-t;after=solver.accum_stats();entry={'point':q,'removed':v,'answer':'SAT' if ans is True else 'UNSAT_UNVERIFIED' if ans is False else 'UNKNOWN','conflicts':after['conflicts']-before['conflicts'],'seconds':elapsed}
    if ans:
        model=set(x for x in solver.get_model() if x>0);col={u:next(c for c in range(4) if X(u,c) in model) for u in V if u!=v};qc=next(c for c in range(4) if Q(c) in model)
        if any(col[a]==col[b] for a,b in E if v not in (a,b)):raise ValueError('Bad base colouring')
        if any(col[u]==qc for u in neigh[q] if u!=v):raise ValueError('Bad new-point colouring')
        word=[col[u] for u in V if u!=v];packed=bytearray((len(word)+3)//4)
        for i,c in enumerate(word):packed[i//4]|=c<<(2*(i%4))
        newwords.append({'removed':v,'colours':base64.b64encode(packed).decode('ascii')})
        gain=0
        for t in point_ids:
            if v not in cov[t] and len({col[u] for u in neigh[t] if u!=v})<4:cov[t].add(v);gain+=1
        if v not in cov[q]:raise ValueError('Target not covered by its own SAT witness')
        entry['new_coverage_pairs']=gain
    log.append(entry)
    if len(log)%20==0 or time.monotonic()-last_report>30:
        print(json.dumps(save('LIVE_COLOUR_COVER'),sort_keys=True),flush=True);last_report=time.monotonic()
else:print(json.dumps(save('ALL_EXTERIOR_ONE_POINT_REPAIRS_CLOSED_THROUGH_508'),sort_keys=True),flush=True)
solver.delete()
