"""Optional positive-witness generator; output must be specified explicitly."""
from pathlib import Path
from itertools import combinations
from pysat.solvers import Solver
import argparse,json
from model import build

HERE=Path(__file__).resolve().parent

def generate():
    graph,summary=build(HERE/'geometry_certificate.json');n=len(graph['classes'])
    E=set(map(tuple,graph['edges']));pairs=list(combinations(range(n),2));nonedges=[p for p in pairs if p not in E]
    clauses=[[4*v+c+1 for c in range(4)] for v in range(n)]
    clauses += [[-4*v-c-1,-4*v-d-1] for v in range(n) for c,d in combinations(range(4),2)]
    clauses += [[-4*a-c-1,-4*b-c-1] for a,b in sorted(E) for c in range(4)]
    words=[];same=set();different=set()
    with Solver(name='cadical195',bootstrap_with=clauses) as solver:
        def save():
            model=set(solver.get_model());word=[]
            for v in range(n):
                colours=[c for c in range(4) if 4*v+c+1 in model]
                if len(colours)!=1:raise RuntimeError('invalid one-hot model')
                word.append(colours[0])
            if any(word[a]==word[b] for a,b in E):raise RuntimeError('bad unit colouring')
            words.append(''.join(map(str,word)))
            same.update(p for p in nonedges if word[p[0]]==word[p[1]])
            different.update(p for p in pairs if word[p[0]]!=word[p[1]])
        if not solver.solve():raise RuntimeError('non-four signal: needs separate certification')
        save()
        for kind,domain,covered in [('same',nonedges,same),('different',pairs,different)]:
            for a,b in domain:
                if (a,b) in covered:continue
                # Every equal/unequal pair can be renamed 00/01. No base pins.
                if not solver.solve(assumptions=[4*a+1,4*b+1+(kind=='different')]):
                    raise RuntimeError(('pair obstruction: needs separate certification',kind,a,b))
                save()
                if (a,b) not in covered:raise RuntimeError('pair-pinning decode')
    return {'schema':'fish-spindle-pair-relations-v1','graph_sha256':summary['graph_sha256'],'words':words,'forced':[]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);args=p.parse_args()
    cert=generate();args.output.write_text(json.dumps(cert,separators=(',',':'))+'\n')
    print(json.dumps({'positive_words':len(cert['words']),'output_bytes':args.output.stat().st_size}))
