#!/usr/bin/env python3
"""Check the complete necessary input cover independently by64 masks."""
import argparse
import itertools
import json
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def verify(path):
    proposed=json.loads(path.read_text())
    Q=(7,52,53,55,56,101);F={101,52,53,55};G={7,53,55,56}
    seed=set(range(6));holes={6,54,102}
    words=set()
    for mask in range(64):
        selected={Q[j] for j in range(6) if mask&(1<<j)}
        if len(selected)>=3 and len(selected&F)>=2 and len(selected&G)>=2:
            words.add(tuple(int(x in selected) for x in Q))
    classes={}
    for word in words:
        values=dict(zip(Q,word))
        image=tuple(values[(5-x)%103] for x in Q)
        need(image in words,'Actual reflection lost an input')
        classes.setdefault(min(word,image),set()).update((word,image))
    representatives=sorted(classes,key=lambda x:(sum(x),x))
    need(len(words)==34 and len(representatives)==19,'Necessary input count changed')
    need(len(proposed['cases'])==19 and proposed['necessary_raw_inputs']==34 and
         proposed['reflection_classes']==19,'Incomplete negative domain')
    need(proposed['holes']==sorted(holes) and proposed['monochromatic_seed']==sorted(seed) and
         proposed['satellites']==list(Q),'Seed/hole/satellite geometry changed')
    need([(x['height'],x['reference']) for x in proposed['mathematical_dependencies']]==[
         (9311,'bafkreiadzldf6d5p3gng3khhmd3ul72bnntyzhxvysmj3owig7sabv3s6y'),
         (9359,'bafkreif6ri5nsn5tquosbma5hny3myl4dhhg5iaobsamkfo6ayp6l3a3l4')],
         'Explicit mathematical premise changed')
    for number,(word,record) in enumerate(zip(representatives,proposed['cases']),1):
        fixed={x:0 for x in seed};fixed.update(zip(Q,word))
        need(record['number']==number and record['opposite_weight']==sum(word) and
             record['satellite_word']==''.join(map(str,word)),'Ordered representative changed')
        need(record['represented_raw_inputs']==[''.join(map(str,w)) for w in sorted(classes[word])],
             'Missing raw input orbit member')
        need(record['opposite_satellites']==[x for x,b in zip(Q,word) if b], 'Opposite point changed')
        need(record['fixed_original_core_bits']==[[x,fixed[x]] for x in sorted(fixed)] and
             record['reflected_to_E1_fixed_core_bits']==sorted([[(4-x)%103,b] for x,b in fixed.items()]),
             'Transported signed twelve-point word changed')
        need(record['other_regular_bits_free']==88 and not record['reflection_invariance_imposed'],
             'Unjustified outside symmetry or restricted domain')
    stabilizer=[(a,b) for a in range(1,103) for b in range(103)
                if {(a*x+b)%103 for x in seed}==seed and {(a*x+b)%103 for x in holes}==holes]
    need(stabilizer==[(1,0),(102,5)],'Matched seed-hole stabilizer changed')
    for A,B,a,b in ((1,102,1,102),(205,210,102,4),(205,108,102,5),(427,324,15,15)):
        need(len({(A*t+B)%618 for t in range(618)})==618,'Noninvertible CRT transport')
        need(all((A*t+B)%6==t%6 and (A*t+B)%103==(a*t+b)%103 for t in range(618)),
             'CRT transport changes phase or field action')
    need({(15*x+15)%103 for x in holes}=={0,1,2} and
         sorted((15*x+15)%103 for x in seed)==[15,30,45,60,75,90],
         'Harmonic-hole six-seed corollary transport failed')
    # Adjacent five-seed rules, followed by complete matched six-seed exclusion.
    domain=tuple(sorted(seed|set(Q)));old=two=final=0
    cores=(seed|F,seed|G);five=(set(range(5)),set(range(1,6)))
    for bits in itertools.product((0,1),repeat=12):
        values=dict(zip(domain,bits))
        mixed=all(len({values[x] for x in core})>1 for core in cores)
        density=True
        for s,core in zip(five,cores):
            colors={values[x] for x in s}
            if len(colors)==1 and sum(values[x]!=next(iter(colors)) for x in core-s)<2:
                density=False
        old+=mixed;two+=density
        final+=density and len({values[x] for x in seed})>1
    need((old,two,final)==(4082,4022,3952),'Necessary joint filter changed')
    return {'necessary_raw_inputs':34,'reflection_classes':19,
            'classes_by_weight':[6,9,3,1],'reflection_fixed_inputs':4,
            'complete_binary_inputs_checked':64,'affine_stabilizer_maps_checked':10506,
            'CRT_point_identities_checked':2472,'joint_inputs_checked':4096,
            'older_mixed_filter_accepts':old,'two_satellite_filter_accepts':two,
            'after_complete_six_seed_exclusion_filter_accepts':final,
            'harmonic_hole_six_seed':[15,30,45,60,75,90],
            'other_regular_bits_free_each':88,'orientation_invariance_imposed':False,
            'global_colorings_counted':False,'W_bound_improved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cover',type=Path,required=True)
    print(json.dumps(verify(p.parse_args().cover)))
