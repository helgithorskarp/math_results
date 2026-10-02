"""Sixteen complete ordinary fourth-selection heads; proposed no-adjacency absent."""
import argparse,json,time
from pathlib import Path
from common import load_encoder,require,sha,endpoint_generator,pins
old=endpoint_generator()
neg,put=old.neg,old.put
PARAMETERS=[(ell,b) for ell in range(10,4,-1) for b in (0,1)]
def stem_for(ell,b):return f'fourth4-fourth-{ell}-b-{b}'
def head_fixed(ell,background):
    require((ell,background) in PARAMETERS,'unsupported fourth head')
    anchors={0,1,2,ell}
    fixed={i:1-background if i in anchors else background for i in range(ell+1)}
    fixed[43]=background
    return fixed
def prefix(inputs,base):
    previous,rows,cursor={0:True},set(),base
    for i,value in enumerate(inputs,1):
        current={0:True}
        for threshold in range(1,min(i,7)+1):
            cursor+=1
            a,b,z=previous.get(threshold,False),previous[threshold-1],cursor
            for row in ((neg(a),z),(neg(value),neg(b),z),(a,value,-z),(a,b,-z)):
                put(rows,row)
            current[threshold]=z
        previous=current
    put(rows,[previous[6]]);put(rows,[-previous[7]])
    return rows,cursor
def main(work):
    began=time.monotonic()
    require(not work.exists(),'fresh work directory required');work.mkdir(parents=True)
    edges=load_encoder().field_edges();premise=pins();records=[]
    for ell,background in PARAMETERS:
        fixed=head_fixed(ell,background)
        free=[i for i in range(44) if i not in fixed];n=len(free)
        index={i:j for j,i in enumerate(free)}
        colors=list(range(1,45))+[(i+1)*(-1 if fixed[i] else 1)
            if i in fixed else 45+index[i] for i in range(44)]
        phases=[bool(fixed[i]) if i in fixed else 45+n+index[i] for i in range(44)]
        field,color,phase,xor=(set() for _ in range(4))
        for edge in edges:
            values=[colors[i] for i in edge];put(field,values);put(field,[-v for v in values])
        for origin in range(88):
            values=[colors[(origin+j)%88] for j in range(7)]
            put(color,values);put(color,[-v for v in values])
            values=[colors[(origin+19*j)%88] for j in range(8)]
            put(color,values);put(color,[-v for v in values])
        for origin in range(44):
            values=[phases[(origin+j)%44] for j in range(8)]
            put(phase,values);put(phase,[neg(v) for v in values])
        for i in free:
            a,b,s=i+1,45+index[i],45+n+index[i]
            xor.update(tuple(sorted(row)) for row in
                ((a,b,-s),(a,-b,s),(-a,b,s),(-a,-b,-s)))
        counter,variables=prefix([phases[i]*(-1 if background else 1) for i in free],44+2*n)
        require(n==42-ell and variables==23+9*n,'wrong SIX exact-count dimension')
        core=field|color|phase|xor|counter;two=set()
        selected=[neg(value) if background else value for value in phases]
        for origin in range(44):
            put(two,[selected[(origin-1)%44],neg(selected[origin]),
                     neg(selected[(origin+1)%44]),selected[(origin+2)%44]])
        require(len(two-core)>0,'new model adds no distinct TWO clauses')
        rows=sorted(core|two,key=lambda row:(len(row),row))+[(-1,)]
        stem=stem_for(ell,background);cnf=work/(stem+'.cnf')
        cnf.write_text(f'p cnf {variables} {len(rows)}\n'+
            ''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,minimum_distance=1,background=background,
            third_selected_index=2,fourth_selected_index=ell,selected_anchors=[0,1,2,ell],
            phase_K=34 if background else 10,free_phase_indices=free,variables=variables,
            clauses=len(rows),cnf_sha256=sha(cnf),free_selected_count=6,selected_anchor_count=4,
            root57_color_cut=True,actual_TWO_cut=True,
            two_lemma_graph=premise['premise']['graph'],
            two_lemma_source_commit=premise['premise']['source_commit'],
            two_clauses_after_substitution=len(two),new_two_clauses=len(two-core),
            next_free_phase=ell+1,proposed_FOURTH4_cut=False,proposed_NO_ADJACENCY_cut=False,
            redundant_ancestor_cuts=False,conditional_successor_cut=False,
            selected_run_start=True,mathematical_exclusion=False))
    result=dict(status='GENERATED_NOT_AUDITED',agent='six-vdw-2',role='researcher',records=records,
                producer_sha256=sha(Path(__file__)),seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
