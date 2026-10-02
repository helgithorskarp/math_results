"""six-reviewer-4: direct positive-witness verifier; stdlib, no target imports."""
import csv
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

P, PERIOD = 103, 618
SIGMA = (0, 0, 0, 1, 1, 1)
STATES = tuple((t, a, b) for t in range(2, P) for a in (0, 1) for b in (0, 1))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def legendre_bit(x):
    """Gauss lemma, rather than Euler's criterion or a square-set oracle."""
    x %= P
    require(x != 0, 'undefined character at root')
    return sum((i * x) % P > P // 2 for i in range(1, (P + 1) // 2)) % 2


BITS = tuple(None if x == 0 else legendre_bit(x) for x in range(P))


def color(state, x, y=0):
    t, a, b = state
    require(x % P not in (0, 1, t), 'root point')
    inputs = (BITS[x % P], BITS[(x - 1) % P] ^ a, BITS[(x - t) % P] ^ b)
    return sorted(inputs)[1] ^ SIGMA[y % 6]


def relabel(state, order):
    t, a, b = state
    roots, signs = (0, 1, t), (0, a, b)
    i, j, k = order
    offset = roots[i]
    slope = (roots[j] - offset) % P
    new = (((roots[k] - offset) * pow(slope, -1, P)) % P,
           signs[j] ^ signs[i], signs[k] ^ signs[i])
    return new, slope, offset, BITS[slope] ^ signs[i]


def orbits():
    """Connected components under two generators, not six-map canonicalization."""
    todo, answer = set(STATES), []
    while todo:
        start = min(todo)
        found, frontier = {start}, [start]
        while frontier:
            z = frontier.pop()
            for order in ((1, 0, 2), (1, 2, 0)):
                w = relabel(z, order)[0]
                if w not in found:
                    found.add(w)
                    frontier.append(w)
        require(found <= todo, 'overlapping components')
        todo -= found
        answer.append(tuple(sorted(found)))
    return tuple(sorted(answer))


def crt(field, phase):
    return (field + P * ((phase - field) % 6)) % PERIOD


def normalize_ap(start, step):
    require(0 <= start < PERIOD and 0 < step < PERIOD, 'AP coordinate range')
    if step > PERIOD // 2:
        start, step = (start + 6 * step) % PERIOD, PERIOD - step
    return start or PERIOD, step


def check_pack(state, pack):
    require(len(pack) >= 9, 'short pack')
    all_columns, transcript = set(), []
    for start, step in pack:
        require(0 <= start < PERIOD and 0 < step < PERIOD, 'AP coordinate range')
        points = tuple((start + i * step) % PERIOD for i in range(7))
        columns = {x % P for x in points}
        require(len(columns) == 7, 'repeated field column')
        require(not columns.intersection((0, 1, state[0])), 'root support')
        require(not columns.intersection(all_columns), 'overlapping supports')
        colors = tuple(color(state, x % P, x % 6) for x in points)
        require(len(set(colors)) == 1, 'mixed AP')
        all_columns.update(columns)
        first, d = normalize_ap(start, step)
        require(d <= 308, 'nonzero field step excludes309')
        lifted = tuple(first + i * d for i in range(7))
        require(lifted[-1] <= 2466, 'uniform integer lift')
        require({x % P for x in lifted} == columns, 'reversal support')
        transcript.append({'start': start, 'step': step, 'points': points,
                           'columns': sorted(columns), 'color': colors[0],
                           'integer_lift': lifted})
    return transcript


def load_csv(path):
    with Path(path).open(newline='') as f:
        rows = list(csv.DictReader(f))
    require(rows and set(rows[0]) == {'t', 'a', 'b', 'slot', 'start', 'step'}, 'CSV schema')
    groups, slots = {}, set()
    for row in rows:
        require(all(v is not None and v.lstrip('-').isdigit() for v in row.values()), 'integer CSV')
        t, a, b, slot, start, step = (int(row[k]) for k in ('t', 'a', 'b', 'slot', 'start', 'step'))
        z = t, a, b
        require(z in STATES and slot >= 0 and (z, slot) not in slots, 'CSV state/slot')
        slots.add((z, slot))
        groups.setdefault(z, []).append((slot, start, step))
    for z, entries in groups.items():
        require(sorted(x[0] for x in entries) == list(range(len(entries))), 'missing slot')
        groups[z] = tuple((x, d) for _, x, d in sorted(entries))
    return groups


def audit(groups):
    components = orbits()
    reps = {o[0] for o in components}
    require(set(groups) == reps, 'complete representatives')
    histogram = dict(sorted(Counter(map(len, components)).items()))
    require(histogram == {2: 1, 3: 2, 6: 66}, 'orbit histogram')
    square = {(i * i) % P for i in range(1, P)}
    require(all(BITS[x] == int(x not in square) for x in range(1, P)), 'Gauss/square agreement')
    multiply = 0
    for x in range(1, P):
        for y in range(1, P):
            require(BITS[(x * y) % P] == (BITS[x] ^ BITS[y]), 'character multiplication')
            multiply += 1
    permutations = tuple(itertools.permutations(range(3)))
    identities = compositions = 0
    fixed_counts = []
    for order in permutations:
        fixed_counts.append(sum(relabel(z, order)[0] == z for z in STATES))
    for z in STATES:
        roots = {0, 1, z[0]}
        for order in permutations:
            w, s, a, exchange = relabel(z, order)
            require({(s * x + a) % P for x in (0, 1, w[0])} == roots, 'root bijection')
            for x in range(P):
                if x not in (0, 1, w[0]):
                    require(color(z, s * x + a) == (color(w, x) ^ exchange), 'field transport')
                    identities += 1
            for next_order in permutations:
                composite = tuple(order[i] for i in next_order)
                require(relabel(w, next_order)[0] == relabel(z, composite)[0], 'group composition')
                compositions += 1
    representative_record = {','.join(map(str, z)): check_pack(z, groups[z]) for z in sorted(reps)}
    whole, exchanges = {}, Counter()
    for component in components:
        rep = component[0]
        for z in component:
            maps = [relabel(z, order) for order in permutations if relabel(z, order)[0] == rep]
            require(bool(maps), 'missing transport')
            _, s, a, exchange = maps[0]
            alpha, beta = crt(s, 1), crt(a, 0)
            require(pow(alpha, -1, PERIOD) * alpha % PERIOD == 1, 'CRT unit')
            pack = tuple(((alpha * x + beta) % PERIOD, alpha * d % PERIOD) for x, d in groups[rep])
            checked = check_pack(z, pack)
            for j, ap in enumerate(checked):
                require(ap['color'] == (representative_record[','.join(map(str, rep))][j]['color'] ^ exchange), 'color exchange')
            whole[','.join(map(str, z))] = checked
            exchanges[exchange] += 1
    phase_witnesses = []
    legal_rows = {tuple(SIGMA[(y + c) % 6] for y in range(6)) for c in range(6)}
    zero_field_cases = 0
    for row in sorted(legal_rows):
        for step in (103, 206, 309, 412, 515):
            for y in range(6):
                require(len({row[(y + i * step) % 6] for i in range(7)}) == 2,
                        'legal phase zero-field AP must be mixed')
                zero_field_cases += 1
    for row in itertools.product((0, 1), repeat=6):
        if row in legal_rows:
            continue
        candidates = [(y, 309) for y in range(6) if row[y] == row[(y + 3) % 6]]
        if not candidates:
            candidates = [(y, 206) for y in range(6) if len({row[(y + 2 * i) % 6] for i in range(3)}) == 1]
        require(candidates, 'illegal phase witness')
        y, step = candidates[0]
        for field in range(P):
            residues = [(crt(field, y) + i * step) % PERIOD for i in range(PERIOD // step)]
            start = min(x or PERIOD for x in residues)
            require(start <= step and start + 6 * step <= 2163, 'short singleton lift')
            require(len({row[(start + i * step) % 6] for i in range(7)}) == 1, 'singleton monochromatic')
        phase_witnesses.append((row, y, step))
    repeated = 0
    for roots in ((0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, 0)):
        for signs in itertools.product((0, 1), repeat=3):
            for x in range(P):
                if x in roots:
                    continue
                value = sorted(BITS[(x - r) % P] ^ b for r, b in zip(roots, signs))[1]
                if len(set(roots)) == 1:
                    oracle = BITS[x] ^ sorted(signs)[1]
                else:
                    common = next(r for r in roots if roots.count(r) == 2)
                    indices = [i for i, r in enumerate(roots) if r == common]
                    other = next(i for i, r in enumerate(roots) if r != common)
                    index = indices[0] if signs[indices[0]] == signs[indices[1]] else other
                    oracle = BITS[(x - roots[index]) % P] ^ signs[index]
                require(value == oracle, 'repeated-root reduction')
                repeated += 1
    canonical = lambda data: json.dumps(data, sort_keys=True, separators=(',', ':')).encode()
    summary = {'status': 'INDEPENDENT_COMPLETE_MAJORITY_AUDIT', 'states': len(STATES),
               'orbits': len(components), 'orbit_histogram': histogram,
               'fixed_counts': fixed_counts, 'regular_field_identities': identities,
               'group_compositions': compositions, 'multiplicativity_inputs': multiply,
               'pack_size_minimum': min(map(len, groups.values())),
               'representative_APs': sum(map(len, groups.values())),
               'transported_APs': sum(len(v) for v in whole.values()),
               'color_exchanges': dict(exchanges), 'illegal_rows': len(phase_witnesses),
               'legal_zero_field_cases': zero_field_cases,
               'repeated_root_regular_inputs': repeated,
               'uniform_distinct_root_interval': 2466, 'illegal_phase_interval': 2163,
               'representative_sha256': hashlib.sha256(canonical(representative_record)).hexdigest(),
               'whole_transport_sha256': hashlib.sha256(canonical(whole)).hexdigest()}
    return summary, {'representatives': representative_record, 'all_states': whole,
                     'phase_witnesses': phase_witnesses, 'summary': summary}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    summary, record = audit(load_csv(args.certificate))
    if args.record:
        args.record.write_text(json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps(summary, sort_keys=True))
