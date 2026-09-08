"""Definition-level audit: intersect all four G49 images in every outer case."""
from collections import Counter
import json
from pathlib import Path
import model

ROOT = Path(__file__).resolve().parent


def audit():
    g40, g49, pairs, _, certificate = model.inputs()
    essential = certificate['g40']['essential']
    counts = Counter()
    case_counts = Counter()
    cases = 0
    for choices, outer, mapped_core in model.outer_cases():
        first_swap, first_reflect, side, second_swap, second_reflect = choices
        x = g40[1]
        ys = model.spindle_targets(x)
        hosts = (model.put_g40(g40, x, first_swap, first_reflect),
                 model.put_g40(g40, ys[side], second_swap, second_reflect))
        direct_core = set(outer)
        for host in hosts:
            for index in essential:
                i, j = pairs[index]
                copies = model.g49_attachment_sets(g49, host[i], host[j])
                counts[len(set.intersection(*(set(copy) for copy in copies)))] += 1
                direct_core.update(set.intersection(*(set(copy) for copy in copies)))
        if direct_core != mapped_core:
            raise ValueError('mapped/direct kernel disagreement')
        case_counts[len(direct_core)] += 1
        cases += 1
    result = {'verified': True, 'outer_cases': cases,
              'direct_pair_intersections': 96 * cases,
              'pair_intersection_size_histogram': {str(k): v for k, v in sorted(counts.items())},
              'direct_unavoidable_order_histogram': {str(k): v for k, v in sorted(case_counts.items())}}
    expected = json.loads((ROOT / 'direct_expected.json').read_text())
    if result != expected:
        raise ValueError('direct-audit expected mismatch')
    return result


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
