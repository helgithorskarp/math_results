"""Unrestricted finite classification; every SAT row retains its literal model."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,time
from encode import catalog,decode,universal,CROSS

def run(catalog_path,output):
 from pysat.solvers import Cadical300
 output=Path(output);output.mkdir(parents=True,exist_ok=False)
 records=catalog(catalog_path);variables,rows=universal();blocked=[];start=time.monotonic()
 (output/'STARTED.json').write_text(json.dumps(dict(cores=len(records),scope='complete order-11 catalog, one disjoint blue K4'))+'\n')
 with (output/'witnesses.u48le').open('wb') as out,Cadical300(bootstrap_with=rows) as solver:
  for i,record in enumerate(records):
   known=decode(record)
   assumptions=[(1 if known[p] else -1)*variables[p] for p in combinations(range(11),2)]
   if solver.solve(assumptions=assumptions):
    model={abs(x):x>0 for x in solver.get_model()}
    word=sum(int(model[variables[p]])<<j for j,p in enumerate(CROSS))
   else:blocked.append(i);word=(1<<48)-1
   out.write(word.to_bytes(6,'little'))
 (output/'BLOCKED_IDS.txt').write_text(''.join(f'{i}\n' for i in blocked))
 result=dict(status='REQUIRES_WITNESS_AND_UNSAT_CHECKS',cores=len(records),sat=len(records)-len(blocked),blocked=blocked,witness_bytes=(output/'witnesses.u48le').stat().st_size,witness_sha256=hashlib.sha256((output/'witnesses.u48le').read_bytes()).hexdigest())
 (output/'CLASSIFICATION.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 return dict(result,seconds=time.monotonic()-start)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('output');a=p.parse_args();print(json.dumps(run(a.catalog,a.output),indent=2))
