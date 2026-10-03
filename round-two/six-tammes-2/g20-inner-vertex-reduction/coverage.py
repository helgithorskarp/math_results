"""Complete literal active-triple census and elementary closed bounds."""
from fractions import Fraction as Q
from itertools import combinations
from frame import CORE,CONTACTS
from exact import require
PAIRS=((0,9),(1,8),(2,12),(4,10),(5,6),(7,11),(8,12),(98,99))
SHORT=((0,5,7),(0,5,11),(0,6,11),(1,2,4),(1,2,10),(1,10,12),(2,4,8),(5,9,11))
FIELDS={'schema_version','actual_agent','role','t_interval','z_interval','intervals_closed','required_labels','original_contacts','other_points','extra_contacts_allowed','normalization_imports','sheet','root','regularity','additional_hypotheses','conclusion','global_bound_claimed','cap_planes','incompatible_pairs','all_low_A_triple','equilateral_short_triples','critical_short_triple','residual_triples','Farkas_positive_factors','alternate_bound2_closed_cover'}

def validate(s):
    require(set(s)==FIELDS,'entire closed-scope system fields')
    expected={'schema_version':1,'actual_agent':'six-tammes-2','role':'researcher','t_interval':['14/25','593/1000'],'z_interval':['6/5','7/5'],'intervals_closed':True,'required_labels':list(CORE),'original_contacts':[list(x) for x in CONTACTS],'other_points':'three_arbitrary_unit_points_with_all_pair_products_at_most_t','extra_contacts_allowed':True,'normalization_imports':[9774,9912],'sheet':[-1,1],'root':'w>0; w*w=R','regularity':'2G-a^4 C^2>0','additional_hypotheses':[],'conclusion':'necessary_260_regular_vertex_systems_only','global_bound_claimed':False,'cap_planes':[{'label':98,'normal':[-8,12,-5],'rhs':9},{'label':99,'normal':[-5,-14,20],'rhs':15}],'incompatible_pairs':[list(x) for x in PAIRS],'all_low_A_triple':[6,7,9],'equilateral_short_triples':[list(x) for x in SHORT],'critical_short_triple':[4,7,99],'alternate_bound2_closed_cover':[['14/25','1153/2000','6/5','13/10'],['14/25','1153/2000','13/10','7/5'],['1153/2000','593/1000','6/5','7/5']]}
    require(all(s[k]==v for k,v in expected.items()),'literal scope, endpoints, contacts, caps and closed cover')
    require(set(s['Farkas_positive_factors'])=={'delta','C0','C4','C6','margin'} and all(type(v)is list and all(type(x)is str for x in v) for v in s['Farkas_positive_factors'].values()),'all positive-factor obligations')
    return tuple(map(Q,s['t_interval'])),tuple(map(Q,s['z_interval']))

def census(s,reverse=False):
    validate(s);labels=(*CORE,98,99);edges=set(CONTACTS)
    cliques=tuple(t for t in combinations(CORE,3) if all(p in edges for p in combinations(t,2)))
    require(cliques==SHORT,'exactly eight required-contact cliques; no1-7 equality premise')
    if reverse:
        triples=[]
        for k in range(len(labels)-1,1,-1):
            for j in range(k-1,0,-1):
                for i in range(j-1,-1,-1):triples.append((labels[i],labels[j],labels[k]))
        triples=sorted(triples)
    else:triples=list(combinations(labels,3))
    paircut=[t for t in triples if any(i in t and j in t for i,j in PAIRS)]
    low=[t for t in triples if t not in paircut and t==(6,7,9)]
    short=[t for t in triples if t not in paircut and t not in low and t in SHORT]
    critical=[t for t in triples if t not in paircut and t not in low and t not in short and t==(4,7,99)]
    residual=[t for t in triples if t not in paircut+low+short+critical]
    require((len(triples),len(paircut),len(low),len(short),len(critical),len(residual))==(364,94,1,8,1,260),'complete disjoint census')
    require(s['residual_triples']==[list(t) for t in residual],'entire literal260-branch list')
    return {'all_active_triples':364,'incompatible_pair_triples':94,'all_low_A_triples':1,'short_equilateral_triples':8,'critical_short_triples':1,'residual_regular_branches':260,'all_closed_seams_retained':True}

def elementary(s):
    (a,b),_=validate(s);rlo=2*a/(1+a);rhi=2*b/(1+b)
    require(0<a<=b<1 and Q(1,2)<rlo<=rhi<1,'closed t/r elementary inequalities')
    # Positive factors J and Q: J' >=27a^2-2b-1>0; aQ=D(az-1)^2+4t^2.
    jp=27*a*a-2*b-1;jlo=9*a**3-a*a-a+1
    require(jp>0 and jlo>0 and 5*a*a-1>0 and 2*(2*b+1)*(b-1)<0,'positive J and the longer circuit coefficient between0and1')
    eqmargin=1+2*b-6*b*b;require(eqmargin>0 and 12*a-2>0,'all equilateral norms strictly below1/2')
    caps=[]
    for label,h,q0,q1 in [(98,9,233,232),(99,15,621,620)]:
        # 2h^2-(1+t)(q0-q1*t), increasing since its derivative is positive.
        derivative=2*q1*a+(q1-q0);minimum=2*h*h-(1+a)*(q0-q1*a)
        require(derivative>0 and minimum>0 and q0-q1*b>h*h,'strict open-cap packing margin on both closed endpoints')
        caps.append({'label':label,'normal_squared_constant':q0,'normal_squared_negative_t_coefficient':q1,'rhs':h,'packing_margin_lower':str(minimum),'derivative_lower':str(derivative)})
    require(caps[0]['packing_margin_lower']=='747/625' and caps[1]['packing_margin_lower']=='2859/125','literal cap margins')
    return {'r_interval':list(map(str,(rlo,rhi))),'J_positive_lower':str(jlo),'J_derivative_lower':str(jp),'equilateral_norm_half_margin':str(eqmargin),'open_caps':caps}
