"""Complete blue-pair orbit interface for one original q7,r5 task."""
from pathlib import Path
from itertools import combinations
import hashlib,json
HERE=Path(__file__).resolve().parent
TASK='bo1-q7-r5-c000004'

def require(ok,message):
    if not ok: raise ValueError(message)

def core():
    document=json.loads((HERE/'CORE.json').read_text());line=document['graph6']
    require(len(line)==19 and ord(line[0])-63==15,'core graph6 dimensions')
    bits=[(ord(c)-63)>>b&1 for c in line[1:] for b in range(5,-1,-1)]
    require(not any(bits[105:]),'core graph6 padding')
    return {(i,j):bits[j*(j-1)//2+i] for j in range(1,15) for i in range(j)}

def allowed(w):
    for a in range(1,5):
        for left in combinations(range(4),a):
            for right in combinations(range(4),5-a):
                if all(not(w>>(4*i+j)&1) for i in left for j in right):return False
    return True

def move(w,g):
    if g<3:
        lo=w>>(4*g)&15;hi=w>>(4*(g+1))&15
        return w^((lo^hi)<<(4*g))^((lo^hi)<<(4*(g+1)))
    if g<6:
        j=g-3;mask=0
        for i in range(4):
            if (w>>(4*i+j)&1)!=(w>>(4*i+j+1)&1):mask|=3<<(4*i+j)
        return w^mask
    return sum((w>>(4*i+j)&1)<<(4*j+i) for i in range(4) for j in range(4))

def orbit_partition():
    remaining={w for w in range(65536) if allowed(w)};answer=[]
    while remaining:
        rep=min(remaining);seen={rep};stack=[rep]
        while stack:
            w=stack.pop()
            for g in range(7):
                z=move(w,g)
                if z not in seen:seen.add(z);stack.append(z)
        require(seen<=remaining,'orbit closure or duplicate')
        remaining-=seen;answer.append((rep,sorted(seen)))
    return answer

def geometry(rep,full=False):
    require(type(rep) is int and 0<=rep<65536 and allowed(rep),'invalid blue-pair word')
    n=43 if full else 23;fixed=core()
    for block in [range(15,19),range(19,23)]:
        for e in combinations(block,2):fixed[e]=0
    for i in range(4):
        for j in range(4):fixed[15+i,19+j]=rep>>(4*i+j)&1
    if full:
        for b in range(5):
            for e in combinations(range(23+4*b,27+4*b),2):fixed[e]=1
    free=[e for e in combinations(range(n),2) if e not in fixed]
    return n,fixed,free,{e:i+1 for i,e in enumerate(free)}

def lex_leq(left,right,first):
    rows=[];prev=None;nextvar=first
    for i,(x,y) in enumerate(zip(left,right)):
        rows.append(([] if prev is None else [-prev])+[-x,y])
        if i+1==len(left):break
        z=nextvar;nextvar+=1
        if prev is not None:rows.append([-z,prev])
        rows.extend([[-z,-x,y],[-z,x,-y]])
        rows.extend([([] if prev is None else [-prev])+[-x,-y,z],([] if prev is None else [-prev])+[x,y,z]])
        prev=z
    return nextvar,rows

def formula(rep,full=False):
    n,fixed,free,var=geometry(rep,full);rows=[]
    systems=[(4,1,range(23)),(5,0,range(n))]
    if full:systems.append((5,1,range(n)))
    for size,color,vs in systems:
        for S in combinations(vs,size):
            if full and color and size==5 and S[-1]<23:continue
            pairs=list(combinations(S,2))
            if any(e in fixed and fixed[e]!=color for e in pairs):continue
            rows.append([(-1 if color else 1)*var[e] for e in pairs if e not in fixed])
    physical=len(rows);first=len(free)+1
    if full:
        blocks=[list(range(23+4*b,27+4*b)) for b in range(5)];comparisons=[]
        for block in blocks:
            for u,v in zip(block,block[1:]):comparisons.append(([var[i,u] for i in range(14,-1,-1)],[var[i,v] for i in range(14,-1,-1)]))
        for a,b in zip(blocks,blocks[1:]):comparisons.append(([var[i,u] for u in a[::-1] for i in range(14,-1,-1)],[var[i,u] for u in b[::-1] for i in range(14,-1,-1)]))
        for a,b in comparisons:first,extra=lex_leq(a,b,first);rows.extend(extra)
    return first-1,rows,physical

def dimacs(rep,full=False):
    nv,rows,_=formula(rep,full)
    return (f'p cnf {nv} {len(rows)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in rows)).encode('ascii')

def check_graph(rep,graph,full=False):
    n,fixed,free,var=geometry(rep,full)
    require(graph.get('order')==n,'graph order')
    edges=graph.get('red_edges');require(isinstance(edges,list),'edge list')
    red=set()
    for e in edges:
        require(isinstance(e,list) and len(e)==2 and all(type(v) is int for v in e) and 0<=e[0]<e[1]<n,'edge syntax')
        require(tuple(e) not in red,'duplicate edge');red.add(tuple(e))
    for e,c in fixed.items():require((e in red)==bool(c),'fixed edge')
    for S in combinations(range(23),4):require(not all(e in red for e in combinations(S,2)),'red tail K4')
    for S in combinations(range(n),5):require(len({e in red for e in combinations(S,2)})==2,'monochromatic K5')
    if full:
        sig=lambda v:sum(int((i,v) in red)<<i for i in range(15));words=[]
        for b in range(5):
            ss=[sig(v) for v in range(23+4*b,27+4*b)];require(ss==sorted(ss),'red-block vertex order');words.append(sum(s<<(15*j) for j,s in enumerate(ss)))
        require(words==sorted(words),'red-block order')
    return {'status':'VERIFIED_GOOD43' if full else 'VERIFIED_TAIL_ONLY','order':n}

def physical_word(graph):
    red={tuple(e) for e in graph['red_edges']}
    free=[e for e in combinations(range(23),2) if not(e[1]<15 or 15<=e[0]<e[1]<19 or 19<=e[0]<e[1])]
    return ''.join(str(int(e in red)) for e in free)

def graph_from_word(word):
    require(isinstance(word,str) and len(word)==136 and not(set(word)-set('01')),'tail word')
    fixed=core()
    for block in [range(15,19),range(19,23)]:
        for e in combinations(block,2):fixed[e]=0
    free=[e for e in combinations(range(23),2) if e not in fixed]
    fixed.update({e:int(word[i]) for i,e in enumerate(free)})
    return {'order':23,'red_edges':[list(e) for e,c in fixed.items() if c]}
