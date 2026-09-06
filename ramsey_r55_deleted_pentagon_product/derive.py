#!/usr/bin/env python3
"""Factor all 24-bit attachment stars through five local status words."""
from itertools import combinations,product
import hashlib,json
from pathlib import Path


def red(u,v):
    i,a=divmod(u,5);j,b=divmod(v,5)
    return (a-b)%5 in (1,4) if i==j else (i-j)%5 in (1,4)


def active(mask,n):
    r=any(mask>>i&1 and mask>>j&1 and (i-j)%5 in (1,4)
          for i,j in combinations(range(n),2))
    b=any(not(mask>>i&1) and not(mask>>j&1) and (i-j)%5 not in (1,4)
          for i,j in combinations(range(n),2))
    return int(r)+2*int(b)


def digest(values):
    return hashlib.sha256(''.join(f'{x}\n' for x in sorted(values)).encode()).hexdigest()


def derive():
    tables={str(n):[[m for m in range(1<<n) if active(m,n)==s] for s in range(4)] for n in (4,5)}
    valid=[]; rejected_weight=0; weights=[]
    for word in product(range(4),repeat=5):
        weight=1
        for i,s in enumerate(word):weight*=len(tables[str(4 if i==4 else 5)][s])
        ok=not any((word[i]&1 and word[j]&1 and (i-j)%5 in (1,4)) or
                   (word[i]&2 and word[j]&2 and (i-j)%5 not in (1,4))
                   for i,j in combinations(range(5),2))
        weights.append([list(word),weight,ok])
        if ok and weight:valid.append([list(word),weight])
        else:rejected_weight+=weight
    stars=set()
    for word,weight in valid:
        choices=[tables[str(4 if i==4 else 5)][s] for i,s in enumerate(word)]
        for masks in product(*choices):
            stars.add(sum(m<<(5*i) for i,m in enumerate(masks)))
    if sum(w for _,w in valid)+rejected_weight!=1<<24:raise RuntimeError('coverage')
    edges=[[u,v] for u,v in combinations(range(24),2) if red(u,v)]
    four_counts=[sum(all(red(u,v)==bool(color) for u,v in combinations(q,2)) for q in combinations(range(24),4)) for color in (0,1)]
    result={'schema':1,'core_order':24,'core_red_edges':edges,'free_pairs_at_43':627,
            'bag_status_masks':tables,'status_words_checked':1024,
            'feasible_positive_weight_words':valid,'complete_star_count':len(stars),
            'rejected_star_count':rejected_weight,'star_set_sha256':digest(stars),
            'signature_table_sha256':hashlib.sha256(json.dumps(weights,separators=(',',':')).encode()).hexdigest(),
            'core_four_cliques_blue_red':four_counts,'forced_red':[20,23],'forced_blue':[21,22]}
    return result,stars

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    result,_=derive();out=json.dumps(result,indent=2)+'\n'
    if a.write:(Path(__file__).resolve().parent/'certificate.json').write_text(out)
    else:print(out,end='')
