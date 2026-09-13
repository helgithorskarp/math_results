#!/usr/bin/env python3
"""Complete collision, unit-circle and zero-weight parameter accounting."""
import argparse,json
from collections import Counter
from pathlib import Path
from interface import A,physical,HERE
import roots

def run(path):
    cert=json.loads(Path(path).read_text());one=physical.polynomial([1]);zero=physical.polynomial([])
    circle=collision=off_circle=zero_weights=0;circle_hist=Counter();zero_hist=Counter()
    for c in cert['components']:
        n=roots.nreal(c);A.need(n==c['real_embeddings'],'exact real root count')
        if not n:continue
        q,x,y=[physical.polynomial(c[k]) for k in ('q','x','y')]
        on_circle=not((x*x+3*y*y-one)%q)
        if on_circle:
            a,b=one,zero
            for _ in range(12):a,b=(a*x-3*b*y)%q,(a*y+b*x)%q
            A.need(not b and not((a-one)%q),'unit-circle parameters lie in mu12')
            circle+=n;circle_hist[str(c['point_count'])]+=n
        if c['point_count']<243:
            collision+=n
            if not on_circle:off_circle+=n
        if 0 in c['colour_weights']:
            zero_weights+=n;zero_hist[f"{c['point_count']}v_{c['edge_count']}e"]+=n
    A.need(circle==12 and dict(circle_hist)=={'84':6,'27':3,'21':3},'all twelve unit-circle roots')
    A.need(collision==200 and off_circle==188 and zero_weights==36,'collision and zero-weight counts')
    return {'status':'PASS','unit_circle_set':'all twelve roots of z^12=1','unit_circle_parameters':circle,'unit_circle_graph_vertices_by_parameter':dict(sorted(circle_hist.items())),'collision_parameters':collision,'off_unit_circle_collision_parameters':off_circle,'zero_weight_parameters':zero_weights,'zero_weight_graphs_by_parameter':dict(sorted(zero_hist.items()))}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.certificate),sort_keys=True,indent=2))
