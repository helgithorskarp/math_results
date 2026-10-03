"""Every affine basis in both table/sector definitions; full original row closure."""
from pathlib import Path
import json,sys
from fractions import Fraction as F
from exact import need,canon,digest
from model import table,sectors,original_rows
from check import rebuild,structure,forms

def run(w):
 allrows=[];entries=0;form_entries=0
 for case in w['cases']:
  n=case['n'];d=len(case['names']);probes=[[0]*d]
  for i in range(d):
   for val in (F(1),F(-2,3)):
    x=[0]*d;x[i]=val;probes.append(x)
  for ordinal,v in enumerate(probes):
   c=dict(case,values=v);a=table(c);b,P=rebuild(c);need(a==b,'EVERY affine table entry');entries+=len(a)**2
   # Arbitrary affine probes need stars and empty rows, not positivity/positive deficits.
   N=2**n-n-1;s=2**(n-1)-n
   C=lambda nn,k:P[nn][k]if 0<=k<=nn else 0
   E=[N-s-sum(C(n-t,u)*b[t-1][u-1]for u in range(1,n-1))for t in range(1,n-1)];loop=N-sum(C(n,t)*E[t-1]for t in range(1,n-1));orig=original_rows(n,a)
   need(orig['empty_rows']==list(map(str,E))and orig['empty_loop']==str(loop),'EVERY affine original empty row/loop')
   ps=sectors(n,a)
   for j,p in enumerate(ps):
    layers,g,L,U=forms(n,b,P,j);need(layers==p['layers']and g==p['g']and L==p['lower']and U==p['upper'],'EVERY affine physical entry');form_entries+=2*len(g)**2
    need(all(not sum(L[t][u]*z[u]for u in range(len(g)))for z in p['kernels']for t in range(len(g))),'full affine constant kernels')
   record=dict(n=n,ordinal=ordinal,values=list(map(str,v)),table=[[str(z)for z in row]for row in a],original=orig,physical=[dict(j=p['j'],lower=[[str(z)for z in row]for row in p['lower']],upper=[[str(z)for z in row]for row in p['upper']])for p in ps]);allrows.append(record)
 return dict(probe_count=len(allrows),table_entries=entries,physical_entries=form_entries,rows=allrows)
if __name__=='__main__':
 w=json.loads(Path(__file__).with_name('WITNESS.json').read_text());v=run(w);Path(sys.argv[1]).write_bytes(canon(v));print(json.dumps({'complete':True,'sha256':digest(v),'bytes':len(canon(v)),'probes':v['probe_count'],'table_entries':v['table_entries'],'physical_entries':v['physical_entries']}))
