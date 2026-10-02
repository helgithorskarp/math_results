"""Post-seal, data-only corroboration; imports no target program.
Full projected populations and every target column record are inspected.
The core intentionally omits zero-leave local filters, yielding a larger
relaxation. Native coordinate sets must be subsets of the independently
computed sets, and both complete coupled tests must be empty.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,hashlib,argparse
from rows import need,encoded
from audit import PAIRS,TRIPLES,column_choices,joint,carriers

def type_key(t):
    return (t['e'],t['k'],t['q'],t['eligible'],tuple(t['ss_hist']),t['psi'],t['margin'])

def failures(types,vector):
    vertices=[t for t,n in zip(types,vector) for _ in range(n)]
    ans=set()
    for i,t in enumerate(vertices):
        radius=0
        for color,demand in enumerate(t[4]):
            possible=[sum(u[4]) for j,u in enumerate(vertices) if i!=j and u[4][color]
                      and not ((t[0]==0 and u[3])or(u[0]==0 and t[3]))]
            if len(possible)<demand:ans.add('too_few_weighted_partners')
            radius+=sum(sorted(possible,reverse=True)[:demand])
        if not t[1] and radius<13:ans.add('hub_complete_radius_two')
    if any(sum(t[4][j]for t in vertices)%2 for j in range(5)):ans.add('odd_weight_layer')
    return sorted(ans)

def compare(own,physical,native):
    types=[(t[0],t[1],t[2],t[3],tuple(t[4]),t[5],t[6]) for t in own['raw_types']]
    original=native/'round-two/six-code-3/scratch'
    authored=json.loads((original/'pass20-T2-producer.json').read_bytes())
    inv=authored['inventory'];mapping={i:types.index(type_key(t)) for i,t in enumerate(inv['types'])}
    need(set(mapping.values())==set(range(60)),'all sixty semantic types bijective')
    raw={(r['fixture'],tuple(r['hubs'])):r for r in physical['raw']}
    for r in authored['rows']:
        ours=raw[r['fixture'],tuple(r['hub_high'])]
        fields={'h':'h','e':'e','k':'k','q':'q','eligible':'eligible','g1_S':'g1','ss_excess':'sigma','psi':'psi','margin':'margin3'}
        need(all(r[a]==ours[b] for a,b in fields.items()),'entire raw row fields')
        need(r['ss_hist']==ours['colors'],'entire raw row colors')
        need(r['hub_weight']==sum(5-ours['replication'][a] for a in ours['hubs']),'raw hub weights')
    need(len(authored['rows'])==len(raw)==426,'entire raw row domain')
    branches={(b['Q'],b['X'],b['tau']):b for b in own['branches']}
    originals=[];vectors_checked=0
    for b in inv['branches']:
        here=branches[b['Q'],b['X'],b['tau']]
        need((b['T'],b['E'],b['K'])==(2,here['E'],here['K']),'all branch totals')
        expected={tuple(r['counts']):r for r in here['records']};seen=set()
        for r in b['templates']:
            v=[0]*60
            for tid,n in r['population']:v[mapping[tid]]=n
            v=tuple(v);need(v in expected and v not in seen,'entire population vector membership/uniqueness');seen.add(v)
            need(r['failures']==failures(types,v),'entire failure list')
            if not r['failures']:originals.append((b,v))
            vectors_checked+=1
        need(seen==set(expected),'every branch full coverage')
    need(vectors_checked==1373 and len(originals)==266,'full census/preliminary coverage')
    cat=json.loads((original/'pass18-hub-friend-catalogue.json').read_bytes())
    nativeprojection=Counter()
    for r in cat['records']:
        key=(mapping[r['type_id']],r['HHH_covered_mask'],tuple(r['hub_deficits']),tuple(r['low_sat_friend_degrees']))
        nativeprojection[key]+=r['frequency']
    wanted={mapping[i] for i in cat['relevant_type_ids']}
    oursprojection=Counter({(key[0],key[1],tuple(key[2]),tuple(key[3])):n
                            for key,n in physical['signatures'] if key[0] in wanted})
    need(oursprojection==nativeprojection,'all projected physical signature frequencies')
    options={tuple(k):tuple(tuple(x)for x in v) for k,v in physical['options']}
    record=json.loads((original/'pass20-full-T2-N-producer.json').read_bytes())
    labelled,normal=carriers();normal={(m,l):(d,t)for m,l,d,t in normal}
    nativecarriers=record['canonical_carriers'];admissible={};macro=Counter()
    for i,c in enumerate(nativecarriers):
        mask=c['global_HHH_mask'];lams=tuple(c['lambda6']);d=tuple(c['D4'])
        t=tuple(sum(set(pair)<=set(TRIPLES[j])for j in range(4)if mask>>j&1)for pair in PAIRS)
        if any(l<x for l,x in zip(lams,t)):macro[i]='actual_distinct_HHH_owners'
        elif d[0]>12 or any(d[0]+d[a]>16 for a in (1,2,3)) or any(not 8<=d[a]+d[b]<=13 for a,b in combinations((1,2,3),2)):
            macro[i]='complementary_pair_role_bounds'
        else:
            need((mask,lams) in normal and normal[mask,lams]==(d,t),'entire independently reduced carrier')
            admissible[i]=(mask,lams,d,t)
    need(len(admissible)==len(normal)==405,'native admissible exactly independent405')
    exact=subset=strict=checked=0;stream=hashlib.sha256();used=set()
    for rec,(b,v) in zip(record['records'],originals):
        need(rec['branch']==[b['Q'],2,b['X'],b['tau']],'ordered preliminary branch')
        need(rec['K']==b['K'] and len(rec['carrier_results'])==696,'complete native carrier rows')
        used.update(i for i,n in enumerate(v)if n)
        cache={}
        for nr in rec['carrier_results']:
            i=nr['carrier_index'];checked+=1
            need(not nr['coupled_N4'],'native coupled relaxation empty')
            if i in macro:
                need(nr['first_failure']==macro[i] and nr['coordinate_N_sets']==[],'entire native macro failure')
                continue
            mask,lams,d,t=admissible[i]
            ns=[]
            for a in range(4):
                key=(mask,a,d[a])
                if key not in cache:cache[key]=column_choices(v,options,mask,a,d[a])
                ns.append(cache[key])
            need(len(nr['coordinate_N_sets'])==4,'all native coordinates present')
            for nsmall,nlarge in zip(nr['coordinate_N_sets'],ns):
                need(set(nsmall)<=set(nlarge),'native zero-filter coordinate contained in independent relaxation')
                subset+=1;exact+=tuple(nsmall)==nlarge;strict+=tuple(nsmall)!=nlarge
            need(not joint(ns,b['K'],lams,t),'larger independent coupled relaxation empty')
            stream.update(encoded([rec['survivor_ordinal'],i,nr['coordinate_N_sets'],ns,nr['first_failure']]))
    need(len(record['records'])==266 and checked==185136,'every native record checked')
    need(used<=wanted,'all28 preliminary types covered by catalogue')
    return {'raw_rows':426,'semantic_types':60,'branches':35,'vectors':vectors_checked,'preliminary':266,
            'native_catalogue_records':len(cat['records']),'projected_signature_keys':len(nativeprojection),
            'selected_actual_marks':cat['relevant_actual_marks'],'light_role_bijections':cat['light_role_bijections'],
            'needed_types':len(used),'native_carriers':696,'independent_reduced_carriers':405,
            'all_native_records':checked,'coordinate_subset_checks':subset,'coordinate_exact':exact,
            'coordinate_strict':strict,'complete_comparison_sha256':stream.hexdigest(),
            'native_whole_sha256':hashlib.sha256((native/'MATHEMATICAL.json').read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--own',type=Path,required=True);p.add_argument('--physical',type=Path,required=True);p.add_argument('--native',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    z=compare(json.loads(a.own.read_bytes()),json.loads(a.physical.read_bytes()),a.native);a.out.write_bytes(encoded(z));print(json.dumps(z,sort_keys=True))
