"""Independent sum-eight radial face: eight exact univariate profiles."""
from fractions import Fraction as F
from math import comb
from polys import cast,symbol,need
WINDOW=F(1,2**16)

def coefficients(p,var):
 degree=max((dict(m).get(var,0) for m in p.terms),default=-1);out=[F(0)]*(degree+1)
 for m,v in p.terms.items():
  need(v[1]==0 and all(name==var for name,_ in m),'whole real univariate');out[dict(m).get(var,0)]+=v[0]
 return out

def majorant(p,var='eta',window=WINDOW):
 c=coefficients(p,var)
 if not c:return {'zero':True,'coefficients':[]}
 val=next(i for i,x in enumerate(c) if x);tail=sum((abs(c[i])*window**(i-val) for i in range(val+1,len(c))),F(0));low=c[val]-tail
 return {'zero':False,'valuation':val,'degree':len(c)-1,'coefficients':list(map(str,c)),'leading':str(c[val]),'absolute_tail':str(tail),'lower_after_factoring':str(low),'strict_positive':low>0}

def radial():
 eta,t=symbol('eta'),symbol('t');a=1-eta;penalty=F(39,5);rows=[]
 for m in range(1,9):
  k=8-m;integrand=(1+a-a*t)**k*(1+a-a*t-F(8,m)*a*a*t)**m
  O=9*integrand.integral('t').substitute({'t':1});P=(1+F(8,m)*a)**m
  d=F(64*(m-1),m)-F(256*(m-1)*(m-2),3*m*m)
  defect=d*a**3;residual=O-P-8*(1-a**9)-penalty*defect;cert=majorant(residual)
  need(cert.get('zero') or cert['strict_positive'],'complete radial profile '+str(m))
  rows.append({'free_count':m,'floor_count':k,'penalty':str(penalty),'whole_scaled_gap':(O-P).record(),'whole_Newton_defect':defect.record(),'whole_residual':residual.record(),'interval_certificate':cert})
 return rows

if __name__=='__main__':
 import json
 r=radial();print(json.dumps(r,sort_keys=True,separators=(',',':')))
 for x in r:print(x['free_count'],x['interval_certificate'].get('valuation'),x['interval_certificate'].get('lower_after_factoring'))
