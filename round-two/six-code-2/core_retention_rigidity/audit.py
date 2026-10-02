"""Independent inverse-triple coverage and deletion-contraction audit.

six-code-2, researcher. No producer import. Physical frozensets and all
extensions of every occupied triple reconstruct the full conflict oracle.
Maximum tail sizes/counts are computed by exact independence recurrences,
without the producer's lower-bound pruning or maximum-clique enumeration.
"""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def need(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def points(word):
    return frozenset(p for p in range(18) if word >> p & 1)


def literal_packing(words, count):
    need(len(words) == len(set(words)) == count, 'packing cardinality or duplicate')
    occupied = set()
    for word in words:
        need(0 <= word < 2 ** 18 and len(points(word)) == 5, 'nonphysical word')
        for triple in combinations(sorted(points(word)), 3):
            need(triple not in occupied, 'repeated physical triple')
            occupied.add(triple)
    need(len(occupied) == 10 * count, 'wrong occupied triple count')


def physical_oracle(fixture):
    core = tuple(fixture['core_words'])
    literal_packing(core, 57)
    owners = defaultdict(set)
    for i, word in enumerate(core):
        for triple in combinations(sorted(points(word)), 3):
            triple = frozenset(triple)
            for other in combinations(sorted(set(range(18)) - triple), 2):
                owners[triple | frozenset(other)].add(i)
    physical = tuple(sorted((sum(2 ** p for p in ps), frozenset(ps))
                            for ps in combinations(range(18), 5)))
    need(len(physical) == 8568, 'incomplete physical universe')
    rows = tuple((word, frozenset(owners[ps])) for word, ps in physical)
    oracle = [[word, sum(2 ** i for i in conflicts)] for word, conflicts in rows]
    return rows, oracle


def check_oracle(actual, expected):
    need(actual == expected and len(actual) == 8568, 'full inverse-extension oracle mismatch')


def base_states(fixture, certificate, allowed):
    core = tuple(fixture['core_words'])
    pairs = tuple(map(tuple, fixture['paired_words']))
    exceptions = tuple(fixture['exceptional_words'])
    need(len(pairs) == 12 and all(len(p) == 2 for p in pairs), 'wrong pair cover')
    variables = tuple(w for pair in pairs for w in pair)
    need(len(set(variables)) == 24 and not set(variables) & set(core), 'false pair cover')
    need(len(exceptions) == len(set(exceptions)) == 2 and
         not set(exceptions) & (set(core) | set(variables)), 'false exceptional options')
    need(set(allowed) == set(variables) | set(exceptions), 'core compatible universe was pruned')
    need(all(len(points(a) & points(b)) >= 3 for a, b in pairs), 'pair is not a conflict clique')
    need(all(len(points(pairs[i][1]) & points(pairs[j][0])) <= 2
             for i in range(12) for j in range(12) if i != j), 'false cross-pair compatibility')
    blocked = [tuple(i for i, pair in enumerate(pairs)
                     if all(len(points(e) & points(w)) >= 3 for w in pair)) for e in exceptions]
    need(all(len(indices) == 4 for indices in blocked) and set(blocked[0]).isdisjoint(blocked[1]),
         'false exception pair obstruction')
    need(list(map(list, blocked)) == certificate['exception_blocked_pair_indices'] and
         certificate['exception_tail_bounds_for_zero_one_two_present'] == [12, 9, 6], 'bad exception certificate')
    edges = [(i, j) for i, j in combinations(range(12), 2)
             if len(points(pairs[i][1]) & points(pairs[j][1])) >= 3]
    need(list(map(list, edges)) == certificate['new_option_conflict_edges'], 'false switch conflict graph')
    adjacency = tuple(sum(2 ** j for j in range(12) if (min(i, j), max(i, j)) in edges)
                      for i in range(12))

    @lru_cache(None)
    def polynomial(domain):
        if not domain:
            return (1,)
        bit = domain & -domain
        vertex = bit.bit_length() - 1
        without = polynomial(domain ^ bit)
        inside = polynomial((domain ^ bit) & ~adjacency[vertex])
        result = [0] * max(len(without), len(inside) + 1)
        for degree, value in enumerate(without):
            result[degree] += value
        for degree, value in enumerate(inside):
            result[degree + 1] += value
        return tuple(result)

    def families(domain, selected):
        if not domain:
            return [selected]
        bit = domain & -domain
        vertex = bit.bit_length() - 1
        return (families(domain ^ bit, selected) +
                families((domain ^ bit) & ~adjacency[vertex], selected | bit))

    switches = sorted(families(2 ** 12 - 1, 0))
    need(switches == certificate['valid_switch_masks'], 'incomplete or false switch family inventory')
    coefficients = polynomial(2 ** 12 - 1)
    need([[i, n] for i, n in enumerate(coefficients) if n] == certificate['switch_size_histogram'],
         'deletion-contraction polynomial mismatch')
    states = [sorted(core + tuple(pairs[i][mask >> i & 1] for i in range(12))) for mask in switches]
    for state in states:
        literal_packing(state, 69)
    need(len(states) == len({tuple(s) for s in states}) == sum(coefficients), 'false maximum-code count')
    return states, coefficients


def maximum_independence(words, deadline):
    point_sets = tuple(points(w) for w in words)
    adjacency = tuple(sum(2 ** j for j, other in enumerate(point_sets)
                          if i != j and len(ps & other) >= 3) for i, ps in enumerate(point_sets))

    @lru_cache(None)
    def recurse(domain):
        if not domain:
            return 0, 1
        if recurse.cache_info().misses % 4096 == 0 and time.monotonic() > deadline:
            raise TimeoutError('INCOMPLETE initial60s independent whole1,596-domain guard')
        remaining = [i for i in range(len(words)) if domain >> i & 1]
        vertex = max(remaining, key=lambda i: (adjacency[i] & domain).bit_count())
        bit = 2 ** vertex
        without, count_without = recurse(domain ^ bit)
        inside, count_inside = recurse((domain ^ bit) & ~adjacency[vertex])
        inside += 1
        if without > inside:
            return without, count_without
        if inside > without:
            return inside, count_inside
        return inside, count_inside + count_without

    maximum, count = recurse(2 ** len(words) - 1)
    return maximum, count, recurse.cache_info().misses


def check_domain_records(records, traces):
    expected = list(map(list, combinations(range(57), 2)))
    need([r['removed_core_indices'] for r in records] == expected, 'omitted, duplicated or out-of-domain core deletion')
    need([t[0] for t in traces] == expected, 'missing maximum-tail trace domain')


def check_trace(candidates, states, core, removed, trace):
    need(trace[1] == list(candidates), 'physical replacement omitted from puncture domain')
    index = {word: i for i, word in enumerate(candidates)}
    retained = set(core) - {core[i] for i in removed}
    expected = sorted(sum(2 ** index[w] for w in set(state) - retained) for state in states)
    need(trace[2] == expected, 'false or incomplete maximum-tail inventory')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=Path, default=Path(__file__).parent / 'INSTANCE.json')
    parser.add_argument('--production', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'AUDIT.json').exists(), 'refuse to overwrite completed audit')
    begin = time.monotonic()
    raw = args.instance.read_bytes()
    fixture = json.loads(raw)
    result = json.loads((args.production / 'RESULT.json').read_bytes())
    need(result['status'] == 'COMPLETE_CORE_RETENTION55_UPPER69_AND_EXACT84_MAXIMA' and
         result['instance_sha256'] == hashlib.sha256(raw).hexdigest(), 'wrong or incomplete producer')
    def load_checked(name, hash_field):
        data = (args.production / name).read_bytes()
        need(hashlib.sha256(data).hexdigest() == result[hash_field], 'producer data changed: ' + name)
        return json.loads(data)
    actual_oracle = load_checked('ORACLE.json', 'full_oracle_sha256')
    rows, oracle = physical_oracle(fixture)
    check_oracle(actual_oracle, oracle)
    certificate = load_checked('CERTIFICATE.json', 'certificate_sha256')
    allowed = [word for word, conflicts in rows if not conflicts]
    states, coefficients = base_states(fixture, certificate, allowed)
    need(load_checked('STATES.json', 'states_sha256') == states, 'literal69-code inventory mismatch')
    records = load_checked('DOMAINS.json', 'domains_sha256')
    traces = load_checked('TAIL_MAXIMA.json', 'tail_maxima_sha256')
    check_domain_records(records, traces)
    core = tuple(fixture['core_words'])
    audit_records = []
    # Independent full-oracle filtering, without producer submask buckets.
    for position, removed in enumerate(combinations(range(57), 2)):
        if time.monotonic() - begin > 60:
            (args.work / 'partial.json').write_bytes(encoded({'status': 'INCOMPLETE_NO_WHOLE_FRONTIER_CLAIM',
                                                            'completed_domains': audit_records, 'initial_guard_seconds': 60}))
            raise TimeoutError('INCOMPLETE initial60s independent whole1,596-domain guard')
        removed_set = frozenset(removed)
        candidates = tuple(w for w, conflicts in rows if conflicts <= removed_set)
        record, trace = records[position], traces[position]
        check_trace(candidates, states, core, removed, trace)
        maximum, count, subproblems = maximum_independence(candidates, begin + 60)
        need(maximum == record['tail_maximum'] == 14 and count == record['maximum_completion_count'] == len(states),
             'independent maximum size/count differs')
        need(record['candidate_count'] == len(candidates) and
             record['candidate_words_sha256'] == hashlib.sha256(encoded(candidates)).hexdigest() and
             record['full_maximum_tail_inventory_sha256'] == hashlib.sha256(encoded([candidates, trace[2]])).hexdigest(),
             'false puncture domain evidence')
        audit_records.append({'removed_core_indices': removed, 'candidate_count': len(candidates),
                              'independent_tail_maximum': maximum, 'independent_maximum_count': count,
                              'deletion_contraction_subproblems': subproblems})
        if len(audit_records) % 400 == 0:
            (args.work / 'partial.json').write_bytes(encoded({'status': 'INCOMPLETE_WITH_COMPLETE_DOMAIN_RECORDS',
                                                            'completed_domains': audit_records, 'initial_guard_seconds': 60}))
            print(json.dumps({'independent_domains': len(audit_records), 'seconds': time.monotonic() - begin}), flush=True)
    damages = []
    def rejects(label, callback):
        try:
            callback()
        except (ValueError, KeyError, IndexError):
            damages.append({'label': label, 'rejected': True})
            return
        raise ValueError('semantic damage accepted: ' + label)
    damaged = deepcopy(actual_oracle)
    damaged.pop()
    rejects('omitted physical word', lambda: check_oracle(damaged, oracle))
    damaged = deepcopy(actual_oracle)
    i = next(i for i, (w, c) in enumerate(damaged) if w in core)
    damaged[i][1] = 0
    rejects('erased core self conflict', lambda: check_oracle(damaged, oracle))
    damaged = deepcopy(actual_oracle)
    i = next(i for i, (w, c) in enumerate(damaged) if w not in core and c)
    damaged[i][1] ^= 1
    rejects('altered outside core conflict', lambda: check_oracle(damaged, oracle))
    damaged = deepcopy(certificate)
    damaged['exception_blocked_pair_indices'][0].pop()
    rejects('false exceptional four-pair obstruction', lambda: base_states(fixture, damaged, allowed))
    damaged = deepcopy(certificate)
    damaged['new_option_conflict_edges'].pop()
    rejects('removed switch conflict edge', lambda: base_states(fixture, damaged, allowed))
    damaged = deepcopy(certificate)
    damaged['switch_size_histogram'][2][1] -= 1
    rejects('false independence polynomial', lambda: base_states(fixture, damaged, allowed))
    damaged = deepcopy(certificate)
    damaged['valid_switch_masks'].pop()
    rejects('omitted maximum completion', lambda: base_states(fixture, damaged, allowed))
    damaged_records = deepcopy(records)
    damaged_records[-1] = deepcopy(records[-2])
    rejects('accounting-consistent duplicated core-deletion domain', lambda: check_domain_records(damaged_records, traces))
    candidates = tuple(traces[0][1])
    damaged_trace = deepcopy(traces[0])
    damaged_trace[1].pop()
    rejects('omitted puncture replacement word', lambda: check_trace(candidates, states, core, tuple(traces[0][0]), damaged_trace))
    damaged_trace = deepcopy(traces[0])
    damaged_trace[2].pop()
    rejects('omitted maximum tail with complete domain', lambda: check_trace(candidates, states, core, tuple(traces[0][0]), damaged_trace))
    rejects('duplicate literal word', lambda: literal_packing(tuple(states[0][:-1]) + (states[0][0],), 69))
    path = args.work / 'DOMAIN_AUDIT.json'
    path.write_bytes(encoded(audit_records))
    value = {'agent': 'six-code-2', 'role': 'researcher',
             'status': 'COMPLETE_INDEPENDENT_CORE_RETENTION55_MAXIMUM_SIZE_COUNT_AND_INVENTORY_AUDIT',
             'instance_sha256': hashlib.sha256(raw).hexdigest(),
             'full8568_inverse_triple_oracle_compared_entrywise': True,
             'independent_switch_polynomial': list(coefficients),
             'independent_literal69_states': len(states), 'independent_core_deletion_domains': len(audit_records),
             'independent_maximum_tail_size_histogram': sorted(Counter(r['independent_tail_maximum'] for r in audit_records).items()),
             'independent_maximum_count_histogram': sorted(Counter(r['independent_maximum_count'] for r in audit_records).items()),
             'all_producer_maximum_tail_inventories_compared_entrywise': True,
             'total_deletion_contraction_subproblems': sum(r['deletion_contraction_subproblems'] for r in audit_records),
             'domain_audit_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'damage_controls': damages,
             'initial_whole_guard_seconds': 60, 'seconds': time.monotonic() - begin,
             'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'degree20_used_as_premise': False, 'solver_used': False,
             'scope': 'Same-author different mathematical algorithms and encodings; not independent peer review. Only the explicitly supplied57-word core and retention55.'}
    (args.work / 'AUDIT.json').write_bytes(encoded(value))
    print(json.dumps(value, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
