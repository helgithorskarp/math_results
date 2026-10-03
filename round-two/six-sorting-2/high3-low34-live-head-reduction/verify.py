"""Separate scalar original-domain and universal forest certificate replay.

No generator, packed module, old negative corpus or private input is used.
The ordinary arbitrary-word and component bridges are written in PROOF.md.
"""
import argparse
from collections import Counter
import copy
from itertools import combinations
import json
from pathlib import Path
import resource
import time

from numeric import bool_word, digest, follow, fresh_domain, need

ROOT = Path(__file__).resolve().parent
DEAD = (4, 5, 6, 7, 9, 10)
PREFIX_SHA = '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4'


def split_word(word, q, component):
    target = ([i for i, gate in enumerate(word) if set(gate) <= component] +
              [i for i, gate in enumerate(word) if not set(gate) <= component])
    permutation = list(range(len(word)))
    for slot, original_index in enumerate(target):
        cursor = permutation.index(original_index)
        while cursor > slot:
            left, right = word[permutation[cursor - 1]], word[permutation[cursor]]
            need(set(left).isdisjoint(right), 'non-disjoint component swap')
            permutation[cursor - 1], permutation[cursor] = permutation[cursor], permutation[cursor - 1]
            cursor -= 1
    moved = [word[i] for i in permutation]
    live = set(DEAD)
    for a, b in moved:
        need(a in live and b in live and a < b, 'reordered binary is not legal')
        live.remove(a)
    need(q in live and all(set(g).isdisjoint({1, 2, 3, 8, q, min(8, q)}) for g in moved[2:]),
         'selected head/tail intersects displaced events')
    need({1, 2, 3, 8, q, min(8, q)}.isdisjoint(set(DEAD) - live),
         'selected head/tail intersects arbitrary final freed preparation')
    local = [[DEAD.index(a), DEAD.index(b)] for a, b in word]
    reordered = [[DEAD.index(a), DEAD.index(b)] for a, b in moved]
    need([bool_word(x, local) for x in range(64)] == [bool_word(x, reordered) for x in range(64)],
         'entire ordered six-port forest function differs')
    return moved


def scalar_forest(word, originals):
    histories = [[r[3], r[4]] for r in originals]
    leaf_routes = {q: q for q in DEAD}
    stages = []
    for a, b in word:
        current_live = set(leaf_routes.values())
        need(a < b and a in current_live and b in current_live, 'invalid live-root binary')
        for r in histories:
            tags, d = r
            if tags & ((1 << a) | (1 << b)):
                d += 1
            if tags >> a & 1 and not tags >> b & 1:
                tags ^= (1 << a) | (1 << b)
            r[:] = [tags, d]
        for leaf, root in leaf_routes.items():
            if root == a:
                leaf_routes[leaf] = b
        costs = {}
        for tags, d in histories:
            secondary = tags & ~6144
            need(tags & 6144 == 6144 and secondary.bit_count() == 1, 'actual third-HIGH tags changed')
            root = secondary.bit_length() - 1
            costs[root] = max(costs.get(root, -1), d)
        need(set(costs) == set(leaf_routes.values()), 'component/original tag partition differs')
        stages.append([[[q, d] for q, d in sorted(costs.items())], sum(1 << d for d in costs.values())])
    parts = {q: {leaf for leaf, root in leaf_routes.items() if root == q} for q in sorted(costs)}
    heads = []
    for q, leaves in parts.items():
        if any(stage[1] > 32768 for stage in stages):
            kind, detail = 'ORDINARY_PREPARATION_MASS', {}
        elif len(word) == 2:
            kind, detail = 'PUBLIC_TWO_BINARY_EXCLUSION', {}
        else:
            r = len(leaves) - 1
            inside = [g for g in word if all(p in leaves for p in g)]
            need(r == len(inside), 'tree leaf/event count is not exact')
            if r <= 2:
                moved = split_word(word, q, leaves)
                kind, detail = 'COMMUTATION_TO_PUBLIC_TWO_BINARY', {
                    'component_binary_count': r, 'reordered_forest': moved,
                    'two_binary_prefix': moved[:2], 'displaced_binary_suffix': moved[2:]}
            elif stages[-1][1] + 2 ** costs[q] > 32768:
                kind, detail = 'ORDINARY_HEAD_MASS', {
                    'exponent': costs[q], 'head_mass': stages[-1][1] + 2 ** costs[q]}
            else:
                need(r == 3 and leaves == {4, 5, 6, 9} and q == 9 and costs[q] == 13,
                     'surviving live component is not the four-eleven exception')
                need(set(inside[0]).isdisjoint(inside[1]) and
                     inside[2] == sorted([max(inside[0]), max(inside[1])]), 'exception tree is not balanced')
                kind, detail = 'TIGHT_ORIGINAL_BALANCED_HEAD_IDENTITY', {
                    'component_binary_count': 3, 'leaves': sorted(leaves), 'original_masks': [0, 3],
                    'head': [8, 9], 'original_D_at_Q': 9, 'additional_head_R': 1,
                    'imported_size': 35, 'forced_size': 45}
        heads.append({'partner': q, 'kind': kind, **detail})
    return {'binary_count': len(word), 'word': word, 'stages': stages,
            'components': [[q, sorted(s)] for q, s in parts.items()], 'live_heads': heads}


