#!/usr/bin/env python3
"""Malformed inputs and separate algebra/colour-search validation."""
import argparse
import copy
import json
from pathlib import Path
import produce as P
import verify as V

def algebra():
    basis=[tuple(int(i==j) for i in range(12)) for j in range(12)]
    for a in basis:
        for b in basis:
            V.require(V.convert(P.mul(a,b))==V.multiply(V.convert(a),V.convert(b)),
                      'basis product disagreement')
        V.require(V.convert(P.conj(a))==V.conjugate(V.convert(a)),'basis conjugation disagreement')
    V.require(V.power(V.T,42)==V.ONE,'primitive root order')
    for d in [1,2,3,6,7,14,21]:V.require(V.power(V.T,d)!=V.ONE,'proper root order')
    return {'basis_products':144,'basis_conjugations':12,'proper_order_exclusions':7}

def dsatur():
    E=V.abstract_seed_edges();adj=[set() for _ in range(21)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    word=[-1]*21;word[0]=0;nodes=0
    def search():
        nonlocal nodes
        nodes+=1
        unknown=[v for v in range(21) if word[v]<0]
        if not unknown:return True
        v=max(unknown,key=lambda v:(len({word[u] for u in adj[v] if word[u]>=0}),len(adj[v]),-v))
        forbidden={word[u] for u in adj[v]}
        for c in range(3):
            if c not in forbidden:
                word[v]=c
                if search():return True
        word[v]=-1
        return False
    V.require(not search(),'independent three-colour search')
    return {'three_colourable':False,'search_nodes':nodes,'algorithm':'DSATUR, vertex zero pinned to colour zero'}

def faults(graph,certificate):
    rejected=[]
    def run(name,edit):
        g,c=copy.deepcopy(graph),copy.deepcopy(certificate);edit(g,c)
        try:V.audit(g,c)
        except ValueError as e:rejected.append({'fault':name,'reason':str(e)});return
        raise ValueError('corruption accepted: '+name)
    run('boolean version',lambda g,c:c.update(version=True))
    run('short colour word',lambda g,c:c['seed_colouring'].pop())
    run('boolean colour',lambda g,c:c['seed_colouring'].__setitem__(0,True))
    run('monochromatic seed',lambda g,c:c.update(seed_colouring=[0]*21))
    run('wrong denominator',lambda g,c:g.update(denominator=14))
    run('missing point',lambda g,c:g['coordinates'].pop())
    run('duplicate point',lambda g,c:g['coordinates'].__setitem__(1,g['coordinates'][0]))
    run('boolean coefficient',lambda g,c:g['coordinates'][0].__setitem__(0,True))
    run('moved point',lambda g,c:g['coordinates'][0].__setitem__(0,g['coordinates'][0][0]+1))
    run('missing copy',lambda g,c:g['copies'].pop())
    run('duplicate isometry',lambda g,c:g['maps'].__setitem__(1,g['maps'][0]))
    run('wrong orientation',lambda g,c:g['maps'][0].update(reflection=not g['maps'][0]['reflection']))
    run('wrong copy point',lambda g,c:g['copies'][0].__setitem__(0,g['copies'][0][1]))
    run('boolean copy index',lambda g,c:g['copies'][0].__setitem__(0,True))
    run('missing unit edge',lambda g,c:g['edges'].pop())
    def extra_edge(g,c):
        edges=set(map(tuple,g['edges']))
        for i in range(651):
            for j in range(i+1,651):
                if (i,j) not in edges:g['edges']=sorted(g['edges']+[[i,j]]);return
    run('invented unit edge',extra_edge)
    return rejected

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args()
    g=json.loads((args.work/'graph.json').read_text());c=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    print(json.dumps({'algebra':algebra(),'independent_lower_search':dsatur(),'rejected_faults':faults(g,c)},sort_keys=True))
if __name__=='__main__':main()
