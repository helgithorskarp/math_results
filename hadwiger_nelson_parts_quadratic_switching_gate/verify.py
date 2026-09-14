#!/usr/bin/env python3
"""Exact whole-support colouring retraction for quadratic Parts switching."""
import argparse
import base64
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
WEIGHTS=(1,3,5,15,11,33,55,165)
DEN=96

def require(condition, detail):
    if not condition:raise ValueError(detail)

def digest(data):return sha256(data).hexdigest()

def product(a,b):
    c=[0]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i^j]+=x*y*WEIGHTS[i&j]
    return c

def distance_squared(p,q):
    out=[0]*8
    for a,b in zip(p,q,strict=True):
        d=[x-y for x,y in zip(a,b,strict=True)]
        square=product(d,d)
        out=[x+y for x,y in zip(out,square,strict=True)]
    return tuple(out)

def conjugate(p):
    return tuple(tuple(-x if i&2 else x for i,x in enumerate(axis)) for axis in p)

def read_inputs():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for filename,h in manifest['inputs'].items():
        require(digest((REPO/filename).read_bytes())==h,('input hash',filename))
    points=[]
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        v=tuple(map(int,line.split()));require(len(v)==16,'coordinate width')
        points.append((v[:8],v[8:]))
    require(len(points)==509,'original count')
    cert=json.loads((REPO/'hadwiger_nelson_parts509_criticality/certificate.json').read_text())
    require(cert['vertices']==509 and cert['edges']==2442,'colouring domain')
    packed=base64.b64decode(cert['deletion_colorings_base64'],validate=True)
    require(digest(packed)==cert['packed_deletion_colorings_sha256'],'packed word hash')
    require(len(packed)==509*127,'packed word size')
    words=[]
    for missing in range(509):
        row=[]
        for vertex in range(509):
            if vertex==missing:row.append(-1);continue
            index=vertex-(vertex>missing)
            byte=packed[127*missing+index//4]
            row.append((byte>>(2*(index%4)))&3)
        words.append(row)
    five=list(map(int,cert['five_coloring']))
    require(len(five)==509 and set(five)<=set(range(5)),'five-word domain')
    return points,words,five

def check_word(labels,edges,colouring,palette):
    require(set(colouring)==set(labels),'word label domain')
    require(set(colouring.values())<=set(palette),'word palette')
    for a,b in edges:
        if a in colouring and b in colouring:
            require(colouring[a]!=colouring[b],('monochromatic edge',a,b))

def check_projection(host_edges,original_edges,projection):
    for a,b in host_edges:
        require(tuple(sorted((projection[a],projection[b]))) in original_edges,('projection failure',a,b))

def pull_back(keep,projection,words):
    require(isinstance(keep,list),'support must be a list')
    require(len(keep)==len(set(keep)) and all(type(v) is int and 0<=v<len(projection) for v in keep),'support domain')
    require(len(keep)<=508,'point cap')
    image={projection[v] for v in keep}
    missing=next(v for v in range(509) if v not in image)
    return missing,{v:words[missing][projection[v]] for v in keep}

def compute():
    points,words,five=read_inputs()
    require(len(set(points))==509,'original collision')
    require(all(conjugate(p)==p for p in points[:374]),'large block not fixed')
    require(all(conjugate(p)!=p for p in points[374:]),'small block fixed point')
    host=points+[conjugate(p) for p in points[374:]]
    projection=list(range(509))+list(range(374,509))
    require(len(set(host))==644,'unexpected image collision')
    target=(DEN*DEN,)+(0,)*7
    edges=[(a,b) for a,b in combinations(range(644),2) if distance_squared(host[a],host[b])==target]
    original={e for e in edges if e[1]<509}
    require(len(original)==2442 and len(edges)==3024,'edge counts')
    mixed=[e for e in edges if 374<=e[0]<509 and e[1]>=509]
    require(not mixed,'cross-sheet unit contact')
    check_projection(edges,original,projection)
    checks=0
    for missing,row in enumerate(words):
        labels=[v for v in range(509) if v!=missing]
        check_word(labels,original,{v:row[v] for v in labels},range(4))
        checks+=sum(missing not in e for e in original)
    check_word(list(range(644)),edges,{v:five[projection[v]] for v in range(644)},range(5))
    # One maximal fibre-deletion support for every missing label. Every
    # relevant smaller support is a restriction of one of these words.
    lifted_checks=0
    for missing,row in enumerate(words):
        labels=[v for v in range(644) if projection[v]!=missing]
        colouring={v:row[projection[v]] for v in labels}
        check_word(labels,edges,colouring,range(4))
        lifted_checks+=sum(projection[a]!=missing and projection[b]!=missing for a,b in edges)
    controls=0
    # Known unit fixture and involution/multiplication controls in the full basis.
    zero=(0,)*8;unit=(DEN,)+(0,)*7
    require(distance_squared((zero,zero),(unit,zero))==target,'unit fixture')
    for i in range(8):
        a=[0]*8;a[i]=1
        require(product(a,a)==[WEIGHTS[i]]+[0]*7,'basis square')
        require(conjugate(conjugate((tuple(a),zero)))==(tuple(a),zero),'involution')
        for j in range(8):
            b=[0]*8;b[j]=1
            left=conjugate((tuple(product(a,b)),zero))[0]
            right=tuple(product(conjugate((tuple(a),zero))[0],conjugate((tuple(b),zero))[0]))
            require(left==right,'automorphism product')
            controls+=1
    rejects=0
    try:check_projection(edges+[(374,509)],original,projection)
    except ValueError:rejects+=1
    else:raise ValueError('loop-producing mixed edge accepted')
    for bad in ([0,0],[-1],list(range(509))):
        try:pull_back(bad,projection,words)
        except ValueError:rejects+=1
        else:raise ValueError('malformed/cap-violating support accepted')
    fixtures=[[],list(range(508)),list(range(374))+list(range(509,643))]
    for missing in range(374,509):
        fixtures.append(list(range(374))+[v if v%2 else v+135 for v in range(374,509) if v!=missing])
    for keep in fixtures:
        _,colouring=pull_back(keep,projection,words);check_word(keep,edges,colouring,range(4))
    facts=dict(original_points=509,original_edges=2442,fixed_points=374,nonfixed_points=135,
               distinct_host_points=644,unit_edges=3024,complete_pair_checks=207046,
               mixed_pair_checks=18225,mixed_unit_edges=0,projection_failures=0,
               denominator=DEN,base_deletion_words=509,base_word_edge_checks=checks,
               maximal_fibre_deletion_words=509,lifted_word_edge_checks=lifted_checks,
               proper_host_five_colouring=True,all_at_most_508_subgraphs_four_colourable=True,
               record_candidate=False,corruptions_rejected=rejects,basis_product_controls=controls,
               support_fixtures=len(fixtures),
               point_sha256=digest(json.dumps(host,separators=(',',':')).encode()),
               edge_sha256=digest(''.join(f'{a},{b}\n' for a,b in edges).encode()),
               projection_sha256=digest(json.dumps(projection,separators=(',',':')).encode()))
    return facts,host,edges,projection,words

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--support',type=Path);ap.add_argument('--colouring-out',type=Path)
    ap.add_argument('--geometry-out',type=Path);args=ap.parse_args()
    require(bool(args.support)==bool(args.colouring_out),'support/output pairing')
    facts,host,edges,projection,words=compute()
    expected=json.loads((HERE/'expected.json').read_text());require(facts==expected,'expected facts')
    if args.support:
        keep=json.loads(args.support.read_text());missing,colours=pull_back(keep,projection,words)
        check_word(keep,edges,colours,range(4))
        args.colouring_out.write_text(json.dumps(dict(missing_label=missing,colouring=colours),sort_keys=True)+'\n')
    if args.geometry_out:args.geometry_out.write_text(json.dumps(dict(points=host,edges=edges,projection=projection),separators=(',',':'))+'\n')
    print(json.dumps(dict(status='QUADRATIC SWITCHING HOST CLOSED THROUGH508 BY EXACT COLOURING RETRACTION',facts=facts),indent=2,sort_keys=True))

if __name__=='__main__':main()
