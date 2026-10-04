"""Untrusted residual-certificate producer, standard library only.

The inverse generation openly adapts D3's published10326 Gauss-Jordan
producer. No ancestor executable/data, reviewer code or PSD factors are
opened. The separate checker never imports this program.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import json


def produce():
    bad = sorted([sum(1 << i for i in pair) for pool in [range(3,12),range(12,21)]
                  for pair in combinations(pool,2)] + [6+(1 << i) for i in range(12,21)])
    seen = {bad[0]}; queue = [bad[0]]; pivots = []
    for u in queue:
        for v in bad:
            if v not in seen and not u & v:
                seen.add(v); queue.append(v); pivots.append(sorted([u,v]))
    pivots.append([12288,49152]); n=len(bad)
    rows = [[F(int(v in e)) for e in pivots] +
            [F(int(i==j)) for j in range(n)] for i,v in enumerate(bad)]
    for j in range(n):
        p=next(i for i in range(j,n) if rows[i][j])
        rows[j],rows[p]=rows[p],rows[j]
        a=rows[j][j]; rows[j]=[v/a for v in rows[j]]
        for i in range(n):
            if i!=j and rows[i][j]:
                a=rows[i][j]; rows[i]=[v-a*w for v,w in zip(rows[i],rows[j])]
    inverse=[[2*v for v in r[n:]] for r in rows]
    if any(v.denominator!=1 for r in inverse for v in r):
        raise ValueError('inverse is not integral over2')
    return {
        'actual_agent':'six-downset-3','role':'researcher','q':18,'k':9,'actual_N':278,'s':58,
        'chart_graph':'bafkreihejcf55p7eu47ms5u4cxblknpmsf2hr7kdy5bwoj4lybbe54z6zm',
        'chart_source':'54ef84d14c0fb6133cbfb8ce6840bfe722226d61',
        'center_graph':'bafkreiarggds2lrbkbbbv5amnjomopfsm32gm4btoez2mzia6cezceknzq',
        'center_source':'df5a588c88f57babcb489c8690399fa5be50a0f7',
        'parent_center_and_PSD_not_rechecked':True,
        'real_tau_interval':['0','1/64'],'eta':'1/1048576',
        'center_proper_floor':'39/4096','center_actual_C_unit_surplus':'9/1048576',
        'bad_vertex_order':bad,'pivot_edge_order':pivots,'inverse_denominator':2,
        'twice_inverse_rows':[' '.join(str(int(v)) for v in r) for r in inverse],
        'residual_denominator':2,'sigma_pivot_multiplier':1,'sigma_gauge_numerator':-1,
        'mixed_edge_numerator':-2,'mixed_pivot_multiplier':1,'mixed_gauge_numerator':1,
        'loop_gauge_numerator':-1,'empty_row_multiplier':-1,'empty_loop_multiplier':1,
        'good_gauge_masks':[2,4],'trace_support_edge_count':16894,'trace_coefficient':1361,
        'local_radius_eta_denominator_power':12,'lift_operator_square':278,
        'proper_operator_cost_coefficient':'10','actual_entry_cost_coefficient':'2',
        'M_entry_cost_coefficient':'1/110','M_operator_cost_coefficient':'139/11',
        'projected_NN_sign_margin':'1/4194304','projected_actual_C_unit_surplus':'1/131072',
        'projected_proper_floor':'1/128','other276_gap':'1/28160',
        'global_blend_coefficient':3,'global_M_entry_cost_coefficient':'346030081/110',
        'global_M_operator_cost_coefficient':'218628791/55'}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.write_text(json.dumps(produce(),sort_keys=True,indent=2)+'\n')
