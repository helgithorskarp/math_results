"""Standard-library checker, no CAS/author arithmetic imports.
Complete coefficient substitution; own rational entry identities; complete
Gaussian grids from independently computed separate-degree bounds.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json,signal
from ring import R,shifted,record as prec
from forms import arrow,tests,model
from linear import need,digest,canonical

def poly(record):
 need(isinstance(record,list) and len(record)<=512,'compact512 input');out={}
 for item in record:
  need(type(item)==list and len(item)==4 and all(type(k)==int and 0<=k<=180 for k in item[:3]),'degree/domain/type');k=tuple(item[:3]);need(k not in out,'unique monomial');v=F(item[3]);need(v!=0,'nonzero coefficient');out[k]=int(v) if v.denominator==1 else v
 return out

def val(p,x):
 powers=[[1] for _ in range(3)]
 for j in range(3):
  for _ in range(max((k[j] for k in p),default=0)):powers[j].append(powers[j][-1]*x[j])
 return sum(v*powers[0][k[0]]*powers[1][k[1]]*powers[2][k[2]] for k,v in p.items())
def degree(p):return tuple(max((k[j] for k in p),default=0) for j in range(3))
def facts(data,boundary):
 c=F(data['constant']);need(c>0,'positive rational factor constant');out=[]
 for f in data['factors']:
  p=poly(f['original']);t=poly(f['shifted']);need(shifted(p,boundary)==t,'ENTIRE original-to-quadrant coefficient substitution');need(t.get((0,0,0),0)>0 and all(v>0 for v in t.values()),'ENTIRE coefficient-positive domain factor');power=f['power'];need(type(power)==int and 1<=power<=180,'factor exponent');out.append((p,t,power))
 return c,out

def actual_factor(c,ff):
 z=R(c)
 for p,_,k in ff:z*=R(p)**k
 return z

def gaussian(A):
 B=[list(map(F,row)) for row in A];z=F(1);n=len(A)
 for j in range(n):
  p=next((i for i in range(j,n) if B[i][j]),None)
  if p is None:return F(0)
  if p!=j:B[p],B[j]=B[j],B[p];z=-z
  a=B[j][j];z*=a
  for i in range(j+1,n):
   k=B[i][j]/a
   for h in range(j+1,n):B[i][h]-=k*B[j][h]
 return z

def check(path,name,order):
 data=json.loads(Path(path).read_text());claimed=data.pop('whole_sha256');need(digest(data)==claimed,'ENTIRE generated record fingerprint');boundary=data['boundary'];need(boundary is False and data.get('domain')=='r=2+u,l=1,q=8+4u+w;u,w>=0','EXACT single-pendant domain');case=next(x for x in data['tests'][name] if x['order']==order);p=poly(case['original_numerator']);shift=poly(case['numerator']);need(shifted(p,boundary)==shift,'ENTIRE numerator substitution');need(shift.get((0,0,0),0)>0 and all(v>0 for v in shift.values()),'ENTIRE leading numerator positivity');den=facts(case['denominator'],boundary);remove=facts(case['removed'],boundary)
 rr=R({(1,0,0):1});ll=R(1);qq=R({(0,0,1):1});A=tests(rr,ll,qq)[name];A=[row[:order] for row in A[:order]];B=[];clearings=[]
 for i,row in enumerate(case['polynomial_matrix']):
  clear=facts(case['positive_row_clearings'][i],boundary);clearings.append(clear);multiplier=actual_factor(*clear);B.append([])
  for j,x in enumerate(row):
   old=poly(x['original']);new=poly(x['shifted']);need(shifted(old,boundary)==new,'EVERY whole cleared entry substitution');need(multiplier*A[i][j]==R(old),'EVERY cleared entry identity in own rational ring');B[-1].append(new)
 def factor_degree(ff):return [sum(k*degree(p)[j] for _,p,k in ff) for j in range(3)]
 def factor_value(data,x):
  z=data[0]
  for _,p,k in data[1]:z*=val(p,x)**k
  return z
 degrees=[sum(max(degree(p)[j] for p in row) for row in B) for j in range(3)];right=[degree(shift)[j]+factor_degree(remove[1])[j] for j in range(3)];clearing_degrees=[sum(factor_degree(f[1])[j] for f in clearings) for j in range(3)];factor_degrees=[a+b for a,b in zip(factor_degree(den[1]),factor_degree(remove[1]))];bounds=[max(x,y,z,w) for x,y,z,w in zip(degrees,right,clearing_degrees,factor_degrees)];count=(bounds[0]+1)*(bounds[1]+1)*(bounds[2]+1);need(max(bounds)<=180 and count<=32768,'fixed180degree/32768grid guard');hash_rows=[]
 for x in product(*(range(d+1) for d in bounds)):
  observed=gaussian([[val(p,x) for p in row] for row in B]);expected=val(shift,x)*remove[0]
  for _,p,k in remove[1]:expected*=val(p,x)**k
  need(observed==expected,'EVERY complete Gaussian determinant identity point');hash_rows.append(observed)
  cleared=F(1)
  for f in clearings:cleared*=factor_value(f,x)
  need(cleared==factor_value(den,x)*factor_value(remove,x),'EVERY complete denominator/clearing product identity point')
 return {'boundary':boundary,'name':name,'order':order,'coefficient_count':len(shift),'whole_numerator':digest(prec(shift)),'bounds':bounds,'all_grid_points':count,'whole_grid':digest(hash_rows),'every_entry_identity':order*order,'whole_certificate':claimed}

def main():
 p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('name');p.add_argument('order',type=int);a=p.parse_args();print(json.dumps(canonical(check(a.path,a.name,a.order)),sort_keys=True,separators=(',',':')))
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s checker phase')));signal.alarm(60);main()
