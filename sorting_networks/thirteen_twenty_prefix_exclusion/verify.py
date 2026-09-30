"""Independent scalar-rank, inverse-fiber and DFS checker.

six-sorting-1 researcher. Imports no generator or comparator code. This
independence is algorithmic, not a claim of external review/formalization.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(13), 2))
MARKERS = GATES


def sha(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def execute(values, gates, high_markers=False):
    values = list(values)
    removed = 0
    for lo, hi in gates:
        assert 0 <= lo < hi < len(values)
        if high_markers and (values[lo] >= 11 or values[hi] >= 11):
            removed += 1
        if values[hi] < values[lo]:
            values[lo], values[hi] = values[hi], values[lo]
    return values, removed


def marker_row(pair):
    remaining = iter(range(11))
    result = [next(remaining) if i not in pair else 11 + pair.index(i) for i in range(13)]
    assert sorted(result) == list(range(13))
    return result


def marker_positions(values):
    return tuple(i for i, value in enumerate(values) if value >= 11)


def original_profile(word):
    result = {}
    for pair in MARKERS:
        out, deletions = execute(marker_row(pair), word, True)
        pair_out = marker_positions(out)
        result[pair_out] = max(result.get(pair_out, -1), deletions)
    return tuple(sorted(result.items()))


def inverse_tables():
    result = {}
    anchor_checks = 0
    for gate in GATES:
        fibers = {}
        forward = {}
        for pair in MARKERS:
            out, charged = execute(marker_row(pair), [gate], True)
            dest = marker_positions(out)
            fibers.setdefault(dest, []).append((pair, charged))
            forward[pair] = (dest, charged)
        for pre in fibers.values():
            assert len(pre) <= 2
            if len(pre) == 2:
                assert all(charged == 1 for pair, charged in pre)
        for port in range(13):
            onehot = [int(i == port) for i in range(13)]
            out, unused = execute(onehot, [gate])
            dest_port = out.index(1)
            pre = [pair for pair in MARKERS if port in pair]
            if port in gate:
                dests = [forward[pair][0] for pair in pre]
                assert len(set(dests)) == len(pre)
                assert all(dest_port in forward[pair][0] and forward[pair][1] == 1 for pair in pre)
            else:
                assert dest_port == port
                assert all((port in pair) == (port in dest) for pair, (dest, charged) in forward.items())
            anchor_checks += 1
        result[gate] = fibers
    assert anchor_checks == 1014
    return result


def encode(f):
    return sorted([[sum(2 ** p for p in pair), depth] for pair, depth in f])


def total(f):
    return sum(2 ** depth for pair, depth in f)


def anchored(f, port):
    return sum(2 ** depth for pair, depth in f if port in pair)


def route_cap(anchor, ceiling):
    result = -1
    while anchor * 2 ** (result + 1) <= ceiling:
        result += 1
    return result


def check_images(fixture):
    p20 = fixture['prefix20']
    assert len(p20) == 20 and p20[-1] == [8, 11]
    q20 = p20[:-1] + [[10, 12]]
    minimum = fixture['minimum_word']
    c25 = fixture['known25_control']
    zcontrol = fixture['Z12_known23_control']
    bcontrol = fixture['B11_known23_control']
    assert len(c25) == 25 and len(zcontrol) == len(bcontrol) == 23
    assert c25[0] == [10, 12]
    qcontrol = [[8, 11]] + c25[1:]
    lifted_z = [[a + 1, b + 1] for a, b in zcontrol]
    lifted_b = [[a + 1, b + 1] for a, b in bcontrol]
    sets = {name: set() for name in ['P19', 'P20', 'Z12', 'Q20', 'B11']}
    for x in range(8192):
        values = [(x // 2 ** i) % 2 for i in range(13)]
        v19, _ = execute(values, p20[:-1])
        v20, _ = execute(values, p20)
        q, _ = execute(values, q20)
        z, _ = execute(v20, minimum)
        b, _ = execute(q, minimum)
        assert z[0] == min(values)
        assert q[12] == b[12] == max(values) and b[0] == min(values)
        assert execute(v20, c25)[0] == sorted(values)
        assert execute(q, qcontrol)[0] == sorted(values)
        assert execute(values, p20 + minimum + lifted_z)[0] == sorted(values)
        assert execute(values, q20 + minimum + lifted_b)[0] == sorted(values)
        assert execute(z[1:], zcontrol)[0] == sorted(z[1:])
        assert execute(b[1:12], bcontrol)[0] == sorted(b[1:12])
        for name, row in [('P19', v19), ('P20', v20), ('Z12', z[1:]), ('Q20', q[:12]), ('B11', b[1:12])]:
            sets[name].add(sum(value * 2 ** i for i, value in enumerate(row)))
    for name, control, n in [('Z12', zcontrol, 12), ('B11', bcontrol, 11)]:
        for x in sets[name]:
            row = [(x // 2 ** i) % 2 for i in range(n)]
            assert execute(row, control)[0] == sorted(row)
    return {name: {'states': sorted(rows), 'count': len(rows), 'sha256': sha(sorted(rows))} for name, rows in sets.items()}


def audit(fixture, expected):
    tables = inverse_tables()
    nongates = tuple(g for g in GATES if set(g).isdisjoint({10, 12}))
    transitions_checked = 0

    def transport(f, gate):
        nonlocal transitions_checked
        prior = dict(f)
        output = []
        for dest, predecessors in tables[gate].items():
            choices = [prior[pair] + charged for pair, charged in predecessors if pair in prior]
            if choices:
                output.append((dest, max(choices)))
        result = tuple(sorted(output))
        assert total(result) >= total(f)
        transitions_checked += 1
        return result

    def permitted(f, last_mass):
        return total(f) <= 512 and anchored(f, 10) <= 256 and anchored(f, 12) <= last_mass

    def saturate(initial, last_mass):
        todo = [f for f in initial if permitted(f, last_mass)]
        reached = set()
        while todo:
            current = todo.pop()
            if current in reached:
                continue
            reached.add(current)
            for gate in reversed(nongates):
                dest = transport(current, gate)
                if permitted(dest, last_mass) and dest not in reached:
                    todo.append(dest)
        # Explicit closure check; every permissible successor is retained.
        for current in reached:
            for gate in nongates:
                dest = transport(current, gate)
                assert not permitted(dest, last_mass) or dest in reached
        return sorted(reached, key=encode)

    f19 = original_profile(fixture['prefix20'][:-1])
    f20 = original_profile(fixture['prefix20'])
    assert fixture['full_budget'] - fixture['S11'] == 9
    assert fixture['S13_lower'] == 44
    ceiling = 2 ** (fixture['full_budget'] - fixture['S11'])
    masses19 = [anchored(f19, p) for p in (10, 12)]
    masses20 = [anchored(f20, p) for p in (10, 12)]
    for word in [fixture['prefix20'][:-1], fixture['prefix20']]:
        ports = set()
        for p in range(13):
            row = [int(i == p) for i in range(13)]
            ports.add(execute(row, word)[0].index(1))
        assert ports == {10, 12}
    pre = saturate([f19], 128)
    cases = []
    for partner in list(range(10)) + [11]:
        unary = (partner, 12)
        seeds = [transport(f, unary) for f in pre]
        post = saturate(seeds, 256)
        terminals = [transport(f, (10, 12)) for f in post]
        assert all(total(f) > ceiling for f in terminals)
        cases.append({'unary': list(unary), 'accepted_seed_count': sum(permitted(f, 256) for f in seeds),
                      'post_profiles': [encode(f) for f in post],
                      'terminal_profiles': [encode(f) for f in terminals],
                      'terminal_weights': [total(f) for f in terminals], 'survivor_count': 0})
    result = {'ceiling': ceiling, 'P19_profile': encode(f19), 'P20_profile': encode(f20),
              'P19_anchor_masses_10_12': masses19, 'P20_anchor_masses_10_12': masses20,
              'P19_route_caps_10_12': [route_cap(m, ceiling) for m in masses19],
              'P20_route_caps_10_12': [route_cap(m, ceiling) for m in masses20],
              'nongate_count': len(nongates), 'pre_profiles': [encode(f) for f in pre],
              'unary_cases': cases, 'images': check_images(fixture),
              'original_Boolean_inputs': 8192,
              'conclusion': {'P20_minimum_suffix': 25, 'Z12_minimum': 23,
                             'P19_full44_maximum_kernel': [[10, 12]],
                             'Q20_interval': [24, 25], 'B11_interval': [22, 23],
                             'global_S13_interval': [44, 45]}}
    assert result == expected, 'Entry-level certificate mismatch'
    return result, transitions_checked


def main():
    if sys.flags.optimize:
        raise RuntimeError('Run without -O: assertions are exact checks.')
    fixture = json.loads((HERE / 'fixture.json').read_text())
    expected = json.loads((HERE / 'certificate.json').read_text())
    result, transitions = audit(fixture, expected)
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'status': 'all_exact_checks_passed', 'algorithm': 'scalar_rank_inverse_fibers_DFS',
                      'certificate_sha256': hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest(),
                      'original_Boolean_inputs': 8192, 'marker_pairs_per_prefix': 78,
                      'local_marker_transition_checks': 6084, 'local_anchor_checks': 1014,
                      'profile_transition_checks': transitions,
                      'image_counts': {k: v['count'] for k, v in result['images'].items()},
                      'pre_profile_count': len(result['pre_profiles']),
                      'post_profile_counts': [len(c['post_profiles']) for c in result['unary_cases']],
                      'conclusion': result['conclusion']}, indent=2))


if __name__ == '__main__':
    main()
