"""Original literal partition/point-map certificate checker; no kernel import."""


def need(ok,msg):
    if not ok:
        raise ValueError(msg)


def freeze(x):
    return tuple(freeze(a) for a in x) if isinstance(x,list) else x


def record(words,old,new):
    witness,free,M,F,holes,hubholes,coarse,key,values,CM,CF,coords=new
    need(freeze(old[0])==witness and old[1]==free and freeze(old[8])==coords,'exact original source row binding')
    fi,H,mate,roles=witness
    need(M==tuple(sorted(tuple(sorted(set(b)-{mate})) for b in words if mate in b)),'every actual original mate-word tail')
    need(F==tuple(sorted(tuple(sorted(set(b)-{free})) for b in words if free in b)),'every actual original free-point word tail')
    ground=set(range(17))-{mate,free};hs=set(H)
    need(set().union(*map(set,M))==ground and sum(map(len,M))==15,'full actual mate partition')
    need(all(len(b)==3 for b in M+F) and sum(map(len,F))==len(set().union(*map(set,F))),'actual disjoint free tails')
    expected_holes=ground-set().union(*map(set,F))
    need(set(holes)==expected_holes and tuple(sorted(expected_holes&hs))==hubholes,'entire actual free-hole set')
    need(len(values)==len(set(values))==17 and set(values)==set(range(16))|{17},'actual full point bijection')
    mapping=dict(enumerate(values))
    need(all(mapping[p]==j for j,p in enumerate(roles)) and mapping[free]==15 and mapping[mate]==17,'fixed Hub roles/free/mate preserved')
    need(sorted(tuple(sorted(mapping[p] for p in b)) for b in M)==sorted(CM),'all original mate-tail images')
    need(sorted(tuple(sorted(mapping[p] for p in b)) for b in F)==sorted(CF),'all original free-tail images')
    color=lambda s:sum(2**p for p in set(s)&set(range(5)))
    hole_image={mapping[p] for p in holes};columns=list(map(set,CF))+[hole_image]
    rows=list(map(set,CM))
    recovered=(5-len(F),tuple(color(c) for c in columns),tuple((color(r),tuple((color(r&c),len((r&c)-set(range(5)))) for c in columns)) for r in rows))
    need(recovered==key,'entire canonical decorated incidence key against original point map')
    coarse_recovered=(5-len(F),color(hole_image),tuple(sorted((color(r),len(r-set(range(5))),len((r&hole_image)-set(range(5)))) for r in rows)))
    need(coarse==freeze(old[7])==coarse_recovered,'complete original coarse291 key binding')
    return True
