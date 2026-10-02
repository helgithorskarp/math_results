"""Physical sets and the written case proof; no production bitsets imported."""
from argparse import ArgumentParser
from itertools import combinations_with_replacement
import json
from math import comb, gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def copy_blocks(next_label=0, blocks=()):
    if next_label == 7:
        yield blocks
        return
    for i in range(len(blocks)):
        yield from copy_blocks(next_label + 1,
                               blocks[:i] + (blocks[i] + (next_label,),) + blocks[i + 1:])
    if len(blocks) < 5:
        yield from copy_blocks(next_label + 1, blocks + ((next_label,),))


def loss(parts, masks):
    return sum(len(m) for m in masks) - sum(len(set().union(*(masks[i] for i in block)))
                                          for block in parts)


def compute():
    S = {t for t in range(180) if t % 9 != 6}
    X = set(range(0, 720, 4)) - set(range(6, 720, 9))
    need({4 * t for t in S} == X and len(S) == 160, 'physical candidate target differs')
    seven = (8, 3, 6, 12, 5, 10, 20)
    free = [d for d in range(2, 721) if 720 % d == 0 and d not in (2, 4)]
    mass = other = phase_controls = original7_controls = 0
    copy_targets = [{x for x in range(5040) if x % 720 in X and x % 7 == s} for s in range(7)]
    for d in free:
        e = d // gcd(d, 4)
        literal = [len(X & set(range(a, 720, d))) for a in range(d)]
        cap = (160 // e) if e % 3 else (180 // e)
        need(max(literal) == cap, 'original cofactor capacity differs')
        physical7 = [len(set(range(a, 5040, 7 * d)) & copy_targets[a % 7]) for a in range(7 * d)]
        need(max(physical7) == cap, 'original7d physical class capacity differs')
        original7_controls += len(physical7)
        for r in range(e):
            g = gcd(e, 9)
            removed = 180 // lcm(e, 9) if (r - 6) % g == 0 else 0
            need(literal[(4 * r) % d] == 180 // e - removed, 'CRT phase count differs')
            phase_controls += 1
        mass += cap
        if d not in seven:
            other += cap
    need(mass == 600 and other == 244, 'resource inventory differs')
    masks = {(e, r): {t for t in S if t % e == r}
             for e in (2, 3, 5) for r in range(e)}
    allocations = tuple(copy_blocks())
    need(len(allocations) == 855 and len(set(allocations)) == 855, 'copy partition census differs')
    representative_losses = {}
    for C in ((0, 0, 0), (0, 0, 1), (0, 1, 1)):
        selected = [masks[2, 0]] + [masks[3, 1]] * 3 + [masks[5, c] for c in C]
        representative_losses[str(C)] = min(loss(blocks, selected) for blocks in allocations)
    need(representative_losses == {'(0, 0, 0)': 24, '(0, 0, 1)': 12, '(0, 1, 1)': 12},
         'literal copy-overlap minima differ from the pigeonhole proof')
    upper = {h: 0 for h in range(115, 121)}
    cases = {'two_or_three_zero_A': 0, 'one_zero_A': 0, 'mixed_nonzero_A': 0,
             'common_A_one_C': 0, 'common_A_two_C': 0, 'common_A_three_C': 0}
    profiles = 0
    for b in range(2):
        for A in combinations_with_replacement(range(3), 3):
            for C in combinations_with_replacement(range(5), 3):
                profiles += 1
                selected = [masks[2, b]] + [masks[3, a] for a in A] + [masks[5, c] for c in C]
                P = sum(len(s) for s in selected)
                L = len(set().union(*selected))
                z = A.count(0)
                delta = 0
                if z >= 2:
                    case = 'two_or_three_zero_A'
                    need(P <= 316, 'multiple zero-A capacity bound fails')
                elif z == 1:
                    case = 'one_zero_A'
                    need(P <= 336 and L >= 130, 'one zero-A support bound fails')
                elif len(set(A)) > 1:
                    case = 'mixed_nonzero_A'
                    need(P == 356 and L >= 140, 'mixed A support bound fails')
                else:
                    r = len(set(C))
                    case = ('common_A_one_C', 'common_A_two_C', 'common_A_three_C')[r - 1]
                    need(P == 356 and L == 110 + 10 * r, 'common A support count fails')
                    delta = (24, 12, 0)[r - 1]
                    # All nonzero intersections used by the copy-overlap
                    # proof are physical, independent of selected phases.
                    B, Amask = selected[0], selected[1]
                    need(len(B & Amask) == 30, 'B/A intersection differs')
                    for Cmask in selected[4:]:
                        need(len(Amask & Cmask) == 12 and len(B & Cmask) == 16 and
                             len(B & Amask & Cmask) == 6, 'A/B/C intersection differs')
                    for i in range(4, 7):
                        for j in range(i + 1, 7):
                            need(len(selected[i] & selected[j]) == (32 if C[i - 4] == C[j - 4] else 0),
                                 'C repeated/distinct intersection differs')
                cases[case] += 1
                for h in upper:
                    bound = P - delta - max(0, L - h)
                    need(bound <= h + 216, 'written seven-resource bound fails')
                    upper[h] = max(upper[h], bound)
    need(profiles == 700 and sum(cases.values()) == profiles, 'phase cases do not partition the domain')
    # Sharpness concerns ONLY this selected-seven relaxation. It is not a
    # first-stage or twenty-nine-resource tail completion witness.
    chosen = [masks[2, 0]] + [masks[3, 1]] * 3 + [masks[5, c] for c in (0, 1, 2)]
    blocks = ((0,), (1,), (2,), (3,), (4, 5, 6))
    unions = [set().union(*(chosen[i] for i in block)) for block in blocks]
    multiplicities = {t: sum(t in Q for Q in unions) for t in S}
    scores = []
    for h in range(115, 121):
        K = set(sorted(S, key=lambda t: (-multiplicities[t], t))[:h])
        score = sum(len(K & Q) for Q in unions)
        need(score == upper[h] == h + 216, 'physical relaxation sharpness differs')
        scores.append({'holes': h, 'maximum_hits': score})
    for row in scores[1:]:
        need(row['maximum_hits'] + other < 5 * row['holes'], 'strict hole cap fails')
    return {'candidate_target_size': len(S), 'free_resource_mass': mass,
            'other_twenty_resource_mass': other,
            'canonical_phase_multisets': profiles, 'canonical_copy_partitions': len(allocations),
            'phase_partition_cases': profiles * len(allocations), 'necessary_hole_upper_bound': 115,
            'selected_seven_top_scores': scores, 'physical_effective_phase_controls': phase_controls,
            'original7d_physical_phase_controls': original7_controls,
            'written_phase_case_counts': cases, 'literal_representative_overlap_minima': representative_losses,
            'tail_completion_asserted': False, 'global_L_min_8_bound_changed': False}


def validate(result, expected):
    for key, value in expected.items():
        need(key in result and result[key] == value, 'frozen expected field differs: ' + key)


def main():
    parser = ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = compute()
    validate(result, json.loads((HERE / 'expected.json').read_text()))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
