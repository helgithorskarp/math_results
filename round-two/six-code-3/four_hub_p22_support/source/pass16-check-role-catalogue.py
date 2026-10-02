"""PRIVATE independent mask signatures, inverse friend pressure, heavy first.

Reuses the credited independent screen compiler only. The first catalogue
imports literal-set producer code; this catalogue does not. Every literal
signature, diagnostic frequency and original-order minimum witness matches.
"""
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import time

ROOT=Path('round-two/six-code-3');S=ROOT/'scratch'
spec=importlib.util.spec_from_file_location('independent_screen',S/'pass16-check-low-friends.py')
screen=importlib.util.module_from_spec(spec);spec.loader.exec_module(screen)

def need(c,m):
    if not c:raise ValueError(m)

def witness_key(w):
    roles=w['hub_roles'];H=tuple(sorted(roles))
    return w['fixture'],H,H.index(roles[0]),tuple(roles[1:])

def main():
    start=time.monotonic()
    raw=(ROOT/'four_hub_p21_endpoint_cut/fixtures.json').read_bytes()
    data=json.loads(raw)
    types=json.loads((ROOT/'four_hub_p21_endpoint_cut/expected.json').read_text())['types']
    index={screen.key(r):i for i,r in enumerate(types)}
    selected={i for r in json.loads((S/'pass16-p21-unit-graphs.json').read_text())['survivors'] for i,n in r['population']}
    signatures={};domain=0;relevant=0;role_count=0
    pairs=list(itertools.combinations(range(4),2));triples=list(itertools.combinations(range(4),3))
    for fi,blocks in enumerate(data['stars']):
        delta,high,low,friend,rows=screen.compile_one(blocks,fi)
        highmask=sum(1<<p for p in high)
        masks=[sum(1<<p for p in q) for q in blocks]
        cover=[0]*17
        for block in masks:
            for p in range(17):
                if block>>p&1:cover[p]|=block^(1<<p)
        leave=[((1<<17)-1)^(1<<p)^cover[p] for p in range(17)]
        inverse=Counter(friend.values());properties={}
        for heavy in range(17):
            for lights in itertools.combinations([p for p in range(17) if p!=heavy],3):
                H=tuple(sorted((heavy,)+lights))
                removed=Counter(friend[p] for p in H if p in friend)
                if any(delta[p]+inverse[p]-removed[p] > 5+4*(2 if p==heavy else 1 if p in lights else 0) for p in high):continue
                domain+=1
                J=tuple(p for p in high if p in H);type_id=index[screen.key(rows[J])]
                if type_id not in selected:continue
                relevant+=1
                if H not in properties:
                    Hmask=sum(1<<p for p in H)
                    counts=tuple(sum((block&Hmask).bit_count()==j for block in masks) for j in range(5))
                    properties[H]=counts
                counts=properties[H]
                for order in itertools.permutations(lights):
                    role_count+=1
                    need(role_count<=743262 and time.monotonic()-start<30,'INCOMPLETE fixed independent role domain guard')
                    roles=(heavy,)+order
                    d=tuple(delta[p] for p in roles)
                    HH=sum(1<<i for i,(a,b) in enumerate(pairs) if leave[roles[a]]>>roles[b]&1)
                    HHH=0
                    for i,t in enumerate(triples):
                        triple=sum(1<<roles[a] for a in t)
                        if any(block&triple==triple for block in masks):HHH|=1<<i
                    isolated=sum(1<<i for i,p in enumerate(roles) if delta[p] and not leave[p]&highmask)
                    signature=(type_id,d,HH,HHH,counts,isolated)
                    witness=dict(fixture=fi,hub_roles=list(roles))
                    if signature not in signatures:signatures[signature]=dict(frequency=0,witness=witness)
                    record=signatures[signature];record['frequency']+=1
                    if witness_key(witness)<witness_key(record['witness']):record['witness']=witness
    records=[dict(type_id=k[0],hub_deficits=list(k[1]),HH_leave_mask=k[2],HHH_covered_mask=k[3],
                  word_hub_counts=list(k[4]),eligible_hub_mask=k[5],**record)
             for k,record in sorted(signatures.items())]
    first=json.loads((S/'pass16-hub-role-catalogue.json').read_text())
    canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
    need(canonical(records)==canonical(first['records']),'all actual837 physical signatures/frequencies/witnesses differ')
    need([domain,relevant,role_count]==[first[k] for k in ('screened_mark_domain','relevant_actual_marks','light_role_bijections')],'full actual marking/bijection counts')
    need(role_count==6*relevant,'every one of the six light-role bijections')
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_TWO_ALGORITHM_ACTUAL_ROLE_CATALOGUE_AGREEMENT',
                actual_screened_markings=domain,relevant_actual_markings=relevant,light_role_bijections=role_count,
                signatures=len(records),all_literal_signatures_frequencies_witnesses_match=True,
                complete_records_sha256=hashlib.sha256(canonical(records)).hexdigest(),
                elapsed_seconds=time.monotonic()-start,independent_peer_review=False,ordinary_bridges_formalized=False,
                frequency_caps_global_centers=False,new_pair_total_claim=None)
    p=S/'pass16-independent-role-catalogue.json';need(not p.exists(),'fresh independent output')
    p.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
