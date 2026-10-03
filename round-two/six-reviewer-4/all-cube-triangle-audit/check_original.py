"""Exact, CAS-free binding of every certificate entry to all original row sums."""
from pathlib import Path
import sys,json
from rational import R,H,Q
from sectors import params,matrices
from polycheck import pair
p=params(H,Q);forms=matrices(p)
# Whole cross forms, not just a selected subblock.
for name,groups in [('even',[[0,1,2],[3,4]]),('odd',[[0],[1,2],[3]])]:
 gm,S=forms[name]
 for a,g in enumerate(groups):
  for b,k in enumerate(groups):
   if a!=b:
    for i in g:
     for j in k:
      if not S[i][j].iszero():raise ValueError('cross-sector cancellation')
for i in range(2):
 for j in range(2):
  if not(forms['even'][1][i+3][j+3]-forms['odd'][1][i+1][j+1]).iszero():raise ValueError('even/odd trace mismatch')
def original(name):
 if name in ['mu','alpha','beta']:return [[p[name]]]
 if name in ['old_plus','old_minus']:return [[p['N']-1-(2*Q if name=='old_plus'else 6*H)]]
 if name=='odd_old':return [[p['N']-1-forms['odd'][1][0][0]/forms['odd'][0][0]]]
 if name=='odd_mean':return [[p['N']-1-forms['odd'][1][3][3]/forms['odd'][0][3]]]
 source,ind={'leaf':('leaf',[0,1]),'standard':('standard',[0,1,2,3]),'even_old':('even',[0,1,2]),'trace':('even',[3,4])}[name];gm,S=forms[source]
 return [[(p['N']-1 if i==j else R(0))-S[r][c]/gm[r]for j,c in enumerate(ind)]for i,r in enumerate(ind)]
def metric(name):
 if name in ['mu','alpha','beta','old_plus','old_minus']:return [R(1)]
 if name in ['odd_old','odd_mean']:return [forms['odd'][0][0 if name=='odd_old'else 3]]
 source,ind={'leaf':('leaf',[0,1]),'standard':('standard',[0,1,2,3]),'even_old':('even',[0,1,2]),'trace':('even',[3,4])}[name]
 return [forms[source][0][i]for i in ind]
def check(r):
 gm=metric(r['name'])
 if len(gm)!=len(r['metric']):raise ValueError('complete original metric')
 for x,y in zip(gm,r['metric']):
  n,d=pair(y)
  if not x.same_pair(n,d):raise ValueError('original metric mismatch')
 A=original(r['name']);count=0
 if len(A)!=len(r['original'])or any(len(x)!=len(y)for x,y in zip(A,r['original'])):raise ValueError('dimension')
 for row,expected in zip(A,r['original']):
  for x,y in zip(row,expected):
   n,d=pair(y)
   if not x.same_pair(n,d):raise ValueError('original entry mismatch')
   count+=1
 return dict(name=r['name'],original_entries=count,whole_cross_sector_zero=True,even_odd_trace_binding=True)
if __name__=='__main__':print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())),sort_keys=True))
