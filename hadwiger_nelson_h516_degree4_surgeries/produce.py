"""Enumerate the frozen final graphs with C++ bitset adjacency; find a K2,3 cover."""
import argparse,hashlib,itertools,json,pathlib,subprocess
D=pathlib.Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);a=ap.parse_args();w=a.work.resolve();w.mkdir(parents=True,exist_ok=True)
    raw=(D/'SOURCE.json').read_bytes();s=json.loads(raw);adj={v:set() for v in s['labels']}
    for u,v in s['edges']:adj[u].add(v);adj[v].add(u)
    centres=sorted(v for v in adj if len(adj[v])==4)
    options={v:[p for p in itertools.combinations(sorted(adj[v]),2) if p[1] not in adj[p[0]]] for v in centres}
    stars={v:adj[v]|{v} for v in centres}
    quads=[q for q in itertools.combinations(centres,4) if all(not(stars[u]&stars[v]) for u,v in itertools.combinations(q,2))]
    cases=[[(c,*p) for c,p in zip(q,ps)] for q in quads for ps in itertools.product(*(options[c] for c in q))]
    if len(quads)!=87 or len(cases)!=53276:raise ValueError('frozen family')
    with (w/'census.in').open('w') as f:
        f.write(f"{len(adj)} {len(s['edges'])} {len(cases)}\n")
        f.write(' '.join(map(str,s['labels']))+'\n')
        for e in s['edges']:f.write(' '.join(map(str,e))+'\n')
        for case in cases:f.write(' '.join(str(x) for op in case for x in op)+'\n')
    subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra',str(D/'census.cpp'),'-o',str(w/'census')],check=True)
    subprocess.run([str(w/'census'),str(w/'census.in'),str(w/'witnesses.txt')],check=True)
    rows=[tuple(map(int,line.split())) for line in (w/'witnesses.txt').read_text().splitlines()]
    if len(rows)!=53276 or any(len(row)!=5 for row in rows):raise ValueError('surviving case or bad output')
    c={'claim':'No injective plane unit-distance realization in the complete four-disjoint-star surgery family','source_sha256':hashlib.sha256(raw).hexdigest(),'centres':centres,'quadruples':87,'cases':53276,'witnesses':sorted(set(rows))}
    data=(json.dumps(c,indent=2)+'\n').encode();(w/'certificate.json').write_bytes(data)
    if data!=(D/'certificate.json').read_bytes():raise ValueError('certificate mismatch')
    print(json.dumps({'labelled_cases':len(rows),'witnesses':len(c['witnesses']),'certificate_bytes':len(data),'certificate_sha256':hashlib.sha256(data).hexdigest(),'survivors':0}))
if __name__=='__main__':main()
