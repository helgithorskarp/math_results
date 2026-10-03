"""Independent literal witness, mask-index and degree-identity validation.

Imports neither enumerator. Exact finite checks do not formalize PROOF.md.
"""
import argparse
import copy
import hashlib
import itertools
import json
import time
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def parameters(short):
    require(short in [(0, 1), (1, 2)], 'canonical carrier')
    counts = [3 if edge == short else 4 for edge in PAIRS]
    quotas = [sum(counts[i] for i, e in enumerate(PAIRS) if a in e)
              + (70 - 4 * [18, 19, 19, 19][a]) for a in range(4)]
    return quotas, [14 - 3 * value for value in counts]


def witness(short, supports, centers, stars, column_rule=True):
    short = tuple(short)
    D, capacities = parameters(short)
    require(len(supports) == len(centers) == 4, 'four columns')
    require(sum(centers) == 4 and all(type(x) is int and x >= 0 for x in centers),
            'four selected rows')
    require(all(type(x) is int and 0 <= x <= D[a] for a, x in enumerate(supports)),
            'support domains')
    require(supports[0] >= 4 and all(supports[a] >= 2 for a in [1, 2, 3]),
            'degree column bounds')
    require(all(centers[a] <= min(supports[a], D[a] - supports[a]) and
                (not centers[a] or supports[a] >= 5) for a in range(4)),
            'selected slot and excess bounds')
    require(len(stars) == 4, 'whole four-row witness')
    row_centers = [a for a in range(4) for _ in range(centers[a])]
    usage = [0] * 6
    for a, star in zip(row_centers, stars):
        require(all(type(i) is int and 0 <= i < 6 for i in star), 'literal edge ids')
        require(len(set(star)) == len(star), 'distinct row edges')
        require(len(star) == max(0, 8 - supports[a]), 'minimum relaxation demand')
        for i in star:
            require(a in PAIRS[i], 'row edge incidence')
            other = PAIRS[i][1] if PAIRS[i][0] == a else PAIRS[i][0]
            if column_rule:
                require(not (capacities[i] == 2 and other > 0 and supports[other] == 2),
                        'actual forbidden column edge')
            usage[i] += 1
    require(all(usage[i] <= capacities[i] for i in range(6)), 'six pair capacities')


def validate_witnesses(math, witnesses):
    triples = [[w['short'], w['N'], w['m']] for w in witnesses]
    require(triples == math['feasible_cases'], 'entire positive witness coverage')
    for w in witnesses:
        witness(w['short'], w['N'], w['m'], w['stars'])


def rejection(action, message):
    try:
        action()
    except ValueError as exc:
        require(str(exc) == message, 'intended semantic rejection: ' + str(exc))
    else:
        raise ValueError('damaged certificate accepted')


