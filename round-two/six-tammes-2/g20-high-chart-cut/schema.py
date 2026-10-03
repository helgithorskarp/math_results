"""The exact geometric scope and its closed rectangular cover."""
from fractions import Fraction as Q
from itertools import product
from frame import CORE,CONTACTS

def require(ok,message):
    if not ok:raise ValueError(message)

def box(row):
    require(type(row)is list and len(row)==4 and all(type(x)is str for x in row),'four exact rational endpoints')
    a,b,c,d=map(Q,row);require(a<b and c<d,'nondegenerate closed box')
    return a,b,c,d

def cover_check(system):
    ta,tb=map(Q,system['t_interval']);za,zb=map(Q,system['excluded_z_interval'])
    covers=system['closed_cover']
    require(type(covers)is list and len(covers)==3,'all three closed boxes')
    expected={
        'lower-corner':((ta,Q(113,200),za,Q(71,50)),[6,8]),
        'upper-t':((Q(113,200),tb,za,zb),[5,12]),
        'upper-z':((ta,tb,Q(71,50),zb),[5,12])}
    require({x['name'] for x in covers}==set(expected),'three different cover roles')
    rows=[]
    for x in covers:
        require(set(x)=={'name','box','contradicting_pair'},'typed cover row')
        b=box(x['box']);want,pair=expected[x['name']]
        require(b==want and x['contradicting_pair']==pair,'exact cover endpoint and packing pair')
        rows.append(b)
    # Membership in a union of axis-aligned closed boxes is constant on
    # every open elementary cell. Its boundary cells are checked too.
    xs=sorted({ta,tb}|{x for a,b,c,d in rows for x in (a,b)})
    ys=sorted({za,zb}|{y for a,b,c,d in rows for y in (c,d)})
    xs=sorted(set(xs+[(a+b)/2 for a,b in zip(xs,xs[1:])]))
    ys=sorted(set(ys+[(a+b)/2 for a,b in zip(ys,ys[1:])]))
    cells=0
    for x,y in product(xs,ys):
        if not (ta<=x<=tb and za<=y<=zb):continue
        require(any(a<=x<=b and c<=y<=d for a,b,c,d in rows),'uncovered elementary cell or boundary')
        cells+=1
    return cells

def validate(system):
    require(system['schema_version']==1,'scope version')
    require(system['actual_agent']=='six-tammes-2' and system['role']=='researcher','actual author and role')
    require(system['t_interval']==['14/25','593/1000'] and system['excluded_z_interval']==['7/5','5/2'],'entire original closed target')
    require(system['core_labels']==list(CORE),'all twelve original labels')
    contacts=system['required_contacts']
    require(type(contacts)is list and len(contacts)==20,'exactly twenty literal contacts')
    require(all(type(x)is list and len(x)==2 and all(type(y)is int for y in x) for x in contacts),'literal contact syntax')
    require(set(map(tuple,contacts))==set(CONTACTS),'original G20 and no added contact')
    for k in ('additional_contacts_allowed','other_points_arbitrary','no_additional_point_required'):
        require(system[k]is True,'arbitrary-point and additional-contact scope')
    require(system['imported_complete_branch']==[-1,1],'complete9774 surviving branch')
    require(system['necessary_core_chart']=='(1-t)^2*z^2<=1','necessary closed chart')
    require(system['necessary_core_regularity']=='2*G>(1+t)^4*C^2','necessary strict regularity')
    require(system['root_equation']=='w^2=(1-t)^2*(1+2t)*G' and system['root_sign']=='w>0','one positive radical')
    require(system['conclusion_is_global_Tammes_bound']is False,'conditional core reduction only')
    require(system['independent_new_result_review']=='pending' and system['formalization']=='unformalized','actual validation status')
    require(set(system)=={'schema_version','actual_agent','role','claim','t_interval','excluded_z_interval','core_labels','required_contacts','additional_contacts_allowed','other_points_arbitrary','imported_complete_branch','necessary_core_chart','necessary_core_regularity','root_equation','root_sign','no_additional_point_required','closed_cover','conclusion_is_global_Tammes_bound','independent_new_result_review','formalization'},'no hidden cohort, addition or scope field')
    return cover_check(system)
