"""Definition-level truth tables for the generic kernel, including repeats."""
import argparse
import itertools as it
import json
from pathlib import Path
from build import kernel, need


def run():
    checks=0;fixtures=0;repeated=0
    # Every 5-vertex coloring and every core/outside split; 6-vertex
    # deterministic samples cover multiple simultaneous candidate five-sets.
    for n,masks in ((5,range(1024)),(6,[0,32767]+list(range(31,32767,137)))):
        pairs=list(it.combinations(range(n),2))
        for mask in masks:
            R={e for i,e in enumerate(pairs) if mask>>i&1}
            for k in range(n+1):
                core={e for e in R if e[1]<k}
                types=[sum(1<<u for u in range(k) if (u,v) in R) for v in range(k,n)]
                repeated+=int(len(types)!=len(set(types)));fixtures+=1
                outside=list(it.combinations(range(k,n),2))
                vals={i+1:e in R for i,e in enumerate(outside)}
                for layer in range(6):
                    _,records=kernel(k,core,types,layer)
                    actual=all(any(vals[abs(l)]==(l>0) for l in r['clause']) for r in records)
                    expected=True
                    for five in it.combinations(range(n),5):
                        if sum(v>=k for v in five)>layer:continue
                        colors=[e in R for e in it.combinations(five,2)]
                        if not any(colors) or all(colors):expected=False
                    need(actual==expected,'literal kernel truth table');checks+=1
    bad=[(-1,[],[],3),(1,[],[2],3),(1,[],[-1],3),(1,[],[True],3),
         (1,[(0,0)],[],3),(1,[],[],6),(1,[],[],-1)]
    for args in bad:
        try:kernel(*args)
        except ValueError:pass
        else:raise ValueError('invalid kernel input accepted')
    return {'status':'VERIFIED','five_vertex_colorings':1024,'six_vertex_colorings':241,
            'core_split_fixtures':fixtures,'fixtures_with_repeated_types':repeated,
            'layer_truth_checks':checks,'malformed_inputs_rejected':len(bad)}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    need(not a.report.exists(),'fresh report');r=run()
    a.report.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
