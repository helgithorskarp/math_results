"""Finite audit of the new equality obstruction, not a Ramsey graph search."""
from itertools import combinations


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def audit():
    triples = list(combinations(range(4),3))
    pairs = list(combinations(range(4),2))
    for mask in range(8):
        x,y,z = ((mask >> k)&1 for k in range(3))
        require(x*y+x*z+(1-y)*(1-z) == int(x==y==z)+x,
                'mixed-triple identity')
    equality = [(d,degree) for d in range(18) for degree in range(18,25)
                if 38-d+degree <= 39]
    require(equality == [(17,18)], 'mixed-triple equality boundary')
    allowed = [s for s in range(16)
               if all(len({(s >> v)&1 for v in q}) == 2 for q in triples)]
    require(allowed == [s for s in range(16) if s.bit_count()==2],
            'outside four-contact patterns')
    records = []
    for mask in range(64):
        edges = {e:(mask >> k)&1 for k,e in enumerate(pairs)}
        def color(a,b):
            return edges[tuple(sorted((a,b)))]
        if any(len({color(a,b) for a,b in combinations(q,2)})==1 for q in triples):
            continue
        forced = [set() for _ in range(4)]
        for q in triples:
            centers = [(v,c) for v in q for c in (0,1)
                       if all(color(v,w)==c for w in q if w!=v)]
            require(len(centers)==1, 'unique mixed-triple center')
            v,c = centers[0]
            forced[v].add(18 if c else 24)
            fourth = next(x for x in range(4) if x not in q)
            require(len({color(fourth,x) for x in q})==2,
                    'fourth vertex must distinguish')
        require(all(len(s)==1 for s in forced), 'consistent forced degrees')
        degrees = [next(iter(s)) for s in forced]
        internal = [sum(color(v,w) for w in range(4) if w!=v) for v in range(4)]
        require(all(d in (1,2) for d in internal), 'internal degree classification')
        feasible = [t for t in range(24)
                    if t<=13 and 23-t<=13
                    and sum(degrees)==4*t+16*2+sum(internal)]
        require(not feasible, 'quadruple boundary unexpectedly feasible')
        records.append({'mask':mask,'internal_red_degrees':internal,
                        'forced_total_red_degrees':degrees,
                        'required_four_times_red_uniform':sum(degrees)-32-sum(internal)})
    require(len(records)==18, 'all 18 nonmonochromatic K4 colorings')
    require(sorted({r['required_four_times_red_uniform'] for r in records}) == [32,46,60],
            'three equality alternatives')
    return {'status':'VERIFIED_FOUR_SET_DISTINGUISHER_OBSTRUCTION',
            'all_K4_colorings_checked':64,'surviving_internal_colorings':18,
            'outside_signatures_checked':16,'mixed_signatures_checked':8,
            'equality_pairs':equality,'permitted_outside_signatures':allowed,
            'records':records,'global_four_set_distinguisher_minimum':17,
            'row_class_cap_on_20_side':3}
