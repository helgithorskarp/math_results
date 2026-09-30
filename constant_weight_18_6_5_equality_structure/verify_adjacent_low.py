#!/usr/bin/env python3
"""Separate replay via all normalized relative affine planes and XOR distances."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import permutations,product
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
U,V,A,B=17,0,16,5
H=tuple(x for x in range(18) if x not in (U,V,B))
AXES=(sum(1<<x for x in (0,1,2,3)),sum(1<<x for x in (0,4,8,12)))
MULT=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
SQUARE=(0,1,3,2)

def require(condition,message):
    if not condition: raise ValueError(message)

def encoded(value):
    return (json.dumps(value,separators=(',',':'),sort_keys=True)+'\n').encode('ascii')

def decode(mask):
    return tuple(i for i in range(18) if mask>>i&1)

def masks(vertices,k):
    """Gosper successors on compact coordinates, lifted to the actual labels."""
    n=len(vertices); value=(1<<k)-1
    while value<1<<n:
        yield sum(1<<vertices[i] for i in range(n) if value>>i&1)
        low=value&-value; next_value=value+low
        value=next_value | (((next_value^value)//low)>>2)

def a4_plane():
    even=[p for p in permutations(range(4))
          if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]
    lines=[sum(1<<(4*x+p[x]) for x in range(4)) for p in even]
    lines += [sum(1<<(4*x+y) for y in range(4)) for x in range(4)]
    lines += [sum(1<<(4*x+y) for x in range(4)) for y in range(4)]
    pair_counts=Counter((x,y) for q in lines for x in decode(q) for y in decode(q) if x<y)
    require(len(set(lines))==20 and len(pair_counts)==120 and set(pair_counts.values())=={1},'invalid permutation plane')
    return sorted(lines)

def check_star(words,center):
    require(len(words)==len(set(words))==20,'star count/distinctness')
    require(all(w.bit_count()==5 and w>>center&1 for w in words),'word weight/center')
    require(all((x^y).bit_count()>=6 for i,x in enumerate(words) for y in words[i+1:]),'star distance')

def root_star(lines):
    words=[(q^1 | 1<<A | 1<<U) if q&1 and q not in AXES else q | 1<<U for q in lines]
    check_star(words,U)
    return words

def automorphism_coverage(lines):
    # Check the four-element arithmetic and every actual line image.
    require(all(MULT[x][y]==MULT[y][x] and MULT[x][MULT[y][z]]==MULT[MULT[x][y]][z]
                and MULT[x][y^z]==MULT[x][y]^MULT[x][z]
                for x in range(4) for y in range(4) for z in range(4)),'field table laws')
    groups=sorted(decode(q^1) for q in lines if q&1)
    group_masks=[sum(1<<x for x in g) for g in groups]
    maps=set(); induced=Counter(); kernels=[]; matrices=0
    for a,b,c,d in product(range(4),repeat=4):
        if MULT[a][d]^MULT[b][c]==0: continue
        matrices+=1
        for e in range(2):
            mapping=[]
            for x,y in product(range(4),repeat=2):
                if e: x,y=SQUARE[x],SQUARE[y]
                mapping.append(4*(MULT[a][x]^MULT[b][y])+(MULT[c][x]^MULT[d][y]))
            mapping=tuple(mapping)
            require(mapping[0]==0 and len(set(mapping))==16,'nonbijective semilinear map')
            images={sum(1<<mapping[x] for x in decode(q)) for q in lines}
            require(images==set(lines),'semilinear map does not preserve all lines')
            action=tuple(group_masks.index(sum(1<<mapping[x] for x in g)) for g in groups)
            maps.add(mapping); induced[action]+=1
            if action==tuple(range(5)): kernels.append(mapping)
    require(matrices==180 and len(maps)==360,'semilinear group coverage')
    require(set(induced)==set(permutations(range(5))) and set(induced.values())=={3},'directions do not have the full S5 action')
    require(len(kernels)==3 and {m[groups[0][0]] for m in kernels}==set(groups[0]),'direction kernel is not point-transitive')
    return {'invertible_matrices':matrices,'semilinear_maps':len(maps),
            'direction_permutations':len(induced),'direction_kernel':len(kernels)}

def partitions(remaining,triples):
    if not remaining:
        yield ()
        return
    first=remaining&-remaining
    for triple in triples:
        if triple&first and triple&remaining==triple:
            for suffix in partitions(remaining^triple,triples):
                yield (triple,)+suffix

def replay():
    lines=a4_plane(); star=root_star(lines)
    groups=sorted(decode(q^1) for q in lines if q&1)
    ordinary=[decode(q) for q in lines if not q&1]
    covered=tuple(x for x in range(18) if x not in (U,V,B,1,2,3,4,8,12))
    triples=[q for q in masks(covered,3) if all(((q|1<<V|1<<B)^w).bit_count()>=6 for w in star)]
    parts=sorted(tuple(sorted(decode(q) for q in part))
                 for part in partitions(sum(1<<x for x in covered),triples))
    require(len(parts)==len(set(parts)),'duplicate origin partitions')
    field_actions=automorphism_coverage(lines)
    quads=list(masks(H,4)); planes={}; cases=[]; normalization_stream=sha256()
    for i,part in enumerate(parts):
        start=time.monotonic()
        targets=[decode(q^1) for q in sorted(AXES)]+list(part)
        # Canonical order agrees with the mathematical fixed two-axis assignment.
        targets[:2]=sorted(targets[:2])
        assignments=[[(targets[0][0],)+p for p in permutations(targets[0][1:])]]
        assignments += [list(permutations(g)) for g in targets[1:]]
        fixed=[w for w in star if w>>V&1]+[sum(1<<x for x in q)|1<<V|1<<B for q in part]
        found=[]; seen=set(); enumerated=0
        for assignment in product(*assignments):
            enumerated+=1
            if enumerated%128==0 and time.monotonic()-start>10:
                raise RuntimeError('INCOMPLETE: relative-plane case cap reached; no exclusion')
            mapping={x:y for source,dest in zip(groups,assignment) for x,y in zip(source,dest)}
            image=tuple(sorted(tuple(sorted(mapping[x] for x in q)) for q in ordinary))
            require(image not in seen,'duplicate normalized field plane')
            seen.add(image); normalization_stream.update(encoded(image))
            other=[sum(1<<x for x in q)|1<<V for q in image]
            if not all((word^w).bit_count()>=6 for word in other for w in star): continue
            vstar=fixed+other
            check_star(vstar,V)
            union=sorted(set(star+vstar))
            require(len(union)==38 and sum(w>>B&1 for w in union)==8,'wrong mandatory anchor blocks')
            bcols=sorted(decode(q) for q in quads
                         if all(((q|1<<B)^w).bit_count()>=6 for w in union))
            neighbors={x:0 for x in H}
            for q in bcols:
                mask=sum(1<<x for x in q)
                for x in q: neighbors[x]|=mask^(1<<x)
            degrees=[neighbors[x].bit_count() for x in H]
            caps=[d//3 for d in degrees]
            bound=sum(caps)//4
            require(bound<=11,'anchor bound does not exclude saturation')
            found.append({'nonorigin_quads':[list(q) for q in image],
                          'anchor_candidates':len(bcols),
                          'anchor_candidate_sha256':sha256(encoded(bcols)).hexdigest(),
                          'pair_union_edges':sum(degrees)//2,
                          'pair_union_degrees':degrees,'point_capacities':caps,
                          'upper_bound':bound})
            require(image not in planes,'second-star duplication')
            planes[image]=tuple(bcols)
        require(enumerated==2592,'incomplete normalized plane coverage')
        cases.append({'index':i,'partition':[list(q) for q in part],
                      'normalized_planes':enumerated,
                      'compatible_second_stars':sorted(found,key=lambda z:z['nonorigin_quads'])})
    compact_cases=[{'index':c['index'],'partition':c['partition'],
                    'normalized_planes':c['normalized_planes'],
                    'compatible_second_stars':len(c['compatible_second_stars']),
                    'compatible_second_stars_sha256':sha256(encoded(c['compatible_second_stars'])).hexdigest()}
                   for c in cases]
    report={'automorphism_coverage':field_actions,'compatible_triples':len(triples),
            'compatible_origin_partitions':len(parts),'normalized_planes_enumerated':sum(c['normalized_planes'] for c in cases),
            'normalized_plane_stream_sha256':normalization_stream.hexdigest(),
            'compatible_second_stars':len(planes),'cases':compact_cases,
            'anchor_extra_words_upper_bound':11,'required_extra_words_for_saturation':12,
            'independent_peer_review':False,'global_72_word_exclusion':False}
    return report,planes,star,parts,cases

def compare_primary(planes,star,parts):
    import check_adjacent_low as primary
    report,other=primary.data()
    require(planes==other,'full second-star or anchor-column entries differ')
    pstar,_,pcases=primary.instances()
    require(set(star)=={sum(1<<x for x in w) for w in pstar},'first-star entries differ')
    Hquads=list(masks(H,4))
    for part,case in zip(parts,pcases):
        require(part==case['partition'],'origin partition entries differ')
        fixed=[w for w in star if w>>V&1]+[sum(1<<x for x in q)|1<<V|1<<B for q in part]
        rows={(x,y) for j,x in enumerate(H) for y in H[j+1:]
              if not any(w>>x&1 and w>>y&1 for w in fixed)}
        columns=sorted(decode(q) for q in Hquads
                       if all(((q|1<<V)^w).bit_count()>=6 for w in star)
                       and all(((q|1<<V)^w).bit_count()>=6 for w in fixed))
        require(rows==set(case['rows']) and columns==case['columns'],'every initial row/column differs')
    require(len(pcases)==len(parts) and report['compatible_second_stars']==len(planes),'coverage counts differ')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--compare-primary',action='store_true')
    args=parser.parse_args()
    report,planes,star,parts,details=replay()
    if args.compare_primary: compare_primary(planes,star,parts)
    path=HERE/'adjacent_low_expected.json'
    expected=json.loads(path.read_text())
    require(len(details)==len(expected['primary']['cases']),'manifest case coverage differs')
    for actual,prior in zip(details,expected['primary']['cases']):
        require(actual['index']==prior['index'] and actual['partition']==prior['partition']
                and actual['compatible_second_stars']==prior['compatible_second_stars'],
                'every second-plane/capacity record differs from the manifest')
    if args.write_expected:
        expected['replay']=report
        path.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        require(expected['replay']==report,'separate replay manifest differs')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__': main()
