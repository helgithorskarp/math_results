"""Independent row census, dual local search, and point-bijection global audit."""
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from census import census
from audit_census import canonical, independent
from audit_local import enumerate_dual
from audit_glue import point_maps, check_union, members
from glue import joins

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def independent_join(root, templates):
    p = 11
    a0 = tuple(row | (1 << p) for row in root['a'])
    b0 = tuple(row | (1 << p) for row in root['b'])
    multiplicities = [(sum(bool(row & (1 << q)) for row in a0),
                       sum(bool(row & (1 << q)) for row in b0)) for q in range(11)]
    q = max(range(11), key=lambda q: (multiplicities[q][0], -multiplicities[q][1], -q))
    alpha, beta = multiplicities[q]
    require(alpha >= 3, 'no high through-pair')
    ta = tuple(set(members(row)) - {p, q} for row in a0 if row & (1 << q))
    tb = tuple(set(members(row)) - {p, q} for row in b0 if row & (1 << q))
    outputs = set()
    mapping_count = 0
    for template in templates:
        for marked in range(11):
            sa = tuple(set(members(row, 11)) - {marked} for row in template['a']
                       if row & (1 << marked))
            sb = tuple(set(members(row, 11)) - {marked} for row in template['b']
                       if row & (1 << marked))
            if (len(sa), len(sb)) != (alpha, beta):
                continue
            source_points = tuple(x for x in range(11) if x != marked)
            target_points = tuple(x for x in range(12) if x not in (p, q))
            for mapping in point_maps(sa, sb, ta, tb, source_points, target_points):
                mapping_count += 1
                mapping[marked] = p
                aq = tuple((1 << q) | sum(1 << mapping[x] for x in members(row, 11))
                           for row in template['a'])
                bq = tuple((1 << q) | sum(1 << mapping[x] for x in members(row, 11))
                           for row in template['b'])
                a = tuple(sorted(set(a0 + aq)))
                b = tuple(sorted(set(b0 + bq)))
                require(len(a) == 10 - alpha and len(b) == 8 - beta, 'join size')
                if check_union(a, b):
                    outputs.add((a, b))
    return p, q, outputs, mapping_count


def finish_without_weights(p, q, through, away):
    a = [set(members(row)) for row in through]
    b = [set(members(row)) for row in away]
    require(len(a) == len(b) == 7, 'unexpected surviving joint link')
    missing_degrees = {v: 4 - sum(v in block for block in b) for v in range(12)}
    if any(value < 0 or value > 1 for value in missing_degrees.values()):
        return 'degree', 0
    forced = {v for v, value in missing_degrees.items() if value == 1}
    require(len(forced) == 6 and not forced & {p, q}, 'forced away block')
    b.append(forced)
    required = [frozenset(t) for t in combinations(range(12), 2)
                if not any(set(t) <= row for row in a)]
    required += [frozenset(t) for t in combinations(range(12), 3)
                 if not any(set(t) <= row for row in a + b)]
    candidates = [set(t) for t in combinations([v for v in range(12) if v not in (p, q)], 5)]
    masks = set(sum(1 << i for i, target in enumerate(required) if target <= row)
                for row in candidates)
    maximal = []
    for value in sorted(masks, key=lambda value: (-value.bit_count(), value)):
        if not any(value | larger == larger for larger in maximal):
            maximal.append(value)
    incidence = [tuple(value for value in maximal if value & (1 << i))
                 for i in range(len(required))]

    @cache
    def possible(uncovered, allowance):
        if not uncovered:
            return True
        if not allowance:
            return False
        if allowance == 1:
            return any(uncovered & value == uncovered for value in maximal)
        if uncovered.bit_count() > allowance * max((uncovered & value).bit_count()
                                                   for value in maximal):
            return False
        edge = min((i for i in range(len(required)) if uncovered & (1 << i)),
                   key=lambda i: len(incidence[i]))
        return any(possible(uncovered & ~value, allowance - 1) for value in incidence[edge])

    require(not possible((1 << len(required)) - 1, 5), 'five-block relaxation survives')
    states = possible.cache_info().misses
    possible.cache_clear()
    return 'set_cover', states


def main():
    records, _ = census()
    states, levels = independent()
    canonical_records = {canonical(tuple(Counter(row['columns'])[m] for m in range(32)), 5)
                         for row in records}
    require(states == canonical_records and len(records) == len(canonical_records),
            'independent through-system census differs')
    fixture = json.loads((ROOT / 'LOCAL.json').read_text())
    expected = {row['type']: row for row in fixture}
    all_templates = []
    local_nodes = 0
    for index, record in enumerate(records):
        covers, nodes = enumerate_dual(record['columns'])
        local_nodes += nodes
        if index in expected:
            require(record['rows'] == expected[index]['a'], 'local through-row fixture differs')
            require(covers == list(map(tuple, expected[index]['covers'])), 'local completions differ')
        else:
            require(not covers, 'unexpected completable local type')
        all_templates.extend(dict(a=record['rows'], b=list(cover)) for cover in covers)
    representatives = json.loads((ROOT / 'LINKS.json').read_text())
    primary = {}
    for template in representatives:
        result = joins(template, representatives)
        primary[tuple(template['a']), tuple(template['b'])] = {
            (tuple(c['a']), tuple(c['b'])) for c in result['configurations']}
    counts = Counter()
    mappings = 0
    joined_cases = 0
    final_states = 0
    compared = set()
    for template in all_templates:
        p, q, configurations, number = independent_join(template, all_templates)
        mappings += number
        joined_cases += len(configurations)
        key = tuple(template['a']), tuple(template['b'])
        if key in primary:
            require(configurations == primary[key], 'independent point-bijection join differs')
            compared.add(key)
        for a, b in configurations:
            reason, nodes = finish_without_weights(p, q, a, b)
            counts[reason] += 1
            final_states += nodes
    require(compared == set(primary), 'not all reduced roots were checked')
    output = dict(status='INDEPENDENT_AUDIT_NO_EXCEPTIONAL_PROFILE',
                  row_extension_levels=levels, local_signature_nodes=local_nodes,
                  labelled_link_roots=len(all_templates), point_bijections=mappings,
                  joined_configurations=joined_cases, exclusions=dict(counts),
                  final_set_cover_states=final_states, compared_representative_roots=len(compared))
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
