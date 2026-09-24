"""Exhaustive exact joins of two complete degree-nine point links."""
from collections import defaultdict,Counter
from itertools import combinations,permutations,product
from math import factorial
from catalogue import CAT, point_automorphisms

P=12
PAIRLIST=list(combinations(range(13),2))
PAIRINDEX={p:i for i,p in enumerate(PAIRLIST)}
ALLBLOCKS=[sum(1<<x for x in t) for t in combinations(range(13),6)]
BITS={b:tuple(x for x in range(13) if b>>x&1) for b in ALLBLOCKS}
PAIRS={b:tuple(PAIRINDEX[t] for t in combinations(BITS[b],2)) for b in ALLBLOCKS}

def columns(rows,vertices):
    return tuple(sum(1<<i for i,b in enumerate(rows) if b>>p&1) for p in vertices)

def key(rows,vertices):
    cols=columns(rows,vertices);k=len(rows)
    return min(tuple(sorted(sum(1<<perm[i] for i in range(k) if m>>i&1) for m in cols)) for perm in permutations(range(k)))

def prepare():
    templates=defaultdict(list);roots=[]
    for d in CAT:
        rows=d['point_signatures'];blocks=d['blocks']
        if any(s.bit_count()==5 for s in rows):
            aut=point_automorphisms(d)
            for orbit in d['point_orbits']:
                h=orbit[0]
                if rows[h].bit_count()!=5:continue
                stabilizer=[a for a in aut if a[h]==h]
                left=set(range(12))-{h}
                while left:
                    q=min(left);left-={a[q] for a in stabilizer}
                    eligible=[r for r in range(12) if r not in (h,q)]
                    def score(r):
                        through=[b&~(1<<r) for b in blocks if b>>r&1]
                        counts=Counter(columns(through,[x for x in range(12) if x!=r]))
                        free=1
                        for n in counts.values():free*=factorial(n)
                        return (rows[r].bit_count(),-free,-r)
                    r=max(eligible,key=score)
                    if rows[r].bit_count()<4:raise ValueError('no second low point of multiplicity >=4')
                    roots.append(dict(id=len(roots),design=d['id'],h=h,q=q,r=r,k=rows[r].bit_count()))
        for orbit in d['point_orbits']:
            marked=orbit[0];k=rows[marked].bit_count()
            if k not in (4,5):continue
            through=tuple(b&~(1<<marked) for b in blocks if b>>marked&1)
            vertices=tuple(x for x in range(12) if x!=marked)
            templates[(k,key(through,vertices))].append(dict(design=d['id'],marked=marked,through=through,vertices=vertices,blocks=blocks))
    return roots,templates

def embeddings(source,target_rows,target_vertices):
    source_groups=defaultdict(list)
    for p,c in zip(source['vertices'],columns(source['through'],source['vertices'])):source_groups[c].append(p)
    sizes={m:len(v) for m,v in source_groups.items()}
    keys=sorted(source_groups)
    for target_order in permutations(target_rows):
        target_groups=defaultdict(list)
        for p,c in zip(target_vertices,columns(target_order,target_vertices)):target_groups[c].append(p)
        if sizes!={m:len(v) for m,v in target_groups.items()}:continue
        for choices in product(*(permutations(target_groups[m]) for m in keys)):
            action=[None]*12;action[source['marked']]=P
            for m,images in zip(keys,choices):
                for old,new in zip(source_groups[m],images):action[old]=new
            yield action

def join(root,templates):
    d=CAT[root['design']];h,q,r,k=(root[n] for n in ('h','q','r','k'))
    fixed=tuple(b|(1<<P) for b in d['blocks'])
    shared=tuple(b&~(1<<r) for b in d['blocks'] if b>>r&1)
    target_vertices=tuple(x for x in range(13) if x not in (P,r))
    candidates=templates[(k,key(shared,target_vertices))]
    targets=[11 if x==h else 10 if x==q else 9 for x in range(13)]
    maxpair=[20 if {a,b}=={h,q} else 5 for a,b in PAIRLIST]
    raw=0;degree_ok=0;pair_ok=0;answers=set();seen=set()
    for temp in candidates:
        for action in embeddings(temp,shared,target_vertices):
            raw+=1
            second=tuple((1<<r)|sum(1<<action[x] for x in range(12) if b>>x&1) for b in temp['blocks'])
            union=tuple(sorted(set(fixed+second)))
            if len(union)!=18-k:raise ValueError('wrong shared-block count')
            if union in seen:continue
            seen.add(union)
            degrees=[0]*13;paircounts=[0]*78
            for b in union:
                for x in BITS[b]:degrees[x]+=1
                for i in PAIRS[b]:paircounts[i]+=1
            remaining=20-len(union)
            if any(not 0<=targets[x]-degrees[x]<=remaining for x in range(13)):continue
            degree_ok+=1
            if any(n>cap for n,cap in zip(paircounts,maxpair)):continue
            pair_ok+=1;answers.add(union)
    return dict(**root,source_templates=len(candidates),raw=raw,unique=len(seen),degree_ok=degree_ok,pair_ok=pair_ok,configurations=sorted(answers))
