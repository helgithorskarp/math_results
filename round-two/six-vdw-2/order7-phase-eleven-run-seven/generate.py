"""Thirty fully fixed phase words; only the 44 lower colors are variables."""
import argparse
import itertools
import json
from pathlib import Path
import time
from common import COMMIT, REF, imported, pins, require, sha

GAPS = [g for g in itertools.product(range(1, 8), repeat=5) if sum(g) == 33]
PARAMETERS = [(index, background) for index in range(len(GAPS)) for background in (0, 1)]

def stem_for(index, background):
    return f'eleven-run7-gap-{index:02d}-b-{background}'

def phase(gaps, background):
    bits = [1-background] * 7 + [background] * gaps[0]
    for gap in gaps[1:]:
        bits += [1-background] + [background] * gap
    require(len(bits) == 44 and sum(v != background for v in bits) == 11, 'wrong fixed phase')
    require(all(len({bits[(i+j) % 44] for j in range(8)}) == 2 for i in range(44)), 'fixed phase8 fails')
    return bits

def put(rows, literals):
    values = set(literals)
    if not any(-v in values for v in values):
        rows.add(tuple(sorted(values)))

def main(work):
    began = time.monotonic(); dependency = pins()
    require(not work.exists(), 'fresh longest-seven model workspace required')
    require(len(GAPS) == 15 and len(PARAMETERS) == 30, 'incomplete fixed-gap cover')
    work.mkdir(parents=True)
    edges = imported('encode.py', 'eleven_run7_encoder').field_edges()
    records = []
    for index, background in PARAMETERS:
        bits = phase(GAPS[index], background)
        colors = list(range(1, 45)) + [(i+1) * (-1 if bits[i] else 1) for i in range(44)]
        field, color = set(), set()
        for edge in edges:
            values = [colors[i] for i in edge]
            put(field, values); put(field, [-v for v in values])
        for origin in range(88):
            for length, step in ((7, 1), (8, 19)):
                values = [colors[(origin+j*step) % 88] for j in range(length)]
                put(color, values); put(color, [-v for v in values])
        rows = sorted(field | color, key=lambda row: (len(row), row)) + [(-1,)]
        stem = stem_for(index, background); path = work / (stem + '.cnf')
        path.write_text(f'p cnf 44 {len(rows)}\n' + ''.join(' '.join(map(str, row)) + ' 0\n' for row in rows))
        records.append(dict(stem=stem, gap_index=index, background=background, background_gaps=list(GAPS[index]),
            phase=bits, phase_K=sum(bits), minority_count=11, normalized_minority_run=list(range(7)),
            minority_run_lengths=[7, 1, 1, 1, 1], background_run_count=5,
            unique_longest_minority_run=True, maximum_minority_run=7, maximum_background_run=7,
            phase_variables=0, lower_orientation_variables=44, independent_lower_colors_before_palette_gauge=44,
            variables=44, clauses=len(rows), cnf_sha256=sha(path), physical_field_clauses=len(field),
            universal_color_clauses=len(color), new_universal_color_clauses=len(color-field),
            only_global_y0_zero=True, gauge_clauses=[[-1]], root3_color_cut=True, root57_color_cut=True,
            nonconstant_phase8_checked=True, phase8_residual_clauses=0,
            isolated_eleven_gap4_rule_used=False, exact_TEN_rules_used=False,
            prior_adjacent_rule_used_as_numerical_cut=False, proposed_run7_exclusion_used=False,
            unrelated_family_cut=False, unpublished_exclusion_used_as_input=False,
            prior_adjacent_ref=REF, source_commit=COMMIT, mathematical_exclusion=False))
    hashes = {r['cnf_sha256'] for r in records}
    require(len(hashes) == 30 and not hashes.intersection(dependency['frozen_prior_cnfs']), 'duplicate or frozen failed input')
    result = dict(agent='six-vdw-2', role='researcher', status='GENERATED_NOT_AUDITED',
                  producer_sha256=sha(Path(__file__)), total_heads=30, records=records, seconds=time.monotonic()-began)
    (work / 'models.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
