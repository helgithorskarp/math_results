"""The one preauthorized full-colouring decision for the attaining screen model."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def need(ok,why):
    if not ok:raise ValueError(why)


def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--screen',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--kissat',default='/scratch/researcher3-kissat/build/kissat');ap.add_argument('--drat-trim',default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    old=load(REPO/'hadwiger_nelson_heule560_global_decision/build.py','old_global')
    _,m,optional,right,edges,q,states,full=old.prepare()
    screen=json.loads(args.screen.read_text());chosen=set(screen['witness']['selected_optional'])|{310,393,578}
    need(len(chosen)<=16,'target cardinality')
    base,colour,selectors,top=old.formula(optional,right,edges,q,states,full)
    base.extend([[selectors[v] if v in chosen else -selectors[v]] for v in optional])
    raw=old.dimacs(base,top);cnf=args.out/'candidate.cnf';cnf.write_bytes(raw);proof=args.out/'candidate.drat'
    logpath=args.out/'kissat.log'
    with logpath.open('wb') as log:
        result=subprocess.run([args.kissat,'--seed=0','--conflicts=2000000','--time=30',str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT,timeout=45,preexec_fn=old.limits)
    report={'native_returncode':result.returncode,'cnf_sha256':old.sha(raw),'variables':top,'clauses':len(base),'selected_optional':sorted(chosen),'vertices':len(m|chosen),'record_improvement':False}
    if result.returncode==10:
        values={}
        for line in logpath.read_text().splitlines():
            if line.startswith('v '):
                for x in map(int,line.split()[1:]):
                    if x:values[abs(x)]=x>0
        need(set(values)==set(range(1,top+1)),'complete native model')
        need(all(any(values[abs(l)]==(l>0) for l in cl) for cl in base),'native clauses')
        cs={}
        for v in (m|chosen)&set(right):
            colours=[c for c in range(4) if values[colour(v,c)]];need(len(colours)==1,'one colour');cs[v]=str(colours[0])
        state=''.join(cs[v] for v in q);need(state in full,'P20 word')
        parent=json.loads((REPO/'hadwiger_nelson_heule560_separator/certificate.json').read_text())['blocks']['full']
        row=next(r for r in parent['states'] if r['state']==state)
        left={v:c for v,c in zip(parent['vertices'],row['colouring']) if v in m|chosen}
        need(all(left[v]==cs[v] for v in q),'boundary match');left.update(cs);cs=left
        need(set(cs)==m|chosen,'full support')
        _,host_edges,_=old.B.geometry();es=[(a,b) for a,b in host_edges if a in cs and b in cs]
        need(all(cs[a]!=cs[b] for a,b in es),'all exact unit edges')
        report.update(status='FOUR_COLOURABLE',unit_edges=len(es),q_state=state,
                      colouring=''.join(cs.get(v,'.') for v in range(632)))
    elif result.returncode==20:
        with (args.out/'drat.log').open('wb') as log:
            r=subprocess.run([args.drat_trim,str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT,timeout=200,preexec_fn=old.limits)
        need(r.returncode==0 and b's VERIFIED' in (args.out/'drat.log').read_bytes().splitlines(),'candidate negative proof')
        report.update(status='CHECKED_TARGET_OBSTRUCTION_REQUIRES_FINAL_AUDIT',proof_sha256=old.sha(proof.read_bytes()))
    else:report['status']='UNKNOWN'
    (args.out/'result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
