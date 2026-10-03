"""Literal complete model contract; ordering of pair lists is immaterial."""
from fractions import Fraction as Q
from itertools import combinations,product
from model import CORE,CONTACTS,PAIRS

def require(ok,message):
    if not ok:raise ValueError(message)

def pairs(actual,expected,name):
    require(isinstance(actual,list) and all(isinstance(p,list) and len(p)==2 and all(type(i)is int for i in p) for p in actual),name+' typed pairs')
    require(len(actual)==len(expected) and set(map(tuple,actual))==set(expected),name+' complete literal set without duplicates')

def layout(s,data):
    require(s['format']=='bounded-twelve-core-arbitrary-three-polynomial-v1','typed full model')
    names=['t','z','w','u0','v0','u1','v1','u2','v2']
    require(s['variables']==names and len(set(s['variables']))==9,'nine distinct real variables')
    require(s['coefficient_ring']=='Z['+','.join(names)+']','integral nine-variable ring')
    require(s['original_core_labels']==list(CORE),'original twelve labels')
    pairs(s['original_twenty_contacts'],CONTACTS,'twenty contacts')
    pairs(s['core_packing_pairs'],PAIRS,'thirty-three cross tests')
    pairs(s['arbitrary_addition_core_pairs'],tuple(product(range(3),CORE)),'thirty-six added-core tests')
    pairs(s['arbitrary_addition_mutual_pairs'],tuple(combinations(range(3),2)),'three mutual tests')
    require(s['sole_frame_branch']==[-1,1],'original sole branch')
    require(s['radical_equalities']==['w^2=D*G'] and s['strict_radical_branch']=='w>0','positive scaled radical, no squared-sign ambiguity')
    for key,value in {'t_closed':['14/25','593/1000'],'z_closed':['-5/2','5/2'],'w_closed':['0','6'],'added_chart_coordinates_closed':['-16/5','16/5']}.items():
        require(s[key]==value,key+' exact closed bounds')
    require(s['core_chart_predicate']=='(1-t)^2*z^2<=1','full core chart')
    require(s['strict_core_regularization_predicate']=='2*G>(1+t)^4*C^2','imported strict whole-frame regularity')
    for key in ('unit_equations_for_additions_eliminated','w_zero_excluded','all_three_actual_additions_arbitrary','no_actual_point13_or_support_or_degree_hypothesis','local_gate9866_is_optional_future_stopping_lemma_and_not_model_constraint'):
        require(s[key] is True,key+' full scope')
    require(s['initial_added_point_proximity_required'] is False and s['symmetry_quotient_applied'] is False,'no additional proximity or symmetry restriction')
    require(s['root_quintic_for_controls']==[-1,-3,2,6,-1,13],'exact incumbent quintic')
    require(s['exact_z0_coefficients']==['-115/16','-4','215/8','-37/2','637/16'],'incumbent chart')
    require(s['strict_improvement_additional_predicate']=='t<tau, with tau the distinguished exact quintic root; do not replace by either bracket endpoint','exact strict improvement, full critical strip')
    require(s['strict_improvement_integral_polynomial']=='13*t^5-t^4+6*t^3+2*t^2-3*t-1<0 (equivalent exactly to t<tau on I)','exact integral strict-improvement predicate')
    require(s['claim_kind']=='lossless bounded conditional polynomial reduction, not an UNSAT certificate or global bound','reduction claim status')
    require(data['format']=='fixed-twelve-three-completion-v1' and data['core_labels']==list(CORE),'credited fixture scope')
    require(data['root_bracket']==['0.59260590292507377809642492233275','0.59260590292507377809642492233276'],'exact distinguished root bracket')
    require(len(data['vectors'])==15 and all(len(v)==3 and all(isinstance(p,list) and len(p)==5 for p in v) for v in data['vectors']),'fifteen three-coordinate exact fixtures')
    require(len(data['alternate_last'])==3 and all(len(p)==5 for p in data['alternate_last']),'exact alternate fixture')
    return {'real_variables':9,'core_contacts':20,'core_packing_inequalities':33,'added_core_inequalities':36,'added_mutual_inequalities':3,'explicit_cleared_packing_inequalities':72,'core_chart_packing_inequality':1,'packing_inequalities_including_chart':73,'core_radical_equalities':1,'added_unit_equations':0}