def reconstruct(fixture):
    prefix = fixture['literal_prefix']
    need(fixture['schema'] == 'HIGH3_LOW34_ZERO_SINGLETON_LIVE_HEAD_REDUCTION_V1' and
         fixture['n'] == 13 and fixture['size_budget'] == 44 and fixture['dead_ports'] == list(DEAD) and
         fixture['binary_counts'] == [2, 3, 4, 5] and digest(prefix) == PREFIX_SHA and len(prefix) == 28,
         'literal proof interface differs')
    need(fixture['imported_size_floors'] == {'10': 29, '11': 35, '12': 39}, 'imported primary floors changed')
    families, ground = {}, {}
    for name, count, low in (('2L', 2, True), ('2H', 2, False), ('3H', 3, False)):
        records, envelope = [], {}
        for ports in combinations(range(13), count):
            mask = sum(1 << q for q in ports)
            lo, hi = (mask, 0) if low else (0, mask)
            record, rows = follow(fresh_domain(lo, hi), prefix, 0)
            records.append(record)
            tag = tuple(record[2:4])
            envelope[tag] = max(envelope.get(tag, -1), record[4])
        families[name] = records
        ground[name] = [[*tag, d] for tag, d in sorted(envelope.items())]
    initial = [[q, max(r[4] for r in families['3H'] if r[3] == 6144 | (1 << q))] for q in DEAD]
    need(initial == fixture['initial_high3_exponents'] and ground['2H'] == [[0, 6144, 9]] and
         ground['2L'] == [[3, 0, 7], [5, 0, 7], [9, 0, 7], [257, 0, 6]], 'ground saturation differs')
    original, rows = follow(fresh_domain(0, 3), prefix, 0)
    need(original == [0, 3, 0, 6144, 9, 0, 0] and len(rows) == 2048, 'tight original cube differs')
    relation = [[v[8], max(v[q] for q in (4, 5, 6, 9))] for v in rows]
    need(all(a <= b for a, b in relation), 'entire2048-row head identity fails')
    # Directly replay every labelled balanced tree and the claimed identity
    # as actual original numerical gates, including absolute R positions.
    pairings = (((4, 5), (6, 9)), ((4, 6), (5, 9)), ((4, 9), (5, 6)))
    identity_checks = []
    for x, y in pairings:
        for first, second in ((x, y), (y, x)):
            binary = [list(first), list(second), sorted([max(x), max(y)])]
            record, after = follow((original, rows), binary + [[8, 9]], 28)
            need(record == [0, 3, 0, 6144, 9, 1, 1 << 31], 'balanced-head D/R/position replay fails')
            need(record[4] + record[5] + 35 > 44, 'actual balanced-head witness insufficient')
            identity_checks.append([binary, record, digest(after)])
    # Independent iterative construction retains every word in each layer.
    # No cost pruning is used to generate the complete labelled universe.
    layer = [([], set(DEAD))]
    forests, counts, reasons = [], {}, Counter()
    for j in range(1, 6):
        nxt = []
        for old, live in layer:
            for a, b in combinations(sorted(live), 2):
                nxt.append((old + [[a, b]], live - {a}))
        layer = nxt
        if j < 2:
            continue
        counts[str(j)] = len(layer)
        for word, live in layer:
            f = scalar_forest(word, families['3H'])
            forests.append(f)
            reasons.update(h['kind'] for h in f['live_heads'])
    need(counts == {'2': 150, '3': 900, '4': 2700, '5': 2700}, 'complete6450 forest layers differ')
    math = {'literal_prefix': prefix, 'all_original_ground_records': families, 'initial_ordinary_classes': ground,
            'initial_third_HIGH_exponents': initial, 'tight_original_record': original,
            'entire2048_leaf_max_relation': relation, 'all6450_labelled_forests_and_live_head_proofs': forests,
            'forest_counts': counts, 'live_head_proof_counts': dict(sorted(reasons.items())),
            'live_head_count': sum(reasons.values()), 'full_freed_head_exclusion': False,
            'zero_HIGH_singleton_live_head_reduction': True, 'unrestricted44_exclusion': False}
    boundary = [x for x in range(8192) if (lambda v: v >> 8 & 1 > max(v >> q & 1 for q in (4, 5, 6, 9)))(bool_word(x, prefix))]
    need(len(boundary) == 10 and boundary[0] == 2069, 'unclamped identity boundary control differs')
    return math, {'all_six_actual_balanced_head_identity_checks': identity_checks,
                  'entire_tight_original_Q_rows_sha256': digest(rows),
                  'global_leaf_relation_counterexamples': boundary, 'numeric_ground_assignments': 612352}