def main():
    parser = argparse.ArgumentParser()
    for name in ['literal', 'dual', 'expected', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'fresh verifier output')
    started, states = time.monotonic(), 0

    def guard():
        nonlocal states
        states += 1
        require(states <= 500000 and time.monotonic() - started < 20,
                'INCOMPLETE original finite-auditor guard; no absence')

    expected = json.loads(args.expected.read_text())
    literal = json.loads(args.literal.read_text())
    dual = json.loads(args.dual.read_text())
    for name, value, path in [('literal', literal, args.literal), ('dual', dual, args.dual)]:
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected['output_sha256'][name],
                'entire frozen program output: ' + name)
        require(value['agent'] == 'six-code-3' and value['role'] == 'researcher' and
                value['ordinary_bridges_formalized'] is False and
                value['independent_person_review'] is False and value['no_code_exclusion'] is True,
                'actual author and scope')
    math = literal['math']
    require(canonical(math) == canonical(dual['math']), 'all independent mathematical fields')
    require(hashlib.sha256(canonical(math)).hexdigest() == expected['whole_math_sha256'],
            'whole mathematical fingerprint')
    require(math['controls'] == expected['controls'], 'whole controls')
    require(math['total_cases'] == 199920 and math['minimum_relaxation_K'] == 17 and
            len(math['feasible_cases']) == 39 and len(math['carriers']) == 2,
            'entire declared finite scope')
    require(len({canonical(r) for r in math['feasible_cases']}) == 39, 'unique feasible records')
    compositions = sorted(m for m in itertools.product(range(5), repeat=4) if sum(m) == 4)
    seen, support_boxes, total = [], 0, 0
    for carrier, short in zip(math['carriers'], [(0, 1), (1, 2)]):
        D, L = parameters(short)
        require(carrier['short'] == list(short) and carrier['D'] == D and carrier['L'] == L,
                'independently rebuilt carrier')
        mask = bytes.fromhex(carrier['feasible_mask_hex'])
        case_number = 0
        for N in itertools.product(*(range(x + 1) for x in D)):
            support_boxes += 1
            for m in compositions:
                guard()
                require(case_number // 8 < len(mask), 'whole mask length')
                if mask[case_number // 8] & (1 << (case_number % 8)):
                    require(sum(N) >= 17, 'all feasible support bounds')
                    seen.append([list(short), list(N), list(m)])
                case_number += 1
        require(case_number == carrier['cases'] and len(mask) == (case_number + 7) // 8,
                'whole carrier mask size')
        if case_number % 8:
            require(mask[-1] >> (case_number % 8) == 0, 'zero padding bits')
        total += case_number
    require(total == 199920 and support_boxes == 5712 and len(compositions) == 35,
            'all support boxes and compositions')
    require(seen == math['feasible_cases'], 'every mask bit and positive record aligned')
    ws = literal['entire_literal_positive_witnesses']
    validate_witnesses(math, ws)
    control = math['controls']
    witness(control['short'], control['positive_N'], control['m'],
            literal['control_positive_stars'])
    witness(control['short'], control['proper_low_N'], control['m'],
            literal['control_counterfactual_stars'], column_rule=False)
    rejection(lambda: witness(control['short'], control['proper_low_N'], control['m'],
                              literal['control_counterfactual_stars']),
              'actual forbidden column edge')
    rejection(lambda: validate_witnesses(math, ws[:-1]), 'entire positive witness coverage')
    damaged = copy.deepcopy(ws[0])
    damaged['stars'][0][1] = damaged['stars'][0][0]
    rejection(lambda: witness(damaged['short'], damaged['N'], damaged['m'], damaged['stars']),
              'distinct row edges')

    # Every LOW vertex has degree one. With j LOW--LOW edges, the HIGH
    # degree sum is twice its internal edges plus 12-2j cross edges.
    degree_equalities = []
    degree_cases = 0
    for high_graph in range(1 << 10):
        for low_matching_edges in range(7):
            guard()
            high_degree_sum = 2 * high_graph.bit_count() + 12 - 2 * low_matching_edges
            if high_degree_sum == 32:
                degree_equalities.append([high_graph, low_matching_edges])
            degree_cases += 1
    require(degree_cases == 7168 and degree_equalities == [[1023, 0]],
            'all elementary HIGH degree identities')
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_EXACT_SUPPORT_CHECK',
                  cases=total, support_boxes=support_boxes, compositions=len(compositions),
                  feasible_relaxations=len(ws), minimum_relaxation_K=17,
                  entire_independent_masks_and_records_equal=True,
                  every_positive_whole_star_witness_valid=True, semantic_rejections=3,
                  degree_identity_cases=degree_cases, degree_equality=degree_equalities,
                  whole_math_sha256=expected['whole_math_sha256'],
                  ordinary_bridges_formalized=False, independent_person_review=False,
                  code_attainment=False, unrestricted_endpoint_improvement=False)
    args.output.write_bytes(canonical(result) + b'\n')
    print(json.dumps(dict(status=result['status'], cases=total, witnesses=len(ws),
                          guard_states=states,
                          output_sha256=hashlib.sha256(args.output.read_bytes()).hexdigest()),
                     sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
