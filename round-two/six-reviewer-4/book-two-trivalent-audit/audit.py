#!/usr/bin/env python3
"""Independent component enumeration; no campaign implementation imports."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import platform
import time

PAIRS = tuple(combinations(range(11), 2))
BIT = {p: 1 << k for k, p in enumerate(PAIRS)}
ALL = (1 << 11) - 1


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vertices(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def edge(i, j):
    return BIT[tuple(sorted((i, j)))]


def rows(mask):
    out = [0] * 11
    for k, (i, j) in enumerate(PAIRS):
        if mask >> k & 1:
            out[i] |= 1 << j
            out[j] |= 1 << i
    return out


def red_forms():
    """Component equations, with no supplied graph catalogue."""
    forms = []
    for a in range(1, 11):
        for b in range(a, 11):
            for c in range(b, 11):
                left = 10 - a - b - c
                if left != 0 and left < 5:
                    continue
                es, nxt = [], 1
                for length in (a, b, c):
                    es.extend(zip([0] + list(range(nxt, nxt + length - 1)),
                                  range(nxt, nxt + length)))
                    nxt += length
                if left:
                    cyc = list(range(nxt, nxt + left))
                    es.extend(zip(cyc, cyc[1:] + cyc[:1]))
                name = f'Y:{a},{b},{c}' + (f'+C{left}' if left else '')
                forms.append((name, sum(edge(*e) for e in es)))
    for k in range(5, 11):
        for t in range(1, 12 - k):
            rem = 11 - k - t
            for density in (10, 11):
                if density == 10 and (rem < 3 or rem == 5):
                    continue
                if density == 11 and rem != 0 and rem < 5:
                    continue
                es = list(zip(range(k), list(range(1, k)) + [0]))
                es.extend(zip([0] + list(range(k, k + t - 1)), range(k, k + t)))
                tail = list(range(k + t, 11))
                es.extend(zip(tail, tail[1:]))
                if density == 11 and rem:
                    es.append((tail[-1], tail[0]))
                name = (f'L10:{k},{t},{rem}' if density == 10 else
                        f'L11:{k},{t}' + (f'+C{rem}' if rem else ''))
                forms.append((name, sum(edge(*e) for e in es)))
    return sorted(forms)


def cycle_covers(interior, allowed):
    """Unique least-vertex, least-direction decomposition into simple cycles."""
    if not interior:
        yield 0
        return
    v = (interior & -interior).bit_length() - 1
    rest = interior ^ (1 << v)

    def walk(current, unused, first, count, mask):
        if count >= 3 and allowed[current] >> v & 1 and first < current:
            for later in cycle_covers(unused, allowed):
                yield mask | edge(current, v) | later
        for w in vertices(allowed[current] & unused):
            yield from walk(w, unused ^ (1 << w), first, count + 1,
                            mask | edge(current, w))

    for w in vertices(allowed[v] & rest):
        yield from walk(w, rest ^ (1 << w), w, 2, edge(v, w))


def path_cycle_covers(endpoints, interior, allowed):
    """All max-degree-two graphs: pair endpoints by simple paths, then cycles."""
    if not endpoints:
        yield from cycle_covers(interior, allowed)
        return
    start = (endpoints & -endpoints).bit_length() - 1
    others = endpoints ^ (1 << start)

    def walk(current, unused, mask):
        for finish in vertices(allowed[current] & others):
            for later in path_cycle_covers(others ^ (1 << finish), unused, allowed):
                yield mask | edge(current, finish) | later
        for w in vertices(allowed[current] & unused):
            yield from walk(w, unused ^ (1 << w), mask | edge(current, w))

    yield from walk(start, interior, 0)


def blue_graphs(degrees, allowed):
    """Delete the unique trivalent vertex; enumerate path/cycle components."""
    root_candidates = [i for i, d in enumerate(degrees) if d == 3]
    require(len(root_candidates) == 1, 'expected exactly one D trivalent vertex')
    root = root_candidates[0]
    for neighborhood in combinations(tuple(vertices(allowed[root])), 3):
        endpoint_mask = interior_mask = initial = 0
        possible = True
        for i, d in enumerate(degrees):
            if i == root:
                continue
            residual = d - (i in neighborhood)
            if residual < 0 or residual > 2:
                possible = False
                break
            if residual == 1:
                endpoint_mask |= 1 << i
            elif residual == 2:
                interior_mask |= 1 << i
        if not possible:
            continue
        active = endpoint_mask | interior_mask
        if any((allowed[i] & active).bit_count() <
               (1 if endpoint_mask >> i & 1 else 2) for i in vertices(active)):
            continue
        for i in neighborhood:
            initial |= edge(root, i)
        for mask in path_cycle_covers(endpoint_mask, interior_mask, allowed):
            yield initial | mask


def literal_pages(red, blue, inside, signs=0):
    adj = [set() for _ in range(22)]

    def add(a, b):
        adj[a].add(b)
        adj[b].add(a)

    for i in range(11):
        if inside >> i & 1:
            add(2 * i, 2 * i + 1)
    for k, (i, j) in enumerate(PAIRS):
        if red >> k & 1:
            for s in (0, 1):
                for t in (0, 1):
                    add(2 * i + s, 2 * j + t)
        elif not blue >> k & 1:
            flip = signs >> k & 1
            for s in (0, 1):
                add(2 * i + s, 2 * j + (s ^ flip))
    comp = [set(range(22)) - adj[i] - {i} for i in range(22)]
    require(all(len(v) == 10 for v in adj), 'lift is not ten-regular')
    pages = []
    for k, (i, j) in enumerate(PAIRS):
        if red >> k & 1:
            kind, cap = 'R', 6
            val = sum(len(adj[2 * i] & adj[2 * j + t]) for t in (0, 1))
        elif blue >> k & 1:
            kind, cap = 'D', 12
            val = sum(len(comp[2 * i] & comp[2 * j + t]) for t in (0, 1))
        else:
            kind, cap = 'M', 9
            flip = signs >> k & 1
            val = (len(adj[2 * i] & adj[2 * j + flip]) +
                   len(comp[2 * i] & comp[2 * j + (1 ^ flip)]))
        pages.append((kind, val, cap))
    return pages


def square_pages(red, blue, inside):
    rr, dd = rows(red), rows(blue)
    out = []
    for k, (i, j) in enumerate(PAIRS):
        q = ((rr[i] & rr[j]).bit_count() + (dd[i] & dd[j]).bit_count() -
             (rr[i] & dd[j]).bit_count() - (dd[i] & rr[j]).bit_count())
        flags = (inside >> i & 1) + (inside >> j & 1)
        out.append(('R', 7 + q + flags, 6) if red >> k & 1 else
                   ('D', 11 + q - flags, 12) if blue >> k & 1 else
                   ('M', 9 + q, 9))
    return out


def obstruction(pages):
    for kind in ('R', 'D', 'M'):
        for k, (got_kind, val, cap) in enumerate(pages):
            if got_kind == kind and val > cap:
                return kind, k, val
    return None


def run():
    forms = red_forms()
    require(len(forms) == 24, 'red component count changed')
    profiles, records = [], []
    raw_total, literal_checks = 0, 0
    raw_failures = Counter()
    for name, red in forms:
        rr = rows(red)
        rd = [x.bit_count() for x in rr]
        require(rd.count(3) == 1 and min(rd) == 1, 'bad red shape')
        root = rd.index(3)
        leaves = [i for i, d in enumerate(rd) if d == 1]
        eligible = sum(1 << i for i in leaves if rr[i] >> root & 1)
        siblings = [edge(l, m) for l, m in combinations(leaves, 2)
                    if rr[l] == rr[m]]
        clauses = []
        for i, j in PAIRS:
            if red & edge(i, j):
                clauses.append(sum(edge(v, j) for v in vertices(rr[i] & ~(1 << j))) |
                               sum(edge(i, v) for v in vertices(rr[j] & ~(1 << i))))
        allowed = [ALL ^ (1 << i) ^ rr[i] for i in range(11)]
        for l in leaves:
            parent = next(vertices(rr[l]))
            allowed[l] &= rr[parent] & ~(1 << l)
        for i in range(11):
            for j in range(11):
                if not allowed[j] >> i & 1:
                    allowed[i] &= ~(1 << j)
        for inside in range(1 << 11):
            if inside & ~eligible or inside.bit_count() % 2:
                continue
            case = f'{name}:F{inside}'
            degrees = [d + (inside >> i & 1) for i, d in enumerate(rd)]
            raw = filtered = 0
            failures, seen = Counter(), set()
            for blue in blue_graphs(degrees, allowed):
                require(blue not in seen, 'duplicate component enumeration')
                seen.add(blue)
                raw += 1
                require(not blue & red, 'overlapping uniform colors')
                require([v.bit_count() for v in rows(blue)] == degrees, 'wrong D degrees')
                full_pages = square_pages(red, blue, inside)
                raw_failure = obstruction(full_pages)
                require(raw_failure is not None, f'unfiltered survivor in {case}')
                raw_failures[raw_failure[0]] += 1
                if any(not blue & e for e in siblings) or any(not blue & c for c in clauses):
                    continue
                filtered += 1
                literal = literal_pages(red, blue, inside)
                require(literal == full_pages, 'page formula disagreement')
                alternating = sum(1 << k for k in range(0, 55, 2))
                require(literal_pages(red, blue, inside, alternating) == full_pages,
                        'alternating signing formula disagreement')
                literal_checks += 2
                fail = obstruction(literal)
                require(fail is not None, f'survivor in {case}')
                failures[fail[0]] += 1
                records.append({'case': case, 'Dmask': blue, 'failure': list(fail)})
            raw_total += raw
            profiles.append({'case': case, 'unfiltered': raw, 'D_completions': filtered,
                             'first_failure_counts': dict(sorted(failures.items()))})
    records.sort(key=lambda r: (r['case'], r['Dmask']))
    canonical = ''.join(json.dumps(r, sort_keys=True, separators=(',', ':')) + '\n'
                        for r in records).encode()
    author_words = [[r['case'], r['Dmask'],
                     [r['failure'][0], *PAIRS[r['failure'][1]], r['failure'][2]]]
                    for r in records]
    author_encoded = ''.join(json.dumps(w, separators=(',', ':')) + '\n'
                             for w in author_words).encode()
    counts = Counter(r['failure'][0] for r in records)
    summary = {'red_forms': len(forms), 'R_inside_cases': len(profiles),
               'unfiltered_degree_graphs': raw_total, 'D_completions': len(records),
               'unfiltered_first_failure_counts': dict(sorted(raw_failures.items())),
               'survivors': 0, 'first_failure_counts': dict(sorted(counts.items())),
               'literal_formula_checks': literal_checks,
               'r10': sum(p['D_completions'] for p in profiles if not p['case'].startswith('L11')),
               'r11': sum(p['D_completions'] for p in profiles if p['case'].startswith('L11')),
               'records_sha256': sha256(canonical).hexdigest(),
               'author_encoding_records_sha256': sha256(author_encoded).hexdigest(),
               'profiles': profiles}
    return summary, records


def small_controls():
    # Direct component enumeration of every simple graph on five labelled vertices,
    # including isolated vertices: exhaustive degree<=2 reference, independent input.
    ps = list(combinations(range(5), 2))
    expected = {}
    trivalent_expected = {}
    for word in range(1 << len(ps)):
        mask = sum(edge(*p) for k, p in enumerate(ps) if word >> k & 1)
        ds = tuple(r.bit_count() for r in rows(mask)[:5])
        if max(ds) <= 2:
            expected.setdefault(ds, set()).add(mask)
        if max(ds) <= 3 and ds.count(3) == 1:
            trivalent_expected.setdefault(ds, set()).add(mask)
    allowed = [((1 << 5) - 1) & ~(1 << i) for i in range(11)]
    for ds in product(range(3), repeat=5):
        ref = expected.get(ds, set())
        endpoints = sum(1 << i for i, d in enumerate(ds) if d == 1)
        interior = sum(1 << i for i, d in enumerate(ds) if d == 2)
        actual = list(path_cycle_covers(endpoints, interior, allowed))
        require(len(actual) == len(set(actual)), 'control duplicate')
        require(set(actual) == ref, 'control missing/extra graph')
    trivalent_domains = 0
    for root in range(5):
        for small in product(range(3), repeat=4):
            ds = tuple(list(small[:root]) + [3] + list(small[root:]))
            actual = list(blue_graphs(list(ds) + [0] * 6, allowed))
            ref = trivalent_expected.get(ds, set())
            require(len(actual) == len(set(actual)) and set(actual) == ref,
                    'deleted-trivalent-vertex control mismatch')
            trivalent_domains += 1
    forbidden_tests = 0
    four_pairs = list(combinations(range(4), 2))
    for forbidden in range(1 << len(four_pairs)):
        permitted = [((1 << 4) - 1) & ~(1 << i) for i in range(11)]
        for k, (i, j) in enumerate(four_pairs):
            if forbidden >> k & 1:
                permitted[i] &= ~(1 << j)
                permitted[j] &= ~(1 << i)
        for ds in product(range(3), repeat=4):
            ref = set()
            for word in range(1 << len(four_pairs)):
                if word & forbidden:
                    continue
                mask = sum(edge(*p) for k, p in enumerate(four_pairs) if word >> k & 1)
                if tuple(r.bit_count() for r in rows(mask)[:4]) == ds:
                    ref.add(mask)
            endpoints = sum(1 << i for i, d in enumerate(ds) if d == 1)
            interior = sum(1 << i for i, d in enumerate(ds) if d == 2)
            actual = list(path_cycle_covers(endpoints, interior, permitted))
            require(len(actual) == len(set(actual)) and set(actual) == ref,
                    'forbidden-edge component control mismatch')
            forbidden_tests += 1
    return {'five_vertex_graphs_examined': 1024, 'degree_vectors_tested': 243,
            'realized_degree_vectors': len(expected), 'forbidden_edge_degree_domains': forbidden_tests,
            'deleted_trivalent_degree_domains': trivalent_domains}


def four_trivalent_profile():
    """Validation only: analytic leaf-capacity proof is the mathematical premise."""
    tested = complete = 0
    for mate in (1, 2, 3):
        other = sorted(set(range(1, 4)) - {mate})
        diagonals = {(0, mate), tuple(other)}
        core = set(combinations(range(4), 2)) - diagonals
        red = sum(edge(*p) for p in core) | sum(edge(i, 5+i) for i in range(4))
        red |= edge(4, 9) | edge(4, 10)
        rr = rows(red)
        target = [3]*4 + [2] + [1]*6
        core_pairs = sorted(diagonals | {(i, 4) for i in range(4)})
        choices = [tuple(vertices(rr[i] & ~(1 << (5+i)))) for i in range(4)]
        for neighbors in product(*choices):
            fixed = edge(9, 10) | sum(edge(5+i, neighbors[i]) for i in range(4))
            for word in range(1 << len(core_pairs)):
                blue = fixed | sum(edge(*p) for k, p in enumerate(core_pairs) if word >> k & 1)
                tested += 1
                if [r.bit_count() for r in rows(blue)] == target:
                    complete += 1
    require(complete == 0, 'four-trivalent profile degree completion found')
    return {'red_core_C4_labelings': 3, 'leaf_choice_core_words': tested,
            'degree_complete_D_graphs': complete, 'computation_is_validation_only': True}


def sign_controls():
    blocks = [([[1, 1], [1, 1]], 1), ([[0, 0], [0, 0]], -1),
              ([[1, 0], [0, 1]], 0), ([[0, 1], [1, 0]], 0)]
    tested = 0
    for (a, wa), (b, wb) in product(blocks, repeat=2):
        red = sum(a[0][s] * b[t][s] for s in range(2) for t in range(2))
        blue = sum((1-a[0][s]) * (1-b[t][s]) for s in range(2) for t in range(2))
        require(red == (1+wa)*(1+wb), 'local uniform red identity')
        require(blue == (1-wa)*(1-wb), 'local uniform blue identity')
        tested += 2
        for flip in (0, 1):
            mixed = sum(a[0][s] * b[flip][s] +
                        (1-a[0][s]) * (1-b[1-flip][s]) for s in range(2))
            require(mixed == 1+wa*wb, 'local matching identity')
            tested += 1
    # With two red siblings, each outside y has q_ly=W_cy-W_xy.
    # Exhaust every remaining local pair of block types; a D edge xy outside D_c
    # gives a strict matching obstruction. This is validation of the written proof.
    for wc, wx in product((-1, 0, 1), repeat=2):
        if wx == -1 and wc != -1:
            require(wc-wx > 0, 'sibling signed-row domination control')
    return {'outside_orbit_spine_identities': tested, 'sibling_row_words': 9}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--author-fixture', type=Path)
    parser.add_argument('--author-records', type=Path)
    parser.add_argument('--write-records', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    controls = small_controls()
    result, records = run()
    result['component_controls'] = controls
    result['sign_controls'] = sign_controls()
    result['four_trivalent_profile_control'] = four_trivalent_profile()
    comparisons = []
    if args.author_fixture:
        fixture = json.loads(args.author_fixture.read_text())['census']
        author = {p['case']: (p['D_completions'], p['first_failure_counts']) for p in fixture['profiles']}
        ours = {p['case']: (p['D_completions'], p['first_failure_counts']) for p in result['profiles']}
        require(ours == author, 'author per-case fixture mismatch')
        comparisons.append('all author per-case counts and first failures')
    if args.author_records:
        author = [json.loads(line) for line in args.author_records.read_text().splitlines()]
        ours = [[r['case'], r['Dmask'],
                 [r['failure'][0], *PAIRS[r['failure'][1]], r['failure'][2]]]
                for r in records]
        require(ours == author, 'entry-level author records mismatch')
        comparisons.append('all 2428 author records entry by entry')
    if args.expected:
        expected = json.loads(args.expected.read_text())
        require(result == expected, 'expected summary mismatch')
    if args.write_records:
        args.write_records.write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({**{k: v for k, v in result.items() if k != 'profiles'},
                      'external_comparisons': comparisons,
                      'python': platform.python_version(), 'seconds': time.monotonic() - started},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
