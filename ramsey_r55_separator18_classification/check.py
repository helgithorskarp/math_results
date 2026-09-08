#!/usr/bin/env python3
"""Independent complete marked-extension enumeration; imports no producer."""
import hashlib
import json
from itertools import combinations, permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def masks(n,k):
    return [sum(1<<v for v in q) for q in combinations(range(n),k)]

def independent(a,m):
    return all(not (a[v]&m) for v in range(len(a)) if m>>v&1)

def encode(a):
    return sum((a[v]>>u&1)<<i for i,(u,v) in enumerate(combinations(range(len(a)),2)))

def decode(n,code):
    a=[0]*n
    for i,(u,v) in enumerate(combinations(range(n),2)):
        if code>>i&1:
            a[u]|=1<<v
            a[v]|=1<<u
    return a

def enumerate_eight():
    # Every labeled valid graph is reached exactly once by deleting its last vertex.
    frontier=[[]]
    counts=[]
    for n in range(8):
        nxt=[]
        for a in frontier:
            forbidden=[m for m in masks(n,3) if independent(a,m)]
            for m in range(1<<n):
                if not independent(a,m) or any(not(m&t) for t in forbidden):
                    continue
                nxt.append([a[v]|((1<<n) if m>>v&1 else 0) for v in range(n)]+[m])
        frontier=nxt
        counts.append(len(frontier))
    unseen={encode(a) for a in frontier}
    need(len(unseen)==len(frontier),'duplicate labeled graph')
    all_codes=sorted(unseen)
    reps=[]
    while unseen:
        code=min(unseen)
        a=decode(8,code)
        orbit=set()
        for p in permutations(range(8)):
            orbit.add(sum((a[p[v]]>>p[u]&1)<<i for i,(u,v) in enumerate(combinations(range(8),2))))
        need(orbit<=unseen,'missing/overlapping full vertex-permutation orbit')
        unseen-=orbit
        reps.append((code,len(orbit)))
    digest=hashlib.sha256(('\n'.join(map(str,all_codes))+'\n').encode()).hexdigest()
    return counts,reps,digest

def literal_check(a):
    # Different, dense definition-level check of every emitted physical graph.
    matrix=[[bool(a[u]>>v&1) for v in range(12)] for u in range(12)]
    need(not any(all(matrix[u][v] for u,v in combinations(q,2)) for q in combinations(range(12),3)), 'emitted triangle')
    need(not any(all(not matrix[u][v] for u,v in combinations(q,2)) for q in combinations(range(12),5)), 'emitted independent5')
    fours=[set(q) for q in combinations(range(12),4) if all(not matrix[u][v] for u,v in combinations(q,2))]
    special=[sorted(q) for q in fours if all(q&t for t in fours)]
    need(special==[[8,9,10,11]],'unique marked independent four failed')

def extensions(reps):
    records=[]
    outputs={}
    for code,orbit_size in reps:
        a=decode(8,code)
        stars=[m for m in range(256) if independent(a,m)]
        triples=[m for m in masks(8,3) if independent(a,m)]
        pairs=[m for m in masks(8,2) if independent(a,m)]
        compatible=[[all((x|y)&t for t in triples) for y in stars] for x in stars]
        out=set()
        pairs_count=triples_count=0
        for i,x in enumerate(stars):
            for j,y in enumerate(stars):
                if not compatible[i][j]:
                    continue
                pairs_count+=1
                for k,z in enumerate(stars):
                    if not compatible[i][k] or not compatible[j][k]:
                        continue
                    if any(not((x|y|z)&t) for t in pairs):
                        continue
                    triples_count+=1
                    for l,w in enumerate(stars):
                        if not compatible[i][l] or not compatible[j][l] or not compatible[k][l] or (x|y|z|w)!=255:
                            continue
                        if any(not((u|v|w)&t) for u,v in ((x,y),(x,z),(y,z)) for t in pairs):
                            continue
                        b=a[:]+[x,y,z,w]
                        for v in range(8):
                            for h,s in enumerate((x,y,z,w)):
                                if s>>v&1:
                                    b[v]|=1<<(8+h)
                        literal_check(b)
                        c=encode(b)
                        need(c not in out,'duplicate ordered marked extension')
                        out.add(c)
        outputs[code]=out
        records.append({'core_code':code,'labeled_orbit_size':orbit_size,'independent_stars':len(stars),'ordered_pair_prefixes':pairs_count,'ordered_triple_prefixes':triples_count,'ordered_extensions':len(out),'extension_codes':sorted(out)})
    return records,outputs

