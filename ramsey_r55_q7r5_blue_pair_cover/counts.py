"""Exact carrier accounting; negative decisions still require the full proof audit."""
from pathlib import Path
from math import comb
import argparse,json
import problem

def calculate(root=None):
    records=json.loads((problem.HERE/'EXPECTED.json').read_text())['results']
    positive=[r for r in records if r['status'] in ['SAT_TAIL_ONLY','TAIL_UNDECIDED']]
    negative=[r for r in records if r['status']=='UNSAT_CHECKED']
    problem.require(len(records)==97 and len(positive)+len(negative)==97,'complete decisions')
    kept=sum(r['orbit_size'] for r in positive);removed=sum(r['orbit_size'] for r in negative)
    problem.require(kept+removed==37823,'complete matrix domain')
    # Four non-root red blocks, two blue blocks, and fifteen core vertices.
    size=comb(2001,4)*comb(1932,2)*37823**7*35714**8*15**105
    if root:
        table=json.loads((Path(root)/'ramsey_r55_maximal_block_order/TASKS.json').read_text())
        row=next(r for r in table['classes'] if (r['q'],r['r'])==(7,5))
        problem.require(row['per_task']==size and row['code_start']==0 and table['tasks']==2189178,'parent carrier count')
        old=json.loads((Path(root)/'ramsey_r55_q7r5_tail_decisions/TASKS.json').read_text())
        problem.require(4 not in old['excluded_core_indices'] and len(old['excluded_core_indices'])==518,'original task already retired')
    problem.require(size%37823==0,'coordinate divisibility');geometry=[]
    for record in positive:
        w=record['representative'];blue=[(i,j) for i in range(4) for j in range(4) if not(w>>(4*i+j)&1)]
        matching=len({i for i,j in blue})==len(blue)==len({j for i,j in blue})
        problem.require(matching and len(blue)<=3,'unexpected survivor geometry')
        geometry.append({'representative':w,'blue_cross_edges':[list(e) for e in blue],'matching_size':len(blue),'labeled_matrices':record['orbit_size']})
    problem.require(sorted(r['matching_size'] for r in geometry)==[0,1,2,3],'four matching types')
    return {'original_task':problem.TASK,'physical_orbit_classes':97,'closed_physical_classes':len(negative),'unknown_full43_classes':len(positive),'positive_tail_witnesses':sum(r['status']=='SAT_TAIL_ONLY' for r in positive),'undecided_tail_classes':sum(r['status']=='TAIL_UNDECIDED' for r in positive),'closed_labeled_pair_matrices':removed,'retained_labeled_pair_matrices':kept,'pair_domain_size':37823,'retained_fraction':f'{kept}/37823','geometric_consequence':'Blue cross edges between the two blue K4 blocks form a matching of size at most three. Four full43 types remain UNKNOWN; tail feasibility of size zero is not decided.','retained_geometry':geometry,'original_task_bare_carrier_size':size,'remaining_bare_carrier_cover':size//37823*kept,'removed_bare_carrier_codes':size//37823*removed,'original_task_global_interval_half_open':[4*size,5*size],'original_registry_total':2189178,'original_registry_excluded_before':518,'new_original_tasks_excluded':0,'original_registry_excluded_after':518,'original_registry_unknown_after':2188660,'q8_original_tasks':2185424,'q8_physical_jobs':956,'q10_closed_physical_children':99,'q10_unknown_physical_children':161,'q10_color_redirects_not_exclusions':94,'scope':'Exact one-coordinate cover reduction for original c000004 only; bare carrier codes are not good43 graphs. A complete physical-class refutation does not retire its original ID.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parent-root');p.add_argument('--output');a=p.parse_args();r=calculate(a.parent_root)
    if a.output:Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
