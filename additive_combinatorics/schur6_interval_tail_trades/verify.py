"""Independent literal audits; no SAT solver, generator, or network used."""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path


def interval(a,b):
    return set(range(a,b+1))


def schur_rows(points):
    points=set(points)
    return [(x,z-x,z) for z in sorted(points) for x in range(1,z//2+1)
            if x in points and z-x in points]


def valid(values):
    return all(len({values[x] for x in row})>1 for row in schur_rows(values))


def small_tail_audit():
    tested=positive=0
    cases=[(n,2,2) for n in range(8,11)]+[(n,3,2) for n in range(13,18)]+[(10,2,3),(13,3,3)]
    for n,a,k in cases:
        u=list(range(1,a));v=list(range(2*a-1,n-3*a+2));w=list(range(n-3*a+2,n-a+1))
        reserved=interval(a,2*a-2)|interval(n+1-a,n)
        assert not schur_rows(reserved)
        points=u+v+w
        all_rows=schur_rows(points);base_rows=schur_rows(u+v)
        for colours in product(range(1,k+1),repeat=len(points)):
            values=dict(zip(points,colours))
            literal=all(len({values[x] for x in row})>1 for row in all_rows)
            base=all(len({values[x] for x in row})>1 for row in base_rows)
            lists={z:set(range(1,k+1)) for z in w}
            for x in u+v:
                for y in u+v:
                    if x+y in lists and values[x]==values[y]:lists[x+y].discard(values[x])
            reduced=base and all(values[z] in lists[z] for z in w)
            reduced=reduced and all(not values[x]==values[y]==values[y-x]
                                    for x,y in combinations(w,2) if y-x in u)
            assert literal==reduced,(n,a,k,colours)
            tested+=1;positive+=literal
    return tested,positive


def main():
    data=json.loads(Path(__file__).with_name('data.json').read_text())
    base={i:c for i,c in enumerate(map(int,data['base160']),1)}
    assert len(base)==160 and set(base.values())==set(range(1,6)) and valid(base)
    seed={d:base[d] for d in range(1,78)}|{154+i:base[i] for i in range(1,151)}
    assert data['u']==''.join(str(seed[x]) for x in range(1,78))
    assert data['v']==''.join(str(seed[x]) for x in range(155,305))
    assert valid(seed)
    w=interval(305,459)
    target_points=set(seed)|w
    part=lambda x:'U' if x<=77 else 'V' if x<=304 else 'W'
    counts=Counter(''.join(part(x) for x in row) for row in schur_rows(target_points))
    assert counts==dict(UUU=1482,UVV=8547,UVW=3003,UWW=8932,VVW=5700)
    hole_sets=[];histograms=[]
    for delta in (0,1):
        fixed={x:c for x,c in seed.items() if not delta or x!=155}
        lists={z:set(range(1,6)) for z in w}
        for z in w:
            for x in range(1,z//2+1):
                y=z-x
                if x in fixed and y in fixed and fixed[x]==fixed[y]:lists[z].discard(fixed[x])
        holes={z for z in w if not lists[z]}
        assert holes==set(data['empty_points'])
        hole_sets.append(sorted(holes));histograms.append(dict(sorted(Counter(map(len,lists.values())).items())))
    for c,pair in enumerate(data['obstruction312'],1):
        assert sum(pair)==312 and all(seed[x]==c for x in pair)

    deletion_graphs=[]
    for delta in (0,1):
        old=interval(78,154+delta)|interval(460,537)
        assert not schur_rows(old)
        m=43+delta
        lower=[112+i for i in range(m)];upper=[460+i for i in range(m)]
        for added in (set(data['empty_points']),interval(312,348)):
            edges=set()
            for row in schur_rows(old|added):
                # Literal triple traversal checks that no other type occurs.
                assert len(set(row)&added)==1 and len(set(row)&old)==2
                edges.add(tuple(sorted(set(row)&old)))
            assert {x for e in edges for x in e}==set(lower+upper)
            assert all((lower[i],upper[i]) in edges for i in range(m))
            assert all((lower[i+1],upper[i]) in edges for i in range(m-1))
            assert all(x in lower and y in upper and upper.index(y)<=lower.index(x) for x,y in edges)
            for t in range(m+1):
                cover=set(upper[:t]+lower[t:])
                assert len(cover)==m and all(set(e)&cover for e in edges)
                result=(old-cover)|added
                assert not schur_rows(result)
                assert len(result)==(127 if len(added)==15 else 149)
            deletion_graphs.append({'delta':delta,'added':len(added),'edges':len(edges),
                                    'minimum_deletions':m,'minimum_covers':m+1})

    # An independent exhaustive control for the matching+chain proof.
    cover_assignments=0
    for m in range(1,11):
        accepted=[]
        for choices in product((0,1),repeat=m):
            # 1 chooses H_i, 0 chooses L_i; matching edges are covered.
            if all(not(choices[i+1]==1 and choices[i]==0) for i in range(m-1)):
                accepted.append(choices)
            cover_assignments+=1
        assert set(accepted)=={(1,)*t+(0,)*(m-t) for t in range(m+1)}

    witnesses=[];pairs=0
    for t in range(45):
        reserved=interval(78,111+t)|interval(312,348)|interval(460+t,537)
        assert len(reserved)==149 and not schur_rows(reserved)
        p=(112+t)//2;r=112+t-p;s=min(78,126-2*t);b=111+t
        assert p+s<=201-t and s<=126-2*t and r<=75+t
        intervals=[[0,p-1],[b+p,b+p+s-1],[348+p,347+p+r]]
        points=set().union(*(interval(a,z) for a,z in intervals))
        assert min(points)==0 and max(points)<=537
        assert len(points)==(190+t if t<=24 else 238-t)
        for x,y in combinations(sorted(points),2):
            assert 1<=y-x<=537 and y-x not in reserved
            pairs+=1
        witnesses.append({'t':t,'vertices':len(points),'implied_R5_lower':len(points)+1,
                          'intervals':intervals})
    tested,positive=small_tail_audit()
    print(json.dumps({'valid_base160':True,'seed_assigned_points':len(seed),
                      'tail_row_counts':dict(sorted(counts.items())),
                      'empty_lists_by_delta':hole_sets,'domain_histograms_by_delta':histograms,
                      'deletion_graphs':deletion_graphs,'small_cover_choices':cover_assignments,
                      'small_complete_assignments':tested,'small_valid_complete_assignments':positive,
                      'witness_pair_checks':pairs,'witnesses':witnesses,
                      'new_schur_bound':False,'family_impossibility_claim':False},
                     indent=2,sort_keys=True))


if __name__=='__main__':main()
