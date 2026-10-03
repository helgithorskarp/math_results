"""Exact-eleven normalized minimum-distance-three branch, both phase values explicit."""
import argparse
import json
from pathlib import Path
import time
from common import COMMIT, REF, encoder, pins, require, sha

PARAMETERS=[0,1]
def stem_for(background):return f'eleven3-mindistance-3-b-{background}'
def fixed_head(background):
    require(background in PARAMETERS,'unsupported minimum-distance-three background')
    return {i:(1-background if i in (0,3) else background) for i in (*range(6),42,43)}

def neg(value):
    return not value if isinstance(value,bool) else -value

def put(target,values):
    if any(value is True for value in values): return
    literals={value for value in values if value is not False}
    if any(-value in literals for value in literals): return
    target.add(tuple(sorted(literals)))

def prefix(inputs,base,exact):
    levels=exact+1;previous={0:True};rows=set();cursor=base
    for j,value in enumerate(inputs,1):
        current={0:True}
        for k in range(1,min(j,levels)+1):
            cursor+=1;a=previous.get(k,False);b=previous[k-1];z=cursor
            for row in ((neg(a),z),(neg(value),neg(b),z),(a,value,-z),(a,b,-z)):
                put(rows,row)
            current[k]=z
        previous=current
    put(rows,[previous[exact]]);put(rows,[-previous[levels]])
    return rows,cursor

def main(work):
    began=time.monotonic();pins();require(not work.exists(),'fresh minimum-distance-three models required')
    work.mkdir(parents=True);edges=encoder().field_edges();records=[]
    for background in PARAMETERS:
        fixed=fixed_head(background);free=[i for i in range(44) if i not in fixed]
        n=len(free);index={i:j for j,i in enumerate(free)}
        colors=list(range(1,45))+[(i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i] for i in range(44)]
        phases=[bool(fixed[i]) if i in fixed else 45+n+index[i] for i in range(44)]
        selected=[neg(v) if background else v for v in phases]
        field,color,phase,xor,spacing=(set() for _ in range(5))
        for edge in edges:
            values=[colors[i] for i in edge];put(field,values);put(field,[-v for v in values])
        for origin in range(88):
            for length,step in ((7,1),(8,19)):
                values=[colors[(origin+j*step)%88] for j in range(length)]
                put(color,values);put(color,[-v for v in values])
        for origin in range(44):
            values=[phases[(origin+j)%44] for j in range(8)]
            put(phase,values);put(phase,[neg(v) for v in values])
            for distance in (1,2):put(spacing,[neg(selected[origin]),neg(selected[(origin+distance)%44])])
        for i in free:
            a,b,s=i+1,45+index[i],45+n+index[i]
            xor.update(tuple(sorted(row)) for row in ((a,b,-s),(a,-b,s),(-a,b,s),(-a,-b,-s)))
        counter,variables=prefix([selected[i] for i in free],44+2*n,9)
        require(n==36 and variables==431,'wrong exact-eleven branch dimension')
        core=field|color|phase|xor|counter
        rows=sorted(core|spacing,key=lambda row:(len(row),row))+[(-1,)]
        stem=stem_for(background);cnf=work/(stem+'.cnf')
        cnf.write_text(f'p cnf {variables} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,background=background,phase_K=33 if background else 11,
            selected_phase_count=11,free_selected_count=9,selected_anchor_count=2,counter_levels=10,
            fixed_phase_positions={str(i):v for i,v in fixed.items()},free_phase_indices=free,
            minimum_selected_distance=3,normalized_selected_pair=[0,3],lower_orientation_variables=44,
            variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),
            conditional_spacing_clauses=len(spacing),new_conditional_spacing_clauses=len(spacing-core),
            conditional_minimum_distance_rule=True,minimum_distance_rule_is_universal=False,
            only_global_y0_zero=True,root3_color_cut=True,root57_color_cut=True,nonconstant_phase8_cut=True,
            exact_TEN_rules_used=False,unpublished_exclusion_used_as_input=False,
            proposed_ELEVEN_exclusion_used=False,regular_spacing_exclusion_used_as_input=False,
            unrelated_family_cut=False,premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False))
    out=dict(agent='six-vdw-2',role='researcher',status='GENERATED_NOT_AUDITED',
        producer_sha256=sha(Path(__file__)),records=records,seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
