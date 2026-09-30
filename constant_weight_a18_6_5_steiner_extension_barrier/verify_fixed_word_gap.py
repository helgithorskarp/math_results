"""Separate complete set/pair-incidence replay of the fixed-word frontier.
Both implementations are by six-code-2, researcher; no peer audit is claimed.
Default imports no production enumerator or search. --compare checks every
record entry against the production MRV implementation. Guards are INCOMPLETE.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import resource
import time
from geometry import classical_design, mask, points, require
from verify_three_gap import pair_graph
from verify_four_gap import close_group

def record_hash(records):
    return sha256((json.dumps(records, separators=(',', ':')) + '\n').encode()).hexdigest()

def normalization(circles, two, single=None):
    start = time.monotonic()
    group, circle_permutations = close_group(circles)
    design = {frozenset(points(c)): c for c in circles}
    contained = {frozenset(q) for c in design for q in combinations(sorted(c), 4)}
    universe = set(map(frozenset, combinations(range(17), 4))) - contained
    fixed = frozenset(points(two['fixed_four_set']))
    orbit = {frozenset(p[i] for i in fixed) for p in group}
    require(orbit == universe and len(orbit) == 2040, 'noncontained orbit incomplete')
    stabilizer = [p for p in group if frozenset(p[i] for i in fixed) == fixed]
    require(len(stabilizer) == 8, 'incorrect pointed stabilizer')
    first_gaps = {c for pts, c in design.items() if len(pts & fixed) >= 3}
    domain = {mask(q) for q in universe if len(q & fixed) <= 1
              and len({c for pts, c in design.items() if len(pts & q) >= 3} & first_gaps) == 1}
    covered = set()
    for case in two['cases']:
        q = frozenset(points(case['second_four_set']))
        partner_orbit = {mask(p[i] for i in q) for p in stabilizer}
        require(partner_orbit <= domain and not partner_orbit & covered, 'bad partner orbit')
        require(sorted(partner_orbit) == case['partner_orbit']
                and len(partner_orbit) == case['orbit_size'], 'partner orbit mismatch')
        gaps = first_gaps | {c for pts, c in design.items() if len(pts & q) >= 3}
        require(sorted(gaps) == case['gaps'] and len(gaps) == 7, 'incorrect pair gaps')
        covered.update(partner_orbit)
    require(covered == domain and len(domain) == 132 and len(two['cases']) == 18,
            'pointed pair cover incomplete')
    if single is not None:
        require(single['fixed_four_set'] == two['fixed_four_set'], 'fixed four-set mismatch')
        extra_domain = set(combinations(sorted(set(circles) - first_gaps), 2))
        extra_cover = set()
        for case in single['cases']:
            pts = [frozenset(points(c)) for c in case['extra_gaps']]
            images = {tuple(sorted(mask(p[i] for i in c) for c in pts)) for p in stabilizer}
            require(images <= extra_domain and not images & extra_cover, 'bad extra-pair orbit')
            require(sorted(map(list, images)) == case['extra_orbit']
                    and len(images) == case['orbit_size'], 'extra-pair orbit mismatch')
            require(sorted(first_gaps | set(case['extra_gaps'])) == case['gaps'], 'wrong single gaps')
            extra_cover.update(images)
        require(extra_cover == extra_domain and len(extra_domain) == 2016,
                'pointed extra-pair cover incomplete')
    return {'group_order': len(group), 'noncontained_words': len(universe),
            'partner_count': len(domain), 'pair_cases': len(two['cases']),
            'single_cases': 0 if single is None else len(single['cases']),
            'seconds': time.monotonic() - start}

def enumerate_sets(circles, gaps, fixed_words):
    start = time.monotonic()
    design = tuple(frozenset(points(c)) for c in circles)
    circle_set = set(design)
    gap_sets = {frozenset(points(c)) for c in gaps}
    fixed_sets = [frozenset(points(q)) for q in fixed_words]
    records, nodes, tested = [], 0, 0
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < 45, 'INCOMPLETE: set enumeration time guard')
        tested += 1
        b = frozenset(pts)
        if b in circle_set or any(len(b & q) > 2 for q in fixed_sets):
            continue
        blockers = [c for c in design if c not in gap_sets and len(c & b) >= 3]
        if any(len(c & b) >= 4 for c in blockers):
            continue
        options = []
        for c in blockers:
            choices = [frozenset(q) for q in combinations(sorted(c), 4)]
            choices = [q for q in choices if len(q & b) <= 2
                       and all(len(q & fixed) <= 1 for fixed in fixed_sets)]
            options.append([(q, frozenset(combinations(sorted(q), 2))) for q in choices])
        selected = []

        def visit(i, owned_pairs):
            nonlocal nodes
            nodes += 1
            if nodes % 1024 == 0:
                require(time.monotonic() - start < 45, 'INCOMPLETE: set recursion time guard')
                require(len(records) <= 40000, 'INCOMPLETE: set record count guard')
            if i == len(options):
                records.append((mask(b), tuple(sorted(mask(q) for q in selected))))
                return
            for q, pairs in options[i]:
                if pairs.isdisjoint(owned_pairs):
                    selected.append(q)
                    visit(i + 1, owned_pairs | pairs)
                    selected.pop()

        visit(0, frozenset())
    records.sort()
    require(tested == 6188 and len(set(records)) == len(records), 'bad old-set coverage')
    require(len(records) <= 40000, 'INCOMPLETE: final set record count guard')
    return records, {'records': len(records), 'records_sha256': record_hash(records),
                     'nodes': nodes, 'seconds': time.monotonic() - start}

def clique_census(adjacency, forbidden):
    start = time.monotonic()
    require(2 <= forbidden <= 8, 'unsupported exclusion target')
    counts = [0] * forbidden
    nodes = 0

    def visit(candidates, depth):
        nonlocal nodes
        while candidates:
            nodes += 1
            if nodes % 1024 == 0:
                require(time.monotonic() - start < 45, 'INCOMPLETE: clique census guard')
            bit = candidates & -candidates
            v = bit.bit_length() - 1
            candidates ^= bit
            counts[depth] += 1
            tail = candidates & adjacency[v]
            if depth == forbidden - 2:
                require(not tail, 'purported forbidden clique exists')
            elif tail:
                visit(tail, depth + 1)

    visit((1 << len(adjacency)) - 1, 0)
    require(counts[0] == len(adjacency), 'vertex census mismatch')
    for i, row in enumerate(adjacency):
        require(time.monotonic() - start < 45, 'INCOMPLETE: graph symmetry guard')
        require(not row >> i & 1, 'self-loop')
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(adjacency[j] >> i & 1, 'asymmetric graph')
            later ^= bit
    require(2 * counts[1] == sum(row.bit_count() for row in adjacency), 'edge census mismatch')
    return {'cliques_by_size': {str(i + 1): c for i, c in enumerate(counts)},
            'forbidden_clique': forbidden, 'seconds': time.monotonic() - start}

def check_witness(circles, records, gaps, fixture, fixed_words):
    words = fixture['words']
    require(len(words) == len(set(words)) == fixture['size'], 'incorrect witness size')
    require(all(type(w) is int and 0 <= w < 1 << 18 for w in words), 'word outside universe')
    sets = [frozenset(i for i in range(18) if w >> i & 1) for w in words]
    require(all(len(w) == 5 for w in sets), 'incorrect weight')
    require(all(len(a & b) <= 2 for a, b in combinations(sets, 2)), 'incompatible words')
    indices = fixture['indices']
    require(all(type(i) is int and 0 <= i < len(records) for i in indices), 'bad record index')
    outsiders = {records[i][0] for i in indices}
    qs = {q for i in indices for q in records[i][1]}
    require(len(outsiders) == len(indices) == fixture['s'], 'repeated or incorrect outsider')
    require(sorted(outsiders) == fixture['outsiders'] and sorted(qs) == fixture['old_parts'],
            'witness records mismatch')
    design = {frozenset(points(c)): c for c in circles}
    outsider_sets = [frozenset(points(b)) for b in outsiders]
    removed = set(gaps) | {c for pts, c in design.items()
                           if any(len(pts & b) >= 3 for b in outsider_sets)}
    expansion = (set(circles) - removed) | outsiders | {q | (1 << 17) for q in qs | set(fixed_words)}
    require(sorted(expansion) == words, 'expansion mismatch')
    x_words = {w for w in words if w >> 17 & 1}
    contained = {w for w in x_words if any((w & ((1 << 17) - 1)) & c
                                         == w & ((1 << 17) - 1) for c in circles)}
    a = len(contained)
    t = len(x_words - contained)
    r = len(set(circles) - set(words))
    s = len({w for w in words if not w >> 17 & 1} - set(circles))
    require((s, a, t, r, r - a) == tuple(fixture[k] for k in ('s', 'a', 't', 'R', 'g')),
            'packing parameters mismatch')
    require(r - a == len(gaps), 'gap count mismatch')
    return {'size': len(words), 's': s, 't': t, 'g': r - a}

def verify_case(circles, case, production_result, branch, fixed, compare):
    start = time.monotonic()
    fixed_words = (fixed,) if branch == 'single' else (fixed, case['second_four_set'])
    require(production_result['complete'], 'production case incomplete')
    require(production_result['gaps'] == case['gaps'], 'production gap mismatch')
    records, enumeration = enumerate_sets(circles, case['gaps'], fixed_words)
    require(enumeration['records'] == production_result['enumeration']['records']
            and enumeration['records_sha256'] == production_result['enumeration']['records_sha256'],
            'full record digest mismatch')
    if compare:
        from generate_fixed_word_gap import enumerate_fixed_words
        other, _ = enumerate_fixed_words(circles, case['gaps'], fixed_words)
        require(records == other, 'entrywise record mismatch')
        del other
    adjacency, graph_hash = pair_graph(records)
    require(graph_hash == production_result['graph']['graph_sha256'], 'full graph digest mismatch')
    maximum = production_result['witness']['s']
    census = clique_census(adjacency, maximum + 1)
    require(census['cliques_by_size'][str(maximum)] > 0, 'no attaining clique')
    require(census['cliques_by_size']['2'] == production_result['graph']['edges'], 'edge count mismatch')
    if maximum >= 3:
        require(census['cliques_by_size']['3'] == production_result['graph']['triangles'], 'triangle count mismatch')
    witness = check_witness(circles, records, case['gaps'], production_result['witness'], fixed_words)
    return {'case': case['case'], 'branch': branch, 'enumeration': enumeration,
            'graph_sha256': graph_hash, 'census': census, 'witness': witness,
            'entrywise_comparison': compare, 'complete': True,
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('fixed_word_gap_expected.json'))
    parser.add_argument('--branch',choices=('single','pair','both'),default='both')
    parser.add_argument('--case',type=int)
    parser.add_argument('--compare',action='store_true')
    parser.add_argument('--checkpoint-dir',type=Path)
    args=parser.parse_args()
    expected=json.loads(args.expected.read_text())
    circles,_=classical_design()
    pair,single=expected['pair_normalization'],expected['single_normalization']
    print(json.dumps({'normalization':normalization(circles,pair,single)}),flush=True)
    branches=('pair','single') if args.branch=='both' else (args.branch,)
    total,seconds,maxima=0,0,Counter()
    for branch in branches:
        norm=pair if branch=='pair' else single
        fixtures=expected[branch+'_cases']
        require(len(fixtures)==len(norm['cases']), 'case manifest incomplete')
        require([c['case'] for c in fixtures]==list(range(len(fixtures))), 'case numbering incomplete')
        cases=norm['cases'] if args.case is None else [norm['cases'][args.case]]
        for case in cases:
            result=verify_case(circles,case,fixtures[case['case']],
                               'two' if branch=='pair' else 'single',norm['fixed_four_set'],args.compare)
            require(result['census']['cliques_by_size']==fixtures[case['case']]['cliques_by_size'],
                    'complete clique census mismatch')
            if args.checkpoint_dir is not None:
                args.checkpoint_dir.mkdir(parents=True,exist_ok=True)
                path=args.checkpoint_dir / (branch+'-'+str(case['case'])+'.json')
                temporary=path.with_suffix('.tmp')
                temporary.write_text(json.dumps(result,indent=2)+'\n')
                temporary.replace(path)
            total+=1; seconds+=result['seconds']; maxima[(branch,result['witness']['s'])]+=1
            print(json.dumps({'branch':branch,'case':case['case'],'complete':True,
                              'maximum_outsiders':result['witness']['s'],'seconds':result['seconds']}),flush=True)
    print(json.dumps({'complete_cases':total,'coverage':'all313cases' if total==313 else 'partial',
                      'maxima':{str(k):v for k,v in sorted(maxima.items())},'seconds':seconds}),flush=True)


if __name__ == '__main__':
    main()
