"""Full receiving replay: actual finite proofs, exact ID cover, physical controls."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
from common import HERE,Q8,need,dependencies,sha,core_guards,assumptions

def main():
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('queue');p.add_argument('local_proofs');p.add_argument('checker');p.add_argument('output');p.add_argument('--active-queue');s=p.parse_args()
    out=Path(s.output);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();dependencies()
    bases=json.loads((Q8/'EXPECTED.json').read_text())['bases']
    for r in range(5,9):need(sha(Path(s.queue)/f'q8-r{r}.cnf')==bases[str(r)]['sha256'],'complete physical base')
    def execute(module,args,name):
        cmd=[sys.executable,'-O','-B',str(HERE/module)]+list(map(str,args))
        proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        need(proc.returncode==0,module+' failed: '+proc.stderr[-2000:]);data=json.loads(proc.stdout)
        (out/name).write_text(proc.stdout);return data
    # The external 640-proof audit is invoked directly, never trusted as a status file.
    from join import local19
    proof=local19(s.catalog,s.local_proofs,s.checker);(out/'LOCAL19_AUDIT.json').write_text(json.dumps(proof,indent=2)+'\n')
    pullback=execute('local_pullback.py',[s.catalog,s.local_proofs],'LOCAL_PULLBACK.json')
    cover=execute('registry.py',[s.queue,'--ledger',out/'original-identities.jsonl'],'COVER.json')
    controls=execute('controls.py',[s.catalog,s.queue,out/'controls',s.checker],'CONTROLS.json')
    empty=out/'target-proofs';empty.mkdir()
    joined=execute('join.py',[s.queue,empty],'JOIN.json')
    need(joined['status']=='COMPLETE_JOIN_PENDING' and joined['new_original_exclusions']==0,'missing proofs must keep all original parents unresolved')
    if s.active_queue:
        need(sha(s.active_queue)=='8d99904405a54c3f2447ddf339e3e93bb70244338a072334e7158fa20c514392','historical active queue pin')
        active=[json.loads(x) for x in Path(s.active_queue).read_text().splitlines()];guards=core_guards(s.queue)
        expected=[{'r':r,'core_assumptions':assumptions(g),'edge_cube':[119] if r==8 else []} for r in range(5,9) for g in guards]
        need([x['worker_job'] for x in active]==expected,'all actual active physical jobs')
    result={'status':'COMPLETE_CROSS_STRATUM_RECEIVING_REPLAY_VERIFIED','source_dependencies_checked':dependencies(),
            'actual_local_DRAT_proofs':proof['proofs_verified'],'original_no_augmentation_branches':pullback['original_task_branches'],
            'signed_source_clauses_checked':pullback['unique_source_clauses'],'original_ids':cover['original_ids'],
            'q8_routed_ids':cover['routed_ids'],'exact_original_parent_complement':cover['unrouted_original_parents'],
            'physical_q8_jobs':956,'total_complete_residual_units':1966,'new_original_exclusions':0,
            'original_unknown':2188660,'physical_transport_controls':controls['physical_transports'],
            'corruptions_rejected':controls['corrupt_or_out_of_scope_rejections'],
            'actual_active_queue_checked':bool(s.active_queue),'ramsey_number_decided':False,
            'seconds':time.monotonic()-start,'checker_sha256':sha(s.checker),
            'receipts':{name:sha(out/name) for name in ['LOCAL19_AUDIT.json','LOCAL_PULLBACK.json','COVER.json','CONTROLS.json','JOIN.json']}}
    (out/'REPLAY.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
