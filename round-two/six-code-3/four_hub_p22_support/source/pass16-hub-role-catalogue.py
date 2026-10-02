"""PRIVATE all accepted actual H4 marks and all six light-role bijections.

Rows are compressed by a physical signature, with a literal witness.
Multiplicity is retained diagnostically and NEVER caps global row use.
Hub role0 is defect two; roles1,2,3 have defect one.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

ROOT=Path('round-two/six-code-3')
sys.path.insert(0,str(ROOT/'four_hub_p21_endpoint_cut'))
import produce

def main():
    start=time.monotonic()
    data=json.loads((ROOT/'four_hub_p21_endpoint_cut/fixtures.json').read_text())
    physical=produce.rows_from_data(data)
    by_row={(r['fixture'],tuple(r['hub_high'])):r for r in physical}
    types=json.loads((ROOT/'four_hub_p21_endpoint_cut/expected.json').read_text())['types']
    type_index={produce.type_key(r):i for i,r in enumerate(types)}
    first=json.loads((ROOT/'scratch/pass16-first-engine-low-friends.json').read_text())
    needed={i for r in json.loads((ROOT/'scratch/pass16-p21-unit-graphs.json').read_text())['survivors'] for i,n in r['population']}
    signatures={};domain_marks=0;role_marks=0;selected_marks=0
    rolepairs=list(itertools.combinations(range(4),2))
    roletriples=list(itertools.combinations(range(4),3))
    for fi,blocks in enumerate(data['stars']):
        s=produce.compile_star(blocks,fi)
        covered={frozenset(pair) for block in blocks for pair in itertools.combinations(block,2)}
        blocksets=[frozenset(b) for b in blocks]
        accepted=int.from_bytes(bytes.fromhex(first['records'][fi]['accepted_membership_hex']),'little')
        for rank,H in enumerate(itertools.combinations(range(17),4)):
            J=tuple(p for p in H if p in s['high'])
            row=by_row[fi,J];type_id=type_index[produce.type_key(row)]
            Hset=frozenset(H)
            bcounts=tuple(sum(len(b&Hset)==j for b in blocksets) for j in range(5))
            if sum(bcounts)!=20:raise ValueError('all twenty physical words classified')
            for offset,heavy in enumerate(H):
                if not accepted>>(4*rank+offset)&1:continue
                domain_marks+=1
                if type_id not in needed:continue
                selected_marks+=1
                for lights in itertools.permutations([p for p in H if p!=heavy]):
                    role_marks+=1
                    if role_marks>743262 or time.monotonic()-start>30:
                        raise RuntimeError('INCOMPLETE fixed full physical role guard; no absence')
                    roles=(heavy,)+lights
                    deficit=tuple(s['delta'][p] for p in roles)
                    leave=sum(1<<i for i,(a,b) in enumerate(rolepairs) if frozenset((roles[a],roles[b])) not in covered)
                    triple=sum(1<<i for i,t in enumerate(roletriples)
                               if any(frozenset(roles[a] for a in t)<=b for b in blocksets))
                    eligible_hubs=sum(1<<i for i,p in enumerate(roles) if p in s['isolated'])
                    signature=(type_id,deficit,leave,triple,bcounts,eligible_hubs)
                    if signature not in signatures:
                        signatures[signature]=dict(frequency=0,witness=dict(fixture=fi,hub_roles=list(roles)))
                    signatures[signature]['frequency']+=1
    records=[dict(type_id=k[0],hub_deficits=list(k[1]),HH_leave_mask=k[2],HHH_covered_mask=k[3],
                  word_hub_counts=list(k[4]),eligible_hub_mask=k[5],**value)
             for k,value in sorted(signatures.items())]
    if domain_marks!=123877:raise ValueError('full physical screen domain')
    if role_marks!=6*selected_marks:raise ValueError('every light-role bijection, including duplicates')
    stats={i:dict(signatures=sum(r['type_id']==i for r in records),
                 T0_signatures=sum(r['type_id']==i and not r['HHH_covered_mask'] for r in records),
                 T1_signatures=sum(r['type_id']==i and r['HHH_covered_mask'].bit_count()<=1 for r in records),
                 min_HH_leaves=min(r['HH_leave_mask'].bit_count() for r in records if r['type_id']==i),
                 max_HH_leaves=max(r['HH_leave_mask'].bit_count() for r in records if r['type_id']==i),
                 min_heavy_deficit=min(r['hub_deficits'][0] for r in records if r['type_id']==i),
                 max_heavy_deficit=max(r['hub_deficits'][0] for r in records if r['type_id']==i)) for i in sorted(needed)}
    out=ROOT/'scratch/pass16-hub-role-catalogue.json'
    if out.exists():raise ValueError('fresh physical catalogue')
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_SINGLE_ENGINE_ACTUAL_HUB_ROLE_CATALOGUE',
                screened_mark_domain=domain_marks,relevant_actual_marks=selected_marks,light_role_bijections=role_marks,
                relevant_type_ids=sorted(needed),pair_roles=rolepairs,triple_roles=roletriples,statistics=stats,records=records,
                frequency_caps_global_centers=False,new_pair_total_claim=None,independent_catalogue_check_pending=True)
    raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()+b'\n';out.write_bytes(raw)
    print(json.dumps(dict(screened_mark_domain=domain_marks,relevant_actual_marks=selected_marks,light_role_bijections=role_marks,
                         signatures=len(records),statistics=stats,elapsed_seconds=time.monotonic()-start,
                         catalogue_sha256=hashlib.sha256(raw).hexdigest()),sort_keys=True))

if __name__=='__main__':main()
