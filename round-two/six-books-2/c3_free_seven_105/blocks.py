"""Exact C3 block constructions and literal ordinary-book page counts."""
import itertools
import json

PAIRS = list(itertools.combinations(range(7), 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_spec(spec):
    require(set(spec) == {'internal', 'cross', 'joins'}, 'spec schema')
    require(len(spec['internal']) == 7 and all(type(x) is int and x in (0, 1)
            for x in spec['internal']), 'internal bits')
    require(len(spec['cross']) == 21 and all(type(x) is int and 0 <= x <= 7
            for x in spec['cross']), 'oriented cross masks')
    require(spec['joins'] is None or (len(spec['joins']) == 7 and all(type(x) is int
            and x in (0, 1) for x in spec['joins'])), 'fixed joins')


def graph(spec):
    """Build red neighbor sets by explicitly applying the action to each edge."""
    validate_spec(spec)
    n = 21 if spec['joins'] is None else 22
    rows = [set() for _ in range(n)]
    edge_orbits = []
    for i, red in enumerate(spec['internal']):
        if red:
            edge_orbits.append([(3*i+t, 3*i+(t+1) % 3) for t in range(3)])
    for (i, j), mask in zip(PAIRS, spec['cross']):
        for offset in range(3):
            if mask >> offset & 1:
                edge_orbits.append([(3*i+t, 3*j+(t+offset) % 3) for t in range(3)])
    if spec['joins'] is not None:
        for i, red in enumerate(spec['joins']):
            if red:
                edge_orbits.append([(3*i+t, 21) for t in range(3)])
    for orbit in edge_orbits:
        for a, b in orbit:
            require(a != b and b not in rows[a], 'loop or duplicate edge orbit')
            rows[a].add(b)
            rows[b].add(a)
    return rows


def literal_summary(rows, red_cap=3, blue_cap=6):
    n = len(rows)
    universe = set(range(n))
    for i, row in enumerate(rows):
        require(i not in row and row <= universe, 'row loop/range')
        require(all(i in rows[j] for j in row), 'asymmetric graph')
    red_hist, blue_hist, bad = {}, {}, []
    for i, j in itertools.combinations(range(n), 2):
        red = j in rows[i]
        pages = rows[i] & rows[j] if red else universe-{i, j}-rows[i]-rows[j]
        count = len(pages)
        hist = red_hist if red else blue_hist
        hist[str(count)] = hist.get(str(count), 0)+1
        if count > (red_cap if red else blue_cap):
            bad.append(dict(spine=[i, j], color='red' if red else 'blue', pages=sorted(pages)))
    degrees = list(map(len, rows))
    return dict(vertices=n, edges=sum(degrees)//2,
                degrees_histogram={str(d): degrees.count(d) for d in sorted(set(degrees))},
                red_histogram=red_hist, blue_histogram=blue_hist,
                caps_valid=not bad, violations=bad, degrees=degrees)


def variable_bindings():
    """Ids1..7 are triangle bits; ids8..70 are oriented pair-offset bits."""
    internal = list(range(1, 8))
    cross = {pair: [8+3*j+k for k in range(3)] for j, pair in enumerate(PAIRS)}
    return internal, cross


def assignment(spec):
    validate_spec(spec)
    internal, cross = variable_bindings()
    values = {v: bool(t) for v, t in zip(internal, spec['internal'])}
    for pair, mask in zip(PAIRS, spec['cross']):
        for k, var in enumerate(cross[pair]):
            values[var] = bool(mask >> k & 1)
    return values


def decode_model(model, joins):
    values = {abs(x): x > 0 for x in model}
    require(all(v in values for v in range(1, 71)), 'incomplete70-bit model')
    internal, cross = variable_bindings()
    spec = dict(internal=[int(values[v]) for v in internal],
                cross=[sum(int(values[v]) << k for k, v in enumerate(cross[pair]))
                       for pair in PAIRS], joins=joins)
    validate_spec(spec)
    return spec


def kg_control():
    roots = list(itertools.combinations(range(7), 2))
    action = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6}
    seen, ordered = set(), []
    for pair in roots:
        if pair in seen:
            continue
        orbit = [pair]
        for _ in range(2):
            orbit.append(tuple(sorted(action[x] for x in orbit[-1])))
        require(len(set(orbit)) == 3 and tuple(sorted(action[x] for x in orbit[-1])) == pair,
                'KG action is not seven free triples')
        seen.update(orbit)
        ordered += orbit
    require(len(ordered) == 21 and len(seen) == 21, 'KG action labeling coverage')
    rows = [{j for j, q in enumerate(ordered) if set(p).isdisjoint(q)}
            for p in ordered]
    spec = dict(internal=[int(3*i+1 in rows[3*i]) for i in range(7)],
                cross=[sum(int(3*j+k in rows[3*i]) << k for k in range(3)) for i, j in PAIRS],
                joins=None)
    require(graph(spec) == rows, 'KG action/block construction mismatch')
    result = literal_summary(rows)
    require(result['edges'] == 105 and result['red_histogram'] == {'3':105}
            and result['blue_histogram'] == {'5':105}, 'KG positive control pages')
    return spec, ordered, result


def rows_text(rows):
    return ''.join(''.join('1' if j in row else '0' for j in range(len(rows)))+'\n'
                   for row in rows)


if __name__ == '__main__':
    spec, labels, summary = kg_control()
    print(json.dumps(dict(spec=spec, root_pairs=labels, summary=summary), sort_keys=True))
