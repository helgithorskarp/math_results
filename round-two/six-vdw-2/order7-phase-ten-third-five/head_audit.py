"""Independent literal clauses, exact-six gates and fourth-selection coverage."""
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


def head_fixed(k, background):
    require(k in range(7, 15), 'unsupported fourth selected index')
    anchors = {0, 1, 6, k}
    return {i: 1-background if i in anchors else background for i in range(44)
            if i in anchors or i == 43 or 2 <= i <= 5 or 6 < i < k}


def counter_check(rows, n, background):
    base = 44+2*n
    cells = {(i, k): base+(i*(i-1)//2 if i <= 7 else 7*(i-1)-21)+k
             for i in range(1, n+1) for k in range(1, min(i, 7)+1)}
    end = base+7*n-21
    require(set(cells.values()) == set(range(base+1, end+1)), 'incomplete counter cells')
    units = {(cells[n, 6],), (-cells[n, 7],)}
    require({row for row in rows if len(row) == 1} == units, 'wrong exact-six units')
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
                    'wrong seven-level gate truth relation')
            checked += 1
        accounted.update(local)
    require(accounted == rows, 'unaccounted counter clause')
    return end, checked


def tiny_controls():
    thresholds = exact = 0
    for m in range(1, 11):
        for bits in itertools.product((0, 1), repeat=m):
            for flip in (0, 1):
                cells = {}
                for i, value in enumerate(bits, 1):
                    for k in range(1, min(i, 7)+1):
                        a = cells.get((i-1, k), False)
                        b = True if k == 1 else cells[i-1, k-1]
                        cells[i, k] = bool(a or ((value ^ flip) and b))
                        require(cells[i, k] == (sum(x ^ flip for x in bits[:i]) >= k),
                                'tiny threshold differs')
                        thresholds += 1
                require((cells.get((m, 6), False) and not cells.get((m, 7), False))
                        == (sum(x ^ flip for x in bits) == 6), 'tiny exact-six differs')
                exact += 1
    return thresholds, exact


def cover_controls():
    checked = 0
    seen = set()
    for m in range(12, 18):
        for count in range(4, 8):
            for extras in itertools.combinations(range(7, m-1), count-3):
                chosen = (0, 1, 6)+extras
                if max((chosen[(i+1) % count]-chosen[i]) % m for i in range(count)) > 8:
                    continue
                selected = set(chosen)
                if any((i-1) % m not in selected and i in selected and (i+1) % m in selected
                       and not any((i+j) % m in selected for j in range(2, 7))
                       for i in range(m)):
                    continue
                fourth = chosen[3]
                require(chosen[:3] == (0, 1, 6) and fourth in range(7, 15),
                        'fourth selection escaped the proved background-run cover')
                for background in (0, 1):
                    bits = [int((i in selected) != bool(background)) for i in range(m)]
                    require(all(bits[i] == 1-background for i in (0, 1, 6, fourth))
                            and bits[-1] == background
                            and all(bits[i] == background for i in list(range(2, 6))+
                                    list(range(7, fourth))), 'lost a fourth-selection head')
                    seen.add((fourth, background))
                    checked += 1
    require(seen == {(k, b) for k in range(7, 15) for b in (0, 1)},
            'tiny controls miss one of the sixteen fourth-selection branches')
    return checked, sorted(seen)


def gauge_controls():
    checked = 0
    for m in range(2, 7):
        for bits in itertools.product((0, 1), repeat=2*m):
            phase = [bits[i] ^ bits[i+m] for i in range(m)]
            for r in range(2*m):
                rotated = [bits[(i+r) % (2*m)] ^ bits[r] for i in range(2*m)]
                require(rotated[0] == 0 and all(rotated[i+m] ==
                        rotated[i] ^ phase[(i+r) % m] for i in range(m)),
                        'scalar rotation or global color gauge lost an orientation')
                checked += 1
    return checked



def density_clauses(fixed, free, background):
    names = {i: 45+len(free)+j for j, i in enumerate(free)}
    rows = set()
    truth_inputs = 0
    for origin in range(44):
        positions = [(origin+j) % 44 for j in range(-1, 7)]
        wanted = [1-background, background, background]+[1-background]*5
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
            require(truth == implication, 'substituted density clause differs from exact antecedent')
            truth_inputs += 1
    return rows, truth_inputs



