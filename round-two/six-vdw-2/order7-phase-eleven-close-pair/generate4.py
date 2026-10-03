"""Two fully fixed exact-eleven cyclic spacing-four phases; all 44 orientations free."""
import argparse
import json
from pathlib import Path
import time
from common import COMMIT, REF, encoder, pins, require, sha

PARAMETERS = [0, 1]

def stem_for(background):
    return f'eleven4-fixed-b-{background}'

def fixed_phase(background):
    require(background in PARAMETERS, 'unsupported background')
    return [background ^ int(i % 4 == 0) for i in range(44)]

def put(rows, values):
    values = set(values)
    if not any(-v in values for v in values):
        rows.add(tuple(sorted(values)))

def main(work):
    began = time.monotonic(); pins()
    require(not work.exists(), 'fresh model directory required'); work.mkdir(parents=True)
    edges = encoder().field_edges(); records = []
    for background in PARAMETERS:
        phases = fixed_phase(background)
        colors = list(range(1,45)) + [(i+1)*(-1 if phases[i] else 1) for i in range(44)]
        field, color = set(), set()
        for edge in edges:
            values = [colors[i] for i in edge]
            put(field, values); put(field, [-v for v in values])
        for origin in range(88):
            for length, step in ((7,1),(8,19)):
                values = [colors[(origin+j*step)%88] for j in range(length)]
                put(color,values); put(color,[-v for v in values])
        require(sum(v != background for v in phases)==11
                and all(len({phases[(i+j)%44] for j in range(8)})==2 for i in range(44)),
                'wrong fixed nonconstant exact-eleven phase')
        rows = sorted(field|color, key=lambda row:(len(row),row)) + [(-1,)]
        stem = stem_for(background); cnf = work/(stem+'.cnf')
        cnf.write_text(f'p cnf 44 {len(rows)}\n' + ''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,background=background,phase_K=sum(phases),
            selected_phase_count=11,selected_indices=list(range(0,44,4)),fixed_phases=phases,
            minimum_selected_distance=4,fully_fixed_phase=True,variables=44,clauses=len(rows),
            lower_orientation_variables=44,phase_auxiliary_variables=0,xor_auxiliary_variables=0,
            counter_auxiliary_variables=0,only_global_y0_zero=True,root3_color_cut=True,
            root57_color_cut=True,nonconstant_phase8_checked=True,orientation_period_four_required=False,
            exact_TEN_rules_used=False,proposed_ELEVEN_exclusion_used=False,
            unpublished_exclusion_used_as_input=False,unrelated_family_cut=False,
            field_clauses=len(field),universal_color_clauses=len(color),
            new_universal_color_clauses=len(color-field),cnf_sha256=sha(cnf),
            premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False))
    out=dict(agent='six-vdw-2',role='researcher',status='GENERATED_NOT_AUDITED',
             producer_sha256=sha(Path(__file__)),records=records,seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
