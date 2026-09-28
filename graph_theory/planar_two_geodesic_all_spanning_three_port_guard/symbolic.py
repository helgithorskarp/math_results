#!/usr/bin/env python3
"""Affine proof that all four one-edge template pairs are ambient geodesics."""

# a path length is an affine form (r,x,y,z,constant), r=m-7.
EDGE_FORMS = [
    (0,1,(0,0,0,0,1)),(1,2,(0,0,0,0,1)),
    (2,3,(0,0,0,0,1)),(3,4,(0,0,0,0,1)),
    (4,5,(0,0,0,0,1)),(5,6,(1,0,0,0,1)),
    (6,0,(0,0,0,0,1)),(0,7,(0,0,0,0,1)),
    (1,3,(0,1,0,0,0)),(1,5,(0,0,1,0,0)),
    (3,5,(0,0,0,1,0)),
]

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def forms(missing, s,t):
    g=[[] for _ in range(8)]
    for i,(a,b,w) in enumerate(EDGE_FORMS):
        if i==missing:continue
        g[a].append((b,w));g[b].append((a,w))
    out=[]
    def dfs(u,seen,w):
        if u==t:out.append(w);return
        for v,c in g[u]:
            if v not in seen:dfs(v,seen|{v},add(w,c))
    dfs(s,{s},(0,0,0,0,0))
    return out

def specialize(w,case,dx=0):
    a,b,c,d,e=w
    # r=5+R; z=r-3+Z; case A x=r+1+X,y=r-1+Y
    if case=='A':return (5*a+6*b+4*c+2*d+e,a+b+c+d,b,c,d)
    # case B x=r-dx, dx=0 or 1; y=r+1+Y
    return (5*a+(5-dx)*b+6*c+2*d+e,a+b+c+d,c,d)

CANDIDATES={
    1:{'A':[(7,1,(0,0,0,0,2)),(2,6,(1,0,0,0,4))],
       'B':[(2,7,(0,1,0,0,3)),(4,6,(1,0,0,0,2))]},
    2:{'A':[(7,2,(0,0,0,0,3)),(3,6,(1,0,0,0,3))],
       'B':[(7,5,(1,0,0,0,3)),(2,4,(0,1,0,0,2))]},
    3:{'A':[(7,3,(0,0,0,0,4)),(4,6,(1,0,0,0,2))],
       'B':[(7,3,(0,0,0,0,4)),(4,6,(1,0,0,0,2))]},
    4:{'A':[(7,4,(0,0,0,0,5)),(5,6,(1,0,0,0,1))],
       'B':[(7,4,(0,0,0,0,5)),(5,6,(1,0,0,0,1))]},
}

def main():
    template_cases = 0
    path_comparisons = 0
    for missing in range(1, 5):
        for case in ('A', 'B'):
            for dx in ((0, 1) if case == 'B' else (0,)):
                for source, target, candidate in CANDIDATES[missing][case]:
                    alternatives = forms(missing, source, target)
                    assert candidate in alternatives
                    expected = specialize(candidate, case, dx)
                    for alternative in alternatives:
                        difference = sub(specialize(alternative, case, dx), expected)
                        assert all(coefficient >= 0 for coefficient in difference), (
                            missing, case, dx, source, target, alternative, difference
                        )
                        path_comparisons += 1
                    template_cases += 1
    print(f"template_cases={template_cases} affine_path_comparisons={path_comparisons} PASS")


if __name__ == '__main__':
    main()
