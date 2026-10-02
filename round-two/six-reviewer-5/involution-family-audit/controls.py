"""Independent exhaustive small-domain and semantic controls."""
from copy import deepcopy
from itertools import combinations,permutations,product
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import audit
import lower
from core import HERE,pin_inputs,require
from clique import maximum,twins

def brute(rows,weights):
    n=len(rows)
    return max(sum(weights[i] for i in range(n) if s>>i&1) for s in range(1<<n) if all(rows[i]>>j&1 for i,j in combinations(range(n),2) if s>>i&1 and s>>j&1))

def check():
    ordinary=weighted=involutions=0
    for n in range(6):
        pairs=list(combinations(range(n),2))
        for flags in range(1<<len(pairs)):
            rows=[0]*n
            for k,(a,b) in enumerate(pairs):
                if flags>>k&1:rows[a]|=1<<b;rows[b]|=1<<a
            chosen,_=maximum(rows);require(len(chosen)==brute(rows,(1,)*n),'small unweighted brute comparison');ordinary+=1
            if n<=4:
                for weights in product((1,2),repeat=n):
                    expanded,_=twins(rows,weights);chosen,_=maximum(expanded)
                    require(len(chosen)==brute(rows,weights),'small true-twin weighted equivalence');weighted+=1
    for n in range(8):
        literal={p for p in permutations(range(n)) if all(p[p[i]]==i for i in range(n))}
        generated=set()
        for fixed in range(n+1):
            seen=set()
            for cells in audit.partitions(range(n),fixed):
                p=list(range(n))
                for cell in cells:
                    if len(cell)==2:p[cell[0]],p[cell[1]]=cell[1],cell[0]
                p=tuple(p);require(p not in seen and sum(p[i]==i for i in range(n))==fixed,'partition uniqueness/fixed count');seen.add(p)
            require(seen=={p for p in literal if sum(p[i]==i for i in range(n))==fixed},'full involution partition versus permutation brute force')
            generated.update(seen)
        require(generated==literal,'full involution cover');involutions+=len(literal)
    rejected=[]
    def reject(name,function):
        try:function()
        except (ValueError,RuntimeError):rejected.append(name)
        else:raise ValueError('damage accepted '+name)
    reject('incomplete-node-guard',lambda:maximum((0,),node_cap=0))
    reject('asymmetric-graph',lambda:maximum((2,0)))
    reject('wrong-twin-weight',lambda:twins((0,),(0,)))
    positive=json.loads((HERE/'WITNESS56.json').read_text())
    for name,damage in [('duplicate-word',lambda d:d['words'].__setitem__(0,d['words'][1])),('wrong-weight',lambda d:d['words'].__setitem__(0,3)),('fixed-instead-of-exchanged',lambda d:d.__setitem__('involution',list(range(18)))),('wrong-center-pair',lambda d:d.__setitem__('centers',[2,3])),('false-degree',lambda d:d['replications'].__setitem__(0,19))]:
        bad=deepcopy(positive);damage(bad);reject(name,lambda bad=bad:lower.check(bad,56,3))
    with TemporaryDirectory(prefix='involution-family-controls-') as name:
        base=Path(name);manifest=(HERE/'INPUTS.json').read_bytes();(base/'INPUTS.json').write_bytes(manifest)
        for r in json.loads(manifest):
            p=base/r['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((HERE/r['path']).read_bytes())
        pin_inputs(base)
        for r in json.loads(manifest):
            p=base/r['path'];original=p.read_bytes();p.write_bytes(original+b'changed')
            reject('changed-pin-'+r['path'],lambda:pin_inputs(base));p.write_bytes(original)
    return {'status':'PASS_EXHAUSTIVE_AND_SEMANTIC_CONTROLS','ordinary_graphs':ordinary,'weighted_graphs':weighted,'literal_small_involutions':involutions,'damage_rejections':rejected}
