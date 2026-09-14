#!/usr/bin/env python3
"""Exact point606 core and literal vertex-deletion certificate verification.

The standard-library path checks geometry, all 530 deletion words, and a
proper five-colouring. Non-four-colourability additionally needs --proof
and --drat-trim, or native regeneration as described in README.md.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
RAD=(1,3,5,15,11,33,55,165)

def require(ok, detail):
    if not ok: raise ValueError(detail)

def digest(data): return sha256(data).hexdigest()

def load_inputs():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,h in manifest['inputs'].items():
        require(digest((REPO/name).read_bytes())==h,('input hash',name))
    points=[]
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if not line or line.startswith('#'): continue
        row=[3*int(x) for x in line.split()]
        require(len(row)==16,'point width')
        points.append((tuple(row[:8]),tuple(row[8:])))
    require(len(points)==509,'original order')
    data=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())
    for p in data['points']:
        axes=[]
        for a in ('x','y'):
            coefficients=[288*Fraction(v) for v in p[a]]
            require(len(coefficients)==8 and all(v.denominator==1 for v in coefficients),'rational coordinates')
            axes.append(tuple(map(int,coefficients)))
        points.append(tuple(axes))
    require(points[606]==((-48,0,0,0,0,-48,0,0),(0,48,0,0,48,0,0,0)),'q606')
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    require(old['vertices']==list(range(585)) and len(old['forced'])==451,'old domain')
    library={v:[old['forced_witness'][str(v)]] for v in old['forced']}
    for row in json.loads((REPO/'hadwiger_nelson_parts509_degree6_lift_family/catalogue.json').read_text()):
        if row['kind']=='forced':
            require(row['index']==len(library[row['key']]),'library index')
            library[row['key']].append(row['witness'])
    return points,old,library,manifest

def norm(p,q):
    """Square directly in the linearly independent multiquadratic basis."""
    answer=[0]*8
    for axis in range(2):
        d=[a-b for a,b in zip(p[axis],q[axis],strict=True)]
        for i in range(8):
            answer[0]+=RAD[i]*d[i]*d[i]
            for j in range(i+1,8):
                answer[i^j]+=2*RAD[i&j]*d[i]*d[j]
    return tuple(answer)

def proper(vertices,edges,word,palette='0123'):
    require(len(word)==len(vertices) and set(word)<=set(palette),'word domain')
    colours=dict(zip(vertices,word,strict=True))
    for a,b in edges:
        if a in colours and b in colours:require(colours[a]!=colours[b],('monochromatic edge',a,b))
    return colours

def instance(vertices,edges):
    pos={v:i for i,v in enumerate(vertices)}
    rows=[[4*i+c+1 for c in range(4)] for i in range(len(vertices))]
    rows += [[-(4*pos[a]+c+1),-(4*pos[b]+c+1)] for a,b in edges for c in range(4)]
    triangle=[0,149,152]
    require(all(tuple(e) in edges for e in combinations(triangle,2)),'pin triangle')
    rows += [[4*pos[v]+c+1] for c,v in enumerate(triangle)]
    return (f'p cnf {4*len(vertices)} {len(rows)}\n'+''.join(' '.join(map(str,r))+' 0\n' for r in rows)).encode()

def compute():
    points,old,library,manifest=load_inputs()
    certificate=json.loads((HERE/'certificate.json').read_text())
    deleted=certificate['deleted_labels']
    host=list(range(585))+[606]
    require(deleted==sorted(set(deleted)) and 122 in deleted and set(deleted)<set(host),'deletion domain')
    require(len({points[v] for v in host})==len(host),'host collisions')
    host_edges=[(a,b) for a,b in combinations(host,2) if norm(points[a],points[b])==(288**2,)+(0,)*7]
    require(len(host_edges)==3090 and sum(b<509 for a,b in host_edges)==2442,'host unit graph')
    keep=[v for v in host if v not in deleted];selected=set(keep)
    edges=[e for e in host_edges if set(e)<=selected]
    require(len(keep)==530 and len(edges)==2648,'core dimensions')
    proper(keep,edges,certificate['five_colouring'],'01234')
    words={};edge_checks=0
    for v,i,append in certificate['original_deletion_references']:
        require(v in keep and v not in words,'reference labels')
        if v==606:
            require(i=='original122' and append is None,'q deletion reference')
            col=dict(zip([x for x in old['vertices'] if x!=122],library[122][0],strict=True))
        else:
            require(isinstance(i,int) and 0<=i<len(library[v]) and append in '0123','library reference')
            col=dict(zip([x for x in old['vertices'] if x!=v],library[v][i],strict=True));col[606]=append
        labels=[x for x in keep if x!=v]
        word=''.join(col[x] for x in labels)
        proper(labels,edges,word);words[v]=word
        edge_checks+=sum(v not in e for e in edges)
    for key,word in certificate['new_deletion_words'].items():
        v=int(key);require(v in keep and v not in words,'new word labels')
        proper([x for x in keep if x!=v],edges,word);words[v]=word
        edge_checks+=sum(v not in e for e in edges)
    require(set(words)==selected,'complete vertex-deletion coverage')
    core_cnf=instance(keep,edges)
    preflight=[v for v in host if v!=122]
    preflight_edges=[e for e in host_edges if 122 not in e]
    preflight_cnf=instance(preflight,preflight_edges)
    # Monochromatic-edge, palette, length, and input-loss controls.
    rejects=0
    bad=list(certificate['five_colouring']);a,b=edges[0];bad[keep.index(b)]=bad[keep.index(a)]
    for word,palette in [(''.join(bad),'01234'),(certificate['five_colouring'][:-1],'01234'),('x'+certificate['five_colouring'][1:],'01234')]:
        try: proper(keep,edges,word,palette)
        except ValueError:rejects+=1
        else:raise ValueError('bad word accepted')
    facts=dict(host_points=586,host_unit_edges=len(host_edges),host_pair_distances=len(host)*(len(host)-1)//2,
               points=530,unit_edges=2648,denominator=288,all_vertex_deletions_four_colourable=True,
               checked_vertex_deletion_words=len(words),new_literal_words=len(certificate['new_deletion_words']),
               deletion_word_edge_checks=edge_checks,five_colouring_checked=True,
               point_sha256=digest(json.dumps([points[v] for v in keep],separators=(',',':')).encode()),
               edge_sha256=digest(''.join(f'{a},{b}\n' for a,b in edges).encode()),
               cnf_sha256=digest(core_cnf),delete122_cnf_sha256=digest(preflight_cnf),
               corruptions_rejected=rejects,record_candidate=False,core_excess_over_cap=22)
    require(facts==manifest['facts'],'expected facts')
    return facts,core_cnf,preflight_cnf

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cnf-out',type=Path);ap.add_argument('--preflight-cnf-out',type=Path)
    ap.add_argument('--proof',type=Path);ap.add_argument('--drat-trim',type=Path);args=ap.parse_args()
    require(bool(args.proof)==bool(args.drat_trim),'proof/checker pairing')
    facts,cnf,preflight=compute()
    if args.cnf_out:args.cnf_out.write_bytes(cnf)
    if args.preflight_cnf_out:args.preflight_cnf_out.write_bytes(preflight)
    result=dict(facts=facts,non_four_proof_checked=False,
                status='EXACT CORE, FIVE-COLOURING AND ALL DELETION WORDS VERIFIED; NON-FOUR PROOF NOT CHECKED')
    if args.proof:
        with tempfile.TemporaryDirectory(prefix='hn-point606-') as td:
            path=Path(td)/'core.cnf';path.write_bytes(cnf)
            p=subprocess.run([str(args.drat_trim.resolve()),str(path),str(args.proof.resolve())],capture_output=True,text=True)
        require(p.returncode==0 and 's VERIFIED' in p.stdout,'non-four proof rejected')
        result.update(non_four_proof_checked=True,status='530-POINT FIVE-CHROMATIC VERTEX-CRITICAL CORE VERIFIED; CAP MISSED')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
