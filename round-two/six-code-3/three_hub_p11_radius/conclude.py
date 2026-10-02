"""Check the exact hypotheses needed by the ordinary final K5 bridge."""
def require(condition,message):
    if not condition:raise ValueError(message)

def conclusion(inventory):
    survivors=[(branch,template) for branch in inventory['branches']
               for template in branch['templates'] if not template['failures']]
    require(len(inventory['branches'])==20,'all20 branches are required')
    require(sum(len(b['templates']) for b in inventory['branches'])==118,'full118 raw inventory')
    require(len(survivors)==1,'exactly one necessary surviving population')
    branch,template=survivors[0]
    require((branch['Q'],branch['T'],branch['X'],branch['tau'])==(5,0,0,0),'final branch hypotheses')
    actual=sorted((inventory['types'][i]['e'],inventory['types'][i]['k'],
                   inventory['types'][i]['q'],inventory['types'][i]['eligible'],
                   tuple(inventory['types'][i]['ss_hist']),c) for i,c in template['population'])
    require(actual==[(0,1,1,False,(4,0,0,0,0),5),
                     (1,1,0,True,(3,0,0,0,0),10)],'actual unit/nonunit closure hypotheses')
    # These integers encode the elementary proof in PROOF.md, not a
    # formalized theorem or an enumeration of physical global packings.
    return dict(branches=20,raw_templates=118,necessary_survivors_before_K5=1,
                unit_component_vertices=5,unit_component_degree=4,
                saturated_high_high_leave_edges_per_unit=3,
                forced_uncovered_unit_triangles=5,required_tau=0,
                three_hub_pair_total_lower_bound=11,
                status='AUTHOR_CHECKED_CONDITIONAL_EXACT_CERTIFICATE',
                independent_mathematical_review=False,ordinary_bridges_formalized=False)
