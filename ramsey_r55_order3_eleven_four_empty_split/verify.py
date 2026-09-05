#!/usr/bin/env python3
"""Fresh reconstruction of all complete split formulas and second proof replays."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import time
import audit
import cube
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True);p.add_argument('--replay-seconds',type=int,default=300);a=p.parse_args()
    work=a.work.resolve();cube.require(not work.exists() and not work.is_relative_to(cube.ROOT.parent),'fresh external work')
    old=json.loads((a.source_work/'result.json').read_text())
    cube.require(old['complete'] and old['contract']['sources']==run.sources(),'complete source and no drift');cube.require(old['contract']['drat_trim']==cube.info(a.drat_trim),'proof checker changed')
    start=time.monotonic();prep=run.prepare(work);cases=cube.cases();rows=[]
    cube.require(prep['parent']==old['preparation']['parent'] and prep['bases']==old['preparation']['bases'],'fresh parent/base mismatch')
    cube.require([r['id'] for r in old['cases']]==[c['id'] for c in cases],'complete eight-case coverage')
    def one(pair):
        case,saved=pair;key=case['id'];cube.require(all(case[k]==saved[k] for k in case),'saved case identity')
        base=work/f"base{case['index']}.cnf";cnf=work/(key+'.cnf');proof=a.source_work/(key+'.drat')
        formula=cube.make(base,cnf,case['branch']);checked=audit.check(base,cnf,case['branch'])
        cube.require(formula==saved['formula'] and checked==saved['audit'] and cube.info(proof)==saved['proof'],'formula/audit/trace mismatch')
        row=dict(case,status=saved['status'],formula=formula,entire_formula_audited=True)
        if saved['status']=='excluded':
            cube.require(saved['solver_code']==20,'source UNSAT code');row['replay']=run.replay(a.drat_trim,cnf,proof,work/(key+'.replay.log'),a.replay_seconds)
        else:
            cube.require(saved['status']=='open' and saved['solver_code']==0 and 's UNKNOWN' in (a.source_work/(key+'.solve.log')).read_text(),'source UNKNOWN')
        run.atomic(work/(key+'.json'),row);return row
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,pair) for pair in zip(cases,old['cases'])]):
            row=future.result();rows.append(row);print('PASS '+row['id']+' '+row['status'],flush=True)
    result=dict(verified=True,complete_base_reconstructions=4,complete_cube_reconstructions=8,preparation=prep,cases=sorted(rows,key=lambda r:r['id']),proof_replays=sum(r['status']=='excluded' for r in rows),excluded=sorted(r['id'] for r in rows if r['status']=='excluded'),open=sorted(r['id'] for r in rows if r['status']=='open'),elapsed_seconds=round(time.monotonic()-start,6))
    cube.require(result['excluded']==old['excluded'] and result['open']==old['open'],'summary mismatch');run.atomic(work/'verification.json',result)
    print('FINISHED '+json.dumps({k:result[k] for k in ('excluded','open','proof_replays','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
