"""Exact controls for ordinary deficit-four and one-nine cubic-root proofs."""
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json,hashlib,sys
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def digest(records):
    return hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest()

def havel(degrees):
    remaining=degrees[:];g=[set() for _ in degrees]
    while max(remaining):
        order=sorted(range(len(g)),key=lambda i:(-remaining[i],i));v=order[0];d=remaining[v];remaining[v]=0
        need(all(remaining[j]>0 for j in order[1:d+1]),'nongraphical control')
        for j in order[1:d+1]:g[v].add(j);g[j].add(v);remaining[j]-=1
    need(list(map(len,g))==degrees,'degree realization')
    return g

def cliquefixture(delta):
    types=[(i,) for i in range(4) for _ in range(4-delta[i])]+list(combinations(range(4),2))
    core=havel([9]*12+[8]*6);g=[set() for _ in range(22)]
    def edge(a,b):g[a].add(b);g[b].add(a)
    for i,j in combinations(range(4),2):edge(i,j)
    for x,t in enumerate(types):
        for i in t:edge(i,x+4)
        for y in core[x]:edge(x+4,y+4)
    return g,types,core

def report():
    result={'schema':1,'integer_packing':[t*(t-1)//2-(t-1) for t in range(5)],'clique_controls':[]}
    need(result['integer_packing']==[1,0,0,1,3],'clique equality integer cases')
    for delta in product(range(5),repeat=4):
        if sum(delta)!=4:continue
        g,types,core=cliquefixture(delta);degree=list(map(len,g));m0=delta.count(0)
        need(degree==[10-d for d in delta]+[10]*18 and sum(degree)//2==108,'signed108 clique degrees')
        roots=[i for i in range(22) if degree[i]==10 and all(degree[j]==10 for j in g[i])]
        need(len(roots)==4*m0+m0*(m0-1)//2,'exact full root count')
        need(all(len(g[i]&g[j])==3 for i,j in combinations(range(4),2)),'clique spine saturation')
        signed=0
        for x in range(18):
            r=len(types[x]);p=sum(y>=12 for y in core[x])
            need(sum(len(types[y]) for y in core[x])==10-r+p,'pair incidence identity')
            for i in range(4):
                common_h=sum(i in types[y] for y in core[x])
                redcommon=(r-1 if i in types[x] else r)+common_h
                if i in types[x]:need(len(g[i]&g[x+4])==redcommon,'red clique/outside identity')
                else:
                    bluei=set(range(22))-{i}-g[i];bluex=set(range(22))-{x+4}-g[x+4]
                    need(len(bluei&bluex)==delta[i]+redcommon,'blue clique/outside identity')
                signed+=1
        # The dense Havel graph is an invalid signed control, not a Book witness.
        need(any(len(g[i]&g[j])>3 for i,j in combinations(range(22),2) if j in g[i]),'unexpected valid red control')
        result['clique_controls'].append({'delta':delta,'full_roots':len(roots),'literal_cross_entries':signed})
    need(len(result['clique_controls'])==35,'all four-slot deficit compositions')
    pair_types=list(combinations(range(4),2));triangles=[]
    for selected in combinations(range(6),3):
        tau=[sum(i in pair_types[x] for x in selected) for i in range(4)]
        sizes=[3-t for t in tau]
        need(sum(sizes)==6,'saturated triangle star size')
        intersection=sum(max(0,2*s-3) for s in sizes)
        need(intersection>=2,'triangle singleton intersection lower bound')
        pages=[1+len(set(pair_types[a])&set(pair_types[b]))+intersection for a,b in combinations(selected,2)]
        need(max(pages)>=4,'forced red book in pair triangle')
        triangles.append({'types':selected,'tau':tau,'singleton_sizes':sizes,'minimum_pages':pages})
    result['pair_triangle_cases']=len(triangles);result['pair_triangle_digest']=digest(triangles)
    need(all(max(0,3-2*t)>=2-t for t in range(4)),'integer triangle bound')
    ep=list(combinations(range(6),2));degree_models=[];trianglefree=0;max2=0;residual=[]
    for mask in range(32768):
        g=[set() for _ in range(6)]
        for k,(a,b) in enumerate(ep):
            if mask>>k&1:g[a].add(b);g[b].add(a)
        d=list(map(len,g));tri=any(b in g[a] and c in g[a]&g[b] for a,b,c in combinations(range(6),3))
        if max(d)<=2:max2+=1;trianglefree+=not tri
        if d!=[2]*4+[3]*2:continue
        degree_models.append(mask)
        four=any(len(g[a]&g[b])>=2 for a,b in combinations(range(6),2))
        if not tri and not four:residual.append(mask)
    result['six_pair_graphs']={'max_degree_two':max2,'max_degree_two_trianglefree':trianglefree}
    result['six_point_residual']={'degree_models':len(degree_models),'degree_model_sha256':digest(degree_models),'girth_at_least_five_models':len(residual)}
    need(not residual,'one-nine cubic four-cycle residual counterexample')
    lines=(HERE/'baseline21.rows').read_text().splitlines();g=[{j for j,c in enumerate(row) if c=='1'} for row in lines]
    need(len(g)==21 and all(len(row)==21 for row in lines),'baseline syntax')
    need(all(i not in g[i] and all((j in g[i])==(i in g[j]) for j in range(21)) for i in range(21)),'baseline simple')
    b=[set(range(21))-{i}-g[i] for i in range(21)]
    red=max(len(g[i]&g[j]) for i,j in combinations(range(21),2) if j in g[i]);blue=max(len(b[i]&b[j]) for i,j in combinations(range(21),2) if j not in g[i])
    need(red==3 and blue==6 and sum(map(len,g))//2==93,'positive primary book control')
    result['primary21']={'edges':93,'red_pages':red,'blue_pages':blue}
    return json.loads(json.dumps(result))

if __name__=='__main__':
    result=report()
    if sys.argv[1:]==['--write']:(HERE/'expected.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    elif sys.argv[1:]:raise ValueError('usage check.py [--write]')
    else:need(result==json.loads((HERE/'expected.json').read_text()),'expected record mismatch')
    print(json.dumps({'status':'PASS','clique_compositions':len(result['clique_controls']),'pair_triangles':result['pair_triangle_cases'],'six_pair_graphs':result['six_pair_graphs'],'six_point_residual':result['six_point_residual']}))
