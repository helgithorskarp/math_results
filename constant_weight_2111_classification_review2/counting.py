"""Exact finite arithmetic checks supplement the ordinary row-count proof."""
from itertools import combinations
from carrier import require

def validate():
    pairs = tuple(combinations(range(3), 2))
    graphs = []
    for mask in range(8):
        edges = tuple(pair for i, pair in enumerate(pairs) if mask >> i & 1)
        homogeneous = sum(sum(z in edge for edge in edges) in (0, 2) for z in range(3))
        require(homogeneous == (3 if len(edges) in (0, 3) else 1), 'homogeneous triple incidence identity failed')
        graphs.append({'edges':edges,'homogeneous':homogeneous})
    possible_u = tuple(u for u in range(0, 19, 2) if 96 <= 54 + 5 * u)
    require(possible_u == (10, 12, 14, 16, 18), 'ten-unit row parity bound failed')
    for u in possible_u:
        for n4 in range(u + 1):
            for n5 in range(u - n4 + 1):
                n6 = u - n4 - n5
                D = 2 * n4 + n5
                J = 3 * (18 - u) + 4 * n4 + 6 * n5 + 8 * n6
                require(J == 54 + 5 * u - 2 * D, 'exact row homogeneous incidence identity failed')
                if J < 96:
                    continue
                require((J - 96) % 2 == 0, 'homogeneous excess parity failed')
                P = (J - 96) // 2
                require(D + P == (5 * u - 42) // 2, 'row count exact refinement failed')
                if u == 10:
                    require(D + P == 4 and n6 >= 6 + n4, 'boundary unit-core distribution refinement failed')
    require(min(u for u in range(0, 19, 2) if 3*u >= 42) == 14, 'conditional five-edge transfer failed')
    require(not any(u >= 42 for u in range(0, 19)), 'conditional four-edge exclusion failed')
    return {'status':'COMPLETE arithmetic bridges; ordinary mathematical premises external', 'three_vertex_graphs':graphs, 'necessary_unit_counts':possible_u, 'u10_identity':'2*n4+n5+P=4 and n6>=6+n4', 'cap5_implies_u_at_least':14,'cap4_excludes72_conditionally':True}

if __name__=='__main__':
    import json
    print(json.dumps(validate(),indent=2))
