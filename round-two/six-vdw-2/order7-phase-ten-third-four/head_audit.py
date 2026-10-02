"""Definition-level field, heterogeneous counter, rule and eight-head audits."""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import resource
import time

from common import pins, require, sha, endpoint_auditor
old = endpoint_auditor()
literal_field, expected_clauses = old.literal_field, old.expected_clauses


def head_fixed(m, background):
    require(m in range(7, 11), 'unsupported fifth selected index')
    return {i: 1-background if (i in (0, 1, 5, 6, m) or (m == 10 and i == 11))
            else background for i in range(44)
            if i in (0, 1, 5, 6, m, 43) or 2 <= i <= 4 or 6 < i < m
            or (m == 10 and i == 11)}


def counter_check(rows, n, background, exact):
    require(exact in (4, 5), 'wrong heterogeneous remainder')
    base, levels = 44+2*n, exact+1
    cells = {(i, k): base+(i*(i-1)//2 if i <= levels
                            else levels*(i-1)-levels*(levels-1)//2)+k
             for i in range(1, n+1) for k in range(1, min(i, levels)+1)}
    end = base+levels*n-levels*(levels-1)//2
    require(set(cells.values()) == set(range(base+1, end+1)), 'incomplete counter cells')
    units = {(cells[n, exact],), (-cells[n, levels],)}
    require({row for row in rows if len(row) == 1} == units, 'wrong heterogeneous exact-count units')
    accounted, checked = set(units), 0
    for (i, k), output in cells.items():
        a = cells.get((i-1, k), False)
        b = True if k == 1 else cells[i-1, k-1]
        value = (44+n+i)*(-1 if background else 1)
        local = {row for row in rows if len(row) > 1 and max(map(abs, row)) == output}
        domain = {abs(v) for v in (a, b, value, output) if not isinstance(v, bool)}
        require(local and all(set(map(abs, row)) <= domain for row in local),
                'wrong gate domain or missing output')
        for bits in itertools.product((0, 1), repeat=len(domain)):
            assignment = dict(zip(sorted(domain), bits))
            def ev(v):
                return v if isinstance(v, bool) else assignment[abs(v)] ^ int(v < 0)
            relation = bool(assignment[output]) == bool(ev(a) or (ev(value) and ev(b)))
            require(all(any(ev(v) for v in row) for row in local) == relation,
                    'wrong heterogeneous gate truth relation')
            checked += 1
        accounted.update(local)
    require(accounted == rows, 'unaccounted counter clause')
    return end, checked


def tiny_controls():
    thresholds = exact_inputs = 0
    for remainder in (4, 5):
        for length in range(1, 11):
            for bits in itertools.product((0, 1), repeat=length):
                for flip in (0, 1):
                    cells = {}
                    for i, value in enumerate(bits, 1):
                        for k in range(1, min(i, remainder+1)+1):
                            a = cells.get((i-1, k), False)
                            b = True if k == 1 else cells[i-1, k-1]
                            cells[i, k] = bool(a or ((value ^ flip) and b))
                            require(cells[i, k] == (sum(x ^ flip for x in bits[:i]) >= k),
                                    'tiny threshold differs')
                            thresholds += 1
                    require((cells.get((length, remainder), False)
                             and not cells.get((length, remainder+1), False))
                            == (sum(x ^ flip for x in bits) == remainder),
                            'tiny heterogeneous exact count differs')
                    exact_inputs += 1
    return thresholds, exact_inputs


def cover_controls():
    checked, seen = 0, set()
    for length in range(12, 19):
        for count in range(5, 10):
            for extras in itertools.combinations(range(7, length-1), count-4):
                chosen = (0, 1, 5, 6)+extras
                selected = set(chosen)
                if any(all((i+j) % length not in selected for j in range(8))
                       for i in range(length)):
                    continue
                good = True
                for origin in range(length):
                    if ((origin-1) % length not in selected and origin in selected
                            and (origin+1) % length in selected):
                        if not any((origin+j) % length in selected for j in range(2, 6)):
                            good = False
                        if (all((origin+j) % length not in selected for j in (2, 3, 4))
                                and not all((origin+j) % length in selected for j in (5, 6))):
                            good = False
                if not good:
                    continue
                fifth = chosen[4]
                require(fifth in range(7, 11), 'fifth escaped the parent-at-five cover')
                require(fifth != 10 or 11 in selected, 'missing pair-at-five sixth anchor')
                for background in (0, 1):
                    bits = [int((i in selected) != bool(background)) for i in range(length)]
                    fixed = head_fixed(fifth, background)
                    require(bits[-1] == background and all(bits[i] == value
                            for i, value in fixed.items() if i != 43),
                            'lost a heterogeneous fifth-selection head')
                    seen.add((fifth, background))
                    checked += 1
    require(seen == {(m, b) for m in range(7, 11) for b in (0, 1)},
            'tiny controls miss an eight-case branch')
    return checked, sorted(seen)


def gauge_controls():
    checked = 0
    for length in range(2, 7):
        for bits in itertools.product((0, 1), repeat=2*length):
            phase = [bits[i] ^ bits[i+length] for i in range(length)]
            for offset in range(2*length):
                rotated = [bits[(i+offset) % (2*length)] ^ bits[offset]
                           for i in range(2*length)]
                require(rotated[0] == 0 and all(rotated[i+length] ==
                        rotated[i] ^ phase[(i+offset) % length] for i in range(length)),
                        'scalar rotation or global gauge lost an orientation')
                checked += 1
    return checked


def rule_clauses(fixed, free, background, offsets):
    require(offsets in ((-1, 0, 1, 2, 3, 4, 5), (-1, 0, 1, 2, 3, 4, 6)),
            'unproved conditional rule')
    names = {i: 45+len(free)+j for j, i in enumerate(free)}
    rows, truth_inputs = set(), 0
    for origin in range(44):
        positions = [(origin+j) % 44 for j in offsets]
        wanted = [1-background, background, background]+[1-background]*4
        true_constant = any(i in fixed and fixed[i] == value
                            for i, value in zip(positions, wanted))
        row = None if true_constant else tuple(sorted({names[i]*(1 if value else -1)
                        for i, value in zip(positions, wanted) if i not in fixed}))
        if row is not None:
            rows.add(row)
        domain = sorted({names[i] for i in positions if i not in fixed})
        for values in itertools.product((0, 1), repeat=len(domain)):
            assignment = dict(zip(domain, values))
            phase = [fixed[i] if i in fixed else assignment[names[i]] for i in positions]
            selected = [value != background for value in phase]
            implication = bool(selected[0] or not selected[1] or not selected[2]
                               or any(selected[3:]))
            truth = row is None or any(assignment[abs(v)] == (v > 0) for v in row)
            require(truth == implication, 'substituted rule differs from antecedent and consequence')
            truth_inputs += 1
    return rows, truth_inputs



def third_four_clause_controls():
    checked = 0
    for origin in range(44):
        positions = [(origin+j) % 44 for j in range(-1, 5)]
        for background in (0, 1):
            signs = [1, -1, -1, 1, 1, 1]
            row = [(position+1)*sign*(-1 if background else 1)
                   for position, sign in zip(positions, signs)]
            for bits in itertools.product((0, 1), repeat=6):
                assignment = dict(zip(positions, bits))
                selected = [bit ^ background for bit in bits]
                implication = bool(selected[0] or not selected[1] or not selected[2]
                                   or any(selected[3:]))
                require(any(assignment[abs(v)-1] == (v > 0) for v in row) == implication,
                        'wrong six-literal third-four conclusion')
                checked += 1
    return checked


def main(work):
    began = time.monotonic()
    pins()
    premise = pins()
    models = json.loads((work/'models.json').read_text())
    expected = [(m, b) for m in range(10, 6, -1) for b in (0, 1)]
    require(models['producer_sha256'] == sha(Path(__file__).with_name('head_generate.py')),
            'changed model producer')
    require([r['stem'] for r in models['records']] ==
            [f'pair-k5-fifth-{m}-b-{b}' for m, b in expected], 'incomplete eight-case fifth-selection cover')
    require({p.name for p in work.glob('*.cnf')} ==
            {f'pair-k5-fifth-{m}-b-{b}.cnf' for m, b in expected}, 'missing or extra model file')
    slots, supports = literal_field()
    records = []
    for record, (m, background) in zip(models['records'], expected):
        exact = 4 if m == 10 else 5
        require(record['minimum_distance'] == 1 and record['third_selected_index'] == 5
                and record['fourth_selected_index'] == 6 and record['fifth_selected_index'] == m
                and record['background'] == background and record['phase_K'] == (34 if background else 10)
                and record['free_selected_count'] == exact and record['selected_anchor_count'] == 10-exact
                and record['root57_color_cut'] is True and record['selected_run_start'] is True
                and record['extra_selected11'] is (m == 10)
                and record['next_free_phase'] == (12 if m == 10 else m+1)
                and record['no_adjacency_cut'] is False and record['conditional_successor_cut'] is False
                and record['adjacent_density_cut'] is True and record['pair_following_cut'] is True
                and record['density_lemma_graph'] == premise['density_graph']
                and record['density_lemma_source_commit'] == premise['density_source_commit']
                and record['pair_lemma_graph'] == premise['pair_graph']
                and record['pair_lemma_source_commit'] == premise['pair_source_commit'],
                'changed heterogeneous head semantics or false premise')
        fixed = head_fixed(m, background)
        free = [i for i in range(44) if i not in fixed]
        semantic, n = expected_clauses(slots, supports, fixed, 1)
        index = {i: j for j, i in enumerate(free)}
        def actual_literal(point):
            i, side = slots[point]
            if not side:
                return i+1
            return (i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i]
        for origin in range(88):
            point = pow(3, origin, 617)
            values = {actual_literal(point*pow(57, j, 617) % 617) for j in range(8)}
            if not any(-v in values for v in values):
                semantic.add(tuple(sorted(values)))
                semantic.add(tuple(sorted(-v for v in values)))
        require(n == len(free) == (31 if m == 10 else 42-m)
                and record['free_phase_indices'] == free
                and record['next_free_phase'] in free,
                'wrong free phase domain or false next neighbor')
        density, density_truth = rule_clauses(fixed, free, background, (-1, 0, 1, 2, 3, 4, 5))
        pair, pair_truth = rule_clauses(fixed, free, background, (-1, 0, 1, 2, 3, 4, 6))
        require(record['density_clauses_after_substitution'] == len(density)
                and record['new_density_clauses'] == len(density-semantic) > 0
                and record['pair_clauses_after_substitution'] == len(pair)
                and record['new_pair_clauses'] == len(pair-(semantic | density)) > 0,
                'missing or misstated necessary rule clauses')
        semantic.update(density | pair)
        cnf = work/(record['stem']+'.cnf')
        text = cnf.read_text().splitlines()
        variables = 34+7*n if m == 10 else 29+8*n
        require(text[0].split() == ['p', 'cnf', str(variables), str(record['clauses'])]
                and record['variables'] == variables, 'wrong heterogeneous model dimension')
        rows = []
        for line in text[1:]:
            values = list(map(int, line.split()))
            require(values and values[-1] == 0 and all(1 <= abs(v) <= variables
                    for v in values[:-1]), 'invalid DIMACS row')
            rows.append(tuple(sorted(values[:-1])))
        counters = {row for row in rows if any(abs(v) > 44+2*n for v in row)}
        end, truth_rows = counter_check(counters, n, background, exact)
        require(end == variables, 'wrong analytic counter labeling')
        require(Counter(rows) == Counter(list(semantic | counters)+[(-1,)])
                and len(rows) == record['clauses'] and sha(cnf) == record['cnf_sha256'],
                'full actual-field pair-strengthened model audit differs')
        records.append(dict(stem=record['stem'], variables=variables, clauses=len(rows),
            cnf_sha256=sha(cnf), counter_truth_rows=truth_rows,
            substituted_density_truth_rows=density_truth, substituted_pair_truth_rows=pair_truth,
            density_clauses_after_substitution=len(density), pair_clauses_after_substitution=len(pair),
            new_density_clauses=record['new_density_clauses'], new_pair_clauses=record['new_pair_clauses'],
            free_selected_count=exact, free_phase_inputs_before_cuts=math.comb(n, exact)))
    thresholds, exact_inputs = tiny_controls()
    cover_inputs, tiny_branches = cover_controls()
    signed_rotations = gauge_controls()
    conclusion_rows = third_four_clause_controls()
    result = dict(agent='six-vdw-2', role='researcher', status='EXACT_K10_PAIR_K5_FIFTH8_AUDIT',
        records=records, literal_APs=375760, removed_zero_APs=4312, signed_supports=26488,
        tiny_threshold_cells=thresholds, tiny_exact_counts=exact_inputs,
        tiny_eight_fifth_case_cover_inputs=cover_inputs, tiny_branches=tiny_branches,
        signed_rotation_controls=signed_rotations,
        third_four_clause_truth_rows=conclusion_rows, counter_exact_counts_tested=[4, 5],
        no_adjacency_cut=False, conditional_successor_cut=False,
        adjacent_density_cut=True, pair_following_cut=True,
        seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path = work/('audit-optimized.json' if not __debug__ else 'audit-normal.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
