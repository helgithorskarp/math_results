"""Independent complete Q[q,k] dual identities and positive-cone certificates."""
from fractions import Fraction as F
from linear import need,canonical,digest
from sparse import poly,add,mul,scale,power,evalp,serial,x,y,e

def subtract(a,b):return add(a,scale(b,-1))
def substitute(p,q,k):
 out={}
 for(i,j),v in p.items():out=add(out,scale(mul(power(q,i),power(k,j)),v))
 need(len(out)<=512,'fixed512term exact sparse guard')
 return out

def polynomials():
 q,k=x,y;G=add(power(q,2),scale(q,7),poly(8),scale(k,-2));ell=add(scale(q,5),poly(4),scale(k,-1));T=mul(q,G);V=subtract(mul(ell,G),mul(scale(q,8),add(scale(q,3),poly(4))))
 B=add(mul(q,add(mul(subtract(q,k),add(scale(q,3),poly(4))),scale(k,3))),scale(k,2));A=subtract(add(mul(add(scale(k,2),poly(1)),power(q,2)),mul(k,q)),scale(k,2));C=mul(ell,subtract(poly(1),k));D=subtract(mul(power(q,2),mul(T,V)),scale(power(B,2),4));aa=mul(scale(q,2),add(mul(V,A),scale(mul(B,C),2)));bb=scale(add(mul(power(q,2),mul(T,C)),scale(mul(B,A),2)),2)
 S=add(mul(mul(q,add(q,poly(1))),add(scale(q,3),poly(5))),scale(add(q,poly(1)),6),scale(k,-4));dd=subtract(mul(S,D),scale(add(mul(aa,q),mul(bb,subtract(scale(q,2),k))),4));return {'G2':G,'ell':ell,'T2':T,'V2':V,'Bq':B,'Aq':A,'C':C,'Dn':D,'an':aa,'bn':bb,'S2':S,'dn':dd}

def positive(p,q,k,label):
 out=substitute(p,q,k);need(out.get((0,0),F(0))>0 and all(v>=0 for v in out.values()),'ALL positive shifted coefficients '+label)
 return {'label':label,'substitution_q':serial(q),'substitution_k':serial(k),'all_coefficients':serial(out),'monomials':len(out),'strict_constant':out[(0,0)],'whole_sha256':digest(serial(out))}

def audit():
 from dual import data
 ps=polynomials();original=[positive(ps[name],add(poly(6),scale(x,3),y),add(poly(2),x),'original q>=3k '+name)for name in['V2','Dn','dn']]
 need([r['monomials']for r in original]==[10,45,78],'complete original133 coefficient census')
 numeric=[]
 for q,k in[(6,2),(74,15),(125,24)]:
  z={name:evalp(p,q,k)for name,p in ps.items()};a=data(q,k)
  need(z['T2']==2*a['T']and z['V2']==2*a['V']and z['Bq']==-q*a['B']and z['Aq']==q*a['A'],'all counted numerator clearings')
  need(z['Dn']==4*q*q*a['D']and z['an']==z['Dn']*a['a']and z['bn']==z['Dn']*a['b']and z['dn']==2*(3*q+5)*z['Dn']*a['d'],'all denominator/derivative identities')
  numeric.append({'q':q,'k':k,'cleared':z,'calibration_only':True})
 # Independent proposed enlargement: all k>=4,q>=k plus k1/2/3,q>=4 faces.
 broad=[]
 for name in['V2','Dn','dn']:broad.append(positive(ps[name],add(poly(4),x,y),add(poly(4),x),'NEW k>=4,q>=k '+name))
 for k in[1,2,3]:
  for name in['V2','Dn','dn']:broad.append(positive(ps[name],add(poly(4),x),poly(k),'NEW k'+str(k)+',q>=4 '+name))
 return {'original_coefficients':original,'new_original_domain_coefficients':broad,'all_unshifted_polynomials':{name:serial(p)for name,p in ps.items()},'denominator_numeric_calibrations':numeric,'scope':'Whole polynomial identities/positive coefficients prove every quantified integer. Three numeric samples corroborate, not extrapolation. New domain all1<=k<=q,q>=4; original Gram counting and lower orientation bridges are proved in PROOF.md.'}

if __name__=='__main__':
 import json,signal
 def alarm(*args):raise TimeoutError('fixed60s exact coefficients; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
