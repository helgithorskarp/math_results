"""Private exact packed screen: can actual9525 minimum-lock close a function?
Only partner4, exactly one prior HIGH equal merge, all762 complete functions.
Original LOW domains remain distinct. This is not a global sorting exclusion.
"""
import importlib.util
import json
from pathlib import Path
import resource
import time
from collections import Counter

ROOT=Path(__file__).resolve().parent


def need(test,message):
    if not test:raise ValueError(message)


def bins(values,dead,n):
    full=(1<<(1<<n))-1
    result=[]
    for x in range(32):
        value=full
        for j,p in enumerate(dead):
            value &= values[p] if x>>j&1 else full ^ values[p]
        result.append(value)
    need(sum(result)==full,'Pattern bins do not partition whole original cube')
    return result


def compose(column,patterns):
    return sum(patterns[x] for x in range(32) if column>>x&1)


def main():
    start=time.monotonic();deadline=start+45
    p=ROOT/'minimum_packed.py'
    spec=importlib.util.spec_from_file_location('credited_minimum_lock_packed',p)
    gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
    fixture=json.loads((ROOT/'fixture.json').read_text())
    prefix=fixture['B23']+fixture['LOW_suffixes']['4']
    proposal=json.loads((ROOT/'work/low26-fiveport-preparation-partner4.json').read_text())
    domain_masks=[r['original_LOW_mask'] for r in json.loads((ROOT/'work/low26-partner4-activity-pilot.json').read_text())['all39_original_domains']]
    need(len(domain_masks)==39 and len(set(domain_masks))==39,'Original cube list differs')
    original={lo:gen.packed(prefix,lo)[0] for lo in domain_masks}
    full_base=gen.packed(prefix)[0]
    target=sum(1<<x for x in range(8192) if x.bit_count()>=11)
    minimum=1<<2047
    rows=[];counts=Counter();branches=[]
    for branch_id,b in enumerate(proposal['branches']):
        gate=b['HIGH_zero_gate'];dead=b['dead_preparation_ports'];need(dead[0]==2,'Locked port index differs')
        patterns={}
        for lo,values in original.items():
            values=list(values);a,q=gate;values[a],values[q]=values[a]&values[q],values[a]|values[q]
            patterns[lo]=bins(values,dead,11)
        full=list(full_base);a,q=gate;full[a],full[q]=full[a]&full[q],full[a]|full[q]
        global_bins=bins(full,dead,13)
        census=Counter()
        for function_id,f in enumerate(b['functions']):
            need(time.monotonic()<deadline,'Operational45s screen guard; partial output is not an exclusion')
            column=f['full_five_variable_columns'][0]
            domains=[lo for lo in domain_masks if compose(column,patterns[lo])==minimum]
            difference=compose(column,global_bins)^target
            witness=(difference & -difference).bit_length()-1 if difference else None
            status='MINIMUM_LOCK_EXCLUDES_STANDARD_SIZE44' if domains and difference else (
                   'MINIMUM_LOCK_BUT_GLOBAL_ORDER_STATISTIC_CORRECT' if domains else 'NO_SINGLE_D9_MINIMUM_LOCK')
            census[status]+=1;counts[status]+=1
            gates=prefix+[gate]+f['shortest_word']
            if domains:
                actual=gen.packed(gates,domains[0])[1]
                need(actual['outer_record']==[domains[0],0,3,0,9,0,0], 'Selected tight original route or identity count differs')
                need(gen.packed(gates,domains[0])[0][2]==minimum,'Stored function and literal minimum differ')
            if witness is not None:
                value=gen.packed(gates)[0][2]>>witness&1
                need(value!=int(witness.bit_count()>=11),'Literal original full witness does not fail')
            rows.append({'branch_id':branch_id,'function_id':function_id,'HIGH_zero_gate':gate,
                         'shortest_word':f['shortest_word'],'function_columns_sha256':gen.digest(f['full_five_variable_columns']),
                         'original_D9_minimum_masks':domains,'full_Boolean_wrong_statistic_witness':witness,
                         'status':status})
        branches.append({'branch_id':branch_id,'HIGH_zero_gate':gate,'function_count':len(b['functions']),
                         'census':dict(census)})
    need(len(rows)==762,'Complete function screen differs')
    out={'agent':'six-sorting-1','role':'researcher','status':'COMPLETE_PRIVATE_ORIGINAL_DOMAIN_MINIMUM_LOCK_SCREEN',
         'source_commit_for_minimum_lock_theorem':'5650ffcfc66c27f85b8e621d4794083de6be81e9',
         'graph_minimum_lock_theorem':'bafkreievpu3snb6v2yj4n3ghmut6qdl664jgjxqrsj4ayb3lrysp3aqvhq',
         'prefix':prefix,'complete_functions':762,'original_D9_cubes':39,'census':dict(counts),
         'branches':branches,'records':rows,'records_sha256':gen.digest(rows),
         'scope':'Partner4 exactlyONE prior HIGH equal merge; all762 necessary complete five-variable functions. Other prior-merge counts, first-LOW-singleton and unrestricted44..45 remain open.',
         'same_author_producer_only':True,'external_person_review_claimed':False,
         'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/'work/partner4-fiveport-minimum-lock-screen.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','prefix')},sort_keys=True))


if __name__=='__main__':main()
