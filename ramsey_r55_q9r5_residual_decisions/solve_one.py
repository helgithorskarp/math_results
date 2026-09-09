"""Single bounded solver invocation; parent supplies the wall-clock limit."""
from pathlib import Path
import ctypes
import hashlib
import json
import sys
import time
from pysat.solvers import Cadical300
from encode import catalogue, formula, dimacs, decode

def main():
    data, output, index = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    row = catalogue(data)[index]
    _, _, clauses = formula(row)
    cnf = dimacs(clauses)
    (output/'input.cnf').write_bytes(cnf)
    t0 = time.monotonic()
    solver = Cadical300(with_proof=True, use_timer=True)
    solver.configure({'seed':0})
    for clause in clauses:
        solver.add_clause(clause)
    solver.conf_budget(200000)
    answer = solver.solve_limited()
    result = {'index':index, 'task':f'bo1-q9-r5-c{index:06d}',
              'cnf_sha256':hashlib.sha256(cnf).hexdigest(), 'clauses':len(clauses),
              'solver_status':{True:'SAT',False:'UNSAT',None:'UNKNOWN'}[answer],
              'seconds':time.monotonic()-t0,'statistics':solver.accum_stats()}
    if answer is True:
        result['residual_edgeword'] = decode(row,solver.get_model())
    elif answer is False:
        # Preserve binary data exactly. PySAT's get_proof() uses strip(), which
        # is not safe on a binary proof. Flush C stdio, then read raw bytes.
        if ctypes.CDLL(None).fflush(None) != 0:
            raise RuntimeError('C stdio flush failed')
        solver.prfile.seek(0)
        proof = solver.prfile.read()
        (output/'proof.raw.drat').write_bytes(proof)
        # An explicit empty-clause record is a claim, not trusted evidence.
        # The independent checker must verify this entire completed stream.
        proof += b'a\x00'
        (output/'proof.drat').write_bytes(proof)
        result['proof_sha256'] = hashlib.sha256(proof).hexdigest()
        result['proof_bytes'] = len(proof)
    solver.delete()
    (output/'solver.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__ == '__main__':
    main()
