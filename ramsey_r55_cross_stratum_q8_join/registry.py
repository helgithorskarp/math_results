"""Exact original identities, complete coverage and conditional parent payoffs."""
from pathlib import Path
import argparse,hashlib,json
from common import COUNTS,route_class,REPO,core_guards,assumptions,dependencies,need

def ranges():
    out=[]
    for q in range(7,11):
        for r in range(5,q+1):
            n=COUNTS[q]
            out.append({'q':q,'r':r,'first':f'bo1-q{q}-r{r}-c000000','last':f'bo1-q{q}-r{r}-c{n-1:06d}',
                        'count':n,'route':route_class(q,r)})
    return out

def original_rows():
    excluded=set(json.loads((REPO/'ramsey_r55_q7r5_tail_decisions/TASKS.json').read_text())['excluded_core_indices'])
    for row in ranges():
        q,r=row['q'],row['r']
        for c in range(row['count']):
            yield {'task':f'bo1-q{q}-r{r}-c{c:06d}','q':q,'r':r,'core':c,'route':row['route'],
                   'original_verdict':'INHERITED_CERTIFIED_UNSAT' if q==7 and r==5 and c in excluded else 'UNKNOWN'}

def census(queue,output=None):
    dependencies();guards=core_guards(queue);digest=hashlib.sha256();counts={};excluded=0;total=0
    inherited=json.loads((REPO/'ramsey_r55_maximal_block_order/TASKS.json').read_text())
    need(inherited['format']=='bo1' and inherited['tasks']==2189178 and len(inherited['classes'])==18,'pinned original registry')
    for new,old in zip(ranges(),inherited['classes']):
        need((new['q'],new['r'],new['first'],new['last'],new['count'])==(old['q'],old['r'],old['first_task'],old['last_task'],old['core_stop']) and old['core_start']==0,'exact inherited original range')
    f=Path(output).open('x') if output else None
    try:
        for row in original_rows():
            raw=json.dumps(row,separators=(',',':'))+'\n';digest.update(raw.encode())
            if f:f.write(raw)
            total+=1;counts[row['route']]=counts.get(row['route'],0)+1
            excluded+=row['original_verdict']=='INHERITED_CERTIFIED_UNSAT'
    finally:
        if f:f.close()
    return {'status':'COMPLETE_ORIGINAL_ID_COVER_AUDITED','original_ids':total,'original_id_stream_sha256':digest.hexdigest(),
            'routed_ids':counts['Q8_PHYSICAL'],'unrouted_original_parents':counts['ORIGINAL_PARENT'],
            'additional_non_q8_ids_routed':counts['Q8_PHYSICAL']-4*COUNTS[8],
            'physical_q8_units':4*len(guards),'complete_residual_units':4*len(guards)+counts['ORIGINAL_PARENT'],
            'whole_r_family_conditional_payoffs':{str(r):sum(x['count'] for x in ranges() if x['r']==r and x['route']=='Q8_PHYSICAL') for r in range(5,9)},
            'inherited_original_exclusions':excluded,'original_unknown':total-excluded,'new_original_exclusions':0,
            'ranges':ranges(),'guard_lengths':{str(k):sum(m.bit_count()==k for m,v in guards) for k in (7,8)},
            'guard_boolean_volume':sum(1<<(55-m.bit_count()) for m,v in guards),
            'scope':'Coverage and a conditional proof join. No missing target proof is a task decision.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('queue');p.add_argument('--ledger');s=p.parse_args()
    print(json.dumps(census(s.queue,s.ledger),indent=2,sort_keys=True))
