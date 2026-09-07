"""Separate literal five-subset and set-intersection verification."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json


def certify(data):
    if not isinstance(data,dict) or set(data)!={'n','red_hex'} or type(data['n']) is not int or data['n']!=19:
        raise ValueError('Exact graph order')
    h=data['red_hex']
    if not isinstance(h,str) or len(h)!=43 or any(x not in '0123456789abcdef' for x in h):raise ValueError('Graph encoding')
    bits=int(h,16)
    if bits.bit_length()>171:raise ValueError('Unused bit set')
    pairs=list(combinations(range(19),2));red={pair for k,pair in enumerate(pairs) if bits>>k&1}
    groups={1:[],0:[]}
    for q in combinations(range(19),4):
        edges=list(combinations(q,2));number=sum(pair in red for pair in edges)
        if number==6:groups[1].append(list(q))
        elif number==0:groups[0].append(list(q))
    for q in combinations(range(19),5):
        number=sum(pair in red for pair in combinations(q,2))
        if number in (0,10):raise ValueError('Forbidden five-subset')
    intersections=Counter()
    for first,second in combinations(groups[1]+groups[0],2):
        size=len(set(first).intersection(second))
        if size==0:raise ValueError('Disjoint homogeneous fours')
        intersections[size]+=1
    for color in (1,0):groups[color].sort(key=lambda q:sum(1<<v for v in q))
    n4=len(groups[1])+len(groups[0])
    if n4==0:raise ValueError('Packing number is zero')
    return {'status':'VERIFIED_GOOD19_PACKING_BRIDGE_COUNTEREXAMPLE','n':19,'red_edges':len(red),
            'red_fours':groups[1],'blue_fours':groups[0],'red_fives':0,'blue_fives':0,
            'four_pairs':n4*(n4-1)//2,'four_intersection_sizes':{str(k):v for k,v in sorted(intersections.items())},
            'vertex_disjoint_monochromatic_four_packing_number':1}

if __name__=='__main__':
    import sys
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('graph.json')
    print(json.dumps(certify(json.loads(path.read_text())),indent=2,sort_keys=True))
