"""Physical obstruction extractor for a large cut or a supplied rank decomposition."""
import hashlib
import json
from itertools import combinations
import sys


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canonical(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()


def read_input(obj):
    need(type(obj) is dict,'input object')
    common={'n','red_hex','rank_color','kind'}
    kind=obj.get('kind')
    need(kind in ('cut','decomposition'),'kind')
    need(set(obj)==common|({'cut'} if kind=='cut' else {'tree_edges'}),'input keys')
    need(type(obj['n']) is int and obj['n']==43,'order')
    s=obj['red_hex']
    need(type(s) is str and len(s)==226 and all(c in '0123456789abcdef' for c in s),'hex syntax')
    word=int(s,16)
    need(word<2**903,'word overflow')
    need(obj['rank_color'] in ('red','blue'),'rank color')
    if kind=='cut':
        q=obj['cut']
        need(type(q) is list and q and len(q)<43 and
             all(type(v) is int and 0<=v<43 for v in q) and q==sorted(set(q)),'cut')
    else:
        edges=obj['tree_edges']
        need(type(edges) is list and len(edges)==83,'tree edge count')
        need(all(type(e) is list and len(e)==2 and all(type(v) is int for v in e)
                 and 0<=e[0]<e[1]<84 for e in edges),'tree edge syntax')
        need(edges==sorted(map(list,set(map(tuple,edges)))),'canonical tree edges')
    adj=[0]*43
    for e,(u,v) in enumerate(combinations(range(43),2)):
        if (word >> e)&1:
            adj[u]|=1<<v;adj[v]|=1<<u
    return word,adj


def basis(rows):
    pivots={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in pivots:
                row^=pivots[p]
            else:
                pivots[p]=row
                break
    return [pivots[p] for p in sorted(pivots,reverse=True)]


def cut_data(adj, mask, color):
    full=(1<<43)-1
    if mask.bit_count()>21:
        mask^=full
    a=[v for v in range(43) if (mask >> v)&1]
    b=[v for v in range(43) if not (mask >> v)&1]
    rows=[sum((((adj[u]>>v)&1) ^ (color=='blue')) << j for j,v in enumerate(b)) for u in a]
    return a,basis(rows)


def tree_masks(edges):
    neighbors=[[] for _ in range(84)]
    for u,v in edges:
        neighbors[u].append(v);neighbors[v].append(u)
    need(all(len(neighbors[v])==(1 if v<43 else 3) for v in range(84)),'tree degrees')
    parent={43:None};order=[43]
    for v in order:
        for w in neighbors[v]:
            if w==parent[v]:continue
            need(w not in parent,'tree cycle')
            parent[w]=v;order.append(w)
    need(len(order)==84,'disconnected tree')
    below={v:(1<<v if v<43 else 0) for v in range(84)}
    for v in reversed(order[1:]):below[parent[v]]|=below[v]
    return [below[v] for v in order[1:]]


def clique(adj, available, k, prefix=()):
    if k==0:return prefix
    while available.bit_count()>=k:
        bit=available & -available;available^=bit;v=bit.bit_length()-1
        answer=clique(adj,available & adj[v],k-1,prefix+(v,))
        if answer is not None:return answer
    return None


def extract(obj):
    _,adj=read_input(obj)
    color=obj['rank_color']
    digest=hashlib.sha256(canonical(obj)).hexdigest()
    if obj['kind']=='cut':
        mask=sum(1<<v for v in obj['cut'])
        cut,bs=cut_data(adj,mask,color)
        width=len(bs)
        admitted=15<=len(cut)<=21 and width<=3
    else:
        data=[cut_data(adj,m,color) for m in tree_masks(obj['tree_edges'])]
        width=max(len(bs) for _,bs in data)
        eligible=[(a,bs) for a,bs in data if 15<=len(a)<=21]
        need(eligible,'centroid cut missing')
        cut,bs=min(eligible,key=lambda x:(len(x[0]),x[0]))
        admitted=width<=3
    if not admitted:
        return {'status':'OUTSIDE_DECLARED_FAMILY','input_sha256':digest,'measured_width':width}
    full=(1<<43)-1
    for c in ('red','blue'):
        rows=adj if c=='red' else [full ^ row ^ (1<<v) for v,row in enumerate(adj)]
        q=clique(rows,full,5)
        if q is not None:
            return {'status':'EXCLUDED_WITH_PHYSICAL_FIVE_SET','input_sha256':digest,
                    'cut':cut,'cut_rank':len(bs),'row_basis':bs,'measured_width':width,
                    'five':list(q),'five_color':c}
    raise RuntimeError('the admitted graph has no bad five: theorem or implementation failure')


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: extract.py INPUT.json')
    with open(sys.argv[1]) as f:obj=json.load(f)
    print(canonical(extract(obj)).decode(),end='')
