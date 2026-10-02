"""Positive certificate producer: root permutations and Euler/bitset APs."""
import argparse
import csv
from itertools import permutations
from pathlib import Path

Q=103;M=618;ALL=(1<<M)-1;PACK=9

def need(ok,message):
    if not ok:raise ValueError(message)

def action(state,pi):
    t,d2,d3=state;roots=(0,1,t);bits=(0,d2,d3)
    scale=(roots[pi[1]]-roots[pi[0]])%Q
    image=((roots[pi[2]]-roots[pi[0]])*pow(scale,-1,Q)%Q,
           bits[pi[1]]^bits[pi[0]],bits[pi[2]]^bits[pi[0]])
    return image

def representatives():
    universe={(t,a,b) for t in range(2,Q) for a in range(2) for b in range(2)}
    remaining=set(universe);out=[];sizes=[]
    while remaining:
        root=min(remaining);orbit={action(root,p) for p in permutations(range(3))}
        need(orbit<=remaining,'invalid or overlapping parameter orbit')
        need(all({action(s,p) for p in permutations(range(3))}==orbit for s in orbit),'parameter action not an orbit')
        remaining-=orbit;out.append(root);sizes.append(len(orbit))
    need(len(out)==69 and sorted(sizes)==[2,3,3]+[6]*66,'complete69 orbit reduction')
    return out

def rotate(word,k):
    k%=M
    return ((word>>k)|(word<<(M-k)))&ALL

def discover(state,variant=0,target=PACK):
    t,d2,d3=state;roots={0,1,t}
    chi=[None]+[int(pow(z,51,Q)!=1) for z in range(1,Q)]
    field=[None if x in roots else int(sum((chi[x],chi[(x-1)%Q]^d2,chi[(x-t)%Q]^d3))>=2) for x in range(Q)]
    masks=[sum(1<<n for n in range(M) if field[n%Q] is not None and (field[n%Q]^int(n%6>=3))==b) for b in (0,1)]
    steps=[d for d in range(1,310) if d%Q]
    if variant in (2,3):steps.reverse()
    if variant>=4:
        order=variant-4
        multipliers=(5,7,11,13,19,23,25,29,31,37,41,43)
        multiplier=multipliers[order%len(multipliers)];shift=order*29%len(steps)
        steps=[steps[(multiplier*k+shift)%len(steps)] for k in range(len(steps))]
    used=set();pairs=[]
    for d in steps:
        free=ALL^sum(1<<n for n in range(M) if n%Q in used)
        candidates=0
        for mask in masks:
            eligible=mask&free;word=eligible
            for j in range(1,7):word&=rotate(eligible,j*d)
            candidates|=word
        while candidates:
            if variant<4:
                a=candidates.bit_length()-1 if variant%2 else (candidates&-candidates).bit_length()-1
            else:
                offset=((variant-4)*37+t*11)%M
                shifted=rotate(candidates,offset)
                a=((shifted&-shifted).bit_length()-1+offset)%M
            support={(a+j*d)%Q for j in range(7)}
            need(len(support)==7 and not support&(roots|used),'invalid disjoint producer support')
            used|=support;pairs.append((a,d))
            if len(pairs)==target:return pairs
            blocked=sum(1<<n for n in range(M) if n%Q in support)
            for j in range(7):candidates&=ALL^rotate(blocked,j*d)
    return pairs

def generate(path):
    rows=[]
    for i,state in enumerate(representatives()):
        best=[]
        for variant in range(68):
            pairs=discover(state,variant)
            if len(pairs)>len(best):best=pairs
            if len(best)==PACK:break
        need(len(best)==PACK,'incomplete positive certificate at '+str(state))
        rows.append([i,*state,*[x for pair in best for x in pair]])
    header=['index','t','d2','d3']+[v for j in range(1,PACK+1) for v in ('a'+str(j),'step'+str(j))]
    with path.open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(header);writer.writerows(rows)
    print('COMPLETE_POSITIVE_CERTIFICATE: 69 parameter orbits; 9 disjoint APs each')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();generate(args.out)

if __name__=='__main__':main()
