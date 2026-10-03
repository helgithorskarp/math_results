"""Exact tagged root3 reductions for all38 entire explicit profile3 matrices. No private certificate is an input.

The algebraic four-cell producer is compared with literal ordinary22-point
mixed spines. All original indexed star domains are freshly regenerated for the selected
entire matrix. Every physical neighborhood is retained without a label quotient.
"""
import argparse
import hashlib
import itertools
import json
import math
import time

COUNTS = (0,0,3,1,2,3,0,2,2,2,0,0,2,1,0)
TYPES = tuple(t for t,n in enumerate(COUNTS,1) for _ in range(n))
MATRICES = {0: (0, 0, 0, 0, 0, 1, 0, 0, 20, 0, 1, 0, 16, 0, 0, 0, 64, 0), 1: (0, 0, 0, 0, 0, 1, 0, 4, 16, 0, 1, 0, 16, 0, 0, 0, 64, 0), 2: (0, 0, 0, 0, 0, 17, 0, 0, 4, 0, 1, 0, 0, 0, 16, 0, 64, 0), 3: (0, 0, 0, 0, 1, 16, 0, 0, 4, 0, 1, 0, 0, 0, 16, 0, 64, 0), 4: (0, 0, 0, 1, 0, 0, 0, 0, 20, 0, 0, 0, 17, 0, 0, 0, 64, 0), 5: (0, 0, 0, 1, 0, 0, 0, 0, 20, 0, 0, 1, 16, 0, 0, 0, 64, 0), 6: (0, 0, 0, 1, 0, 0, 0, 4, 16, 0, 0, 0, 17, 0, 0, 0, 64, 0), 7: (0, 0, 0, 1, 0, 0, 0, 4, 16, 0, 0, 1, 16, 0, 0, 0, 64, 0), 8: (0, 0, 0, 1, 0, 16, 0, 0, 4, 0, 0, 0, 1, 0, 16, 0, 64, 0), 9: (0, 0, 0, 1, 0, 17, 0, 0, 0, 0, 0, 0, 16, 0, 4, 0, 0, 64), 10: (0, 0, 0, 1, 1, 16, 0, 0, 0, 0, 0, 0, 16, 0, 4, 0, 0, 64), 11: (0, 0, 4, 0, 0, 16, 0, 0, 1, 0, 0, 0, 16, 0, 0, 0, 65, 0), 12: (0, 0, 4, 0, 0, 16, 0, 0, 1, 0, 0, 0, 16, 0, 0, 1, 64, 0), 13: (0, 0, 4, 0, 0, 16, 0, 0, 1, 0, 16, 0, 1, 0, 0, 0, 64, 0), 14: (0, 0, 4, 0, 0, 17, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 64, 1), 15: (0, 0, 4, 0, 0, 17, 0, 0, 0, 0, 16, 0, 0, 0, 1, 0, 64, 0), 16: (0, 0, 4, 0, 1, 16, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 64, 1), 17: (0, 0, 4, 0, 1, 16, 0, 0, 0, 0, 16, 0, 0, 0, 1, 0, 64, 0), 18: (0, 0, 4, 16, 0, 0, 0, 0, 1, 0, 0, 0, 17, 0, 0, 0, 64, 0), 19: (0, 0, 4, 16, 0, 0, 0, 0, 1, 0, 0, 1, 16, 0, 0, 0, 64, 0), 20: (0, 0, 4, 16, 0, 1, 0, 0, 0, 0, 0, 0, 16, 0, 1, 0, 64, 0), 21: (0, 0, 5, 16, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 64, 0), 22: (0, 0, 5, 16, 0, 0, 0, 0, 0, 1, 16, 0, 0, 0, 0, 0, 64, 0), 23: (0, 0, 16, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 81, 0), 24: (0, 0, 16, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 80, 0), 25: (0, 0, 16, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 16, 65, 0), 26: (0, 0, 16, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 17, 64, 0), 27: (0, 0, 16, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 68), 28: (0, 0, 16, 1, 0, 16, 0, 0, 4, 0, 0, 0, 64, 0, 0, 0, 1, 0), 29: (0, 0, 16, 1, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 4), 30: (0, 0, 16, 1, 0, 17, 0, 0, 4, 0, 64, 0, 0, 0, 0, 0, 0, 0), 31: (0, 0, 16, 1, 1, 16, 0, 0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 4), 32: (0, 0, 16, 1, 1, 16, 0, 0, 4, 0, 64, 0, 0, 0, 0, 0, 0, 0), 33: (0, 0, 16, 16, 0, 1, 0, 0, 4, 0, 1, 0, 64, 0, 0, 0, 0, 0), 34: (0, 0, 16, 17, 0, 0, 0, 0, 4, 0, 0, 0, 65, 0, 0, 0, 0, 0), 35: (0, 0, 16, 17, 0, 0, 0, 0, 4, 0, 0, 1, 64, 0, 0, 0, 0, 0), 36: (0, 1, 4, 16, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 64, 0), 37: (0, 1, 4, 16, 0, 0, 0, 0, 0, 1, 16, 0, 0, 0, 0, 0, 64, 0)}
CASE_ORDER = tuple(range(38))
MARKS = {0: 16, 1: 16, 2: 16, 3: 16, 4: 16, 5: 16, 6: 16, 7: 16, 8: 16, 9: 17, 10: 17, 11: 16, 12: 16, 13: 16, 14: 16, 15: 16, 16: 16, 17: 16, 18: 16, 19: 16, 20: 16, 21: 16, 22: 16, 23: 16, 24: 16, 25: 16, 26: 16, 27: 17, 28: 12, 29: 14, 30: 10, 31: 14, 32: 10, 33: 12, 34: 12, 35: 12, 36: 16, 37: 16}
MARK_FULL_TAGS = {0: (13, 64), 1: (13, 64), 2: (13, 64), 3: (13, 64), 4: (13, 64), 5: (13, 64), 6: (13, 64), 7: (13, 64), 8: (13, 64), 9: (14, 64), 10: (14, 64), 11: (13, 65), 12: (13, 64), 13: (13, 64), 14: (13, 64), 15: (13, 64), 16: (13, 64), 17: (13, 64), 18: (13, 64), 19: (13, 64), 20: (13, 64), 21: (13, 64), 22: (13, 64), 23: (13, 81), 24: (13, 80), 25: (13, 65), 26: (13, 64), 27: (14, 68), 28: (9, 64), 29: (10, 64), 30: (8, 64), 31: (10, 64), 32: (8, 64), 33: (9, 64), 34: (9, 65), 35: (9, 64), 36: (13, 64), 37: (13, 64)}
MARK_STAR_COUNTS = {0: 144, 1: 144, 2: 144, 3: 144, 4: 144, 5: 144, 6: 144, 7: 144, 8: 144, 9: 74, 10: 74, 11: 39, 12: 144, 13: 144, 14: 144, 15: 144, 16: 144, 17: 144, 18: 144, 19: 144, 20: 144, 21: 144, 22: 144, 23: 0, 24: 15, 25: 39, 26: 144, 27: 12, 28: 81, 29: 45, 30: 63, 31: 45, 32: 63, 33: 81, 34: 24, 35: 81, 36: 144, 37: 144}
PAIRS = {0: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 1: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 2: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 3: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 4: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 5: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 6: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 7: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 8: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 9: ((9, 11), (9, 12), (9, 15), (9, 16), (10, 11), (10, 12), (10, 15), (10, 16), (11, 12), (11, 13), (11, 14), (12, 13), (12, 14)), 10: ((9, 11), (9, 12), (9, 15), (9, 16), (10, 11), (10, 12), (10, 15), (10, 16), (11, 12), (11, 13), (11, 14), (12, 13), (12, 14)), 11: ((9, 10), (9, 13), (9, 14), (10, 13), (10, 14)), 12: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 13: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 14: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 15: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 16: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 17: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 18: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 19: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 20: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 21: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 22: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 23: (), 24: ((9, 10), (9, 13), (9, 14), (10, 13), (10, 14)), 25: ((9, 10), (9, 13), (9, 14), (10, 13), (10, 14)), 26: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 27: ((9, 11), (9, 12), (10, 11), (10, 12)), 28: ((9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (11, 13), (11, 14), (13, 14)), 29: ((9, 15), (9, 16), (10, 15), (10, 16), (11, 12)), 30: ((9, 11), (9, 12), (9, 15), (9, 16), (9, 17), (11, 12), (11, 13), (11, 14), (12, 13), (12, 14)), 31: ((9, 15), (9, 16), (10, 15), (10, 16), (11, 12)), 32: ((9, 11), (9, 12), (9, 15), (9, 16), (9, 17), (11, 12), (11, 13), (11, 14), (12, 13), (12, 14)), 33: ((9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (11, 13), (11, 14), (13, 14)), 34: ((9, 13), (9, 14), (10, 13), (10, 14)), 35: ((9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (11, 13), (11, 14), (13, 14)), 36: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)), 37: ((9, 11), (9, 12), (9, 13), (9, 14), (9, 17), (10, 11), (10, 12), (10, 13), (10, 14), (10, 17), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14))}
ROOT_LOW = 3
B = tuple(range(9))
CELLS = ((0,1,2),(3,),(4,5),(6,7,8))
CASE_INDEX = 0
COLUMNS = MATRICES[CASE_INDEX]
MARK = MARKS[CASE_INDEX]
A = tuple(x for x,t in enumerate(TYPES) if t&8 and x!=MARK)+(MARK,)
ALLOWED_PAIRS = PAIRS[CASE_INDEX]
REPRESENTATIVE_PAIRS = ALLOWED_PAIRS


