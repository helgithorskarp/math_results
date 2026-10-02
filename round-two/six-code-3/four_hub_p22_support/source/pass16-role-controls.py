"""PRIVATE actual witness transports, all light-role maps, semantic damage."""
import importlib.util
import itertools
import json
from pathlib import Path

ROOT=Path('round-two/six-code-3');S=ROOT/'scratch'
spec=importlib.util.spec_from_file_location('screen_check',S/'pass16-check-low-friends.py')
screen=importlib.util.module_from_spec(spec);spec.loader.exec_module(screen)
PAIR=list(itertools.combinations(range(4),2))
TRIPLE=list(itertools.combinations(range(4),3))

def need(c,m):
    if not c:raise ValueError(m)

def signature(r):
    return (r['type_id'],tuple(r['hub_deficits']),r['HH_leave_mask'],r['HHH_covered_mask'],tuple(r['word_hub_counts']),r['eligible_hub_mask'])

def transform(r,permutation):
    return (r['type_id'],tuple(r['hub_deficits'][p] for p in permutation),
            sum(1<<i for i,t in enumerate(PAIR) if r['HH_leave_mask']>>PAIR.index(tuple(sorted(permutation[p] for p in t)))&1),
            sum(1<<i for i,t in enumerate(TRIPLE) if r['HHH_covered_mask']>>TRIPLE.index(tuple(sorted(permutation[p] for p in t)))&1),
            tuple(r['word_hub_counts']),sum(1<<i for i,p in enumerate(permutation) if r['eligible_hub_mask']>>p&1))

def witness_signature(blocks,fi,roles,types):
    need(len(roles)==len(set(roles))==4,'four distinct physical hub roles')
    delta,high,low,friend,rows=screen.compile_one(blocks,fi)
    H=set(roles);row=rows[tuple(p for p in high if p in H)]
    ids={screen.key(r):i for i,r in enumerate(types)}
    pointpairs={tuple(sorted(p)) for block in blocks for p in itertools.combinations(block,2)}
    blocksets=[set(b) for b in blocks]
    d=tuple(delta[p] for p in roles)
    hh=sum(1<<i for i,(a,b) in enumerate(PAIR) if tuple(sorted((roles[a],roles[b]))) not in pointpairs)
    hhh=sum(1<<i for i,t in enumerate(TRIPLE) if any({roles[a] for a in t}<=b for b in blocksets))
    b=tuple(sum(len(q&H)==j for q in blocksets) for j in range(5))
    eligible=sum(1<<i for i,p in enumerate(roles) if p in high and all(tuple(sorted((p,v))) in pointpairs for v in high if v!=p))
    return ids[screen.key(row)],d,hh,hhh,b,eligible

def main():
    data=json.loads((ROOT/'four_hub_p21_endpoint_cut/fixtures.json').read_text())
    types=json.loads((ROOT/'four_hub_p21_endpoint_cut/expected.json').read_text())['types']
    catalog=json.loads((S/'pass16-hub-role-catalogue.json').read_text())['records']
    table={signature(r):r for r in catalog}
    role_transports=0;actual_transports=0
    for r in catalog:
        t=types[r['type_id']]
        need(sum(r['hub_deficits'])==t['hub_weight'],'hub mass projection')
        need(bool(r['eligible_hub_mask'])==t['eligible'],'actual isolated hub eligibility')
        b=r['word_hub_counts'];L=r['HH_leave_mask'].bit_count()
        need(sum(b)==20 and b[2]+3*b[3]+6*b[4]+L==6,'actual HH pair ownership')
        need(r['HHH_covered_mask'].bit_count()==b[3]+4*b[4],'actual HHH coverage')
        need(sum(j*b[j] for j in range(5))==20-t['hub_weight'],'actual hub replications')
        for light_map in itertools.permutations((1,2,3)):
            transported=transform(r,(0,)+light_map)
            need(transported in table and table[transported]['frequency']==r['frequency'],'full light-role bijection/frequency symmetry')
            role_transports+=1
        witness=r['witness'];fi=witness['fixture'];roles=witness['hub_roles']
        for pmap in (tuple((p+5)%17 for p in range(17)),tuple((3*p+2)%17 for p in range(17))):
            need(len(set(pmap))==17,'actual point bijection')
            blocks=[[pmap[p] for p in q] for q in data['stars'][fi]]
            newroles=[pmap[p] for p in roles]
            need(witness_signature(blocks,fi,newroles,types)==signature(r),'actual transported witness signature')
            actual_transports+=1
    # Damage compares physical meaning before any frozen expected-output check.
    first=catalog[0];w=first['witness'];correct=witness_signature(data['stars'][w['fixture']],w['fixture'],w['hub_roles'],types)
    damages=0
    for field in ('hub_deficits','HH_leave_mask','HHH_covered_mask','eligible_hub_mask'):
        changed=dict(first)
        if field=='hub_deficits':changed[field]=list(first[field]);changed[field][0]+=1
        else:changed[field]^=1
        need(signature(changed)!=correct,'semantic signature damage passed')
        damages+=1
    badroles=list(w['hub_roles']);badroles[1]=badroles[0]
    try:witness_signature(data['stars'][w['fixture']],w['fixture'],badroles,types)
    except ValueError:damages+=1
    else:raise ValueError('repeated literal hub role accepted')
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_PHYSICAL_CATALOGUE_CONTROLS_PASS',
                all_signatures=837,all_light_role_transports=role_transports,actual_witness_point_transports=actual_transports,
                semantic_damages_rejected=damages,frequency_caps_global_centers=False,new_pair_total_claim=None)
    out=S/'pass16-role-controls.json';need(not out.exists(),'fresh controls output')
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
