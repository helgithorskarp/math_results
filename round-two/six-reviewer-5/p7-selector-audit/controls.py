"""Semantic damages and exhaustive small-graph oracle, normal and -O."""
import copy
from itertools import combinations
import json
from pathlib import Path
from interface import decode_all, opposite_hypotheses, literal, HERE
from selectors import guaranteed_points, check, remaining_boundary
from rows import domain
from inventory import derive
from clique import maximum
from star_primitives import require


def checks():
    rejected = []
    def reject(label, call):
        try: call()
        except (ValueError,RuntimeError,IndexError): rejected.append(label)
        else: raise ValueError('damage accepted: '+label)
    stars = json.loads((HERE/'fixtures.json').read_text())['stars']
    carrier = json.loads((HERE/'BRIDGE34.json').read_text())['raw_positive_maps']
    witness = json.loads((HERE/'WITNESS61.json').read_text())
    reject('missing normalized core',lambda:decode_all(stars,carrier[:-1]))
    damaged = copy.deepcopy(carrier); damaged[-1] = copy.deepcopy(damaged[-2])
    reject('duplicate normalized physical carrier',lambda:decode_all(stars,damaged))
    damaged = copy.deepcopy(carrier); damaged[23]['point_map'][0] = damaged[23]['point_map'][1]
    reject('nonbijective physical point transport',lambda:decode_all(stars,damaged))
    damaged = copy.deepcopy(carrier); damaged[23]['word_masks'][0] ^= 1
    reject('changed actual core',lambda:decode_all(stars,damaged))
    reject('duplicate completion word',lambda:literal(witness['word_masks']+[witness['word_masks'][0]]))
    missing = list(witness['word_masks']); missing.remove(next(m for m in missing if m >> witness['roles'][0] & 1))
    reject('missing saturated-center word',lambda:opposite_hypotheses(missing,witness['roles']))
    reject('wrong center orientation',lambda:opposite_hypotheses(witness['word_masks'],[witness['roles'][1],witness['roles'][0],*witness['roles'][2:]]))
    reject('collapsed opposite hubs',lambda:opposite_hypotheses(witness['word_masks'],[witness['roles'][0],witness['roles'][1],witness['roles'][2],witness['roles'][2],witness['roles'][4]]))
    reject('covered tail outside physical count',lambda:guaranteed_points(6,6,0,0))
    reject('negative outside edges',lambda:guaranteed_points(6,5,0,-1))
    _,rows,_ = domain(); _,survivors,_,_ = derive(rows,(2,2,3),2,1)
    wrong = copy.deepcopy(survivors[0]); wrong['Q'] = 2
    reject('last reciprocal required charge altered',lambda:check(rows,(2,2,3),2,1,wrong))
    wrong = copy.deepcopy(survivors[0]); wrong['X'] = 1
    reject('unit-SS boundary lost',lambda:remaining_boundary(rows,(2,2,3),wrong))
    reject('asymmetric residual graph',lambda:maximum([2,0]))
    reject('incomplete clique guard',lambda:maximum([2,1],node_cap=0))
    graphs = 0
    for n in range(6):
        pairs = tuple(combinations(range(n),2))
        for bits in range(1 << len(pairs)):
            adjacency = [0]*n
            for i,(a,b) in enumerate(pairs):
                if bits >> i & 1: adjacency[a] |= 1 << b; adjacency[b] |= 1 << a
            clique,_ = maximum(adjacency)
            brute = max((s.bit_count() for s in range(1 << n) if
                         all(adjacency[a] >> b & 1 for a,b in pairs if s >> a & 1 and s >> b & 1)),default=0)
            require(len(clique) == brute,'independent complete subset-clique oracle differs')
            graphs += 1
    require(graphs == 1100 and len(rejected) == 14,'complete semantic controls')
    return {'semantic_damages_rejected':rejected,'exhaustive_simple_graphs_n_le5':graphs,
            'literal_sharp61_positive_control':True}
