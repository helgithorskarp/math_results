"""Small input fixtures only; neither finite proof algorithm lives here."""
from itertools import combinations
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def primary_problem(directory):
    lines=(Path(directory)/'baseline21.rows').read_text().splitlines()
    require(len(lines)==21 and all(len(row)==21 and set(row)<={'0','1'} for row in lines),'primary syntax')
    old=[{j for j,c in enumerate(row) if c=='1'} for row in lines]
    require(all(i not in old[i] and all((j in old[i])==(i in old[j]) for j in range(21)) for i in range(21)), 'primary simple')
    blue=[set(range(21))-{i}-old[i] for i in range(21)]
    degree=[len(g) for g in old]
    require(sum(degree)//2==93 and degree.count(8)==4 and degree.count(9)==16 and degree.count(10)==1,'primary degrees')
    require(max(len(old[i]&old[j]) for i,j in combinations(range(21),2) if j in old[i])==3,'primary red books')
    require(max(len(blue[i]&blue[j]) for i,j in combinations(range(21),2) if j not in old[i])==6,'primary blue books')
    v=degree.index(10);a=sorted(old[v]);b=sorted(set(range(21))-{v}-old[v]);order=[v]+a+b
    inverse={x:i for i,x in enumerate(order)}
    g=[{inverse[j] for j in old[x]} for x in order]
    local=[sum(1<<j for j in range(10) if j+1 in g[i+1]) for i in range(10)]
    words=[sum(1<<i for i in range(10) if i+1 not in g[j+11]) for j in range(10)]
    deficits=[10-len(g[j+11]) for j in range(10)]
    actual_stars=[sum(1<<j for j in range(10) if j+11 in g[b+11]) for b in range(10)]
    masks=[sum(1<<j for j in row) for row in g]
    return local,words,deficits,actual_stars,masks


def weighted_controls():
    records=[]
    for name in ['four-cycle','K2,3']:
        p=[set() for _ in range(10)]
        def pe(a,b):p[a].add(b);p[b].add(a)
        if name=='four-cycle':
            for i in range(5):
                pe(i,(i+1)%5);pe(i+5,5+(i+1)%5);pe(i,i+5)
            marked=0
        else:
            for i in [0,1]:
                for j in [2,3,4]:pe(i,j)
            for i in [8,9]:
                for j in [5,6,7]:pe(i,j)
            for i in [2,3,4]:pe(i,i+3)
            marked=1
        original=[sum(1<<i for i in range(10) if (b-i)%11<5) for b in range(11)]
        degrees=[z.bit_count() for z in original];remaining=degrees[:];outside=[set() for _ in range(11)]
        while max(remaining):
            order=sorted(range(11),key=lambda i:(-remaining[i],i));v=order[0];d=remaining[v]
            require(all(remaining[j]>0 for j in order[1:d+1]),'control graphical')
            remaining[v]=0
            for j in order[1:d+1]:outside[v].add(j);outside[j].add(v);remaining[j]-=1
        for deficiency in [1,2]:
            words=original[:];bb=[row.copy() for row in outside]
            available=[b for b,z in enumerate(words) if not z>>marked&1]
            if deficiency==1:chosen=available[:1]
            else:
                chosen=list(next((b,c) for b,c in combinations(available,2) if c not in bb[b]))
                b,c=chosen;bb[b].add(c);bb[c].add(b)
            for b in chosen:words[b]|=1<<marked
            g=[set() for _ in range(22)]
            def edge(a,b):g[a].add(b);g[b].add(a)
            for i in range(10):
                edge(0,i+1)
                for j in p[i]:edge(i+1,j+1)
                for b,z in enumerate(words):
                    if not z>>i&1:edge(i+1,b+11)
            for b in range(11):
                for c in bb[b]:edge(b+11,c+11)
            delta=[10-len(row) for row in g]
            require(sum(delta)==2 and min(delta)>=0 and max(delta)<=2,'signed109 degree control')
            records.append({'name':name+'-delta'+str(deficiency),
                            'neighbor_masks':[sum(1<<j for j in row) for row in g],
                            'local':[sum(1<<j for j in row) for row in p],
                            'miss_rows':words,'marked':marked,'deficiency':deficiency})
    return records
