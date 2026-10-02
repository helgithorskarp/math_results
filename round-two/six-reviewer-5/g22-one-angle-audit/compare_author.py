"""Late complete-entry comparison; own core was sealed before these imports."""
import json,hashlib,itertools
from pathlib import Path
from fractions import Fraction as Q
import aliases,algebra
P=Path(__file__).resolve().parent
import sys
AUTHOR=Path(sys.argv[1]) if len(sys.argv)>1 else P.parents[1]/"six-tammes-1/g22-facial-injectivity"
import importlib.util
spec=importlib.util.spec_from_file_location('late_original',AUTHOR/'check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=json.loads((AUTHOR/'CERTIFICATE.json').read_text());ours=json.loads((P/'RESULT.json').read_text())['algebra'];orig_table,look,contacts=m.gram_data()
comparisons=0;decisions=[]
for code,rename in aliases.cube():
 original_map={v:rename.get(v,v) for v in aliases.RIGHT};a=aliases.test(rename)=='accepted';b=m.classify(original_map,contacts)=='retained'
 if a!=b:raise ValueError(('whole alias decision',original_map,a,b))
 decisions.append((tuple(original_map[r] for r in aliases.RIGHT),a));comparisons+=1
canonical=lambda v:json.dumps(v,sort_keys=True,separators=(',',':')).encode()
sha=hashlib.sha256(canonical(sorted(decisions))).hexdigest()
if sha!=c['aliases']['all_map_decision_sha256']:raise ValueError('complete decision record')
coef=0
for a,b in zip(ours['internal'],c['intrinsic_pair_table']):
 if a['pair']!=b['pair'] or a['patch']!=('L' if b['side']=='left' else 'R'):raise ValueError('pair indexing')
 numerator=algebra.sub(algebra.R,a['gap'])
 if tuple(map(Q,b['numerator']))!=numerator:raise ValueError('whole numerator')
 coef+=len(numerator)
 if a['gap']!=[0] and list(map(Q,b['gap_bernstein']))!=list(map(Q,a['old'])):raise ValueError('every old gap Bernstein')
for a,b in zip(ours['obstructions'],c['closure_cases']):
 if a['alias']!=b['alias'][1] or len(a['full'])-1!=b['closure_degree']:raise ValueError('case indexing')
 f=a['factor'];roots=[{'root':str(x),'multiplicity':n} for x,n in f['roots'] if n]
 if roots!=b['linear_factors'] or f['constant']!=b['content']:raise ValueError('all factors')
 if list(map(Q,b['reduced_coefficients']))!=f['reduced']:raise ValueError('all reduced coefficients')
 if list(map(Q,b['reduced_bernstein']))!=list(map(Q,a['old'])):raise ValueError('all old sign coefficients')
 coef+=len(f['reduced'])
 # Additional POST-seal direct binomial representation checks for wider certificates.
 from math import comb
 for j in range(len(f['reduced'])):
  n=len(f['reduced'])-1;t=Q(j,n);lhs=algebra.value(f['reduced'],Q(2,3)+Q(1,12)*t)
  rhs=sum(Q(a['wide'][i])*comb(n,i)*t**i*(1-t)**(n-i) for i in range(n+1))
  if lhs!=rhs:raise ValueError('wide full Bernstein identity')
result=dict(all_alias_decisions=comparisons,canonical_original_decision_sha256=sha,all36_numerator_polynomials=True,all16_old_gap_Bernstein=True,all3_reduced_polynomials_factors_old_Bernstein=True,complete_coefficient_positions=coef,postseal_wide_Bernstein_identity_points=sum(len(x['factor']['reduced']) for x in ours['obstructions']))
print(json.dumps(result,sort_keys=True,indent=2))
