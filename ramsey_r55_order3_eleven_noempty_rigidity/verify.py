#!/usr/bin/env python3
"""Fresh reconstruction of the complete cover and fifteen formulas; second replay."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import argparse
import json
import time
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--replay-seconds',type=int,default=300);a=p.parse_args()
    work=a.work.resolve();run.require(not work.exists() and not work.is_relative_to(run.ROOT.parent),'fresh external directory')
    old=json.loads((a.source_work/'result.json').read_text());start=time.monotonic()
    run.require(old['complete'] and old['contract']['sources']==run.sources(),'complete unchanged source')
    run.require(old['contract']['drat_trim']==run.info(a.drat_trim),'unchanged proof checker')
    prep,data=run.prepare(work);run.require(prep==old['preparation'],'fresh preparation differs')
    run.require([r['index'] for r in old['cases']]==list(range(15)),'complete coverage');rows=[]
    def one(pair):
        case,saved=pair;key=f"p{case['index']:02}"
        run.require(all(case[k]==saved[k] for k in case),'case identity')
        rebuilt=run.make_case(work,case);run.require(all(rebuilt[k]==saved[k] for k in rebuilt),'fresh formula/audit differs')
        proof=a.source_work/(key+'.drat');run.require(run.info(proof)==saved['proof'],'trace identity')
        row=dict(case,status=saved['status'],**rebuilt)
        if saved['status']=='excluded':
            run.require(saved['solver_code']==20,'UNSAT exit');row['replay']=run.replay(a.drat_trim,work/(key+'.cnf'),proof,work/(key+'.replay.log'),a.replay_seconds)
        else:run.require(saved['status']=='open' and saved['solver_code']==0 and 's UNKNOWN' in (a.source_work/(key+'.solve.log')).read_text(),'explicit saved UNKNOWN')
        run.atomic(work/(key+'.json'),row);return row
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,pair) for pair in zip(data['cases'],old['cases'])]):
            row=future.result();rows.append(row);print('PASS '+str(row['index'])+' '+row['status'],flush=True)
    answer=dict(verified=True,complete_formula_reconstructions=15,preparation=prep,cases=sorted(rows,key=lambda r:r['index']),
        proof_replays=sum(r['status']=='excluded' for r in rows),excluded=sorted(r['index'] for r in rows if r['status']=='excluded'),
        open=sorted(r['index'] for r in rows if r['status']=='open'),elapsed_seconds=round(time.monotonic()-start,6))
    run.require(answer['excluded']==old['excluded'] and answer['open']==old['open'],'summary differs')
    run.atomic(work/'verification.json',answer);print('FINISHED '+json.dumps({k:answer[k] for k in ('verified','proof_replays','excluded','open','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
