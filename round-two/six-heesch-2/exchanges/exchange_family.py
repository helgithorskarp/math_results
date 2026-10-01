"""Complete one-delete-two-add family about the published seventeen-hex."""
from itertools import combinations
from geometry import canonical,connected,halo,holes


def generate(seed):
    seed=set(seed);raw_checked=set();out=set()
    for deleted in sorted(seed):
        old=seed-{deleted}
        # A connected final shape has an addition adjacent to an old cell;
        # the other is adjacent to an old cell or the first addition.
        # The deletion intermediate may be disconnected.
        for a in sorted(halo(old)):
            for b in sorted(halo(old|{a})):
                raw=tuple(sorted(old|{a,b}))
                if raw in raw_checked:continue
                raw_checked.add(raw)
                assert len(raw)==18
                if connected(raw) and not holes(raw):out.add(canonical(raw))
    return tuple(sorted(out)),len(raw_checked)


def cell_complex(cells):
    """Full-edge components and Euler characteristic, with integer vertices."""
    corners=((0,2),(1,1),(1,-1),(0,-2),(-1,-1),(-1,1))
    cells=tuple(cells);parent=list(range(len(cells)))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    vertices=set();edges={}
    for i,(x,y) in enumerate(cells):
        vs=[(2*x+y+a,3*y+b) for a,b in corners]
        vertices.update(vs)
        for k in range(6):
            edge=tuple(sorted((vs[k],vs[(k+1)%6])))
            if edge in edges:parent[root(i)]=root(edges[edge])
            else:edges[edge]=i
    return len({root(i) for i in range(len(cells))}),len(vertices)-len(edges)+len(cells)


def independent_generate(seed):
    assert cell_complex({(0,0)})==(1,1)
    assert cell_complex({(0,0),(1,0)})==(1,1)
    assert cell_complex({(0,0),(4,0)})==(2,2)
    assert cell_complex(halo({(0,0)}))==(1,0)
    seed=set(seed);pool=seed|halo(seed);pool|=halo(pool)
    checked=set();out=set()
    for deleted in sorted(seed):
        old=seed-{deleted}
        # Uniform radius-two pool and unordered pairs, rather than growth.
        for a,b in combinations(sorted(pool-old),2):
            raw=tuple(sorted(old|{a,b}))
            if raw in checked:continue
            checked.add(raw)
            if cell_complex(raw)==(1,1):out.add(canonical(raw))
    return tuple(sorted(out)),len(checked)
