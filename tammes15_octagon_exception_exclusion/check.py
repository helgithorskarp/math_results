#!/usr/bin/env python3
"""Stdlib exact ten-template, two-frame and complete extension certificate audit."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse,json
from field import Field,selftest as field_controls
from rational import Rat
from polynomial import need,root_count,value,mul
from patches import catalog,coords,neighbors,dot,t,one,sign_open,REF,image
from geometry import lens,to_field,branch_field,sum_field

A_EDGES=frozenset(((0,1),(0,4),(0,5),(0,6),(0,7),(1,2),(1,3),(1,4),(2,3),(3,4),(4,5),(5,6),(6,7)))
B_EDGES=frozenset(((0,1),(0,2),(0,3),(0,4),(1,2),(2,3),(3,4)))
E=(2,7)
FIELDS={'version','root_polynomial','root_bracket','origin_tetrahedron','rejected_orientation','collision_pair','norm_squared_bound'}

def refine_root(p,bracket):
    need(len(bracket)==2 and all(len(q)==2 and all(type(c) is int for c in q) and q[1]>0 for q in bracket),'root bracket format')
    lo,hi=(Fraction(*q) for q in bracket)
    need(Fraction(1,2)<lo<hi<Fraction(3,5),'root bracket range')
    need(root_count(p)==root_count(p,lo,hi)==1,'root counts')
    sl,sh=value(p,lo),value(p,hi)
    need(sl*sh<0,'root endpoint signs')
    for _ in range(160):
        mid=(lo+hi)/2;sm=value(p,mid)
        need(sm!=0,'unexpected rational midpoint root')
        if sm*sl>0:lo,sl=mid,sm
        else:hi,sh=mid,sm
    need(root_count(p,lo,hi)==1,'refined root count')
    return Field(p,((lo.numerator,lo.denominator),(hi.numerator,hi.denominator)))

def schema():
    models,counts=catalog(8)
    need(counts['triangulations']==132 and counts['degree_compatible']==84 and counts['dihedral_models']==8,'A8 cover')
    aa=[m for m in models if m['edges']==A_EDGES]
    need(len(aa)==1 and aa[0]['type']==0,'exceptional model')
    A=aa[0];a=A['a'];nb=neighbors(A_EDGES,8)
    need(not nb[E[0]]&nb[E[1]],'exceptional pair has no old neighbor')
    b=coords(B_EDGES,5);bn=neighbors(B_EDGES,5)
    need([i for i in range(5) if len(bn[i])==2]==[1,4],'B ears')
    need(image(B_EDGES,(0,4,3,2,1))==B_EDGES,'B ear interchange')
    k=dot(b[1],b[4]);need(k==t*(9*t*t-2*t-3)/(one+t)**2,'B ear Gram formula')
    c,n,D=lens(a,*E);need(sign_open(D)==1,'exceptional lens real')
    entries=[]
    for i,j in combinations(range(8),2):
        old=nb[i]&nb[j]
        if len(old)!=1:continue
        extra=Counter(E+(i,j))
        if any(len(nb[z])+extra[z]>5 for z in range(8)):continue
        old=next(iter(old));w=dot(a[i],a[j]);need(sign_open(one+w)==1,'forced-ear divisor')
        v=[2*t/(one+w)*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
        need(dot(v,v)==one and dot(v,a[i])==dot(v,a[j])==t,'forced second ear')
        alpha=dot(c,v)-k;beta=dot(n,v);R=alpha*alpha-D*beta*beta
        edges=set(A_EDGES)|{(x+8,y+8) for x,y in B_EDGES}|{(2,9),(7,9),(i,12),(j,12)}
        need(len(edges)==24,'prescribed edge count')
        entries.append({'pair':(i,j,old),'v':v,'alpha':alpha,'beta':beta,'R':R,'edges':edges})
    need(len(entries)==10,'complete ten-template cover')
    model={'n':8,'A':{'a':a},'B':{'b':b,'edges':B_EDGES,'ears':(1,4),'kappa':k}}
    return entries,model,c,n,D

def prepare(data):
    need(set(data)==FIELDS and data['version']==1,'certificate fields/version')
    p=tuple(data['root_polynomial'])
    need(len(p)==16 and all(type(x) is int for x in p),'degree-15 polynomial format')
    f=refine_root(p,data['root_bracket'])
    entries,model,c,n,D=schema();active=[];signs=[]
    for index,entry in enumerate(entries):
        sign=sign_open(entry['R']);signs.append(sign)
        if sign==0:active.append((index,entry))
    need(len(active)==1 and active[0][0]==8 and active[0][1]['pair']==(5,6,0),'unique active template')
    index,entry=active[0]
    need(entry['R'].n==mul(mul((-1,1),(-1,1)),p),'complete residual polynomial identity')
    need(sign_open(Rat(entry['R'].d))!=0,'active residual denominator')
    need(sign_open(entry['alpha'])==-1 and sign_open(entry['beta'])==1,'physical radical signs')
    u=[x-(entry['alpha']/entry['beta'])*y for x,y in zip(c,n)]
    case={'u':u,'v':entry['v']}
    fu,fv=[tuple(to_field(f,x) for x in q) for q in (u,entry['v'])]
    need(not f.element(entry['R'].n) and bool(f.element(entry['R'].d)),'quotient residual')
    need(f.dot(fu,fu)==f.dot(fv,fv)==f.one,'forced ear unit norms')
    need(f.dot(fu,fv)==to_field(f,model['B']['kappa']),'unsquared ear Gram')
    need(f.sign(to_field(f,one-model['B']['kappa']**2))==1,'independent fixed ears')
    for z in E:need(f.dot(fu,tuple(to_field(f,x) for x in model['A']['a'][z]))==f.t,'exceptional ear contacts')
    need(data['rejected_orientation'] in (-1,1),'orientation format')
    pair=tuple(data['collision_pair'])
    need(len(pair)==2 and all(type(x) is int and 0<=x<13 for x in pair) and pair[0]<pair[1] and pair not in entry['edges'],'collision witness pair')
    branches={sg:branch_field(model,case,sg,f) for sg in (-1,1)}
    rejected=data['rejected_orientation']
    need(f.sign(f.sub(f.dot(branches[rejected][pair[0]],branches[rejected][pair[1]]),f.t))>0,'rejected orientation collision')
    good=branches[-rejected]
    need(all(f.dot(x,x)==f.one for x in good.values()),'all13 unit norms')
    need(all(f.dot(good[i],good[j])==f.t for i,j in entry['edges']),'all24 prescribed contacts')
    comparisons=[f.sign(f.sub(f.dot(good[i],good[j]),f.t)) for i,j in combinations(range(13),2)]
    contacts=comparisons.count(0)
    need(all(q<=0 for q in comparisons),'all78 packing inequalities; t<1 also forces distinct labels')
    return f,good,signs,contacts

def boundedness(f,points,labels):
    need(len(labels)==4 and len(set(labels))==4 and all(type(i) is int and 0<=i<13 for i in labels),'origin tetrahedron labels')
    chosen=[points[i] for i in labels]
    weights=[f.det3([chosen[j] for j in range(4) if j!=i]) for i in range(4)]
    weights=[f.neg(x) if i%2 else x for i,x in enumerate(weights)]
    total=sum_field(f,weights);weights=[f.div(x,total) for x in weights]
    need(all(f.sign(w)>0 for w in weights),'positive origin tetrahedron')
    need(sum_field(f,weights)==f.one,'tetrahedron weight sum')
    need(all(not sum_field(f,(f.mul(w,v[k]) for w,v in zip(weights,chosen))) for k in range(3)),'origin relation')

def extension(f,points,data):
    boundedness(f,points,data['origin_tetrahedron'])
    raw=data['norm_squared_bound']
    need(len(raw)==2 and all(type(q) is int for q in raw) and raw[1]>0,'norm bound format')
    bound=Fraction(*raw);need(0<bound<1,'strict unit exclusion bound')
    rows=[[sum_field(f,(f.mul(x,f.one if i==j else f.t) for j,x in enumerate(points[k]))) for i in range(3)] for k in range(13)]
    vertices={};counts={'singular':0,'infeasible':0,'feasible_triples':0}
    for triple in combinations(range(13),3):
        v=f.solve3([rows[i] for i in triple],[f.t]*3)
        if v is None:counts['singular']+=1;continue
        if any(f.sign(f.sub(f.dot(points[i],v),f.t))>0 for i in range(13)):
            counts['infeasible']+=1;continue
        need(f.sign(f.sub(f.dot(v,v),f.number(bound)))<0,'feasible vertex norm bound')
        counts['feasible_triples']+=1;vertices.setdefault(v,triple)
    need(sum(counts.values())==286 and vertices,'complete286 triple cover')
    for v,w in combinations(vertices,2):
        need(any(f.sign(f.sub(x,y))!=0 for x,y in zip(v,w)),'distinct vertices at the certified real root')
    return {**counts,'triples':286,'distinct_vertices':len(vertices),'norm_squared_upper_bound':raw,'additional_unit_points_at_most':0}

def verify(data):
    f,points,signs,contacts=prepare(data)
    return {'agent':'six-tammes-2','role':'researcher','status':'AUTHOR_AUDITED_EXACT_CERTIFICATE','templates':10,'scalar_residual_Bernstein_signs':signs,'active_template':8,'root_degree':15,'roots_open_half_three_fifths':1,'valid_orientation':-data['rejected_orientation'],'packing_points':13,'contacts':contacts,'extension':extension(f,points,data),'trust_boundary':'Unformalized geometric cover and ordinary exact Python execution; independent mathematical review pending. No global Tammes15 bound.'}

def controls(data):
    from copy import deepcopy
    field_controls()
    need(root_count(mul(mul((-1,2),(-1,2)),(-3,5)))==0,'endpoint root removal control')
    need(root_count(mul((-11,20),(-11,20)))==1,'multiple root control')
    changes=[('version',2),('root_bracket',[[599,1000],[3,5]]),('root_polynomial',[0]*15+[1]),('collision_pair',[0,1]),('rejected_orientation',-1)]
    for key,bad in changes:
        altered=deepcopy(data);altered[key]=bad
        try:prepare(altered)
        except ValueError:pass
        else:raise ValueError('false '+key+' certificate accepted')
    f,points,_,_=prepare(data)
    for key,bad in [('origin_tetrahedron',[0,0,4,8]),('norm_squared_bound',[1,1])]:
        altered=deepcopy(data);altered[key]=bad
        try:extension(f,points,altered)
        except ValueError:pass
        else:raise ValueError('false '+key+' extension accepted')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    data=json.loads(Path(__file__).with_name('certificate.json').read_text())
    if args.selftest:controls(data)
    print(json.dumps(verify(data),indent=2,sort_keys=True))
