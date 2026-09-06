#!/usr/bin/env python3
"""Fresh reconstruction; second DRAT replay or standalone literal witness inspection."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import shutil
import time
import audit
import controls
import generate as gen
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True);p.add_argument('--replay-seconds',type=int,default=300);a=p.parse_args()
    work=a.work.resolve();gen.need(not work.exists() and not work.is_relative_to(gen.ROOT.parent),'fresh external directory')
    old=json.loads((a.source_work/'result.json').read_text());gen.need(old['complete'] and old['contract']['sources']==run.sources(),'complete frozen source')
    gen.need(old['contract']['drat_trim']==gen.info(a.drat_trim),'same proof checker')
    start=time.monotonic();prep=run.prepare(work);gen.need(prep==old['preparation'],'fresh preparation');cases=gen.cases();rows=[]
    gen.need([c['index'] for c in cases]==[c['index'] for c in old['cases']],'six-case coverage')
    def one(pair):
        case,saved=pair;gen.need(all(case[k]==saved[k] for k in case),'case identity');key='c'+str(case['index']);cnf=work/(key+'.cnf')
        row=dict(case,status=saved['status'],formula=gen.write(cnf,case),audit=audit.check_formula(cnf,case))
        gen.need(row['formula']==saved['formula'] and row['audit']==saved['audit'],'fresh exact formula')
        proof=a.source_work/(key+'.drat');gen.need(gen.info(proof)==saved['trace'],'trace identity')
        if saved['status']=='local_excluded':
            gen.need(saved['solver_code']==20,'UNSAT code');row['replay']=run.replay(a.drat_trim,cnf,proof,work/(key+'.replay.log'),a.replay_seconds)
            gen.need(row['replay']['rat_core_lemmas']==saved['replay']['rat_core_lemmas'],'RAT counts')
        elif saved['status']=='local_witness':
            edges=work/(key+'.edges');shutil.copyfile(a.source_work/(key+'.edges'),edges)
            row.update(graph=audit.check_graph(edges,case),edge_file=gen.info(edges),graph_controls=controls.graph_controls(edges,case,work/(key+'_controls')))
            gen.need(all(row[k]==saved[k] for k in ('graph','edge_file','graph_controls')),'literal witness and corruption checks')
        else:
            gen.need(saved['status']=='unknown' and saved['solver_code']==0 and 's UNKNOWN' in (a.source_work/(key+'.solve.log')).read_text(),'saved UNKNOWN')
        run.atomic(work/(key+'.json'),row);return row
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,pair) for pair in zip(cases,old['cases'])]):
            row=future.result();rows.append(row);print('PASS '+str(row['index'])+' '+row['status'],flush=True)
    answer=dict(verified=True,preparation=prep,cases=sorted(rows,key=lambda c:c['index']),
                formulas_rebuilt=6,second_full_proof_replays=sum(c['status']=='local_excluded' for c in rows),
                literal_witness_checks=sum(c['status']=='local_witness' for c in rows),elapsed_seconds=round(time.monotonic()-start,6))
    gen.need(run.sources()==old['contract']['sources'],'source drift');run.atomic(work/'verification.json',answer)
    print('FINISHED '+json.dumps({k:answer[k] for k in ('verified','formulas_rebuilt','second_full_proof_replays','literal_witness_checks','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
