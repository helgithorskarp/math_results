"""Standalone dense verifier; no producer, graph catalog, or solver imports."""
import hashlib
import json
from itertools import combinations
import sys


def check(ok, why):
    if not ok:raise ValueError(why)


def dense_rank(rows):
    a=[list(row) for row in rows]
    r=0
    for col in range(len(a[0]) if a else 0):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        for i in range(len(a)):
            if i!=r and a[i][col]:
                a[i]=[(x+y)%2 for x,y in zip(a[i],a[r])]
        r+=1
    return r


def parse(obj):
    check(type(obj) is dict,'object')
    kind=obj.get('kind');check(kind in ['cut','decomposition'],'kind')
    check(set(obj)=={'n','red_hex','rank_color','kind',('cut' if kind=='cut' else 'tree_edges')},'keys')
    check(type(obj['n']) is int and obj['n']==43,'n')
    s=obj['red_hex'];check(type(s) is str and len(s)==226 and set(s)<=set('0123456789abcdef'),'hex')
    word=int(s,16);check(word<2**903,'overflow')
    color=obj['rank_color'];check(color in ['red','blue'],'color')
    graph=[[0]*43 for _ in range(43)]
    bit=0
    for u in range(43):
        for v in range(u+1,43):
            graph[u][v]=graph[v][u]=(word//2**bit)%2;bit+=1
    if kind=='cut':
        a=obj['cut']
        check(type(a) is list and 0<len(a)<43 and all(type(v) is int and 0<=v<43 for v in a)
              and a==sorted(set(a)),'cut')
        cuts=[frozenset(a if len(a)<=21 else set(range(43))-set(a))]
    else:
        edges=obj['tree_edges']
        check(type(edges) is list and len(edges)==83,'edge count')
        check(all(type(e) is list and len(e)==2 and all(type(v) is int for v in e)
                  and 0<=e[0]<e[1]<84 for e in edges),'edge syntax')
        check(edges==sorted([list(e) for e in set(tuple(e) for e in edges)]),'edge order/uniqueness')
        neighbors=[set() for _ in range(84)]
        for u,v in edges:neighbors[u].add(v);neighbors[v].add(u)
        check([len(ns) for ns in neighbors]==[1]*43+[3]*41,'tree degree sequence')
        seen={0};todo=[0]
        for u in todo:
            for v in neighbors[u]-seen:seen.add(v);todo.append(v)
        check(len(seen)==84,'connectivity')
        # Connectivity and |E|=|V|-1 prove this is a tree. Independently
        # remove each edge and traverse its component to obtain leaf cuts.
        cuts=[]
        for u,v in edges:
            seen={u};todo=[u]
            for x in todo:
                for y in neighbors[x]:
                    if {x,y}=={u,v} or y in seen:continue
                    seen.add(y);todo.append(y)
            a=seen & set(range(43))
            check(a and len(a)<43,'tree leaf cut')
            cuts.append(frozenset(a if len(a)<=21 else set(range(43))-a))
    return graph,cuts,color


def verify(obj, cert):
    graph,cuts,color=parse(obj)
    check(type(cert) is dict,'certificate')
    canonical=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
    check(cert.get('input_sha256')==hashlib.sha256(canonical).hexdigest(),'input binding')
    def matrix(a):
        b=sorted(set(range(43))-set(a))
        return [[graph[u][v] if color=='red' else 1-graph[u][v] for v in b] for u in sorted(a)]
    widths=[dense_rank(matrix(a)) for a in cuts]
    width=max(widths)
    check(type(cert.get('measured_width')) is int and cert['measured_width']==width,'width')
    admitted=(width<=3 and (obj['kind']=='decomposition' or 15<=len(cuts[0])<=21))
    if not admitted:
        check(cert.get('status')=='OUTSIDE_DECLARED_FAMILY','outside verdict')
        return {'status':'VERIFIED_OUTSIDE_DECLARED_FAMILY','ramsey_feasibility':'NOT_DECIDED'}
    check(cert.get('status')=='EXCLUDED_WITH_PHYSICAL_FIVE_SET','exclusion status')
    a=cert.get('cut')
    check(type(a) is list and all(type(v) is int for v in a) and a==sorted(set(a))
          and 15<=len(a)<=21 and frozenset(a) in cuts,'certificate cut')
    m=matrix(a);rank=dense_rank(m)
    check(type(cert.get('cut_rank')) is int and cert['cut_rank']==rank<=3,'cut rank')
    basis=cert.get('row_basis');columns=43-len(a)
    check(type(basis) is list and len(basis)==rank and
          all(type(x) is int and 0<x<2**columns for x in basis),'basis syntax')
    dense_basis=[[(x//2**j)%2 for j in range(columns)] for x in basis]
    check(dense_rank(dense_basis)==rank,'independent basis')
    span={0}
    for x in basis:span|={v ^ x for v in list(span)}
    check(all(sum(bit<<j for j,bit in enumerate(row)) in span for row in m),'row-space coverage')
    five=cert.get('five');c=cert.get('five_color')
    check(type(five) is list and len(five)==5 and all(type(v) is int and 0<=v<43 for v in five)
          and five==sorted(set(five)) and c in ['red','blue'],'five-set syntax')
    check(all(graph[u][v]==int(c=='red') for u,v in combinations(five,2)),'false physical five-set')
    return {'status':'VERIFIED_PHYSICAL_EXCLUSION','tree_cuts_checked':len(cuts),
            'cut_size':len(a),'cut_rank':rank,'physical_pairs_checked':10}


if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: verify.py INPUT.json CERTIFICATE.json')
    with open(sys.argv[1]) as f:obj=json.load(f)
    with open(sys.argv[2]) as f:cert=json.load(f)
    print(json.dumps(verify(obj,cert),sort_keys=True,separators=(',',':')))
