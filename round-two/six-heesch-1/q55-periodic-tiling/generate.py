"""Generate five literal disc coronas in the two-orbit Q55 plane tiling."""
import json
from pathlib import Path
import geometry as g

HERE = Path(__file__).resolve().parent
data = json.loads((HERE/'input.json').read_text())
raw = set(map(tuple,data['cells']))
shapes = g.images(raw)
root = shapes.index(g.norm(raw))
flip = shapes.index(g.norm([(-x,y) for x,y in raw]))
levels = []
for k in range(6):
    shell = []
    for u in range(-k,k+1):
        for v in range(-k,k+1):
            if max(abs(u),abs(v),abs(u+v)) != k:
                continue
            shell.append([flip if v%2 else root,
                11*u+11*(v//2)+6*(v%2),5*v])
    levels.append(sorted(shell))
fixture = dict(cells=data['cells'],levels=levels)
g.verify_lower(fixture)
(HERE/'five-coronas.json').write_text(json.dumps(fixture,indent=2)+'\n')
print(json.dumps(dict(coronas=5,copies=sum(map(len,levels)),cells=55*sum(map(len,levels)))))
