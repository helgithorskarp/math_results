#!/usr/bin/env python3
"""Audit actual cyclic tuples, then strictly check a RUP model extension.

The credited checker supplies only its positive-hint unit-propagation kernel.
This extension is deliberately not a refutation and contains no empty clause.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import time
from pathlib import Path

CHECKER_SHA256 = '55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def expected_models(lam):
    q = 103
    require(2 <= lam < q, 'Bad hole normalization')
    holes = {0, 1, lam}
    regular = tuple(x for x in range(q) if x not in holes)
    pairs = list(itertools.combinations(regular, 2))
    labels = {pair: i+1 for i, pair in enumerate(pairs)}
    root = regular[0]
    base = set()
    for x,y in itertools.combinations(regular[1:], 2):
        ids = labels[(root,x)], labels[(root,y)], labels[(x,y)]
        for bits in itertools.product((0,1), repeat=3):
            if sum(bits) % 2:
                base.add(tuple(sorted(v if b == 0 else -v for v,b in zip(ids,bits))))
    cycle_count = len(base)
    length = 6*q
    groups = {}
    skipped = retained = same_field = 0
    for step in range(1,length):
        for start in range(length):
            residues = tuple((start+j*step) % length for j in range(7))
            fields = tuple(t % q for t in residues)
            if any(x in holes for x in fields):
                skipped += 1
                continue
            retained += 1
            word = tuple(int(t % 6 >= 3) for t in residues)
            if len(set(fields)) == 1:
                require(len(set(word)) == 2, 'Bad same-column phase word')
                same_field += 1
                continue
            require(len(set(fields)) == 7, 'Unexpected repeated field tuple')
            if fields[::-1] < fields:
                fields, word = fields[::-1], word[::-1]
            words = groups.setdefault(fields,set())
            words.add(word)
            words.add(tuple(1-x for x in word))
    forbidden = set()
    for word in itertools.product((0,1), repeat=7):
        parities = {word[j]^word[j+3] for j in range(4)}
        if len(parities) == 1:
            forbidden.add(word)
    require(len(forbidden) == 16, 'Bad seven-word parity truth table')
    ladders = set()
    for fields, words in groups.items():
        require(words == forbidden, 'Actual cyclic words do not match both ladders')
        row = tuple(sorted(labels[tuple(sorted((fields[j],fields[j+3])))] for j in range(4)))
        require(len(set(row)) == 4, 'Bad ladder domain')
        ladders.add(row)
        base.add(row)
        base.add(tuple(sorted(-x for x in row)))
    cores = set()
    end_pairs = list(itertools.combinations(range(q),2))
    inv2, inv4, inv6 = (pow(d,-1,q) for d in (2,4,6))
    seven_by_endpoints = {}
    for first,last in end_pairs:
        step = (last-first)*inv6 % q
        seven_by_endpoints[first,last] = frozenset((first+j*step) % q for j in range(7))
        radius = (last-first)*inv4 % q
        center = (first+last)*inv2 % q
        if any((center+j*radius) % q in holes for j in range(-2,3)):
            continue
        core = {(center+j*radius) % q for j in range(-4,5)}
        core.update((center+j*radius*inv2) % q for j in (-3,-1,1,3))
        require(len(core) == 13, 'Bad core endpoint construction')
        cores.add(tuple(sorted(core-holes)))
    cuts = set()
    kernel = set()
    core_endpoint_tests = 0
    for core in cores:
        row = tuple(labels[(core[0],x)] for x in core[1:])
        cuts.add(row)
        support = frozenset(core)
        contains = False
        for endpoints in itertools.combinations(core,2):
            core_endpoint_tests += 1
            if seven_by_endpoints[endpoints] <= support:
                contains = True
        if not contains:
            kernel.add(row)
    compressed = base | kernel
    full = base | cuts
    metadata = {'lambda': lam, 'variables': len(pairs), 'root': root,
                'root_cycle_clauses': cycle_count, 'seven_ladders': len(ladders),
                'all_actual_cyclic_pairs': length*(length-1), 'retained_cyclic_pairs': retained,
                'skipped_cyclic_pairs': skipped, 'same_field_mixed_pairs': same_field,
                'all_seed_endpoint_pairs': len(end_pairs), 'all_core_endpoint_tests': core_endpoint_tests,
                'retained_kernel_cuts': len(kernel), 'derived_local_cuts_required': len(cuts)-len(kernel)}
    return compressed, full, metadata


def load_checker(path):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == CHECKER_SHA256, 'Changed credited strict checker pin')
    spec = importlib.util.spec_from_file_location('credited_rup_kernel', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_extension(directory, lam, checker_path):
    started = time.monotonic()
    checker = load_checker(checker_path)
    compressed, full, metadata = expected_models(lam)
    cnf = directory/'compressed.cnf'
    target = directory/'full.cnf'
    proof = directory/'extension.lrat'
    n, count, active = checker.read_cnf(cnf)
    target_n, target_count, target_rows = checker.read_cnf(target)
    require(n == target_n == 4950, 'Changed pair domain')
    require(count == len(compressed) and set(active.values()) == compressed, 'Compressed model differs from actual/endpoint audit')
    require(target_count == len(full) and set(target_rows.values()) == full, 'Full target model differs from actual/endpoint audit')
    for row in itertools.chain(active.values(),target_rows.values()):
        require(row == tuple(sorted(set(row))) and all(-x not in row for x in row), 'Noncanonical model clause')
    require(compressed <= full, 'Full model does not retain every compressed input row')
    maximum = count
    additions = hints_used = 0
    with proof.open() as stream:
        for number,line in enumerate(stream,1):
            tokens = list(map(int,line.split()))
            require(len(tokens) >= 4 and tokens.count(0) == 2 and tokens[-1] == 0, 'Malformed addition at line '+str(number))
            cid = tokens[0]
            split = tokens.index(0)
            clause, hints = tokens[1:split], tokens[split+1:-1]
            require(cid > maximum and cid not in active, 'Nonincreasing/duplicate addition ID')
            require(clause and clause == sorted(set(clause)) and all(-x not in clause for x in clause), 'Empty/noncanonical/tautological extension clause')
            require(all(1 <= abs(x) <= n for x in clause), 'Extension literal outside pair domain')
            require(hints and all(h > 0 for h in hints), 'Nonpositive/empty proof hint domain')
            hints_used += checker.check_addition(clause,hints,active)
            active[cid] = tuple(clause)
            maximum = cid
            additions += 1
    require(full <= set(active.values()), 'Some full-model target clauses are not derived')
    require(not any(not row for row in active.values()), 'Unexpected refutation')
    return {'status': 'EXACT_POSITIVE_RUP_MODEL_EQUIVALENCE_NO_REFUTATION', **metadata,
            'compressed_clauses': count, 'full_clauses': target_count,
            'checked_additions': additions, 'propagation_hints_checked': hints_used,
            'compressed_sha256': hashlib.sha256(cnf.read_bytes()).hexdigest(),
            'full_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
            'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
            'checker_sha256': CHECKER_SHA256, 'empty_clause_checked': False,
            'mathematical_exclusion_claimed': False, 'native_solver_invoked': False,
            'seconds': time.monotonic()-started}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--lambda', dest='lam', type=int, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check_extension(args.directory,args.lam,args.checker)
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
