#!/usr/bin/env python3
"""Exact adjacent degree-two obstruction: enumerate second links, then bound an anchor."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
U,V,A,B = 17,0,16,5
AXES = {frozenset([0,1,2,3]),frozenset([0,4,8,12])}
H = tuple(sorted(set(range(18))-{U,V,B}))

def require(value, message):
    if not value:
        raise ValueError(message)

def encoded(value):
    return (json.dumps(value,separators=(',',':'),sort_keys=True)+'\n').encode('ascii')

def mul4(a,b):
    result=0
    while b:
        if b&1: result^=a
        a<<=1; b>>=1
        if a&4: a^=7
    return result

def field_plane():
    lines=[frozenset(4*x+(mul4(m,x)^c) for x in range(4))
           for m in range(4) for c in range(4)]
    lines += [frozenset(4*x+y for y in range(4)) for x in range(4)]
    counts=Counter(p for line in lines for p in combinations(sorted(line),2))
    require(len(set(lines))==20 and len(counts)==120 and set(counts.values())=={1},'invalid field plane')
    return lines

def first_star():
    result=[frozenset((q-{0})|{A,U}) if 0 in q and q not in AXES
            else frozenset(q|{U}) for q in field_plane()]
    validate_star(result,U)
    return result

def validate_star(words,center):
    require(len(words)==len(set(words))==20,'star size/distinctness')
    require(all(len(w)==5 and center in w for w in words),'star weights/center')
    require(all(len(x&y)<=2 for x,y in combinations(words,2)),'star repeated triple')

def triple_partitions(points):
    if not points:
        yield ()
        return
    first=points[0]
    for rest in combinations(points[1:],2):
        triple=(first,)+rest
        left=tuple(x for x in points if x not in triple)
        for suffix in triple_partitions(left):
            yield (triple,)+suffix

def instances():
    star=first_star()
    covered=tuple(sorted(set(range(18))-{U,V,B,1,2,3,4,8,12}))
    triples=[q for q in combinations(covered,3)
             if all(len((frozenset(q)|{V,B})&w)<=2 for w in star)]
    triple_set=set(triples)
    all_parts=list(triple_partitions(covered))
    parts=sorted(p for p in all_parts if set(p)<=triple_set)
    require(len(all_parts)==280 and len(set(all_parts))==280,'incomplete triple partitions')
    result=[]
    for part in parts:
        fixed=[w for w in star if V in w]+[frozenset(q)|{V,B} for q in part]
        groups=[w-{V,U,B} for w in fixed]
        require(len(fixed)==5 and set.union(*map(set,groups))==set(H)
                and sum(map(len,groups))==15,'wrong origin-line groups')
        rows=sorted(p for p in combinations(H,2) if not any(set(p)<=g for g in groups))
        row_set=set(rows)
        cols=[q for q in combinations(H,4) if set(combinations(q,2))<=row_set
              and all(len((frozenset(q)|{V})&w)<=2 for w in star)]
        require(len(rows)==90,'wrong second-plane pair universe')
        result.append({'partition':part,'fixed':fixed,'rows':rows,'columns':cols})
    return star,triples,result

def all_covers(rows,columns,node_cap=200000,seconds=10):
    """Yield every pair partition; no quotient or heuristic pruning."""
    index={p:i for i,p in enumerate(rows)}
    masks=[sum(1<<index[p] for p in combinations(q,2)) for q in columns]
    row_cols=[0]*len(rows)
    for i,mask in enumerate(masks):
        for j in range(len(rows)):
            if mask>>j&1: row_cols[j]|=1<<i
    conflicts=[]
    for mask in masks:
        blocked=0
        for j in range(len(rows)):
            if mask>>j&1: blocked|=row_cols[j]
        conflicts.append(blocked)
    start=time.monotonic(); nodes=0; answers=[]
    def visit(uncovered,active,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>node_cap or (nodes%128==0 and time.monotonic()-start>seconds):
            raise RuntimeError('INCOMPLETE: pair-cover cap reached; no exclusion')
        if not uncovered:
            answer=tuple(sorted(columns[i] for i in chosen))
            counts=Counter(p for q in answer for p in combinations(q,2))
            require(set(counts)==set(rows) and set(counts.values())<={1},'incorrect cover witness')
            answers.append(answer)
            return
        choices=[]; bits=uncovered
        while bits:
            bit=bits&-bits; j=bit.bit_length()-1
            opts=active&row_cols[j]
            if not opts: return
            choices.append((opts.bit_count(),j,opts)); bits^=bit
        _,_,options=min(choices)
        while options:
            bit=options&-options; i=bit.bit_length()-1
            require(masks[i]&uncovered==masks[i],'column covers an already used pair')
            visit(uncovered^masks[i],active&~conflicts[i],chosen+(i,))
            options^=bit
    visit((1<<len(rows))-1,(1<<len(columns))-1,())
    require(len(answers)==len(set(answers)),'duplicate exact covers')
    return sorted(answers),nodes

def anchor_columns(star,vstar):
    return [q for q in combinations(H,4)
            if all(len((frozenset(q)|{B})&w)<=2 for w in star+vstar)]

def capacity(columns,vertices):
    pairs=set(p for q in columns for p in combinations(q,2))
    degrees=[sum(x in p for p in pairs) for x in vertices]
    caps=[d//3 for d in degrees]
    return {'pair_union_edges':len(pairs),'pair_union_degrees':degrees,
            'point_capacities':caps,'upper_bound':sum(caps)//4}

def data():
    star,triples,cases=instances()
    output=[]; planes={}
    for i,case in enumerate(cases):
        covers,nodes=all_covers(case['rows'],case['columns'])
        details=[]
        for cover in covers:
            vstar=case['fixed']+[frozenset(q)|{V} for q in cover]
            validate_star(vstar,V)
            require(all(len(x&y)<=2 for x in star for y in vstar if x!=y),'incompatible stars')
            union=set(star+vstar)
            require(len(union)==38 and sum(B in w for w in union)==8,'wrong fixed anchor incidence')
            cols=anchor_columns(star,vstar)
            bound=capacity(cols,H)
            require(bound['upper_bound']<=11,'anchor capacity does not exclude replication twenty')
            plane={'nonorigin_quads':[list(q) for q in cover],
                   'anchor_candidates':len(cols),
                   'anchor_candidate_sha256':sha256(encoded(cols)).hexdigest(),**bound}
            details.append(plane)
            key=tuple(cover)
            require(key not in planes,'a plane belongs to two different origin partitions')
            planes[key]=tuple(cols)
        output.append({'index':i,'partition':[list(q) for q in case['partition']],
                       'rows':len(case['rows']),'columns':len(case['columns']),
                       'cover_nodes':nodes,'compatible_second_stars':details})
    report={'complete_triple_partitions':280,'compatible_triples':len(triples),
            'compatible_origin_partitions':len(cases),'cases':output,
            'compatible_second_stars':len(planes),'anchor_extra_words_upper_bound':11,
            'required_extra_words_for_saturation':12,
            'theorem_depends_on_computation':True,'global_72_word_exclusion':False}
    return report,planes

def controls():
    checked=0
    for n in range(6):
        pairs=tuple(combinations(range(n),2))
        for bits in range(1<<len(pairs)):
            rows=tuple(p for i,p in enumerate(pairs) if bits>>i&1)
            cols=[q for q in combinations(range(n),4) if set(combinations(q,2))<=set(rows)]
            brute=[]; packing_max=0
            for chosen in range(1<<len(cols)):
                words=[q for i,q in enumerate(cols) if chosen>>i&1]
                counter=Counter(p for q in words for p in combinations(q,2))
                if set(counter.values())<={1}:
                    packing_max=max(packing_max,len(words))
                    if set(counter)==set(rows): brute.append(tuple(words))
            actual,_=all_covers(rows,cols)
            require(set(actual)==set(brute),'small pair-cover mismatch')
            require(packing_max<=capacity(cols,range(n))['upper_bound'],'small capacity bound false')
            checked+=1
    lines=[tuple(sorted(q)) for q in field_plane()]
    covers,_=all_covers(tuple(combinations(range(16),2)),lines)
    require(covers==[tuple(sorted(lines))],'known positive affine plane rejected')
    # The ordinary six-third argument is checked in all ten labeled partitions.
    checked_conflicts=0
    for first in combinations(range(5),2):
        rest=set(range(5))-set(first)
        fixed=[frozenset({5,6,7}|set(first)),frozenset({5,6}|rest)]
        for tail in combinations(range(5),2):
            word=frozenset({5,7,8}|set(tail))
            require(any(len(word&q)>=3 for q in fixed),'six-third block conflict false')
            checked_conflicts+=1
    # Semantic controls: the mathematical validator, not an expected-output hash.
    good=first_star(); rejected=0
    for corrupted in ([good[0]]+good[:-1], [good[0]-{U}]+good[1:]):
        try: validate_star(corrupted,U)
        except ValueError: rejected+=1
    require(rejected==2,'corrupted star accepted')
    return {'simple_graphs_checked':checked,'six_third_conflicts_checked':checked_conflicts,
            'positive_affine_cover':True,'semantic_corruptions_rejected':rejected}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args()
    report,_=data(); report['controls']=controls()
    path=HERE/'adjacent_low_expected.json'
    if args.write_expected:
        expected=json.loads(path.read_text()) if path.exists() else {}
        expected['primary']=report
        path.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        require(json.loads(path.read_text())['primary']==report,'primary manifest differs')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__': main()
