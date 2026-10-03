"""Eight conditional maximum-gap heads with exactly eleven isolated selections."""
import argparse
import json
from pathlib import Path
import time
from common import COMMIT, REF, encoder, pins, require, sha

PAIR_STARTS=sorted(range(8,40),key=lambda j:(abs(j-22),j))+[7,40,5,42]
PARAMETERS=[(j,b) for j in PAIR_STARTS for b in (0,1)]

def stem_for(j,b):return f'eleven-gap4-pairs-j-{j}-b-{b}'

def fixed_head(j,b):
    require((j,b) in PARAMETERS,'unsupported conditional minimum-pair gap4 head')
    selected={0,5,j,(j+2)%44}; background={1,2,3,4,6,43,(j-1)%44,(j+1)%44,(j+3)%44}
    require(not(selected & background),'colliding conditional head assignments')
    return {i:1-b for i in selected}|{i:b for i in background}

def neg(value):
    return not value if isinstance(value,bool) else -value

def put(target,values):
    if any(v is True for v in values):return
    literals={v for v in values if v is not False}
    if any(-v in literals for v in literals):return
    target.add(tuple(sorted(literals)))

def prefix(inputs,base,exact):
    previous={0:True};rows=set();cursor=base;levels=exact+1
    for j,value in enumerate(inputs,1):
        current={0:True}
        for k in range(1,min(j,levels)+1):
            cursor+=1;a=previous.get(k,False);b=previous[k-1];z=cursor
            for row in ((neg(a),z),(neg(value),neg(b),z),(a,value,-z),(a,b,-z)):put(rows,row)
            current[k]=z
        previous=current
    put(rows,[previous[exact]]);put(rows,[-previous[levels]])
    return rows,cursor

def main(work):
    began=time.monotonic();pins();require(not work.exists(),'fresh seventy-two pair heads required')
    work.mkdir(parents=True);edges=encoder().field_edges();records=[]
    for j,background in PARAMETERS:
        m=5;fixed=fixed_head(j,background);free=[i for i in range(44) if i not in fixed]
        n=len(free);index={i:j for j,i in enumerate(free)}
        colors=list(range(1,45))+[(i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i] for i in range(44)]
        phases=[bool(fixed[i]) if i in fixed else 45+n+index[i] for i in range(44)]
        selected=[neg(v) if background else v for v in phases]
        field,color,phase,xor,isolation,maxgap=(set() for _ in range(6))
        for edge in edges:
            values=[colors[i] for i in edge];put(field,values);put(field,[-v for v in values])
        for origin in range(88):
            for length,step in ((7,1),(8,19)):
                values=[colors[(origin+j*step)%88] for j in range(length)]
                put(color,values);put(color,[-v for v in values])
        for origin in range(44):
            values=[phases[(origin+j)%44] for j in range(8)]
            put(phase,values);put(phase,[neg(v) for v in values])
            put(isolation,[neg(selected[origin]),neg(selected[(origin+1)%44])])
            put(maxgap,[selected[(origin+j)%44] for j in range(m)])
        for i in free:
            a,b,s=i+1,45+index[i],45+n+index[i]
            xor.update(tuple(sorted(row)) for row in ((a,b,-s),(a,-b,s),(-a,b,s),(-a,-b,-s)))
        known=sum(v!=background for v in fixed.values());exact=11-known
        counter,variables=prefix([selected[i] for i in free],44+2*n,exact)
        require(variables==44+(exact+3)*n-exact*(exact+1)//2,'wrong exact-eleven maximum-gap dimension')
        core=field|color|phase|xor|counter
        require(len(isolation-core)>0,'missing conditional isolation clauses')
        require(m==8 or len(maxgap-(core|isolation))>0,'missing conditional maximum-gap restriction')
        rows=sorted(core|isolation|maxgap,key=lambda row:(len(row),row))+[(-1,)]
        stem=stem_for(j,background);cnf=work/(stem+'.cnf')
        cnf.write_text(f'p cnf {variables} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,next_selected=m,maximum_background_gap=m-1,background=background,
            phase_K=33 if background else 11,selected_phase_count=11,free_selected_count=exact,
            selected_anchor_count=known,counter_levels=exact+1,
            minimum_pair_start=j,minimum_pair_selected_positions=[j,(j+2)%44],
            minimum_pair_background_positions=[(j-1)%44,(j+1)%44,(j+3)%44],
            conditional_minimum_pair_head=True,minimum_pair_rule_is_universal=False,
            fixed_phase_positions={str(i):v for i,v in fixed.items()},free_phase_indices=free,
            lower_orientation_variables=44,minimum_selected_distance_at_least=2,
            normalized_selected_pair=[0,m],variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),
            conditional_isolation_clauses=len(isolation),new_conditional_isolation_clauses=len(isolation-core),
            maximum_gap_clauses=len(maxgap),new_maximum_gap_clauses=len(maxgap-(core|isolation)),
            conditional_all_selected_isolated=True,isolation_rule_is_universal=False,
            maximum_gap_normalization=True,maximum_gap_rule_is_global_phase_restriction=False,
            next_phase_after_selected_fixed_background=True,only_global_y0_zero=True,
            root3_color_cut=True,root57_color_cut=True,nonconstant_phase8_cut=True,
            exact_TEN_rules_used=False,proposed_ELEVEN_exclusion_used=False,
            gap_four_lemma_used_as_unconditional_native_cut=False,unpublished_exclusion_used_as_input=False,
            unrelated_family_cut=False,premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False))
    out=dict(agent='six-vdw-2',role='researcher',status='GENERATED_NOT_AUDITED',
        producer_sha256=sha(Path(__file__)),records=records,seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