def select(case):
    global CASE_INDEX,COLUMNS,MARK,A,ALLOWED_PAIRS,REPRESENTATIVE_PAIRS
    require(type(case) is int and case in MATRICES,"Selected explicit case outside complete38 profile3 inventory")
    CASE_INDEX=case;COLUMNS=MATRICES[case];MARK=MARKS[case]
    A=tuple(x for x,t in enumerate(TYPES) if t&8 and x!=MARK)+(MARK,)
    ALLOWED_PAIRS=PAIRS[case];REPRESENTATIVE_PAIRS=ALLOWED_PAIRS


def require(ok, message):
    if not ok: raise ValueError(message)


class Guard:
    def __init__(self):
        self.start=time.monotonic(); self.work=0

    def tick(self):
        if self.work>=2000000 or time.monotonic()-self.start>=40:
            raise ValueError('Operational reduction guard; incomplete, no exclusion')
        self.work+=1


def encode(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def sigma(x,i):
    return (COLUMNS[x]>>(2*i))&3


def image_word(word,phi):
    return sum(1<<phi[x] for x in range(18) if word&(1<<x))


def actions():
    return [tuple(range(18))]  # Every labelled graph is retained; no quotient action.


def configuration():
    require((TYPES[MARK], COLUMNS[MARK])==MARK_FULL_TAGS[CASE_INDEX], "Selected whole derived-mark tag differs")
    require(len(TYPES)==18 and len(A)==9 and A[-1]==MARK
            and [x for x in A if sigma(x,3)==1]==[MARK],
            'Whole derived marked high-type frame differs')
    require(tuple(x for x,t in enumerate(TYPES) if t&8)==tuple(sorted(A)),
            'Root red neighborhood is not the displayed nine highs')
    require(all(sum(bool(t&(1<<i)) for t in TYPES)==9 for i in range(4)),
            'Low degree margin differs')
    budget=[72-sum(10-TYPES[x].bit_count() for x in range(18) if TYPES[x]&(1<<i))
            for i in range(4)]
    require(budget==[2,1,2,1], 'Profile3 mixed row budgets differ')
    require([sum(sigma(x,i) for x in range(18)) for i in range(4)]==budget,
            'Selected case entire mixed matrix row sums differ')
    require([sum(sigma(x,i) for x in range(18) if TYPES[x]&(1<<i))
             for i in range(4)]==[1]*4, 'Selected case red row subtotals differ')
    require(all(sigma(x,i) in (0,1) for x in range(18) for i in range(4)),
            'No-carry deficit component differs')
    require(all(sum(sigma(x,i) for x in range(18) if TYPES[x]&(1<<j))==
                sum(sigma(x,j) for x in range(18) if TYPES[x]&(1<<i))
                for i in range(4) for j in range(4)),
            'Necessary mixed transport is not symmetric')
    require([3-sigma(x,3) for x in A]==[3]*8+[2],
            'Distinguished local degree sequence differs')
    require([5-sigma(x,3) for x in B]==[5]*9, 'Cut column ranks differ')
    require(all(0<=10-TYPES[x].bit_count()-(3-sigma(x,3))<=9 for x in A)
            and 10-TYPES[MARK].bit_count()-2 in (5,6,7), 'Derived cut row ranks differ')
    require(tuple(tuple(B.index(x) for x in B if TYPES[x]==t) for t in (3,4,5,6))==CELLS,
            'Outside four-cell partition differs')
    return budget


def cell_producer(guard):
    """Solve the four integer equations before generating physical cut words."""
    records=[];stars=[]
    for neighbors in itertools.combinations(A[:-1],2):
        guard.tick()
        r=[(3 if TYPES[MARK]&(1<<i) else 5)-sigma(MARK,i)-
           sum(bool(TYPES[x]&(1<<i)) for x in neighbors) for i in range(3)]
        s=10-TYPES[MARK].bit_count()-2
        b=2*s-sum(r);a=r[0]+r[1]-s+b;c=s-b-r[1];d=s-b-r[0]
        counts=(a,b,c,d)
        words=[]
        if all(0<=n<=len(cell) for n,cell in zip(counts,CELLS)):
            for chosen in itertools.product(*(itertools.combinations(cell,n)
                                              for cell,n in zip(CELLS,counts))):
                guard.tick()
                word=sum(1<<x for group in chosen for x in group)
                words.append(word)
                stars.append(sum(1<<x for x in neighbors)+
                             sum(1<<B[j] for j in range(9) if word&(1<<j)))
        records.append(dict(neighbors=list(neighbors),remaining_low_counts=r,
                            four_cell_counts=list(counts),cut_words=sorted(words)))
    require(tuple(tuple(r['neighbors']) for r in records if r['cut_words'])==ALLOWED_PAIRS,
            'Whole necessary distinguished neighbor-pair set differs')
    require(len(stars)==len(set(stars))==MARK_STAR_COUNTS[CASE_INDEX], 'Whole four-cell star set differs')
    return records,sorted(stars)


def literal_original_domains(guard):
    """Direct physical22-point neighborhoods; no four-cell formula is read."""
    allpoints=(1<<22)-1
    low_red=[sum(1<<(4+x) for x,t in enumerate(TYPES) if t&(1<<i)) for i in range(4)]
    low_blue=[allpoints^(1<<i)^low_red[i] for i in range(4)]
    result=[];raw=0
    for x,t in enumerate(TYPES):
        kept=[]
        for chosen in itertools.combinations([y for y in range(18) if y!=x],10-t.bit_count()):
            guard.tick();raw+=1
            star=sum(1<<y for y in chosen)
            red=t|(star<<4)
            blue=allpoints^(1<<(4+x))^red
            deficits=[]
            for i in range(4):
                is_red=bool(t&(1<<i))
                pages=((low_red[i]&red) if is_red else (low_blue[i]&blue)).bit_count()
                deficits.append((3 if is_red else 6)-pages)
            if deficits==[sigma(x,i) for i in range(4)]: kept.append(star)
        result.append(sorted(kept))
    require(raw==422994, 'Complete original physical star cardinality differs')
    return result,raw


def literal_mark_sets(guard):
    """A second literal decoder for all selected root stars, using actual sets."""
    universe=set(range(22));low=[{4+x for x,t in enumerate(TYPES) if t&(1<<i)}
                                for i in range(4)]
    expected=[sigma(MARK,i) for i in range(4)];kept=[];raw=0
    for chosen in itertools.combinations([x for x in range(18) if x!=MARK],10-TYPES[MARK].bit_count()):
        guard.tick();raw+=1
        red={i for i in range(4) if TYPES[MARK]&(1<<i)}|{4+x for x in chosen}
        blue=universe-red-{4+MARK}
        deficits=[]
        for i in range(4):
            if i in red: pages=len(low[i]&red);cap=3
            else: pages=len((universe-low[i]-{i})&blue);cap=6
            deficits.append(cap-pages)
        if deficits==expected: kept.append(sum(1<<x for x in chosen))
    require(raw==math.comb(17,10-TYPES[MARK].bit_count()), 'Literal mark-subset domain incomplete')
    return sorted(kept),raw


def run():
    guard=Guard();configuration()
    produced,stars=cell_producer(guard)
    domains,raw=literal_original_domains(guard)
    literal,mark_raw=literal_mark_sets(guard)
    require(stars==domains[MARK]==literal, 'Whole algebraic and both literal mark stars differ')
    phis=actions();transports=[]
    for phi in phis:
        require(sorted(phi)==list(range(18)), 'Selected high image is not a bijection')
        require(all(TYPES[x]==TYPES[phi[x]] and COLUMNS[x]==COLUMNS[phi[x]]
                    for x in range(18)), 'Selected image changes a whole type/deficit tag')
        for x,row in enumerate(domains):
            for word in row: guard.tick()
            require(sorted(image_word(word,phi) for word in row)==domains[phi[x]],
                    'Complete original indexed star domains do not transport')
        transports.append(list(phi))
    action_set=set(phis)
    require(all(tuple(p[q[x]] for x in range(18)) in action_set for p in phis for q in phis),
            'Selected label actions do not form a group')
    for pair in ALLOWED_PAIRS:
        require(any(tuple(sorted(p[x] for x in pair)) in REPRESENTATIVE_PAIRS for p in phis),
                'Allowed pair has no selected representative transport')
    # Actual semantic coverage probes: dropping a valid star, replacing a
    # pair by the forbidden two type8 points, and swapping unequal full tags must fail.
    if stars:
        require(stars[:-1]!=literal, 'Missing valid physical star was accepted')
    else:
        fabricated=sum(1<<x for x in next(itertools.combinations([x for x in range(18) if x!=MARK],10-TYPES[MARK].bit_count())))
        require([fabricated]!=literal, 'Invalid nonempty physical star pool was accepted')
    forbidden=next(r for r in produced if not r['cut_words'])
    require(tuple(forbidden['neighbors']) not in ALLOWED_PAIRS,
            'An actual cell-forbidden physical pair was admitted')
    bad=list(range(18));bad[9],bad[11]=bad[11],bad[9]
    require(any((TYPES[x],COLUMNS[x])!=(TYPES[bad[x]],COLUMNS[bad[x]]) for x in range(18)),
            'Unequal-tag label swap was accepted')
    result=dict(agent='six-books-3',role='researcher',
        status='COMPLETE_NECESSARY_TAGGED_ROOT3_NEIGHBOR_REDUCTION',case_index=CASE_INDEX,
        counts=list(COUNTS),high_types=list(TYPES),columns=list(COLUMNS),
        root_low=ROOT_LOW,distinguished_high=MARK,ordered_A=list(A),ordered_B=list(B),
        A_tags=[[TYPES[x],COLUMNS[x]] for x in A],B_tags=[[TYPES[x],COLUMNS[x]] for x in B],
        A_local_degrees=[3]*8+[2],cut_row_ranks=[10-TYPES[x].bit_count()-(3-sigma(x,3)) for x in A],cut_column_ranks=[5]*9,
        four_cell_sizes=[3,1,2,3],all28_pair_records=produced,
        whole_distinguished_stars=stars,whole_original_indexed_domains=domains,
        original_raw_stars=raw,literal_set_raw_mark_stars=mark_raw,
        selected_label_actions=transports,allowed_physical_pairs=[list(p) for p in ALLOWED_PAIRS],
        representative_pairs=[list(p) for p in REPRESENTATIVE_PAIRS],
        whole_original_indexed_star_count=sum(map(len,domains)),
        all_original_domains_literal_transported=True,
        actual_host_automorphism_required=False,case_excluded=any(not row for row in domains),
        empty_original_high_domains=[x for x,row in enumerate(domains) if not row],
        whole_profile_excluded=False,ordinary_bridges_formalized=False,
        independent_person_review=False,semantic_damage_probes=3,actual_forbidden_pair=forbidden['neighbors'],
        work_units=guard.work,work_guard=2000000,internal_seconds_guard=40)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out');parser.add_argument('--case',type=int,required=True)
    args=parser.parse_args();select(args.case);record=run();data=encode(record)
    if args.out:
        from pathlib import Path
        Path(args.out).write_bytes(data+b'\n')
    print(json.dumps(dict(status=record['status'],raw_stars=record['original_raw_stars'],
        complete_original_stars=record['whole_original_indexed_star_count'],
        distinguished_stars=len(record['whole_distinguished_stars']),
        allowed_pairs=record['allowed_physical_pairs'],representative_pairs=record['representative_pairs'],
        whole_record_bytes=len(data),whole_record_sha256=hashlib.sha256(data).hexdigest(),
        work_units=record['work_units']),sort_keys=True,separators=(',',':')))
