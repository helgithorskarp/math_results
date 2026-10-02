"""Private full relevant physical H4 marks with exact hub-friend degrees.

Literal point sets determine the unordered H properties once, then explicit
24 role bijections transport them. Every accepted mark and all six light
orders are retained, including local HHH mask15/four-hub words. Frequency
is diagnostic; it NEVER caps repeated rows in a global code.
"""
from collections import Counter
import hashlib,itertools,json,sys,time
from pathlib import Path
R=Path('round-two/six-code-3');S=R/'scratch'
sys.path.insert(0,str(R/'four_hub_p21_endpoint_cut'))
import produce
PAIR=list(itertools.combinations(range(4),2));TRIPLE=list(itertools.combinations(range(4),3))

def need(c,m):
    if not c:raise ValueError(m)

def tables():
    out={}
    for order in itertools.permutations(range(4)):
        pm=[PAIR.index(tuple(sorted((order[a],order[b])))) for a,b in PAIR]
        tm=[TRIPLE.index(tuple(sorted(order[a] for a in t))) for t in TRIPLE]
        out[order]=([sum(1<<i for i,j in enumerate(pm) if mask>>j&1) for mask in range(64)],
                    [sum(1<<i for i,j in enumerate(tm) if mask>>j&1) for mask in range(16)],
                    [sum(1<<i for i,j in enumerate(order) if mask>>j&1) for mask in range(16)])
    return out

def main():
    start=time.monotonic();data=json.loads((R/'four_hub_p21_endpoint_cut/fixtures.json').read_text())
    rows=produce.rows_from_data(data);byrow={(r['fixture'],tuple(r['hub_high'])):r for r in rows}
    types=json.loads((R/'four_hub_p21_endpoint_cut/expected.json').read_text())['types'];index={produce.type_key(r):i for i,r in enumerate(types)}
    screen=json.loads((S/'pass16-first-engine-low-friends.json').read_text())
    needed=set([0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 40, 42, 44, 46, 47, 49, 50, 53, 56, 57])
    maps=tables();signatures={};domain=selected=transports=0
    for fi,blocks in enumerate(data['stars']):
        star=produce.compile_star(blocks,fi);bs=[frozenset(b) for b in blocks]
        covered={frozenset(p) for b in bs for p in itertools.combinations(sorted(b),2)}
        covered3={frozenset(t) for b in bs for t in itertools.combinations(sorted(b),3)}
        low=set(range(17))-star['high']
        accepted=int.from_bytes(bytes.fromhex(screen['records'][fi]['accepted_membership_hex']),'little')
        for rank,H in enumerate(itertools.combinations(range(17),4)):
            Hset=frozenset(H);J=tuple(p for p in H if p in star['high']);row=byrow[fi,J];tid=index[produce.type_key(row)]
            good=[offset for offset in range(4) if accepted>>(4*rank+offset)&1]
            domain+=len(good)
            if tid not in needed or not good:continue
            baseD=tuple(star['delta'][p] for p in H)
            baseL=tuple(sum(frozenset((p,t)) not in covered for t in low-Hset) for p in H)
            baseHH=sum(1<<i for i,(a,b) in enumerate(PAIR) if frozenset((H[a],H[b])) not in covered)
            baseHHH=sum(1<<i for i,t in enumerate(TRIPLE) if frozenset(H[a] for a in t) in covered3)
            counts=tuple(sum(len(b&Hset)==j for b in bs) for j in range(5))
            baseEligible=sum(1<<i for i,p in enumerate(H) if p in star['isolated'])
            need(sum(counts)==20 and baseHHH in (0,1,2,4,8,15),'all20 words and allowable local HHH ownership')
            need(sum(baseL)==row['k']+3*row['hub_weight']-row['q']-baseHH.bit_count(),'exact hub-friend sum identity')
            need(sum(baseL)<=13-(row['h']-row['k']),'distinct LOW-SAT friend support')
            need(all(baseL[a]==0 for a,d in enumerate(baseD) if d==0),'LOW-LOW hub friend violation')
            for heavy in good:
                selected+=1
                for lights in itertools.permutations([a for a in range(4) if a!=heavy]):
                    transports+=1
                    if transports>743262 or time.monotonic()-start>30:raise RuntimeError('INCOMPLETE fixed full physical role guard; no absence')
                    order=(heavy,)+lights;roles=tuple(H[a] for a in order);pm,tm,em=maps[order]
                    d=tuple(baseD[a] for a in order);friends=tuple(baseL[a] for a in order)
                    signature=(tid,d,pm[baseHH],tm[baseHHH],counts,em[baseEligible],friends)
                    if signature not in signatures:signatures[signature]=dict(frequency=0,witness=dict(fixture=fi,hub_roles=list(roles)))
                    signatures[signature]['frequency']+=1
        print(json.dumps(dict(fixture=fi,screened_marks=domain,selected_marks=selected,role_transports=transports,signatures=len(signatures),elapsed_seconds=time.monotonic()-start)),flush=True)
    need(domain==123877 and transports==6*selected,'complete actual marks and six light orders')
    records=[dict(type_id=k[0],hub_deficits=list(k[1]),HH_leave_mask=k[2],HHH_covered_mask=k[3],word_hub_counts=list(k[4]),eligible_hub_mask=k[5],low_sat_friend_degrees=list(k[6]),**value) for k,value in sorted(signatures.items())]
    canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
    out=S/'pass21-T1-hub-friend-catalogue.json';need(not out.exists(),'fresh catalogue')
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_SINGLE_ENGINE_EXACT_HUB_FRIEND_SIGNATURES',screened_mark_domain=domain,relevant_actual_marks=selected,light_role_bijections=transports,relevant_type_ids=sorted(needed),pair_roles=PAIR,triple_roles=TRIPLE,records=records,frequency_caps_global_centers=False,higher_T_and_four_hub_words_retained=True,independent_catalogue_check_pending=True,new_pair_total_claim=None)
    out.write_bytes(canonical(result)+b'\n')
    print(json.dumps(dict(screened_marks=domain,selected_marks=selected,role_transports=transports,signatures=len(records),by_local_HHH={mask:sum(r['HHH_covered_mask']==mask for r in records) for mask in (0,1,2,4,8,15)},records_sha256=hashlib.sha256(canonical(records)).hexdigest(),elapsed_seconds=time.monotonic()-start)),flush=True)
if __name__=='__main__':main()
