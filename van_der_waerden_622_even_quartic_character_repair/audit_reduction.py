"""Capped arithmetic audits supporting the written quartic normalization.

These checks do not replace the symbolic coverage proof. Parameters mode
covers all(A,B) in five disjoint chunks. No polynomial or word enumeration
outside the stated finite parameter domains is asserted.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import resource
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(index):
    if index < 3:
        return [(0, 1, 11)[index], 0, 0, 0, 1]
    if index < 314:
        return [index - 3, 0, 1, 0, 1]
    return [index - 314, 0, 11, 0, 1]


def audit_field():
    squares = {pow(u, 2, 311) for u in range(1, 311)}
    fourths = {pow(u, 4, 311) for u in range(1, 311)}
    require(len(squares) == 155 and squares == fourths and 11 not in squares, 'power classes')
    pairs, lifts = 0, 0
    for multiplier in range(1, 311):
        for value in range(311):
            left = pow(multiplier * value % 311, 155, 311)
            right = pow(multiplier, 155, 311) * pow(value, 155, 311) % 311
            require(left == right, 'character multiplicativity')
            pairs += 1
    for u in range(1, 311):
        M = u if u % 2 else u + 311
        require(M % 311 == u and M % 2 == 1 and math.gcd(M, 622) == 1, 'odd CRT unit')
        for v in range(311):
            V = v if v % 2 == 0 else v + 311
            require(V % 311 == v and V % 2 == 0, 'even CRT shift')
            lifts += 1
    cases = pairs + lifts + 2 * 310 + 311 + 3
    require(cases <= 200000, 'case cap')
    return {'status': 'QUARTIC_FIELD_POWER_CHARACTER_AND_CRT_AUDIT_PASSED',
            'character_parameter_pairs': pairs, 'CRT_parameter_pairs': lifts,
            'square_and_fourth_power_image_size': 155, 'nonsquare_representative': 11,
            'conservative_combined_cases': cases}


def audit_shift():
    pairs = 0
    for alpha in range(1, 311):
        for beta in range(311):
            v = -beta * pow(4 * alpha % 311, -1, 311) % 311
            require((4 * alpha * v + beta) % 311 == 0, 'quartic cubic-term cancellation')
            pairs += 1
    return {'status': 'ALL_QUARTIC_LEADING_AND_CUBIC_COEFFICIENT_SHIFT_PAIRS_PASSED',
            'leading_cubic_coefficient_pairs': pairs, 'conservative_combined_cases': pairs}


def audit_parameters(start, count):
    require(0 <= start < 311 and 1 <= count <= 64 and start + count <= 311, 'parameter range')
    square_root, fourth_root = {}, {}
    for u in range(1, 311):
        square_root.setdefault(u * u % 311, u)
        fourth_root.setdefault(pow(u, 4, 311), u)
    require(set(square_root) == set(fourth_root) and len(square_root) == 155, 'power images')
    pairs, indexes = 0, set()
    for A in range(start, start + count):
        for B in range(311):
            if A:
                delta = 1 if A in square_root else 11
                u = square_root[A * pow(delta, -1, 311) % 311]
                constant = B * pow(pow(u, 4, 311), -1, 311) % 311
                index = (3 if delta == 1 else 314) + constant
            elif B:
                delta = 1 if B in fourth_root else 11
                u = fourth_root[B * pow(delta, -1, 311) % 311]
                index = 1 if delta == 1 else 2
            else:
                u, index = 1, 0
            require(1 <= u <= 310 and 0 <= index < 625, 'normalization domain')
            Q = canonical(index)
            normalized = [B * pow(pow(u, 4, 311), -1, 311) % 311,
                          0, A * pow(u * u % 311, -1, 311) % 311, 0, 1]
            require(Q == normalized, 'exact normalized coefficient identity')
            original = [B, 0, A, 0, 1]
            restored = [pow(u, 4, 311) * q * pow(pow(u, j, 311), -1, 311) % 311
                        for j, q in enumerate(Q)]
            require(restored == original, 'scalar and substitution restoration')
            pairs += 1
            indexes.add(index)
    cases = 8 * pairs + 2 * 310 + 1
    require(cases <= 200000, 'case cap')
    return {'status': 'EXACT_EVEN_QUARTIC_TWO_PARAMETER_NORMALIZATION_SLICE_PASSED',
            'A_start_inclusive': start, 'A_stop_exclusive': start + count,
            'AB_parameter_pairs': pairs, 'canonical_indexes_reached': sorted(indexes),
            'conservative_combined_cases': cases}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['field', 'shift', 'parameters'], required=True)
    parser.add_argument('--start', type=int)
    parser.add_argument('--count', type=int)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'output exists')
    began = time.monotonic()
    if args.mode == 'field':
        result = audit_field()
    elif args.mode == 'shift':
        result = audit_shift()
    else:
        require(args.start is not None and args.count is not None, 'parameter slice required')
        result = audit_parameters(args.start, args.count)
    result.update(agent='six-vdw-1', role='researcher', checked_at=datetime.now(timezone.utc).isoformat(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  seconds=time.monotonic() - began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  threads=1, hard_child_seconds=30,
                  exhaustive_all_polynomial_coefficients_claim=False,
                  symbolic_proof_still_required=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'conservative_combined_cases', 'seconds']}), flush=True)


if __name__ == '__main__':
    main()
