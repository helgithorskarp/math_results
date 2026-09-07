#!/usr/bin/env python3
"""Directly check the frozen formula's SAT word and its nonextendable partition."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

SOURCE_SHA = '201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d'
CNF_SHA = '57058179a7ca8dd5d74c9711f202a53378b1adba9001786687dd92e82d3cf038'
CYCLES_SHA = 'bac6fe6962012d4ae5c79e65e9ad5dc39383bfd5c40d651f9cff877ac61b5a63'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def quotient(v):
    return 0 if v == 5 else v - int(v > 5)


def inspect_header(cert, source_raw, cnf_raw, cycles_raw):
    require(cert['format'] == 1 and cert['variables'] == 739, 'wrong certificate format')
    require(digest(source_raw) == SOURCE_SHA == cert['source_graph_sha256'], 'source identity mismatch')
    require(digest(cnf_raw) == CNF_SHA == cert['cnf_sha256'], 'CNF identity mismatch')
    require(digest(cycles_raw) == CYCLES_SHA == cert['frozen_cycles_sha256'], 'cycle identity mismatch')
    word = cert['boolean_word']
    require(type(word) is str and len(word) == 739 and set(word) <= {'0', '1'}, 'malformed Boolean word')
    require((word[0], word[12], word[41]) == ('0', '0', '1'), 'anchor pins fail')
    cycle = cert['monochromatic_odd_cycle']
    require(type(cycle) is list and all(type(v) is int and 0 <= v < 739 for v in cycle), 'bad cycle index')
    require(len(cycle) == 5 and len(set(cycle)) == 5, 'not a simple five-cycle')
    require(len({word[v] for v in cycle}) == 1, 'witness cycle is not monochromatic')
    return word, cycle


def check(cert, source_raw, cnf_raw, cycles_raw):
    word, obstruction = inspect_header(cert, source_raw, cnf_raw, cycles_raw)
    source = json.loads(source_raw)
    require(source['G1_endpoints'] == [0, 5], 'wrong endpoints')
    original_edges = {frozenset(e) for e in source['G1_edges']}
    require(len(original_edges) == 3985 and all(len(e) == 2 for e in original_edges), 'wrong source graph')
    edges = {frozenset(quotient(v) for v in e) for e in original_edges}
    require(len(edges) == 3983 and all(len(e) == 2 for e in edges), 'wrong quotient')
    require(all(frozenset((obstruction[i-1], v)) in edges for i, v in enumerate(obstruction)), 'cycle has a nonedge')
    original_cycle = cert['original_monochromatic_odd_cycle']
    require(len(original_cycle) == 5 and len(set(original_cycle)) == 5, 'bad original cycle')
    require([quotient(v) for v in original_cycle] == obstruction, 'original cycle map differs')
    require(all(frozenset((original_cycle[i-1], v)) in original_edges for i, v in enumerate(original_cycle)), 'original cycle has a nonedge')
    require(all(word[quotient(v)] == '0' for v in original_cycle), 'original cycle is not in zero part')
    # These triangle pins lose no four-colouring: rename the colours 00,01,10.
    require(all(frozenset(e) in edges for e in [(0, 12), (0, 41), (12, 41)]), 'anchor is not a triangle')
    frozen = json.loads(cycles_raw)
    require(frozen['quotient_labels'] == [i for i in range(740) if i != 5], 'wrong quotient labels')
    pins = [[-1], [-13], [42]]
    require(frozen['pins'] == pins, 'wrong stored pins')
    required_clauses = Counter(tuple(c) for c in pins)
    keys = set()
    histogram = Counter()
    for cycle in frozen['walks']:
        require(len(cycle) >= 3 and len(cycle) % 2 == 1 and len(set(cycle)) == len(cycle), 'not a simple odd cycle')
        require(all(type(v) is int and 0 <= v < 739 for v in cycle), 'invalid cycle label')
        require(all(frozenset((cycle[i-1], v)) in edges for i, v in enumerate(cycle)), 'saved cycle has a nonedge')
        key = tuple(sorted(cycle))
        require(key not in keys, 'duplicate cycle vertex set')
        keys.add(key)
        histogram[len(cycle)] += 1
        required_clauses[tuple(v + 1 for v in key)] += 1
        required_clauses[tuple(-v - 1 for v in key)] += 1
        require(len({word[v] for v in cycle}) == 2, 'a saved cycle is monochromatic')
    require(len(keys) == 147686, 'wrong saved cycle count')
    require(tuple(sorted(obstruction)) not in keys, 'obstruction already in frozen family')
    # A fresh adjacency intersection verifies the complete triangle inventory.
    neighbours = [set() for _ in range(739)]
    for edge in edges:
        a, b = tuple(edge)
        neighbours[a].add(b)
        neighbours[b].add(a)
    triangles = {(a, b, c) for a in range(739) for b in neighbours[a] if b > a
                 for c in neighbours[a] & neighbours[b] if c > b}
    require(triangles == {k for k in keys if len(k) == 3}, 'triangle inventory differs')
    actual = Counter()
    lines = cnf_raw.decode().splitlines()
    require(lines[0] == 'p cnf 739 295375', 'wrong DIMACS header')
    for line in lines[1:]:
        row = [int(s) for s in line.split()]
        require(row and row[-1] == 0 and all(1 <= abs(lit) <= 739 for lit in row[:-1]), 'malformed clause')
        clause = tuple(row[:-1])
        actual[clause] += 1
        require(any((word[abs(lit)-1] == '1') == (lit > 0) for lit in clause), 'SAT word violates a clause')
    require(actual == required_clauses, 'CNF differs from saved odd-cycle constraints')
    require(sum(actual.values()) == 295375, 'wrong clause count')
    return {'frozen_formula_satisfiable': True,
            'all_saved_cycles_valid_and_bichromatic': True,
            'clauses_directly_checked': sum(actual.values()), 'odd_cycles_checked': len(keys),
            'quotient_vertices': 739, 'quotient_edges': len(edges),
            'partition_sizes': [word.count('0'), word.count('1')],
            'unlisted_monochromatic_quotient_cycle': obstruction,
            'original_monochromatic_cycle': original_cycle,
            'partition_cannot_extend_to_four_colouring': True,
            'original_endpoint_forcing_decided': False,
            'graph_four_colourability_decided': False,
            'new_refinement_rounds': 0, 'record_improvement': False,
            'cnf_sha256': CNF_SHA, 'cycles_sha256': CYCLES_SHA,
            'boolean_word_sha256': digest(word.encode()),
            'cycle_lengths': dict(sorted(histogram.items()))}


def malformed_controls(cert, source_raw, cnf_raw, cycles_raw):
    cases = []
    bad = copy.deepcopy(cert); bad['variables'] = 738
    cases.append((bad, source_raw, cnf_raw, cycles_raw))
    bad = copy.deepcopy(cert); bad['boolean_word'] = '1' + bad['boolean_word'][1:]
    cases.append((bad, source_raw, cnf_raw, cycles_raw))
    bad = copy.deepcopy(cert); bad['monochromatic_odd_cycle'] = bad['monochromatic_odd_cycle'][:4]
    cases.append((bad, source_raw, cnf_raw, cycles_raw))
    bad = copy.deepcopy(cert); bad['monochromatic_odd_cycle'][0] = 739
    cases.append((bad, source_raw, cnf_raw, cycles_raw))
    cases.append((cert, source_raw + b' ', cnf_raw, cycles_raw))
    cases.append((cert, source_raw, cnf_raw + b' ', cycles_raw))
    cases.append((cert, source_raw, cnf_raw, cycles_raw + b' '))
    rejected = 0
    for case in cases:
        try:
            inspect_header(*case)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed control was accepted')
    return rejected


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frozen_directory', type=Path, help='Rebuilt or preserved frozen files outside the repository')
    args = parser.parse_args()
    cert = json.loads((here / 'certificate.json').read_text())
    source_raw = (here.parent / 'hadwiger_nelson_haugland2131_exact_reproduction/graph.json').read_bytes()
    cnf_raw = (args.frozen_directory / 'odd_cycles.cnf').read_bytes()
    cycles_raw = (args.frozen_directory / 'cycles.json').read_bytes()
    result = check(cert, source_raw, cnf_raw, cycles_raw)
    result['malformed_controls_rejected'] = malformed_controls(cert, source_raw, cnf_raw, cycles_raw)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
