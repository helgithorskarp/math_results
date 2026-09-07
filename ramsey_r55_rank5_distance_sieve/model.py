"""Complete h3783 baseline with physical duplicate-row distance filtering."""
from itertools import combinations
import json
import sys

import base_model
from base_model import factors, physical


def selected_pairs(row_labels):
    groups={}
    for vertex,label in enumerate(row_labels):
        groups.setdefault(label,[]).append(vertex)
    classes=sorted((vertices for vertices in groups.values() if len(vertices)>=2),
                   key=lambda vertices:vertices[0])
    return [vertices[:2] for vertices in classes]


def pair_distances(graph,pairs):
    bits=int(graph['red_hex'],16)
    rows=[0]*43
    for k,(a,b) in enumerate(combinations(range(43),2)):
        if bits >> k & 1:
            rows[a] |= 1 << b;rows[b] |= 1 << a
    result=[]
    for a,b in pairs:
        mask=(rows[a]^rows[b]) & ~((1 << a)|(1 << b))
        result.append({'pair':[a,b],'distinguishers':[v for v in range(43) if mask >> v & 1]})
    return result


def classify(data):
    previous=base_model.classify(data)
    if not previous.get('baseline') or not previous.get('keep'):
        return {'baseline':False,'reason':'outside_previous_rank5_sieve','previous':previous}
    a,b,bits=factors(data)
    pairs=selected_pairs(a)
    distances=pair_distances(physical(data),pairs)
    for record in distances:
        if len(record['distinguishers'])<8:
            return {'baseline':True,'keep':False,'reason':'duplicate_row_distance',
                    'selected_pairs':pairs,'failed_pair':record}
    return {'baseline':True,'keep':True,'reason':'survives_necessary_distance_filter',
            'selected_pairs':pairs}


if __name__=='__main__':
    with open(sys.argv[1],encoding='utf-8') as f:data=json.load(f)
    print(json.dumps({'classification':classify(data),'graph':physical(data)},sort_keys=True))
