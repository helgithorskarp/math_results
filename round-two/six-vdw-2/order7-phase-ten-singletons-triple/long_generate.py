"""Twenty-eight ordinary exact-ten heads with one prescribed long run and singleton exterior."""
import argparse
import json
from pathlib import Path
import time
from common import COMMIT, REF, encoder, pins, require, sha

PARAMETERS = [(t,m,b) for t in (5,4)
              for m in (range(t+7,t,-1) if t != 3 else (4,)) for b in (0,1)]

def stem_for(t,m,b):
    return f'run45-t-{t}-next-{m}-b-{b}'

def fixed_head(t,m,b):
    require((t,m,b) in PARAMETERS,'unsupported ordinary unique-run head')
    return {i:1-b for i in range(t)} | {i:b for i in range(t,m)} | {m:1-b,m+1:b,43:b}

def neg(value):
    return not value if isinstance(value,bool) else -value

def put(target,values):
    if any(value is True for value in values):return
    literals = {value for value in values if value is not False}
    if any(-value in literals for value in literals):return
    target.add(tuple(sorted(literals)))

def prefix(inputs,base,exact):
    levels = exact+1;previous={0:True};rows=set();cursor=base
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
    began=time.monotonic();pins();require(not work.exists(),'fresh model directory required');work.mkdir(parents=True)
    edges=encoder().field_edges();records=[]
    for t,m,background in PARAMETERS:
        fixed=fixed_head(t,m,background);free=[i for i in range(44) if i not in fixed]
        index={i:j for j,i in enumerate(free)};n=len(free);remainder=9-t;levels=10-t
        colors=list(range(1,45))+[(i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i] for i in range(44)]
        phases=[bool(fixed[i]) if i in fixed else 45+n+index[i] for i in range(44)]
        field,color,phase,xor,two,fourth,outside=(set() for _ in range(7))
        for edge in edges:
            values=[colors[i] for i in edge];put(field,values);put(field,[-v for v in values])
        for origin in range(88):
            values=[colors[(origin+j)%88] for j in range(7)];put(color,values);put(color,[-v for v in values])
            values=[colors[(origin+19*j)%88] for j in range(8)];put(color,values);put(color,[-v for v in values])
        for origin in range(44):
            values=[phases[(origin+j)%44] for j in range(8)];put(phase,values);put(phase,[neg(v) for v in values])
        for i in free:
            a,b,s=i+1,45+index[i],45+n+index[i]
            xor.update(tuple(sorted(row)) for row in ((a,b,-s),(a,-b,s),(-a,b,s),(-a,-b,-s)))
        selected=[neg(value) if background else value for value in phases]
        for origin in range(44):
            values=lambda offsets:[selected[(origin+j)%44] for j in offsets]
            a,b,c,d=values((-1,0,1,2));put(two,[a,neg(b),neg(c),d])
            a,b,c,d,e=values((-1,0,1,3,4));put(fourth,[a,neg(b),neg(c),d,e])
            if origin not in range(t-1):
                put(outside,[neg(selected[origin]),neg(selected[(origin+1)%44])])
        counter,variables=prefix([selected[i] for i in free],44+2*n,remainder)
        require(n==41-m and variables==44+(2+levels)*n-levels*(levels-1)//2,'wrong heterogeneous exact count')
        core=field|color|phase|xor|two|fourth|counter
        require(len(outside-core)>0,'no distinct outside-singleton constraints')
        rows=sorted(core|outside,key=lambda row:(len(row),row))+[(-1,)]
        stem=stem_for(t,m,background);cnf=work/(stem+'.cnf')
        cnf.write_text(f'p cnf {variables} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,long_run_length=t,next_singleton=m,background=background,
            fixed_phase_positions={str(i):v for i,v in fixed.items()},free_phase_indices=free,
            variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),phase_K=34 if background else 10,
            selected_phase_count=10,free_selected_count=remainder,selected_anchor_count=t+1,
            counter_levels=levels,outside_singleton_clauses=len(outside),new_outside_singleton_clauses=len(outside-core),
            actual_TWO_cut=True,actual_FOURTH4_cut=True,actual_at_most_one_long_run_cut=True,
            only_global_y0_zero=True,root57_color_cut=True,minimum_distance=1,
            next_phase_after_singleton_fixed_background=True,proposed_global_no_adjacency_cut=False,
            proposed_no_run45_cut=False,new_length6_exclusion_used_as_input=False,
            unrelated_family_cut=False,premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False))
    out=dict(agent='six-vdw-2',role='researcher',status='GENERATED_NOT_AUDITED',
             producer_sha256=sha(Path(__file__)),records=records,seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);main(p.parse_args().work.absolute())