def parse_catalog():
    # Dense graph6 decoder; no producer import or bitstring decoder.
    raw=(HERE/'r35_12.g6').read_bytes()
    parsed=[]
    for line in raw.splitlines():
        need(len(line)==12 and line[0]==75,'catalog line shape')
        values=[x-63 for x in line[1:]]
        need(all(0<=v<64 for v in values),'catalog alphabet')
        matrix=[[0]*12 for _ in range(12)]
        k=0
        for v in range(12):
            for u in range(v):
                bit=values[k//6]>>(5-k%6)&1
                matrix[u][v]=matrix[v][u]=bit
                k+=1
        parsed.append(matrix)
    need(len(parsed)==12,'catalog entry count')
    return raw,parsed

def catalog_audit(certificate,outputs):
    raw,graphs=parse_catalog()
    rows=[]
    transported={code:set() for code in outputs}
    for index,a in enumerate(graphs):
        need(not any(all(a[u][v] for u,v in combinations(q,2)) for q in combinations(range(12),3)),'catalog triangle')
        need(not any(all(not a[u][v] for u,v in combinations(q,2)) for q in combinations(range(12),5)),'catalog independent5')
        fours=[q for q in combinations(range(12),4) if all(not a[u][v] for u,v in combinations(q,2))]
        special=[]
        # All 4096 physical contact words, rather than the producer's intersecting-family test.
        for word in range(4096):
            red=[v for v in range(12) if word>>v&1]
            blue=[v for v in range(12) if not(word>>v&1)]
            if len(red)!=8 or any(a[u][v] for u,v in combinations(blue,2)):
                continue
            if any(all(not a[u][v] for u,v in combinations(q,2)) for q in combinations(red,4)):
                continue
            special.append(blue)
        rows.append({'index':index,'code':sum(a[u][v]<<i for i,(u,v) in enumerate(combinations(range(12),2))),'independent_fours':len(fours),'special_fours':sorted(special)})
        for q in special:
            remainder=[v for v in range(12) if v not in q]
            matched=False
            for p in permutations(remainder):
                core=sum(a[p[u]][p[v]]<<i for i,(u,v) in enumerate(combinations(range(8),2)))
                if core not in outputs:
                    continue
                matched=True
                for tail in permutations(q):
                    order=p+tail
                    transported[core].add(sum(a[order[u]][order[v]]<<i for i,(u,v) in enumerate(combinations(range(12),2))))
            need(matched,'catalog core absent from independently exhaustive classification')
    need(certificate['catalog_crosscheck']=={'sha256':hashlib.sha256(raw).hexdigest(),'rows':rows},'catalog census mismatch')
    need(transported==outputs,'entry-level marked-extension/census image mismatch')
    return sum(len(s) for s in transported.values())

def profiles():
    types=[(a,alpha) for a in range(1,25) for alpha,cap in ((1,4),(2,13),(3,24)) if alpha<=a<=cap]
    rows=[]
    for k in range(19):
        found=[]
        def visit(start,remain,budget,chosen):
            if remain==0:
                if len(chosen)>=2:
                    found.append(tuple(chosen))
                return
            for j in range(start,len(types)):
                a,alpha=types[j]
                if a>remain or alpha>budget or a+k<19:
                    continue
                visit(j,remain-a,budget-alpha,chosen+[(a,alpha)])
        visit(0,43-k,4,[])
        for seq in sorted(found):
            row={'separator_size':k,'component_types':[list(x) for x in seq]}
            clique=next((a for a,alpha in seq if a>1 and alpha==1),None)
            if clique is not None:
                missed=k-(18-(clique-1))
                lower=k-clique*missed
                upper={2:13,3:4,4:0}[clique]
                need(lower>upper,'clique contradiction failed')
                row.update(reason='clique_common_neighborhood',a=clique,lower=lower,upper=upper)
            elif seq==((13,2),(13,2)):
                need(k==17,'13+13 boundary')
                row.update(reason='two_thirteen_components')
            elif seq==((12,2),(13,2)):
                need(k==18,'12+13 boundary')
                row.update(reason='unique_twelve_attachment')
            elif seq==((1,1),(24,3)):
                need(k==18,'singleton boundary')
                row.update(reason='allowed_singleton_boundary')
            else:
                raise ValueError(('uncovered',k,seq))
            rows.append(row)
    return rows

def validate(certificate,outputs):
    need(certificate['schema']=='separator18-v1','certificate schema')
    need(certificate['claim']=='Every separator of size at most18 in good43 has size18 and components1,24; it is the neighborhood of its isolated degree18 vertex.','unsupported claim')
    need(certificate['component_profiles']==profiles(),'component-profile coverage')
    return catalog_audit(certificate,outputs)

def main():
    import copy
    c=json.loads((HERE/'CERTIFICATE.json').read_text())
    counts,reps,digest=enumerate_eight()
    records,outputs=extensions(reps)
    images=validate(c,outputs)
    # Cheap structural corruptions are checked before the full catalog transport.
    bad=[]
    x=copy.deepcopy(c);x['schema']='separator19-v1';bad.append(x)
    x=copy.deepcopy(c);x['component_profiles'].pop();bad.append(x)
    x=copy.deepcopy(c);x['component_profiles'][0]['lower']-=1;bad.append(x)
    x=copy.deepcopy(c);x['catalog_crosscheck']['rows'][2]['special_fours'].append([4,5,6,7]);bad.append(x)
    for x in bad:
        try:
            validate(x,outputs)
        except ValueError:
            continue
        raise ValueError('accepted a corrupted certificate')
    result={'status':'VERIFIED_SEPARATOR18_COMPLETE_CLASSIFICATION','labeled_R34_counts_n1_to_n8':counts,'labeled_R34_8_codes_sha256':digest,'complete_marked_extension_classes':records,'physical_catalog_transport_images':images,'catalog_contact_words_checked':12*4096,'component_profiles':len(profiles()),'excluded_profiles':sum(r['reason']!='allowed_singleton_boundary' for r in profiles()),'rejected_certificate_mutations':len(bad),'catalog_completeness_required':False,'good43_found':False,'target_solver_calls':0}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
