"""Complete length-six heads, fixed phases, exactly44 original color variables."""
import argparse
import json
import time
from pathlib import Path
from common import COMMIT, REF, ROOT, SOURCE, encoder, pins, require, sha

PARAMETERS = [(gap, background) for gap in range(5) for background in (0, 1)]

def stem_for(gap, background):
    return f'length6-gap-{gap}-b-{background}'

def phase_word(gap, background):
    require((gap, background) in PARAMETERS, 'unsupported length6 head')
    gaps = [6 if j == gap else 7 for j in range(5)]
    selected = list(range(6))
    cursor = 5
    for length in gaps[:4]:
        cursor += length + 1
        selected.append(cursor)
    require(cursor + gaps[4] + 1 == 44, 'wrong cyclic phase length')
    return [background ^ int(i in selected) for i in range(44)], gaps, selected

def put(target, values):
    if any(value is True for value in values):
        return
    literals = set(value for value in values if value is not False)
    if any(-value in literals for value in literals):
        return
    target.add(tuple(sorted(literals)))

def main(work):
    began = time.monotonic()
    pins()
    require(not work.exists(), 'fresh work directory required')
    work.mkdir(parents=True)
    field_edges = encoder().field_edges()
    plan = json.loads((SOURCE / 'PHASE_EXPECTED.json').read_text())['length6_case_plan']
    records = []
    for index, (gap, background) in enumerate(PARAMETERS):
        phase, gaps, selected = phase_word(gap, background)
        require(plan[index]['phases'] == phase and plan[index]['gaps'] == gaps
                and plan[index]['selected'] == selected
                and plan[index]['background'] == background
                and plan[index]['deficient_gap'] == gap, 'published ten-head plan differs')
        colors = list(range(1, 45)) + [(-1 if phase[i] else 1) * (i + 1) for i in range(44)]
        field, root3, root57 = set(), set(), set()
        for edge in field_edges:
            values = [colors[i] for i in edge]
            put(field, values)
            put(field, [-v for v in values])
        for origin in range(88):
            values = [colors[(origin+j) % 88] for j in range(7)]
            put(root3, values)
            put(root3, [-v for v in values])
            values = [colors[(origin+19*j) % 88] for j in range(8)]
            put(root57, values)
            put(root57, [-v for v in values])
        require(all(len({phase[(origin+j) % 44] for j in range(8)}) == 2
                    for origin in range(44)), 'fixed phase violates phase8')
        for origin in range(44):
            s = lambda j: phase[(origin+j) % 44] != background
            require(s(-1) or not s(0) or not s(1) or s(2), 'fixed phase violates actual TWO')
            require(s(-1) or not s(0) or not s(1) or s(3) or s(4),
                    'fixed phase violates actual FOURTH4')
        rows = sorted(field | root3 | root57, key=lambda row: (len(row), row)) + [(-1,)]
        stem = stem_for(gap, background)
        cnf = work / (stem + '.cnf')
        cnf.write_text(f'p cnf 44 {len(rows)}\n' + ''.join(
            ' '.join(map(str, row)) + ' 0\n' for row in rows))
        records.append(dict(stem=stem, deficient_gap=gap, background=background,
                            selected=selected, phases=phase, gaps=gaps,
                            phase_K=sum(phase), selected_phase_count=10, variables=44,
                            clauses=len(rows), cnf_sha256=sha(cnf),
                            field_clauses=len(field), root3_clauses=len(root3),
                            root57_clauses=len(root57), actual_TWO_checked=True,
                            actual_FOURTH4_checked=True, phase8_checked=True,
                            all_phases_fixed=True, phase_auxiliaries=0, counter_auxiliaries=0,
                            color_auxiliaries=0, only_global_y0_zero=True,
                            reflection_assumed=False, phase_exchange_assumed=False,
                            proposed_length6_exclusion_cut=False, proposed_no_adjacency_cut=False,
                            unrelated_family_cut=False, premise_ref=REF, source_commit=COMMIT,
                            mathematical_exclusion=False))
    out = dict(agent='six-vdw-2', role='researcher', status='GENERATED_NOT_AUDITED',
               producer_sha256=sha(Path(__file__)), records=records,
               seconds=time.monotonic()-began)
    (work / 'models.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'records'}), flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', required=True, type=Path)
    main(p.parse_args().work.absolute())
