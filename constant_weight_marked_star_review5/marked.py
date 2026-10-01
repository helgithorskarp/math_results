"""Reviewer-owned labelled carrier and complete whole-point-star search."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import comb
import time
import json

def require(value,message):
    if not value:raise ValueError(message)

def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

class Incomplete(RuntimeError):pass

class Guard:
    def __init__(self,limit=200000,seconds=10):
        require(type(limit)is int and 0<=limit<=200000 and 0<seconds<=10,'invalid guards')
        self.nodes=0;self.limit=limit;self.seconds=seconds;self.began=time.monotonic()
    def tick(self):
        self.nodes+=1
        if self.nodes>self.limit or (self.nodes%64==0 and time.monotonic()-self.began>self.seconds):
            raise Incomplete('whole-star guard reached')

def bits(value):
    while value:
        low=value&-value;yield low.bit_length()-1;value-=low

def model():
    cells=tuple((r,c) for r in range(4) for c in range(4) if r!=c)
    anchors=((12,13,15,16),)
    anchors+=tuple(tuple(i for i,cell in enumerate(cells) if cell[0]==r)+(15,) for r in range(4))
    anchors+=tuple(tuple(i for i,cell in enumerate(cells) if cell[1]==c)+(16,) for c in range(4))
    anchors=tuple(tuple(sorted(q)) for q in anchors)
    used=Counter(p for q in anchors for p in combinations(q,2))
    require(len(anchors)==9 and len(used)==54 and set(used.values())=={1},'invalid anchors')
    eligible=tuple(p for p in combinations(range(15),2) if p not in used)
    candidates=tuple(q for q in combinations(range(15),4) if all(p not in used for p in combinations(q,2)))
    # An independently expressed cell criterion checks all1365quadruples.
    alternate=tuple(q for q in combinations(range(15),4) if not {12,13}<=set(q)
                    and len({cells[x][0] for x in q if x<12})==len([x for x in q if x<12])
                    and len({cells[x][1] for x in q if x<12})==len([x for x in q if x<12]))
    require(len(eligible)==80 and len(candidates)==225 and candidates==alternate,'incomplete literal universe')
    return dict(cells=cells,anchors=anchors,used=frozenset(used),eligible=eligible,candidates=candidates)

def instance(data,other_high):
    other_high=tuple(other_high);H=frozenset(other_high)|{14}
    require(len(other_high)==4 and len(H)==5 and set(other_high)<=set(range(14)),'invalid high placement')
    R=sum(p in data['used'] for p in combinations(other_high,2))
    target=tuple(4 if x in H else 5 for x in range(17))
    quota=tuple(target[x]-sum(x in q for q in data['anchors']) for x in range(15))
    require(min(quota)>=0 and sum(quota)==44,'invalid residual point quotas')
    columns=tuple(q for q in data['candidates'] if comb(len(set(q)&set(other_high)),2)<=2-R)
    mandatory=tuple(p for p in data['eligible'] if not(set(p)&H) or 14 in p and set(p)<=H)
    if R<=2:require(all(set(combinations(q,2))&set(mandatory) for q in columns),'unexplained optional column')
    return dict(high=other_high,R=R,direct=R>2,quota=quota,columns=columns,mandatory=mandatory)

def solve(eligible,columns,quota,mandatory,limit=200000,seconds=10):
    quota=tuple(quota);columns=tuple(tuple(q) for q in columns)
    require(len(quota)==15 and all(type(x)is int and x>=0 for x in quota),'invalid quota')
    require(len(set(eligible))==len(eligible) and all(tuple(sorted(set(p)))==p and len(p)==2 and all(type(x)is int and 0<=x<15 for x in p) for p in eligible),'invalid pair universe')
    require(len(set(columns))==len(columns),'duplicate columns')
    index={p:i for i,p in enumerate(eligible)}
    require(len(set(mandatory))==len(mandatory) and set(mandatory)<=set(eligible),'invalid mandatory pairs')
    masks=[];point_rows=[0]*15;pair_rows=[0]*len(eligible)
    for i,q in enumerate(columns):
        require(len(q)==4 and tuple(sorted(set(q)))==q and all(type(x)is int and 0<=x<15 for x in q),'invalid quadruple')
        pairs=tuple(combinations(q,2));require(set(pairs)<=set(eligible),'column outside pair universe')
        masks.append(sum(1<<index[p] for p in pairs))
        for x in q:point_rows[x]|=1<<i
        for p in pairs:pair_rows[index[p]]|=1<<i
    conflicts=[]
    for mask in masks:
        value=0
        for e in bits(mask):value|=pair_rows[e]
        conflicts.append(value)
    incident=[sum(1<<i for i,p in enumerate(eligible) if x in p) for x in range(15)]
    need=sum(1<<index[p] for p in mandatory);active=(1<<len(columns))-1
    for x,n in enumerate(quota):
        if not n:active&=~point_rows[x]
    guard=Guard(limit,seconds);output=[]
    def visit(left,need,active,chosen):
        guard.tick()
        if not any(left):
            if not need:output.append(tuple(sorted(chosen)))
            return
        if any((active&point_rows[x]).bit_count()<n for x,n in enumerate(left)):return
        if any(not(active&pair_rows[e]) for e in bits(need)):return
        v=min((x for x,n in enumerate(left) if n),
              key=lambda x:(comb((active&point_rows[x]).bit_count(),left[x]),x))
        def star(options,count,left,need,active,chosen):
            guard.tick()
            if not count:
                if not(need&incident[v]):visit(left,need,active,chosen)
                return
            if options.bit_count()<count:return
            if any(not(options&pair_rows[e]) for e in bits(need&incident[v])):return
            while options:
                i=next(bits(options));options&=options-1
                after=list(left);zero=0
                for x in columns[i]:
                    after[x]-=1;require(after[x]>=0,'quota underflow')
                    if not after[x]:zero|=point_rows[x]
                remaining=active&~conflicts[i]&~zero
                star(options&remaining,count-1,tuple(after),need&~masks[i],remaining,chosen+(i,))
        star(active&point_rows[v],left[v],left,need,active,chosen)
    visit(quota,need,active,())
    require(len(set(output))==len(output),'duplicated complete packing')
    return tuple(sorted(output)),guard.nodes

def packing(blocks,marked=14):
    blocks=tuple(sorted(tuple(sorted(q)) for q in blocks))
    require(len(blocks)==len(set(blocks))==20 and all(len(q)==len(set(q))==4 and all(type(x)is int and 0<=x<17 for x in q) for q in blocks),'malformed20packing')
    pairs=Counter(p for q in blocks for p in combinations(q,2));require(len(pairs)==120 and set(pairs.values())=={1},'repeated pair')
    reps=tuple(sum(x in q for q in blocks) for x in range(17));require(sorted(reps)==[4]*5+[5]*12,'wrong unit profile')
    H=frozenset(x for x,n in enumerate(reps) if n==4)
    leave=frozenset(combinations(range(17),2))-set(pairs)
    core=tuple(p for p in sorted(leave) if set(p)<=H)
    require(marked in H and len(core)==4 and all(marked not in p for p in core),'incorrect marked high core')
    require(all(set(p)&H for p in leave),'low-low leave edge')
    return dict(blocks=blocks,reps=reps,high=H,leave=leave,core=core)
