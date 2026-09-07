"""Optional complete positive-colouring producer. PySAT1.9.dev15 required."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import time

from pysat.solvers import Cadical195
import geometry as g


def colouring(n,edges,k):
    clauses = [[k*i+c+1 for c in range(k)] for i in range(n)]
    clauses += [[-(k*i+a+1),-(k*i+b+1)] for i in range(n)
                for a in range(k) for b in range(a+1,k)]
    clauses += [[-(k*i+c+1),-(k*j+c+1)] for i,j in edges for c in range(k)]
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None,solver.accum_stats()
        model = set(solver.get_model())
        word = [next(c for c in range(k) if k*i+c+1 in model) for i in range(n)]
        if any(word[i]==word[j] for i,j in edges):
            raise ValueError('invalid solver colouring')
        return word,solver.accum_stats()


def pack(word):
    data = bytearray((len(word)+3)//4)
    for i,c in enumerate(word):
        data[i//4] |= c << (2*(i%4))
    return base64.b64encode(data).decode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--limit',type=int,default=812,help='pilot only if below812')
    args = parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    points = g.seed()
    base_edges = g.edges_exact(points,g.scale(g.ONE,g.D*g.D))
    base_word,_ = colouring(29,base_edges,4)
    if base_word is None:
        raise ValueError('unexpected seed obstruction; preserve separately')
    start = time.monotonic()
    certificate = {'version':1,'family':'Snail seed-centred seed-axis D9',
                   'address_order':'k,reflection,seed; k=0..2; reflection=0,1; seed=0..28',
                   'seed_sha256':hashlib.sha256((Path(__file__).parent/'seed.json').read_bytes()).hexdigest(),
                   'base_word':pack(base_word),'cases':[]}
    evidence = []
    for c in range(29):
        for a in range(29):
            if c == a:
                continue
            if len(evidence) >= args.limit:
                break
            graph = g.case(points,c,a)
            n,edges = len(graph['points']),graph['edges']
            word,stats = colouring(n,edges,4)
            if word is None:
                (args.output/f'UNPROVED_UNSAT_{c}_{a}.json').write_text(json.dumps(graph))
                raise RuntimeError(('UNSAT requires independent proof',c,a))
            formal = [word[i] for i in graph['address_ids']]
            certificate['cases'].append([c,a,pack(formal)])
            raw = json.dumps({'points':graph['points'],'address_ids':graph['address_ids'],
                              'edges':edges},separators=(',',':')).encode()
            record = {'centre':c,'axis':a,'D3_vertices':n,'D3_edges':len(edges),
                      'D9_vertices':3*n-2,'D9_edges':3*len(edges),
                      'geometry_sha256':hashlib.sha256(raw).hexdigest(),'conflicts':stats['conflicts']}
            evidence.append(record)
            (args.output/f'case_{c:02}_{a:02}.json').write_bytes(raw)
            if len(evidence)%29==0 or len(evidence)==args.limit:
                print(json.dumps({'cases':len(evidence),'elapsed_seconds':time.monotonic()-start,
                                  'latest':record}),flush=True)
    certificate['complete'] = len(evidence)==812
    (args.output/'certificate.json').write_text(json.dumps(certificate,separators=(',',':'))+'\n')
    (args.output/'census.json').write_text(json.dumps(evidence,indent=2)+'\n')
    summary = {'complete':len(evidence)==812,'cases':len(evidence),'seed_vertices':29,
               'seed_edges':len(base_edges),'seed_degrees':[sum(i in edge for edge in base_edges) for i in range(29)],
               'D3_vertices_range':[min(x['D3_vertices'] for x in evidence),max(x['D3_vertices'] for x in evidence)],
               'D3_edges_range':[min(x['D3_edges'] for x in evidence),max(x['D3_edges'] for x in evidence)],
               'D9_vertices_range':[min(x['D9_vertices'] for x in evidence),max(x['D9_vertices'] for x in evidence)],
               'D9_edges_range':[min(x['D9_edges'] for x in evidence),max(x['D9_edges'] for x in evidence)],
               'max_solver_conflicts':max(x['conflicts'] for x in evidence),
               'elapsed_seconds':time.monotonic()-start}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


if __name__ == '__main__':
    main()
