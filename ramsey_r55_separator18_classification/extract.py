#!/usr/bin/env python3
"""Extract a literal bad five from a supplied member of the excluded cut class."""
import argparse
import json
from itertools import combinations
from pathlib import Path

def require(ok,message):
    if not ok:
        raise ValueError(message)

def clique(adj, pool, k):
    if k==0:
        return []
    while pool.bit_count()>=k:
        bit=pool&-pool
        pool-=bit
        v=bit.bit_length()-1
        tail=clique(adj,pool&adj[v],k-1)
        if tail is not None:
            return [v]+tail
    return None

def parse(obj):
    require(set(obj)=={'n','red_hex','separator','cut_color'},'input fields')
    require(type(obj['n']) is int and obj['n']==43,'order43 required')
    word=obj['red_hex']
    require(isinstance(word,str) and len(word)==226 and all(c in '0123456789abcdef' for c in word),'903-bit lowercase physical graph word')
    code=int(word,16)
    require(code<1<<903,'nonzero padding')
    s=obj['separator']
    require(isinstance(s,list) and all(type(v) is int and 0<=v<43 for v in s) and s==sorted(set(s)) and len(s)<=18,'separator shape')
    require(obj['cut_color'] in ('red','blue'),'cut color')
    adj=[0]*43
    for i,(u,v) in enumerate(combinations(range(43),2)):
        if code>>i&1:
            adj[u]|=1<<v
            adj[v]|=1<<u
    full=(1<<43)-1
    comp=[full^(1<<v)^adj[v] for v in range(43)]
    red,blue=(adj,comp) if obj['cut_color']=='red' else (comp,adj)
    remaining=full^sum(1<<v for v in s)
    parts=[]
    while remaining:
        todo=remaining&-remaining
        part=0
        while todo:
            bit=todo&-todo
            todo-=bit
            if part&bit:
                continue
            part|=bit
            v=bit.bit_length()-1
            todo|=red[v]&remaining&~part
        remaining&=~part
        parts.append(part)
    parts.sort(key=lambda m:(m.bit_count(),m))
    require(len(parts)>=2,'not a separator in supplied color')
    require(not(len(s)==18 and [m.bit_count() for m in parts]==[1,24]),'allowed singleton boundary is not the excluded family')
    return red,blue,s,parts

def extract(obj):
    red,blue,s,parts=parse(obj)
    full=(1<<43)-1
    def result(vertices,color,route):
        require(len(vertices)==5 and len(set(vertices))==5,'bad extracted size')
        require(all((red if color=='red' else blue)[u]>>v&1 for u,v in combinations(vertices,2)),'bad extracted edges')
        actual=color if obj['cut_color']=='red' else ('blue' if color=='red' else 'red')
        return {'status':'CERTIFIED_MONOCHROMATIC_FIVE','color':actual,'vertices':sorted(vertices),'route':route}
    independent=[]
    for part in parts:
        for color,adj in (('red',red),('blue',blue)):
            q=clique(adj,part,5)
            if q is not None:
                return result(q,color,'component_five')
        for k in range(4,0,-1):
            q=clique(blue,part,k)
            if q is not None:
                independent.append(q)
                break
    if sum(map(len,independent))>=5:
        return result([v for q in independent for v in q][:5],'blue','component_independence_budget')
    sizes=[p.bit_count() for p in parts]
    # Use the new mechanism before the generic minimum-degree shortcuts.
    if sizes==[12,13] and list(map(len,independent))==[2,2]:
        a,b=parts
        words=[]
        for z in s:
            for part in (a,b):
                q=clique(red,red[z]&part,4)
                if q is not None:
                    return result([z]+q,'red','separator_red_four')
            qa=clique(blue,blue[z]&a,2)
            qb=clique(blue,blue[z]&b,2)
            if qa is not None and qb is not None:
                return result([z]+qa+qb,'blue','separator_two_blue_pairs')
            require(qb is not None and (blue[z]&a).bit_count()==4 and qa is None,'small Ramsey attachment implication failed')
            words.append(red[z]&a)
        # The complete 12-vertex lemma proves this for arbitrary labels.
        require(len(set(words))==1,'complete unique-attachment lemma contradicted')
        triangle=clique(red,words[0],3)
        require(triangle is not None,'eight-vertex Ramsey triangle implication failed')
        for u,v in combinations(s,2):
            if red[u]>>v&1:
                return result([u,v]+triangle,'red','unique_attachment_red_pair')
        return result(s[:5],'blue','unique_attachment_blue_separator')
    for v in range(43):
        if red[v].bit_count()<18:
            pool=blue[v]
            q=clique(blue,pool,4)
            if q is not None:
                return result([v]+q,'blue','minimum_degree')
            q=clique(red,pool,5)
            require(q is not None,'R(4,5)<=25 implication failed')
            return result(q,'red','minimum_degree')
    for part,ind in zip(parts,independent):
        a=part.bit_count()
        if len(ind)==1 and a>=2:
            vertices=[v for v in range(43) if part>>v&1]
            pool=sum(1<<v for v in s)
            for v in vertices:
                pool&=red[v]
            q=clique(blue,pool,5)
            if q is not None:
                return result(q,'blue','clique_common_neighborhood')
            q=clique(red,pool,5-a)
            require(q is not None,'small Ramsey common-neighborhood implication failed')
            return result(vertices+q,'red','clique_common_neighborhood')
    if sizes==[13,13]:
        z=s[0]
        pairs=[]
        for part in parts:
            q=clique(red,red[z]&part,4)
            if q is not None:
                return result([z]+q,'red','thirteen_red_four')
            q=clique(blue,blue[z]&part,2)
            require(q is not None,'thirteen-component blue-pair implication failed')
            pairs+=q
        return result([z]+pairs,'blue','two_thirteen_components')
    raise ValueError('complete separator arithmetic contradicted; no graph verdict emitted')

def cut_clauses(a,b):
    """Physical pairs in the two global cut clauses; no DIMACS variable convention."""
    require(all(isinstance(x,list) and x==sorted(set(x)) and all(type(v) is int and 0<=v<43 for v in x) for x in (a,b)),'cut vertex lists')
    require(not(set(a)&set(b)) and min(len(a),len(b))>=2 and len(a)+len(b)>=25,'proper cut of total size>=25 required')
    pairs=sorted([sorted([u,v]) for u in a for v in b])
    return {'at_least_one_red':pairs,'at_least_one_blue':pairs}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('graph',type=Path)
    args=ap.parse_args()
    print(json.dumps(extract(json.loads(args.graph.read_text())),sort_keys=True,indent=2))
