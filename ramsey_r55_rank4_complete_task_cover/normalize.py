"""Transport any admissible rank-four factor presentation into a covered task."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import re
import sys
import model


@lru_cache(maxsize=1)
def linear_maps():
    maps=[]
    def extend(basis,span):
        if len(basis)==4:
            image=[]
            for x in range(16):
                y=0
                for k,b in enumerate(basis):
                    if x>>k&1:y^=b
                image.append(y)
            maps.append(tuple(image));return
        for b in range(1,16):
            if b not in span:extend(basis+[b],span|{x^b for x in span})
    extend([],{0})
    if len(maps)!=20160:raise ValueError('group size')
    return tuple(maps)


def normalize(data):
    if not isinstance(data,dict) or set(data)!={'rows','columns','internal_hex'}:raise ValueError('factor schema')
    rows,cols=data['rows'],data['columns'];h=data['internal_hex']
    for xs,n in [(rows,20),(cols,23)]:
        if not isinstance(xs,list) or len(xs)!=n or any(type(x) is not int or not 0<=x<16 for x in xs) or model.rank(xs)!=4:raise ValueError('factor list')
    counts=Counter(rows)
    if counts[0]>1 or max(counts.values())>3:raise ValueError('row caps')
    if not isinstance(h,str) or re.fullmatch('[0-9a-f]{111}',h) is None or int(h,16)>=2**443:raise ValueError('internal encoding')
    best=None;chosen=None
    for image in linear_maps():
        code=sum(counts[x]<<(2*(image[x]-1)) for x in range(1,16))
        if best is None or code<best:best=code;chosen=image
    dual=[]
    for b in range(16):
        values=[z for z in range(16) if all(model.dot(chosen[1<<k],z)==((b>>k)&1) for k in range(4))]
        if len(values)!=1:raise ValueError('dual transport')
        dual.append(values[0])
    left=sorted(range(20),key=lambda i:(chosen[rows[i]],i))
    right=sorted(range(23),key=lambda j:(dual[cols[j]],j))
    order=left+[20+j for j in right]
    if [chosen[rows[i]] for i in left]!=model.rows_from_code(best):raise ValueError('normal row layout')
    old_internal={pair:(int(h,16)>>k)&1 for k,pair in enumerate(p for p in combinations(range(43),2) if (p[0]<20)==(p[1]<20))}
    bits=0
    for k,(i,j) in enumerate(p for p in combinations(range(43),2) if (p[0]<20)==(p[1]<20)):
        bits|=old_internal[tuple(sorted((order[i],order[j])))]<<k
    parameters={'row_code':best,'columns':[dual[cols[j]] for j in right],'internal_hex':format(bits,'0111x')}
    task=model.target(best)
    return {'parameters':parameters,'new_to_old':order,'row_linear_map':list(chosen),'column_dual_map':dual,
            'base_filters_hold':task.base_holds(parameters['columns'],bits),'graph':task.graph(parameters['columns'],bits)}


if __name__=='__main__':print(json.dumps(normalize(json.loads(Path(sys.argv[1]).read_text())),sort_keys=True))
