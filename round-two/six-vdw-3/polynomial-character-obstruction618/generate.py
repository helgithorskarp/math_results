"""Produce positive AP certificates using Euler characters and bit rotations."""
import argparse
import csv
from pathlib import Path

Q=103
PERIOD=618
ALL=(1<<PERIOD)-1
PACKING=8
HEADER=['index','c0','c1','c2','c3']+[x for j in range(1,9) for x in ('a'+str(j),'d'+str(j))]

def need(condition,message):
    if not condition:raise ValueError(message)

def templates():
    out=[(1,0,0,0),(0,1,0,0)]
    out += [((-a)%Q,0,1,0) for a in (0,1,3)]
    out += [(0,a,0,1) for a in (0,1,3)]
    out += [(b,a,0,1) for b in (1,5,25) for a in range(Q)]
    need(len(out)==317 and len(set(out))==317,'canonical coefficient inventory')
    return out

def rotate_right(word,shift):
    shift%=PERIOD
    return ((word>>shift)|(word<<(PERIOD-shift)))&ALL

def discover(coefficients,variant):
    character=[None]+[int(pow(z,51,Q)!=1) for z in range(1,Q)]
    orientation=[]
    for x in range(Q):
        z=0
        for c in reversed(coefficients):z=(z*x+c)%Q
        orientation.append(character[z])
    masks=[sum(1<<n for n in range(PERIOD)
               if orientation[n%Q] is not None and
               (orientation[n%Q]^int(n%6>=3))==b) for b in (0,1)]
    steps=[d for d in range(1,PERIOD//2+1) if d%Q]
    need(0<=variant<4,'unknown fixed search order')
    if variant>=2:steps.reverse()
    used=set();pairs=[]
    for d in steps:
        allowed=ALL^sum(1<<n for n in range(PERIOD) if n%Q in used)
        candidate=0
        for mask in masks:
            eligible=mask&allowed;starts=eligible
            for j in range(1,7):starts&=rotate_right(eligible,j*d)
            candidate|=starts
        while candidate:
            a=candidate.bit_length()-1 if variant%2 else (candidate&-candidate).bit_length()-1
            support={(a+j*d)%Q for j in range(7)}
            need(len(support)==7 and not support&used,'producer disjoint support')
            need(all(orientation[x] is not None for x in support),'producer root avoidance')
            used.update(support);pairs.append((a,d))
            if len(pairs)==PACKING:return pairs
            blocked=sum(1<<n for n in range(PERIOD) if n%Q in support)
            for j in range(7):candidate&=ALL^rotate_right(blocked,j*d)
    return None

def generate(path):
    rows=[]
    for index,coeff in enumerate(templates()):
        pairs=None
        for variant in range(4):
            pairs=discover(coeff,variant)
            if pairs is not None:break
        need(pairs is not None,'incomplete positive certificate at index '+str(index))
        rows.append([index,*coeff,*[v for pair in pairs for v in pair]])
    with path.open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(HEADER);writer.writerows(rows)
    print('COMPLETE_POSITIVE_CERTIFICATE: 317 polynomials; 8 disjoint APs each')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();generate(args.out)

if __name__=='__main__':main()
