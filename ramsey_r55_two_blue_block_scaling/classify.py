"""Retain a literal witness for every positive core, requiring full coverage."""
from pathlib import Path
from itertools import combinations
import argparse,json,time,hashlib
import model

def run(catalog,output,seconds=1800):
 from pysat.solvers import Cadical300
 output=Path(output);output.mkdir(parents=True,exist_ok=False)
 records=model.catalog(catalog);variables,clauses=model.universal();start=time.monotonic();blocked=[]
 (output/'STARTED.json').write_text(json.dumps(dict(scope='all 546356 cores, complete two-blue-block extension',global_envelope_seconds=seconds),indent=2)+'\n')
 with Cadical300(bootstrap_with=clauses) as solver,(output/'witnesses.u112le').open('wb') as out:
  for i,record in enumerate(records):
   known=model.decode(record);assumptions=[(1 if known[p] else -1)*variables[p] for p in combinations(range(11),2)]
   verdict=solver.solve(assumptions=assumptions)
   if type(verdict) is not bool:raise RuntimeError('nonterminal solver response')
   if verdict:
    values={abs(x):x>0 for x in solver.get_model()}
    word=sum(int(values[variables[p]])<<j for j,p in enumerate(model.FREE))
   else:blocked.append(i);word=(1<<112)-1
   out.write(word.to_bytes(14,'little'))
   if time.monotonic()-start>seconds:raise RuntimeError('incomplete classification; global resource envelope exceeded')
 (output/'BLOCKED_IDS.txt').write_text(''.join(f'{i}\n' for i in blocked))
 result=dict(status='REQUIRES_INDEPENDENT_WITNESS_AND_PROOF_CHECKS',cores=len(records),sat=len(records)-len(blocked),blocked=blocked,witness_bytes=(output/'witnesses.u112le').stat().st_size,witness_sha256=hashlib.sha256((output/'witnesses.u112le').read_bytes()).hexdigest(),seconds=time.monotonic()-start)
 (output/'CLASSIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('output');p.add_argument('--seconds',type=float,default=1800);a=p.parse_args();print(json.dumps(run(a.catalog,a.output,a.seconds),indent=2))
