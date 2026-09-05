#!/usr/bin/env python3
"""Fresh full reconstruction of all19 formulas and second proof replay."""
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
    cases=cube.cases();cube.require([r['index'] for r in old['cases']]==[c['index'] for c in cases],'complete19-case coverage');rows=[]
    def one(pair):
        case,saved=pair;key=f"c{case['index']}";cube.require(all(case[k]==saved[k] for k in case if k!='formula') and case['formula']==saved['base'],'case identity')
        rebuilt=run.make_case(work,case)
        cube.require(all(rebuilt[k]==saved[k] for k in rebuilt),'fresh complete base/formula/audit differs')
        proof=a.source_work/(key+'.drat');cube.require(cube.info(proof)==saved['proof'],'trace identity')
        row=dict({k:v for k,v in case.items() if k!='formula'},base=case['formula'],status=saved['status'],**rebuilt)
        if saved['status']=='excluded':
            cube.require(saved['solver_code']==20,'UNSAT exit');row['replay']=run.replay(a.drat_trim,work/(key+'.cnf'),proof,work/(key+'.replay.log'),a.replay_seconds)
        else:cube.require(saved['status']=='open' and saved['solver_code']==0 and 's UNKNOWN' in (a.source_work/(key+'.solve.log')).read_text(),'saved UNKNOWN')
        run.atomic(work/(key+'.json'),row);return row
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,pair) for pair in zip(cases,old['cases'])]):
            row=future.result();rows.append(row);print('PASS '+str(row['index'])+' '+row['status'],flush=True)
    answer=dict(verified=True,complete_base_reconstructions=25,complete_formula_reconstructions=19,preparation=prep,
        cases=sorted(rows,key=lambda r:r['index']),proof_replays=sum(r['status']=='excluded' for r in rows),
        excluded=sorted(r['index'] for r in rows if r['status']=='excluded'),open=sorted(r['index'] for r in rows if r['status']=='open'),
        elapsed_seconds=round(time.monotonic()-start,6))
    cube.require(answer['excluded']==old['excluded'] and answer['open']==old['open'],'summary differs')
    run.atomic(work/'verification.json',answer)
    print('FINISHED '+json.dumps({k:answer[k] for k in ('verified','proof_replays','excluded','open','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
