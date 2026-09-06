"""Exact activity factors and the five-class cancellation certificate."""
from itertools import combinations,product
import hashlib,json


def red(u,v):
    i,a=divmod(u,5);j,b=divmod(v,5)
    return (a-b)%5 in (1,4) if i==j else abs(i-j)==1


def produce():
    tables=[[],[],[],[]]
    for m in range(32):
        r=any(m>>i&1 and m>>j&1 and (i-j)%5 in (1,4) for i,j in combinations(range(5),2))
        b=any(not(m>>i&1) and not(m>>j&1) and (i-j)%5 not in (1,4) for i,j in combinations(range(5),2))
        tables[int(r)+2*int(b)].append(m)
    words=[];stars=set()
    for w in product(range(4),repeat=4):
        if any((w[i]&1 and w[j]&1 and abs(i-j)==1) or (w[i]&2 and w[j]&2 and abs(i-j)!=1) for i,j in combinations(range(4),2)):continue
        if not all(tables[s] for s in w):continue
        words.append(list(w))
        stars.update(sum(m<<(5*i) for i,m in enumerate(ms)) for ms in product(*(tables[s] for s in w)))
    edges=[[i,(i+1)%5] for i in range(5)]
    supports=[{'classes':[i,(i+1)%5],'common_blue':(i+1)%5,'common_red_edge':[(i+3)%5,(i+4)%5]} for i in range(5)]
    rows=[]
    for i in range(5):
        a=[0]*5;a[i]=a[(i+1)%5]=1;rows.append({'a':a,'rhs':8})
    rows.append({'a':[-1]*5,'rhs':-22})
    cert={'schema':1,'profile':[19]*2+[20]*5+[21]*36,'core_order':20,
          'core_red_edges':[[u,v] for u,v in combinations(range(20),2) if red(u,v)],
          'free_physical_pairs_before_degrees':713,'bag_status_masks':tables,
          'status_words_checked':256,'feasible_positive_words':words,'admissible_stars':len(stars),
          'star_set_sha256':hashlib.sha256(''.join(f'{m}\n' for m in sorted(stars)).encode()).hexdigest(),
          'edge_classes':edges,'class_pair_supports':supports,'outside_order':23,
          'end_bag_core_degree':7,'bag_degree_sum_cap':105,'blue_incidence_minimum':45,
          'ordinary_star_minimum':22,'small_ramsey_threshold':9,
          'farkas_rows':rows,'farkas_multipliers':[1,1,1,1,1,2],'farkas_rhs':-4}
    return cert,stars

if __name__=='__main__':print(json.dumps(produce()[0],indent=2))
