#!/usr/bin/env python3
"""Fresh full reconstruction, literal audits and second complete proof replays."""
from pathlib import Path
import argparse
import json
import resource
import time
import audit
import generate as gen
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True);p.add_argument('--replay-seconds',type=int,default=300);a=p.parse_args()
    source=a.source_work.resolve();work=a.work.resolve();gen.need(not work.is_relative_to(gen.ROOT.parent) and work!=source,'fresh external path')
    gen.need(not work.exists(),'verification work must be fresh');work.mkdir(parents=True)
    result=json.loads((source/'result.json').read_text());contract=result['contract'];start=time.monotonic()
    gen.need(result['complete'] and result['maximal_branch_excluded'],'two completed refutations required for theorem verification')
    gen.need(run.sources()==contract['sources'],'frozen source contract');gen.need(gen.info(a.drat_trim)==contract['drat_trim'],'checker identity')
    reps=gen.representatives();gen.need(reps==json.loads((source/'representatives.json').read_text()),'exact reconstructed representatives')
    gen.need(gen.boundary()==json.loads((source/'boundary.json').read_text()),'fresh boundary bookkeeping')
    check=audit.check_representatives(reps);gen.need(check==result['representatives'],'entry-level representative verification')
    rows=[]
    for old in result['cases']:
        kind=old['kind'];path=work/(kind+'.cnf');identity=gen.write(path,kind)
        gen.need(identity==old['formula'] and gen.info(source/(kind+'.cnf'))=={k:identity[k] for k in ('bytes','sha256')},'fresh and original full formula identity')
        checked=audit.check_formula(path,kind,reps);gen.need(checked==old['audit'],'fresh independent clauses')
        proof=source/(kind+'.drat');gen.need(gen.info(proof)==old['proof'],'full trace identity')
        replay=run.replay(a.drat_trim,path,proof,work/(kind+'.replay.log'),a.replay_seconds)
        gen.need(replay['rat_core_lemmas']==old['replay']['rat_core_lemmas'],'full replay RAT identity')
        rows.append(dict(kind=kind,formula=identity,audit=checked,proof=old['proof'],replay=replay))
        print('VERIFIED '+kind,flush=True)
    gen.need(run.sources()==contract['sources'],'source drift')
    report=dict(source_result=gen.info(source/'result.json'),representatives=check,cases=rows,maximal_branch_excluded=True,
        new_whole_core_exclusions=[],target_graph=False,all_sources_match=True,elapsed_seconds=round(time.monotonic()-start,6),
        largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    run.atomic(work/'verification.json',report);print('FINISHED '+json.dumps(report),flush=True)


if __name__=='__main__':main()
