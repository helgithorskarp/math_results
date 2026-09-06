"""Optional bounded witness search; not part of the proof replay."""
import argparse,json,time
from pathlib import Path
from itertools import combinations
from build import build,check_colours,digest

def main():
    assert __debug__
    from pysat.solvers import Solver
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    data,stats=build();n=len(data['hulls']);v=lambda i,c:4*i+c+1
    clauses=[[v(i,c) for c in range(4)] for i in range(n)]
    clauses.extend([-v(i,c),-v(i,d)] for i in range(n) for c,d in combinations(range(4),2))
    clauses.extend([-v(i,c),-v(j,c)] for i,j in data['edges'] for c in range(4))
    clauses.extend([-v(i,c) for i in tri] for tri in data['triples'] for c in range(4))
    with Solver(name='cadical195',bootstrap_with=clauses) as s:
        s.conf_budget(100000);result=s.solve_limited();solver_stats=s.accum_stats()
        assert result is True, ('no witness; not a geometric obstruction', result)
        model=set(s.get_model());colours=[next(c for c in range(4) if v(i,c) in model) for i in range(n)]
    check_colours(data,colours)
    cert={'colours':colours,'colours_sha256':digest(colours),
          'labelled_colours':''.join(str(colours[g]) for g in data['groups'])}
    (out/'certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
    (out/'expected.json').write_text(json.dumps(stats,indent=2)+'\n')
    result={'solver':'CaDiCaL 1.9.5','python_sat':'1.8.dev24','queries':1,'conflict_cap':100000,
            'variables':4*n,'clauses':len(clauses),'status':'SAT','solver_stats':solver_stats,'seconds':time.monotonic()-start}
    (out/'discovery.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
