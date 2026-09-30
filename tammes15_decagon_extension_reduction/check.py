#!/usr/bin/env python3
"""Exact complete480-triple continuous extension reduction, using stdlib only."""
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path
import argparse,copy,json
from family import dot,t,one
from fractions import Fraction
from polynomial import need,F,ROOT_LO,ROOT_HI,value,bernstein,primitive,root_count
from polytope import core,origin_relation,active_triple,ordinary,sign,code,encode

KEYS=((2,1,1),(3,1,1),(6,50,-1),(6,1,1))

def audit_type(entry):
    need(set(entry)=={'key','aliases','canonical_mask','origin_tetrahedron','cover'},'type fields')
    points,mask,mapping=core(entry['key'],entry['aliases']);need(mask==entry['canonical_mask'],'canonical mask')
    weights=origin_relation(points,entry['origin_tetrahedron']);labels=sorted(points)
    cover={tuple(z[:3]):z[3:] for z in entry['cover']}
    need(len(cover)==len(entry['cover'])==120 and list(cover)==list(combinations(labels,3)),'complete ordered120-triple cover')
    vertices={};rejected=0
    for triple,witness in cover.items():
        normals,d,numer=active_triple(points,triple);need(d.n,'not identically singular')
        if witness[0]==1:
            need(len(witness)==3 and witness[1] in points and witness[2] in points,'opposite-side witness format')
            a,b=witness[1:]
            need(sign(t*d-ordinary(normals[a],numer))==1 and sign(t*d-ordinary(normals[b],numer))==-1,'opposite signed sides')
            rejected+=1;continue
        need(witness==[0],'feasible row format');y=[x/d for x in numer]
        need(all(sign(type(t)(x.d)) in (-1,1) for x in y),'vertex coordinate denominators')
        need(all(not (ordinary(normals[j],y)-t).n for j in triple),'active constraints')
        need(all(sign(t-ordinary(n,y)) in (0,1) for n in normals.values()),'vertex feasibility')
        position=sign(dot(y,y)-one);need(position in (-1,1),'strict norm classification')
        row=vertices.setdefault(code(y),{'y':y,'outside':position==1,'triples':[],'independent':[]})
        row['triples'].append(list(triple))
        if sign(d) in (-1,1):row['independent'].append(list(triple))
    rows=list(vertices.values());need(all(z['independent'] for z in rows),'every real vertex has uniform independent triple')
    for a,b in combinations(rows,2):need(any(sign(x-y) in (-1,1) for x,y in zip(a['y'],b['y'])),'uniform vertex distinctness')
    outside=[z for z in rows if z['outside']];need(len(outside)==4,'four exterior vertices')
    return {'key':entry['key'],'canonical_mask':mask,'total_triples':120,'opposite_side_triples':rejected,'feasible_triples':120-rejected,'vertices':len(rows),'inside_vertices':len(rows)-4,'exterior_vertices':4,'origin_tetrahedron':entry['origin_tetrahedron'],'origin_weights':[encode(x) for x in weights],'exterior_seed_triples':[z['independent'][0] for z in outside]},points,mapping,outside

def verify(data):
    need(set(data)=={'version','types','six_alias_cases'} and data['version']==1,'certificate fields')
    need([tuple(z['key']) for z in data['types']]==list(KEYS),'four representative keys')
    cases=data['six_alias_cases'];need(len(cases)==6 and len({tuple(z[:3]) for z in cases})==6,'six alias cases')
    summaries=[];reps={}
    for entry in data['types']:
        summary,points,mapping,outside=audit_type(entry);summaries.append(summary);reps[summary['canonical_mask']]=(points,mapping)
    need(len(reps)==4,'four distinct contact types')
    for p,c,sg,aliases in cases:
        points,mask,mapping=core((p,c,sg),aliases);need(mask in reps,'six-case representative cover')
        rp,rm=reps[mask];inverse={j:i for i,j in rm.items()};corr={i:inverse[j] for i,j in mapping.items()}
        need(all(not (dot(points[i],points[j])-dot(rp[corr[i]],rp[corr[j]])).n for i,j in combinations(sorted(points),2)),'exact Gram isometry throughout interval')
    assignments=list(combinations_with_replacement(range(4),5))
    need(len(assignments)==56 and set(assignments)=={tuple(sorted(z)) for z in product(range(4),repeat=5)},'complete unlabeled56-cap-assignment cover')
    need(all(x>0 for x in bernstein(tuple(i*F[i] for i in range(1,len(F))))) and value(F,ROOT_LO)<0<value(F,ROOT_HI),'F increasing, incumbent isolating signs')
    return {'agent':'six-tammes-2','role':'researcher','status':'AUTHOR_AUDITED_EXACT_224_SYSTEM_REDUCTION','types':summaries,'six_placements_exactly_isometric_to_four_representatives':True,'polytope_interval':[[1,2],[3,5]],'closed_cap_cover_threshold':1,'cap_assignments_per_type':56,'semialgebraic_systems':224,'variables_per_system':16,'strict_improvement_encoding':'225t-113>=0,2t-1>0,3-5t>0,F(t)<0; five3-vectors with unit H norms,core and pair packing inequalities,and assigned exteriorvertex dot>=1.','scope':'Exact conditional equivalence for these decagon cores. Systems have NOT been solved. No15-extension exclusion,global optimizer occurrence or numerical bound improvement. Independent mathematical review pending.'}

def controls(data):
    need(primitive((-1,))==(1,),'constant normalization')
    need(root_count((-1,2))==root_count((-3,5))==0 and root_count((1,-4,4),Fraction(0),Fraction(1))==1,'Sturm endpoints and multiple roots')
    for kind in ('missing_row','duplicate_row','reversed_sides','false_origin','false_alias','wrong_mask','missing_type','duplicate_six'):
        bad=copy.deepcopy(data);entry=bad['types'][0]
        if kind=='missing_row':entry['cover'].pop()
        elif kind=='duplicate_row':entry['cover'].append(entry['cover'][0])
        elif kind=='reversed_sides':
            row=next(z for z in entry['cover'] if z[3]==1);row[4],row[5]=row[5],row[4]
        elif kind=='false_origin':entry['origin_tetrahedron']=[0,1,7,11]
        elif kind=='false_alias':entry['aliases'][0][0]=2
        elif kind=='wrong_mask':entry['canonical_mask']^=1
        elif kind=='missing_type':bad['types'].pop()
        else:bad['six_alias_cases'][-1]=copy.deepcopy(bad['six_alias_cases'][0])
        try:verify(bad)
        except ValueError:pass
        else:raise ValueError('false '+kind+' certificate accepted')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    data=json.loads(Path(__file__).with_name('certificate.json').read_text());result=verify(data)
    if args.selftest:controls(data)
    print(json.dumps(result,indent=2,sort_keys=True))
