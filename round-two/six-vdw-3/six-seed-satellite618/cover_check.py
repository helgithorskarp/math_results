#!/usr/bin/env python3
"""Independent exact coverage and consequence of adjacent five-seed rules.

The two-satellite input theorem is an explicit mathematical dependency,
graph9311/sourceb18c33b5, rather than a fresh proof in this program.
"""
import argparse
import itertools
import json
from pathlib import Path


def need(condition,message):
    if not condition:
        raise ValueError(message)


def cover():
    q=103
    holes={6,54,102}
    seed=set(range(6))
    satellites=(7,52,53,55,56,101)
    left={101,52,53,55}
    right={7,53,55,56}
    domain=tuple(sorted(seed|set(satellites)))
    # These are two of the four fully density-two-covered geometries in9311.
    proved_geometries={(5,53,101),(5,53,102),(5,54,102),(6,54,102)}
    for start in (0,1):
        normalized=tuple(sorted((x-start)%q for x in holes))
        need(normalized in proved_geometries,'Cited five-seed theorem does not apply')
    five_seeds=(set(range(5)),set(range(1,6)))
    five_cores=(seed|left,seed|right)
    def older(word):
        return all(len({word[x] for x in core})>1 for core in five_cores)
    def two(word):
        for s,core in zip(five_seeds,five_cores):
            values={word[x] for x in s}
            if len(values)==1:
                color=next(iter(values))
                if sum(word[x]!=color for x in core-s)<2:
                    return False
        return True
    def three(word):
        if not two(word):
            return False
        values={word[x] for x in seed}
        if len(values)==1:
            color=next(iter(values))
            if sum(word[x]!=color for x in satellites)<3:
                return False
        return True
    counts=[0,0,0]
    removed=[]
    for bits in itertools.product((0,1),repeat=12):
        word=dict(zip(domain,bits))
        a,b,c=older(word),two(word),three(word)
        need(not c or b,'New consequence lost its five-seed premise')
        need(not b or a,'Two-satellite rules do not imply older mixed cuts')
        for j,value in enumerate((a,b,c)):counts[j]+=value
        if b and not c:removed.append(''.join(map(str,bits)))
    need(counts==[4082,4022,4020] and len(removed)==2,'Joint word filter changed')
    surviving=[]
    sparse=[]
    histogram={str(j):0 for j in range(7)}
    for bits in itertools.product((0,1),repeat=6):
        word={x:0 for x in seed}
        word.update(zip(satellites,bits))
        direct=two(word)
        independent=sum(word[x] for x in left)>=2 and sum(word[x] for x in right)>=2
        need(direct==independent,'Adjacent five-seed translation mismatch')
        if direct:
            surviving.append(bits)
            histogram[str(sum(bits))]+=1
            if sum(bits)==2:sparse.append(bits)
    need(len(surviving)==16+18+1==35,'Two-four-set exact count changed')
    need(histogram=={'0':0,'1':0,'2':1,'3':12,'4':15,'5':6,'6':1},
         'Opposite-weight distribution changed')
    need(len(sparse)==1,'Sparse counterexample cover is not complete')
    positives=tuple(x for x,b in zip(satellites,sparse[0]) if b)
    need(positives==(53,55) and set(positives)==left&right,'Unique weight-two word changed')
    word={x:0 for x in seed}
    word.update(zip(satellites,sparse[0]))
    reflected=sorted(((4-x)%q,b) for x,b in word.items())
    need(tuple(sorted((4-x)%q for x in holes))==(5,53,101),'Reflected hole shape changed')
    need(reflected==[(x,int(x in (52,54))) for x in (0,1,2,3,4,6,51,52,54,55,100,102)],
         'Independent reflected signed word changed')
    stabilizer=[]
    for a in range(1,q):
        for b in range(q):
            if {(a*x+b)%q for x in seed}==seed and {(a*x+b)%q for x in holes}==holes:
                stabilizer.append((a,b))
    need(stabilizer==[(1,0),(102,5)],'Matched seed-hole affine stabilizer changed')
    crt=[(1,102,1,102),(205,210,102,4),(205,108,102,5)]
    for A,B,a,b in crt:
        need(len({(A*t+B)%618 for t in range(618)})==618,'CRT map is not invertible')
        need(all((A*t+B)%6==t%6 and (A*t+B)%103==(a*t+b)%103 for t in range(618)),
             'CRT map does not preserve phase and field action')
    def orbits(words):
        classes=set()
        fixed=0
        for bits in words:
            values=dict(zip(satellites,bits))
            image=tuple(values[(5-x)%q] for x in satellites)
            need(image in words,'Input reflection lost a covered word')
            classes.add(min(bits,image))
            fixed+=image==bits
        return len(classes),fixed
    oldclasses,oldfixed=orbits(surviving)
    newwords=[bits for bits in surviving if sum(bits)>=3]
    newclasses,newfixed=orbits(newwords)
    need((oldclasses,oldfixed,newclasses,newfixed)==(20,5,19,4),'Reflection consequence changed')
    return {'dependency':{'height':9311,
                         'reference':'bafkreiadzldf6d5p3gng3khhmd3ul72bnntyzhxvysmj3owig7sabv3s6y',
                         'source_commit':'b18c33b5f51ce2c6b9c9bdb092cbdb5871b09b78'},
            'q':q,'modulus':618,'holes':sorted(holes),'monochromatic_six_seed':sorted(seed),
            'six_satellites':list(satellites),'required_two_satellite_sets':[sorted(left),sorted(right)],
            'joint_twelve_point_inputs':4096,'older_mixed_filter_accepts':counts[0],
            'published_two_satellite_filter_accepts':counts[1],
            'three_satellite_filter_accepts_after_new_refutation':counts[2],
            'new_joint_inputs_removed':removed,'six_satellite_inputs':64,
            'published_rules_necessary_inputs':len(surviving),'published_rules_weight_histogram':histogram,
            'unique_remaining_at_most_two_input':{'opposite_satellites':list(positives),
                'reflected_holes':[5,53,101],'reflected_fixed_core_bits':[list(x) for x in reflected]},
            'necessary_six_satellite_inputs_after_new_refutation':len(newwords),
            'old_input_reflection_classes':oldclasses,'new_input_reflection_classes':newclasses,
            'old_reflection_fixed_inputs':oldfixed,'new_reflection_fixed_inputs':newfixed,
            'seed_hole_affine_stabilizer':[list(x) for x in stabilizer],
            'affine_parameters_checked':10506,'CRT_point_identities_checked':1854,
            'other_regular_bits_free':88,'reflection_invariance_imposed':False,
            'number_of_sparse_negative_inputs':1,'counts_are_necessary_inputs_only':True,
            'admissible_global_colorings_counted':False,'W_bound_improved':False}


def manifest_guard(path):
    expected=json.loads(path.read_text())
    actual=cover()
    need(expected['cover']==actual,'Frozen negative coverage or consequence changed')
    need(expected['number_of_sparse_negative_inputs']==1,'Incomplete declared sparse family')
    bits=actual['unique_remaining_at_most_two_input']['reflected_fixed_core_bits']
    need(expected['model']['fixed_core_bits']==bits and expected['model']['other_regular_bits_free']==88,
         'Frozen model does not match the unique necessary input')
    return actual


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path)
    args=parser.parse_args()
    print(json.dumps(manifest_guard(args.expected) if args.expected else cover()))
