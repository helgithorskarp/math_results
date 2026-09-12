"""Independent audit of a complete canonical 43-vertex receiver input."""
from pathlib import Path
from itertools import combinations,product
import argparse,hashlib,json
from verify import decoded_core,clique_sets,need

def audit(rep,path):
    fixed=decoded_core()
    for block in [range(15,19),range(19,23)]:
        for e in combinations(block,2):fixed[e]=0
    for i in range(4):
        for j in range(4):fixed[15+i,19+j]=rep>>(4*i+j)&1
    blocks=[list(range(23+4*b,27+4*b)) for b in range(5)]
    for block in blocks:
        for e in combinations(block,2):fixed[e]=1
    free=[e for e in combinations(range(43),2) if e not in fixed];var={e:i+1 for i,e in enumerate(free)};need(len(free)==740,'physical variables')
    with Path(path).open() as f:
        h=f.readline().split();need(h[:2]==['p','cnf'] and len(h)==4,'DIMACS header');nv,nc=map(int,h[2:]);count=0
        def read():
            nonlocal count
            words=list(map(int,f.readline().split()));need(words and words[-1]==0 and 0 not in words[:-1] and all(abs(x)<=nv for x in words[:-1]),'literal syntax');count+=1;return words[:-1]
        for n,size,color in [(23,4,1),(43,5,0),(43,5,1)]:
            adj=[0]*n
            for u,v in combinations(range(n),2):
                if (u,v) not in fixed or fixed[u,v]==color:adj[u]|=1<<v;adj[v]|=1<<u
            for S in clique_sets(adj,size):
                if size==5 and color==1 and S[-1]<23:continue
                expected=[(-1 if color else 1)*var[e] for e in combinations(S,2) if e in var]
                need(read()==expected,'physical full43 clause')
        physical=count;words=[]
        for block in blocks:
            for u,v in zip(block,block[1:]):words.append(([var[i,u] for i in range(14,-1,-1)],[var[i,v] for i in range(14,-1,-1)]))
        for a,b in zip(blocks,blocks[1:]):words.append(([var[i,u] for u in a[::-1] for i in range(14,-1,-1)],[var[i,u] for u in b[::-1] for i in range(14,-1,-1)]))
        nextvar=741;gates=0
        for left,right in words:
            previous=None
            for j,(x,y) in enumerate(zip(left,right)):
                final=j+1==len(left);z=None if final else nextvar
                clauses=[read() for _ in range(1 if final else (5 if previous is None else 6))]
                variables={x,y}|({previous} if previous else set())|({z} if z else set());need({abs(v) for c in clauses for v in c}==variables,'comparator support');variables=sorted(variables)
                for vals in product([False,True],repeat=len(variables)):
                    a=dict(zip(variables,vals));p=True if previous is None else a[previous]
                    wanted=(not p or not a[x] or a[y]) and (z is None or a[z]==(p and a[x]==a[y]))
                    got=all(any(a[abs(v)]==(v>0) for v in c) for c in clauses);need(wanted==got,'comparator truth table')
                if not final:previous=nextvar;nextvar+=1
                gates+=1
        need(count==nc and nextvar-1==nv and not f.read().strip(),'full input exhaustion')
    return {'status':'AUDITED_COMPLETE_PHYSICAL43_RECEIVER','representative':rep,'physical_variables':740,'variables':nv,'clauses':nc,'physical_clauses':physical,'comparator_gates':gates,'cnf_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'five_vertex_sets_covered':962598,'tail_red_four_sets_covered':8855,'original_task_status':'UNKNOWN'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--representative',type=int,required=True);p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();r=audit(a.representative,a.input)
    if a.output:Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