def strengthened_clause_controls():
    checked = 0
    for origin in range(44):
        positions = [(origin+j) % 44 for j in range(-1, 6)]
        for background in (0, 1):
            signs = [1, -1, -1, 1, 1, 1, 1]
            clause = [(i+1)*sign*(-1 if background else 1)
                      for i, sign in zip(positions, signs)]
            for bits in itertools.product((0, 1), repeat=7):
                assignment = dict(zip(positions, bits))
                selected = [bit ^ background for bit in bits]
                implication = bool(selected[0] or not selected[1] or not selected[2]
                                   or any(selected[3:]))
                truth = any(assignment[abs(v)-1] == (v > 0) for v in clause)
                require(truth == implication, 'wrong third-five clause or background sign')
                checked += 1
    return checked


def main(work):
    began = time.monotonic()
    pins()
    premise = pins()
    models = json.loads((work/'models.json').read_text())
    expected = [(k, b) for k in range(14, 6, -1) for b in (0, 1)]
    require([r['stem'] for r in models['records']] ==
            [f'density-k6-fourth-{k}-b-{b}' for k, b in expected], 'incomplete sixteen-case fourth-selection cover')
    require({p.name for p in work.glob('*.cnf')} ==
            {f'density-k6-fourth-{k}-b-{b}.cnf' for k, b in expected}, 'missing or extra model file')
    slots, supports = literal_field()
    records = []
    for record, (k, background) in zip(models['records'], expected):
        require(record['minimum_distance'] == 1 and record['third_selected_index'] == 6
                and record['fourth_selected_index'] == k
                and record['background'] == background and record['phase_K'] == (34 if background else 10)
                and record['free_selected_count'] == 6 and record['root57_color_cut'] is True
                and record['selected_run_start'] is True and record['next_phase_unfixed'] is True
                and record['no_adjacency_cut'] is False and record['conditional_successor_cut'] is False
                and record['adjacent_density_cut'] is True
                and record['density_lemma_graph'] == premise['density_graph']
                and record['density_lemma_source_commit'] == premise['density_source_commit'],
                'changed adjacent-branch semantics or imported false premise')
        fixed = head_fixed(k, background)
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
        require(n == len(free) == 42-k and record['free_phase_indices'] == free
                and k+1 in free, 'wrong free phase domain or forced next background')
        density, density_truth = density_clauses(fixed, free, background)
        require(record['density_clauses_after_substitution'] == len(density)
                and record['new_density_clauses'] == len(density-semantic) > 0,
                'missing or misstated added density clauses')
        semantic.update(density)
        cnf = work/(record['stem']+'.cnf')
        text = cnf.read_text().splitlines()
        variables = 23+9*n
        require(text[0].split() == ['p', 'cnf', str(variables), str(record['clauses'])]
                and record['variables'] == variables, 'wrong adjacent model dimension')
        rows = []
        for line in text[1:]:
            values = list(map(int, line.split()))
            require(values and values[-1] == 0 and all(1 <= abs(v) <= variables
                    for v in values[:-1]), 'invalid DIMACS row')
            rows.append(tuple(sorted(values[:-1])))
        counters = {row for row in rows if any(abs(v) > 44+2*n for v in row)}
        end, truth_rows = counter_check(counters, n, background)
        require(end == variables, 'wrong analytic cell labeling')
        require(Counter(rows) == Counter(list(semantic | counters)+[(-1,)])
                and len(rows) == record['clauses'] and sha(cnf) == record['cnf_sha256'],
                'full actual-field density-strengthened model audit differs')
        records.append(dict(stem=record['stem'], variables=variables, clauses=len(rows),
            cnf_sha256=sha(cnf), counter_truth_rows=truth_rows,
            substituted_density_truth_rows=density_truth,
            density_clauses_after_substitution=len(density),
            new_density_clauses=record['new_density_clauses'],
            free_phase_inputs_before_cuts=math.comb(n, 6)))
    thresholds, exact = tiny_controls()
    cover_inputs, tiny_branches = cover_controls()
    signed_rotations = gauge_controls()
    strengthened_rows = strengthened_clause_controls()
    result = dict(agent='six-vdw-2', role='researcher', status='EXACT_K10_DENSITY_K6_FOURTH16_AUDIT',
        records=records, literal_APs=375760, removed_zero_APs=4312, signed_supports=26488,
        tiny_threshold_cells=thresholds, tiny_exact_counts=exact,
        tiny_sixteen_fourth_case_cover_inputs=cover_inputs, tiny_branches=tiny_branches,
        signed_rotation_controls=signed_rotations,
        strengthened_clause_truth_rows=strengthened_rows,
        no_adjacency_cut=False, conditional_successor_cut=False, adjacent_density_cut=True,
        seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path = work/('audit-optimized.json' if not __debug__ else 'audit-normal.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
