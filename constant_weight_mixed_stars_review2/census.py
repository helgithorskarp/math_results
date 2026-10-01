"""Bounded, resumable independent mixed and double-row census driver."""
from pathlib import Path
from itertools import combinations
import argparse,json,time,resource
from exact import insist, encoded
from first import digest, run_native, transport, leave
from hashlib import sha256
import carrier


def save(p,value):
    q=p.with_suffix(p.suffix+'.tmp');q.write_bytes(encoded(value));q.replace(p)


def proof_sources():
    base=Path(__file__).resolve().parent
    return {name:sha256((base/name).read_bytes()).hexdigest()
            for name in ('census.py','carrier.py','first.py','exact.py','partition.cpp')}


def run(args):
    first=json.loads((args.work/'first.json').read_text())
    template=tuple(first['templates'][args.shape]);group=tuple(map(tuple,first['groups'][args.shape]))
    base=carrier.baseline(template)
    cp=carrier.c_orbits(group)
    definition={'shape':args.shape,'template':template,'triples':base['triples'],'candidates':base['candidates'],'groups':group,'c_reps':[q for q,_,_ in cp]}
    fingerprint=digest(definition)
    published=json.loads((args.target/'expected.json').read_text())['shapes'][[0,2].index(args.shape)]
    insist(fingerprint==published['definition_sha256'],'mixed definition differs from pinned source')
    reference=None
    if args.reference:
        original=json.loads((args.reference/f'census_s{args.shape}.json').read_text())
        keys=['c_index','c','p','c_orbit_size','stabilizer_order','raw_h','h_orbits','raw_h_sha256','h_representatives_sha256',
              'native_nodes','native_max_nodes','covers','output_cover_batch_sha256s','positives']
        insist(digest([{k:q[k] for k in keys} for q in original['completed_models']])==published['production_record_sha256'],'reference model records not authenticated by public source')
        reference=original['completed_models']
    path=args.work/f'mixed_s{args.shape}.json'
    state=json.loads(path.read_text()) if path.exists() else {'agent':'six-reviewer-2','role':'independent mathematical reviewer','shape':args.shape,'definition_sha256':fingerprint,'status':'INCOMPLETE independent mixed census','models':[],'proof_sources':proof_sources()}
    insist(state['definition_sha256']==fingerprint,'resume definition changed')
    insist(state.get('proof_sources')==proof_sources(),'resume proof source changed or unbound; use a fresh work directory')
    completed={v['c_index']:v for v in state['models']}
    pair_list=tuple(combinations(range(16),2))
    new=0
    for ci,(c,weight,stabilizer) in enumerate(cp):
        if ci in completed:continue
        if new>=args.max_models:break
        started=time.monotonic()
        domain,graph_metrics=carrier.mixed_graphs(base,c)
        reps=carrier.leave_orbits(domain,stabilizer)
        raw_hash,rep_hash=digest(domain),digest(reps)
        if reference is not None:
            old=reference[ci]
            insist(old['c_index']==ci and tuple(old['c'])==c and old['raw_h_sha256']==raw_hash and old['h_representatives_sha256']==rep_hash,'entrywise reference domain differs')
        positive=[];states=0;max_states=0;hashes=[]
        for low in range(0,len(reps),512):
            batch=reps[low:low+512]
            exclusions=[frozenset((a-1,b-1) for a,b in set(g)|base['common_pairs']) for g in batch]
            records=run_native(args.work,16,tuple(sorted(w>>1 for w in base['candidates'])),exclusions)
            covers=[[list(w<<1 for w in cov) for cov in row['covers']] for row in records]
            hashes.append(digest(covers))
            if reference is not None:insist(hashes[-1]==reference[ci]['output_cover_batch_sha256s'][low//512],'entrywise complete native cover outputs differ')
            for offset,(g,row,solutions) in enumerate(zip(batch,records,covers)):
                states+=row['states'];max_states=max(max_states,row['states'])
                for cov in solutions:
                    star=carrier.second(template,base,cov,g,[1,1,1,2])
                    actual_c=tuple(z for z in range(1,17) if sum(w>>z&1 for w in star)==4)
                    insist(actual_c==c,'positive C marking')
                    positive.append({'h_index':low+offset,'cover':cov,'star':star})
            save(args.work/f'mixed_s{args.shape}_progress.json',{'status':'INCOMPLETE C model','c_index':ci,'complete_fibers':low+len(batch),'total_fibers':len(reps)})
        if reference is not None:insist(encoded(positive)==encoded(reference[ci]['positives']),'entrywise positive words differ')
        t=frozenset(z for q in base['triples'] for z in q)
        record={'c_index':ci,'c':c,'p':len(set(c)&t),'c_orbit_size':weight,'stabilizer_order':len(stabilizer),'raw_h':len(domain),'h_orbits':len(reps),
                'raw_h_sha256':raw_hash,'h_representatives_sha256':rep_hash,'states':states,'max_states':max_states,'covers':len(positive),
                'output_cover_batch_sha256s':hashes,'positives':positive,'graph_metrics':graph_metrics,'seconds':time.monotonic()-started}
        completed[ci]=record;new+=1
        state['models']=[completed[k] for k in sorted(completed)]
        state['status']='COMPLETE independent mixed census' if len(completed)==len(cp) else 'INCOMPLETE independent mixed census'
        state['maxrss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        state['comparison_reference_optional']=reference is not None
        save(path,state)
        print(json.dumps({k:v for k,v in record.items() if k not in ('output_cover_batch_sha256s','positives','graph_metrics')},sort_keys=True),flush=True)
    print(json.dumps({'shape':args.shape,'status':state['status'],'models':len(completed),'total':len(cp),'fibers':sum(q['h_orbits'] for q in completed.values()),'new_models':new}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--target',type=Path,required=True)
    p.add_argument('--shape',type=int,choices=(0,2),required=True);p.add_argument('--max-models',type=int,default=1000)
    p.add_argument('--reference',type=Path)
    a=p.parse_args();insist(a.max_models>0,'positive model count');run(a)
