"""Generate positive colouring recipes for the complete target ball family."""
import argparse
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
PERMS=list(permutations(range(4)))
MARKS=(303,435)


def inputs():
    plan=json.loads((HERE/'inputs.json').read_text())
    raw=(HERE.parent/plan['graph_file']).read_bytes()
    if sha256(raw).hexdigest()!=plan['graph_sha256']:raise ValueError('graph input hash')
    edges=[tuple(e) for e in json.loads(raw)['G3_edges']]
    words=[[int(c) for c in line] for line in (HERE/'half_colourings.txt').read_text().splitlines()]
    if len(words)!=16 or any(len(w)!=1066 for w in words):raise ValueError('half colourings')
    return plan,edges,words


def maximal_balls(adj,limit):
    balls={}
    for root in range(len(adj)):
        visited={root};layer={root};radius=0
        while True:
            nxt=set().union(*(adj[v] for v in layer))-visited
            if not nxt or len(visited)+len(nxt)>limit:break
            visited|=nxt;layer=nxt;radius+=1
        mask=sum(1<<v for v in visited)
        balls.setdefault(mask,(root,radius))
    maximal=[]
    for mask in sorted(balls,key=lambda b:(-b.bit_count(),b)):
        if not any(mask&old==mask for old in maximal):maximal.append(mask)
    return balls,maximal


def options(support,active,words,adj):
    result={}
    for wi,word in enumerate(words):
        for colour in range(4):
            reached={0} if 0 in support else set();stack=list(reached)
            if colour:
                while stack:
                    u=stack.pop()
                    for v in adj[u]&support:
                        if v not in reached and word[v] in (0,colour):
                            reached.add(v);stack.append(v)
            out={v:(colour-word[v] if colour and word[v] in (0,colour) and v not in reached else word[v]) for v in support}
            signature=sum((out.get(mark,-1)==0)<<j for j,mark in enumerate(MARKS) if active>>j&1)
            result.setdefault(signature,(wi,colour,out))
            if signature==0:return result
    return result


def generate():
    plan,edges,words=inputs();n=plan['vertices'];adj=[set() for _ in range(n)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    half=[{v for v in adj[u] if v<1066} for u in range(1066)]
    for word in words:
        if any(word[u]==word[v] for u,v in edges if v<1066):raise ValueError('invalid half colouring')
    balls,maximal=maximal_balls(adj,plan['limit']);recipes=[]
    for mask in maximal:
        support={v for v in range(n) if mask>>v&1}
        left={v for v in support if v<1066}
        right={0 if v==0 else v-1065 for v in support if v==0 or v>=1066}
        active=sum((m in left and m in right)<<j for j,m in enumerate(MARKS))
        lo=options(left,active,words,half);ro=options(right,active,words,half);answer=None
        induced=[(u,v) for u,v in edges if u in support and v in support]
        for a,l in lo.items():
            for b,r in ro.items():
                if 0 in support and a&b:continue
                for pi,perm in enumerate(PERMS):
                    if 0 in support and perm[0]!=0:continue
                    colour=dict(l[2]);colour.update({(0 if v==0 else v+1065):perm[c] for v,c in r[2].items()})
                    if all(colour[u]!=colour[v] for u,v in induced):
                        answer=[*balls[mask],l[0],l[1],r[0],r[1],pi];break
                if answer:break
            if answer:break
        if answer is None:raise ValueError(('unresolved ball',balls[mask],len(support)))
        recipes.append(answer)
    return {'version':1,'limit':plan['limit'],'recipes':recipes}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    start=time.monotonic();cert=generate();raw=(json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n').encode()
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'certificate.json').write_bytes(raw)
    print(json.dumps({'certificate_bytes':len(raw),'certificate_sha256':sha256(raw).hexdigest(),'recipes':len(cert['recipes']),'seconds':time.monotonic()-start},sort_keys=True))

if __name__=='__main__':main()
