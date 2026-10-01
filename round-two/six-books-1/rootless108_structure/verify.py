"""Separate bit-neighbor, literal subset and edge-backtracking controls."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib,copy
HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)

def sha(data):return hashlib.sha256(json.dumps(data,separators=(',',':')).encode()).hexdigest()

def compositions(total,length):
    if length==1:yield (total,);return
    for first in range(total+1):
        for rest in compositions(total-first,length-1):yield (first,)+rest

def complement_fixture(delta):
    # Realize the blue H graph in reverse label order, then complement it.
    remain=[8]*12+[9]*6;blue=[0]*18
    while any(remain):
        v=max(range(18),key=lambda x:(remain[x],x));d=remain[v];remain[v]=0
        choices=sorted((j for j in range(18) if remain[j]),key=lambda x:(-remain[x],-x))[:d]
        require(len(choices)==d,'blue degree fixture')
        for j in choices:blue[v]|=1<<j;blue[j]|=1<<v;remain[j]-=1
    core=[((1<<18)-1)^(1<<x)^blue[x] for x in range(18)]
    require([x.bit_count() for x in core]==[9]*12+[8]*6,'complement degrees')
    types=[{i} for i in range(4) for _ in range(4-delta[i])]+[set(pair) for pair in combinations(range(4),2)]
    g=[15^(1<<i) for i in range(4)]+[row<<4 for row in core]
    for x,t in enumerate(types):
        for i in t:g[i]|=1<<(x+4);g[x+4]|=1<<i
    return g,types,core

def compute():
    result={'schema':1,'integer_packing':[sum(range(t))-t+1 for t in range(5)],'clique_controls':[]}
    for delta in compositions(4,4):
        g,types,core=complement_fixture(delta);degree=[row.bit_count() for row in g]
        require(degree==[10-d for d in delta]+[10]*18 and sum(degree)==216,'signed108 literal degrees')
        roots=[i for i in range(22) if degree[i]==10 and all(degree[j]==10 for j in range(22) if g[i]>>j&1)]
        m0=sum(d==0 for d in delta);require(len(roots)==4*m0+len(list(combinations(range(m0),2))),'full roots')
        require(all((g[i]&g[j]).bit_count()==3 for i,j in combinations(range(4),2)),'six saturated low spines')
        entries=0
        for x,t in enumerate(types):
            r=len(t);p=sum(bool(core[x]>>y&1) for y in range(12,18))
            require(sum(len(types[y]) for y in range(18) if core[x]>>y&1)==10-r+p,'literal type count')
            for i in range(4):
                m=sum(i in types[y] for y in range(18) if core[x]>>y&1)
                if i in t:literal=(g[i]&g[x+4]).bit_count();need=r-1+m
                else:
                    bx=((1<<22)-1)^g[x+4]^(1<<(x+4));bi=((1<<22)-1)^g[i]^(1<<i)
                    literal=(bx&bi).bit_count();need=delta[i]+r+m
                require(literal==need,'literal low/H spine');entries+=1
        require(any((g[i]&g[j]).bit_count()>3 for i,j in combinations(range(22),2) if g[i]>>j&1),'dense invalid signed fixture')
        result['clique_controls'].append({'delta':delta,'full_roots':len(roots),'literal_cross_entries':entries})
    labels=list(combinations(range(4),2));triangles=[]
    for selected in combinations(range(6),3):
        tau=[sum(i in labels[x] for x in selected) for i in range(4)];sizes=[3-t for t in tau]
        words=[0]
        for i,s in enumerate(sizes):
            choices=[sum(1<<(3*i+j) for j in chosen) for chosen in combinations(range(3),s)]
            words=[a|b for a in words for b in choices]
        minimum=min((a&b).bit_count() for a in words for b in words)
        require(minimum>=2,'literal triangle singleton minimum')
        pages=[1+len(set(labels[a])&set(labels[b]))+minimum for a,b in combinations(selected,2)]
        require(max(pages)>=4,'literal forced red book')
        triangles.append({'types':selected,'tau':tau,'singleton_sizes':sizes,'minimum_pages':pages})
    result['pair_triangle_cases']=len(triangles);result['pair_triangle_digest']=sha(triangles)
    ep=list(combinations(range(6),2));max2=trianglefree=0;neighbors=[0]*6
    def all_max2(pos):
        nonlocal max2,trianglefree
        if pos==15:
            max2+=1
            trianglefree+=not any(neighbors[a]>>b&1 and neighbors[a]&neighbors[b] for a,b in ep)
            return
        a,b=ep[pos];all_max2(pos+1)
        if neighbors[a].bit_count()<2 and neighbors[b].bit_count()<2:
            neighbors[a]|=1<<b;neighbors[b]|=1<<a;all_max2(pos+1);neighbors[a]^=1<<b;neighbors[b]^=1<<a
    all_max2(0);result['six_pair_graphs']={'max_degree_two':max2,'max_degree_two_trianglefree':trianglefree}
    masks=[];girth_models=[];remaining=[2]*4+[3]*2;neighbors=[0]*6
    def degrees_visit(i):
        if i==6:
            require(not any(remaining),'residual degree leaf')
            mask=sum(1<<k for k,(a,b) in enumerate(ep) if neighbors[a]>>b&1);masks.append(mask)
            # Literal breadth-first neighborhoods: no child is in layer1,
            # and no two distinct branches share a layer2 point.
            good=True
            for r in range(6):
                first={j for j in range(6) if neighbors[r]>>j&1};used=set()
                for j in first:
                    children={v for v in range(6) if v!=r and neighbors[j]>>v&1}
                    if children&first or children&used:good=False;break
                    used|=children
                if not good:break
            if good:girth_models.append(mask)
            return
        needed=remaining[i];available=[j for j in range(i+1,6) if remaining[j]]
        for choice in combinations(available,needed):
            remaining[i]=0
            for j in choice:remaining[j]-=1;neighbors[i]|=1<<j;neighbors[j]|=1<<i
            if all(0<=remaining[j]<=5-i-1 for j in range(i+1,6)):degrees_visit(i+1)
            for j in choice:remaining[j]+=1;neighbors[i]^=1<<j;neighbors[j]^=1<<i
            remaining[i]=needed
    degrees_visit(0);require(len(masks)==len(set(masks)),'duplicate residual degree model')
    result['six_point_residual']={'degree_models':len(masks),'degree_model_sha256':sha(sorted(masks)),'girth_at_least_five_models':len(girth_models)}
    require(not girth_models,'literal cubic one-nine four-cycle residual')
    lines=(HERE/'baseline21.rows').read_text().splitlines();require(len(lines)==21 and all(len(row)==21 and set(row)<={'0','1'} for row in lines),'primary syntax')
    red=[int(row[::-1],2) for row in lines];blue=[((1<<21)-1)^red[i]^(1<<i) for i in range(21)]
    require(all(not red[i]>>i&1 and all((red[i]>>j&1)==(red[j]>>i&1) for j in range(21)) for i in range(21)),'primary simple')
    rm=max((red[i]&red[j]).bit_count() for i,j in combinations(range(21),2) if red[i]>>j&1);bm=max((blue[i]&blue[j]).bit_count() for i,j in combinations(range(21),2) if not red[i]>>j&1)
    require(rm==3 and bm==6 and sum(x.bit_count() for x in red)==186,'primary positive book')
    result['primary21']={'edges':93,'red_pages':rm,'blue_pages':bm}
    return json.loads(json.dumps(result))

if __name__=='__main__':
    actual=compute();expected=json.loads((HERE/'expected.json').read_text());require(actual==expected,'independent report mismatch')
    damages=[]
    bad=copy.deepcopy(expected);bad['clique_controls'].pop();damages.append(bad)
    bad=copy.deepcopy(expected);bad['clique_controls'][0]['full_roots']+=1;damages.append(bad)
    bad=copy.deepcopy(expected);bad['pair_triangle_digest']='0'*64;damages.append(bad)
    bad=copy.deepcopy(expected);bad['six_point_residual']['girth_at_least_five_models']=1;damages.append(bad)
    bad=copy.deepcopy(expected);bad['six_pair_graphs']['max_degree_two_trianglefree']+=1;damages.append(bad)
    bad=copy.deepcopy(expected);bad['primary21']['blue_pages']=7;damages.append(bad)
    rejected=0
    for bad in damages:
        try:require(actual==bad,'damaged record')
        except ValueError:rejected+=1
        else:raise ValueError('damaged record accepted')
    require(rejected==6,'six damaged controls')
    print(json.dumps({'status':'PASS','damaged_records_rejected':rejected,'clique_compositions':len(actual['clique_controls']),'pair_triangles':actual['pair_triangle_cases'],'six_point_residual':actual['six_point_residual']}))
