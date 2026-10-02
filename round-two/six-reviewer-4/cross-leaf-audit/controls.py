#!/usr/bin/env python3
"""Small definition-level, transport, witness and damaged-record controls."""
import argparse
from collections import Counter
from copy import deepcopy
from itertools import combinations, permutations, product
import hashlib
import json
from math import comb
from pathlib import Path
from compare import build
from reproduce import canonical, require
from structure import controls as matrix_controls

def move(mask,p):
    return sum(1<<p[i] for i in range(len(p)) if mask&(1<<i))

def core_controls():
    words=[]
    for word in product(range(3),repeat=4):
        degree=[sum(t!=omitted for omitted in word) for t in range(3)]
        if max(degree)<=3:words.append(word)
    require(len(words)==36,'ordinary omission domain')
    counts=Counter();normal=set();tagged=0
    for sx0,sx1,sy0,sy1 in words:
        if sx0==sx1:counts['Xsame']+=1;continue
        if sy0==sy1:counts['Ysame']+=1;continue
        counts['cross']+=1
        repeat=next(t for t in range(3) if [sx0,sx1,sy0,sy1].count(t)==2)
        r=0 if sx0==repeat else 1
        sy_repeat=0 if sy0==repeat else 1
        other_sx=[sx0,sx1][1-r];other_sy=[sy0,sy1][1-sy_repeat]
        tmap={repeat:0,other_sx:1,other_sy:2}
        p=list(range(22))
        p[11+sy_repeat]=11;p[12-sy_repeat]=12
        for t in range(3):p[13+t]=13+tmap[t]
        require(sorted(p)==list(range(22)),'core transport permutation')
        masks=[sum(1<<tmap[t] for t in range(3) if t!=om) for om in [sx0,sx1,sy0,sy1]]
        if sy_repeat:masks[2],masks[3]=masks[3],masks[2]
        require(masks==([6,5] if r==0 else [5,6])+[6,3],'both SX retained normalization')
        normal.add((r,tuple(masks)))
        inverse=[p.index(i) for i in range(22)]
        for lows in combinations(range(11,22),3):
            image={p[i] for i in lows};require({inverse[i] for i in image}==set(lows),'individual low-tag transport')
            tagged+=1
    require(dict(counts)=={'Ysame':6,'cross':24,'Xsame':6},'36-core partition')
    flags=[l for l in product(range(2),repeat=5) if sum(l)<=3]
    require(len(flags)==26 and sum(comb(6,3-sum(l)) for l in flags)==165,'all low placements')
    require(len(normal)==2,'no actual SX choice deleted')
    return {'ordinary_omission_words':36,'cross_cores':24,'same_side_cores_each':6,
            'individual_cross_core_low_transports':tagged,'normalized_SX_choices':2,
            'flag_words':26,'labeled_other_low_placements_per_core':165}

def subset_controls():
    minima={};blue_minima={}
    for a,b in product(range(64),repeat=2):
        k=(a.bit_count(),b.bit_count());v=(a&b).bit_count();w=((63^a)&(63^b)).bit_count()
        minima[k]=min(minima.get(k,7),v);blue_minima[k]=min(blue_minima.get(k,7),w)
        require(v>=max(0,sum(k)-6) and w>=max(0,6-sum(k)),'literal colored lower bounds')
    require(all(v==max(0,sum(k)-6) for k,v in minima.items()),'red bound attained at every rank')
    require(all(v==max(0,6-sum(k)) for k,v in blue_minima.items()),'blue bound attained at every rank')
    transports=0;tagged=0
    for prototype,intersection,size in [((15,51),2,90),((15,23),3,120)]:
        images=set()
        for p in permutations(range(6)):
            images.add(tuple(move(mask,p) for mask in prototype));transports+=1
            inverse=tuple(p.index(i) for i in range(6))
            for low in range(64):
                require(move(move(low,p),inverse)==low,'Q tags travel through normalization')
                tagged+=1
        target={(a,b) for a,b in product(range(64),repeat=2) if a.bit_count()==b.bit_count()==4 and (a&b).bit_count()==intersection}
        require(len(images)==size and images==target,'entire ordered prototype orbit')
    return {'subset_pairs':4096,'exact_rank_minima_each_color':49,'ordered_SX_transports':transports,
            'Q_low_mask_transport_controls':tagged,'ordered_pair_orbit_sizes':[90,120]}

