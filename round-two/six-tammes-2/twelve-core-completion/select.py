"""Floating selection of a proposed fixed-root exact certificate.

NumPy is a discovery dependency only. Every proposed literal must be
accepted by check.py, which uses no floating-point operation or NumPy.
Actual author six-tammes-2, researcher.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import json
import numpy as np

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'INPUT.json').read_text())
t=float('0.592605902925073778096424922332755')
def evaluate(poly):
    result=0.
    for c in reversed(poly):result=result*t+float(Fraction(c))
    return result
V=np.array([[evaluate(poly) for poly in row] for row in data['vectors']])
H=(1-t)*np.eye(3)+t*np.ones((3,3))
normal=np.array([evaluate(poly) for poly in data['cap_center']])
bound=float(Fraction(data['cap_bound']))
q=np.linalg.solve(np.array([H@V[i] for i in (8,9,11)]),np.full(3,t))
other=np.array([evaluate(poly) for poly in data['alternate_last']])
core=data['core_labels'];index_chars='abcdefghijklmn'
cases=[('cut',core+['cut'],np.array([H@V[i] for i in core]+[H@normal]),
        np.array([t]*12+[bound]),[V[3],V[13],q],.99),
       ('original-fourteen',core+[3,13],np.array([H@V[i] for i in core+[3,13]]),
        np.full(14,t),[V[14],other],.75),
       ('other-fourteen',core+[3,'q'],np.array([H@V[i] for i in core]+[H@V[3],H@q]),
        np.full(14,t),[V[14],other],.75)]
plan={'format':'fixed-twelve-three-completion-plan-v1','cases':[]}
for name,names,rows,rhs,units,short in cases:
    tokens=[]
    for inds in combinations(range(len(rows)),3):
        matrix=rows[list(inds)]
        if abs(float(np.linalg.det(matrix)))<1e-10:
            tokens.append('S');continue
        point=np.linalg.solve(matrix,rhs[list(inds)])
        residual=rows@point-rhs;j=int(np.argmax(residual))
        if float(residual[j])>1e-8:
            tokens.append('I'+index_chars[j]);continue
        if float(point@H@point)<short-1e-8:
            tokens.append('N');continue
        matches=[i for i,v in enumerate(units) if np.linalg.norm(point-v)<1e-7]
        if len(matches)!=1:raise ValueError('unresolved floating instruction, not a certificate')
        tokens.append('U'+index_chars[matches[0]])
    plan['cases'].append({'name':name,'labels':names,'tokens':tokens})
(HERE/'PLAN.json').write_text(json.dumps(plan,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps({'status':'proposed_unverified_floating_selection','numpy_version':np.__version__,
                  'case_literal_counts':[len(case['tokens']) for case in plan['cases']],
                  'total_literals':sum(len(case['tokens']) for case in plan['cases'])},sort_keys=True))
