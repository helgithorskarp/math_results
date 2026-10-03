"""Literal claim and complete interval/triple-cover validation."""
from itertools import combinations
from fractions import Fraction as Q
from model import LABELS,CONTACTS,NORMAL,CUT
from algebra import LO,HI,require

FORMAT='derived-g24-one-cap-v1'
def system():
    return {'format':FORMAT,'closed_parameter_interval':[str(LO),str(HI)],
            'core_labels':list(LABELS),'literal_contacts':[list(x) for x in CONTACTS],
            'fresh_label13_means':'the x forced by2-x,9-x,10-x; different older G24 mask',
            'fixed_coefficient_normal':list(NORMAL),'cut_bound':CUT,
            'short_norm_squared_bound':'49/50','positive_dependence_labels':[0,4,9,11],
            'all_additional_points':'arbitrary unit vectors avoiding all13 core points',
            'extra_contact_or_face_or_degree_premise_for_capacity':False,
            'capacity_claim':'at most one additional code point; total cardinality<=14',
            'global_Tammes_bound_claimed':False,'optimizer_motif_occurrence_claimed':False,
            'normalization':'basis(p1,p2,p4), H_t=(1-t)Id+t11^T; no orientation quotient',
            'cap_plane_label':99,'parameter_cover_max_depth':9,
            'singular_case':'identically zero determinant; a vertex needs an independent triple',
            'infeasible_case':'two inactive Cramer residuals of opposite strict signs',
            'short_case':'49D^2-50<W,W>_t>0 on the entire closed cell'}

def validate_system(s):
    def typed(x):
        require(not isinstance(x,float),'no floating proof input')
        if isinstance(x,dict):
            for v in x.values():typed(v)
        elif isinstance(x,list):
            for v in x:typed(v)
    typed(s)
    require(s==system(),'exact literal system/scope/closed-band agreement')

def validate_cover(leaves):
    require(type(leaves)is list and bool(leaves),'nonempty parameter cover')
    paths=[]
    for l in leaves:
        require(type(l)is dict and l.get('type') in ('N','I2'),'known leaf predicate')
        p=l.get('path');require(type(p)is list and len(p)<=9 and all(type(b)is int and b in (0,1) for b in p),'binary closed-cell path')
        paths.append(tuple(p))
        keys={'path','type'} if l['type']=='N' else {'path','type','positive_residual','negative_residual'}
        require(set(l)==keys,'complete literal leaf fields')
    require(len(set(paths))==len(paths),'unique parameter cells')
    paths=set(paths)
    def walk(prefix):
        if prefix in paths:
            require(not any(len(p)>len(prefix) and p[:len(prefix)]==prefix for p in paths),'prefix-free parameter cover')
            return
        require(any(p[:len(prefix)]==prefix for p in paths) and len(prefix)<9,'complete binary cover, no missing branch')
        walk(prefix+(0,));walk(prefix+(1,))
    walk(())

def validate(c):
    require(type(c)is dict and set(c)=={'system','boundedness_determinant_sign','records'},'complete certificate fields')
    validate_system(c['system'])
    require(type(c['boundedness_determinant_sign'])is int and c['boundedness_determinant_sign'] in (-1,1),'boundedness orientation')
    records=c['records'];require(type(records)is list,'triple census')
    expected=set(combinations(tuple(LABELS)+(99,),3));seen=set()
    for r in records:
        require(type(r)is dict and type(r.get('triple'))is list and len(r['triple'])==3 and all(type(x)is int for x in r['triple']),'three literal integer labels')
        inds=tuple(r['triple']);require(inds in expected and inds not in seen,'complete unique ordered triple census');seen.add(inds)
        if r.get('type')=='S':require(set(r)=={'triple','type'},'singular record fields')
        else:
            require(r.get('type')=='COVER' and set(r)=={'triple','type','leaves'},'triple closed cover fields');validate_cover(r['leaves'])
            for l in r['leaves']:
                if l['type']=='I2':
                    j,k=l['positive_residual'],l['negative_residual']
                    require(type(j)is int and type(k)is int and j!=k and j not in inds and k not in inds and j in LABELS+(99,) and k in LABELS+(99,),'two different inactive residual planes')
    require(seen==expected and len(records)==364,'ALL364 triples, no incomplete enumeration')
