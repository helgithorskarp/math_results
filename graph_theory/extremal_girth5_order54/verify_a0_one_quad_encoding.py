"""Truth-table controls for weighted sequential-counter inputs used by the SAT model."""
import itertools,json,hashlib
from pysat.formula import IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver
patterns=[(1,2,3),(1,1,2),(-1,2,2),(-1,-2,3,3),(1,1,2,2,3,3)]
checked=[]
for lits in patterns:
 for bound in range(len(lits)+1):
  pool=IDPool(start_from=4);cnf=CardEnc.equals(lits=list(lits),bound=bound,vpool=pool,encoding=EncType.seqcounter)
  with Solver(name='g4',bootstrap_with=cnf) as s:
   for bits in itertools.product((0,1),repeat=3):
    want=sum(bits[abs(x)-1] if x>0 else 1-bits[abs(x)-1] for x in lits)==bound
    got=s.solve(assumptions=[i+1 if b else -(i+1) for i,b in enumerate(bits)])
    if got!=want:raise ValueError((lits,bound,bits))
    checked.append((lits,bound,bits,got))
print(json.dumps({'cardinality_assignments':len(checked),'entry_sha256':hashlib.sha256(json.dumps(checked).encode()).hexdigest(),'negative_literals_and_repeated_variables':True},indent=2))
