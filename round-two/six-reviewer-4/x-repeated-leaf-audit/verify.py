"""Separate labelled-set enumeration and complete physical-page controls."""
from itertools import product, combinations
from collections import Counter
from pathlib import Path
import importlib.util, json, hashlib, ast

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def independent_domain():
    # Build directly from the stated old neighbourhood, not the mask skeleton.
    old_to_new = [2,1,3,4,5,6,7,8,9,10]
    leaf = [[1,8,9],[0],[6,7],[4,5],[3,7,9],[3,6,8],
            [2,5,9],[2,4,8],[0,5,7],[0,4,6]]
    fixed = {i:set() for i in range(14)}
    def add(g,x,y):
        g[x].add(y); g[y].add(x)
    for x in range(10):
        add(fixed,0,old_to_new[x])
        for y in leaf[x]:
            add(fixed,old_to_new[x],old_to_new[y])
    for t in range(11,14):
        add(fixed,2,t)
        if t!=11:
            add(fixed,9,t);add(fixed,10,t)
    all14 = set(range(14))
    choices = [[s for s in range(8) if s.bit_count()>=minimum]
               for minimum in [2,2,1,1,1,1]]
    accepted = []
    visited = 0
    for word in product(*choices):
        visited += 1
        g={x:ys.copy() for x,ys in fixed.items()}
        for x,s in enumerate(word):
            for t in range(3):
                if s & (1<<t):
                    add(g,3+x,11+t)
        degrees = [10,10,9]+[10]*8+[len(g[t])+4 for t in [11,12,13]]
        out = [degrees[x]-len(g[x]) for x in range(14)]
        if any(k<0 or k>8 for k in out):
            continue
        okay=True
        for i,j in combinations(range(14),2):
            if j in g[i]:
                lower=len(g[i]&g[j])+max(0,out[i]+out[j]-8)
                if lower>3:
                    okay=False;break
            else:
                bi=all14-g[i]-{i};bj=all14-g[j]-{j}
                lower=len(bi&bj)+max(0,8-out[i]-out[j])
                if lower>6:
                    okay=False;break
        if okay:
            rows=[[x for x in range(6) if t+11 in g[x+3]] for t in range(3)]
            accepted.append({'columns':list(word),'T_rows':rows,
                'lows':[5-len(rows[0]),3-len(rows[1]),3-len(rows[2])],
                'degrees':degrees,'red_rows':[sum(1<<y for y in g[x]) for x in range(14)]})
    accepted.sort(key=lambda d:tuple(d['columns']))
    return visited,accepted

def subset_controls():
    Q=set(range(6));subsets=[set(c) for k in range(7) for c in combinations(Q,k)]
    tested=0
    for A,B in product(subsets,repeat=2):
        require(len(A&B)>=max(0,len(A)+len(B)-6),'red minimum')
        require(len((Q-A)&(Q-B))>=max(0,6-len(A)-len(B)),'blue minimum')
        tested+=1
    return tested

def independent_finish(d):
    Q=set(range(6));threes=[set(c) for c in combinations(Q,3)]
    own=[{3,5},{2,4}];Ws=[set(r) for r in d['T_rows'][1:]]
    p=[[len(W&s) for s in own] for W in Ws]
    frames=pairs=accepted=0
    minimum_blue=None
    for A,B in product([set(c) for c in combinations(Q,4)],repeat=2):
        if len(A&B)!=2:
            continue
        frames+=1
        P=Q-A;R=Q-B
        require(len(P)==len(R)==2 and not P&R,'disjoint complements')
        zs=[[Z for Z in threes if 1+p[t][0]+len(A&Z)<=3
             and 1+p[t][1]+len(B&Z)<=3] for t in range(2)]
        for Z1,Z2 in product(*zs):
            # Complete red neighborhoods, reconstructed without mask arithmetic.
            SX0={0,2,6,8,12,13}|{16+y for y in A}
            SX1={0,2,5,7,12,13}|{16+y for y in B}
            T1={2,9,10,15}|{3+x for x in Ws[0]}|{16+y for y in Z1}
            T2={2,9,10,14}|{3+x for x in Ws[1]}|{16+y for y in Z2}
            require(len(SX0)==len(SX1)==10,'full SX degrees')
            require(len(T1)==d['degrees'][12] and len(T2)==d['degrees'][13],'full T degrees')
            require(len(SX0&SX1)==6,'full SX pair')
            require(all(len(S&T)<=3 for S,T in product([SX0,SX1],[T1,T2])),'full red spines')
            all22=set(range(22))
            blue=len((all22-T1-{12})&(all22-T2-{13}))
            require(blue==20-len(T1)-len(T2)+len(T1&T2),'complement identity')
            minimum_blue=blue if minimum_blue is None else min(blue,minimum_blue)
            pairs+=1
            if blue<=6:
                accepted+=1
    return frames,pairs,accepted,minimum_blue

def baseline(path):
    b=Path(path).read_bytes();text=b.decode().split('search_function_used')[0].strip()
    rows=ast.literal_eval(text);require(type(rows) is list and len(rows)==21,'baseline order')
    require(all(type(r) is list and len(r)==21 for r in rows),'baseline shape')
    require(all(type(rows[i][j]) is int and rows[i][j] in [0,1]
                and rows[i][j]==rows[j][i] and (i!=j or rows[i][j]==0)
                for i in range(21) for j in range(21)),'baseline matrix')
    hist=[Counter(),Counter()];edges=0
    for i,j in combinations(range(21),2):
        red=1-rows[i][j]  # primary file: zero=red, one=blue
        pages=sum(rows[i][k]==1-red and rows[j][k]==1-red for k in range(21) if k not in [i,j])
        hist[red][pages]+=1;edges+=red
    require(edges==93 and max(hist[1])==3 and max(hist[0])==6,'primary baseline pages')
    return {'raw_sha256':hashlib.sha256(b).hexdigest(),'vertices':21,'red_edges':edges,
            'blue_pairs':210-edges,'red_page_histogram':dict(sorted(hist[1].items())),
            'blue_page_histogram':dict(sorted(hist[0].items()))}

def main():
    import census
    summary,D,first_finish=census.generate()
    visited,separate=independent_domain()
    require(separate==sorted(D,key=lambda d:tuple(d['columns'])),'all independent full set rows')
    finishes=[independent_finish(d) for d in separate]
    require(sum(f[0] for f in finishes)==summary['SX_frames'],'every frame count')
    require(sum(f[1] for f in finishes)==summary['compatible_T_row_pairs'],'every compatible row-pair count')
    require(all(f[2]==0 for f in finishes),'all independent endpoint exclusions')
    from compare import compare
    original=json.loads((Path(__file__).with_name('original')/'EXPECTED.json').read_text())
    record={'independent':summary,'controls':{'column_words':visited,'entrywise_equal_rows':len(D),
        'outside_subset_pairs':subset_controls(),
        'minimum_common_blue_pages':min(f[3] for f in finishes if f[3] is not None)},
        'original_comparison':compare(D,original),
        'baseline':baseline(Path(__file__).with_name('primary-21.txt'))}
    expected=Path(__file__).with_name('expected.json')
    if expected.exists():require((census.canonical(record)+'\n').encode()==expected.read_bytes(),'entire compact expected record')
    print(census.canonical(record))

if __name__=='__main__':
    main()
