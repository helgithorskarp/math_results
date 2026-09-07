#!/usr/bin/env python3
"""Check the fixed pilot using tensor-ring arithmetic, without SAT or producer imports."""
import argparse
from collections import defaultdict
from functools import lru_cache
from itertools import product
from math import gcd
import hashlib
import json
from pathlib import Path
import time

CENTRES = [[0,0,0,0],[4,13,7,9],[0,6,13,9],[5,11,13,6],
           [10,14,14,6],[9,3,8,10],[6,14,10,3],[11,8,11,12]]


def require(ok,why):
    if not ok: raise ValueError(why)


def multiply(v,w):
    # omega^2=omega-1, tau^2=tau-18. Index=i+2*j means omega^i tau^j.
    result=[0]*4
    for i,a in enumerate(v):
        for j,b in enumerate(w):
            if not a or not b: continue
            u=(i&1)+(j&1);t=(i>>1)+(j>>1)
            terms_u=[(u,1)] if u<2 else [(0,-1),(1,1)]
            terms_t=[(t,1)] if t<2 else [(0,-18),(1,1)]
            for k,c in terms_u:
                for l,d in terms_t:result[k+2*l]+=a*b*c*d
    return tuple(result)


def conjugate(v):
    a,b,c,d=v
    return a+b+c+d,-b-d,-c-d,d


@lru_cache(None)
def algebraic_norm(v):
    a,b,c,d=multiply(v,conjugate(v))
    require(b==c and d==-2*b,'norm not fixed by physical conjugation')
    # sqrt(213) = -1+2omega+2tau-4omega*tau.
    return 16*a+8*b,8*b


def integer_rank(vectors):
    rows=[list(v) for v in vectors];position=0
    for col in range(4):
        pivot=next((i for i in range(position,len(rows)) if rows[i][col]),None)
        if pivot is None:continue
        rows[position],rows[pivot]=rows[pivot],rows[position]
        for i in range(position+1,len(rows)):
            if rows[i][col]:
                a,b=rows[position][col],rows[i][col]
                rows[i]=[a*x-b*y for x,y in zip(rows[i],rows[position])]
                divisor=gcd(*rows[i])
                if divisor:rows[i]=[x//divisor for x in rows[i]]
        position+=1
        if position==4:break
    return position


def reconstruct(centre):
    candidates=[]
    for v in product(range(-10,11),range(-10,11),range(-3,4),range(-3,4)):
        scaled=tuple(16*x-h for x,h in zip(v,centre))
        candidates.append((algebraic_norm(scaled)[0],v))
    candidates.sort();threshold=candidates[507][0]
    require(all(6*threshold<71*(176-centre[j])**2 for j in (0,1)), 'a/b truncation')
    require(all(threshold<213*(64-centre[j])**2 for j in (2,3)), 'c/d truncation')
    points=[v for score,v in candidates[:508]]
    require(len(set(points))==508,'colliding lattice labels')
    edges=defaultdict(list);directions=defaultdict(set)
    for j,w in enumerate(points):
        for i,v in enumerate(points[:j]):
            delta=tuple(a-b for a,b in zip(w,v));norm=algebraic_norm(delta)
            a,b=norm
            require(a>0 and a*a>213*b*b,'nonpositive physical norm')
            edges[norm].append([i,j]);directions[norm].add(delta)
    selected=[]
    for n in sorted(edges,key=lambda n:(-len(edges[n]),n)):
        if integer_rank(sorted(directions[n]))==4:
            selected.append(n)
            if len(selected)==4:break
    return points,threshold,edges,directions,selected


def check_word(word,edges):
    require(type(word) is str and len(word)==508 and set(word)<=set('0123'),'bad colour word')
    require(all(word[i]!=word[j] for i,j in edges),'monochromatic unit edge')


def audit(certificate,work=None):
    require(certificate['format']==1 and certificate['vertices']==508,'wrong format/order')
    require(certificate['field']=='Q(sqrt(-3),sqrt(-71))','wrong field')
    require(certificate['candidate_cap']==32 and certificate['conflict_cap']==100000,'wrong gate')
    require(not certificate['stopped_on_signal'],'unexpected claimed signal')
    require([w['centre16'] for w in certificate['windows']]==CENTRES,'wrong sample windows')
    # Small exact controls use separate ring identities and non-rational norms.
    e=[tuple(int(i==j) for i in range(4)) for j in range(4)]
    require(multiply(e[1],e[1])==(-1,1,0,0),'omega polynomial')
    require(multiply(e[2],e[2])==(-18,0,1,0),'tau polynomial')
    require(all(conjugate(conjugate(v))==v for v in e),'conjugation involution')
    require(algebraic_norm(e[0])==(16,0) and algebraic_norm(e[2])==(288,0),'rational norm controls')
    require(algebraic_norm((0,1,1,0))==(312,8),'radical sign control')
    sizes=[];stream=hashlib.sha256();total_edge_checks=0;cases=0;corruptions=0
    for wi,row in enumerate(certificate['windows']):
        points,threshold,groups,directions,selected=reconstruct(row['centre16'])
        require(row['threshold']==threshold,'incorrect window threshold')
        require(len(row['candidates'])==4,'incomplete candidate list')
        require([tuple(c['norm16']) for c in row['candidates']]==selected,'selection protocol mismatch')
        if work:
            generated=json.loads((work/f'window_{wi}.json').read_text())
            require(generated['points']==[list(v) for v in points],'producer point mismatch')
        for ci,c in enumerate(row['candidates']):
            n=tuple(c['norm16']);edges=sorted(groups[n])
            require(c['edge_count']==len(edges),'edge-count mismatch')
            require(c['step_rank']==4 and integer_rank(directions[n])==4,'step-rank mismatch')
            require(c['observed_step_vectors']==len(directions[n]),'direction-count mismatch')
            require(c['status']=='SAT','certificate is not a colouring')
            check_word(c['colouring'],edges)
            if work:require(generated['candidates'][ci]['edges']==edges,'producer edge mismatch')
            # One deliberately corrupted colouring per sampled graph must fail.
            i,j=edges[0];bad=list(c['colouring']);bad[j]=bad[i]
            try:check_word(''.join(bad),edges)
            except ValueError:corruptions+=1
            else:raise ValueError('accepted corrupt colouring')
            stream.update((c['colouring']+'\n').encode())
            total_edge_checks+=len(edges);sizes.append(len(edges));cases+=1
    require(cases==32 and corruptions==32,'wrong sample count')
    return {'verified':True,'candidate_count':cases,'vertices_per_candidate':508,
            'edge_count_min':min(sizes),'edge_count_max':max(sizes),
            'unit_edges_checked':total_edge_checks,'all_pair_norm_checks':8*508*507//2,
            'verified_four_colourings':32,'rejected_corrupt_colourings':corruptions,
            'non_four_colourable_signals':0,'unknown_queries':0,
            'colour_stream_sha256':stream.hexdigest(),'rank_four_candidates':32,
            'field_or_family_closure_claimed':False,'record_improvement':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate',type=Path,required=True)
    p.add_argument('--work',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args();start=time.monotonic()
    data=args.certificate.read_bytes();result=audit(json.loads(data),args.work)
    result['certificate_sha256']=hashlib.sha256(data).hexdigest()
    if args.output:args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
    print(json.dumps({'seconds':time.monotonic()-start,'cached_norms':algebraic_norm.cache_info().currsize}))


if __name__=='__main__':main()
