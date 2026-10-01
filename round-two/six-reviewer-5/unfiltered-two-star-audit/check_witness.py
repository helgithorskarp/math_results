"""Standalone literal lower certificates; no generator/search is imported."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

def require(ok, message):
    if not ok: raise ValueError(message)

def check(row):
    masks=row['word_masks'];marks=row['marks']
    require(type(masks) is list and all(type(m) is int and 0<m<2**18 for m in masks), 'mask domain')
    words=[frozenset(p for p in range(18) if m>>p & 1) for m in masks]
    require(len(set(words))==len(words) and all(len(w)==5 for w in words), 'distinct five-subsets')
    require(all(len(a&b)<=2 for a,b in combinations(words,2)), 'packing')
    x,y,u,v=(marks[p] for p in ('x','y','u','v'))
    require(len({x,y,u,v})==4 and all(type(p) is int and 0<=p<18 for p in (x,y,u,v)), 'roles')
    degree=[sum(p in w for w in words) for p in range(18)]
    pair=lambda p,q:sum({p,q}<=w for w in words)
    covered=lambda p,q,r:any({p,q,r}<=w for w in words)
    require(degree[x]==degree[y]==20, 'saturated centers')
    require(pair(x,y)==4 and pair(x,v)==5 and not covered(x,y,v), 'premise1')
    require(pair(x,u) in (3,4) and all(pair(x,p) in (4,5) for p in range(18) if p not in (x,u)), 'first pair row')
    deficient={p for p in range(18) if p!=x and pair(x,p)<5}
    require(all(covered(x,u,p) for p in deficient-{u}), 'isolated deficient hub')
    require(pair(y,u)==pair(y,v)==5 and all(pair(y,p) in (4,5) for p in range(18) if p!=y), 'unit second row')
    require(pair(x,u)==row['lambda_xu'], 'hub attribution')
    triangles=[p for p in range(18) if p not in(x,y,u,v) and pair(x,p)==pair(y,p)==4 and not covered(x,y,p)]
    return {'index':row['index'],'size':len(words),'lambda_xu':pair(x,u),
            'triangle_witnesses':triangles,'degree_profile':dict(sorted(Counter(degree).items()))}

def main():
    rows=json.loads(Path(__file__).with_name('WITNESSES.json').read_text())
    require(len(rows)==34 and {r['index'] for r in rows}==set(range(34)), 'witness coverage')
    records=[check(row) for row in rows]
    require(max(r['size'] for r in records)==66, 'sharp66 witness')
    require(max(r['size'] for r in records if r['lambda_xu']==4)==63, 'sharp63 witness')
    require(max(r['size'] for r in records if not r['triangle_witnesses'])==58, 'sharp58 witness')
    print(json.dumps({'status':'PASS_LITERAL_SHARPNESS_WITNESSES','witnesses':34,
                      'sharp66':records[6],'sharp63':records[27],'sharp58':records[18]},sort_keys=True))

if __name__=='__main__':main()
