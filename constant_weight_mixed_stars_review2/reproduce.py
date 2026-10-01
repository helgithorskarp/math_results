"""Complete serial independent review, with source-bound mixed-census resume."""
from pathlib import Path
from types import SimpleNamespace
from itertools import combinations
from hashlib import sha256
import argparse,json,subprocess,time,resource
import first,carrier,census,double,residual
from exact import insist,encoded,packing


def controls(work):
    source=Path(__file__).with_name('partition.cpp')
    result=first.run_native(work,4,(15,),[frozenset()],'positive-control')[0]
    insist(result['covers']==[[15]],'native genuine positive fixture')
    inp,out=work/'positive-control.input',work/'guard-control.jsonl'
    p=subprocess.run([str(work/'partition'),str(inp),str(out),'0'],capture_output=True,text=True,timeout=15)
    insist(p.returncode!=0 and 'INCOMPLETE' in p.stderr,'native zero guard must report incomplete')
    failures=0
    for text in ('17 0 0\n','4 1 0\n7\n','4 1 1\n15\n0 2 0 0\n','4 1 1\n15\n0 1 6\n'):
        inp.write_text(text)
        p=subprocess.run([str(work/'partition'),str(inp),str(out)],capture_output=True,text=True,timeout=15)
        insist(p.returncode!=0,'native malformed input accepted');failures+=1
    return {'genuine_native_four_point_cover':True,'native_zero_guard_incomplete':True,'native_invalid_inputs_rejected':failures,'kernel_sha256':sha256(source.read_bytes()).hexdigest()}


def baseline(classification):
    raw=(classification/'acl69.txt').read_bytes();words=[int(w,2) for w in raw.splitlines()]
    packing(words,size=69)
    centers=[]
    for x in range(18):
        if sum(w>>x&1 for w in words)!=20:continue
        deficits={y:5-sum((w>>x&1)!=0 and (w>>y&1)!=0 for w in words) for y in range(18) if y!=x}
        if sorted(v for v in deficits.values() if v)==[1,2,2]:
            centers.append({'point':x,'deficit_two_neighbors':[{'point':y,'replication':sum(w>>y&1 for w in words)} for y in sorted(deficits) if deficits[y]==2]})
    insist([c['point'] for c in centers]==[3],'known69 profile control')
    return {'words':69,'sha256':sha256(raw).hexdigest(),'coordinate0':'rightmost printed digit','profile221_centers':centers,'scope':'Known69 shows that a single saturated221 row is possible below72; it is not a new construction.'}


def stable_result(work,classification):
    f=json.loads((work/'first.json').read_text());d=json.loads((work/'double.json').read_text());r=json.loads((work/'residual.json').read_text())
    mixed=[]
    for shape in (0,2):
        j=json.loads((work/f'mixed_s{shape}.json').read_text());m=j['models']
        insist(j['status']=='COMPLETE independent mixed census' and len(m)==(110 if shape==0 else 161),'incomplete mixed domain')
        insist(j['proof_sources']==census.proof_sources(),'cached proof source mismatch')
        insist([q['c_index'] for q in m]==list(range(len(m))) and sum(q['c_orbit_size'] for q in m)==560 and sum(q['c_orbit_size']*q['raw_h'] for q in m)==2118918,'mixed coverage/weight')
        pure_keys=['c_index','c','p','c_orbit_size','stabilizer_order','raw_h','h_orbits','raw_h_sha256','h_representatives_sha256','output_cover_batch_sha256s','positives']
        mixed.append({'shape':shape,'definition_sha256':j['definition_sha256'],'C_orbits':len(m),'fibers':sum(q['h_orbits'] for q in m),'weighted_C_choices':560,'weighted_labeled_leaves':2118918,'cover_counts_by_p':[sum(q['covers'] for q in m if q['p']==p) for p in range(4)],'complete_mathematical_stream_sha256':first.digest([{k:q[k] for k in pure_keys} for q in m]),'native_states':sum(q['states'] for q in m),'max_case_states':max(q['max_states'] for q in m),'carrier_states':sum(q['graph_metrics']['states'] for q in m),'max_carrier_root_states':max(q['graph_metrics']['max_root_states'] for q in m)})
    return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'COMPLETE independent sharp double/mixed bounds and no221-at72 review',
            'first':{k:f[k] for k in ('stats','stars_by_shape','native_nodes','literal_nodes','max_native_case_states')},
            'first_template_sha256':first.digest(f['templates']),'first_group_orders':list(map(len,f['groups'])),'mixed':mixed,
            'double':{'stats':d['stats'],'branch_counts':[len(b['stars']) for b in d['branches']],'actual_second_stars':148,'joint_orbits':31,'star_stream_sha256':first.digest([b['stars'] for b in d['branches']]),'orbit_stream_sha256':first.digest(d['orbits']),'native_states':d['states'],'max_case_states':d['max_case_states']},
            'residual':[{'mode':scope['mode'],'cases':len(scope['cases']),'restricted_upper_bound':scope['restricted_upper_bound'],'complete_case_stream_sha256':first.digest(scope['cases']),'nodes':sum(q['nodes'] for q in scope['cases'])} for scope in r['cases']],
            'residual_controls':r['controls'],'attaining_witnesses':r['witnesses'],'baseline69':baseline(classification),'native_controls':controls(work)}


def run(args):
    started=time.monotonic();args.work.mkdir(parents=True,exist_ok=True)
    manifest=json.loads(Path(__file__).with_name('INPUT.json').read_text())
    for section,path in [('classification_runtime',args.classification),('mixed_runtime',args.target)]:
        for item in manifest[section]:
            insist(sha256((path/item['filename']).read_bytes()).hexdigest()==item['sha256'],'pinned runtime input differs: '+item['filename'])
    source=Path(__file__).resolve().parent
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(source/'partition.cpp'),'-o',str(args.work/'partition')],check=True,timeout=45)
    first.classify(args.work,json.loads((args.classification/'expected.json').read_text()))
    for shape in (0,2):
        census.run(SimpleNamespace(work=args.work,target=args.target,shape=shape,max_models=1000,reference=None))
    double.run(SimpleNamespace(work=args.work,classification=args.classification))
    residual.run(SimpleNamespace(work=args.work,classification=args.classification,target=args.target))
    result=stable_result(args.work,args.classification);raw=encoded(result)
    if args.record:args.expected.write_bytes(raw)
    else:insist(raw==args.expected.read_bytes(),'complete stable expected record differs')
    metrics={'status':result['status'],'expected_sha256':sha256(raw).hexdigest(),'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cold_mixed_census_or_source_bound_complete_resume':'Inspect model logs; completed cached models are skipped only if proof sources and mathematical definitions match.'}
    (args.work/'metrics.json').write_bytes(encoded(metrics));print(json.dumps(metrics,sort_keys=True),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();base=Path(__file__).resolve().parents[1]
    p.add_argument('--work',type=Path,required=True);p.add_argument('--classification',type=Path,default=base/'coding_theory/a18_6_5_double_221_pair')
    p.add_argument('--target',type=Path,default=base/'coding_theory/a18_6_5_no_221_at_72');p.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    p.add_argument('--record',action='store_true',help='Explicitly record a new expected baseline, rather than compare it.')
    run(p.parse_args())
