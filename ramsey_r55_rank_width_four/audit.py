"""Finite proof checks; these are not an enumeration of all good43 graphs."""
from collections import Counter
from itertools import combinations, permutations, product
from math import comb
import json


def require(ok, why):
    if not ok:
        raise ValueError(why)


def dot(x, y):
    return sum(((x >> j) & 1)*((y >> j) & 1) for j in range(3)) % 2


def main():
    out = {}
    partitions = Counter()
    for p, q, r in permutations(range(1, 8), 3):
        cells = [set(y for y in range(8) if dot(u,y)==1 and dot(v,y)==0)
                 for u,v in [(p,q),(q,r),(r,p)]]
        require(all(len(c)==2 for c in cells), 'two labels per contact cell')
        require(all(not (u & v) for u,v in combinations(cells,2)), 'disjoint cells')
        remainder = set(range(8))-set.union(*cells)
        require(len(remainder)==2 and 0 in remainder, 'zero and one nonzero remainder')
        kind = 'rank_two' if p ^ q ^ r == 0 else 'rank_three'
        image = {tuple(dot(x,y) for x in (p,q,r)) for y in range(8)}
        require(len(image)==(4 if kind=='rank_two' else 8), 'independent label rank')
        partitions[kind] += 1
    out['ordered_three_label_partitions'] = dict(partitions)
    pairs = 0
    for p,q in permutations(range(1,8),2):
        require(sum(dot(p,y)==dot(q,y)==1 for y in range(8))==2, 'common red labels')
        pairs += 1
    out['ordered_pair_intersections'] = pairs
    require(all(sum(dot(x,y)==0 for y in range(1,8))==3 for x in range(1,8)),
            'three nonzero blue labels')

    # Definition-level R(3,3) check on every graph of order six.
    edges = list(combinations(range(6),2))
    edge_index = {e:i for i,e in enumerate(edges)}
    tri = [[edge_index[e] for e in combinations(q,2)] for q in combinations(range(6),3)]
    for word in range(1 << len(edges)):
        require(any(len({(word >> e)&1 for e in t})==1 for t in tri), 'R33 control')
    out['six_vertex_graphs'] = 32768

    # All internal graphs of a five-class, with literal distinguishers.
    e5=list(combinations(range(5),2)); index5={e:i for i,e in enumerate(e5)}
    maxima=0
    for word in range(1024):
        count=0
        for q in combinations(range(5),3):
            for v in range(5):
                if v not in q:
                    values={(word >> index5[tuple(sorted((u,v)))])&1 for u in q}
                    count += len(values)==2
        maxima=max(maxima,count)
        require(count<=20,'internal five-class capacity')
    outside=[sum(len({(s>>v)&1 for v in q})==2 for q in combinations(range(5),3))
             for s in range(32)]
    require(maxima==20 and max(outside)==9 and outside[0]==outside[-1]==0,
            'five-class equality values')
    out['five_class_graphs']=1024
    out['outside_five_signatures']=32
    out['five_class_capacity']={'internal':maxima,'outside':max(outside)}

    # Complete integer occupancy controls, including the exceptional blue triple.
    counts=Counter()
    for nonzero in product(range(5),repeat=7):
        for z in (0,1):
            a=z+sum(nonzero)
            if a not in (20,21):
                continue
            large=[i for i,s in enumerate(nonzero) if s>=3]
            require(len(large)>=3,'three mixed classes without an exception')
            counts[str(a)+'_no_exception']+=1
            if a==21:
                for i in large:
                    if nonzero[i]==3:
                        require(len(large)-1>=3,'three mixed classes with one exceptional triple')
                        counts['21_one_blue_triple']+=1
    out['complete_population_cases']=dict(counts)
    cases=[]
    for a,b,z in [(20,23,2),(21,22,1)]:
        require(20+9*(a-5)<170,'five-class contradiction')
        require(a<23,'A zero pair excluded')
        require((b<23 and z==1) or (b==23 and b<25 and z==2),'B zero cap')
        require(b-z-15==6>4,'red triangle impossible')
        possible_t=[t for t in range(5) if 54<=2*a+4+2*t]
        require(possible_t==([] if a==20 else [4]),'blue triangle cross count')
        if a==21:
            require(2*(b-4)-b>10,'two exceptional labels impossible')
        upper=15+5+z
        require(upper<b,'balanced global contradiction')
        cases.append({'a':a,'b':b,'B_zero_cap':z,'minimum_nonzero_red_contacts':6,
                      'possible_blue_triangle_contacts':possible_t,'B_upper_bound':upper})
    out['balanced_cases']=cases
    out['centroid_triples']=0
    for a in range(1,22):
        for b in range(1,22):
            c=43-a-b
            if 1<=c<=21:
                require(15<=max(a,b,c)<=21,'centroid large side')
                out['centroid_triples']+=1
    require(out['centroid_triples']==231,'centroid count')
    out['status']='BALANCED_RANK_THREE_CASES_EXCLUDED_AND_RANK_WIDTH_FOUR'
    return out


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,separators=(',',':')))
