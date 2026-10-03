"""Bit intersections and canonical free-column permutations; source names kept."""
import itertools as it
import time

CACHE={}


def need(ok,msg):
    if not ok:
        raise ValueError(msg)


def bits(mask):
    return tuple(p for p in range(17) if mask>>p&1)


def freeze(x):
    return tuple(freeze(a) for a in x) if isinstance(x,list) else x


def canonical(d,row_hubs,col_hubs,matrix):
    raw=(d,row_hubs,col_hubs,matrix)
    if raw in CACHE:
        return CACHE[raw],0
    pure=tuple(j for j,h in enumerate(col_hubs[:-1]) if h==0)
    fixed=tuple(sorted((j for j,h in enumerate(col_hubs[:-1]) if h),key=lambda j:col_hubs[j]))
    answers=[]
    for perm in it.permutations(pure):
        order=perm+fixed+(len(col_hubs)-1,)
        rows=tuple(sorted(range(5),key=lambda i:(row_hubs[i],tuple(matrix[i][j] for j in order),i)))
        key=(d,tuple(col_hubs[j] for j in order),tuple((row_hubs[i],tuple(matrix[i][j] for j in order)) for i in rows))
        answers.append((key,order,rows))
    need(answers and len(answers)<=24,'bounded full pure-free-column orders')
    result=min(answers)
    CACHE[raw]=result
    return result,len(answers)


def physical(words,source_rows):
    start=time.monotonic()
    blocks=tuple(sum(1<<p for p in w) for w in words)
    fi,H,mate,_=source_rows[0][0]
    free=source_rows[0][1]
    d=source_rows[0][2]
    M=tuple(sorted((bits(b^(1<<mate)) for b in blocks if b>>mate&1)))
    F=tuple(sorted((bits(b^(1<<free)) for b in blocks if b>>free&1)))
    mm=tuple(sum(1<<p for p in a) for a in M)
    ff=tuple(sum(1<<p for p in a) for a in F)
    ground=((1<<17)-1)^(1<<mate)^(1<<free)
    need(len(M)==5 and len(F)==5-d and all(len(b)==3 for b in M+F),'literal two disjoint tail partitions')
    need(all((a&b)==0 for a,b in it.combinations(mm,2)) and all((a&b)==0 for a,b in it.combinations(ff,2)),'each original root partition disjoint')
    need(sum(mm)==ground and all(not(b>>mate&1) for b in ff),'mate/free uncovered; mate tails cover all15')
    need(all((a&b).bit_count()<=1 for a in mm for b in ff),'each intersection cell at mostone original point')
    holes=ground^sum(ff)
    colm=ff+(holes,)
    result=[];states=0
    for old in source_rows:
        witness=freeze(old[0]);roles=witness[3]
        need(witness[:3]==freeze(source_rows[0][0])[:3] and old[1]==free and old[2]==d,'all12 transports same actual owner/free point')
        hm=sum(1<<p for p in roles)
        row_hubs=tuple(sum(1<<j for j,p in enumerate(roles) if a>>p&1) for a in mm)
        col_hubs=tuple(sum(1<<j for j,p in enumerate(roles) if a>>p&1) for a in colm)
        cells=tuple(tuple(a&b for b in colm) for a in mm)
        matrix=tuple(tuple((sum(1<<j for j,p in enumerate(roles) if v>>p&1),(v&~hm).bit_count()) for v in row) for row in cells)
        (key,order,rows),used=canonical(d,row_hubs,col_hubs,matrix)
        states+=1+used
        need(states<=100000 and time.monotonic()-start<=10,'INCOMPLETE original100000-state/10s physical-owner case')
        mapping=dict(zip(roles,range(5)))|{free:15,mate:17}
        next_sat=5
        for i in rows:
            for j in order:
                for p in bits(cells[i][j]&~hm):
                    mapping[p]=next_sat
                    next_sat+=1
        need(next_sat==15 and set(mapping)==set(range(17)) and set(mapping.values())==set(range(16))|{17},'full17-point labelled bijection')
        cm=tuple(tuple(sorted(mapping[p] for p in M[i])) for i in rows)
        cf=tuple(tuple(sorted(mapping[p] for p in F[j])) for j in order[:-1])
        coarse=(d,col_hubs[-1],tuple(sorted((h,3-h.bit_count(),(mm[i]&holes&~hm).bit_count()) for i,h in enumerate(row_hubs))))
        need(coarse==freeze(old[7]),'full coarse291 profile exactly reproduced')
        result.append((witness,free,M,F,bits(holes),bits(holes&hm),coarse,key,tuple(mapping[p] for p in range(17)),cm,cf,freeze(old[8])))
    need(len(result)==12 and time.monotonic()-start<=10,'complete original12-role physical-owner case')
    return sorted(result),states
