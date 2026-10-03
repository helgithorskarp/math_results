"""Packed producer of a compact universal live-head reduction certificate.

Full records are local generated state. The public certificate contains
ground classes, the tight original witness and complete-record hashes.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

from packed import HIGH, LOW, marked_ports, transition, truth_columns

ROOT = Path(__file__).resolve().parent
DEAD = (4, 5, 6, 7, 9, 10)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def profile(prefix, lo, hi):
    columns = iter(truth_columns(13 - (lo | hi).bit_count()))
    v = [LOW if lo >> q & 1 else HIGH if hi >> q & 1 else next(columns) for q in range(13)]
    d = r = ids = 0
    for i, gate in enumerate(prefix):
        hit, redundant = transition(v, *gate)
        d += hit
        r += redundant
        ids |= redundant << i
    return [lo, hi, *marked_ports(v), d, r, ids], v


def words(count, live=DEAD, prefix=()):
    if count == 0:
        yield [list(g) for g in prefix]
    else:
        for a, b in combinations(live, 2):
            yield from words(count - 1, tuple(q for q in live if q != a), prefix + ((a, b),))


def forest(word, initial):
    costs, parts, stages = dict(initial), {q: {q} for q in DEAD}, []
    for a, b in word:
        need(a in costs and b in costs, 'non-live binary')
        costs[b] = 1 + max(costs.pop(a), costs[b])
        parts[b] |= parts.pop(a)
        stages.append([[[q, e] for q, e in sorted(costs.items())], sum(1 << e for e in costs.values())])
    heads = []
    for q, component in sorted(parts.items()):
        if any(stage[1] > 32768 for stage in stages):
            kind, details = 'ORDINARY_PREPARATION_MASS', {}
        elif len(word) == 2:
            kind, details = 'PUBLIC_TWO_BINARY_EXCLUSION', {}
        else:
            inside = [g for g in word if set(g) <= component]
            outside = [g for g in word if not set(g) <= component]
            if len(inside) <= 2:
                reordered = inside + outside
                prefix2, suffix = reordered[:2], reordered[2:]
                need(all(set(g).isdisjoint({8, q, 1, 2, 3, min(8, q)}) for g in suffix),
                     'head/tail does not commute through outside events')
                kind, details = 'COMMUTATION_TO_PUBLIC_TWO_BINARY', {
                    'component_binary_count': len(inside), 'reordered_forest': reordered,
                    'two_binary_prefix': prefix2, 'displaced_binary_suffix': suffix}
            elif stages[-1][1] + (1 << costs[q]) > 32768:
                kind, details = 'ORDINARY_HEAD_MASS', {
                    'exponent': costs[q], 'head_mass': stages[-1][1] + (1 << costs[q])}
            else:
                need(component == {4, 5, 6, 9} and q == 9 and costs[q] == 13,
                     'unexpected live-component exception')
                need(len(inside) == 3 and set(inside[0]).isdisjoint(inside[1]), 'unbalanced exception')
                kind, details = 'TIGHT_ORIGINAL_BALANCED_HEAD_IDENTITY', {
                    'component_binary_count': 3, 'leaves': sorted(component), 'original_masks': [0, 3],
                    'head': [8, 9], 'original_D_at_Q': 9, 'additional_head_R': 1,
                    'imported_size': 35, 'forced_size': 45}
        heads.append({'partner': q, 'kind': kind, **details})
    return {'binary_count': len(word), 'word': word, 'stages': stages,
            'components': [[q, sorted(s)] for q, s in sorted(parts.items())], 'live_heads': heads}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'generated/produced.json')
    parser.add_argument('--certificate', type=Path, default=ROOT / 'generated/certificate.json')
    args = parser.parse_args()
    start = time.monotonic()
    fixture = json.loads((ROOT / 'fixture.json').read_text())
    prefix = fixture['literal_prefix']
    need(digest(prefix) == '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4', 'literal Q changed')
    families, initial_classes = {}, {}
    for name, count, is_low in (('2L', 2, True), ('2H', 2, False), ('3H', 3, False)):
        records, envelope = [], {}
        for ports in combinations(range(13), count):
            mask = sum(1 << q for q in ports)
            record, _ = profile(prefix, mask if is_low else 0, 0 if is_low else mask)
            records.append(record)
            tag = tuple(record[2:4])
            envelope[tag] = max(envelope.get(tag, -1), record[4])
        families[name] = records
        initial_classes[name] = [[*tag, d] for tag, d in sorted(envelope.items())]
    initial = {q: max(r[4] for r in families['3H'] if r[3] == 6144 | (1 << q)) for q in DEAD}
    need(sorted(initial.items()) == [(4, 11), (5, 11), (6, 11), (7, 13), (9, 11), (10, 12)], 'ground high exponents changed')
    original, v = profile(prefix, 0, 3)
    need(original == [0, 3, 0, 6144, 9, 0, 0], 'tight original record changed')
    maximum = v[4] | v[5] | v[6] | v[9]
    relation = [[v[8] >> x & 1, maximum >> x & 1] for x in range(2048)]
    need(all(a <= b for a, b in relation), 'entire tight-domain leaf relation fails')
    all_forests, counts, reasons = [], {}, Counter()
    for j in (2, 3, 4, 5):
        records = [forest(w, initial) for w in words(j)]
        counts[str(j)] = len(records)
        for f in records:
            reasons.update(h['kind'] for h in f['live_heads'])
        all_forests.extend(records)
    need(counts == {'2': 150, '3': 900, '4': 2700, '5': 2700}, 'complete labelled-forest counts changed')
    math = {'literal_prefix': prefix, 'all_original_ground_records': families,
            'initial_ordinary_classes': initial_classes, 'initial_third_HIGH_exponents': [[q, e] for q, e in sorted(initial.items())],
            'tight_original_record': original, 'entire2048_leaf_max_relation': relation,
            'all6450_labelled_forests_and_live_head_proofs': all_forests,
            'forest_counts': counts, 'live_head_proof_counts': dict(sorted(reasons.items())),
            'live_head_count': sum(reasons.values()), 'full_freed_head_exclusion': False,
            'zero_HIGH_singleton_live_head_reduction': True, 'unrestricted44_exclusion': False}
    compact = {'schema': fixture['schema'], 'prefix_sha256': digest(prefix), 'size_budget': 44,
               'binary_counts': [2, 3, 4, 5], 'initial_ordinary_classes': initial_classes,
               'initial_third_HIGH_exponents': math['initial_third_HIGH_exponents'],
               'tight_original_record': original, 'original_masks': [0, 3], 'head': [8, 9],
               'component_leaves': [4, 5, 6, 9], 'whole_clamped_assignments': 2048,
               'entire_leaf_max_relation_sha256': digest(relation), 'imported_size': 35, 'forced_size': 45,
               'all_original_ground_records_sha256': digest(families),
               'all6450_labelled_forest_proofs_sha256': digest(all_forests),
               'forest_counts': counts, 'live_head_proof_counts': math['live_head_proof_counts'],
               'live_head_count': math['live_head_count'], 'entire_mathematical_record_sha256': digest(math)}
    out = {'agent': 'six-sorting-2', 'role': 'researcher', 'mathematical': math,
           'entire_mathematical_record_sha256': digest(math), 'seconds': time.monotonic() - start,
           'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(',', ':')) + '\n')
    args.certificate.write_text(json.dumps(compact, indent=2) + '\n')
    print(json.dumps({**{k: v for k, v in out.items() if k != 'mathematical'},
                      'forest_counts': counts, 'live_head_proof_counts': math['live_head_proof_counts']}))


if __name__ == '__main__':
    main()
