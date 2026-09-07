"""Literal target verifier. The CLI accepts exactly 43 physical vertices."""
from itertools import combinations
import json
from pathlib import Path
import re
import sys


def adjacency(graph,require_target=True):
    if not isinstance(graph,dict) or set(graph)!={'n','red_hex'}:raise ValueError('graph schema')
    n=graph['n'];h=graph['red_hex']
    if type(n) is not int or n<1 or n>43 or (require_target and n!=43):raise ValueError('not a 43-vertex target')
    width=(n*(n-1)//2+3)//4
    if not isinstance(h,str) or re.fullmatch(f'[0-9a-f]{{{width}}}',h) is None or int(h,16)>=2**(n*(n-1)//2):raise ValueError('graph bits')
    rows=[[0]*n for _ in range(n)]
    for k,(u,v) in enumerate(combinations(range(n),2)):rows[u][v]=rows[v][u]=(int(h,16)>>k)&1
    return rows


def count(graph,require_target=True):
    a=adjacency(graph,require_target);n=len(a);red=0;blue=0;first=None;tested=0
    for q in combinations(range(n),5):
        colors=[a[u][v] for u,v in combinations(q,2)]
        if all(colors):
            red+=1
            if first is None:first={'color':'red','vertices':list(q)}
        if not any(colors):
            blue+=1
            if first is None:first={'color':'blue','vertices':list(q)}
        tested+=1
    return {'n':n,'red_fives':red,'blue_fives':blue,'five_subsets_checked':tested,'first_violation':first,
            'status':'VERIFIED_GOOD43' if n==43 and red==blue==0 else 'VERIFIED_CONTROL_GOOD' if red==blue==0 else 'REJECTED_MONOCHROMATIC_FIVE'}


if __name__=='__main__':
    result=count(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps(result,sort_keys=True))
    if result['status']!='VERIFIED_GOOD43':sys.exit(1)
