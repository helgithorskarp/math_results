#!/usr/bin/env python3
"""Exact complete overlap reduction; only Python integer/Fraction arithmetic."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse,copy,json
from field import Field,selftest as field_controls
from family import models,branch_rat,branch_field,dot,sign_open,t,one
from polynomial import need,F,ROOT_LO,ROOT_HI,primitive,pgcd,root_count,value,bernstein
import exception

FIELDS={'version','roots','active','zero_rejections','root_rejections','zero_aliases','disjoint_branches','exception_root'}
def allowed(pair):return pair[0]<8 and pair[1] in (8,9,10)

def root(entry):
    p=tuple(entry['polynomial']);lo,hi=(Fraction(*q) for q in entry['bracket'])
    need(len(p)>1 and all(type(x) is int for x in p) and primitive(p)==p,'root polynomial')
    need(Fraction(1,2)<lo<hi<Fraction(3,5),'root domain')
    need(value(p,lo)*value(p,hi)<0,'root endpoints')
    need(root_count(p)==root_count(p,lo,hi)==1,'root count')
    return p,lo,hi

def rat_points(model,case,orientation):
    points={**model['a'],**branch_rat(case,orientation)}
    need(all(not (dot(x,x)-one).n for x in points.values()),'continuous frame norms')
    return points

def uniform_rejection(points,pair):
    pair=tuple(pair);need(len(pair)==2 and 0<=pair[0]<pair[1]<13,'uniform pair format')
    g=dot(points[pair[0]],points[pair[1]])
    need(sign_open(g-t)==1,'uniform collision')
    if allowed(pair):need(sign_open(one-g)==1,'uniform collision is distinct despite permitted identification')

def root_rejection(points,f,pair):
    pair=tuple(pair);need(len(pair)==2 and 0<=pair[0]<pair[1]<13,'root pair format')
    g=f.dot(points[pair[0]],points[pair[1]])
    need(f.sign(f.sub(g,f.t))>0,'root collision')
    if allowed(pair):need(f.sign(f.sub(f.one,g))>0,'root collision is distinct despite permitted identification')

def decagon(edges,labels):
    edges=frozenset(edges);triangles=[p for p in combinations(labels,3) if all(e in edges for e in combinations(p,2))]
    counts=Counter(e for triangle in triangles for e in combinations(triangle,2));boundary={e for e in edges if counts[e]==1}
    need(len(edges)==17 and len(triangles)==8 and len(boundary)==10 and max(counts.values())==2,'decagon incidence')
    nb={i:{j for e in boundary if i in e for j in e if j!=i} for i in labels};need(all(len(z)==2 for z in nb.values()),'decagon boundary degrees')
    order=[min(labels)]
    while len(order)<10:
        options=nb[order[-1]]-set(order);need(options,'decagon boundary disconnected');order.append(min(options))
    need(order[0] in nb[order[-1]],'decagon boundary cycle')
    index={v:i for i,v in enumerate(order)};converted={tuple(sorted((index[i],index[j]))) for i,j in edges}
    need(not any(len(set(e+f))==4 and (e[0]<f[0]<e[1]<f[1] or f[0]<e[0]<f[1]<e[1]) for e,f in combinations(converted,2)),'decagon noncrossing diagonals')
    pairs=list(combinations(range(10),2))
    def mask(es):return sum(1<<k for k,e in enumerate(pairs) if e in es)
    def image(s,d):return {tuple(sorted(((s+d*i)%10,(s+d*j)%10))) for i,j in converted}
    canonical=min(mask(image(s,d)) for s in range(10) for d in (-1,1))
    return order,canonical,triangles

def alias(model,case,orientation,pairs):
    points=rat_points(model,case,orientation)
    need(len(pairs)==3 and {j for _,j in pairs}=={8,9,10} and len({i for i,_ in pairs})==3,'three distinct shared B anchors')
    mapping={i:i for i in range(13)}
    for i,j in pairs:
        need(type(i) is int and 0<=i<8 and j in (8,9,10),'alias domain')
        need(all(not (x-y).n for x,y in zip(points[i],points[j])),'alias coefficient identity')
        mapping[j]=i
    triangle=tuple(sorted(mapping[j] for j in (8,9,10)))
    prescribed_triangles={tuple(sorted(model['record']['anchors']))}|{tuple(sorted((v,i,j))) for v,i,j,old in model['record']['steps']}
    need(triangle in prescribed_triangles and all(e in model['record']['edges'] for e in combinations(triangle,2)),'B anchor triangle prescribed in A')
    quotient={mapping[i]:points[i] for i in range(13)};need(len(quotient)==10,'ten quotient positions')
    contacts=[]
    for i,j in combinations(sorted(quotient),2):
        g=dot(quotient[i],quotient[j]);need(sign_open(one-g)==1,'ten real positions distinct throughout interval')
        gap=t-g
        need(not gap.n or sign_open(gap)==1,'continuous quotient packing')
        if not gap.n:contacts.append((i,j))
    prescribed={tuple(sorted((mapping[i],mapping[j]))) for i,j in case['edges']}
    need(all(i!=j for i,j in prescribed) and prescribed==set(contacts),'exact seventeen quotient contacts')
    order,canonical,triangles=decagon(prescribed,sorted(quotient))
    need(triangle in triangles,'shared contact triangle')
    return {'shared_B_anchor_triangle':list(triangle),'anchor_aliases':pairs,'packing_points':10,'contacts':17,'boundary_order':order,'canonical_decagon_mask':canonical}

def tables(data):
    need(set(data)==FIELDS and data['version']==1,'certificate fields/version')
    roots=[root(x) for x in data['roots']];need(len(roots)==9,'nine-root table')
    def keyed(name,with_value=True):
        rows=data[name];out={tuple(row[:3]):row[3] if with_value else None for row in rows}
        need(len(out)==len(rows),'duplicate '+name+' key');return out
    zr=keyed('zero_rejections');za=keyed('zero_aliases');rr=keyed('root_rejections');db=keyed('disjoint_branches',False)
    need(len(zr)==8 and len(za)==6 and len(rr)==40 and len(db)==6,'branch table counts')
    need(not (set(zr)&set(za)) and not (set(rr)&set(db)),'branch tables disjoint')
    active={(p,c):r for p,c,r in data['active']};need(len(active)==len(data['active'])==26,'active root table')
    return roots,zr,za,rr,db,active

def verify(data):
    need(all(q>0 for q in bernstein(tuple(i*F[i] for i in range(1,len(F))))) and value(F,ROOT_LO)<0<value(F,ROOT_HI),'incumbent interval certification')
    roots,zr,za,rr,db,active=tables(data);used_zr=set();used_za=set();used_rr=set();used_db=set();used_active=set()
    rootless=above=incumbent=zeros=0;aliases=[]
    for p,model in enumerate(models()):
        for c,case in enumerate(model['cases']):
            numerator=primitive(case['residual'].n)
            if not numerator:
                zeros+=1
                for orientation in (-1,1):
                    key=(p,c,orientation)
                    need((key in zr)!=(key in za),'continuous branch cover')
                    if key in zr:uniform_rejection(rat_points(model,case,orientation),zr[key]);used_zr.add(key)
                    else:aliases.append({'key':list(key),**alias(model,case,orientation,za[key])});used_za.add(key)
                continue
            count=root_count(numerator)
            if count==0:rootless+=1;need((p,c) not in active,'spurious active row');continue
            need(count==1 and (p,c) in active,'complete scalar root cover');used_active.add((p,c))
            index=active[(p,c)];need(type(index) is int and 0<=index<len(roots),'root index');factor,lo,hi=roots[index]
            need(pgcd(numerator,factor)==factor,'residual/root identity')
            if factor==F:incumbent+=1;continue
            if lo>ROOT_HI:above+=1;continue
            need(hi<ROOT_LO,'strict improvement root comparison')
            f=Field(factor,data['roots'][index]['bracket'])
            for orientation in (-1,1):
                key=(p,c,orientation);need((key in rr)!=(key in db),'algebraic branch cover')
                points=branch_field(model,case,orientation,f)
                need(all(f.dot(x,x)==f.one for x in points.values()),'algebraic full frame norms')
                if key in rr:root_rejection(points,f,rr[key]);used_rr.add(key)
                else:
                    need(all(f.sign(f.sub(f.t,f.dot(points[i],points[j])))>=0 for i,j in combinations(range(13),2)),'disjoint branch packing proves no shared positions')
                    used_db.add(key)
    need((rootless,above,incumbent,zeros)==(322,2,1,7),'355-case scalar partition')
    need(used_zr==set(zr) and used_za==set(za) and used_rr==set(rr) and used_db==set(db) and used_active==set(active),'no unused certificate row')
    groups={}
    for row in aliases:groups.setdefault(row['canonical_decagon_mask'],[]).append(row['key'])
    need(len(groups)==4,'four decagon types')
    return {'agent':'six-tammes-2','role':'researcher','status':'AUTHOR_AUDITED_EXACT_OVERLAP_REDUCTION','old_neighbor_cases':355,'rootless':rootless,'above_incumbent':above,'incumbent_root':incumbent,'continuous_cases':zeros,'continuous_branches_rejected_with_overlaps':8,'continuous_shared_triangle_branches':aliases,'algebraic_branches_rejected_with_overlaps':40,'disjoint13_branches_using_prior_extension_theorem':6,'decagon_types':[{'canonical_mask':key,'branch_keys':value} for key,value in sorted(groups.items())],'exception':exception.verify(data['exception_root']),'scope':'B ears remain outside A; A and B each internally distinct. For strict incumbent improvements, vertex-disjointness is replaced by no common prescribed anchor triangle. Four continuous10-point types remain when that triangle is shared; no15-point extension or global bound is claimed for those survivors. Independent mathematical review pending.'}

def controls(data):
    field_controls();need(primitive((-1,))==primitive((1,))==(1,),'constant polynomial normalization')
    need(root_count((-1,2))==root_count((-3,5))==0 and root_count((1,-4,4),Fraction(0),Fraction(1))==1,'Sturm boundary/multiplicity')
    all_models=models();row=data['zero_aliases'][0];p,c,sg,pairs=row;model=all_models[p];case=model['cases'][c]
    bad=copy.deepcopy(pairs);bad[0][0]=(bad[0][0]+1)%8
    try:alias(model,case,sg,bad)
    except ValueError:pass
    else:raise ValueError('false alias accepted')
    points=rat_points(model,case,sg)
    try:uniform_rejection(points,pairs[0])
    except ValueError:pass
    else:raise ValueError('shared anchor falsely rejected as distinct collision')
    for name in ('zero_rejections','zero_aliases','root_rejections','disjoint_branches','active'):
        bad=copy.deepcopy(data);bad[name].append(copy.deepcopy(bad[name][0]))
        try:tables(bad)
        except ValueError:pass
        else:raise ValueError('duplicate '+name+' accepted')
    bad=copy.deepcopy(data['exception_root']);bad['root_bracket']=[[599,1000],[3,5]]
    try:exception.verify(bad)
    except ValueError:pass
    else:raise ValueError('false exceptional root accepted')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    data=json.loads(Path(__file__).with_name('certificate.json').read_text())
    if args.selftest:controls(data)
    print(json.dumps(verify(data),indent=2,sort_keys=True))
