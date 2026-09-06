#!/usr/bin/env python3
"""Fresh independent formula reconstruction and second full terminal-evidence check."""
from pathlib import Path
import argparse
import json
import time
import run


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True);p.add_argument('--replay-seconds',type=int,default=300);a=p.parse_args()
    before=time.monotonic();work=a.work.resolve();source=a.source_work.resolve()
    run.generate.need(not work.is_relative_to(run.ROOT.parent) and work!=source,'separate external verification directory')
    r=json.loads((source/'result.json').read_text())
    run.generate.need(r['complete'] and run.sources()==r['contract']['sources'],'complete run and unchanged sources')
    run.generate.need(run.generate.identity(a.drat_trim)==r['contract']['drat_trim'],'pinned full DRAT checker')
    run.generate.need([x['color'] for x in r['cases']]==['blue','red'],'complete two-case list')
    fresh=run.prepare(work)
    run.generate.need(fresh==r['preparation'],'entire fresh reconstruction matches')
    rows=[];replays=0
    for old in r['cases']:
        color=old['color'];cnf=work/(color+'.cnf');trace=source/(color+'.drat');log=source/(color+'.solve.log')
        run.generate.need(run.generate.identity(cnf)==old['formula'] and run.generate.identity(trace)==old['trace'],'formula and trace identities')
        row=dict(color=color,status=old['status'],formula=old['formula'],trace=old['trace'])
        if old['status']=='excluded':
            run.generate.need(old['solver_code']==20 and old['replay']['verified'],'first complete proof replay')
            row['replay']=run.replay(a.drat_trim,cnf,trace,work/(color+'.replay.log'),a.replay_seconds);replays+=1
        elif old['status']=='open':
            run.generate.need(old['solver_code']==0 and 's UNKNOWN' in log.read_text(),'explicit original UNKNOWN')
        elif old['status']=='target_graph_verified':
            model=run.decode.write(log,work/(color+'.edges'));run.decode.satisfies(model,cnf)
            row['graph']=run.check.graph(work/(color+'.edges'),color)
            run.generate.need(row['graph']==old['graph'],'fresh literal graph check')
        else:raise ValueError('nonterminal bounded case')
        rows.append(row)
    answer=dict(verified=True,preparation=fresh,cases=rows,proof_replays=replays,excluded=r['excluded'],open=r['open'],target_graph=r['target_graph'],seconds=round(time.monotonic()-before,6))
    run.generate.need(run.sources()==r['contract']['sources'],'sources unchanged after verification')
    run.atomic(work/'verification.json',answer)
    print('PASS fresh complete direct formulas and evidence '+json.dumps({k:answer[k] for k in ('excluded','open','target_graph','proof_replays','seconds')}))
