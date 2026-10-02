"""Exact maximum completions of all 1,596 literal 55-word core punctures.

six-code-2, researcher. Standard library; all replacement words are the
8,568 physical five-subsets. No output symmetry or point-degree filter.
Bulky regenerated oracles/domain traces stay in the supplied work folder.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import time


def need(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def word_triples(word):
    return tuple(sum(1 << p for p in triple)
                 for triple in combinations([p for p in range(18) if word >> p & 1], 3))


def packing(words, count):
    need(len(words) == len(set(words)) == count, 'wrong or duplicate code cardinality')
    need(all(0 <= w < 1 << 18 and w.bit_count() == 5 for w in words), 'nonphysical word')
    need(all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)), 'literal code violates distance')


def input_data(fixture):
    core = tuple(fixture['core_words'])
    pairs = tuple(map(tuple, fixture['paired_words']))
    exceptions = tuple(fixture['exceptional_words'])
    packing(core, 57)
    need(len(pairs) == 12 and all(len(p) == 2 for p in pairs), 'wrong pair cover')
    variables = tuple(w for pair in pairs for w in pair)
    need(len(set(variables)) == 24 and not set(variables) & set(core), 'overlapping pair cover')
    need(len(exceptions) == len(set(exceptions)) == 2 and
         not set(exceptions) & (set(core) | set(variables)), 'wrong exceptions')
    need(all(0 <= w < 1 << 18 and w.bit_count() == 5 for w in variables + exceptions), 'nonphysical option')
    packing(core + tuple(a for a, b in pairs), 69)
    return core, pairs, exceptions


def base_certificate(core, pairs, exceptions, allowed):
    need(set(allowed) == {w for pair in pairs for w in pair} | set(exceptions), 'incomplete 26-word core domain')
    need(all((a & b).bit_count() >= 3 for a, b in pairs), 'pair is not a conflict clique')
    need(all((pairs[i][1] & pairs[j][0]).bit_count() <= 2 for i in range(12)
             for j in range(12) if i != j), 'new option has unrecorded old-word conflict')
    blocked = [tuple(i for i, (a, b) in enumerate(pairs)
                     if (e & a).bit_count() >= 3 and (e & b).bit_count() >= 3) for e in exceptions]
    need(all(len(indices) == 4 for indices in blocked) and not set(blocked[0]) & set(blocked[1]),
         'exceptional option lacks disjoint four-pair obstruction')
    edges = tuple((i, j) for i, j in combinations(range(12), 2)
                  if (pairs[i][1] & pairs[j][1]).bit_count() >= 3)
    switches = []
    states = []
    for mask in range(1 << 12):
        if any(mask >> i & 1 and mask >> j & 1 for i, j in edges):
            continue
        words = tuple(sorted(pairs[i][mask >> i & 1] for i in range(12)))
        packing(core + words, 69)
        switches.append(mask)
        states.append(words)
    polynomial = sorted(Counter(mask.bit_count() for mask in switches).items())
    return {'pair_count': 12, 'exception_blocked_pair_indices': blocked,
            'exception_tail_bounds_for_zero_one_two_present': [12, 9, 6],
            'new_option_conflict_edges': edges,
            'valid_switch_masks': switches, 'switch_size_histogram': polynomial}, tuple(states)


def maximum_cliques(words, lower, deadline):
    adjacency = tuple(sum(1 << j for j, b in enumerate(words)
                          if a != b and (a & b).bit_count() <= 2) for a in words)
    best = lower
    maxima = []
    nodes = 0

    def visit(domain, selected, size):
        nonlocal best, maxima, nodes
        nodes += 1
        if nodes % 4096 == 0 and time.monotonic() > deadline:
            raise TimeoutError('INCOMPLETE initial60s whole1,596-domain guard')
        if size > best:
            best, maxima = size, [selected]
        elif size == best:
            maxima.append(selected)
        while domain:
            # Strict inequality preserves every maximum, not just one.
            if size + domain.bit_count() < best:
                break
            bit = domain & -domain
            domain ^= bit
            vertex = bit.bit_length() - 1
            visit(domain & adjacency[vertex], selected | bit, size + 1)

    visit((1 << len(words)) - 1, 0, 0)
    need(maxima and len(maxima) == len(set(maxima)), 'missing or duplicate maximum clique')
    return best, tuple(sorted(maxima)), nodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=Path, default=Path(__file__).parent / 'INSTANCE.json')
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'RESULT.json').exists(), 'refuse to overwrite completed evidence')
    begin = time.monotonic()
    raw = args.instance.read_bytes()
    core, pairs, exceptions = input_data(json.loads(raw))
    physical = tuple(sorted(sum(1 << p for p in ps) for ps in combinations(range(18), 5)))
    need(len(physical) == len(set(physical)) == 8568, 'incomplete physical universe')
    owners = {}
    for i, word in enumerate(core):
        for triple in word_triples(word):
            need(triple not in owners, 'core repeats a physical triple')
            owners[triple] = i
    need(len(owners) == 570, 'wrong core triple count')
    oracle = []
    buckets = defaultdict(list)
    for word in physical:
        direct = sum(1 << i for i, b in enumerate(core) if (word & b).bit_count() >= 3)
        triples = 0
        for triple in word_triples(word):
            if triple in owners:
                triples |= 1 << owners[triple]
        need(direct == triples, 'entrywise physical / triple-owner conflict mismatch')
        oracle.append([word, direct])
        if direct.bit_count() <= 2:
            buckets[direct].append(word)
    oracle_path = args.work / 'ORACLE.json'
    oracle_path.write_bytes(encoded(oracle))
    certificate, states = base_certificate(core, pairs, exceptions, buckets[0])
    (args.work / 'CERTIFICATE.json').write_bytes(encoded(certificate))
    (args.work / 'STATES.json').write_bytes(encoded([sorted(core + state) for state in states]))
    state_keys = set(states)
    records = []
    traces = []
    for removed in combinations(range(57), 2):
        mask = sum(1 << i for i in removed)
        candidates = tuple(sorted(buckets[0] + buckets[1 << removed[0]] +
                                  buckets[1 << removed[1]] + buckets[mask]))
        best, maxima, nodes = maximum_cliques(candidates, 14, begin + 60)
        restored_states = []
        for tail in maxima:
            selected = tuple(candidates[i] for i in range(len(candidates)) if tail >> i & 1)
            if best >= 15:
                code = tuple(sorted([w for i, w in enumerate(core) if i not in removed] + list(selected[:15])))
                packing(code, 70)
                (args.work / 'WITNESS70.json').write_bytes(encoded({'words': code, 'removed': removed}))
                raise ValueError('literal70 gain needs separate claim; no negative completion result')
            restored = all(core[i] in selected for i in removed)
            variable = tuple(w for w in selected if w not in core)
            if not restored or variable not in state_keys:
                code = tuple(sorted([w for i, w in enumerate(core) if i not in removed] + list(selected)))
                packing(code, 69)
                (args.work / 'WITNESS69_ESCAPE.json').write_bytes(encoded({'words': code, 'removed': removed}))
                raise ValueError('neutral69 escape from core component; no rigidity claim')
            restored_states.append(variable)
        need(best == 14 and set(restored_states) == state_keys and len(maxima) == len(state_keys),
             'maximum completion inventory does not exactly equal base states')
        graph_hash = hashlib.sha256(encoded([candidates, maxima])).hexdigest()
        records.append({'removed_core_indices': removed, 'candidate_count': len(candidates),
                        'candidate_words_sha256': hashlib.sha256(encoded(candidates)).hexdigest(),
                        'tail_maximum': best, 'code_maximum': 55 + best,
                        'maximum_completion_count': len(maxima),
                        'all_maxima_restore_both_deleted_core_words': True,
                        'full_maximum_tail_inventory_sha256': graph_hash, 'clique_DFS_nodes': nodes})
        traces.append([removed, candidates, maxima])
        if len(records) % 200 == 0:
            (args.work / 'partial.json').write_bytes(encoded({'status': 'INCOMPLETE_WITH_COMPLETE_DOMAIN_RECORDS',
                                                            'completed_domains': records, 'initial_guard_seconds': 60}))
            print(json.dumps({'completed_domains': len(records), 'seconds': time.monotonic() - begin}), flush=True)
    need(len(records) == comb(57, 2) == 1596, 'incomplete two-core deletion domain')
    domain_path, trace_path = args.work / 'DOMAINS.json', args.work / 'TAIL_MAXIMA.json'
    domain_path.write_bytes(encoded(records))
    trace_path.write_bytes(encoded(traces))
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_CORE_RETENTION55_UPPER69_AND_EXACT84_MAXIMA',
              'instance_sha256': hashlib.sha256(raw).hexdigest(),
              'all8568_literal_and_triple_owner_conflicts_entrywise_equal': True,
              'full_oracle_sha256': hashlib.sha256(oracle_path.read_bytes()).hexdigest(),
              'core_conflict_size_histogram': sorted(Counter(c.bit_count() for w, c in oracle).items()),
              'core_words': 57, 'retained_core_words': 55, 'physical_word_universe': 8568,
              'core_compatible_new_words': len(buckets[0]), 'paired_options': 12,
              'exceptional_options': 2, 'all_core_maximum_codes': len(states),
              'switch_size_histogram': certificate['switch_size_histogram'],
              'two_core_deletion_domains': len(records),
              'two_core_domain_candidate_size_histogram': sorted(Counter(r['candidate_count'] for r in records).items()),
              'code_maximum_histogram': sorted(Counter(r['code_maximum'] for r in records).items()),
              'maximum_completion_count_histogram': sorted(Counter(r['maximum_completion_count'] for r in records).items()),
              'all_maxima_restore_deleted_core_words': True, 'total_clique_DFS_nodes': sum(r['clique_DFS_nodes'] for r in records),
              'domains_sha256': hashlib.sha256(domain_path.read_bytes()).hexdigest(),
              'tail_maxima_sha256': hashlib.sha256(trace_path.read_bytes()).hexdigest(),
              'certificate_sha256': hashlib.sha256((args.work / 'CERTIFICATE.json').read_bytes()).hexdigest(),
              'states_sha256': hashlib.sha256((args.work / 'STATES.json').read_bytes()).hexdigest(),
              'initial_whole_guard_seconds': 60, 'seconds': time.monotonic() - begin,
              'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'degree20_used_as_premise': False, 'solver_used': False,
              'scope': 'Only codes containing at least55 of the explicitly supplied57 core words. No global70 absence, no new lower69 record.'}
    (args.work / 'RESULT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
