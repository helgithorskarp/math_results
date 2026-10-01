"""Exhaustive independent small graphs and semantic rejection controls."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import audit
from clique import maximum

def run():
    data,seeds,bridge,cert=audit.inputs()
    count=0
    for n in range(6):
        pairs=list(combinations(range(n),2))
        for flags in range(1<<len(pairs)):
            adj=[0]*n
            for k,(i,j) in enumerate(pairs):
                if flags>>k & 1:
                    adj[i]|=1<<j;adj[j]|=1<<i
            brute=max(s.bit_count() for s in range(1<<n) if all(adj[i]>>j & 1 for i,j in pairs if s>>i & 1 and s>>j & 1))
            chosen,_=maximum(adj)
            audit.need(len(chosen)==brute, 'clique differs from exhaustive subset maximum')
            count+=1
    rejected=[]
    def reject(name,function):
        try: function()
        except (ValueError,RuntimeError): rejected.append(name)
        else: raise ValueError('damage accepted: '+name)
    reject('zero-node-incomplete',lambda:maximum((0,),node_cap=0))
    reject('asymmetric-graph',lambda:maximum((2,0)))
    row=bridge['raw_positive_maps'][0];u,v,y=row['first'][1];core=row['word_masks']
    cs=audit.domain(core,y);adj=audit.graph(cs);e=cert['entries'][0]
    for name,modified in [('duplicate-word',core[:-1]+[core[0]]),('wrong-weight',[3]+core[1:]),('point-outside-domain',[(1<<18)|core[0]]+core[1:])]:
        reject(name,lambda modified=modified:audit.roles(modified,u,y,v))
    reject('uncompleted-center',lambda:audit.roles(core[:-1],u,y,v))
    reject('coalesced-roles',lambda:audit.roles(core,u,y,u))
    reject('incorrect-first-hub',lambda:audit.roles(core,17,y,v))
    reject('missing-color',lambda:audit.coloring(cs,adj,e['colors'][:-1],e['capacity']))
    reject('color-bool',lambda:audit.coloring(cs,adj,[True]+e['colors'][1:],e['capacity']))
    colors=deepcopy(e['colors']);i,j=next((i,j) for i,j in combinations(range(len(cs)),2) if adj[i]>>j & 1)
    colors[j]=colors[i]
    reject('compatible-same-color',lambda:audit.coloring(cs,adj,colors,e['capacity']))
    reject('representative-cover-gap',lambda:audit.representatives(data,{**bridge,'raw_positive_maps':bridge['raw_positive_maps'][:-1]},cert))
    reject('expired-full-audit',lambda:audit.representatives(data,bridge,cert,deadline=0))
    with TemporaryDirectory(prefix='unfiltered-review-controls-') as name:
        base=Path(name);pins=json.loads((audit.HERE/'INPUTS.json').read_text())
        (base/'INPUTS.json').write_bytes((audit.HERE/'INPUTS.json').read_bytes())
        for fn in pins:(base/fn).write_bytes((audit.HERE/fn).read_bytes())
        audit.inputs(base)
        for fn in pins:
            original=(base/fn).read_bytes();(base/fn).write_bytes(original+b'changed')
            reject('changed-pin-'+fn,lambda:audit.inputs(base))
            (base/fn).write_bytes(original)
    return {'status':'PASS_INDEPENDENT_CONTROLS','ordinary_graphs':count,'damage_rejections':rejected}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
