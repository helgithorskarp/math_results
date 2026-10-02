"""Positive AP producer for arbitrary Boolean rules on three affine inputs.

Fold coinciding inputs to one through three distinct ORIGINAL roots.
Inputs are affine F103 characters; every original root remains free.
Truth-table bit i has argument bits (i0,i1,i2); global output is gauged
at the all-zero abstract argument, independent of actual field patterns.
"""
import argparse
import csv
from itertools import permutations
from pathlib import Path

Q=103;M=618;ALL=(1<<M)-1;PACK=9
PERM=tuple(permutations(range(3)))
CHI=[None]+[int(pow(x,51,Q)!=1) for x in range(1,Q)]
COLUMNS=[sum(1<<n for n in range(M) if n%Q==r) for r in range(Q)]
STEPS=tuple(d for d in range(1,310) if d%Q)

def need(ok,message):
    if not ok:raise ValueError(message)

def changed_truth(word,pi,toggle):
    changed=0
    for assignment in range(8):
        old=sum((((assignment>>i)&1)^toggle)<<pi[i] for i in range(3))
        changed|=((word>>old)&1)<<assignment
    flip=changed&1
    return changed^(255 if flip else 0),flip

TRANSFORMS={(pi,toggle,word):changed_truth(word,pi,toggle)
    for pi in PERM for toggle in (0,1) for word in range(0,256,2)}

def action3(state,pi):
    t,word=state;roots=(0,1,t)
    s=(roots[pi[1]]-roots[pi[0]])%Q
    tnew=(roots[pi[2]]-roots[pi[0]])*pow(s,-1,Q)%Q
    transformed,flip=TRANSFORMS[pi,CHI[s],word]
    return (tnew,transformed),flip

def action2(word):
    changed=0
    for assignment in range(4):
        old=(1-((assignment>>1)&1))+2*(1-(assignment&1))
        changed|=((word>>old)&1)<<assignment
    flip=changed&1
    return changed^(15 if flip else 0),flip

def cases():
    out=[(1,0,word) for word in (0,2)]
    seen=set()
    for word in range(0,16,2):
        if word in seen:continue
        orbit={word,action2(word)[0]};seen|=orbit;out.append((2,0,word))
    need(len(out)==8 and seen==set(range(0,16,2)),'complete one/two-root cover')
    domain={(t,w) for t in range(2,Q) for w in range(0,256,2)};seen=set();hist={}
    for state in sorted(domain):
        if state in seen:continue
        orbit={action3(state,p)[0] for p in PERM}
        need(orbit<=domain and not orbit&seen,'disjoint parameter orbits')
        need(all({action3(member,p)[0] for p in PERM}==orbit for member in orbit),'root/truth orbit closure')
        seen|=orbit;out.append((3,*state));hist[len(orbit)]=hist.get(len(orbit),0)+1
    need(seen==domain and hist=={6:2144,3:16,2:8} and len(out)==2176,'complete2176 parameter classes')
    return out

def rotate(word,k):
    k%=M
    return ((word>>k)|(word<<(M-k)))&ALL

def root_labels(state):
    k,t,_=state
    return (0,) if k==1 else ((0,1) if k==2 else (0,1,t))

def discover(state,variant=0,target=PACK):
    roots=root_labels(state);word=state[2]
    field=[None if x in roots else (word>>sum(CHI[(x-r)%Q]<<i for i,r in enumerate(roots)))&1 for x in range(Q)]
    masks=[sum(1<<n for n in range(M) if field[n%Q] is not None and (field[n%Q]^int(n%6>=3))==b) for b in (0,1)]
    steps=list(STEPS)
    if variant in (2,3):steps.reverse()
    if variant>=4:
        order=variant-4;multipliers=(5,7,11,13,19,23,25,29,31,37,41,43)
        mult=multipliers[order%len(multipliers)];shift=order*29%len(steps)
        steps=[steps[(mult*i+shift)%len(steps)] for i in range(len(steps))]
    free=ALL;used=set();pairs=[]
    for d in steps:
        starts=0
        for mask in masks:
            eligible=mask&free;intersection=eligible
            for j in range(1,7):intersection&=rotate(eligible,j*d)
            starts|=intersection
        while starts:
            if variant<4:
                a=starts.bit_length()-1 if variant%2 else (starts&-starts).bit_length()-1
            else:
                offset=((variant-4)*37+state[1]*11+word)%M
                shifted=rotate(starts,offset);a=((shifted&-shifted).bit_length()-1+offset)%M
            support={(a+j*d)%Q for j in range(7)}
            need(len(support)==7 and not support&(set(roots)|used),'positive packing support')
            used|=support;pairs.append((a,d))
            if len(pairs)==target:return pairs
            blocked=sum(COLUMNS[r] for r in support);free&=ALL^blocked
            for j in range(7):starts&=ALL^rotate(blocked,j*d)
    return pairs

def positive_pack(state):
    best=[]
    for variant in range(68):
        pairs=discover(state,variant)
        if len(pairs)>len(best):best=pairs
        if len(best)==PACK:return best
    raise ValueError('positive packing incomplete at '+str(state)+'; found '+str(len(best))+'; no exclusion/optimum follows')

def main():
    p=argparse.ArgumentParser();p.add_argument('--first',type=int,required=True);p.add_argument('--last',type=int,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();states=cases();need(0<=args.first<args.last<=len(states),'valid canonical batch range')
    rows=[]
    for i in range(args.first,args.last):
        state=states[i];pairs=positive_pack(state);rows.append([i,*state,*[n for pair in pairs for n in pair]])
    header=['index','roots','t','truth']+[v for j in range(1,PACK+1) for v in ('a'+str(j),'step'+str(j))]
    with args.out.open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(header);writer.writerows(rows)
    print('COMPLETE_POSITIVE_BATCH: '+str(args.first)+'..'+str(args.last)+'; nine disjoint actual APs each')

if __name__=='__main__':main()