def compact_from(math, fixture):
    return {'schema': fixture['schema'], 'prefix_sha256': digest(math['literal_prefix']), 'size_budget': 44,
            'binary_counts': [2, 3, 4, 5], 'initial_ordinary_classes': math['initial_ordinary_classes'],
            'initial_third_HIGH_exponents': math['initial_third_HIGH_exponents'],
            'tight_original_record': math['tight_original_record'], 'original_masks': [0, 3], 'head': [8, 9],
            'component_leaves': [4, 5, 6, 9], 'whole_clamped_assignments': 2048,
            'entire_leaf_max_relation_sha256': digest(math['entire2048_leaf_max_relation']),
            'imported_size': 35, 'forced_size': 45,
            'all_original_ground_records_sha256': digest(math['all_original_ground_records']),
            'all6450_labelled_forest_proofs_sha256': digest(math['all6450_labelled_forests_and_live_head_proofs']),
            'forest_counts': math['forest_counts'], 'live_head_proof_counts': math['live_head_proof_counts'],
            'live_head_count': math['live_head_count'], 'entire_mathematical_record_sha256': digest(math)}


def controls(math, compact, fixture):
    rejected = []

    def fail(name, operation):
        try:
            operation()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damage accepted: ' + name)

    # These mutations target fields that have been independently rebuilt
    # from all original inputs and every labelled history, not hash-only
    # checks of a producer that could have self-certified bad mathematics.
    damages = []
    for name, key, value in (
        ('wrong_size_budget', 'size_budget', 45),
        ('missing_binary_layer', 'binary_counts', [2, 3, 4]),
        ('wrong_original_masks', 'original_masks', [0, 5]),
        ('wrong_head_endpoint', 'head', [7, 9]),
        ('missing_component_leaf', 'component_leaves', [4, 5, 6]),
        ('wrong_cube_cardinality', 'whole_clamped_assignments', 1024),
        ('weakened_imported_floor', 'imported_size', 34),
        ('non_strict_forced_size', 'forced_size', 44),
        ('wrong_leaf_relation_digest', 'entire_leaf_max_relation_sha256', '0' * 64),
        ('wrong_forests_digest', 'all6450_labelled_forest_proofs_sha256', '0' * 64),
    ):
        damaged = copy.deepcopy(compact)
        damaged[key] = value
        damages.append((name, damaged))
    damaged = copy.deepcopy(compact)
    damaged['tight_original_record'][4] = 8
    damages.append(('wrong_original_D', damaged))
    damaged = copy.deepcopy(compact)
    damaged['forest_counts']['4'] -= 1
    damages.append(('missing_labelled_binary_history', damaged))
    for name, damaged in damages:
        fail(name, lambda d=damaged: need(d == compact_from(math, fixture), 'scalar certificate differs'))
    fail('crossing_overlapping_component_events',
         lambda: split_word([[4, 5], [5, 6], [6, 9]], 9, {6, 9}))
    fail('selecting_non_live_partner',
         lambda: split_word([[4, 5], [6, 9], [5, 9]], 5, {4, 5, 6, 9}))
    # The equality case is real: four events, root9 at exponent13, M24576.
    # It must use the clamped identity, not a non-strict ordinary-mass test.
    boundary = scalar_forest([[4, 5], [6, 9], [5, 9], [7, 10]], math['all_original_ground_records']['3H'])
    head = next(h for h in boundary['live_heads'] if h['partner'] == 9)
    need(boundary['stages'][-1][1] + 8192 == 32768 and
         head['kind'] == 'TIGHT_ORIGINAL_BALANCED_HEAD_IDENTITY', 'strict ordinary-mass boundary lost')
    fail('mistaking_mass_equality_for_exclusion',
         lambda: need(boundary['stages'][-1][1] + 8192 > 32768, 'mass equality is not a contradiction'))
    record = math['tight_original_record']
    fail('deletion_count_without_head_identity_is_insufficient',
         lambda: need(record[4] + record[5] + 35 > 44, 'base tight cost alone does not exclude'))
    # A full correct45 network supplies the positive whole-input control.
    positive = json.loads((ROOT / 'positive45.json').read_text())
    word = positive['gates']
    need(len(word) == 45 and all(bool_word(x, word) == sum(1 << q for q in range(13)
         if x.bit_count() >= 13 - q) for x in range(8192)), 'positive45 network does not sort')
    return {'rejected_damages': rejected, 'rejected_damage_count': len(rejected),
            'mass_equality_case_uses_identity': boundary, 'positive45_Boolean_inputs': 8192}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--producer', type=Path, default=ROOT / 'generated/produced.json')
    parser.add_argument('--certificate', type=Path, default=ROOT / 'generated/certificate.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'generated/checked.json')
    args = parser.parse_args()
    started = time.monotonic()
    fixture = json.loads((ROOT / 'fixture.json').read_text())
    math, extra = reconstruct(fixture)
    produced = json.loads(args.producer.read_text())
    need(math == produced['mathematical'] and digest(math) == produced['entire_mathematical_record_sha256'],
         'entire independently reconstructed mathematical record differs')
    compact = compact_from(math, fixture)
    need(json.loads(args.certificate.read_text()) == compact, 'public compact certificate differs from actual scalar proof')
    checked = {'entire_reproduced_mathematical_sha256': digest(math), 'compact_certificate': compact,
               'extra_original_numeric_checks': extra, 'controls': controls(math, compact, fixture),
               'ordinary_normalization_and_threshold_bridges': 'written unformalized proof',
               'independent_person_review': 'pending', 'unrestricted44_exclusion': False}
    out = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_SEPARATE_SCALAR_LIVE_HEAD_REDUCTION',
           'mathematical': checked, 'entire_mathematical_record_sha256': digest(checked),
           'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'mathematical'}))


if __name__ == '__main__':
    main()
