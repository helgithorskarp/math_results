#!/usr/bin/env python3
"""Fresh complete reconstruction and second full proof replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import time
import anchor
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--replay-seconds',type=int,default=300);a=p.parse_args()
    work=a.work.resolve();anchor.require(not work.exists() and not work.is_relative_to(anchor.ROOT.parent),'fresh external work')
    old=json.loads((a.source_work/'result.json').read_text())
    anchor.require(old['complete'] and old['contract']['sources']==run.sources(),'complete source and no drift')
    anchor.require(old['contract']['drat_trim']==anchor.info(a.drat_trim),'checker changed')
    start=time.monotonic();prep=run.prepare(work)
    anchor.require(prep==old['preparation'],'entrywise fresh reconstruction')
    anchor.require([{k:r[k] for k in ('id','type','bits')} for r in old['cases']]==anchor.cases(),'complete two-case coverage')
    rows=[]
    def one(saved):
        key=saved['id'];proof=a.source_work/(key+'.drat');cnf=work/(key+'.cnf')
        anchor.require(anchor.info(proof)==saved['proof'] and anchor.info(cnf)==saved['formula'],'trace/formula identity')
        row={k:saved[k] for k in ('id','type','bits','status','formula')}
        if saved['status']=='excluded':
            anchor.require(saved['solver_code']==20,'UNSAT exit');row['replay']=run.replay(a.drat_trim,cnf,proof,work/(key+'.replay.log'),a.replay_seconds)
        else:anchor.require(saved['status']=='open' and saved['solver_code']==0 and 's UNKNOWN' in (a.source_work/(key+'.solve.log')).read_text(),'saved UNKNOWN')
        run.atomic(work/(key+'.json'),row);return row
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,row) for row in old['cases']]):
            row=future.result();rows.append(row);print('PASS '+row['id']+' '+row['status'],flush=True)
    answer=dict(verified=True,complete_formula_reconstructions=2,preparation=prep,cases=sorted(rows,key=lambda r:r['id']),
        proof_replays=sum(r['status']=='excluded' for r in rows),elapsed_seconds=round(time.monotonic()-start,6))
    run.atomic(work/'verification.json',answer);print('FINISHED '+json.dumps({k:answer[k] for k in ('verified','proof_replays','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
