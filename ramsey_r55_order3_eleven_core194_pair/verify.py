#!/usr/bin/env python3
"""Fresh full reconstruction of both full formulas and second proof replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import time
import cube
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--replay-seconds',type=int,default=300);a=p.parse_args()
    work=a.work.resolve();cube.require(not work.exists() and not work.is_relative_to(cube.ROOT.parent),'fresh external directory')
    old=json.loads((a.source_work/'result.json').read_text())
    cube.require(old['complete'] and old['contract']['sources']==run.sources(),'complete source and no drift')
    cube.require(old['contract']['drat_trim']==cube.info(a.drat_trim),'checker changed')
    start=time.monotonic();prep=run.prepare(work);cube.require(prep==old['preparation'],'fresh preparation differs')
    cases=cube.cases();cube.require([r['id'] for r in old['cases']]==[c['id'] for c in cases],'complete two-case coverage');rows=[]
    def one(pair):
        case,saved=pair;key=case['id'];cube.require(all(case[k]==saved[k] for k in case) and cube.BASE==saved['base'],'case identity')
        rebuilt=run.make_case(work,case)
        cube.require(all(rebuilt[k]==saved[k] for k in rebuilt),'fresh complete base/formula/audit differs')
        proof=a.source_work/(key+'.drat');cube.require(cube.info(proof)==saved['proof'],'trace identity')
        row=dict(case,base=cube.BASE,status=saved['status'],**rebuilt)
        if saved['status']=='excluded':
            cube.require(saved['solver_code']==20,'UNSAT exit');row['replay']=run.replay(a.drat_trim,work/(key+'.cnf'),proof,work/(key+'.replay.log'),a.replay_seconds)
        else:cube.require(saved['status']=='open' and saved['solver_code']==0 and 's UNKNOWN' in (a.source_work/(key+'.solve.log')).read_text(),'saved UNKNOWN')
        run.atomic(work/(key+'.json'),row);return row
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,pair) for pair in zip(cases,old['cases'])]):
            row=future.result();rows.append(row);print('PASS '+row['id']+' '+row['status'],flush=True)
    answer=dict(verified=True,complete_base_reconstructions=1,complete_formula_reconstructions=2,preparation=prep,
        cases=sorted(rows,key=lambda r:r['id']),proof_replays=sum(r['status']=='excluded' for r in rows),
        excluded=sorted(r['id'] for r in rows if r['status']=='excluded'),open=sorted(r['id'] for r in rows if r['status']=='open'),
        elapsed_seconds=round(time.monotonic()-start,6))
    cube.require(answer['excluded']==old['excluded'] and answer['open']==old['open'],'summary differs')
    run.atomic(work/'verification.json',answer)
    print('FINISHED '+json.dumps({k:answer[k] for k in ('verified','proof_replays','excluded','open','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
