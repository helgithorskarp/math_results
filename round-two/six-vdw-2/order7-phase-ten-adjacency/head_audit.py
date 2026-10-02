"""Independent actual-field clauses, exact-six gates and fourteen-case coverage."""
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
    require(k in range(7, 14), 'unsupported fourth selected index')
    anchors = {0, 2, 5, k}
    return {i: 1-background if i in anchors else background for i in range(44)
            if i in anchors or 5 < i < k or
            any(min((i-x) % 44, (x-i) % 44) == 1 for x in anchors)}


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
    local = cover = 0
    seen = set()
    for background in (0, 1):
        for bits in itertools.product((0, 1), repeat=4):
            selected = [value != background for value in bits]
            forbidden = bits == (1-background, 1-background, background, background)
            require((not (selected[0] and selected[1]) or selected[2] or selected[3])
                    == (not forbidden), 'unsubstituted successor formula differs')
            local += 1
    # Literal subsets of short cyclic domains, without importing any generator.
    # These finite controls supplement the written 44-cycle coverage argument.
    for m in range(12, 18):
        for count in range(4, min(m//2, 6)+1):
            for tail in itertools.combinations(range(1, m), count-1):
                chosen = (0,)+tail
                gaps = [(chosen[(i+1) % count]-chosen[i]) % m for i in range(count)]
                if min(gaps) < 2 or max(gaps) > 8:
                    continue
                if any(g == 2 and gaps[(i+1) % count] not in (2, 3)
                       for i, g in enumerate(gaps)):
                    continue
                for root in range(count):
                    if gaps[root] != 2 or gaps[(root+1) % count] != 3:
                        continue
                    selected_positions = sorted((x-chosen[root]) % m for x in chosen)
                    require(selected_positions[:3] == [0, 2, 5], 'lost (2,3) root')
                    k = selected_positions[3]
                    require(k in range(7, 14), 'third gap outside fourteen-case cover')
                    for background in (0, 1):
                        bits = [int((i in selected_positions) != bool(background)) for i in range(m)]
                        anchors = {0, 2, 5, k}
                        for i in range(m):
                            if i in anchors:
                                require(bits[i] == 1-background, 'lost selected anchor')
                            elif 5 < i < k or any(min((i-x) % m, (x-i) % m) == 1
                                                  for x in anchors):
                                require(bits[i] == background, 'lost forced background')
                        seen.add((k, background))
                        cover += 1
    require(seen == {(k, b) for k in range(7, 14) for b in (0, 1)},
            'tiny controls miss a branch')
    return cover, local, sorted(seen)


def main(work):
    began = time.monotonic()
    pins()
    models = json.loads((work/'models.json').read_text())
    expected = [(k, b) for k in range(13, 6, -1) for b in (0, 1)]
    require([r['stem'] for r in models['records']] ==
            [f'gap-2-3-next-{k}-b-{b}' for k, b in expected], 'incomplete fourteen-case cover')
    require({p.name for p in work.glob('*.cnf')} ==
            {f'gap-2-3-next-{k}-b-{b}.cnf' for k, b in expected}, 'missing or extra model file')
    slots, supports = literal_field()
    records = []
    for record, (k, background) in zip(models['records'], expected):
        require(record['minimum_distance'] == 2 and record['fourth_selected_index'] == k
                and record['third_gap'] == k-5 and record['background'] == background
                and record['phase_K'] == (34 if background else 10)
                and record['free_selected_count'] == 6 and record['root57_color_cut'] is True
                and record['successor_cut'] is True and record['successor_shift_count'] == 44,
                'changed branch semantics')
        fixed = head_fixed(k, background)
        free = [i for i in range(44) if i not in fixed]
        semantic, n = expected_clauses(slots, supports, fixed, 2)
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
        require(n == len(free) == 41-k and record['free_phase_indices'] == free,
                'wrong free phase domain')
        successor, successor_truth_rows = set(), 0
        for origin in range(44):
            positions = [(origin+d) % 44 for d in (0, 2, 4, 5)]
            forbidden = [1-background, 1-background, background, background]
            if any(i in fixed and fixed[i] != value for i, value in zip(positions, forbidden)):
                continue
            literals = tuple(sorted((45+n+index[i])*(1 if value == 0 else -1)
                                    for i, value in zip(positions, forbidden) if i not in fixed))
            require(literals, 'head violates a constant successor clause')
            successor.add(literals)
            domain = [i for i in positions if i not in fixed]
            for values in itertools.product((0, 1), repeat=len(domain)):
                assignment = dict(zip(domain, values))
                actual = [fixed[i] if i in fixed else assignment[i] for i in positions]
                selected = [x != background for x in actual]
                necessary = not (selected[0] and selected[1]) or selected[2] or selected[3]
                row_value = any(assignment[free[abs(v)-45-n]] == (v > 0) for v in literals)
                require(bool(row_value) == bool(necessary), 'wrong substituted successor truth relation')
                successor_truth_rows += 1
        require(len(successor) == record['successor_clauses'], 'changed successor clause count')
        semantic.update(successor)
        cnf = work/(record['stem']+'.cnf')
        text = cnf.read_text().splitlines()
        variables = 23+9*n
        require(text[0].split() == ['p', 'cnf', str(variables), str(record['clauses'])]
                and record['variables'] == variables, 'wrong model dimension')
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
                'full actual-field fourteen-case model audit differs')
        records.append(dict(stem=record['stem'], variables=variables, clauses=len(rows),
            cnf_sha256=sha(cnf), counter_truth_rows=truth_rows,
            successor_clauses=len(successor), successor_truth_rows=successor_truth_rows,
            free_phase_inputs_before_cuts=math.comb(n, 6)))
    thresholds, exact = tiny_controls()
    cover_inputs, local_truth_rows, tiny_branches = cover_controls()
    result = dict(agent='six-vdw-2', role='researcher', status='EXACT_K10_D2_GAP23_THIRD14_AUDIT',
        records=records, literal_APs=375760, removed_zero_APs=4312, signed_supports=26488,
        tiny_threshold_cells=thresholds, tiny_exact_counts=exact,
        tiny_fourteen_case_cover_inputs=cover_inputs, tiny_branches=tiny_branches,
        successor_local_truth_rows=local_truth_rows, seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path = work/('audit-optimized.json' if not __debug__ else 'audit-normal.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
