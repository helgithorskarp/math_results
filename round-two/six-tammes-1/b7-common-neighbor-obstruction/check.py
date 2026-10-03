"""Exact whole-band common-neighbor obstruction; six-tammes-1/researcher.

Forward reflection and Bernstein certificate. The generic Cauchy--Schwarz
argument is ordinary geometry; the new information is six explicit masks.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import argparse,json
from poly import add,neg,mul,bernstein

ROOT=Path(__file__).resolve().parent
PARENT_SHA='a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'
PREVIOUS_SHA='b92549e6c9c7047df9c85d7a67fc724a42f3175006050c4fb5984205d2be9b11'
R,D=[F(0),F(1)],[F(2),F(-1)]
LO,HI=F(7,10),F(3,4)
B=((1,2,4),(2,4,8),(1,2,10),(1,10,12))
K=[F(x) for x in (4,0,-8,-4,2,1)]
PREVIOUS_STRICT=(36,42,43,44,45,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79)
EXCLUDED=(42,65,69,72,75,76,77,78,79)

def need(ok,why):
    if not ok:raise ValueError(why)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))+'\n'
def digest(x):return sha256(canonical(x).encode()).hexdigest()
def enc(p):return [str(x) for x in p]
def at(p,x):return sum(v*x**i for i,v in enumerate(p))
def negative(p,lo=LO,hi=HI):
    bs=bernstein(p,lo,hi)
    need(all(x<0 for x in bs),'strict negative bound on entire closed interval')
    return bs
def inner(v,w):
    diagonal=[];sv=[];sw=[]
    for x,y in zip(v,w):diagonal=add(diagonal,mul(x,y));sv=add(sv,x);sw=add(sw,y)
    return add(mul([F(2),F(-2)],diagonal),mul(R,mul(sv,sw)))
def flip(u,v,w):return [add(mul(R,add(x,y)),neg(z)) for x,y,z in zip(u,v,w)]
def reconstruct(triangles):
    ps={1:[[F(1)],[],[]],2:[[],[F(1)],[]],4:[[],[],[F(1)]]}
    ps[8]=flip(ps[2],ps[4],ps[1]);ps[10]=flip(ps[1],ps[2],ps[4]);ps[12]=flip(ps[1],ps[10],ps[2])
    done=set(B);todo=set(map(tuple,triangles))-done
    while todo:
        t=next((t for t in sorted(todo) if len(set(t)&set(ps))==2),None)
        need(t is not None,'one fresh B triangle available')
        u,v=sorted(set(t)&set(ps));parents=[q for q in done if u in q and v in q]
        need(len(parents)==1,'unique predecessor sharing whole B edge')
        old=next(x for x in parents[0] if x not in (u,v));fresh=next(x for x in t if x not in (u,v))
        need(fresh not in ps,'distinct fresh B label')
        ps[fresh]=flip(ps[u],ps[v],ps[old]);done.add(t);todo.remove(t)
    need(set(ps)=={1,2,4,8,10,12,20,21,22},'whole nine-point B support')
    need(all(inner(v,v)==D for v in ps.values()),'all B unit identities')
    for t in triangles:
        for u,v in combinations(t,2):need(inner(ps[u],ps[v])==R,'every required B contact')
    return ps
def inputs():
    bs=(ROOT/'PARENT.json').read_bytes();old=(ROOT/'PREVIOUS.json').read_bytes()
    need(sha256(bs).hexdigest()==PARENT_SHA,'entire immutable9972 input')
    need(sha256(old).hexdigest()==PREVIOUS_SHA,'entire immutable10068 cover')
    p,q=json.loads(bs),json.loads(old)
    need(p['B']==[list(t) for t in B],'whole B seed')
    need(q['parent_sha256']==PARENT_SHA,'previous cover binds same whole parent')
    need(q['remaining_strict_maps']==list(PREVIOUS_STRICT),'entire imported23 strict list')
    need(q['remaining_closed_maps']==[8]+list(PREVIOUS_STRICT),'entire imported24 closed list')
    need(len(p['full_band_maps'])==53 and len(p['strict_improvement_maps'])==52,'entire parent cover sizes')
    cuts=[row['map'] for row in q['rows']]
    need(len(cuts)==29 and len(set(cuts))==29,'entire imported29 cuts')
    need([i for i in p['full_band_maps'] if i not in cuts]==q['remaining_closed_maps'],'whole closed residual correspondence')
    need([i for i in p['strict_improvement_maps'] if i not in cuts]==q['remaining_strict_maps'],'whole strict residual correspondence')
    return p,q
def build():
    p,q=inputs();rows=[];cases=[];keys={}
    bs=negative(K);upper=max(bs)
    need(upper==F(-64373,100000),'exact uniform K upper bound')
    for i in EXCLUDED:
        row=p['geometric_maps'][i];a=next((a for a in (6,7,9) if sum(x==a for x,y in row['cross'])==2),None)
        need(a is not None,'specified A leaf has two B neighbors')
        pair=sorted(y for x,y in row['cross'] if x==a);need(len(pair)==2 and len(set(pair))==2,'two distinct B labels')
        key=(row['shape'],tuple(pair))
        if key not in keys:
            ps=reconstruct(p['all_shapes'][row['shape']]);u,v=pair;g=inner(ps[u],ps[v]);L=add(D,g)
            s=add(mul(D,L),neg(mul([F(2)],mul(R,R))))
            need(s==mul([F(2),F(-2)],K),'entire Cauchy--Schwarz gap identity')
            index=len(cases);keys[key]=index
            cases.append({'case':index,'shape':row['shape'],'B_triangles':p['all_shapes'][row['shape']],
                          'pair':pair,'B_points':{str(x):[enc(t) for t in ps[x]] for x in sorted(ps)},
                          'pair_N':enc(g),'S':enc(s)})
        rows.append({'map':i,'shape':row['shape'],'anchor':a,'pair':pair,'case':keys[key],'cross':row['cross']})
    need(len(cases)==6 and len({x['shape'] for x in cases})==5,'six distinct masks in five B shapes')
    left=[i for i in q['remaining_closed_maps'] if i not in EXCLUDED]
    strict=[i for i in q['remaining_strict_maps'] if i not in EXCLUDED]
    need(len(left)==15 and len(strict)==14 and set(left)-set(strict)=={8},'whole15/14 necessary residual lists')
    return {'format':'b7-common-neighbor-obstruction-v1','actual_author':'six-tammes-1','role':'researcher',
            'parent_sha256':PARENT_SHA,'previous_sha256':PREVIOUS_SHA,
            'cosine_closed_band':['7/13','3/5'],'r_closed_band':[str(LO),str(HI)],'B_seed':[list(t) for t in B],
            'K':enc(K),'K_Bernstein':enc(bs),'K_closed_upper':str(upper),
            'cases':cases,'excluded_maps':list(EXCLUDED),'rows':rows,
            'remaining_closed_maps':left,'remaining_strict_maps':strict,
            'scope':'Six nine-distinct-unit B7/pair masks admit no unit common c-neighbor in R3 on closedJ; nine15-label maps excluded. Physical corollary imports ALL9972/9813/10038/10068; no global bound.'}
def verify(record,expected=None):
    if expected is None:expected=build()
    need(record==expected,'whole geometric record, every field and every case')
    return {'status':'complete','cases':6,'excluded_maps':9,'remaining_closed':15,'remaining_strict':14,'certificate_sha256':digest(record)}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit');parser.add_argument('--certificate');args=parser.parse_args()
    expected=build()
    if args.emit:Path(args.emit).write_text(canonical(expected))
    supplied=json.loads(Path(args.certificate).read_text()) if args.certificate else expected
    print(canonical(verify(supplied,expected)).strip())
