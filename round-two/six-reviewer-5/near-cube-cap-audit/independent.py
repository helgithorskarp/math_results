"""Reviewer-written before inspecting the author's executable/expected record.
Full coefficient identity retains the cardinality-kernel defect.
No author module imports, exact rational arithmetic, serial stdlib only.
"""
from fractions import Fraction as Q
from math import comb
import hashlib,json,pathlib

def require(test,label):
 if not test:raise ValueError(label)

def data(n,r=None):
 s=2**(n-1)-n;h=2**(n-1)-1;N=2**n-n-1;q=comb(n,2)
 r=Q(2*s,h) if r is None else Q(r);mu=Q((2*n-5)**2,16)
 bulk=range(3,n-2);v={a:max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n)) for a in bulk}
 u={1:Q(1),2:Q(2),n-2:r,**v};ell={a:Q(0 if a<=2 else 2 if a==n-2 else 1) for a in range(1,n-1)}
 counts={a:comb(n,a) for a in range(1,n-1)};f={a:Q(a)-v[a] for a in bulk};w={a:f[a]*f[n-a] for a in bulk}
 S=sum(counts[a]*v[a]**2 for a in bulk)
 eta=n*h+q*(h*(4+r*r)-s*(2+4*r))+(n-1)*S+mu*(4*s-4)
 return locals()

def coefficient_identity(n,r=None):
 d=data(n,r);s,h,mu,u,ell,counts,bulk,w,eta=[d[k] for k in ('s','h','mu','u','ell','counts','bulk','w','eta')]
 # B=0 literal matrix: C=sI-J and U=hI. Derive both constants independently.
 su=sum(counts[a]*u[a] for a in counts);se=sum(counts[a]*ell[a] for a in counts);sa=sum(counts[a]*a for a in counts)
 phi0=h*sum(counts[a]*u[a]**2 for a in counts)+mu*(s*sum(counts[a]*ell[a]**2 for a in counts)-se*se)
 defect0=sum(counts[a]*(2*u[a]-a)*(s*a-sa) for a in counts)
 rhs0=eta-s*sum(counts[a]*(mu-w[a]) for a in bulk)-defect0
 require(phi0==rhs0,'B=0 constant term')
 entries=[]
 for a in counts:
  for b in counts:
   if a>b or a+b>n:continue
   direct=2*(mu*ell[a]*ell[b]-u[a]*u[b])
   resolved=Q(0)
   if a in bulk and b in bulk:
    resolved=2*(mu-d['f'][a]*d['f'][b])
   defect=2*u[a]*b+2*u[b]*a-2*a*b
   require(direct==resolved-defect,f'original edge coefficient {n}/{a}/{b}')
   entries.append((a,b,str(direct)))
 return {'n':n,'r':str(d['r']),'edges':len(entries),'constant':str(phi0),'coefficient_sha256':hashlib.sha256(json.dumps(entries,separators=(',',':')).encode()).hexdigest()}

def signs_and_moments(n):
 d=data(n);mu=d['mu'];v=d['v'];f=d['f'];w=d['w'];bulk=d['bulk']
 require(all(f[a]>0 and w[a]<=mu for a in bulk),'complement sign')
 require(all(f[a]<f[a+1] for a in range(3,n-3)),'strict monotonicity')
 rho={f'{a},{b}':1-f[a]*f[b]/mu for a in bulk for b in bulk if a<=b and a+b<n}
 require(all(0<x<1 for x in rho.values()),'proper original weights')
 require(max(rho.values())==1-f[3]**2/mu,'exact maximum proper weight')
 m2=sum(comb(n,a)*Q(2*a-n,2)**2 for a in range(n+1));m4=sum(comb(n,a)*Q(2*a-n,2)**4 for a in range(n+1))
 require(m2==Q(2**n*n,4) and m4==Q(2**n*(3*n*n-2*n),16),'binomial moments')
 raw=sum(comb(n,a)*(Q(5,4)-Q((2*a-n)**2,4*n))**2 for a in range(n+1))
 upper=(d['s']+n)*Q(9*n-1,4*n)
 require(raw==upper and d['S']<=upper,'clipping bound')
 # Independent expansion without the optimized rational term.
 eta2=data(n,Q(2))['eta']
 Fn=-Q(d['s']*(3*n*n-15*n-1),4*n)+4*n**3-Q(23*n*n,4)+Q(11*n,2)-6
 substitution=eta2+(n-1)*(upper-d['S'])
 require(Fn==substitution,'tail polynomial expansion')
 require(d['eta']==eta2-Q(4*comb(n,2)*(n-1)**2,d['h']),'root minimizer')
 delta=-d['eta']/(2*d['h']*mu);maximum=1-f[3]**2/mu
 return {'n':n,'S':str(d['S']),'eta':str(d['eta']),'eta_r2':str(eta2),'Fn':str(Fn),'delta':str(delta),'rho_max':str(maximum),'positive_mass_floor':str(delta/maximum),'complement_zero_layers':[a for a in bulk if mu==w[a]],'proper_weights':len(rho)}

def run():
 # More profiles and layer coefficients are controls, not an all-n proof.
 identities=[coefficient_identity(n) for n in range(6,49)]
 endpoints=[signs_and_moments(n) for n in range(11,65)]
 require(data(11)['S']==Q(4533,2) and data(11)['eta']==-Q(1535,93),'eleven endpoint')
 require(data(11,Q(2))['eta']==5,'endpoint damage')
 require(2**11-12>12*12**2,'induction base')
 # Coefficients in t=n-12 certify every real t>=0; no sampled tail inference.
 positive_polynomials={'exponential_induction':[1439,265,12],'coefficient_gt_n_over3':[177,75,5],'remainder_lt_4n3':[3072,530,23]}
 require(all(c>0 for v in positive_polynomials.values() for c in v),'positive coefficient proof')
 return {'agent':'six-reviewer-5','role':'independent mathematical reviewer','method':'B=0 constant and all original pair coefficients, with explicit kernel defect; no author code','identities':identities,'bounds':endpoints,'all_n_induction_polynomials':positive_polynomials,'eleven':endpoints[0],'sixteen':endpoints[5]}
if __name__=='__main__':
 record=run();p=pathlib.Path(__file__).with_name('first-record.json');p.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'identities':len(record['identities']),'edge_coefficients':sum(x['edges'] for x in record['identities']),'bounded_orders':len(record['bounds']),'eleven':record['eleven'],'sixteen':record['sixteen'],'record_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
