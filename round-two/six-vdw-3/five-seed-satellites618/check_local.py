#!/usr/bin/env python3
"""Independent actual-cyclic projection and complete local ternary word audit."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def check(path):
    proposed=json.loads(path.read_text());q=103;length=618
    seed=set(range(5));satellites=(101,102,5,6,52,53,54,55)
    need(proposed['q']==q and proposed['seed']==sorted(seed) and proposed['satellite_order']==list(satellites),'Local domain altered')
    union=seed|set(satellites);terms=set();actual_pairs=0;all_pairs=0;carriers=set()
    # No algebraic ladder or path predicate is imported. Reconstruct blocked
    # point values from every actual cyclic tuple and both monochromatic colors.
    for step in range(1,length):
        for start in range(length):
            residues=tuple((start+j*step)%length for j in range(7));all_pairs+=1
            fields=tuple(t%q for t in residues)
            if not set(fields)<=union:continue
            actual_pairs+=1
            for color in (0,1):
                required={};consistent=True
                for t,x in zip(residues,fields):
                    bit=int(t%6>=3)^color
                    if (x in seed and bit!=0) or (x in required and required[x]!=bit):consistent=False;break
                    required[x]=bit
                if consistent:
                    term=tuple(sorted((x,bit) for x,bit in required.items() if x not in seed))
                    need(bool(term),'A seed-only forbidden AP escaped the proposal')
                    terms.add(term);carriers.add(tuple(x for x,_ in term))
    def good(word):
        values=dict(zip(satellites,word))
        return not any(all(values[x] is not None and values[x]==bit for x,bit in term) for term in terms)
    profiles=[];zero=[];accepted=inputs=0;word_records=[]
    for h in range(4):
        for holes in itertools.combinations(sorted(satellites),h):
            remaining=[x for x in satellites if x not in holes];weights=[0]*(len(remaining)+1)
            for bits in itertools.product((0,1),repeat=len(remaining)):
                values=dict(zip(remaining,bits));word=tuple(None if x in holes else values[x] for x in satellites)
                valid=good(word);inputs+=1;accepted+=int(valid)
                word_records.append(''.join('.' if x is None else str(x) for x in word)+':'+str(int(valid)))
                if valid:weights[sum(bits)]+=1
            minimum=next(i for i,n in enumerate(weights) if n)
            profiles.append({'holes':list(holes),'other_color_polynomial':weights,'accepted':sum(weights),'minimum_other_color':minimum})
            if minimum==0:zero.append(list(holes))
    lookup={tuple(p['holes']):p for p in proposed['profiles']}
    need(len(lookup)==len(profiles),'Profile domain mismatch')
    for p in profiles:
        old=lookup[tuple(p['holes'])]
        for key,value in p.items():need(old[key]==value,'Local literal profile mismatch: '+key)
        holes=set(p['holes'])
        for component,key in ((satellites[:4],'path_polynomial'),(satellites[4:],'triple_polynomial')):
            regular=[x for x in component if x not in holes]
            component_terms=[t for t in terms if {x for x,_ in t}<=set(component)]
            counts=[0]*(len(regular)+1)
            for bits in itertools.product((0,1),repeat=len(regular)):
                values=dict(zip(regular,bits))
                bad=any(not holes.intersection(x for x,_ in t) and all(values[x]==bit for x,bit in t) for t in component_terms)
                if not bad:counts[sum(bits)]+=1
            need(counts==old[key],'Literal component polynomial mismatch')
        pa=old['path_polynomial'];pb=old['triple_polynomial']
        convolved=[0]*(len(pa)+len(pb)-1)
        for i,x in enumerate(pa):
            for j,y in enumerate(pb):convolved[i+j]+=x*y
        need(convolved==p['other_color_polynomial'],'Product profile mismatch')
    need(zero==proposed['zero_other_color_hole_triples'],'Zero-other-color geography mismatch')
    reflected=lambda h:tuple(sorted((4-x)%q for x in h))
    classes=sorted({min(tuple(p['holes']),reflected(p['holes'])) for p in profiles})
    need(list(map(list,classes))==proposed['profile_classes'] and len(classes)==49,'Satellite quotient altered')
    zero_classes=sorted({min(tuple(h),reflected(h)) for h in zero})
    need(list(map(list,zero_classes))==proposed['zero_other_color_reflection_classes'] and len(zero_classes)==3,'Zero-growth cover narrowed')
    need((inputs,accepted)==(proposed['local_inputs'],proposed['local_accepted']),'Local coverage count mismatch')
    # Independent raw triple traversal; membership only in literal carriers.
    minimum_histogram={i:0 for i in range(4)};raw_zero=[];raw_owners=set();raw_count=0
    for holes in itertools.combinations([x for x in range(q) if x not in seed],3):
        local=tuple(x for x in holes if x in satellites)
        minimum=next(p['minimum_other_color'] for p in profiles if tuple(p['holes'])==local)
        minimum_histogram[minimum]+=1;raw_count+=1
        if minimum==0:raw_zero.append(list(holes))
        image=tuple(sorted((4-x)%q for x in holes));need(image!=holes,'Seed stabilizer unexpectedly fixes a three-hole set')
        raw_owners.add(min(holes,image))
    need(raw_count==proposed['raw_seed_disjoint_hole_triples']==math.comb(98,3),'Raw hole cover mismatch')
    need({str(k):v for k,v in minimum_histogram.items()}==proposed['raw_minimum_other_color_histogram'],'Raw minimum histogram mismatch')
    need(raw_zero==zero and len(raw_owners)==76048,'Seed-hole reflection cover mismatch')
    return {'agent':'six-vdw-3','role':'researcher','status':'LOCAL_CORE_LITERAL_AUDITED_NOT_GLOBAL_EXCLUSION',
            'all_actual_cyclic_pairs_checked':all_pairs,'pairs_supported_on_local_union':actual_pairs,
            'literal_forbidden_terms':len(terms),'literal_carriers':list(map(list,sorted(carriers))),
            'local_inputs':inputs,'local_accepted':accepted,'local_profiles':len(profiles),
            'local_reflection_classes':len(classes),'zero_other_color_reflection_classes':list(map(list,zero_classes)),
            'all_local_truth_sha256':hashlib.sha256(('\n'.join(word_records)+'\n').encode()).hexdigest(),
            'raw_hole_triples':raw_count,'raw_reflection_classes':len(raw_owners),
            'raw_minimum_other_color_histogram':minimum_histogram,
            'zero_other_color_holes':zero,'global_satellite_growth_proved':False,'W_bound_improved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('path',type=Path)
    a=p.parse_args();print(json.dumps(check(a.path)))
