"""Disjoint six-head generation; complete120 cover requires all20 persisted batches."""
import argparse
import itertools
import json
from pathlib import Path
import time
from common import COMMIT, REF, RUN7_COMMIT, RUN7_REF, imported, pins, require, sha

GAPS = [g for g in itertools.product(range(1, 8), repeat=5) if sum(g) == 33]
PARAMETERS = [(slot, index, background) for slot in range(1, 5) for index in range(len(GAPS)) for background in (0, 1)]

def stem_for(slot, index, background):
    return f'eleven-run6-batch-pair-{slot}-gap-{index:02d}-b-{background}'

def profile_for(slot):
    return [6] + [2 if j == slot else 1 for j in range(1, 5)]

def phase(slot, gaps, background):
    bits = []
    for run, gap in zip(profile_for(slot), gaps):
        bits += [1-background]*run + [background]*gap
    require(len(bits) == 44 and sum(v != background for v in bits) == 11, 'wrong fixed phase')
    require(all(len({bits[(i+j) % 44] for j in range(8)}) == 2 for i in range(44)), 'fixed phase8 fails')
    return bits

def put(rows, literals):
    values = set(literals)
    if not any(-v in values for v in values):
        rows.add(tuple(sorted(values)))

def main(work, batch):
    began = time.monotonic(); dependency = pins()
    require(type(batch) is int and 0 <= batch < 20, 'preselected disjoint generation batch required')
    require(len(GAPS) == 15 and len(PARAMETERS) == 120, 'incomplete fixed cover')
    work.mkdir(parents=True, exist_ok=True)
    output = work/f'generate-batch-{batch}.json'
    require(not output.exists() and not (work/'models.json').exists(), 'existing generation batch or whole manifest is frozen')
    edges = imported('encode.py', 'eleven_run6_batch_encoder').field_edges()
    records = []
    for slot, index, background in PARAMETERS[6*batch:6*batch+6]:
        bits = phase(slot, GAPS[index], background)
        colors = list(range(1, 45)) + [(i+1)*(-1 if bits[i] else 1) for i in range(44)]
        field, color = set(), set()
        for edge in edges:
            values = [colors[i] for i in edge]
            put(field, values); put(field, [-v for v in values])
        for origin in range(88):
            for length, step in ((7, 1), (8, 19)):
                values = [colors[(origin+j*step) % 88] for j in range(length)]
                put(color, values); put(color, [-v for v in values])
        rows = sorted(field | color, key=lambda row: (len(row), row)) + [(-1,)]
        stem = stem_for(slot, index, background); path = work/(stem+'.cnf')
        require(not path.exists() and not path.with_suffix('.cnf.tmp').exists(), 'partial or completed case path is frozen')
        temporary = path.with_suffix('.cnf.tmp')
        temporary.write_text(f'p cnf 44 {len(rows)}\n'+''.join(' '.join(map(str, row))+' 0\n' for row in rows))
        temporary.replace(path)
        records.append(dict(stem=stem, pair_run_slot=slot, gap_index=index, background=background, background_gaps=list(GAPS[index]),
            phase=bits, phase_K=sum(bits), minority_count=11, normalized_minority_run=list(range(6)),
            minority_run_lengths=profile_for(slot), minority_run_count=5, background_run_count=5,
            unique_longest_minority_run=True, maximum_minority_run=6, maximum_background_run=7,
            phase_variables=0, lower_orientation_variables=44, independent_lower_colors_before_palette_gauge=44,
            variables=44, clauses=len(rows), cnf_sha256=sha(path), physical_field_clauses=len(field),
            universal_color_clauses=len(color), new_universal_color_clauses=len(color-field),
            only_global_y0_zero=True, gauge_clauses=[[-1]], root3_color_cut=True, root57_color_cut=True,
            nonconstant_phase8_checked=True, phase8_residual_clauses=0,
            isolated_eleven_gap4_rule_used=False, exact_TEN_rules_used=False,
            prior_adjacent_rule_used_as_numerical_cut=False, prior_run7_rule_used_as_numerical_cut=False,
            proposed_run6_five_exclusion_used=False, unrelated_family_cut=False, unpublished_exclusion_used_as_input=False,
            prior_adjacent_ref=REF, adjacent_source_commit=COMMIT, prior_run7_context_ref=RUN7_REF,
            source_commit=RUN7_COMMIT, mathematical_exclusion=False))
    hashes = {r['cnf_sha256'] for r in records}
    require(len(hashes) == 6 and not hashes.intersection(dependency['frozen_prior_cnfs'])
            and not hashes.intersection(dependency['completed_run7_cnfs']), 'duplicate or previously attempted input')
    result = dict(agent='six-vdw-2', role='researcher', status='GENERATED_NOT_AUDITED',
                  producer_sha256=sha(Path(__file__)), batch=batch, total_heads=6, records=records, seconds=time.monotonic()-began)
    temporary = output.with_suffix('.json.tmp'); temporary.write_text(json.dumps(result, indent=2)+'\n'); temporary.replace(output)
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}), flush=True)

def merge(work):
    began = time.monotonic(); dependency = pins()
    require(not (work/'models.json').exists(), 'existing merged cover is frozen')
    require(len(list(work.glob('generate-batch-*.json'))) == 20, 'incomplete or extra generation batch')
    records = []
    for batch in range(20):
        data = json.loads((work/f'generate-batch-{batch}.json').read_text())
        require(set(data) == {'agent','role','status','producer_sha256','batch','total_heads','records','seconds'}
                and data['agent'] == 'six-vdw-2' and data['role'] == 'researcher'
                and data['status'] == 'GENERATED_NOT_AUDITED' and data['producer_sha256'] == sha(Path(__file__))
                and data['batch'] == batch and data['total_heads'] == 6
                and [(r['pair_run_slot'],r['gap_index'],r['background']) for r in data['records']] == PARAMETERS[6*batch:6*batch+6],
                'whole persisted six-head generation batch differs')
        for record in data['records']:
            require(sha(work/(record['stem']+'.cnf')) == record['cnf_sha256'], 'persisted generated case bytes changed')
        records.extend(data['records'])
    hashes = {r['cnf_sha256'] for r in records}
    require(len(records) == len(hashes) == 120
            and [(r['pair_run_slot'],r['gap_index'],r['background']) for r in records] == PARAMETERS
            and not hashes.intersection(dependency['frozen_prior_cnfs'])
            and not hashes.intersection(dependency['completed_run7_cnfs']), 'incomplete, repeated or previously attempted merged case')
    result = dict(agent='six-vdw-2', role='researcher', status='GENERATED_NOT_AUDITED',
                  producer_sha256=sha(Path(__file__)), total_heads=120, records=records, seconds=time.monotonic()-began)
    temporary = work/'models.json.tmp'; temporary.write_text(json.dumps(result, indent=2)+'\n'); temporary.replace(work/'models.json')
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--batch', type=int); parser.add_argument('--merge', action='store_true'); args = parser.parse_args()
    require((args.batch is None) == args.merge, 'choose exactly one generation batch or complete merge')
    if args.merge:
        merge(args.work.absolute())
    else:
        main(args.work.absolute(), args.batch)
