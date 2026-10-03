"""Literal parent scope and a complete disjoint five-case refinement."""
from fractions import Fraction as Q
from itertools import combinations
import hashlib,json
CORE=(0,1,2,4,5,6,7,8,9,10,11,12)
A=(0,5,6,7,9,11);B=(1,2,4,8,10,12)
CONTACTS=((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),(2,10),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(9,10),(9,11),(10,12))
CUTS=((0,6,7),(1,4,12),(2,8,10),(5,7,9),(6,9,11))
PARENT_SHA='de2b78260162b7b0a4482ba61ddc532c23783ed1e81f9b2e067c3c50badde1de'
RECIPES={'excess067':['a']*6+['b']*2+['c']*2+['3t-1','bz+1'],
         'excess579':['t']+['a']*10+['b']*2+['c']*2+['3t-1','bz+1','bz+1','Q'],
         'excess6911':['a']*5+['b']*2+['c']*2+['3t-1','bz+1'],
         'excess067_square':['a']+['b']*4+['c']*2+['J','Q'],
         'excess579_square':['a']*2+['b']*4+['c']*2+['J']}
SIGNS=[['excess067','B'],['excess067_square','A'],['excess579','B'],['excess579_square','A'],['excess6911','A'],['excess6911','B']]
def require(ok,message):
    if not ok:raise ValueError(message)

def validate(s,parent_bytes,reverse=False):
    require(hashlib.sha256(parent_bytes).hexdigest()==PARENT_SHA,'entire immutable parent system pin')
    p=json.loads(parent_bytes)
    expected={'schema_version':1,'actual_agent':'six-tammes-2','role':'researcher','t_interval':['14/25','593/1000'],'z_interval':['6/5','7/5'],
              'intervals_closed':True,'original_required_labels':list(CORE),'original_contacts':[list(x) for x in CONTACTS],
              'extra_contacts_allowed':True,'additional_hypotheses':[],'logical_imports':[9774,9912,10109],
              'root':'w>0; w*w=R','regularity':'2G-a^4 C^2>0','selected_Gram_rank':'strict_positive; zero_rank_is_only_an_ineligible_basis',
              'parent_system_sha256':PARENT_SHA,'new_excluded_triples':[list(x) for x in CUTS],
              'all_remaining_feasibility':'UNRESOLVED','three_arbitrary_packing_additions':'force_one_of255_necessary_parent_vertex_systems',
              'structural_conclusion':'every_long_vertex_uses_both_core_components_or_a_cap_plane',
              'capacity_claimed':False,'global_Tammes15_bound_claimed':False,'positive_factor_recipes':RECIPES,
              'square_integer_multipliers':{'excess067_square':1,'excess579_square':4},'strict_sign_obligations':SIGNS}
    require(set(s)==set(expected)|{'remaining_regular_triples'},'entire refined scope fields')
    require(all(s[k]==v for k,v in expected.items()),'literal hypotheses, closed endpoints, signed radical, rank and recipes')
    require(all(type(i)is int for i in s['original_required_labels']) and all(type(i)is int for x in s['original_contacts']+s['new_excluded_triples']+s['remaining_regular_triples'] for i in x),'integer original labels and triples')
    require(type(s['schema_version'])is int and all(type(s[k])is bool for k in ('intervals_closed','extra_contacts_allowed','capacity_claimed','global_Tammes15_bound_claimed')),'literal schema and scope booleans')
    labels=(*CORE,98,99);pairs=((0,9),(1,8),(2,12),(4,10),(5,6),(7,11),(8,12),(98,99))
    short=[q for q in combinations(CORE,3) if all(x in CONTACTS for x in combinations(q,2))]
    triples=list(combinations(labels,3))
    if reverse:triples=sorted(tuple(sorted(q)) for q in combinations(reversed(labels),3))
    previous=[q for q in triples if not any(i in q and j in q for i,j in pairs) and q not in short and q not in ((6,7,9),(4,7,99))]
    require(len(triples)==364 and len(short)==8 and len(previous)==260,'complete parent census')
    require(p['residual_triples']==[list(q) for q in previous],'all original260 literals regenerated')
    pure=[q for q in previous if set(q)<=set(A) or set(q)<=set(B)]
    require(tuple(pure)==CUTS,'exactly five parent component-only triples')
    remaining=[q for q in previous if q not in CUTS]
    require(len(remaining)==255 and s['remaining_regular_triples']==[list(q) for q in remaining],'all255 literals, no omitted surviving basis')
    require(all(98 in q or 99 in q or bool(set(q)&set(A)) and bool(set(q)&set(B)) for q in remaining),'all remaining bases mixed or cap-bearing')
    lo,hi=map(Q,s['t_interval']);rlo,rhi=2*lo/(1+lo),2*hi/(1+hi)
    require(0<lo<=hi<1 and Q(1,2)<rlo<=rhi<1,'closed component Gram and B-circuit guards')
    require(29*lo-15==Q(31,25) and 25*lo-9==5 and 5*lo*lo-1>0,'strict closed elementary cap/norm margins')
    jlo=9*lo**3-lo*lo-lo+1;jprime=27*lo*lo-2*hi-1
    require(jlo==Q(26671,15625) and jprime>0,'J strictly positive on whole closed interval')
    return {'all364_triples_regenerated':364,'imported_parent_residuals':260,'new_component_exclusions':5,'remaining_regular_systems':255,
            'all_component_only_supports_removed':True,'cap99_B_margin_lower':'31/25','cap98_B_margin_lower':'5',
            'r_closed_interval':list(map(str,(rlo,rhi))),'one_minus_r_squared_lower':str(1-rhi*rhi),
            'J_positive_lower':str(jlo),'J_derivative_lower':str(jprime),'closed_endpoints_retained':True}