def book_controls(full, primary):
    raw=json.loads(primary.read_text());n=len(raw);require(n==21,'primary order')
    pages=[[],[]]
    for i,j in combinations(range(n),2):
        # Packaged rows are RED adjacency; raw primary off-diagonal zero is RED.
        color=raw[i][j]
        pages[color].append(sum(k!=i and k!=j and raw[i][k]==color and raw[j][k]==color for k in range(n)))
    require((len(pages[1]),len(pages[0]),max(pages[1]),max(pages[0]))==(93,117,3,6),'primary positive control')
    for color,n,allowed in [(1,5,True),(1,6,False),(0,8,True),(0,9,False)]:
        cap=3 if color else 6
        require((n-2<=cap)==allowed,'colored book threshold')
    transported=0
    for row in full['records']['joins']:
        r=[set(v) for v in build(row)]
        for i,mask in enumerate([0,63,0]+row[27:33]+row[20:27]):
            for y in range(6):
                if mask&(1<<y):r[i].add(16+y);r[16+y].add(i)
        i,j=row[39:41];pages=[p for p in range(22) if row[41]&(1<<p)]
        require(len(pages)>=4 and j in r[i] and all(p in r[i] and p in r[j] for p in pages),'whole literal known-red witness')
        for shift in range(6):
            p=list(range(16))+[16+(y+shift)%6 for y in range(6)]
            rr=[set() for _ in range(22)]
            for a in range(22):rr[p[a]]={p[b] for b in r[a]}
            require(p[j] in rr[p[i]] and all(p[k] in rr[p[i]] and p[k] in rr[p[j]] for k in pages),'physical witness transport')
            require(all(not(rr[y]&set(range(16,22))) for y in range(16,22)),'unassigned Q edges became red')
            transported+=1
    return {'primary_n':21,'red_edges':93,'blue_pairs':117,'page_maxima':[3,6],
            'primary_rows_sha256':hashlib.sha256(primary.read_bytes()).hexdigest(),
            'colored_threshold_controls':4,'individual_known_books':len(full['records']['joins']),
            'physical_Q_witness_transports':transported}

def unique(items):
    out={}
    for k,v in items:
        require(k not in out,'duplicate JSON field');out[k]=v
    return out

def damages(full):
    def accept(text):
        value=json.loads(text,object_pairs_hook=unique)
        require(canonical(value)==canonical(full),'entire regenerated record differs')
    mutations=[lambda r:r['records']['x'].pop(),lambda r:r['records']['x'].append(r['records']['x'][0]),
               lambda r:r['records']['x'][0].__setitem__(0,1),
               lambda r:r['records']['x'][0].__setitem__(1,1-r['records']['x'][0][1]),
               lambda r:r['records']['frames'].pop(),lambda r:r['records']['frames'][0].__setitem__(21,15),
               lambda r:r['records']['joins'].pop(),lambda r:r['records']['joins'][0].__setitem__(33,1),
               lambda r:r['records']['joins'][0].__setitem__(39,0),
               lambda r:r['records']['joins'][0].__setitem__(41,1),
               lambda r:r['coordinates'].__setitem__(9,'SY0'),
               lambda r:r['metadata'].__setitem__('cartesian_tuples',0)]
    texts=[]
    for mutate in mutations:
        value=deepcopy(full);mutate(value);texts.append(canonical(value).decode())
    base=canonical(full).decode().rstrip()
    texts.extend([base[:-1]+',"metadata":'+json.dumps(full['metadata'])+'}',base+' false'])
    for text in texts:
        try:accept(text)
        except (ValueError,json.JSONDecodeError):continue
        raise ValueError('damaged record accepted')
    return {'rejected_whole_record_or_encoding_damages':len(texts),
            'damage_basis':'strict duplicate-field decoder and equality to entire freshly regenerated domains; no count-only acceptance'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();full=json.loads(a.full.read_text())
    result={'core':core_controls(),'subsets':subset_controls(),
            'books':book_controls(full,Path(__file__).with_name('primary21.json')),
            'signed_matrix':matrix_controls(),'damages':damages(full)}
    a.out.write_bytes(canonical(result));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
