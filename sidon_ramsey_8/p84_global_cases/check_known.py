"""Check published P80 witnesses in both encodings, including labels at 83."""
import json
from pathlib import Path
from encode import build, decode
from orbits import sidon
from pysat.solvers import Solver
source=Path(__file__).resolve().parent
rows=[sorted(int(x)-1 for x in line.split()) for line in (source.parent/'p80_extension_barrier/partition80.txt').read_text().splitlines()]
rows.sort(key=min)
assert sorted(x for r in rows for x in r)==list(range(80)) and all(sidon(r) for r in rows)
records=[]
for shift in [0,4]:
    part=[[x+shift for x in r] for r in rows]
    for kind in ['difference','sums']:
        f,m=build(list(range(shift,shift+80)),[10]*8,kind)
        colors={x:c for c,r in enumerate(part) for x in r}
        with Solver(name='g3',bootstrap_with=f.clauses) as solver:
            assert solver.solve(assumptions=[i*8+colors[x]+1 for i,x in enumerate(m['domain'])])
            assert decode(solver.get_model(),m)==part
        records.append({'n':80,'shift':shift,'kind':kind,'valid':True})
print(json.dumps(records))
