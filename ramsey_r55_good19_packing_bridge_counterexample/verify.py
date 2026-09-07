"""Independent bitset certificate for the failed nineteen-vertex packing bridge."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,json


def certify(graph):
    if not isinstance(graph,dict) or set(graph)!={'n','red_hex'} or type(graph['n']) is not int or graph['n']!=19:
        raise ValueError('Exactly19 physical vertices required')
    h=graph['red_hex']
    if not isinstance(h,str) or len(h)!=43 or any(c not in '0123456789abcdef' for c in h) or int(h,16)>=1<<171:
        raise ValueError('Exact171 graph bits required')
    bits=int(h,16);red=[0]*19;position=0
    for u in range(19):
        for v in range(u+1,19):
            if bits>>position&1:red[u]|=1<<v;red[v]|=1<<u
            position+=1
    universe=(1<<19)-1;blue=[universe^row^(1<<v) for v,row in enumerate(red)]
    def cliques(rows,candidates,size,prefix=0):
        if size==0:
            yield prefix;return
        while candidates.bit_count()>=size:
            bit=candidates&-candidates;candidates^=bit
            yield from cliques(rows,candidates&rows[bit.bit_length()-1],size-1,prefix|bit)
    red5=list(cliques(red,universe,5));blue5=list(cliques(blue,universe,5))
    if red5 or blue5:raise ValueError('Monochromatic5-set exists')
    rf=sorted(cliques(red,universe,4));bf=sorted(cliques(blue,universe,4));all4=rf+bf
    if not all4:raise ValueError('Packing number is zero')
    intersections=Counter((x&y).bit_count() for x,y in combinations(all4,2))
    if intersections[0]:raise ValueError('Disjoint monochromatic4-sets exist')
    def vertices(mask):return [v for v in range(19) if mask>>v&1]
    return {'status':'VERIFIED_GOOD19_PACKING_BRIDGE_COUNTEREXAMPLE','n':19,'red_edges':bits.bit_count(),
            'red_fours':[vertices(x) for x in rf],'blue_fours':[vertices(x) for x in bf],
            'red_fives':0,'blue_fives':0,'four_pairs':len(all4)*(len(all4)-1)//2,
            'four_intersection_sizes':{str(k):v for k,v in sorted(intersections.items()) if v},
            'vertex_disjoint_monochromatic_four_packing_number':1}


if __name__=='__main__':
    import sys
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('graph.json')
    result=certify(json.loads(path.read_text()))
    print(json.dumps(result,indent=2,sort_keys=True))
