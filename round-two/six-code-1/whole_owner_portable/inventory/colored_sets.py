"""Set partition intersections; enumerate all free-tail orders independently."""
import itertools as it
import time

TABLE={}


def check(ok,msg):
    if not ok:
        raise ValueError(msg)


def tup(x):
    return tuple(tup(a) for a in x) if isinstance(x,list) else x


def normalize(deficit,hub_rows,hub_columns,entries):
    input_key=(deficit,hub_rows,hub_columns,entries)
    if input_key in TABLE:
        return TABLE[input_key],0
    candidates=[];states=0
    r=len(hub_columns)-1
    for perm in it.permutations(range(r)):
        states+=1
        if tuple(hub_columns[j] for j in perm)!=tuple(sorted(hub_columns[:-1])):
            continue
        columns=perm+(r,)
        colored_rows=[(hub_rows[i],tuple(entries[i][j] for j in columns),i) for i in range(5)]
        colored_rows.sort()
        rows=tuple(item[2] for item in colored_rows)
        normal=(deficit,tuple(hub_columns[j] for j in columns),tuple((h,parts) for h,parts,i in colored_rows))
        candidates.append((normal,columns,rows))
    check(candidates and states<=24,'all r! original free-tail orders')
    answer=min(candidates)
    TABLE[input_key]=answer
    return answer,states


def physical(words,source_rows):
    begin=time.monotonic()
    blocks=[set(w) for w in words]
    identity=source_rows[0][0]
    fi,H,mate,first_roles=identity
    free=source_rows[0][1]
    actual_M=sorted((b-{mate} for b in blocks if mate in b),key=lambda b:tuple(sorted(b)))
    actual_F=sorted((b-{free} for b in blocks if free in b),key=lambda b:tuple(sorted(b)))
    d=5-len(actual_F)
    ground=set(range(17))-{mate,free}
    check(len(actual_M)==5 and len(actual_F) in (3,4) and all(len(a)==3 for a in actual_M+actual_F),'literal3/4 free-tail cells')
    check(sum(map(len,actual_M))==len(set().union(*actual_M))==15 and set().union(*actual_M)==ground,'entire original mate partition')
    check(sum(map(len,actual_F))==len(set().union(*actual_F)) and all(a<=ground for a in actual_F),'entire original free partition')
    check(all(len(a&b)<=1 for a in actual_M for b in actual_F),'simple original cell intersections')
    unused=ground-set().union(*actual_F)
    columns=actual_F+[unused]
    records=[];states=0
    for old in source_rows:
        fi,H,mate,roles=old[0]
        check(old[0][:3]==identity[:3] and old[1]==free and old[2]==d,'source transport owner identity')
        position={p:j for j,p in enumerate(roles)}
        Hset=set(H)
        color=lambda cell:sum(2**position[p] for p in cell&Hset)
        hub_rows=tuple(color(cell) for cell in actual_M)
        hub_columns=tuple(color(cell) for cell in columns)
        cells=[[a&b for b in columns] for a in actual_M]
        entries=tuple(tuple((color(cell),len(cell-Hset)) for cell in row) for row in cells)
        (key,colperm,rowperm),used=normalize(d,hub_rows,hub_columns,entries)
        states+=used+1
        check(states<=100000 and time.monotonic()-begin<=10,'INCOMPLETE original100000-state/10s physical-owner oracle')
        mapping={p:j for j,p in enumerate(roles)}
        mapping.update({mate:17,free:15})
        satellite=5
        for i in rowperm:
            for j in colperm:
                for p in sorted(cells[i][j]-Hset):
                    mapping[p]=satellite
                    satellite+=1
        check(satellite==15 and sorted(mapping)==list(range(17)) and sorted(mapping.values())==list(range(16))+[17],'actual complete original point map')
        M=tuple(tuple(sorted(mapping[p] for p in actual_M[i])) for i in rowperm)
        F=tuple(tuple(sorted(mapping[p] for p in actual_F[j])) for j in colperm[:-1])
        coarse=(d,color(unused),tuple(sorted((color(cell),len(cell-Hset),len(cell&unused-Hset)) for cell in actual_M)))
        check(coarse==tup(old[7]),'independent original coarse profile')
        records.append((tup(old[0]),free,tuple(tuple(sorted(a)) for a in actual_M),tuple(tuple(sorted(a)) for a in actual_F),
            tuple(sorted(unused)),tuple(sorted(unused&Hset)),coarse,key,tuple(mapping[p] for p in range(17)),M,F,tup(old[8])))
    check(len(records)==12 and time.monotonic()-begin<=10,'all12 source role transports')
    return sorted(records),states
