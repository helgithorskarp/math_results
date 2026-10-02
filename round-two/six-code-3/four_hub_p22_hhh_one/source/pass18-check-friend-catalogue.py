"""Private independent full H4 friend-degree signature reconstruction.

Heavy-first marked carriers, independent mask leave/HHH lookup, and
inverse LOW-friend counts excluding hubs. No author mathematical imports.
All signature records, diagnostics and minimum original-order witnesses
are compared, rather than only a projected type set or total count.
"""
from collections import Counter
import hashlib,importlib.util,itertools,json,time
from pathlib import Path
R=Path('round-two/six-code-3');S=R/'scratch'
spec=importlib.util.spec_from_file_location('independent_screen',S/'pass16-check-low-friends.py')
screen=importlib.util.module_from_spec(spec);spec.loader.exec_module(screen)

def need(c,m):
    if not c:raise ValueError(m)

def wkey(w):
    roles=w['hub_roles'];H=tuple(sorted(roles));return w['fixture'],H,H.index(roles[0]),tuple(roles[1:])

def main():
    start=time.monotonic();data=json.loads((R/'four_hub_p21_endpoint_cut/fixtures.json').read_text());types=json.loads((R/'four_hub_p21_endpoint_cut/expected.json').read_text())['types']
    index={screen.key(r):i for i,r in enumerate(types)}
    wanted=set([0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,34,35,36,40,42,44,46,47,49,50,53,56,57])
    pairs=list(itertools.combinations(range(4),2));triples=list(itertools.combinations(range(4),3))
    domain=relevant=transports=0;signatures={}
    for fi,blocks in enumerate(data['stars']):
        delta,high,low,friend,rows=screen.compile_one(blocks,fi);highmask=sum(1<<p for p in high)
        masks=[sum(1<<p for p in b) for b in blocks];cover=[0]*17
        triples_owned={sum(1<<p for p in t) for b in blocks for t in itertools.combinations(b,3)}
        for block in masks:
            for p in range(17):
                if block>>p&1:cover[p]|=block^(1<<p)
        leave=[((1<<17)-1)^(1<<p)^cover[p] for p in range(17)];inverse=Counter(friend.values());properties={}
        for heavy in range(17):
            for lights in itertools.combinations([p for p in range(17) if p!=heavy],3):
                H=tuple(sorted((heavy,)+lights));removed=Counter(friend[p] for p in H if p in friend)
                if any(delta[p]+inverse[p]-removed[p]>5+4*(2 if p==heavy else 1 if p in lights else 0) for p in high):continue
                domain+=1;J=tuple(p for p in high if p in H);tid=index[screen.key(rows[J])]
                if tid not in wanted:continue
                relevant+=1
                if H not in properties:
                    Hmask=sum(1<<p for p in H);properties[H]=tuple(sum((block&Hmask).bit_count()==j for block in masks) for j in range(5))
                counts=properties[H]
                for order in itertools.permutations(lights):
                    transports+=1;need(transports<=743262 and time.monotonic()-start<30,'INCOMPLETE fixed independent friend-mark guard')
                    roles=(heavy,)+order;d=tuple(delta[p] for p in roles)
                    HH=sum(1<<i for i,(a,b) in enumerate(pairs) if leave[roles[a]]>>roles[b]&1)
                    HHH=sum(1<<i for i,t in enumerate(triples) if sum(1<<roles[a] for a in t) in triples_owned)
                    eligible=sum(1<<i for i,p in enumerate(roles) if delta[p] and not leave[p]&highmask)
                    friends=tuple(inverse[p]-removed[p] if delta[p] else 0 for p in roles)
                    need(sum(friends)==rows[J]['k']+3*rows[J]['hub_weight']-rows[J]['q']-HH.bit_count(),'independent exact friend-degree sum')
                    signature=(tid,d,HH,HHH,counts,eligible,friends);witness=dict(fixture=fi,hub_roles=list(roles))
                    if signature not in signatures:signatures[signature]=dict(frequency=0,witness=witness)
                    rec=signatures[signature];rec['frequency']+=1
                    if wkey(witness)<wkey(rec['witness']):rec['witness']=witness
        print(json.dumps(dict(fixture=fi,actual_marks=domain,selected_marks=relevant,role_transports=transports,signatures=len(signatures),elapsed_seconds=time.monotonic()-start)),flush=True)
    records=[dict(type_id=k[0],hub_deficits=list(k[1]),HH_leave_mask=k[2],HHH_covered_mask=k[3],word_hub_counts=list(k[4]),eligible_hub_mask=k[5],low_sat_friend_degrees=list(k[6]),**rec) for k,rec in sorted(signatures.items())]
    first=json.loads((S/'pass18-hub-friend-catalogue.json').read_text());canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
    need(canonical(records)==canonical(first['records']),'every exact physical signature/frequency/witness differs')
    need([domain,relevant,transports]==[first[k] for k in ['screened_mark_domain','relevant_actual_marks','light_role_bijections']],'all marking/transport totals')
    need(transports==6*relevant and domain==123877,'full domain and six light bijections')
    need(sorted(wanted)==first['relevant_type_ids'],'all needed type IDs')
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_TWO_ENGINE_FRIEND_SIGNATURE_AGREEMENT',screened_mark_domain=domain,relevant_actual_marks=relevant,light_role_bijections=transports,exact_signatures=len(records),all_records_frequencies_minimum_witnesses_match=True,records_sha256=hashlib.sha256(canonical(records)).hexdigest(),elapsed_seconds=time.monotonic()-start,ordinary_bridges_formalized=False,external_review=False,frequency_caps_global_centers=False,new_pair_total_claim=None)
    out=S/'pass18-independent-friend-catalogue.json';need(not out.exists(),'fresh independent record');out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
