#!/usr/bin/env python3
"""Exact descriptions of the real unit-circle and zero-weight boundaries."""
import argparse,json
from collections import Counter
from pathlib import Path
from interface import A,physical
import roots


def run(path):
    j=json.loads(Path(path).read_text());one=physical.polynomial([1]);zero=physical.polynomial([])
    hist=Counter();circle=0;zero_weights=0
    for c in j['components']:
        n=roots.nreal(c)
        A.need(n==c['real_embeddings'],'exact real count')
        if not n:continue
        q,x,y=[physical.polynomial(c[k]) for k in ('q','x','y')]
        if not(x*x+3*y*y-one)%q:
            a,b=one,zero
            for _ in range(6):a,b=(a*x-3*b*y)%q,(a*y+b*x)%q
            A.need(not b and not(a*a-one)%q,'unit-circle roots are twelfth roots of unity')
            circle+=n;hist[str(c['point_count'])]+=n
        if 0 in c['colour_weights']:
            zero_weights+=n
            A.need(c['point_count']==129 and c['edge_count']==195 and len(c['active_curves'])==62,'zero-weight physical family')
    A.need(circle==12 and dict(hist)=={'84':6,'27':3,'21':3},'complete unit-circle boundary')
    A.need(zero_weights==8,'complete zero-weight boundary')
    return {'status':'PASS','unit_circle_parameters':circle,'unit_circle_set':'all twelve roots of z^12=1','unit_circle_graph_vertices_by_parameter':dict(sorted(hist.items())),'zero_weight_parameters':zero_weights}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.certificate),sort_keys=True,indent=2))
