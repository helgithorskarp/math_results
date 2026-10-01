"""Literal historical blocks and finite controls for the ordinary coding proof."""
from collections import Counter
from hashlib import sha256
from itertools import combinations,product
from marked import canonical,packing,require
from classify import maps

def historical():
    # Transcribed from Stanton--Street1987 scanned pp208,213 (CaseVII(f)).
    words='ABCD EFGH IJKL MNOP AEIM BFJN CGKO DHLP AHJO BGIP CFLM DEKN AGLN BHKM CEJP DFIO AFKP BELO CHIN DGJM'.split()
    replaced={'ABCD':'BCD','EFGH':'FGH','AFKP':'AKP','BELO':'ELO'}
    return tuple(sorted(tuple(sorted(tuple(ord(c)-65 for c in replaced.get(w,w))+((16,) if w in replaced else ()))) for w in words))

def gf4(a,b):
    value=0
    while b:
        if b&1:value^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return value

def isolation_is_essential():
    rows=[tuple(4*x+y for y in range(4)) for x in range(4)]
    lines=rows+[tuple(4*x+(gf4(m,x)^b) for x in range(4)) for m,b in product(range(4),repeat=2)]
    counts=Counter(p for q in lines for p in combinations(sorted(q),2))
    require(len(lines)==len(set(lines))==20 and len(counts)==120 and set(counts.values())=={1},'invalid affine fixture')
    blocks=tuple(sorted(tuple(sorted(16 if y==0 else 4*x+y for y in range(4))) for x in range(4)))+tuple(lines[4:])
    blocks=tuple(sorted(tuple(sorted(q)) for q in blocks))
    reps=tuple(sum(x in q for q in blocks) for x in range(17))
    counts=Counter(p for q in blocks for p in combinations(q,2))
    require(len(counts)==120 and set(counts.values())=={1} and sorted(reps)==[4]*5+[5]*12,'invalid switched fixture')
    H={x for x,n in enumerate(reps) if n==4};leave=set(combinations(range(17),2))-set(counts)
    core=tuple(sorted(p for p in leave if set(p)<=H))
    require(core==tuple((x,16) for x in (0,4,8,12)) and all(set(p)&H for p in leave),'wrong high core')
    require(all(any(x in p for p in core) for x in H),'isolated high point in K1,4')
    return dict(blocks=blocks,high=sorted(H),core=core,core_type='K1,4',marked_isolation_absent=True)

def bridge(reference,target):
    graphs=[]
    for mask in range(8):
        pairs=tuple(p for i,p in enumerate(combinations(range(3),2)) if mask>>i&1)
        degrees=tuple(sum(x in p for p in pairs) for x in range(3))
        J=sum(n in (0,2) for n in degrees)
        require(J==1+2*int(len(pairs) in (0,3)),'homogeneous triple identity')
        graphs.append(dict(mask=mask,degrees=degrees,homogeneous=J))
    allowed=tuple(5-f for f in range(5) if f<=f*(f-1)//2)
    require(allowed==(5,2,1),'wrong deficit possibilities')
    patterns=sorted([a,b,c] for a,b,c in product(range(18),repeat=3) if a+b+c==17 and a+2*b+5*c==25)
    require(patterns==[[9,8,0],[12,4,1],[15,0,2]],'integer pattern list incomplete')
    require(all(4*a+3*b==60 and a>=9 for a,b,c in patterns),'degree/template count')
    require(355-17*20==15 and 816-71*10==106 and 136-6*15==46 and 106-46==60,'ordinary counts')
    require(85-4*15==25 and 68-25==43 and 43+17+46==106,'homogeneous equality chain')
    require(30*4==60*2 and 136-30==60+46,'edge/nonedge path counts')
    hist=historical();packing(hist,16)
    isom,tries=maps(hist,reference,16,14)
    require(len(isom)==8,'historical fixture outside class')
    require(patterns==target['near71_pair_deficit_counts_1_2_5'] and target['near71_saturated_deficit_graph_edges']==30 and target['near71_uncovered_triples_sat']==60 and target['near71_uncovered_triples_through_unique_unsaturated']==46,'target arithmetic differs')
    return dict(status='COMPLETE',three_point_graphs=graphs,patterns=patterns,allowed_x_pair_deficits=allowed,
                B_edges=30,B_uncovered_triples=60,x_uncovered_triples=46,
                historical_fixture=hist,historical_fixture_sha256=sha256(canonical(hist)).hexdigest(),
                historical_isomorphisms=8,historical_map_candidates=tries,historical_first_isomorphism=isom[0],
                isolation_counterexample=isolation_is_essential(),ordinary_proof_is_not_formalized=True)
