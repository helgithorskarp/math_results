"""Physical-input and proof-scope controls; these are not peer review."""
import copy
import itertools
import json
from pathlib import Path
import produce
import verify
from conclude import conclusion

def require(condition,message):
    if not condition:raise ValueError(message)
def rejects(function,value):
    try:function(value)
    except ValueError:return
    raise ValueError('semantic damage was accepted')

def run(data,inventory):
    checks=[]
    for damage in ('missing_quadruple','repeated_quadruple','repeated_pair','out_of_domain'):
        bad=copy.deepcopy(data)
        if damage=='missing_quadruple':bad['stars'][0].pop()
        elif damage=='repeated_quadruple':bad['stars'][0][1]=bad['stars'][0][0][:]
        elif damage=='out_of_domain':bad['stars'][0][0][0]=17
        else:
            p,q=bad['stars'][0][0][:2]
            others=[v for v in range(17) if v not in (p,q)]
            bad['stars'][0][1]=[p,q]+others[:2]
        rejects(produce.rows_from_data,bad);rejects(verify.literal_rows,bad)
        checks.append('physical_'+damage)
    transported_rows=0
    for mapping in ([16-p for p in range(17)],[(3*p+7)%17 for p in range(17)]):
        moved=copy.deepcopy(data)
        moved['stars']=[[[mapping[p] for p in reversed(word)] for word in reversed(star)]
                        for star in data['stars']]
        first=produce.rows_from_data(moved);second=verify.literal_rows(moved)
        require(produce.canonical(first)==verify.CANON(second),'actual point transport disagrees')
        require(produce.canonical(produce.inventories(first))==verify.CANON(inventory),'point transport changes whole inventory')
        transported_rows+=len(first)
    checks.append('two_actual_point_bijections_on_all23_stars_and426_marks')
    rows=produce.rows_from_data(data)
    require(any(row['e']==4 and row['h']==1 for row in rows),'actual missing-link-point category omitted')
    failures=[row for row in rows if row['margin']<0]
    require(len(failures)==8 and all(row['k']==5 and row['margin']==-3 for row in failures),'actual five-hub scope failures omitted')
    checks+=['retain_actual_e4_rows','retain_all_eight_actual_k5_failures']
    for damage in ('omit_last_template','omit_branch','alter_eligibility','alter_weight','alter_tau'):
        bad=copy.deepcopy(inventory)
        branch=next(b for b in bad['branches'] if b['Q']==5)
        survivor=next(t for t in branch['templates'] if not t['failures'])
        if damage=='omit_last_template':branch['templates'].remove(survivor)
        elif damage=='omit_branch':bad['branches'].pop(0)
        elif damage=='alter_tau':branch['tau']=1
        else:
            i=next(i for i,c in survivor['population'] if bad['types'][i]['e']==1)
            if damage=='alter_eligibility':bad['types'][i]['eligible']=False
            else:bad['types'][i]['ss_hist']=[2,1,0,0,0]
        rejects(conclusion,bad);checks.append('final_bridge_'+damage)
    # A contracted Mobius-Kantor graph satisfies degree/girth and weighted
    # matching checks of the old Q0 survivor but fails radius-two coverage.
    # It is a graph-only countermodel, not a code or a star realization.
    edges=set()
    def vertex(layer,i):return 0 if i==0 else i if layer==0 else 7+i
    for i in range(8):
        for a,b in (((0,i),(0,(i+1)%8)),((0,i),(1,i)),((1,i),(1,(i+3)%8))):
            u,v=vertex(*a),vertex(*b)
            if u!=v:edges.add(tuple(sorted((u,v))))
    adjacency=[set() for _ in range(15)]
    for u,v in edges:adjacency[u].add(v);adjacency[v].add(u)
    require(len(edges)==23 and sorted(map(len,adjacency))==[3]*14+[4],'countermodel degree inventory')
    for u in range(15):
        require(not any(v in adjacency[w] for v,w in itertools.combinations(adjacency[u],2)),'countermodel triangle')
        for v in range(u+1,15):require(len(adjacency[u]&adjacency[v])<=1,'countermodel four-cycle')
    reached={0}|adjacency[0]|set().union(*(adjacency[v] for v in adjacency[0]))
    require(len(reached)==13,'countermodel actual radius')
    checks.append('degree_and_girth_alone_do_not_imply_global_star_coverage')
    # Distinct neighbours are essential: one eligible unit cannot use one
    # noneligible neighbour four times. Both different implementations reject.
    types=inventory['types']
    a=next(t for t in types if t['e']==0 and t['k']==1 and t['q']==0)
    b=next(t for t in types if t['e']==1 and t['k']==1 and t['q']==1 and t['ss_excess']==0)
    require('too_few_weighted_partners' in produce.necessary_failures([a,b]),'distinct-neighbour producer')
    ia,ib=types.index(a),types.index(b)
    require('too_few_weighted_partners' in verify.audit_population(types,[(ia,1),(ib,1)]),'distinct-neighbour auditor')
    checks.append('one_endpoint_cannot_be_repeated_as_four_neighbours')
    return dict(status='PASS',checks=checks,checks_count=len(checks),
                transported_physical_row_records=transported_rows,
                graph_only_countermodel_vertices=15,graph_only_radius_covered=13)
