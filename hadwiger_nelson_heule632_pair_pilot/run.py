#!/usr/bin/env python3
"""Run only the frozen pair pilot, stopping at its first checked obstruction."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import time
import build
import independent
import native

HERE=Path(__file__).resolve().parent


def save(path,value):
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');temp.replace(path)


def run(out,kissat,drat,controls):
    start=time.monotonic();plan=json.loads((HERE/'plan.json').read_text());prep=json.loads((HERE/'preparation.json').read_text())
    build.need(sha256((HERE/'preparation.json').read_bytes()).hexdigest()==plan['preparation_sha256'],'frozen preparation')
    tests=json.loads(controls.read_text());build.need(tests['status']=='ALL ENCODING AND NATIVE CONTROLS VERIFIED' and tests['boolean_assignments']==32768,'controls first')
    build.need(sha256(kissat.read_bytes()).hexdigest()==plan['solver']['sha256'],'frozen solver executable')
    build.need(sha256(drat.read_bytes()).hexdigest()==plan['proof_checker']['sha256'],'frozen checker executable')
    points,edges,large=build.geometry();other,ind_edges,ind_large=independent.geometry()
    build.need(edges==ind_edges and large==ind_large,'entrywise independent geometry')
    build.need(prep==independent.selection(ind_edges,ind_large),'all24 selections and CNFs independently rebuilt before query')
    out.mkdir(parents=True,exist_ok=False);records=[];positive=[];winner=None;upper=None
    for row in prep['selected']:
        i=row['index'];omitted=row['omitted'];vertices=sorted(set(range(632))-set(omitted))
        clauses,raw,vs,tri=build.formula(vertices,edges,4)
        build.need(sha256(raw).hexdigest()==row['cnf_sha256'],'frozen query formula')
        cnf=out/f'{i:02d}.cnf';proof=out/f'{i:02d}.drat';log=out/f'{i:02d}.log';cnf.write_bytes(raw)
        save(out/'checkpoint.json',{'phase':'four-colour query','inflight':i,'completed':records})
        info=native.solve(kissat,cnf,proof,log);record=dict(row,**info)
        if info['status']=='SAT':
            ans=build.decode(log.read_text(),vs,4,clauses);checks=build.check_colouring(ans,vertices,edges,4)
            text=''.join(str(ans[v]) if v in ans else '.' for v in range(632))
            build.need(independent.colouring(text,omitted,ind_edges,4)==checks,'independent positive graph check')
            positive.append({'index':i,'omitted':omitted,'colouring':text});record['edge_checks']=checks
        elif info['status']=='UNSAT':
            record['drat']=native.check_proof(drat,cnf,proof,out/f'{i:02d}.check.log')
            build.need(record['drat']['verified'],'unverified negative result: stop and inspect proof')
            record['status']='UNSAT_VERIFIED';winner=i
        records.append(record);save(out/'records.json',records);save(out/'positive.json',positive)
        print(json.dumps({'index':i,'omitted':omitted,'status':record['status'],'seconds':record['seconds']}),flush=True)
        if winner is not None:
            clauses,raw,vs,tri=build.formula(vertices,edges,5);cnf5=out/'five.cnf';cnf5.write_bytes(raw)
            save(out/'checkpoint.json',{'phase':'conditional five-colour certificate','winner':winner,'completed':records})
            upper=native.solve(kissat,cnf5,out/'five.drat',out/'five.log');upper.update(cnf_sha256=sha256(raw).hexdigest(),cnf_bytes=len(raw),variables=len(vertices)*5,clauses=len(clauses))
            if upper['status']=='SAT':
                ans=build.decode((out/'five.log').read_text(),vs,5,clauses);upper['colouring']=''.join(str(ans[v]) if v in ans else '.' for v in range(632));upper['edge_checks']=independent.colouring(upper['colouring'],omitted,ind_edges,5)
            save(out/'upper.json',upper);break
    counts=Counter(row['status'] for row in records)
    result={'status':'BOUNDED H632 PAIR PILOT COMPLETE','prepared':24,'attempted':len(records),'unattempted':24-len(records),'outcomes':dict(counts),'winner':winner,'five_colour_certificate':upper is not None and upper['status']=='SAT','unit_vertices_if_winner':630 if winner is not None else None,'unit_edges_if_winner':records[-1]['unit_edges'] if winner is not None else None,'full_pair_domain':118828,'family_closed':False,'record_improvement':False,'seconds':time.monotonic()-start}
    save(out/'result.json',result);save(out/'checkpoint.json',{'phase':'COMPLETE','result':result});print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--kissat',type=Path,required=True);ap.add_argument('--drat-trim',type=Path,required=True);ap.add_argument('--controls',type=Path,required=True)
    a=ap.parse_args();run(a.out,a.kissat,a.drat_trim,a.controls)
