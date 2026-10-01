"""Complete literal two-anchor models and labelled matrix census."""
from collections import Counter
from hashlib import sha256
from itertools import combinations,product
from common import require,canonical

PAIRS=tuple(combinations(range(15),2))

def model(lengths):
    missing=set(); begin=0
    for length in lengths:
        for x in range(begin,begin+length):
            missing.add((x,x))
            missing.add((x,begin+(x-begin+1)%length))
        begin+=length
    require(begin==5 and lengths in ((5,),(3,2),(2,3)), 'invalid cycle model')
    cells=tuple((r,c) for r in range(5) for c in range(5) if (r,c) not in missing)
    anchors=tuple(tuple(i for i,(r,c) in enumerate(cells) if r==j)+(15,) for j in range(5))
    anchors+=tuple(tuple(i for i,(r,c) in enumerate(cells) if c==j)+(16,) for j in range(5))
    covered=Counter(p for q in anchors for p in combinations(q,2))
    require(len(cells)==15 and len(covered)==60 and set(covered.values())=={1},'bad anchors')
    internal={p for p in covered if p[1]<15}
    eligible=tuple(p for p in PAIRS if p not in internal)
    candidates=tuple(q for q in combinations(range(15),4)
                     if set(combinations(q,2)).isdisjoint(internal))
    require(len(eligible)==75 and len(candidates)==(95 if lengths==(5,) else 96),'bad full candidates')
    # Separate matching criterion for every one of the1365possible cell quadruples.
    matching=tuple(q for q in combinations(range(15),4)
                   if len({cells[x][0] for x in q})==len({cells[x][1] for x in q})==4)
    require(candidates==matching,'pair legality and four-matchings disagree')
    return dict(cells=cells,anchors=anchors,internal=internal,eligible=eligible,candidates=candidates)

def matrix_census():
    counts=Counter(); stream=sha256()
    for rows in product(tuple(combinations(range(5),2)),repeat=5):
        degree=Counter(c for row in rows for c in row)
        if any(degree[c]!=2 for c in range(5)): continue
        adjacency=[set() for _ in range(10)]
        for r,row in enumerate(rows):
            for c in row: adjacency[r].add(c+5); adjacency[c+5].add(r)
        require(all(len(n)==2 for n in adjacency),'noncycle complement')
        unseen=set(range(10)); sizes=[]
        while unseen:
            pending=[min(unseen)]; component=set()
            while pending:
                x=pending.pop()
                if x in component: continue
                component.add(x); pending.extend(adjacency[x]-component)
            require(component<=unseen,'overlapping cycle components')
            unseen-=component; sizes.append(len(component))
        shape=tuple(sorted(sizes))
        require(shape in ((10,),(4,6)),'unclassified bipartite2regular shape')
        counts[str(shape)]+=1; stream.update(canonical(rows))
    require(counts=={'(10,)':1440,'(4, 6)':600},'complete matrix census mismatch')
    return dict(matrices=sum(counts.values()),shape_counts=dict(counts),sha256=stream.hexdigest())
