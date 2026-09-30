"""Independent Python transport/witness layer for the native exhaustive audit.

six-reviewer-1, independent mathematical reviewer. Standard library only.
The attributed source fixture is untrusted data; no author code is imported.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

CASES = [('triangle', (0, 1, 6)), ('star', (0, 1, 2)),
         ('path', (0, 6, 11)), ('wedge_edge', (0, 1, 15)),
         ('matching', (0, 11, 18))]
ROOTS = list(itertools.combinations(range(7), 2))
POSITIONS = list(itertools.combinations(range(4), 2))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def core_edges(deleted):
    labels = [u for u in range(21) if u not in deleted]
    red = {edge(i, j) for i, j in itertools.combinations(range(18), 2)
           if not set(ROOTS[labels[i]]) & set(ROOTS[labels[j]])}
    return labels, red


def graph(red, domain, indices, joining):
    result = set(red)
    for j, i in enumerate(indices):
        need(type(i) is int and 0 <= i < len(domain), 'pattern index')
        result.update((u, 18+j) for u in range(18) if domain[i] & (1 << u))
    need(type(joining) is int and 0 <= joining < 64, 'joining mask')
    result.update((18+i, 18+j) for b, (i, j) in enumerate(POSITIONS)
                  if joining & (1 << b))
    return result


def pages(red, u, v):
    color = edge(u, v) in red
    return color, [w for w in range(22) if w != u and w != v
                   and ((edge(u, w) in red) == color)
                   and ((edge(v, w) in red) == color)]


def root_stabilizer(deleted, labels):
    root_edges = {ROOTS[u] for u in deleted}
    degrees = [sum(x in pair for pair in root_edges) for x in range(7)]
    classes = [[x for x in range(7) if degrees[x] == d] for d in sorted(set(degrees))]
    lookup = {ROOTS[u]: i for i, u in enumerate(labels)}
    out = []
    # Enumerate only degree-preserving point maps; verify adjacency afterward.
    for images in itertools.product(*(itertools.permutations(c) for c in classes)):
        point_map = dict(itertools.chain.from_iterable(zip(c, im) for c, im in zip(classes, images)))
        if {edge(point_map[a], point_map[b]) for a, b in root_edges} != root_edges:
            continue
        perm = [lookup[edge(point_map[a], point_map[b])] for a, b in (ROOTS[u] for u in labels)]
        need(sorted(perm) == list(range(18)), 'not a core permutation')
        out.append(perm)
    need(len({tuple(p) for p in out}) == len(out), 'duplicate root action')
    return out


def validate(data, fixture):
    need(data['controls'] is True and data['transport_witnesses'] == 1330, 'incomplete native census')
    need(data['cohorts'] == [35, 140, 420, 630, 105], 'core classification')
    need([x['name'] for x in data['cases']] == [n for n, d in CASES], 'native case order')
    need(fixture['format'] == 'kneser18-obstructions-v1', 'fixture format')
    need([(x['name'], tuple(x['deleted'])) for x in fixture['cases']] == CASES, 'fixture case cohort')
    result = []
    for native, source, (name, deleted) in zip(data['cases'], fixture['cases'], CASES):
        labels, red = core_edges(deleted)
        domain = native['domain']
        need(domain == sorted(set(domain)), 'domain ordering/repeats')
        need(all(type(p) is int and 0 <= p < (1 << 18) for p in domain), 'pattern range')
        pairs = native['pair_colors']
        need(pairs == sorted(pairs) and len({tuple(x) for x in pairs}) == len(pairs), 'pair ordering')
        need(all(0 <= i < j < len(domain) and c in (0, 1) for i, j, c in pairs), 'pair shape/loop')
        frontier = {tuple(x) for x in native['frontier']}
        need(len(frontier) == len(native['frontier']), 'frontier repeats')
        need(native['cross_color_flags'][0] == 0, 'cross-spine refinement fails')
        need(sum(native['cross_color_flags']) == len(frontier), 'cross histogram total')
        # Independent set-based check of every candidate and the stronger witness location.
        for key in frontier:
            indices, joining = key[:4], key[4]
            need(tuple(sorted(set(indices))) == indices, 'four-pattern order')
            g = graph(red, domain, indices, joining)
            need(any(len(ps) > (3 if c else 6)
                     for u in range(18) for v in range(18, 22)
                     for c, ps in [pages(g, u, v)]), 'no cross-spine book')
        stabilizer = root_stabilizer(deleted, labels)
        domain_lookup = {p: i for i, p in enumerate(domain)}
        covered, keys, sizes = set(), [], []
        for witness in source['obstructions']:
            indices, joining = witness['indices'], witness['joining_mask']
            need(len(indices) == 4 and indices == sorted(set(indices)), 'witness indices')
            key = tuple(indices)+(joining,)
            need(key in frontier, 'witness not in frontier')
            g = graph(red, domain, indices, joining)
            spine, listed = witness['spine'], witness['pages']
            need(len(spine) == 2 and all(type(x) is int for x in spine), 'spine shape')
            u, v = spine
            need(0 <= u < v < 22, 'spine range')
            color, actual = pages(g, u, v)
            need(len(listed) == (4 if color else 7), 'page number')
            need(all(type(w) is int and 0 <= w < 22 for w in listed), 'page range')
            need(listed == sorted(set(listed)) and set(listed) <= set(actual), 'false pages')
            orbit = set()
            for perm in stabilizer:
                need({edge(perm[a], perm[b]) for a, b in red} == red, 'false core action')
                moved = [sum(1 << perm[u] for u in range(18) if domain[i] & (1 << u)) for i in indices]
                try:
                    moved_indices = [domain_lookup[p] for p in moved]
                except KeyError as exc:
                    raise ValueError('domain transport gap') from exc
                ordered = sorted(moved_indices)
                need(len(set(ordered)) == 4, 'transport collapse')
                outside = [18+ordered.index(i) for i in moved_indices]
                full_map = perm+outside
                image = {edge(full_map[a], full_map[b]) for a, b in g}
                image_joining = sum(1 << b for b, (a, b0) in enumerate(POSITIONS)
                                    if (18+a, 18+b0) in image)
                image_key = tuple(ordered)+(image_joining,)
                need(image == graph(red, domain, ordered, image_joining), 'false full-graph transport')
                orbit.add(image_key)
            need(type(witness['orbit_size']) is int and len(orbit) == witness['orbit_size'], 'orbit size')
            need(min(orbit) == key and orbit <= frontier, 'orbit representative')
            need(not orbit & covered, 'overlapping orbit')
            covered |= orbit;keys.append(key);sizes.append(len(orbit))
        need(keys == sorted(keys) and covered == frontier, 'uncovered frontier')
        result.append({'name':name,'core_count':data['cohorts'][len(result)],
                       'domain_size':len(domain),'domain_sha256':digest(domain),
                       'colored_pairs':len(pairs),'pair_sha256':digest(pairs),
                       'compatibility_edges':native['compatibility_edges'],
                       'four_cliques':native['four_cliques'],'frontier_size':len(frontier),
                       'frontier_sha256':digest(sorted(frontier)),
                       'root_stabilizer':len(stabilizer),'obstruction_orbits':len(keys),
                       'orbit_sizes':sizes,'spine_location_flags':native['violation_flags'],
                       'cross_color_flags':native['cross_color_flags'],
                       'valid_22_completions':0})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('binary', type=Path)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    p = subprocess.run([str(args.binary.resolve())],capture_output=True,text=True,timeout=90)
    need(p.returncode == 0, 'native computation failed: '+p.stderr)
    data = json.loads(p.stdout)
    fixture_path = directory/'source_obstructions.json'
    fixture = json.loads(fixture_path.read_text())
    cases = validate(data, fixture)
    bad = []
    for label in ['format','missing_case','false_page','wrong_orbit','missing_orbit','joining_range']:
        f = copy.deepcopy(fixture)
        if label == 'format':f['format'] = 'unknown'
        elif label == 'missing_case':f['cases'].pop()
        elif label == 'false_page':f['cases'][0]['obstructions'][0]['pages'][0] = f['cases'][0]['obstructions'][0]['spine'][0]
        elif label == 'wrong_orbit':f['cases'][0]['obstructions'][0]['orbit_size'] += 1
        elif label == 'missing_orbit':f['cases'][-1]['obstructions'].pop()
        else:f['cases'][0]['obstructions'][0]['joining_mask'] = 64
        try:validate(data, f)
        except (ValueError, KeyError):bad.append(label)
        else:raise ValueError('negative control accepted: '+label)
    out = {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
           'complete':True,'masks_visited':5*(1 << 18),'transport_witnesses':1330,
           'fixture_sha256':hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
           'cases':cases,'negative_controls':bad,
           'strengthening':'Every pair-compatible four-vertex attachment has a forbidden cross-spine book.'}
    if args.expected:
        need(out == json.loads(args.expected.read_text()), 'expected-output mismatch')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
