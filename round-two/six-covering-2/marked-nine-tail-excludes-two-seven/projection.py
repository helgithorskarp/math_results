"""Branch-coupled rectangle-projection bounds for every surviving original role."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import lcm,prod
from pathlib import Path

LITERAL=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
BASE_PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))


def generate(cap):
    if cap['domain']['literal_prefix']!=list(map(list,LITERAL)) or cap['uniform_parent6_upper']>=117:
        raise ValueError('Predecessor literal/capacity certificate not applicable')
    R6=tuple(x for x in range(6,2520,8) if all(x%m!=a for m,a in BASE_PREFIX))
    grid_rows=[]
    for e,nines in ((0,(3,6)),(2,(2,5,8))):
        actual=sorted([x%9,x%5,x%7] for x in R6 if x%3==e)
        expected=sorted(map(list,product(nines,range(5),range(1,7))))
        if actual!=expected:raise ValueError('Literal physical parent not the complete product grid')
        grid_rows.append([e,actual])
    C={d:max(pops) for d,pops in cap['all_single_phase_populations']}
    U={tuple(g):v for g,v in cap['all_partition_union_upper_bounds']}
    @lru_cache(None)
    def rectangle(group,e):
        shape=(2 if e==0 else 3,5,6);N=prod(shape)
        if not group:return 0
        if 3 in group:return N
        axes=[tuple(i for i,v in enumerate((9,5,7)) if d%v==0) for d in group]
        if any(not a for a in axes):raise ValueError('Invalid branch-projected cofactor')
        bounds=[]
        for assignment in product(*axes):
            multiplicities=[assignment.count(i) for i in range(3)]
            bounds.append(N-prod(max(0,a-b) for a,b in zip(shape,multiplicities)))
        return min(bounds)
    def qp(Qa,Qb):
        return min(U[Qa],U[Qb],sum(C[lcm(a,b)] for a in Qa for b in Qb))
    inventories=[];roles=0;coupled=0;maximum=0;high=[]
    for inventory_index,(H,Q,_,_) in enumerate(cap['survivors_ge87']):
        H=tuple(H);Q=tuple(Q);rows=[]
        branch_positions=[i for i,d in enumerate(H+Q) if d%3==0]
        for hb in product((0,1),repeat=len(H)):
            HA=tuple(d for d,b in zip(H,hb) if b==0)
            HB=tuple(d for d,b in zip(H,hb) if b==1)
            for qr in product((0,1,2),repeat=len(Q)):
                roles+=1
                Qa=tuple(d for d,b in zip(Q,qr) if b==0)
                Qb=tuple(d for d,b in zip(Q,qr) if b==1)
                QB=tuple(d for d,b in zip(Q,qr) if b==2)
                global_cap=min(150,U[HA]+qp(Qa,Qb),U[HB]+U[QB]) if QB else 0
                branch_rows=[]
                if global_cap>=87:
                    for branches in product((0,2),repeat=len(branch_positions)):
                        fixed=dict(zip(branch_positions,branches));bounds=[]
                        for e in (0,2):
                            ah=tuple(d for i,d in enumerate(H) if hb[i]==0 and (d%3 or fixed[i]==e))
                            bh=tuple(d for i,d in enumerate(H) if hb[i]==1 and (d%3 or fixed[i]==e))
                            a=tuple(d for j,d in enumerate(Q) if qr[j]==0 and (d%3 or fixed[len(H)+j]==e))
                            b=tuple(d for j,d in enumerate(Q) if qr[j]==1 and (d%3 or fixed[len(H)+j]==e))
                            same=tuple(d for j,d in enumerate(Q) if qr[j]==2 and (d%3 or fixed[len(H)+j]==e))
                            # Every two-arm intersection is empty or one LCM row.
                            opposite_group=tuple(sorted(ah+tuple(lcm(x,y) for x in a for y in b)))
                            same_group=tuple(sorted(bh+same))
                            opposite=rectangle(opposite_group,e);other=rectangle(same_group,e)
                            bounds.append([e,list(opposite_group),list(same_group),opposite,other,min(opposite,other)])
                        bound=min(global_cap,sum(row[-1] for row in bounds))
                        branch_rows.append([list(branches),bounds,bound]);coupled+=1;maximum=max(maximum,bound)
                        if bound>=87:high.append([inventory_index,list(hb),list(qr),list(branches),bound])
                else:maximum=max(maximum,global_cap)
                rows.append([list(hb),list(qr),global_cap,branch_rows])
        inventories.append({'H':list(H),'Q':list(Q),'branch_positions':branch_positions,'all_role_rows':rows})
    # Store all evaluated rectangle groups, each exact projection count reconstructible.
    groups=set()
    for block in inventories:
        for _,_,_,branch_rows in block['all_role_rows']:
            for _,bounds,_ in branch_rows:
                for e,a,b,_,_,_ in bounds:groups.add((tuple(a),e));groups.add((tuple(b),e))
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':'two-seven-projection',
        'domain':{'minimum_exactly':8,'original_moduli_divide':10080,'literal_prefix':list(map(list,LITERAL)),
                  'essential_originals':[16,32],'productive_TAILs_exactly':9,'counts_in_actual_hole_parents2_6':[2,7],
                  'BASE_lower_bound_imported':177,'parent2_original48_phase26_forced_by_checked_predecessors':True,
                  'productive_parent6_extras_exactly':6,'essential32_requires_missing_same_half_Q_arm':True,
                  'Q_in_placed_quarter_redundant_at_exact_minimum_count':True,
                  'cofactor_divisible_by3_productive_branch_choices':[0,2],
                  'all_original_odd_phases_and_omissions_free':True,'cross_H_Q_equal_cofactors_legal':True,
                  'unproductive_selected_tails_allowed':True,'actual_LCM_may_be_proper_divisor':True,
                  'ordinary_proof_formalized':False,'independent_person_reviewed':False,'global_bound_changed':False},
        'literal_product_grids':grid_rows,'original_six_extra_inventories':inventories,
        'all_projection_union_values':[[list(g),e,rectangle(g,e)] for g,e in sorted(groups)],
        'H_orientation_order':[14,6],'Q_quarter_order':[14,30,22],
        'inventory_count':len(inventories),'all_role_assignments':roles,'all_unpruned_mod3_phase_cases':coupled,
        'uniform_role_branch_upper':maximum,'survivors_ge87':high,'survivor_count':len(high),
        'entire_two_seven_excluded_by_projection':len(high)==0,'new_six_three_or126_numeric_input_used':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capacity',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();r=generate(json.loads(a.capacity.read_text()));a.out.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'inventories':r['inventory_count'],'roles':r['all_role_assignments'],
                      'coupled_cases':r['all_unpruned_mod3_phase_cases'],'upper':r['uniform_role_branch_upper'],
                      'survivors':r['survivor_count'],'excluded':r['entire_two_seven_excluded_by_projection'],
                      'sha256':sha256(a.out.read_bytes()).hexdigest()}))
